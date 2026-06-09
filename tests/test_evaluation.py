"""Tests for evaluation helpers."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bsdf.evaluation import summarize_error_by_hour, summarize_forecast_by_day


class EvaluationTests(unittest.TestCase):
    """Validate forecast analysis summaries."""

    def test_summarize_error_by_hour(self) -> None:
        predictions = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(["2011-01-01 00:00", "2011-01-01 00:30"]),
                "hr": [0, 0],
                "cnt": [10, 20],
                "prediction": [12, 16],
                "absolute_error": [2, 4],
            }
        )
        summary = summarize_error_by_hour(predictions)

        self.assertEqual(summary.loc[0, "mad"], 3)

    def test_summarize_forecast_by_day(self) -> None:
        predictions = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(["2011-01-01 00:00", "2011-01-01 01:00"]),
                "cnt": [10, 20],
                "prediction": [12, 16],
                "absolute_error": [2, 4],
            }
        )
        summary = summarize_forecast_by_day(predictions)

        self.assertEqual(summary.loc[0, "actual_total"], 30)
        self.assertEqual(summary.loc[0, "predicted_total"], 28)


if __name__ == "__main__":
    unittest.main()
