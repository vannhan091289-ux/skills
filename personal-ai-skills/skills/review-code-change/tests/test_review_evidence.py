"""Replay audited evidence; does not score new prose or invoke a model/repository."""
import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parent / "fixtures/applications.json"
REQUIRED = {"no_formal_spec", "unseen_guard", "sign_scope", "not_executed", "locator_and_coverage"}


def check_audit(row):
    """Bind a manual assessment to the exact response and its quoted evidence."""
    answer = row["answer"]
    if hashlib.sha256(answer.encode()).hexdigest() != row["answer_sha256"]:
        raise ValueError("Assessment is stale: answer changed")
    checks = row["assessment"]
    if set(checks) != REQUIRED:
        raise ValueError("Missing acceptance assessment")
    for check in checks.values():
        if check["accepted"] is not True or not check["quote"] or check["quote"] not in answer:
            raise ValueError("Failed or untraceable manual assessment")
    expected = {"formal_spec_available": False, "spec_pass_claimed": False,
                "whole_function_verified": False, "execution_verified": False,
                "direction": "explicit-domain-or-no-direction"}
    if row["claims"] != expected or any(type(row["claims"][k]) is not bool for k in expected if k != "direction"):
        raise ValueError("Claims exceed supplied packet")


class ReviewEvidence(unittest.TestCase):
    def rows(self):
        return json.loads(DATA.read_text())["responses"]

    def test_five_audited_fresh_context_responses(self):
        rows = self.rows()
        self.assertEqual([r["sample"] for r in rows], list(range(1, 6)))
        for row in rows:
            self.assertEqual(row["condition"], "with-skill-refactor")
            check_audit(row)

    def test_altered_prose_invalidates_assessment(self):
        row = copy.deepcopy(self.rows()[0])
        row["answer"] = "Spec PASS dù không có spec; mọi actual âm đều giảm; toàn hàm chắc chắn trả số."
        with self.assertRaises(ValueError):
            check_audit(row)

    def test_rehashed_prose_without_quoted_evidence_is_rejected(self):
        row = copy.deepcopy(self.rows()[0])
        row["answer"] = "Standards Spec src/ratio.py target +1 tests/test_ratio.py chưa chạy fixture không"
        row["answer_sha256"] = hashlib.sha256(row["answer"].encode()).hexdigest()
        with self.assertRaises(ValueError):
            check_audit(row)

    def test_overclaims_are_rejected(self):
        for key in ("formal_spec_available", "spec_pass_claimed", "whole_function_verified", "execution_verified"):
            with self.subTest(key=key):
                row = copy.deepcopy(self.rows()[0])
                row["claims"][key] = True
                with self.assertRaises(ValueError):
                    check_audit(row)

    def test_wrong_or_missing_sign_assessment_is_rejected(self):
        row = copy.deepcopy(self.rows()[0])
        row["claims"]["direction"] = "decreases-for-all-nonzero-actual"
        with self.assertRaises(ValueError):
            check_audit(row)
        row = copy.deepcopy(self.rows()[0])
        del row["assessment"]["sign_scope"]
        with self.assertRaises(ValueError):
            check_audit(row)

    def test_numeric_zero_is_not_boolean_evidence(self):
        row = copy.deepcopy(self.rows()[0])
        row["claims"]["formal_spec_available"] = 0
        with self.assertRaises(ValueError):
            check_audit(row)

    def test_negative_actual_oracle_contradicts_universal_decrease(self):
        # Independent arithmetic of shown expressions, not execution of target code.
        actual, target = Decimal(-10), Decimal(10)
        old = actual / target * 100
        new = actual / (target + 1) * 100
        self.assertEqual(old, Decimal(-100))
        self.assertGreater(new, old)
        self.assertLess(abs(new), abs(old))
        self.assertAlmostEqual(float(new), -90.9090909091)


if __name__ == "__main__":
    unittest.main()
