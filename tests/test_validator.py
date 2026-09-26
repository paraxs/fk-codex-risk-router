"""Mutation checks for published routing and activation contract."""

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

    def test_current_package(self):
        self.assertEqual(validate(self.files), "0.5.0")

    def test_route_gap(self):
        self.rejects("SKILL.md", "C 4–6", "C 5–6", "route gap")

    def test_route_overlap(self):
        self.rejects("SKILL.md", "C 4–6", "C 3–6", "route overlap")

    def test_old_model_returns(self):
        self.rejects("SKILL.md", "`gpt-6-luna`", "`gpt-5.6-luna`", "model IDs")

    def test_astra_implementation_returns(self):
        self.rejects("SKILL.md", "It must not implement patches", "It may implement patches", "supervisor/budget rule")

    def test_budget_increase(self):
        self.rejects("SKILL.md", "max_dispatches = 4", "max_dispatches = 20", "supervisor/budget rule")

    def test_implicit_activation(self):
        self.rejects("agents/openai.yaml", "allow_implicit_invocation: false", "allow_implicit_invocation: true", "activation policy")

    def test_wrong_invocation(self):
        self.rejects("agents/openai.yaml", "$codex-risk-router", "$other-router", "metadata invocation")

    def test_broken_reference(self):
        self.rejects("SKILL.md", "references/cost-control.md", "references/missing.md", "broken link")

    def test_version_drift(self):
        self.rejects("README.md", "Router 0.5.0", "Router 0.4.0", "version drift")


if __name__ == "__main__":
    unittest.main()
