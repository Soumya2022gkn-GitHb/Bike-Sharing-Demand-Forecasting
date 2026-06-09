"""Tests for feature engineering."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bsdf.features import add_time_features, create_feature_target_split
from bsdf.modeling import build_candidate_models


class FeatureTests(unittest.TestCase):
    """Validate feature transformations."""

    def test_add_time_features_creates_cyclical_columns(self) -> None:
        data = pd.DataFrame({"hr": [0, 12], "mnth": [1, 7]})
        featured = add_time_features(data)

        for column in ["hour_sin", "hour_cos", "month_sin", "month_cos"]:
            self.assertIn(column, featured.columns)

    def test_create_feature_target_split_excludes_target(self) -> None:
        data = pd.DataFrame(
            {
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
                "hour_sin": [0.0],
                "hour_cos": [1.0],
                "month_sin": [0.5],
                "month_cos": [0.87],
                "cnt": [16],
            }
        )
        features, target = create_feature_target_split(data)

        self.assertNotIn("cnt", features.columns)
        self.assertEqual(target.iloc[0], 16)

    def test_candidate_models_include_xgboost_when_installed(self) -> None:
        models = build_candidate_models(random_state=42)

        self.assertIn("linear_regression", models)
        self.assertIn("random_forest", models)
        self.assertIn("gradient_boosting", models)
        self.assertIn("xgboost", models)


if __name__ == "__main__":
    unittest.main()
