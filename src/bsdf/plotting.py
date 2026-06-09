"""Plotting helpers for EDA and model diagnostics."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

from bsdf.features import FEATURE_COLUMNS

MODEL_DISPLAY_NAMES = {
    "linear_regression": "Linear Regression",
    "random_forest": "Random Forest",
    "gradient_boosting": "Gradient Boosting",
    "xgboost": "XGBoost",
}
SEASON_LABELS = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter",
}
WEATHER_LABELS = {
    1: "Clear / Few Clouds",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow",
}
WORKING_DAY_LABELS = {
    0: "Weekend / Holiday",
    1: "Working Day",
}


def format_model_name(model_name: str) -> str:
    """Return a business-friendly model name."""

    return MODEL_DISPLAY_NAMES.get(model_name, model_name.replace("_", " ").title())


def save_figure(output_path: Path) -> Path:
    """Save the active matplotlib figure."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    return output_path


def plot_demand_trends(data: pd.DataFrame, output_path: Path) -> Path:
    """Plot hourly target distribution and daily demand trend."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    axes[0].hist(data["cnt"], bins=50, color="#2c7fb8", edgecolor="white")
    axes[0].set_title("Distribution of hourly rentals")
    axes[0].set_xlabel("Hourly rental count")
    daily = data.set_index("timestamp")["cnt"].resample("D").sum()
    daily.plot(ax=axes[1], color="#41ab5d")
    axes[1].set_title("Daily rentals over time")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Daily rental count")
    return save_figure(output_path)


def plot_weather_demand_analysis(data: pd.DataFrame, output_path: Path) -> Path:
    """Plot demand by working day, season, and weather situation."""

    fig, axes = plt.subplots(1, 3, figsize=(18, 4))
    hourly_workingday = data.groupby(["hr", "workingday"], as_index=False)["cnt"].mean()
    for workingday, group in hourly_workingday.groupby("workingday"):
        axes[0].plot(group["hr"], group["cnt"], marker="o", label=WORKING_DAY_LABELS.get(workingday, workingday))
    axes[0].set_title("Hourly demand by working day")
    axes[0].set_xlabel("Hour")
    axes[0].set_ylabel("Average rentals")
    axes[0].legend()

    seasonal_demand = data.groupby("season")["cnt"].mean().rename(index=SEASON_LABELS)
    seasonal_demand.plot(kind="bar", ax=axes[1], color="#fdae61")
    axes[1].set_title("Average demand by season")
    axes[1].set_xlabel("Season")
    axes[1].set_ylabel("Average rentals")
    axes[1].tick_params(axis="x", rotation=0)

    weather_demand = data.groupby("weathersit")["cnt"].mean().rename(index=WEATHER_LABELS)
    weather_demand.plot(kind="bar", ax=axes[2], color="#8073ac")
    axes[2].set_title("Average demand by weather")
    axes[2].set_xlabel("Weather situation")
    axes[2].set_ylabel("Average rentals")
    axes[2].tick_params(axis="x", rotation=20)
    return save_figure(output_path)


def plot_correlation_heatmap(data: pd.DataFrame, output_path: Path) -> Path:
    """Plot a correlation heat map for continuous variables."""

    numeric_columns = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
    correlation = data[numeric_columns].corr()
    plt.figure(figsize=(8, 6))
    plt.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(label="Correlation")
    plt.xticks(range(len(numeric_columns)), numeric_columns, rotation=45, ha="right")
    plt.yticks(range(len(numeric_columns)), numeric_columns)
    for row_index, row_name in enumerate(numeric_columns):
        for column_index, column_name in enumerate(numeric_columns):
            value = correlation.loc[row_name, column_name]
            plt.text(column_index, row_index, f"{value:.2f}", ha="center", va="center", color="black")
    plt.title("Correlation heat map")
    return save_figure(output_path)


def plot_error_distribution(prediction_frame: pd.DataFrame, output_path: Path) -> Path:
    """Plot actual vs forecast and the absolute error distribution."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    sample = prediction_frame.tail(14 * 24)
    axes[0].plot(sample["timestamp"], sample["cnt"], label="Actual", color="#2b8cbe")
    axes[0].plot(sample["timestamp"], sample["prediction"], label="Forecast", color="#e34a33")
    axes[0].set_title("Actual vs forecast - last 14 test days")
    axes[0].set_xlabel("Timestamp")
    axes[0].set_ylabel("Hourly rentals")
    axes[0].legend()
    axes[0].tick_params(axis="x", rotation=30)
    axes[1].hist(prediction_frame["absolute_error"], bins=40, color="#756bb1", edgecolor="white")
    axes[1].set_title("Absolute forecast error")
    axes[1].set_xlabel("Absolute error in hourly rentals")
    return save_figure(output_path)


