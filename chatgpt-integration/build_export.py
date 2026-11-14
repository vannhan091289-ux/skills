"""Build a pinned distribution. No network, source execution or installation.

Requires the existing reviewed PyYAML. Updating the source pin is a review step.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import re
import zipfile

import yaml

SOURCE_COMMIT = '6cdbc9726f3b1cca1dba03c22a2475bbe8541ea7'
REGISTRY_SHA256 = '7463a446855810bbc0ee5f889ca1f523f9c25888f63cb5cbdee74641d5d9af06'
SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def safe_relative(value):
    parts = value.split('/')
    if '\\' in value or '\x00' in value or any(p in ('', '.', '..') for p in parts):
        raise ValueError('unsafe source path')
    return PurePosixPath(value)


def source_snapshot(source):
    if source.is_symlink() or any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('source symlink rejected')
    raw = (source / 'registry.yaml').read_bytes()
    if digest(raw) != REGISTRY_SHA256:
        raise ValueError('source registry differs from reviewed pin')
    registry = yaml.safe_load(raw)
    files = {}
    entries = registry['governance_files'] + [f for skill in registry['skills'] for f in skill['files']]
    for row in entries:
        rel = safe_relative(row['path'])
        path = source / rel
        if not path.is_file() or path.is_symlink():
            raise ValueError(f'missing or symlink source: {rel}')
        data = path.read_bytes()
        if digest(data) != row['sha256']:
            raise ValueError(f'source integrity hash mismatch: {rel}')
        files[str(rel)] = data
    actual = {p.relative_to(source).as_posix() for p in (source / 'skills').rglob('*') if p.is_file()}
    expected = {p for p in files if p.startswith('skills/')}
    if actual != expected:
        raise ValueError('unregistered skill file or incomplete inventory')
    if len(registry['skills']) != 11:
        raise ValueError('expected eleven reviewed skills')
    return registry, files


def build(source, destination):
    source = Path(source).absolute()
    destination = Path(destination).absolute()
    archive = destination.with_suffix('.zip')
    if destination.exists() or destination.is_symlink() or archive.exists() or archive.is_symlink():
        raise FileExistsError('refusing to replace an existing destination or archive')
    src, dst = source.resolve(), destination.resolve()
    if src == dst or src in dst.parents or dst in src.parents:
        raise ValueError('source and destination overlap')
    registry, snapshot = source_snapshot(source)
    manifest = {'$schema': SCHEMA, 'name': 'personal-ai-skills',
                'version': registry['library']['version'],
                'description': 'Vietnamese evidence-based personal workflows; eleven reviewed skills.'}
    if not re.fullmatch(r'^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$', manifest['name']):
        raise ValueError('invalid plugin name')
    provenance = {'schema_version': 1, 'source_repository': 'https://github.com/vannhan091289-ux/skills',
                  'source_commit': SOURCE_COMMIT, 'source_root': 'personal-ai-skills',
                  'source_registry_sha256': REGISTRY_SHA256, 'library_version': manifest['version'],
                  'chatgpt_runtime_verified': False,
                  'skills': [{'name': s['name'], 'version': s['version'], 'role': s['role']} for s in registry['skills']],
                  'source_file_sha256': {p: digest(b) for p, b in sorted(snapshot.items())}}
    catalog = {'name': 'personal-ai-skills-chatgpt', 'interface': {'displayName': 'Personal AI Skills'},
               'plugins': [{'name': 'personal-ai-skills',
                            'source': {'source': 'local', 'path': './plugins/personal-ai-skills'},
                            'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                            'category': 'Productivity'}]}
    plugin_files = dict(snapshot)
    plugin_files['plugin.json'] = json_bytes(manifest)
    plugin_files['provenance.json'] = json_bytes(provenance)
    plugin_files['README.md'] = (
        '# Personal AI Skills — ChatGPT distribution\n\n'
        'Generated from the canonical pinned library; edit the canonical source, never this export.\n'
        'Choose one named skill per task. Read its usage guard and relevant governance documents.\n'
        'Bundled scripts/tests are inert resources; review before any explicitly authorized execution.\n'
        'No apps, MCP servers, hooks, installation settings or connector permissions are granted.\n'
        'ChatGPT installation and runtime are unverified. See provenance.json for versions and source hashes.\n'
        'Retain each package LICENSE/NOTICE; there is no single license replacing third-party notices.\n'
    ).encode()
    payload = {f'plugins/personal-ai-skills/{p}': b for p, b in plugin_files.items()}
    payload['.agents/plugins/marketplace.json'] = json_bytes(catalog)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()  # Exclusive creation; existing user files are never replaced.
    written = []
    archive_created = False
    try:
        for rel, data in sorted(payload.items()):
            path = destination / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(data)
            written.append(path)
        with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
            archive_created = True
            for rel, data in sorted(payload.items()):
                item = zipfile.ZipInfo(rel, date_time=(2026, 11, 9, 0, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o100644 << 16
                z.writestr(item, data)
    except Exception:
        for path in reversed(written):
            path.unlink(missing_ok=True)
        if archive_created:
            archive.unlink(missing_ok=True)
        for path in sorted(destination.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and not path.is_symlink():
                try:
                    path.rmdir()
                except OSError:
                    pass
        try:
            destination.rmdir()
        except OSError:
            pass
        raise
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--destination', required=True, type=Path)
    args = parser.parse_args()
    print(build(args.source, args.destination))
