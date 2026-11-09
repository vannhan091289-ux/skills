"""Distribution acceptance tests; never execute a bundled skill helper."""
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import unittest
import zipfile

import yaml
from build_export import build

SOURCE = Path(__file__).resolve().parents[1] / 'personal-ai-skills'


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        shutil.copytree(SOURCE, self.source)
        self.dest = self.root / 'export'

    def test_complete_plugin_and_archive_preserve_source_bytes(self):
        archive = build(self.source, self.dest)
        plugin = self.dest / 'plugins/personal-ai-skills'
        manifest = json.loads((plugin / 'plugin.json').read_text())
        self.assertEqual(set(manifest), {'$schema', 'name', 'version', 'description'})
        self.assertEqual(manifest['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        registry = yaml.safe_load((self.source / 'registry.yaml').read_text())
        self.assertEqual(len(list((plugin / 'skills').iterdir())), 11)
        for group in registry['skills']:
            for entry in group['files']:
                self.assertEqual((plugin / entry['path']).read_bytes(), (self.source / entry['path']).read_bytes())
        provenance = json.loads((plugin / 'provenance.json').read_text())
        self.assertFalse(provenance['chatgpt_runtime_verified'])
        self.assertEqual(provenance['source_commit'], '6cdbc9726f3b1cca1dba03c22a2475bbe8541ea7')
        catalog = json.loads((self.dest / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(len(catalog['plugins']), 1)
        entry = catalog['plugins'][0]
        self.assertEqual(entry['policy']['installation'], 'AVAILABLE')
        self.assertEqual((self.dest / entry['source']['path']).resolve(), plugin.resolve())
        with zipfile.ZipFile(archive) as z:
            entries = [p for p in self.dest.rglob('*') if p.is_file()]
            self.assertEqual(set(z.namelist()), {p.relative_to(self.dest).as_posix() for p in entries})
            for p in entries:
                self.assertEqual(z.read(p.relative_to(self.dest).as_posix()), p.read_bytes())
        self.assertFalse(any(p.name in {'.app.json', 'mcp.json', '.mcp.json', 'hooks.json', 'config.toml'} for p in self.dest.rglob('*')))

    def rejected(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            build(self.source, self.dest)
        self.assertFalse(self.dest.exists())
        self.assertFalse(self.dest.with_suffix('.zip').exists())

    def test_tampered_skill_is_rejected_before_writing(self):
        with (self.source / 'skills/audit-branch-kpi/SKILL.md').open('a') as stream:
            stream.write('\nTampered')
        self.rejected('hash|integrity')

    def test_unregistered_file_is_rejected_before_writing(self):
        (self.source / 'skills/audit-branch-kpi/hooks.json').write_text('{}')
        self.rejected('inventory|unregistered')

    def test_symlink_is_rejected(self):
        file = self.source / 'skills/audit-branch-kpi/SKILL.md'
        original = self.root / 'original.md'
        file.rename(original)
        file.symlink_to(original)
        self.rejected('symlink')

    def test_changed_registry_is_rejected(self):
        registry = self.source / 'registry.yaml'
        registry.write_text(registry.read_text() + '\n# unreviewed modification\n')
        self.rejected('registry')

    def test_destination_inside_source_is_rejected(self):
        self.dest = self.source / 'export'
        self.rejected('overlap')

    def test_existing_destination_is_preserved(self):
        self.dest.mkdir()
        sentinel = self.dest / 'keep.txt'
        sentinel.write_text('user work')
        with self.assertRaises(FileExistsError):
            build(self.source, self.dest)
        self.assertEqual(sentinel.read_text(), 'user work')

    def test_existing_archive_is_preserved(self):
        archive = self.dest.with_suffix('.zip')
        archive.write_bytes(b'user archive')
        with self.assertRaises(FileExistsError):
            build(self.source, self.dest)
        self.assertEqual(archive.read_bytes(), b'user archive')
        self.assertFalse(self.dest.exists())

    def test_archive_is_reproducible(self):
        first = build(self.source, self.dest)
        second = build(self.source, self.root / 'another-export')
        self.assertEqual(hashlib.sha256(first.read_bytes()).hexdigest(), hashlib.sha256(second.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
