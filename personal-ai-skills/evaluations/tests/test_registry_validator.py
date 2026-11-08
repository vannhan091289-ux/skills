"""Synthetic contract tests; never import or execute skill source files."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import yaml

VALIDATOR = Path(__file__).resolve().parents[1] / 'validate_library.py'
CORE = ['review-academic-thesis', 'audit-branch-kpi', 'review-code-change']
SUPPORT = ['grammar-checker-vi', 'scientific-thinking-literature-review']
GOV = {'security_policy': 'governance/security-policy.md',
       'quality_gates': 'governance/quality-gates.md',
       'data_classification': 'governance/data-classification.md'}


def put(root, path, text):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def records(root, folder):
    return [{'path': p.relative_to(root).as_posix(),
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted((root / folder).rglob('*')) if p.is_file()]


def fixture(root):
    put(root, 'README.md', '# Synthetic skill library\n')
    for path in GOV.values():
        put(root, path, '# Policy\nSynthetic working rules.\n')
    registry = {'schema_version': 1, 'library': {'name': 'personal-ai-skills', 'version': '1.0.0'},
                'governance': GOV.copy(), 'skills': [], 'adapters': [],
                'governance_files': records(root, 'governance')}
    for name in CORE + SUPPORT:
        folder = 'skills/' + name
        put(root, folder + '/SKILL.md', f'---\nname: {name}\ndescription: Synthetic workflow.\n---\n# Workflow\nRead [rules](references/rules.md).\n')
        put(root, folder + '/LICENSE.txt', 'Copyright synthetic fixture; permissive use.\n')
        for sub in ['references', 'assets', 'scripts', 'tests']:
            put(root, folder + '/' + sub + '/example.txt', 'Useful synthetic example.\n')
        put(root, folder + '/scripts/run_checks.py', 'def validate(value):\n    return value == 1\n')
        put(root, folder + '/tests/test_contract.py', 'import unittest\n\nclass Contract(unittest.TestCase):\n    def test_valid(self):\n        self.assertTrue(True)\n')
        put(root, folder + '/references/rules.md', '# Rules\nValidate evidence.\n')
        registry['skills'].append({'name': name, 'path': folder, 'version': '1.0.0',
                                  'role': 'core' if name in CORE else 'support',
                                  'status': 'STATIC_GO', 'runtime_scope': 'Synthetic static checks only',
                                  'installed_name': None, 'files': records(root, folder)})
    for name in ['chatgpt', 'gemini', 'claude', 'codex']:
        folder = 'adapters/' + name
        mode = 'manual-context' if name in ['chatgpt', 'gemini'] else 'documented-native'
        put(root, folder + '/README.md', '# Adapter\nRead the registry and follow documented instructions.\n')
        manifest = {'schema_version': 1, 'name': name, 'mode': mode, 'runtime_verified': False,
                    'source_registry': '../../registry.yaml', 'instructions': 'README.md',
                    'official_sources': ['https://example.com/docs'], 'required_steps': ['Read governance.']}
        put(root, folder + '/adapter.yaml', yaml.safe_dump(manifest))
        registry['adapters'].append({'name': name, 'path': folder, 'mode': mode,
                                    'runtime_verified': False, 'files': records(root, folder)})
    put(root, 'evaluations/fixtures/fixture-catalog.json', json.dumps({'schema_version': 1, 'classification': 'PUBLIC_SYNTHETIC', 'fixtures': [{'path': 'skills/audit-branch-kpi/assets/example.txt', 'type': 'synthetic-example'}]}))
    put(root, 'evaluations/fixtures/case.json', '{"synthetic": true, "expected": "STATIC_GO"}\n')
    put(root, 'evaluations/reports/result.json', '{"synthetic": true, "passed": true}\n')
    save(root, registry)
    return registry


def save(root, registry):
    put(root, 'registry.yaml', yaml.safe_dump(registry, sort_keys=False))


class RegistryContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert VALIDATOR.is_file(), 'Missing read-only canonical validator implementation'
        spec = importlib.util.spec_from_file_location('canonical_validator', VALIDATOR)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.registry = fixture(self.root)

    def check_bad(self):
        result = self.module.validate(self.root)
        self.assertEqual(result['status'], 'REWORK', result)
        self.assertTrue(result['errors'])
        self.assertTrue(all(isinstance(e, str) for e in result['errors']))

    def refresh(self, category, index=0):
        entry = self.registry[category][index]
        entry['files'] = records(self.root, entry['path'])
        save(self.root, self.registry)

    def test_valid_and_read_only(self):
        before = records(self.root, '.')
        result = self.module.validate(self.root)
        self.assertEqual(result, {'status': 'STATIC_GO', 'errors': [], 'skills_checked': 5, 'adapters_checked': 4})
        self.assertEqual(before, records(self.root, '.'))

    def test_both_preserved_support_skills_are_required(self):
        import shutil
        for name in SUPPORT:
            shutil.rmtree(self.root / 'skills' / name)
        self.registry['skills'] = self.registry['skills'][:3]
        save(self.root, self.registry)
        self.check_bad()

    def test_scripts_outside_registered_surface_are_rejected(self):
        for path in ['rogue.py', 'evaluations/rogue.py', 'governance/rogue.py',
                     'evaluations/tests/test_rogue.py', 'evaluations/opaque']:
            with self.subTest(path=path):
                target = self.root / path
                put(self.root, path, '#!/usr/bin/env python3\nraise RuntimeError("never run")\n')
                self.check_bad()
                target.unlink()
        put(self.root, 'evaluations/executable.dat', 'Opaque data\n')
        (self.root / 'evaluations/executable.dat').chmod(0o755)
        self.check_bad()
        (self.root / 'evaluations/executable.dat').unlink()
        put(self.root, 'evaluations/README.md', '# Evaluation notes\nPublic synthetic evidence.\n')
        self.assertEqual(self.module.validate(self.root)['status'], 'STATIC_GO')

    def test_governance_requires_exact_physical_closure(self):
        put(self.root, 'governance/extra.md', '# Undeclared policy\n')
        self.check_bad()

    def test_fixture_catalog_paths_and_schema(self):
        valid = {'schema_version': 1, 'classification': 'PUBLIC_SYNTHETIC',
                 'fixtures': [{'path': 'skills/audit-branch-kpi/assets/example.txt', 'type': 'synthetic-example'}]}
        import copy
        variants = [None, [], {'schema_version': True}, dict(valid, fixtures=[]),
                    dict(valid, classification=False)]
        for path in ['skills/missing/data.json', 'skills/audit-branch-kpi/assets', '../escape', '/tmp/escape', 'skills\\escape']:
            item = copy.deepcopy(valid)
            item['fixtures'][0]['path'] = path
            variants.append(item)
        for wrong in [None, [], True, 1]:
            item = copy.deepcopy(valid)
            item['fixtures'][0]['type'] = wrong
            variants.append(item)
        for catalog in variants:
            with self.subTest(catalog=catalog):
                put(self.root, 'evaluations/fixtures/fixture-catalog.json', json.dumps(catalog))
                self.check_bad()
        (self.root / 'evaluations/fixtures/fixture-catalog.json').unlink()
        self.check_bad()

    def test_core_resources_cannot_be_todo_placeholders(self):
        import shutil
        for sub in ['references', 'assets', 'scripts', 'tests']:
            with self.subTest(sub=sub):
                self.registry = fixture(self.root)
                folder = self.root / 'skills/review-academic-thesis' / sub
                shutil.rmtree(folder)
                put(self.root, folder.relative_to(self.root).as_posix() + '/placeholder.txt', 'TODO')
                self.refresh('skills')
                self.check_bad()

    def test_core_requires_script_and_test_files_not_only_prose(self):
        import shutil
        for sub in ['scripts', 'tests']:
            with self.subTest(sub=sub):
                self.registry = fixture(self.root)
                folder = self.root / 'skills/review-academic-thesis' / sub
                shutil.rmtree(folder)
                put(self.root, folder.relative_to(self.root).as_posix() + '/explanation.md', '# Explanation\nThese are substantial prose instructions only.\n')
                self.refresh('skills')
                self.check_bad()

    def test_wrong_top_level_types(self):
        for value in [None, [], True, 'wrong', {'schema_version': True}, {'skills': [[1]]}]:
            with self.subTest(value=value):
                put(self.root, 'registry.yaml', yaml.safe_dump(value))
                self.check_bad()

    def test_wrong_field_types_and_duplicates(self):
        import copy
        baseline = copy.deepcopy(self.registry)
        mutations = [('name', []), ('path', {}), ('version', 1), ('role', True),
                     ('status', []), ('runtime_scope', None), ('installed_name', False), ('files', {})]
        for key, value in mutations:
            with self.subTest(key=key):
                self.registry = copy.deepcopy(baseline)
                self.registry['skills'][0][key] = value
                save(self.root, self.registry)
                self.check_bad()
        self.registry = baseline
        self.registry['skills'].append(self.registry['skills'][0])
        save(self.root, self.registry)
        self.check_bad()

    def test_missing_core(self):
        self.registry['skills'] = self.registry['skills'][1:]
        save(self.root, self.registry)
        self.check_bad()

    def test_required_directories_cannot_be_placeholder_only(self):
        import shutil
        for folder in ['skills/review-academic-thesis/scripts', 'evaluations/fixtures', 'evaluations/reports']:
            with self.subTest(folder=folder):
                fixture(self.root)
                shutil.rmtree(self.root / folder)
                put(self.root, folder + '/.gitkeep', '')
                self.registry = yaml.safe_load((self.root / 'registry.yaml').read_text())
                self.refresh('skills')
                self.check_bad()

    def test_symlink_anywhere(self):
        (self.root / 'evaluations/link').symlink_to('/tmp')
        self.check_bad()

    def test_unsafe_declared_paths_and_missing_hash(self):
        entry = self.registry['skills'][0]
        original = entry['files'][0].copy()
        for path in ['../escape', '/tmp/escape', 'skills\\escape', 'skills/review-academic-thesis/../x']:
            with self.subTest(path=path):
                entry['files'][0] = dict(original, path=path)
                save(self.root, self.registry)
                self.check_bad()
        entry['files'][0] = {'path': original['path']}
        save(self.root, self.registry)
        self.check_bad()

    def test_hash_tamper_missing_and_undeclared_files(self):
        file = self.root / self.registry['skills'][0]['files'][0]['path']
        file.write_text('tampered')
        self.check_bad()
        file.unlink()
        self.check_bad()
        fixture(self.root)
        put(self.root, 'skills/review-academic-thesis/scripts/hidden.py', 'raise RuntimeError("MUST NOT RUN")\n')
        self.check_bad()

    def test_duplicate_file_records(self):
        self.registry['skills'][0]['files'].append(self.registry['skills'][0]['files'][0])
        save(self.root, self.registry)
        self.check_bad()

    def test_adapter_claim_and_source_registry(self):
        p = 'adapters/chatgpt/adapter.yaml'
        for key, value in [('runtime_verified', True), ('runtime_verified', 0),
                           ('name', 'codex'), ('mode', 'native'), ('source_registry', '../registry.yaml'),
                           ('instructions', '../README.md')]:
            with self.subTest(key=key, value=value):
                self.registry = fixture(self.root)
                manifest = yaml.safe_load((self.root / p).read_text())
                manifest[key] = value
                put(self.root, p, yaml.safe_dump(manifest))
                self.refresh('adapters')
                self.check_bad()

    def test_missing_adapter_and_governance_wrong_mapping(self):
        self.registry['adapters'].pop()
        save(self.root, self.registry)
        self.check_bad()
        self.registry = fixture(self.root)
        self.registry['governance']['quality_gates'] = 'governance/security-policy.md'
        save(self.root, self.registry)
        self.check_bad()

    def test_frontmatter_and_local_link_closure(self):
        p = 'skills/review-academic-thesis/SKILL.md'
        cases = ['no frontmatter', '---\nname: []\ndescription: ok\n---\n',
                 '---\nname: review-academic-thesis\ndescription: true\n---\n',
                 '---\nname: review-academic-thesis\ndescription: ok\n---\n[escape](../../registry.yaml)',
                 '---\nname: review-academic-thesis\ndescription: ok\n---\n[missing](missing.md)']
        for text in cases:
            with self.subTest(text=text):
                put(self.root, p, text)
                self.refresh('skills')
                self.check_bad()

    def test_description_length_boundary(self):
        path = 'skills/review-academic-thesis/SKILL.md'
        for description, status in [('x' * 1024, 'STATIC_GO'), ('x' * 1025, 'REWORK'), (' ' + 'x' * 1024, 'REWORK')]:
            put(self.root, path, '---\nname: review-academic-thesis\ndescription: ' + json.dumps(description) + '\n---\n# Workflow\n')
            self.refresh('skills')
            self.assertEqual(self.module.validate(self.root)['status'], status)

    def test_valid_cli_counts_and_no_stderr(self):
        process = subprocess.run([sys.executable, '-B', str(VALIDATOR), str(self.root)], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0)
        self.assertEqual(process.stderr, '')
        result = json.loads(process.stdout)
        self.assertEqual((result['skills_checked'], result['adapters_checked']), (5, 4))

    def test_missing_license_and_unregistered_adapter_file(self):
        (self.root / 'skills/review-academic-thesis/LICENSE.txt').unlink()
        self.refresh('skills')
        self.check_bad()
        self.registry = fixture(self.root)
        put(self.root, 'adapters/chatgpt/extra.txt', 'Unregistered context')
        self.check_bad()

    def test_malformed_adapter_and_frontmatter_yaml(self):
        for path in ['adapters/chatgpt/adapter.yaml', 'skills/review-academic-thesis/SKILL.md']:
            self.registry = fixture(self.root)
            put(self.root, path, '---\nname: [unterminated\n---\n')
            self.refresh('adapters' if path.startswith('adapters') else 'skills')
            self.check_bad()

    def test_duplicate_yaml_keys_every_surface(self):
        for path in ['registry.yaml', 'adapters/chatgpt/adapter.yaml', 'skills/review-academic-thesis/SKILL.md']:
            with self.subTest(path=path):
                self.registry = fixture(self.root)
                text = (self.root / path).read_text()
                if path.endswith('SKILL.md'):
                    text = text.replace('description: Synthetic workflow.', 'description: one\ndescription: two')
                else:
                    text += '\nname: one\nname: two\n'
                put(self.root, path, text)
                if path.startswith('adapters'):
                    self.refresh('adapters')
                elif path.startswith('skills'):
                    self.refresh('skills')
                self.check_bad()

    def test_unhashable_yaml_key_and_malformed_cli_emit_json(self):
        for text in ['? [a, b]\n: value\n', 'skills: [unterminated', '---\n!!python/object:os.system {}']:
            with self.subTest(text=text):
                put(self.root, 'registry.yaml', text)
                self.check_bad()
                process = subprocess.run([sys.executable, str(VALIDATOR), str(self.root)], capture_output=True, text=True)
                self.assertEqual(process.returncode, 1)
                self.assertEqual(process.stderr, '')
                self.assertEqual(json.loads(process.stdout)['status'], 'REWORK')


if __name__ == '__main__':
    unittest.main()
