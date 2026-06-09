"""Feature engineering for hourly bike demand forecasting."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COLUMN = "cnt"
LEAKAGE_COLUMNS = ["instant", "dteday",
                   "timestamp", "casual", "registered", "cnt"]
CATEGORICAL_FEATURES = ["season", "yr", "mnth", "hr",
                        "holiday", "weekday", "workingday", "weathersit"]
NUMERIC_FEATURES = [
    "temp",
    "atemp",
    "hum",
    "windspeed",
    "hour_sin",
    "hour_cos",
    "month_sin",
    "month_cos",
]
FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def add_time_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add cyclical time features for hour and month."""

    featured_data = data.copy()
    featured_data["hour_sin"] = np.sin(2 * np.pi * featured_data["hr"] / 24)
    featured_data["hour_cos"] = np.cos(2 * np.pi * featured_data["hr"] / 24)
    featured_data["month_sin"] = np.sin(2 * np.pi * featured_data["mnth"] / 12)
    featured_data["month_cos"] = np.cos(2 * np.pi * featured_data["mnth"] / 12)
    return featured_data


def create_feature_target_split(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return model features and target without leakage columns."""

    missing_features = set(FEATURE_COLUMNS).difference(data.columns)
    if missing_features:
        raise ValueError(
            f"Missing feature columns: {sorted(missing_features)}")
    return data[FEATURE_COLUMNS].copy(), data[TARGET_COLUMN].copy()


def build_preprocessor(scale_numeric: bool) -> ColumnTransformer:
    """Build preprocessing for categorical encoding and optional scaling."""

    numeric_transformer = StandardScaler() if scale_numeric else "passthrough"
    return ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore",
             sparse_output=False), CATEGORICAL_FEATURES),
            ("numeric", numeric_transformer, NUMERIC_FEATURES),
        ],
        remainder="drop",
    )
