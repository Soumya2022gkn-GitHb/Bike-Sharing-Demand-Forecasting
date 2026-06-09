"""Tests for interactive dashboard scenario helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bsdf.features import FEATURE_COLUMNS
from bsdf.scenario import build_scenario_features


class ScenarioTests(unittest.TestCase):
    """Validate one-row scenario feature generation for the Streamlit UI."""

    def test_build_scenario_features_returns_model_columns(self) -> None:
        features = build_scenario_features(
            season=3,
            year=1,
            month=9,
            hour=17,
            holiday=0,
            weekday=5,
            workingday=1,
            weather=1,
            temperature_celsius=24.0,
            feels_like_celsius=27.0,
            humidity_percent=55.0,
            windspeed_normalized=0.20,
        )

        self.assertEqual(list(features.columns), FEATURE_COLUMNS)
        self.assertEqual(features.shape, (1, len(FEATURE_COLUMNS)))
        self.assertAlmostEqual(features.loc[0, "temp"], 24.0 / 41)
        self.assertAlmostEqual(features.loc[0, "hum"], 0.55)


if __name__ == "__main__":
    unittest.main()

