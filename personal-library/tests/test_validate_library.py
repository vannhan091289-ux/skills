"""Offline acceptance and adversarial fixtures for the docs-only library gate."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_library.py"
COMMIT = "a" * 40
LICENSE = "MIT License\n\nCopyright (c) 2026 Test Contributors\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files.\n"


class LibraryValidationTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "First-party validator feature is unavailable")
        spec = importlib.util.spec_from_file_location("library_validator", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.lock = {"schema_version": 1, "sources": [{
            "id": "test-source", "repository": "owner/source", "upstream_repository": "origin/source",
            "commit_sha": COMMIT, "visibility": "public", "license": "MIT",
            "review_status": "accepted-with-guards", "files": []}]}
        self.catalog = {"schema_version": 1, "skills": [{"name": "test-skill", "path": "skills/test-skill", "status": "staged", "source_id": "test-source"}]}
        self.inventory = {"schema_version": 1, "repositories": [{
            "repository": "owner/source", "visibility": "public", "commit_sha": COMMIT,
            "tree_complete": True, "files_enumerated": 3, "counts": {"skill-entry": 1}}],
            "artifacts": [{"repository": "owner/source", "commit_sha": COMMIT,
                "path": "skills/test-skill/SKILL.md", "blob_sha": "b" * 40,
                "kind": "skill-entry", "mode": "100644", "review_status": "content-reviewed"}],
            "duplicates": [], "totals": {"repositories": 1, "files_enumerated": 3,
                "artifacts": 1, "skill_entries": 1, "unique_skill_blobs": 1, "duplicate_skill_groups": 0}}
        self.add_file("skills/test-skill/SKILL.md", "---\nname: test-skill\ndescription: Use when proofreading a supplied text.\n---\n\nRead [checks](references/checks.md).\n")
        self.add_file("skills/test-skill/references/checks.md", "# Checks\n\nKeep values unchanged.\n")
        self.add_file("skills/test-skill/LICENSE.txt", LICENSE)

    def add_file(self, path, content):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8")
        dest.write_bytes(data)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        self.lock["sources"][0]["files"].append({"path": path, "upstream_path": path,
            "git_blob_sha": blob,
            "sha256": hashlib.sha256(data).hexdigest()})
        if path == "skills/test-skill/SKILL.md":
            self.inventory["artifacts"][0]["blob_sha"] = blob

    def replace_file(self, path, content):
        self.lock["sources"][0]["files"] = [x for x in self.lock["sources"][0]["files"] if x["path"] != path]
        self.add_file(path, content)

    def run_validation(self):
        for path, value in [("sources.lock.json", self.lock), ("catalog.json", self.catalog), ("inventory/public.json", self.inventory)]:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(value), encoding="utf-8")
        return self.module.validate(self.root)

    def assert_rejected(self, expected):
        result = self.run_validation()
        self.assertEqual(result["status"], "REWORK", result)
        self.assertTrue(any(expected in str(e) for e in result["errors"]), result)

    def test_accepts_complete_pinned_document_bundle(self):
        result = self.run_validation()
        self.assertEqual(result, {"status": "STATIC_GO", "errors": [], "skills_checked": 1, "files_checked": 3})

    def test_rejects_tampered_file_bytes(self):
        (self.root / "skills/test-skill/references/checks.md").write_text("tamper", encoding="utf-8")
        self.assert_rejected("hash")

    def test_rejects_wrong_git_blob_with_matching_sha256(self):
        self.lock["sources"][0]["files"][0]["git_blob_sha"] = "0" * 40
        self.assert_rejected("git blob")

    def test_rejects_private_source(self):
        self.lock["sources"][0]["visibility"] = "private"
        self.assert_rejected("public")

    def test_rejects_mutable_commit_ref(self):
        self.lock["sources"][0]["commit_sha"] = "main"
        self.assert_rejected("commit_sha")

    def test_rejects_short_hash(self):
        self.lock["sources"][0]["files"][0]["sha256"] = "a" * 63
        self.assert_rejected("sha256")

    def test_rejects_path_traversal(self):
        self.lock["sources"][0]["files"][0]["path"] = "../escape.md"
        self.assert_rejected("unsafe path")

    def test_rejects_absolute_path(self):
        self.catalog["skills"][0]["path"] = "/tmp/escape"
        self.assert_rejected("unsafe path")

    def test_rejects_windows_path(self):
        self.lock["sources"][0]["files"][0]["path"] = "skills\\test-skill\\SKILL.md"
        self.assert_rejected("unsafe path")

    def test_rejects_duplicate_locked_paths(self):
        self.lock["sources"][0]["files"].append(copy.deepcopy(self.lock["sources"][0]["files"][0]))
        self.assert_rejected("duplicate locked path")

    def test_rejects_duplicate_source_id(self):
        self.lock["sources"].append(copy.deepcopy(self.lock["sources"][0]))
        self.assert_rejected("duplicate source id")

    def test_rejects_duplicate_catalog_name(self):
        self.catalog["skills"].append(copy.deepcopy(self.catalog["skills"][0]))
        self.assert_rejected("duplicate skill name")

    def test_rejects_unknown_source_id(self):
        self.catalog["skills"][0]["source_id"] = "not-reviewed"
        self.assert_rejected("unknown source_id")

    def test_rejects_symlink_in_skill_bundle(self):
        (self.root / "skills/test-skill/alias.md").symlink_to("SKILL.md")
        self.assert_rejected("symlink")

    def test_rejects_missing_dependency(self):
        (self.root / "skills/test-skill/references/checks.md").unlink()
        self.assert_rejected("missing local link")

    def test_rejects_dependency_escaping_skill(self):
        self.replace_file("skills/test-skill/SKILL.md", "---\nname: test-skill\ndescription: Use when proofreading.\n---\n[bad](../../catalog.json)\n")
        self.assert_rejected("escapes skill")

    def test_rejects_unlocked_extra_file(self):
        (self.root / "skills/test-skill/extra.md").write_text("not reviewed", encoding="utf-8")
        self.assert_rejected("unlocked")

    def test_rejects_code_under_docs_only_skills(self):
        self.add_file("skills/test-skill/helper.py", "print('must not execute')\n")
        self.assert_rejected("docs-only")

    def test_rejects_executable_permission_on_document(self):
        (self.root / "skills/test-skill/references/checks.md").chmod(0o755)
        self.assert_rejected("executable")

    def test_rejects_missing_license(self):
        self.lock["sources"][0]["files"] = [f for f in self.lock["sources"][0]["files"] if not f["path"].endswith("LICENSE.txt")]
        (self.root / "skills/test-skill/LICENSE.txt").unlink()
        self.assert_rejected("LICENSE.txt")

    def test_rejects_license_without_notice(self):
        self.replace_file("skills/test-skill/LICENSE.txt", "MIT\n")
        self.assert_rejected("license notice")

    def test_rejects_name_folder_mismatch(self):
        self.replace_file("skills/test-skill/SKILL.md", "---\nname: wrong-name\ndescription: Use when proofreading.\n---\n")
        self.assert_rejected("frontmatter name")

    def test_rejects_empty_description(self):
        self.replace_file("skills/test-skill/SKILL.md", "---\nname: test-skill\ndescription: \n---\n")
        self.assert_rejected("description")

    def test_accepts_description_at_1024_character_limit(self):
        self.replace_file("skills/test-skill/SKILL.md", "---\nname: test-skill\ndescription: " + "a" * 1024 + "\n---\n")
        self.assertEqual(self.run_validation()["status"], "STATIC_GO")

    def test_rejects_description_above_limit(self):
        self.replace_file("skills/test-skill/SKILL.md", "---\nname: test-skill\ndescription: " + "a" * 1025 + "\n---\n")
        self.assert_rejected("description")

    def test_rejects_duplicate_frontmatter_keys(self):
        self.replace_file("skills/test-skill/SKILL.md", "---\nname: test-skill\nname: test-skill\ndescription: Use when proofreading.\n---\n")
        self.assert_rejected("duplicate frontmatter")

    def test_accepts_remote_and_fragment_links_without_network(self):
        self.replace_file("skills/test-skill/references/checks.md", "# Checks\n[web](https://example.invalid) [self](#checks)\n")
        self.assertEqual(self.run_validation()["status"], "STATIC_GO")

    def test_rejects_private_inventory_repository(self):
        self.inventory["repositories"][0]["visibility"] = "private"
        self.assert_rejected("public")

    def test_rejects_undeclared_inventory_artifact(self):
        self.inventory["artifacts"][0]["repository"] = "secret/repo"
        self.assert_rejected("undeclared")

    def test_rejects_inventory_snapshot_mismatch(self):
        self.inventory["artifacts"][0]["commit_sha"] = "c" * 40
        self.assert_rejected("snapshot")

    def test_reports_malformed_json_without_exception(self):
        self.run_validation()
        (self.root / "catalog.json").write_text("{", encoding="utf-8")
        result = self.module.validate(self.root)
        self.assertEqual(result["status"], "REWORK")
        self.assertTrue(result["errors"])

    def test_reports_wrong_schema_types_without_exception(self):
        self.catalog["skills"] = None
        self.assert_rejected("skills")

    def test_rejects_symlinked_metadata_directory(self):
        (self.root / "inventory").symlink_to(self.root.parent, target_is_directory=True)
        result = self.module.validate(self.root)
        self.assertEqual(result["status"], "REWORK")
        self.assertTrue(any("symlink" in e for e in result["errors"]))

    def test_rejects_missing_reference_style_dependency(self):
        self.replace_file("skills/test-skill/references/checks.md", "Read [extra].\n\n[extra]: missing.md\n")
        self.assert_rejected("missing local link")

    def test_rejects_empty_bundle_catalog(self):
        self.catalog["skills"] = []
        self.lock["sources"] = []
        for file in (self.root / "skills").rglob("*"):
            if file.is_file():
                file.unlink()
        self.assert_rejected("nonempty")

    def test_reports_malformed_link_without_exception(self):
        self.replace_file("skills/test-skill/references/checks.md", "[broken](http://[bad)\n")
        self.assert_rejected("malformed link")

    def test_rejects_unhashable_review_status_without_exception(self):
        self.lock["sources"][0]["review_status"] = []
        self.assert_rejected("review")

    def test_cli_malformed_review_status_still_returns_json(self):
        self.lock["sources"][0]["review_status"] = []
        self.run_validation_without_call()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["status"], "REWORK")
        self.assertEqual(result.stderr, "")

    def run_validation_without_call(self):
        for path, value in [("sources.lock.json", self.lock), ("catalog.json", self.catalog), ("inventory/public.json", self.inventory)]:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(value), encoding="utf-8")

    def test_rejects_source_commit_not_matching_inventory(self):
        self.lock["sources"][0]["commit_sha"] = "0" * 40
        self.assert_rejected("source snapshot")

    def test_rejects_source_repository_outside_public_inventory(self):
        self.lock["sources"][0]["repository"] = "not-in/inventory"
        self.assert_rejected("source repository")

    def test_rejects_uninventoried_upstream_skill_path(self):
        self.lock["sources"][0]["files"][0]["upstream_path"] = "nonexistent/SKILL.md"
        self.assert_rejected("upstream artifact")

    def test_rejects_upstream_artifact_blob_mismatch(self):
        self.inventory["artifacts"][0]["blob_sha"] = "0" * 40
        self.assert_rejected("upstream artifact")

    def test_rejects_empty_inventory_artifacts(self):
        self.inventory["artifacts"] = []
        self.assert_rejected("nonempty artifacts")

    def test_rejects_inconsistent_per_repo_kind_counts(self):
        self.inventory["repositories"][0]["counts"]["skill-entry"] = 0
        self.assert_rejected("counts")

    def test_rejects_invalid_counts_type_without_exception(self):
        self.inventory["repositories"][0]["counts"] = []
        self.assert_rejected("counts")

    def test_rejects_inconsistent_inventory_totals(self):
        for field in self.inventory["totals"]:
            with self.subTest(field=field):
                self.inventory["totals"][field] += 1
                self.assert_rejected("totals")
                self.inventory["totals"][field] -= 1

    def test_rejects_boolean_as_inventory_count(self):
        self.inventory["repositories"][0]["files_enumerated"] = True
        self.assert_rejected("files_enumerated")

    def test_rejects_duplicate_groups_not_derived_from_artifacts(self):
        self.inventory["duplicates"] = [{"blob_sha": "0" * 40, "paths": []}]
        self.assert_rejected("duplicate groups")

    def test_accepts_valid_duplicate_groups_with_exact_members(self):
        second = copy.deepcopy(self.inventory["artifacts"][0])
        second["path"] = "copies/test-skill/SKILL.md"
        self.inventory["artifacts"].append(second)
        self.inventory["repositories"][0]["counts"]["skill-entry"] = 2
        self.inventory["totals"].update({"artifacts": 2, "skill_entries": 2, "duplicate_skill_groups": 1})
        self.inventory["duplicates"] = [{"blob_sha": second["blob_sha"], "paths": [
            {key: item[key] for key in ("repository", "path", "mode")} for item in self.inventory["artifacts"]]}]
        self.assertEqual(self.run_validation()["status"], "STATIC_GO")

    def test_rejects_inventory_kind_with_unhashable_type(self):
        self.inventory["artifacts"][0]["kind"] = []
        self.assert_rejected("kind")

    def test_rejects_inventory_mode_with_unhashable_type(self):
        for mode in ([], {}):
            with self.subTest(mode=mode):
                self.inventory["artifacts"][0]["mode"] = mode
                self.assert_rejected("mode")

    def test_rejects_malformed_totals_object_without_exception(self):
        self.inventory["totals"] = []
        self.assert_rejected("totals")

    def test_cli_json_and_exit_status(self):
        self.run_validation()
        good = subprocess.run([sys.executable, str(SCRIPT), str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)["status"], "STATIC_GO")
        (self.root / "skills/test-skill/SKILL.md").write_text("tamper", encoding="utf-8")
        bad = subprocess.run([sys.executable, str(SCRIPT), str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(bad.returncode, 1, bad.stderr)
        self.assertEqual(json.loads(bad.stdout)["status"], "REWORK")


if __name__ == "__main__":
    unittest.main()
