"""Replay checked synthetic outputs; no model is called by these tests."""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"tests/fixtures/review-cases.json").read_text())

class ThesisReviewContract(unittest.TestCase):
    def test_excerpt_covers_conflict_with_real_packet_locators(self):
        answer=DATA["excerpt"]["answer"]
        for value in ["p12","p24","p38","80","120","confirmed_inconsistency"]:
            self.assertIn(value,answer)

    def test_excerpt_does_not_claim_full_text_review_or_citation_verification(self):
        answer=DATA["excerpt"]["answer"]
        self.assertIn("chưa phải thẩm định toàn văn",answer)
        self.assertIn("không chấm điểm",answer)
        self.assertNotRegex(answer,r"10\.\d{4,9}/\S+")

    def test_positive_rubric_is_simulation_not_certification(self):
        answer=DATA["positive_fulltext_assigned_simulation"]["answer"]
        self.assertIn("100/100",answer)
        self.assertIn("mô phỏng",answer)
        self.assertIn("không phải",answer)

    def test_invalid_weights_and_false_coverage_are_not_accepted(self):
        answer=DATA["boundary_invalid_weights_source_injection"]["answer"]
        self.assertIn("110%",answer)
        self.assertIn("không tự rescale",answer)
        self.assertIn("chưa đọc",answer)

    def test_missing_doi_and_plagiarism_not_filled_in(self):
        answer=DATA["negative_missing_doi_plagiarism"]["answer"]
        self.assertIn("Không có đủ bằng chứng",answer)
        self.assertIn("chưa xác minh",answer)
        self.assertNotRegex(answer,r"10\.\d{4,9}/\S+")

    def test_local_resource_closure(self):
        for md in ROOT.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)",md.read_text()):
                if "://" in link or link.startswith("#"):continue
                target=(md.parent/link.split("#")[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT.resolve()))
                self.assertTrue(target.exists())

if __name__=="__main__":
    unittest.main()

