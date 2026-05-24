# =========================================================
# File: app/app.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from datetime import datetime

import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# Define Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

MODELS_DIR = (

    PROJECT_ROOT
    / "models"
)

DATA_DIR = (

    PROJECT_ROOT
    / "data"
    / "processed"
)

GRAPHS_DIR = (

    PROJECT_ROOT
    / "graphs"
)


# =========================================================
# Define File Paths
# =========================================================

MODEL_FILE = (

    MODELS_DIR
    / "xgboost_model.pkl"
)

SCALER_FILE = (

    MODELS_DIR
    / "scaler.pkl"
)

DATA_FILE = (

    DATA_DIR
    / "feature_engineered_data.csv"
)


# =========================================================
# Load Model & Data
# =========================================================

@st.cache_resource
def load_model():
    """
    Load trained forecasting model.
    """

    model = joblib.load(

        MODEL_FILE
    )

    return model


@st.cache_resource
def load_scaler():
    """
    Load feature scaler.
    """

    scaler = joblib.load(

        SCALER_FILE
    )

    return scaler


@st.cache_data
def load_dataset():
    """
    Load forecasting dataset.
    """

    dataframe = pd.read_csv(

        DATA_FILE
    )

    return dataframe


# =========================================================
# Initialize Application
# =========================================================

st.set_page_config(

    page_title="Bike Sharing Demand Forecasting",

    page_icon="🚲",

    layout="wide"
)


# =========================================================
# Application Title
# =========================================================

st.title(

    "🚲 Bike Sharing Demand Forecasting"
)

st.markdown(

    """
    Predict hourly bike rental demand using
    Machine Learning and XGBoost Forecasting.
    """
)


# =========================================================
# Load Resources
# =========================================================

try:

    model = load_model()

    scaler = load_scaler()

    df = load_dataset()

except Exception as error:

    st.error(

        f"Error loading resources: {error}"
    )

    st.stop()


# =========================================================
# Sidebar
# =========================================================

st.sidebar.title(

    "Forecast Configuration"
)

st.sidebar.markdown(

    """
    Configure bike rental forecasting inputs.
    """
)


# =========================================================
# User Inputs
# =========================================================

season = st.sidebar.selectbox(

    "Season",

    [1, 2, 3, 4],

    help="""
    1 = Spring
    2 = Summer
    3 = Fall
    4 = Winter
    """
)

year = st.sidebar.selectbox(

    "Year",

    [0, 1],

    help="""
    0 = 2011
    1 = 2012
    """
)

month = st.sidebar.slider(

    "Month",

    1,

    12,

    6
)

hour = st.sidebar.slider(

    "Hour of Day",

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

    2
)

workingday = st.sidebar.selectbox(

    "Working Day",

    [0, 1]
)

weather = st.sidebar.selectbox(

    "Weather Situation",

    [1, 2, 3, 4]
)

temperature = st.sidebar.slider(

    "Temperature",

    0.0,

    1.0,

    0.5
)

feels_like_temp = st.sidebar.slider(

    "Feels Like Temperature",

    0.0,

    1.0,

    0.5
)

humidity = st.sidebar.slider(

    "Humidity",

    0.0,

    1.0,

    0.5
)

windspeed = st.sidebar.slider(

    "Wind Speed",

    0.0,

    1.0,

    0.2
)


# =========================================================
# Create Feature Vector
# =========================================================

input_data = pd.DataFrame({

    "season": [season],

    "yr": [year],

    "mnth": [month],

    "hr": [hour],

    "holiday": [holiday],

    "weekday": [weekday],

    "workingday": [workingday],

    "weathersit": [weather],

    "temp": [temperature],

    "atemp": [feels_like_temp],

    "hum": [humidity],

    "windspeed": [windspeed]
})


# =========================================================
# Prediction Button
# =========================================================

