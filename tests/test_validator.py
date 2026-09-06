"""Mutation checks for repository validation, not LLM behavior tests."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_router import load_files, validate


class ConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.files = load_files()

    def rejects(self, file, old, new, reason):
        self.assertIn(old, self.files[file])
        self.files[file] = self.files[file].replace(old, new, 1)
        with self.assertRaisesRegex(ValueError, reason):
            validate(self.files)

    def test_current_repository(self):
        self.assertEqual(validate(self.files), "0.4.0")

    def test_routing_gap(self):
        self.rejects("SKILL.md", "C 4–6", "C 5–6", "gap")

    def test_routing_overlap(self):
        self.rejects("SKILL.md", "C 4–6", "C 3–6", "overlap")

    def test_readme_routing_drift(self):
        self.rejects("README.md", "C 7–9", "C 7–8", "gap")

    def test_version_drift(self):
        self.rejects("README.md", "router-v0.4.0-", "router-v9.9.9-", "version drift")

    def test_wrong_model(self):
        self.rejects("SKILL.md", "`gpt-5.6-luna`", "`gpt-5.6-typo`", "model IDs")

    def test_implicit_activation(self):
        self.rejects(
            "agents/openai.yaml",
            "allow_implicit_invocation: false",
            "allow_implicit_invocation: true",
            "activation policy",
        )

    def test_wrong_invocation(self):
        self.rejects(
            "agents/openai.yaml",
            "$codex-risk-router",
            "$other-router",
            "default invocation",
        )

    def test_missing_icon(self):
        self.rejects(
            "agents/openai.yaml",
            "./assets/icon.svg",
            "./assets/missing.svg",
            "missing icon",
        )

    def test_statistics_schema(self):
        self.rejects(
            "references/statistics.md",
            '"schema_version":2',
            '"schema_version":1',
            "statistics schema",
        )

    def test_statistics_attempt_budget(self):
        self.rejects(
            "references/statistics.md",
            '"implementation_attempts":1',
            '"implementation_attempts":3',
            "attempt budget",
        )

    def test_broken_link(self):
        self.files["SKILL.md"] += "\n[missing](references/missing.md)\n"
        with self.assertRaisesRegex(ValueError, "broken link"):
            validate(self.files)

    def test_required_phase_stop_cannot_disappear(self):
        self.rejects(
            "SKILL.md",
            "the next roadmap phase would begin",
            "all roadmap phases are complete",
            "hardening rule",
        )

    def test_roadmap_is_not_implementation_authority(self):
        self.rejects(
            "SKILL.md",
            "A roadmap is not implementation authorization.",
            "A roadmap may authorize implementation.",
            "hardening rule",
        )


if __name__ == "__main__":
    unittest.main()
