"""Behavioral checks for the finite Collatz learning exercise."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "collatz_lab.py"
sys.path.insert(0, str(ROOT / "scripts"))


class CollatzObservations(unittest.TestCase):
    def observe(self, start: int, max_steps: int):
        # Import after asserting availability so a missing exercise is a clear failure.
        self.assertTrue(SCRIPT.is_file(), "the bounded Collatz exercise is missing")
        from collatz_lab import observe

        return observe(start, max_steps)

    def test_six_reaches_one_on_the_last_allowed_step(self):
        result = self.observe(6, 8)
        self.assertEqual((result.status, result.steps, result.last, result.peak),
                         ("reached_1", 8, 1, 16))

    def test_cutoff_is_unresolved_instead_of_a_counterexample(self):
        result = self.observe(6, 7)
        self.assertEqual((result.status, result.steps, result.last, result.peak),
                         ("step_limit", 7, 2, 16))

    def test_twenty_seven_matches_the_article_example(self):
        result = self.observe(27, 111)
        self.assertEqual((result.status, result.steps, result.last, result.peak),
                         ("reached_1", 111, 1, 9232))

    def test_one_is_already_reached_without_any_transition(self):
        result = self.observe(1, 0)
        self.assertEqual((result.status, result.steps, result.last, result.peak),
                         ("reached_1", 0, 1, 1))

    def test_zero_budget_preserves_an_unresolved_start(self):
        result = self.observe(6, 0)
        self.assertEqual((result.status, result.steps, result.last, result.peak),
                         ("step_limit", 0, 6, 6))

    def test_even_transition_keeps_large_integers_exact(self):
        result = self.observe(18014398509481986, 1)
        self.assertIs(type(result.last), int)
        self.assertEqual((result.status, result.steps, result.last, result.peak),
                         ("step_limit", 1, 9007199254740993, 18014398509481986))

    def test_odd_transition_is_not_a_combined_odd_and_even_step(self):
        result = self.observe(3, 1)
        self.assertEqual((result.status, result.steps, result.last, result.peak),
                         ("step_limit", 1, 10, 10))

    def test_invalid_domain_is_rejected(self):
        for start, max_steps in [(0, 5), (-1, 5), (6, -1)]:
            with self.subTest(start=start, max_steps=max_steps):
                with self.assertRaises(ValueError):
                    self.observe(start, max_steps)

    def test_cli_emits_the_cutoff_budget_and_finite_scope(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "6", "--max-steps", "7"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual({key: payload[key] for key in
                          ("start", "max_steps", "status", "steps", "last", "peak")},
                         {"start": 6, "max_steps": 7, "status": "step_limit",
                          "steps": 7, "last": 2, "peak": 16})
        self.assertIs(payload["proves_conjecture"], False)
        self.assertTrue(payload["interpretation"])
        self.assertEqual(result.stderr, "")

    def test_cli_rejects_invalid_numbers_without_a_traceback(self):
        for arguments in [("0",), ("-2",), ("6", "--max-steps", "-1"), ("2.5",)]:
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), *arguments],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_cli_reports_a_decimal_output_limit_without_partial_json(self):
        limit = getattr(sys.int_info, "str_digits_check_threshold", 0)
        if not limit:
            self.skipTest("runtime has no decimal integer conversion limit")

        # Use the runtime's supported minimum in this child only, independent of
        # environment configuration. The input fits; one odd step adds a digit.
        command = [sys.executable, "-X", f"int_max_str_digits={limit}",
                   str(SCRIPT), "9" * limit, "--max-steps"]
        control = subprocess.run(command + ["0"], capture_output=True, text=True)
        self.assertEqual(control.returncode, 0, control.stderr)
        self.assertEqual(json.loads(control.stdout)["steps"], 0)

        result = subprocess.run(command + ["1"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
