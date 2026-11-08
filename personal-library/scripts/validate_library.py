"""Offline, fail-closed validation for this pinned, documentation-only library.

Frontmatter validation deliberately supports single-line name/description scalars,
not the full YAML language. No bundle code is imported or executed. This is a
static integrity gate, not a prompt-injection detector or behavioral assurance.
SKILL.md provenance is joined to the public snapshot inventory. Reference and
license files require the separate remote source review because this inventory
does not enumerate them. Enumerated-file totals reconcile declared metadata;
the offline gate cannot independently establish complete remote tree coverage.
"""
from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[\"'][^\n]*?[\"'])?\s*\)")
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>]+>|\S+)", re.MULTILINE)
DOC_SUFFIXES = {".md", ".txt"}


def _safe_path(value):
    return (isinstance(value, str) and bool(value) and "\\" not in value
            and "\0" not in value and not value.startswith("/")
            and not re.match(r"^[A-Za-z]:", value)
            and all(part not in {"", ".", ".."} for part in value.split("/")))


def _scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return value[1:-1].replace("''", "'")
    if value.startswith(("|", ">", "[", "{", "&", "*", "!")):
        return None
    return value


def _frontmatter(text, label, errors):
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        errors.append(f"{label}: missing frontmatter delimiters")
        return {}
    fields = {}
    for line in lines[1:lines.index("---", 1)]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if not match:
            errors.append(f"{label}: unsupported frontmatter syntax")
            continue
        key, raw = match.groups()
        if key in fields:
            errors.append(f"{label}: duplicate frontmatter key {key}")
        fields[key] = _scalar(raw or "")
    return fields


