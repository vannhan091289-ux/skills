"""Assertions on captured applications; does not rerun a model or prove broad accuracy."""
import json
from pathlib import Path
import re
import unittest

EVIDENCE=Path(__file__).resolve().parents[1]/"evidence"
def load(skill,number):
    return json.loads((EVIDENCE/f"green-{skill}-{number}.json").read_text())

class CapturedApplications(unittest.TestCase):
    def test_five_fresh_samples_per_condition_and_skill_are_present(self):
        for condition in ("baseline","green"):
            for skill in ("kpi","thesis"):
                for n in range(1,6):
                    x=json.loads((EVIDENCE/f"{condition}-{skill}-{n}.json").read_text())
                    self.assertEqual(x["skill"],skill)
                    self.assertEqual(x["sample"],n)
                    self.assertTrue(x["answer"].strip())

    def test_kpi_numbers_scope_and_unresolved_zero_remain_in_outputs(self):
        for n in range(1,6):
            a=load("kpi",n)["answer"]
            self.assertRegex(a,r"73[,.]3333")
            self.assertIn("REWORK",a)
            self.assertRegex(a,r"110|80\s*\+\s*30")
            self.assertRegex(a,r"150|100\s*\+\s*50")
            self.assertTrue("undefined" in a.lower() or "không xác định" in a)
            self.assertRegex(a,r"không (?:xếp|tự đổi|thay|đổi)")
            self.assertIn("snapshot",a.lower())
            self.assertIn("SYSTEM",a)
            self.assertIn("chưa",a.lower())

    def test_thesis_locator_conflict_and_citation_limits_are_preserved(self):
        for n in range(1,6):
            a=load("thesis",n)["answer"]
            self.assertIn("REWORK",a)
            self.assertIn("p12",a);self.assertIn("p24",a);self.assertIn("p38",a)
            self.assertIn("80",a);self.assertIn("120",a)
            self.assertIn("confirmed_inconsistency",a)
            self.assertIn("DOI",a)
            self.assertIn("rubric",a)
            self.assertTrue("không chấm" in a.lower())
            self.assertIn("không",a.lower())
            self.assertNotRegex(a,r"10\.\d{4,9}/\S+")

    def test_applied_reports_respect_requested_word_limit(self):
        for skill in ("kpi","thesis"):
            for n in range(1,6):
                self.assertLess(len(load(skill,n)["answer"].split()),350)

if __name__=="__main__":
    unittest.main()

