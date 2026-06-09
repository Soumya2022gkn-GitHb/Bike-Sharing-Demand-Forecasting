"""Model evaluation and forecast analysis utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict[str, float]:
    """Evaluate a fitted model with business-friendly regression metrics."""

    predictions = np.clip(model.predict(X_test), a_min=0, a_max=None)
    return {
        "mean_absolute_deviation": mean_absolute_error(y_test, predictions),
        "mean_absolute_percentage_error": mean_absolute_percentage_error(y_test, predictions),
        "r2_score": r2_score(y_test, predictions),
    }


def compare_models(models: dict, X_test: pd.DataFrame, y_test: pd.Series) -> pd.DataFrame:
    """Compare all fitted models on the same test period."""

    rows = []
    for model_name, model in models.items():
        metrics = evaluate_model(model, X_test, y_test)
        rows.append({"model": model_name, **metrics})
    return pd.DataFrame(rows).sort_values("mean_absolute_deviation").reset_index(drop=True)


def build_prediction_frame(model, test_data: pd.DataFrame, X_test: pd.DataFrame) -> pd.DataFrame:
    """Create a timestamped forecast frame with absolute errors."""

    predictions = np.clip(model.predict(X_test), a_min=0, a_max=None)
    prediction_frame = test_data[["timestamp", "cnt", "hr", "weekday", "workingday", "weathersit"]].copy()
    prediction_frame["prediction"] = predictions
    prediction_frame["absolute_error"] = (prediction_frame["cnt"] - prediction_frame["prediction"]).abs()
    return prediction_frame


def summarize_error_by_hour(prediction_frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize forecast error by hour of day."""

    return (
        prediction_frame.groupby("hr", as_index=False)
        .agg(actual_mean=("cnt", "mean"), prediction_mean=("prediction", "mean"), mad=("absolute_error", "mean"))
        .round(2)
    )


def summarize_forecast_by_day(prediction_frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize actual and forecast demand by calendar day."""

    daily = prediction_frame.copy()
    daily["date"] = daily["timestamp"].dt.date
    return (
        daily.groupby("date", as_index=False)
        .agg(actual_total=("cnt", "sum"), predicted_total=("prediction", "sum"), mad=("absolute_error", "mean"))
        .round(2)
    )

