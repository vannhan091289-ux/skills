#!/usr/bin/env python3
"""Read-only structural/integrity checks for the canonical portable library.

Requires PyYAML 6.0.3. Hashes detect changed bytes; they do not establish source
 authenticity, host permissions, native discovery, or runtime compatibility.
No network, source imports/execution, installation, or file writes occur.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

CORE = {'review-academic-thesis', 'audit-branch-kpi', 'review-code-change'}
EXPANSION = {'plan-branch-execution', 'track-management-actions', 'review-business-policy',
             'research-with-evidence', 'prepare-interactive-training', 'create-visual-learning-assets'}
SUPPORT = {'grammar-checker-vi', 'scientific-thinking-literature-review'}
SCRIPT_SUFFIXES = {'.py', '.sh', '.bash', '.zsh', '.fish', '.js', '.mjs', '.cjs', '.ts', '.rb', '.pl', '.php', '.ps1', '.bat', '.cmd'}
EXECUTABLE_SUFFIXES = SCRIPT_SUFFIXES | {'.pyc', '.pyo', '.so', '.dylib', '.dll', '.exe', '.jar', '.wasm', '.ipynb'}
FIRST_PARTY = {'evaluations/validate_library.py', 'evaluations/tests/test_layout_contract.py',
               'evaluations/tests/test_registry_validator.py'}
ADAPTERS = {'chatgpt', 'gemini', 'claude', 'codex'}
GOVERNANCE = {'security_policy': 'governance/security-policy.md',
              'quality_gates': 'governance/quality-gates.md',
              'data_classification': 'governance/data-classification.md'}


class Invalid(ValueError):
    """A validation failure safe to show to the caller."""


class UniqueSafeLoader(yaml.SafeLoader):
    """Safe YAML with duplicate mapping keys rejected at every depth."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in result:
                raise Invalid(f'duplicate YAML key: {key!r}')
            result[key] = loader.construct_object(value_node, deep=deep)
        except TypeError as exc:
            raise Invalid('YAML mapping key must be hashable') from exc
    return result


UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def require(condition, message):
    if not condition:
        raise Invalid(message)


def mapping(value, keys, label):
    require(type(value) is dict, f'{label}: expected mapping')
    require(set(value) == set(keys), f'{label}: unexpected or missing fields')


def string(value, label):
    require(type(value) is str and bool(value.strip()), f'{label}: expected nonempty string')


def safe_path(value):
    string(value, 'path')
    require('\\' not in value and '\x00' not in value, f'unsafe path: {value!r}')
    require(not value.startswith('/') and all(p not in ('', '.', '..') for p in value.split('/')),
            f'unsafe path: {value!r}')
    return PurePosixPath(value)


def load_yaml(path):
    return yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueSafeLoader)


def useful_files(folder):
    """Reject empty/cache/obvious placeholder evidence; no semantic execution claim."""
    if not folder.is_dir():
        return []
    useful = []
    for path in folder.rglob('*'):
        if (not path.is_file() or not path.stat().st_size or path.suffix in ('.pyc', '.pyo')
                or any(p.startswith('.') or p == '__pycache__' for p in path.relative_to(folder).parts)):
            continue
        text = path.read_bytes().decode('utf-8', errors='replace').strip()
        if not text or re.fullmatch(r'[#\s]*(?:todo|tbd|placeholder|fixme)(?:[ :._-].*)?', text, re.I):
            continue
        useful.append(path)
    return useful


def code_resources(folder, is_test=False):
    for path in useful_files(folder):
        if path.suffix.lower() not in SCRIPT_SUFFIXES:
            continue
        if is_test and not (path.name.startswith('test_') or '.test.' in path.name or path.stem.endswith('_test')):
            continue
        lines = [line.strip() for line in path.read_text(encoding='utf-8').splitlines()
                 if line.strip() and not line.lstrip().startswith(('#', '//'))
                 and line.strip() not in ('pass', '...', 'TODO', 'TBD')]
        if len(lines) >= 2:
            return True
    return False