if st.sidebar.button(

    "Generate Forecast"
):

    try:

        # ================================================
        # Generate Prediction
        # ================================================

        prediction = model.predict(

            input_data
        )[0]

        prediction = max(

            0,

            round(prediction)
        )

        # ================================================
        # Display Forecast
        # ================================================

        st.success(

            f"Predicted Hourly Bike Demand: "
            f"{prediction}"
        )

        # ================================================
        # Forecast Category
        # ================================================

        if prediction < 100:

            demand_level = "Low Demand"

        elif prediction < 300:

            demand_level = "Moderate Demand"

        else:

            demand_level = "High Demand"

        st.info(

            f"Demand Category: {demand_level}"
        )

        # ================================================
        # Gauge Visualization
        # ================================================

        gauge_chart = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=prediction,

                title={

                    "text":
                    "Bike Demand Forecast"
                },

                gauge={

                    "axis": {

                        "range": [0, 1000]
                    }
                }
            )
        )

        st.plotly_chart(

            gauge_chart,

            use_container_width=True
        )

    except Exception as error:

        st.error(

            f"Prediction Error: {error}"
        )


# =========================================================
# Dataset Overview
# =========================================================

st.header(

    "📊 Dataset Overview"
)

st.write(

    df.head()
)


# =========================================================
# Dataset Shape
# =========================================================

st.subheader(

    "Dataset Shape"
)

st.write(

    f"Rows: {df.shape[0]}"
)

st.write(

    f"Columns: {df.shape[1]}"
)


# =========================================================
# Hourly Demand Trend
# =========================================================

st.header(

    "📈 Hourly Bike Demand Trend"
)

hourly_demand = (

    df.groupby("hr")["cnt"]
    .mean()
    .reset_index()
)

hourly_chart = px.line(

    hourly_demand,

    x="hr",

    y="cnt",

    markers=True,

    title="Average Hourly Bike Demand"
)

st.plotly_chart(

    hourly_chart,

    use_container_width=True
)


# =========================================================
# Seasonal Demand Trend
# =========================================================

st.header(

    "🌦 Seasonal Demand Analysis"
)

seasonal_demand = (

    df.groupby("season")["cnt"]
    .mean()
    .reset_index()
)

season_chart = px.bar(

    seasonal_demand,

    x="season",

    y="cnt",

    title="Seasonal Bike Demand"
)

st.plotly_chart(

    season_chart,

    use_container_width=True
)


# =========================================================
# Weather Impact
# =========================================================

st.header(

    "☁ Weather Impact on Demand"
)

weather_demand = (

    df.groupby("weathersit")["cnt"]
    .mean()
    .reset_index()
)

weather_chart = px.bar(

    weather_demand,

    x="weathersit",

    y="cnt",

    title="Weather Impact on Bike Demand"
)

st.plotly_chart(

    weather_chart,

    use_container_width=True
)


# =========================================================
# Temperature Correlation
# =========================================================

st.header(

    "🌡 Temperature vs Bike Demand"
)

temp_chart = px.scatter(

    df,

    x="temp",

    y="cnt",

    opacity=0.6,

    title="Temperature vs Bike Demand"
)

st.plotly_chart(

    temp_chart,

    use_container_width=True
)


# =========================================================
# Business Insights
# =========================================================

st.header(

    "💡 Business Insights"
)

business_insights = [

    "Peak-hour demand occurs during commuting hours.",

    "Weather conditions significantly affect rentals.",

    "Weekends show different demand behavior.",

    "Seasonality impacts operational planning.",

    "Short-term forecasting improves bicycle logistics."
]

for insight in business_insights:

    st.markdown(

        f"- {insight}"
    )


# =========================================================
# Operational Recommendations
# =========================================================

st.header(

    "⚙ Operational Recommendations"
)

recommendations = [

    "Refresh forecasts every 1-3 hours.",

    "Monitor peak-hour demand closely.",

    "Increase bike availability during high demand.",

    "Use weather forecasts for operational planning.",

    "Retrain forecasting models seasonally."
]

for recommendation in recommendations:

    st.markdown(

        f"- {recommendation}"
    )


# =========================================================
# Forecasting Summary
# =========================================================

st.header(

    "📌 Forecasting Summary"
)

st.markdown(

    """
    The Bike Sharing Demand Forecasting system
    predicts hourly bicycle rental demand using
    machine learning and operational forecasting.

    The forecasting pipeline supports:
    - demand prediction,
    - logistics optimization,
    - staffing planning,
    - and operational decision-making.

    XGBoost was selected because it:
    - handles nonlinear demand patterns,
    - captures seasonality effectively,
    - models weather influence,
    - and delivers strong forecasting accuracy.
    """
)


# =========================================================
# Footer
# =========================================================

st.markdown("---")

st.caption(

    f"""
    Bike Sharing Demand Forecasting System
    | Generated on:
    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
)