def validate(root: Path) -> dict:
    """Return static gate results without network access or modifying root."""
    root = Path(root)
    errors = []
    checked_files = 0
    checked_skills = 0

    def problem(message):
        errors.append(message)

    def load_json(relative):
        target = root / relative
        if target.is_symlink():
            problem(f"{relative}: symlink is forbidden")
            return {}
        try:
            value = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            problem(f"{relative}: cannot read valid JSON ({type(exc).__name__})")
            return {}
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            problem(f"{relative}: expected object with schema_version 1")
            return {}
        return value

    def objects(value, label):
        if not isinstance(value, list):
            problem(f"{label}: expected list")
            return []
        valid = []
        for item in value:
            if isinstance(item, dict):
                valid.append(item)
            else:
                problem(f"{label}: expected object entries")
        return valid

    def pin(value, label, regex=HEX40):
        if not isinstance(value, str) or not regex.fullmatch(value):
            problem(f"{label}: invalid pinned hash")

    if root.is_symlink() or not root.is_dir():
        return {"status": "REWORK", "errors": ["root must be a real directory, not a symlink"], "skills_checked": 0, "files_checked": 0}
    # os.walk does not follow directory links. Reject them before any bundle read.
    for directory, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            if (Path(directory) / name).is_symlink():
                problem(f"{(Path(directory) / name).relative_to(root)}: symlink is forbidden")
    if errors:
        return {"status": "REWORK", "errors": errors, "skills_checked": 0, "files_checked": 0}
    lock = load_json("sources.lock.json")
    catalog = load_json("catalog.json")
    inventory = load_json("inventory/public.json")
    sources = {}
    locked = {}
    if not lock.get("sources") or not catalog.get("skills"):
        problem("sources and catalog skills must be nonempty")
    for source in objects(lock.get("sources"), "sources"):
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id:
            problem("source id: expected nonempty string")
            continue
        if source_id in sources:
            problem(f"duplicate source id: {source_id}")
        sources[source_id] = source
        if source.get("visibility") != "public":
            problem(f"{source_id}: source must be public")
        for field in ("repository", "upstream_repository"):
            if not isinstance(source.get(field), str) or not REPOSITORY.fullmatch(source[field]):
                problem(f"{source_id}: invalid {field}")
        pin(source.get("commit_sha"), f"{source_id} commit_sha")
        if source.get("license") != "MIT":
            problem(f"{source_id}: this gate permits only reviewed MIT bundles")
        if not isinstance(source.get("review_status"), str) or source["review_status"] not in {"accepted", "accepted-with-guards"}:
            problem(f"{source_id}: source review is not accepted")
        for entry in objects(source.get("files"), f"{source_id} files"):
            path = entry.get("path")
            if not _safe_path(path):
                problem(f"{source_id}: unsafe path {path!r}")
                continue
            if not path.startswith("skills/"):
                problem(f"{source_id}: locked file must be under skills/: {path}")
            if path in locked:
                problem(f"duplicate locked path: {path}")
            locked[path] = (source_id, entry)
            if not _safe_path(entry.get("upstream_path")):
                problem(f"{path}: unsafe path in upstream_path")
            pin(entry.get("git_blob_sha"), f"{path} git_blob_sha")
            pin(entry.get("sha256"), f"{path} sha256", HEX64)
            target = root / path
            if target.is_symlink() or any(parent.is_symlink() for parent in target.parents if parent == root or root in parent.parents):
                problem(f"{path}: symlink cannot be read")
                continue
            if not target.is_file():
                problem(f"{path}: missing locked file")
                continue
            checked_files += 1
            if target.suffix.lower() not in DOC_SUFFIXES:
                problem(f"{path}: docs-only bundle contains unsupported file type")
            if target.stat().st_mode & 0o111:
                problem(f"{path}: executable permission is forbidden")
            try:
                data = target.read_bytes()
                data.decode("utf-8")
            except (OSError, UnicodeError):
                problem(f"{path}: cannot read UTF-8 document")
                continue
            if hashlib.sha256(data).hexdigest() != entry.get("sha256"):
                problem(f"{path}: SHA256 hash mismatch")
            blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
            if blob != entry.get("git_blob_sha"):
                problem(f"{path}: git blob hash mismatch")

    names, skill_paths = set(), set()
    used_sources = set()
    for skill in objects(catalog.get("skills"), "catalog skills"):
        name, path = skill.get("name"), skill.get("path")
        if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64:
            problem(f"invalid skill name: {name!r}")
            continue
        if name in names:
            problem(f"duplicate skill name: {name}")
        names.add(name)
        if not _safe_path(path):
            problem(f"{name}: unsafe path {path!r}")
            continue
        if path != f"skills/{name}":
            problem(f"{name}: catalog path must match skills/name")
        if path in skill_paths:
            problem(f"duplicate skill path: {path}")
        skill_paths.add(path)
        if skill.get("status") != "staged":
            problem(f"{name}: only staged status is supported by this gate")
        source_id = skill.get("source_id")
        if not isinstance(source_id, str) or source_id not in sources:
            problem(f"{name}: unknown source_id")
        else:
            used_sources.add(source_id)
        skill_root = root / path
        if skill_root.is_symlink() or not skill_root.is_dir():
            problem(f"{name}: skill directory is missing or symlink")
            continue
        checked_skills += 1
        entrypoint = skill_root / "SKILL.md"
        try:
            fields = _frontmatter(entrypoint.read_text(encoding="utf-8"), str(path), errors)
        except (OSError, UnicodeError):
            fields = {}
            problem(f"{path}: cannot read SKILL.md")
        if fields.get("name") != name:
            problem(f"{path}: frontmatter name must match folder")
        description = fields.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            problem(f"{path}: description must contain 1..1024 characters")
        license_path = f"{path}/LICENSE.txt"
        if license_path not in locked:
            problem(f"{path}: missing locked LICENSE.txt")
        else:
            try:
                notice = (root / license_path).read_text(encoding="utf-8")
                if not all(token in notice for token in ("MIT License", "Copyright", "Permission is hereby granted")):
                    problem(f"{license_path}: missing MIT license notice")
            except (OSError, UnicodeError):
                problem(f"{license_path}: cannot read license notice")
        for file in skill_root.rglob("*"):
            if file.is_symlink() or not file.is_file():
                continue
            relative = file.relative_to(root).as_posix()
            if relative not in locked:
                problem(f"{relative}: unlocked bundle file")
            elif locked[relative][0] != source_id:
                problem(f"{relative}: file source differs from catalog source_id")
            if file.suffix.lower() != ".md":
                continue
            try:
                text = file.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            for match in list(LINK.finditer(text)) + list(REFERENCE_LINK.finditer(text)):
                target = match.group(1).strip("<>")
                try:
                    parts = urlsplit(target)
                except ValueError:
                    problem(f"{relative}: malformed link")
                    continue
                if parts.scheme or parts.netloc:
                    if parts.scheme not in {"http", "https", "mailto"}:
                        problem(f"{relative}: unsupported link scheme")
                    continue
                if not parts.path:
                    continue
                decoded = unquote(parts.path)
                if "\\" in decoded or "\0" in decoded or decoded.startswith("/"):
                    problem(f"{relative}: local link escapes skill")
                    continue
                destination = (file.parent / decoded).resolve()
                if not destination.is_relative_to(skill_root.resolve()):
                    problem(f"{relative}: local link escapes skill")
                elif not destination.exists():
                    problem(f"{relative}: missing local link {target}")
    for source_id in sources.keys() - used_sources:
        problem(f"{source_id}: source is not referenced by catalog")
    for path in locked:
        if not any(path.startswith(skill_path + "/") for skill_path in skill_paths):
            problem(f"{path}: locked file belongs to no catalog skill")
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        for file in skills_dir.rglob("*"):
            if file.is_file() and not file.is_symlink() and file.relative_to(root).as_posix() not in locked:
                problem(f"{file.relative_to(root)}: unlocked file under skills/")

    repositories = {}
    for repo in objects(inventory.get("repositories"), "inventory repositories"):
        name = repo.get("repository")
        if not isinstance(name, str) or not REPOSITORY.fullmatch(name):
            problem("inventory repository has invalid name")
            continue
        if name in repositories:
            problem(f"duplicate inventory repository: {name}")
        repositories[name] = repo
        if repo.get("visibility") != "public":
            problem(f"{name}: inventory repository must be public")
        pin(repo.get("commit_sha"), f"{name} inventory commit_sha")
        if repo.get("tree_complete") is not True:
            problem(f"{name}: inventory tree is incomplete")
    artifact_keys = set()
    artifact_index = {}
    kind_counts = defaultdict(Counter)
    skill_blobs = defaultdict(list)
    artifacts = objects(inventory.get("artifacts"), "inventory artifacts")
    if not artifacts:
        problem("inventory must have nonempty artifacts")
    for artifact in artifacts:
        name = artifact.get("repository")
        if not isinstance(name, str) or name not in repositories:
            problem("inventory artifact has undeclared repository")
        elif artifact.get("commit_sha") != repositories[name].get("commit_sha"):
            problem(f"{name}: artifact snapshot does not match repository")
        pin(artifact.get("commit_sha"), "artifact commit_sha")
        pin(artifact.get("blob_sha"), "artifact blob_sha")
        if not _safe_path(artifact.get("path")):
            problem("inventory artifact has unsafe path")
        key = (name, artifact.get("path"))
        if all(isinstance(x, str) for x in key):
            if key in artifact_keys:
                problem(f"duplicate inventory artifact: {key}")
            artifact_keys.add(key)
            artifact_index[key] = artifact
        kind = artifact.get("kind")
        mode = artifact.get("mode")
        if not isinstance(mode, str) or mode not in {"100644", "100755", "120000"}:
            problem("inventory artifact mode must be a supported Git blob mode")
        if not isinstance(kind, str) or not kind:
            problem("inventory artifact kind must be a nonempty string")
        elif isinstance(name, str):
            kind_counts[name][kind] += 1
        if kind == "skill-entry" and isinstance(artifact.get("blob_sha"), str):
            skill_blobs[artifact["blob_sha"]].append(artifact)

    for source_id, source in sources.items():
        name = source.get("repository")
        repo = repositories.get(name) if isinstance(name, str) else None
        if repo is None or repo.get("visibility") != "public":
            problem(f"{source_id}: source repository is absent from public inventory")
        elif source.get("commit_sha") != repo.get("commit_sha"):
            problem(f"{source_id}: source snapshot differs from public inventory")
        for entry in objects(source.get("files"), f"{source_id} files"):
            if not isinstance(entry.get("path"), str) or not entry["path"].endswith("/SKILL.md"):
                continue
            upstream_path = entry.get("upstream_path")
            artifact = artifact_index.get((name, upstream_path)) if isinstance(name, str) and isinstance(upstream_path, str) else None
            if (artifact is None or artifact.get("commit_sha") != source.get("commit_sha")
                    or artifact.get("blob_sha") != entry.get("git_blob_sha")
                    or artifact.get("kind") != "skill-entry"):
                problem(f"{source_id}: upstream artifact does not match locked SKILL.md")

    files_enumerated = 0
    for name, repo in repositories.items():
        count = repo.get("files_enumerated")
        if type(count) is not int or count < 0:
            problem(f"{name}: files_enumerated must be a nonnegative integer")
        else:
            files_enumerated += count
            if count < sum(kind_counts[name].values()):
                problem(f"{name}: files_enumerated is smaller than artifact counts")
        declared = repo.get("counts")
        if (not isinstance(declared, dict)
                or any(not isinstance(key, str) or type(value) is not int or value < 0 for key, value in declared.items())
                or declared != dict(kind_counts[name])):
            problem(f"{name}: counts do not match inventory artifacts")

    duplicate_blobs = {blob: members for blob, members in skill_blobs.items() if len(members) > 1}
    expected_totals = {
        "repositories": len(repositories),
        "files_enumerated": files_enumerated,
        "artifacts": len(artifacts),
        "skill_entries": sum(len(members) for members in skill_blobs.values()),
        "unique_skill_blobs": len(skill_blobs),
        "duplicate_skill_groups": len(duplicate_blobs),
    }
    totals = inventory.get("totals")
    if (not isinstance(totals, dict) or set(totals) != set(expected_totals)
            or any(type(totals.get(key)) is not int or totals.get(key) != value for key, value in expected_totals.items())):
        problem("inventory totals do not match recomputed aggregates")
    if "duplicates" in inventory:
        expected_groups = {
            blob: {(member["repository"], member["path"], member.get("mode")) for member in members}
            for blob, members in duplicate_blobs.items()
            if all(isinstance(member.get("repository"), str) and isinstance(member.get("path"), str)
                   and isinstance(member.get("mode"), str) for member in members)
        }
        declared_groups = {}
        valid_groups = isinstance(inventory["duplicates"], list)
        for group in objects(inventory["duplicates"], "inventory duplicate groups"):
            blob = group.get("blob_sha")
            if not isinstance(blob, str) or not HEX40.fullmatch(blob) or blob in declared_groups:
                valid_groups = False
                continue
            members = group.get("paths")
            if not isinstance(members, list):
                valid_groups = False
                continue
            paths = set()
            for member in members:
                if not isinstance(member, dict) or any(not isinstance(member.get(key), str) for key in ("repository", "path", "mode")):
                    valid_groups = False
                    continue
                paths.add(tuple(member[key] for key in ("repository", "path", "mode")))
            if len(paths) != len(members):
                valid_groups = False
            declared_groups[blob] = paths
        if not valid_groups or declared_groups != expected_groups:
            problem("inventory duplicate groups do not match skill artifact memberships")
    return {"status": "REWORK" if errors else "STATIC_GO", "errors": errors,
            "skills_checked": checked_skills, "files_checked": checked_files}


def main():
    if len(sys.argv) != 2:
        result = {"status": "REWORK", "errors": ["usage: validate_library.py ROOT"], "skills_checked": 0, "files_checked": 0}
    else:
        result = validate(Path(sys.argv[1]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
