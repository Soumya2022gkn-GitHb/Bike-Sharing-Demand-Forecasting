"""Interactive scenario prediction helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd

from bsdf.features import FEATURE_COLUMNS, add_time_features
from bsdf.plotting import MODEL_DISPLAY_NAMES

MODEL_ORDER = ["xgboost", "random_forest", "gradient_boosting", "linear_regression"]
WEEKDAY_LABELS = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
}


def get_display_name(model_name: str) -> str:
    """Return a clean model name for dashboard display."""

    return MODEL_DISPLAY_NAMES.get(model_name, model_name.replace("_", " ").title())


def build_scenario_features(
    *,
    season: int,
    year: int,
    month: int,
    hour: int,
    holiday: int,
    weekday: int,
    workingday: int,
    weather: int,
    temperature_celsius: float,
    feels_like_celsius: float,
    humidity_percent: float,
    windspeed_normalized: float,
) -> pd.DataFrame:
    """Build a one-row feature frame from user-selected inputs."""

    scenario = pd.DataFrame(
        [
            {
                "season": season,
                "yr": year,
                "mnth": month,
                "hr": hour,
                "holiday": holiday,
                "weekday": weekday,
                "workingday": workingday,
                "weathersit": weather,
                "temp": temperature_celsius / 41,
                "atemp": feels_like_celsius / 50,
                "hum": humidity_percent / 100,
                "windspeed": windspeed_normalized,
            }
        ]
    )
    scenario = add_time_features(scenario)
    return scenario[FEATURE_COLUMNS]


def predict_scenario(models: dict[str, object], features: pd.DataFrame) -> pd.DataFrame:
    """Predict one scenario with every loaded model."""

    rows = []
    for model_name, model in models.items():
        prediction = float(np.clip(model.predict(features)[0], a_min=0, a_max=None))
        rows.append(
            {
                "model": model_name,
                "model_name": get_display_name(model_name),
                "predicted_hourly_rentals": round(prediction, 1),
            }
        )
    return pd.DataFrame(rows).sort_values("predicted_hourly_rentals", ascending=False)

