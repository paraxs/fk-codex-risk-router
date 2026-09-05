"""Mutation checks for the repository validator, not model-behavior tests."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_router import load_files, routing_table, validate


class ConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.files = load_files()

    def rejects(self, file, old, new, reason):
        self.assertIn(old, self.files[file])
        self.files[file] = self.files[file].replace(old, new, 1)
        with self.assertRaisesRegex(ValueError, reason):
            validate(self.files)

    def test_current_repository(self):
        self.assertRegex(validate(self.files), r"^\d+\.\d+\.\d+$")

    def test_routing_gap(self):
        self.rejects("SKILL.md", "C 4–6", "C 5–6", "Gaps")

    def test_routing_overlap(self):
        self.rejects("SKILL.md", "C 4–6", "C 3–6", "Overlapping")

    def test_routing_parity_even_if_coverage_is_valid(self):
        self.files["README.md"] = self.files["README.md"].replace("| Balanced | C 0–3 | C 4–6 |", "| Balanced | C 0–2 | C 3–6 |")
        with self.assertRaisesRegex(ValueError, "routing drift"):
            validate(self.files)

    def test_routing_duplicate_mode(self):
        self.files["SKILL.md"] += "\n| balanced | C 0–3 | C 4–6 | C 7–8 | C 9–10 |\n"
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate(self.files)

    def test_all_modes_cover_every_complexity(self):
        for routes in routing_table(self.files["SKILL.md"]).values():
            self.assertEqual(set(routes), set(range(11)))

    def test_wrong_model(self):
        self.rejects("SKILL.md", "`gpt-5.6-luna`", "`gpt-5.6-typo`", "model ID")

    def test_readme_version_drift(self):
        self.rejects("README.md", "router-v", "router-v99", "Version drift")

    def test_implicit_activation(self):
        self.rejects("agents/openai.yaml", "allow_implicit_invocation: false", "allow_implicit_invocation: true", "Implicit activation")

    def test_unknown_metadata(self):
        self.files["agents/openai.yaml"] += "  products: [codex]\n"
        with self.assertRaisesRegex(ValueError, "policy key"):
            validate(self.files)

    def test_wrong_invocation(self):
        self.rejects("agents/openai.yaml", "$codex-risk-router", "$other-skill", "invocation")

    def test_missing_icon(self):
        self.rejects("agents/openai.yaml", "./assets/icon.svg", "./assets/missing.svg", "icon path")

    def test_statistics_version(self):
        self.rejects("references/statistics.md", '"router_version":"', '"router_version":"99', "Statistics version")

    def test_missing_statistics_timestamp(self):
        self.rejects("references/statistics.md", '"recorded_at":null,', '', "timestamp")

    def test_statistics_attempt_mismatch(self):
        self.rejects("references/statistics.md", '"retry_count":0', '"retry_count":2', "attempts")

    def test_broken_link(self):
        self.files["SKILL.md"] += "\n[missing](references/missing.md)\n"
        with self.assertRaisesRegex(ValueError, "Broken link"):
            validate(self.files)

    def test_svg_ladder_regression(self):
        self.rejects("docs/risk-router-flow.svg", "no mandatory ladder", "Luna → Terra → Sol → Astra", "mandatory ladder")


if __name__ == "__main__":
    unittest.main()
