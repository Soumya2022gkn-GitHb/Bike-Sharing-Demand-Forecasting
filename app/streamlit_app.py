"""Streamlit app for bike-sharing demand forecast review."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from bsdf.config import get_config
from bsdf.data import load_processed_data, split_time_ordered_data
from bsdf.evaluation import build_prediction_frame
from bsdf.features import add_time_features, create_feature_target_split
from bsdf.plotting import MODEL_DISPLAY_NAMES, SEASON_LABELS, WEATHER_LABELS
from bsdf.scenario import (
    MODEL_ORDER,
    WEEKDAY_LABELS,
    build_scenario_features,
    get_display_name,
    predict_scenario,
)
from bsdf.utils import load_model


@st.cache_data
def load_forecast_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load actual demand, model comparison, and forecast output."""

    config = get_config(PROJECT_ROOT)
    data = add_time_features(load_processed_data(config))
    comparison_path = config.processed_dir / "model_comparison.csv"
    predictions_path = config.processed_dir / "hourly_predictions_test.csv"
    model_path = config.model_dir / "best_model.joblib"

    if comparison_path.exists():
        comparison = pd.read_csv(comparison_path)
    else:
        comparison = pd.DataFrame()

    if predictions_path.exists():
        predictions = pd.read_csv(predictions_path, parse_dates=["timestamp"])
    elif model_path.exists():
        _, test_data = split_time_ordered_data(data, config.test_fraction)
        X_test, _ = create_feature_target_split(test_data)
        predictions = build_prediction_frame(
            load_model(model_path), test_data, X_test)
    else:
        predictions = pd.DataFrame()

    return data, comparison, predictions


@st.cache_resource
def load_available_models() -> dict[str, object]:
    """Load every trained model artifact available in the project."""

    config = get_config(PROJECT_ROOT)
    models = {}
    for model_name in MODEL_ORDER:
        model_path = config.model_dir / f"{model_name}.joblib"
        if model_path.exists():
            models[model_name] = load_model(model_path)
    return models


def main() -> None:
    """Render the forecast monitoring dashboard."""

    st.set_page_config(
        page_title="Bike-Sharing Demand Forecasting", layout="wide")
    st.title("Bike-Sharing Demand Forecasting")

    data, comparison, predictions = load_forecast_data()
    models = load_available_models()
    if data.empty:
        st.warning("No processed data found. Run notebooks 1 to 4 first.")
        return

    metric_columns = st.columns(3)
    metric_columns[0].metric("Historical rows", f"{len(data):,}")
    metric_columns[1].metric("Average hourly demand",
                             f"{data['cnt'].mean():.1f}")
    metric_columns[2].metric("Peak hourly demand", f"{data['cnt'].max():,.0f}")

    if not comparison.empty:
        st.subheader("Model Comparison")
        st.dataframe(comparison, use_container_width=True)
        best = comparison.iloc[0]
        st.metric("Selected best model", get_display_name(str(best["model"])))
        st.metric("Selected model MAD",
                  f"{best['mean_absolute_deviation']:.2f}")

    st.subheader("Interactive Scenario Prediction")
    if not models:
        st.warning("No trained model artifacts found. Run notebook 3 first.")
    else:
        model_names = list(models.keys())
        default_model = comparison.iloc[0]["model"] if not comparison.empty else model_names[0]
        selected_model = st.selectbox(
            "Model",
            options=model_names,
            index=model_names.index(default_model) if default_model in model_names else 0,
            format_func=get_display_name,
        )

        control_columns = st.columns(4)
        season = control_columns[0].selectbox(
            "Season",
            options=list(SEASON_LABELS.keys()),
            format_func=lambda value: SEASON_LABELS[value],
            index=2,
        )
        month = control_columns[1].slider("Month", min_value=1, max_value=12, value=9)
        hour = control_columns[2].slider("Hour", min_value=0, max_value=23, value=17)
        weather = control_columns[3].selectbox(
            "Weather",
            options=list(WEATHER_LABELS.keys()),
            format_func=lambda value: WEATHER_LABELS[value],
        )

        control_columns = st.columns(4)
        weekday_name = control_columns[0].selectbox("Weekday", options=list(WEEKDAY_LABELS.keys()), index=5)
        workingday = control_columns[1].toggle("Working day", value=True)
        holiday = control_columns[2].toggle("Holiday", value=False)
        year_label = control_columns[3].selectbox("Historical year pattern", options=["2011", "2012"], index=1)

        control_columns = st.columns(4)
        temperature_celsius = control_columns[0].slider("Temperature (C)", 0.0, 41.0, 24.0, 0.5)
        feels_like_celsius = control_columns[1].slider("Feels like (C)", 0.0, 50.0, 27.0, 0.5)
        humidity_percent = control_columns[2].slider("Humidity (%)", 0.0, 100.0, 55.0, 1.0)
        windspeed_normalized = control_columns[3].slider("Windspeed (normalized)", 0.0, 1.0, 0.20, 0.01)

        scenario_features = build_scenario_features(
            season=season,
            year=1 if year_label == "2012" else 0,
            month=month,
            hour=hour,
            holiday=int(holiday),
            weekday=WEEKDAY_LABELS[weekday_name],
            workingday=int(workingday),
            weather=weather,
            temperature_celsius=temperature_celsius,
            feels_like_celsius=feels_like_celsius,
            humidity_percent=humidity_percent,
            windspeed_normalized=windspeed_normalized,
        )
        selected_prediction = predict_scenario({selected_model: models[selected_model]}, scenario_features).iloc[0][
            "predicted_hourly_rentals"
        ]
        st.metric("Predicted hourly rentals", f"{selected_prediction:.0f}")

        scenario_predictions = predict_scenario(models, scenario_features)
        st.dataframe(scenario_predictions, use_container_width=True, hide_index=True)
        st.bar_chart(scenario_predictions.set_index("model_name")["predicted_hourly_rentals"])

        with st.expander("Scenario feature values sent to the model"):
            st.dataframe(scenario_features, use_container_width=True, hide_index=True)

    st.subheader("Demand Trend")
    daily = data.set_index("timestamp")["cnt"].resample("D").sum()
    st.line_chart(daily)

    if not predictions.empty:
        st.subheader("Forecast vs Actual")
        forecast_view = predictions.set_index(
            "timestamp")[["cnt", "prediction"]].tail(14 * 24)
        st.line_chart(forecast_view)

        st.subheader("Error Distribution")
        st.bar_chart(
            predictions["absolute_error"].round().value_counts().sort_index())

    st.subheader("Weather Demand Analysis")
    weather_summary = data.groupby("weathersit", as_index=False)["cnt"].mean()
    st.dataframe(weather_summary.rename(
        columns={"cnt": "average_hourly_demand"}), use_container_width=True)


if __name__ == "__main__":
    main()