def check_executable_surface(root, registered):
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        with path.open('rb') as stream:
            shebang = stream.read(2) == b'#!'
        executable = path.suffix.lower() in EXECUTABLE_SUFFIXES or path.stat().st_mode & 0o111 or shebang
        require(not executable or relative in registered or relative in FIRST_PARTY,
                f'undeclared executable/script: {relative}')


def fixture_catalog(root):
    path = root / 'evaluations/fixtures/fixture-catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8'))
    mapping(catalog, {'schema_version', 'classification', 'fixtures'}, 'fixture catalog')
    require(type(catalog['schema_version']) is int and catalog['schema_version'] == 1,
            'fixture catalog schema_version must be integer 1')
    require(catalog['classification'] == 'PUBLIC_SYNTHETIC', 'fixture catalog must be PUBLIC_SYNTHETIC')
    require(type(catalog['fixtures']) is list and bool(catalog['fixtures']), 'fixture catalog requires nonempty fixtures')
    seen = set()
    for record in catalog['fixtures']:
        mapping(record, {'path', 'type'}, 'fixture catalog record')
        relative = safe_path(record['path']).as_posix()
        string(record['type'], 'fixture catalog type')
        require(relative not in seen, f'duplicate fixture path: {relative}')
        seen.add(relative)
        target = root / relative
        require(target.resolve().is_relative_to(root.resolve()) and target.is_file() and not target.is_symlink(),
                f'fixture catalog target missing or unsafe: {relative}')


def inventory(root, records, prefix=None, expected=None):
    require(type(records) is list and bool(records), 'files: expected nonempty list')
    seen = set()
    for record in records:
        mapping(record, {'path', 'sha256'}, 'file record')
        relative = safe_path(record['path']).as_posix()
        require(relative not in seen, f'duplicate file path: {relative}')
        seen.add(relative)
        if prefix is not None:
            require(relative.startswith(prefix + '/'), f'file outside declared folder: {relative}')
        sha = record['sha256']
        require(type(sha) is str and re.fullmatch('[0-9a-fA-F]{64}', sha) is not None,
                f'invalid SHA256: {relative}')
        target = root / relative
        require(target.is_file() and not target.is_symlink(), f'missing regular file: {relative}')
        require(hashlib.sha256(target.read_bytes()).hexdigest() == sha.lower(), f'hash mismatch: {relative}')
    if prefix is not None:
        actual = {p.relative_to(root).as_posix() for p in (root / prefix).rglob('*') if p.is_file()}
        require(actual == seen, f'file closure mismatch: {prefix}; undeclared={sorted(actual - seen)}; missing={sorted(seen - actual)}')
    if expected is not None:
        require(seen == set(expected), 'governance file coverage mismatch')
    return seen


def frontmatter(path, name):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    require(match is not None, f'{name}: missing frontmatter')
    metadata = yaml.load(match.group(1), Loader=UniqueSafeLoader)
    require(type(metadata) is dict, f'{name}: frontmatter must be mapping')
    require(metadata.get('name') == name and type(metadata.get('name')) is str, f'{name}: frontmatter name mismatch')
    description = metadata.get('description')
    require(type(description) is str and bool(description.strip()) and len(description) <= 1024,
            f'{name}: description must have 1..1024 characters')


def markdown_links(root, folder, files):
    closure = {(root / f).resolve() for f in files}
    boundary = (root / folder).resolve()
    for relative in files:
        path = root / relative
        if path.suffix.lower() != '.md':
            continue
        text = path.read_text(encoding='utf-8')
        # Both inline/image links and Markdown reference definitions.
        links = re.findall(r'!?\[[^\]\n]*\]\(\s*(<[^>]*>|[^\s)]+)', text)
        links += re.findall(r'^\s{0,3}\[[^\]\n]+\]:\s*(<[^>]*>|\S+)', text, re.M)
        for link in links:
            link = link.strip('<>')
            parts = urlsplit(link)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            local = unquote(parts.path)
            require('\\' not in local and not local.startswith('/') and '\x00' not in local,
                    f'unsafe Markdown link: {relative}: {link}')
            target = (path.parent / local).resolve()
            require(target.is_relative_to(boundary) and target in closure,
                    f'Markdown link outside resource closure or missing: {relative}: {link}')


