"""Package acceptance tests for the two authored domain skills."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("audit-branch-kpi", "review-academic-thesis")

class DomainSkillPackages(unittest.TestCase):
    def test_required_entrypoints_and_notices_exist(self):
        for name in NAMES:
            with self.subTest(name=name):
                self.assertTrue((ROOT/name/"SKILL.md").is_file(), "Requested skill is not yet implemented")
                self.assertIn("MIT License",(ROOT/name/"LICENSE.txt").read_text())

    def test_names_descriptions_and_discovery_metadata(self):
        for name in NAMES:
            with self.subTest(name=name):
                p=ROOT/name/"SKILL.md"
                self.assertTrue(p.is_file(),"Requested skill is not yet implemented")
                text=p.read_text()
                header=re.match(r"\A---\n(.*?)\n---\n",text,re.S)
                self.assertIsNotNone(header)
                fields=dict(re.findall(r"^(name|description|license): (.+)$",header.group(1),re.M))
                self.assertEqual(fields["name"],name)
                description=json.loads(fields["description"])
                self.assertTrue(1<=len(description)<=1024)
                self.assertLess(len(text.splitlines()),500)
                ui=(ROOT/name/"agents/openai.yaml").read_text()
                self.assertIn("$"+name,ui)
                short=re.search(r'^  short_description: (.+)$',ui,re.M).group(1)
                self.assertTrue(25<=len(json.loads(short))<=64)
                self.assertNotIn("allow_implicit_invocation: false",ui)

    def test_relative_resource_closure_and_no_symlinks(self):
        for name in NAMES:
            folder=ROOT/name
            self.assertTrue((folder/"SKILL.md").is_file(),"Requested skill is not yet implemented")
            for p in folder.rglob("*"):
                self.assertFalse(p.is_symlink(),str(p))
                if p.is_file() and p.suffix==".md":
                    for link in re.findall(r"\]\(([^)]+)\)",p.read_text()):
                        if "://" in link or link.startswith("#"):continue
                        dest=(p.parent/link.split("#")[0]).resolve()
                        self.assertTrue(dest.is_relative_to(folder.resolve()),str(p))
                        self.assertTrue(dest.exists(),str(dest))

    def test_guard_is_loaded_by_each_skill(self):
        for name in NAMES:
            entry=ROOT/name/"SKILL.md"
            self.assertTrue(entry.is_file(),"Requested skill is not yet implemented")
            self.assertIn("references/usage-guard.md",entry.read_text())
            guard=(ROOT/name/"references/usage-guard.md").read_text()
            for term in ("SYSTEM","khách hàng","DOI","Spec Kit"):
                self.assertIn(term,guard)

    def test_demo_calculator_fixture_has_no_customer_fields(self):
        path=ROOT/"audit-branch-kpi/assets/demo-ratio.json"
        self.assertTrue(path.is_file(),"Requested helper example is not yet implemented")
        data=json.loads(path.read_text())
        self.assertEqual(data["schema_version"],1)
        self.assertEqual(data["formula"]["operation"],"ratio_pct")
        self.assertEqual(set(data["rows"][0]),{"entity_id","period","unit","numerator","denominator"})

if __name__=="__main__":
    unittest.main()

