import math
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

from statistical_analysis import bootstrap_improvement, hedges_g


class StatisticalAnalysisTests(unittest.TestCase):
    def test_positive_improvement_and_interval_for_better_candidate(self):
        result = bootstrap_improvement(
            [0.44, 0.45, 0.46, 0.45, 0.44],
            [0.33, 0.34, 0.35, 0.34, 0.33],
            resamples=2_000,
            seed=42,
        )

        self.assertGreater(result["absolute_improvement"], 0.0)
        self.assertGreater(result["percent_improvement"], 0.0)
        self.assertGreater(result["absolute_ci_low"], 0.0)
        self.assertGreater(result["hedges_g"], 0.0)
        self.assertEqual(result["baseline_n"], 5)
        self.assertEqual(result["candidate_n"], 5)

    def test_seed_makes_bootstrap_reproducible(self):
        first = bootstrap_improvement([1.0, 1.2, 0.9], [0.7, 0.8, 0.9], resamples=500, seed=7)
        second = bootstrap_improvement([1.0, 1.2, 0.9], [0.7, 0.8, 0.9], resamples=500, seed=7)

        self.assertEqual(first, second)

    def test_zero_variance_has_no_standardized_effect(self):
        self.assertIsNone(hedges_g([1.0, 1.0], [0.5, 0.5]))

    def test_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            bootstrap_improvement([1.0], [0.5, 0.6])
        with self.assertRaises(ValueError):
            bootstrap_improvement([1.0, math.nan], [0.5, 0.6])
        with self.assertRaises(ValueError):
            bootstrap_improvement([1.0, 1.1], [0.5, 0.6], resamples=99)


if __name__ == "__main__":
    unittest.main()
