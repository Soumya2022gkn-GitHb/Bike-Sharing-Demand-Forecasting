"""Tests for data validation and preprocessing."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bsdf.data import preprocess_hourly_data, validate_hourly_data


class DataTests(unittest.TestCase):
    """Validate the data ingestion contract."""

    def setUp(self) -> None:
        self.raw_data = pd.DataFrame(
            {
                "instant": [1],
                "dteday": ["2011-01-01"],
                "season": [1],
                "yr": [0],
                "mnth": [1],
                "hr": [0],
                "holiday": [0],
                "weekday": [6],
                "workingday": [0],
                "weathersit": [1],
                "temp": [0.24],
                "atemp": [0.2879],
                "hum": [0.81],
                "windspeed": [0.0],
                "casual": [3],
                "registered": [13],
                "cnt": [16],
            }
        )

    def test_validate_accepts_expected_schema(self) -> None:
        validate_hourly_data(self.raw_data)

    def test_preprocess_adds_timestamp(self) -> None:
        processed = preprocess_hourly_data(self.raw_data)
        self.assertIn("timestamp", processed.columns)
        self.assertEqual(processed.loc[0, "timestamp"], pd.Timestamp("2011-01-01"))


if __name__ == "__main__":
    unittest.main()
