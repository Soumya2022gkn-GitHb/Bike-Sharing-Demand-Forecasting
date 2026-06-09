# =========================================================
# File: app/app.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
from typing import Dict

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# =========================================================
# Streamlit Configuration
# =========================================================

st.set_page_config(

    page_title="Bike Sharing Demand Forecasting",

    page_icon="🚲",

    layout="wide"
)

# =========================================================
# VERIFY CURRENT FILE
# =========================================================

st.write(
    f"Running File: {__file__}"
)

# =========================================================
# Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "xgboost_model.pkl"
)

# =========================================================
# Expected Feature Columns
# =========================================================

EXPECTED_COLUMNS = [

    'instant',
    'season',
    'yr',
    'mnth',
    'hr',
    'holiday',
    'weekday',
    'workingday',
    'weathersit',
    'temp',
    'atemp',
    'hum',
    'windspeed',
    'casual',
    'registered',
    'day',
    'is_weekend',
    'is_peak_hour',
    'year',
    'quarter',
    'week_of_year',
    'day_of_year',
    'business_hours',
    'late_night',
    'rush_hour',
    'is_summer',
    'is_winter',
    'is_fall',
    'is_spring',
    'weather_severity',
    'hr_sin',
    'hr_cos',
    'mnth_sin',
    'mnth_cos'
]

# =========================================================
# Load Trained Model
# =========================================================


@st.cache_resource
def load_model():

    if not MODEL_PATH.exists():

        st.error(

            f"""
Model file not found.

Expected:
{MODEL_PATH}

Please train the model first:

python training/train_xgboost.py
"""
        )

        st.stop()

    try:

        model = joblib.load(MODEL_PATH)

        return model

    except Exception as error:

        st.error(

            f"""
Failed to load model.

Error:
{error}

IMPORTANT:

Delete old model:
models/xgboost_model.pkl

Then retrain:

python training/train_xgboost.py
"""
        )

        st.stop()


# =========================================================
# Sidebar Inputs
# =========================================================

def get_sidebar_inputs() -> Dict:

    st.sidebar.header(
        "Forecast Inputs"
    )

    season = st.sidebar.selectbox(

        "Season",

        [1, 2, 3, 4],

        format_func=lambda x: {

            1: "Spring",
            2: "Summer",
            3: "Fall",
            4: "Winter"

        }[x]
    )

    year = st.sidebar.selectbox(

        "Year",

        [0, 1],

        format_func=lambda x: {

            0: "2011",
            1: "2012"

        }[x]
    )

    month = st.sidebar.slider(

        "Month",

        1,
        12,
        6
    )

    hour = st.sidebar.slider(

        "Hour",

        0,
        23,
        12
    )

    holiday = st.sidebar.selectbox(

        "Holiday",

        [0, 1]
    )

    weekday = st.sidebar.slider(

        "Weekday",

        0,
        6,
        1
    )

    workingday = st.sidebar.selectbox(

        "Working Day",

        [0, 1]
    )

    weathersit = st.sidebar.selectbox(

        "Weather Condition",

        [1, 2, 3, 4],

        format_func=lambda x: {

            1: "Clear",
            2: "Mist",
            3: "Light Rain",
            4: "Heavy Rain"

        }[x]
    )

    temp = st.sidebar.slider(

        "Temperature",

        0.0,
        1.0,
        0.5
    )

    atemp = st.sidebar.slider(

        "Feels Like Temperature",

        0.0,
        1.0,
        0.5
    )

    hum = st.sidebar.slider(

        "Humidity",

        0.0,
        1.0,
        0.5
    )

    windspeed = st.sidebar.slider(

        "Windspeed",

        0.0,
        1.0,
        0.2
    )

    return {

        "season": season,

        "yr": year,

        "mnth": month,

        "hr": hour,

        "holiday": holiday,

        "weekday": weekday,

        "workingday": workingday,

        "weathersit": weathersit,

        "temp": temp,

        "atemp": atemp,

        "hum": hum,

        "windspeed": windspeed
    }


# =========================================================
# Feature Engineering
# =========================================================