def check_tree(root):
    require(root.is_dir() and not root.is_symlink(), 'root must be a regular directory')
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        require(not path.is_symlink(), f'symlink forbidden: {relative}')
        require(not any(p.startswith('.') for p in relative.parts), f'hidden file/directory forbidden: {relative}')
        require(path.is_file() or path.is_dir(), f'nonregular filesystem object: {relative}')


def _validate(root, result):
    check_tree(root)
    require((root / 'README.md').is_file() and (root / 'README.md').stat().st_size > 0, 'missing README.md')
    registry = load_yaml(root / 'registry.yaml')
    mapping(registry, {'schema_version', 'library', 'governance', 'skills', 'adapters', 'governance_files'}, 'registry')
    require(type(registry['schema_version']) is int and registry['schema_version'] == 1, 'schema_version must be integer 1')
    mapping(registry['library'], {'name', 'version'}, 'library')
    require(registry['library']['name'] == 'personal-ai-skills', 'library name mismatch')
    string(registry['library']['version'], 'library.version')
    version = re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?', registry['library']['version'])
    require(version is not None, 'library.version must be a semantic version')
    required_core = CORE | EXPANSION if tuple(map(int, version.groups())) >= (1, 1, 0) else CORE
    mapping(registry['governance'], GOVERNANCE, 'governance')
    require(registry['governance'] == GOVERNANCE, 'governance mapping mismatch')
    inventory(root, registry['governance_files'], prefix='governance', expected=GOVERNANCE.values())
    require(type(registry['skills']) is list, 'skills must be a list')
    names = set()
    registered_skill_files = set()
    for skill in registry['skills']:
        mapping(skill, {'name', 'path', 'version', 'role', 'status', 'runtime_scope', 'installed_name', 'files'}, 'skill')
        name = skill['name']
        require(type(name) is str and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', name) is not None, 'invalid skill name')
        require(name not in names, f'duplicate skill: {name}')
        names.add(name)
        require(skill['path'] == 'skills/' + name, f'{name}: path mismatch')
        string(skill['version'], f'{name}.version')
        require(type(skill['role']) is str and skill['role'] in ('core', 'support'), f'{name}: invalid role')
        require(skill['role'] == ('core' if name in CORE | EXPANSION else 'support'), f'{name}: incorrect role')
        require(type(skill['status']) is str and skill['status'] in ('PILOT_GO', 'STATIC_GO'), f'{name}: invalid status')
        string(skill['runtime_scope'], f'{name}.runtime_scope')
        require(skill['installed_name'] is None or (type(skill['installed_name']) is str and bool(skill['installed_name'].strip())),
                f'{name}: installed_name must be string or null')
        files = inventory(root, skill['files'], prefix=skill['path'])
        registered_skill_files.update(files)
        require(f"{skill['path']}/SKILL.md" in files, f'{name}: missing SKILL.md')
        require(any(f"{skill['path']}/{license_name}" in files and (root / skill['path'] / license_name).stat().st_size > 0
                    for license_name in ('LICENSE', 'LICENSE.txt', 'LICENSE.md')), f'{name}: missing license')
        frontmatter(root / skill['path'] / 'SKILL.md', name)
        if name in CORE | EXPANSION:
            for sub in ('references', 'assets', 'scripts', 'tests'):
                require(bool(useful_files(root / skill['path'] / sub)), f'{name}: {sub} must have useful nonempty files')
            require(code_resources(root / skill['path'] / 'scripts'), f'{name}: scripts require substantive script file')
            require(code_resources(root / skill['path'] / 'tests', is_test=True), f'{name}: tests require substantive test file')
        markdown_links(root, skill['path'], files)
        result['skills_checked'] += 1
    required_names = required_core | SUPPORT
    require(names == required_names, f'canonical inventory for version incomplete; missing={sorted(required_names - names)}; extra={sorted(names - required_names)}')
    actual_skills = {p.name for p in (root / 'skills').iterdir()}
    require(actual_skills == names, 'unregistered skill folder/file')
    require(type(registry['adapters']) is list, 'adapters must be a list')
    adapters = set()
    for adapter in registry['adapters']:
        mapping(adapter, {'name', 'path', 'mode', 'runtime_verified', 'files'}, 'adapter')
        name = adapter['name']
        require(type(name) is str and name in ADAPTERS and name not in adapters, 'invalid or duplicate adapter name')
        adapters.add(name)
        require(adapter['path'] == 'adapters/' + name, f'{name}: adapter path mismatch')
        require(type(adapter['mode']) is str and adapter['mode'] in ('manual-context', 'documented-native'), f'{name}: unsupported mode')
        require(adapter['runtime_verified'] is False, f'{name}: runtime_verified must be false')
        files = inventory(root, adapter['files'], prefix=adapter['path'])
        require({adapter['path'] + '/README.md', adapter['path'] + '/adapter.yaml'} <= files, f'{name}: missing adapter files')
        manifest = load_yaml(root / adapter['path'] / 'adapter.yaml')
        mapping(manifest, {'schema_version', 'name', 'mode', 'runtime_verified', 'source_registry', 'instructions', 'official_sources', 'required_steps'}, f'{name} manifest')
        require(type(manifest['schema_version']) is int and manifest['schema_version'] == 1, f'{name}: invalid manifest schema')
        require(manifest['name'] == name and manifest['mode'] == adapter['mode'] and manifest['runtime_verified'] is False,
                f'{name}: manifest disagrees with registry')
        require(manifest['source_registry'] == '../../registry.yaml' and
                (root / adapter['path'] / manifest['source_registry']).resolve() == (root / 'registry.yaml').resolve(),
                f'{name}: source_registry must resolve to library registry')
        require(manifest['instructions'] == 'README.md', f'{name}: instructions must be README.md')
        require((root / adapter['path'] / 'README.md').stat().st_size > 0, f'{name}: empty README.md')
        for key in ('official_sources', 'required_steps'):
            require(type(manifest[key]) is list and bool(manifest[key]), f'{name}: {key} must be nonempty list')
            for value in manifest[key]:
                string(value, f'{name}.{key}')
        result['adapters_checked'] += 1
    require(adapters == ADAPTERS, 'exactly four supported adapters required')
    require({p.name for p in (root / 'adapters').iterdir()} == ADAPTERS, 'unregistered adapter folder/file')
    check_executable_surface(root, registered_skill_files)
    fixture_catalog(root)
    for folder in ('evaluations/fixtures', 'evaluations/reports'):
        require(bool(useful_files(root / folder)), f'{folder} must contain nonempty evidence')


def validate(root: Path) -> dict:
    """Return JSON-compatible diagnostics; malformed input never escapes as traceback."""
    result = {'status': 'STATIC_GO', 'errors': [], 'skills_checked': 0, 'adapters_checked': 0}
    try:
        _validate(Path(root).absolute(), result)
    except Exception as exc:
        result['status'] = 'REWORK'
        result['errors'].append(f'{type(exc).__name__}: {exc}')
    return result


def main():
    if len(sys.argv) != 2:
        result = {'status': 'REWORK', 'errors': ['Usage: python validate_library.py ROOT'], 'skills_checked': 0, 'adapters_checked': 0}
    else:
        result = validate(Path(sys.argv[1]))
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['status'] == 'STATIC_GO' else 1


if __name__ == '__main__':
    sys.exit(main())
