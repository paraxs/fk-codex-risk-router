"""Behavioral unit tests for the deterministic v0.4 route helper."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from route import PROCESS_BUDGET, recommend


class RouteTests(unittest.TestCase):
    def test_balanced_routine_change_uses_terra_without_astra_leadership(self):
        result = recommend(5, 2)
        self.assertEqual(result.worker_model, "gpt-5.6-terra")
        self.assertEqual(result.worker_reasoning, "medium")
        self.assertFalse(result.astra_leadership_required)
        self.assertFalse(result.review_required)

    def test_balanced_c9_uses_sol_not_astra(self):
        result = recommend(9, 3)
        self.assertEqual(result.worker_model, "gpt-5.6-sol")
        self.assertEqual(result.worker_reasoning, "high")

    def test_quality_c9_uses_astra(self):
        result = recommend(9, 3, mode="quality")
        self.assertEqual(result.worker_model, "gpt-6-astra")

    def test_mid_risk_review_uses_sol(self):
        result = recommend(6, 5)
        self.assertTrue(result.review_required)
        self.assertEqual(result.review_model, "gpt-5.6-sol")

    def test_high_risk_review_uses_astra(self):
        result = recommend(6, 8)
        self.assertTrue(result.review_required)
        self.assertEqual(result.review_model, "gpt-6-astra")

    def test_partial_validation_requires_review_even_at_low_risk(self):
        result = recommend(2, 1, deterministic_validation=False)
        self.assertTrue(result.review_required)
        self.assertEqual(result.review_model, "gpt-5.6-sol")

    def test_audit_is_astra_led_without_second_reviewer(self):
        result = recommend(7, 2, task_kind="audit")
        self.assertTrue(result.astra_leadership_required)
        self.assertEqual(result.worker_model, "gpt-6-astra")
        self.assertEqual(result.execution_hint, "plan_only")
        self.assertFalse(result.review_required)

    def test_unresolved_c8_diagnosis_uses_astra_leadership_gate(self):
        result = recommend(8, 3, task_kind="diagnosis")
        self.assertTrue(result.astra_leadership_required)
        self.assertEqual(result.worker_model, "gpt-6-astra")

    def test_expensive_leadership_is_explicit_opt_in(self):
        adaptive = recommend(4, 2)
        fixed = recommend(4, 2, leadership="astra")
        self.assertFalse(adaptive.astra_leadership_required)
        self.assertTrue(fixed.astra_leadership_required)

    def test_astra_review_policy_only_upgrades_required_review(self):
        no_review = recommend(3, 2, review="astra")
        required = recommend(5, 4, review="astra")
        self.assertFalse(no_review.review_required)
        self.assertEqual(required.review_model, "gpt-6-astra")

    def test_disabled_astra_worker_falls_back_to_sol(self):
        result = recommend(10, 3, astra="disabled")
        self.assertEqual(result.worker_model, "gpt-5.6-sol")
        self.assertFalse(result.worker_approval_required)

    def test_ask_astra_marks_approval_without_claiming_execution(self):
        result = recommend(10, 3, astra="ask")
        self.assertEqual(result.worker_model, "gpt-6-astra")
        self.assertTrue(result.worker_approval_required)

    def test_plan_only_has_no_worker_or_review(self):
        result = recommend(8, 4, task_kind="plan_only")
        self.assertIsNone(result.worker_model)
        self.assertEqual(result.execution_hint, "plan_only")
        self.assertFalse(result.review_required)

    def test_default_budget_has_hard_global_limits(self):
        result = recommend(5, 5)
        self.assertEqual(result.process_budget["work_units"], 1)
        self.assertEqual(result.process_budget["implementation_workers"], 1)
        self.assertEqual(result.process_budget["implementation_attempts"], 2)
        self.assertEqual(result.process_budget, PROCESS_BUDGET)

    def test_scores_must_be_in_range(self):
        with self.assertRaisesRegex(ValueError, "complexity"):
            recommend(11, 2)
        with self.assertRaisesRegex(ValueError, "risk"):
            recommend(2, -1)


if __name__ == "__main__":
    unittest.main()