def create_feature_dataframe(
    forecasting_inputs: Dict
) -> pd.DataFrame:
    """
    Create production-ready numeric feature dataframe.
    """

    df = pd.DataFrame({

        key: [value]

        for key, value in forecasting_inputs.items()
    })

    # =====================================================
    # Default Numeric Features
    # =====================================================

    df["instant"] = 0

    df["casual"] = 0

    df["registered"] = 0

    df["day"] = 1

    # =====================================================
    # Time Features
    # =====================================================

    df["year"] = 2011 + df["yr"]

    df["quarter"] = (
        ((df["mnth"] - 1) // 3) + 1
    )

    df["week_of_year"] = 1

    df["day_of_year"] = 1

    # =====================================================
    # Weekend Feature
    # =====================================================

    df["is_weekend"] = (
        df["weekday"].isin([0, 6])
    ).astype(int)

    # =====================================================
    # Peak Hour
    # =====================================================

    df["is_peak_hour"] = (
        df["hr"].isin([7, 8, 9, 17, 18, 19])
    ).astype(int)

    # =====================================================
    # Business Hours
    # =====================================================

    df["business_hours"] = (
        df["hr"].between(9, 17)
    ).astype(int)

    # =====================================================
    # Late Night
    # =====================================================

    df["late_night"] = (
        df["hr"].between(0, 5)
    ).astype(int)

    # =====================================================
    # Rush Hour
    # =====================================================

    df["rush_hour"] = (
        df["hr"].isin([7, 8, 9, 17, 18, 19])
    ).astype(int)

    # =====================================================
    # Seasonal Flags
    # =====================================================

    df["is_summer"] = (
        df["season"] == 2
    ).astype(int)

    df["is_winter"] = (
        df["season"] == 4
    ).astype(int)

    df["is_fall"] = (
        df["season"] == 3
    ).astype(int)

    df["is_spring"] = (
        df["season"] == 1
    ).astype(int)

    # =====================================================
    # Weather Severity
    # =====================================================

    df["weather_severity"] = df["weathersit"]

    # =====================================================
    # Cyclical Features
    # =====================================================

    df["hr_sin"] = np.sin(
        2 * np.pi * df["hr"] / 24
    )

    df["hr_cos"] = np.cos(
        2 * np.pi * df["hr"] / 24
    )

    df["mnth_sin"] = np.sin(
        2 * np.pi * df["mnth"] / 12
    )

    df["mnth_cos"] = np.cos(
        2 * np.pi * df["mnth"] / 12
    )

    # =====================================================
    # EXACT FEATURE ORDER
    # =====================================================

    df = df[EXPECTED_COLUMNS]

    return df


# =========================================================
# Prediction Function
# =========================================================

def generate_prediction(
    model,
    feature_dataframe: pd.DataFrame
) -> float:

    try:

        prediction = model.predict(
            feature_dataframe
        )[0]

        return round(prediction, 2)

    except Exception as error:

        st.error(

            f"""
Prediction Error:

{error}

IMPORTANT FIX:

1. Delete OLD model:
models/xgboost_model.pkl

2. Retrain model:
python training/train_xgboost.py

3. Restart Streamlit:
streamlit run app/app.py
"""
        )

        st.stop()


# =========================================================
# Gauge Chart
# =========================================================

def create_gauge_chart(
    prediction: float
):

    figure = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=prediction,

            title={

                "text":
                "Predicted Bike Demand"
            },

            gauge={

                "axis": {

                    "range": [0, 1000]
                }
            }
        )
    )

    return figure


# =========================================================
# Business Recommendation
# =========================================================

def display_business_recommendation(
    prediction: float
):

    st.subheader(
        "Business Recommendation"
    )

    if prediction < 200:

        st.info(
            "Low bike demand expected."
        )

    elif prediction < 500:

        st.warning(
            "Moderate bike demand expected."
        )

    else:

        st.error(
            "High bike demand expected."
        )


# =========================================================
# Main Application
# =========================================================

def main():

    st.title(
        "🚲 Bike Sharing Demand Forecasting"
    )

    st.markdown(
        """
Forecast hourly bicycle rental demand using:

- seasonal trends,
- weather conditions,
- and operational time features.
"""
    )

    # =====================================================
    # Load Model
    # =====================================================

    model = load_model()

    # =====================================================
    # User Inputs
    # =====================================================

    forecasting_inputs = (
        get_sidebar_inputs()
    )

    # =====================================================
    # Create Feature DataFrame
    # =====================================================

    feature_dataframe = (
        create_feature_dataframe(
            forecasting_inputs
        )
    )

    # =====================================================
    # DEBUG FEATURE COLUMNS
    # =====================================================

    st.write(
        "Feature Columns Sent To Model:"
    )

    st.write(
        feature_dataframe.columns.tolist()
    )

    # =====================================================
    # DEBUG FEATURE DATAFRAME
    # =====================================================

    with st.expander(
        "View Engineered Features"
    ):

        st.dataframe(
            feature_dataframe
        )

    # =====================================================
    # Generate Prediction
    # =====================================================

    if st.button(
        "Generate Forecast"
    ):

        prediction = generate_prediction(

            model,

            feature_dataframe
        )

        st.success(

            f"""
Predicted Hourly Bike Demand:
{prediction:.2f}
"""
        )

        # =================================================
        # Gauge Chart
        # =================================================

        figure = create_gauge_chart(
            prediction
        )

        st.plotly_chart(

            figure,

            use_container_width=True
        )

        # =================================================
        # Recommendation
        # =================================================

        display_business_recommendation(
            prediction
        )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":

    main()
