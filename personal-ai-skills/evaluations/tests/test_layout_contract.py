"""The user's canonical tree is a required, populated structure."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]

class CanonicalLayout(unittest.TestCase):
    def test_required_top_level_files_exist(self):
        for rel in ["README.md","registry.yaml","governance/security-policy.md","governance/quality-gates.md","governance/data-classification.md"]:
            with self.subTest(path=rel):
                self.assertTrue((ROOT/rel).is_file(), "Required canonical file has not been built")

    def test_all_three_core_packages_are_populated(self):
        for name in ["review-academic-thesis","audit-branch-kpi","review-code-change"]:
            with self.subTest(skill=name):
                folder=ROOT/"skills"/name
                self.assertTrue((folder/"SKILL.md").is_file(), "Required core skill is missing")
                for sub in ["references","assets","scripts","tests"]:
                    self.assertTrue((folder/sub).is_dir(),sub)
                    useful=[p for p in (folder/sub).rglob("*") if p.is_file() and p.name!=".gitkeep" and "__pycache__" not in p.parts]
                    self.assertTrue(useful,f"{name}/{sub} must contain useful resources")

    def test_adapters_have_manifests_and_actual_instructions(self):
        for host in ["chatgpt","gemini","claude","codex"]:
            with self.subTest(host=host):
                self.assertTrue((ROOT/"adapters"/host/"adapter.yaml").is_file())
                self.assertTrue((ROOT/"adapters"/host/"README.md").is_file())

    def test_fixture_and_report_directories_contain_evidence(self):
        for rel in ["evaluations/fixtures","evaluations/reports"]:
            self.assertTrue((ROOT/rel).is_dir())
            self.assertTrue(any(p.is_file() and p.name!=".gitkeep" for p in (ROOT/rel).rglob("*")))

if __name__=="__main__":
    unittest.main()