def plot_feature_importance(model, X_test: pd.DataFrame, y_test: pd.Series, output_path: Path) -> pd.DataFrame:
    """Plot permutation importance and return the importance table."""

    importance = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=8,
        random_state=42,
        scoring="neg_mean_absolute_error",
    )
    importance_frame = (
        pd.DataFrame({"feature": FEATURE_COLUMNS, "importance": importance.importances_mean})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    plt.figure(figsize=(8, 5))
    plt.barh(importance_frame["feature"], importance_frame["importance"], color="#31a354")
    plt.gca().invert_yaxis()
    plt.title("Permutation importance on the test period")
    plt.xlabel("Increase in MAE when feature is shuffled")
    plt.ylabel("Feature")
    save_figure(output_path)
    return importance_frame


def plot_model_comparison(comparison: pd.DataFrame, output_path: Path) -> Path:
    """Plot model comparison by mean absolute deviation."""

    ordered = comparison.sort_values("mean_absolute_deviation", ascending=True)
    plt.figure(figsize=(8, 4))
    colors = ["#2ca25f" if index == 0 else "#74a9cf" for index in range(len(ordered))]
    labels = [format_model_name(model_name) for model_name in ordered["model"]]
    plt.barh(labels, ordered["mean_absolute_deviation"], color=colors)
    plt.gca().invert_yaxis()
    plt.title("Model comparison by mean absolute deviation")
    plt.xlabel("Mean absolute deviation, hourly rentals")
    plt.ylabel("Model")
    for row_index, value in enumerate(ordered["mean_absolute_deviation"]):
        plt.text(value + 1, row_index, f"{value:.2f}", va="center")
    return save_figure(output_path)


def plot_model_metric_comparison(comparison: pd.DataFrame, output_path: Path) -> Path:
    """Plot MAD, MAPE, and R-squared for every trained model."""

    metrics = [
        ("mean_absolute_deviation", "MAD\n(lower is better)", True),
        ("mean_absolute_percentage_error", "MAPE\n(lower is better)", True),
        ("r2_score", "R-squared\n(higher is better)", False),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))

    for axis, (metric, title, lower_is_better) in zip(axes, metrics):
        ordered = comparison.sort_values(metric, ascending=lower_is_better)
        labels = [format_model_name(model_name) for model_name in ordered["model"]]
        values = ordered[metric]
        colors = ["#2ca25f" if index == 0 else "#9ecae1" for index in range(len(ordered))]

        axis.barh(labels, values, color=colors)
        axis.invert_yaxis()
        axis.set_title(title)
        axis.set_xlabel(metric.replace("_", " ").title())
        for row_index, value in enumerate(values):
            axis.text(value + max(values) * 0.02, row_index, f"{value:.3f}", va="center")

    return save_figure(output_path)


def plot_model_forecast_comparison(
    models: dict[str, object],
    test_data: pd.DataFrame,
    X_test: pd.DataFrame,
    output_path: Path,
    hours: int = 7 * 24,
) -> Path:
    """Plot actual demand against each model forecast for a recent test window."""

    sample = test_data.tail(hours).copy()
    X_sample = X_test.tail(hours)

    plt.figure(figsize=(14, 5))
    plt.plot(sample["timestamp"], sample["cnt"], label="Actual", color="#111111", linewidth=2.4)

    palette = {
        "linear_regression": "#9e9ac8",
        "random_forest": "#3182bd",
        "gradient_boosting": "#fd8d3c",
        "xgboost": "#31a354",
    }
    for model_name, model in models.items():
        predictions = np.clip(model.predict(X_sample), a_min=0, a_max=None)
        plt.plot(
            sample["timestamp"],
            predictions,
            label=format_model_name(model_name),
            color=palette.get(model_name),
            linewidth=1.4,
            alpha=0.9,
        )

    plt.title("Forecast comparison by model - last 7 test days")
    plt.xlabel("Timestamp")
    plt.ylabel("Hourly rentals")
    plt.legend(ncol=3)
    plt.xticks(rotation=30)
    return save_figure(output_path)


def plot_model_error_by_hour(
    models: dict[str, object],
    test_data: pd.DataFrame,
    X_test: pd.DataFrame,
    output_path: Path,
) -> pd.DataFrame:
    """Plot mean absolute error by hour for each trained model."""

    error_frames = []
    for model_name, model in models.items():
        predictions = np.clip(model.predict(X_test), a_min=0, a_max=None)
        model_errors = pd.DataFrame(
            {
                "model": format_model_name(model_name),
                "hr": test_data["hr"].to_numpy(),
                "absolute_error": np.abs(test_data["cnt"].to_numpy() - predictions),
            }
        )
        error_frames.append(model_errors)

    error_by_hour = (
        pd.concat(error_frames, ignore_index=True)
        .groupby(["model", "hr"], as_index=False)["absolute_error"]
        .mean()
    )

    plt.figure(figsize=(12, 5))
    for model_name, group in error_by_hour.groupby("model"):
        plt.plot(group["hr"], group["absolute_error"], marker="o", label=model_name)

    plt.title("Mean absolute error by hour and model")
    plt.xlabel("Hour of day")
    plt.ylabel("Mean absolute error")
    plt.xticks(range(0, 24))
    plt.legend(ncol=2)
    save_figure(output_path)
    return error_by_hour
