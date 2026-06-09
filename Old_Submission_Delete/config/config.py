# =========================================================
# File: config/config.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

"""
=========================================================
 Configuration File
=========================================================

This configuration module centralizes all project-wide
settings, constants, file paths, model parameters,
feature settings, and operational forecasting options.

Purpose:
---------------------------------------------------------
1. Improve maintainability
2. Support production deployment
3. Centralize configuration management
4. Simplify environment setup
5. Improve scalability
6. Support collaborative development

Target Variable:
---------------------------------------------------------
cnt -> Hourly Bike Rental Demand

=========================================================
"""


# =========================================================
# Import Required Libraries
# =========================================================

from pathlib import Path


# =========================================================
# Project Root Directory
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# =========================================================
# Data Directories
# =========================================================

DATA_DIR = (
    PROJECT_ROOT
    / "data"
)

RAW_DATA_DIR = (
    DATA_DIR
    / "raw"
)

PROCESSED_DATA_DIR = (
    DATA_DIR
    / "processed"
)


# =========================================================
# Dataset Files
# =========================================================

RAW_DATA_FILE = (
    RAW_DATA_DIR
    / "hour.csv"
)

CLEANED_DATA_FILE = (
    PROCESSED_DATA_DIR
    / "cleaned_bike_data.csv"
)

FEATURE_ENGINEERED_DATA_FILE = (
    PROCESSED_DATA_DIR
    / "feature_engineered_data.csv"
)

TRAIN_DATA_FILE = (
    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

TEST_DATA_FILE = (
    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)


# =========================================================
# Model Directory
# =========================================================

MODELS_DIR = (
    PROJECT_ROOT
    / "models"
)

MODELS_DIR.mkdir(
    exist_ok=True
)


# =========================================================
# Saved Model Files
# =========================================================

LINEAR_REGRESSION_MODEL = (
    MODELS_DIR
    / "linear_regression_model.pkl"
)

RANDOM_FOREST_MODEL = (
    MODELS_DIR
    / "random_forest_model.pkl"
)

XGBOOST_MODEL = (
    MODELS_DIR
    / "xgboost_model.pkl"
)

SCALER_MODEL = (
    MODELS_DIR
    / "scaler.pkl"
)


# =========================================================
# Graphs Directory
# =========================================================

GRAPHS_DIR = (
    PROJECT_ROOT
    / "graphs"
)

GRAPHS_DIR.mkdir(
    exist_ok=True
)


# =========================================================
# Reports Directory
# =========================================================

REPORTS_DIR = (
    PROJECT_ROOT
    / "reports"
)

REPORTS_DIR.mkdir(
    exist_ok=True
)


# =========================================================
# Notebook Directory
# =========================================================

NOTEBOOKS_DIR = (
    PROJECT_ROOT
    / "notebooks"
)

NOTEBOOKS_DIR.mkdir(
    exist_ok=True
)


# =========================================================
# Logging Directory
# =========================================================

LOG_DIR = (
    PROJECT_ROOT
    / "logs"
)

LOG_DIR.mkdir(
    exist_ok=True
)

LOG_FILE = (
    LOG_DIR
    / "bike_forecasting.log"
)


# =========================================================
# Random State
# =========================================================

RANDOM_STATE = 42


# =========================================================
# Train-Test Split Configuration
# =========================================================

TEST_SIZE = 0.20


# =========================================================
# Target Variable
# =========================================================

TARGET_COLUMN = "cnt"


# =========================================================
# Feature Columns
# =========================================================

FEATURE_COLUMNS = [

    "season",
    "yr",
    "mnth",
    "hr",
    "holiday",
    "weekday",
    "workingday",
    "weathersit",
    "temp",
    "atemp",
    "hum",
    "windspeed"
]


# =========================================================
# Categorical Features
# =========================================================

CATEGORICAL_FEATURES = [

    "season",
    "holiday",
    "weekday",
    "workingday",
    "weathersit"
]


# =========================================================
# Numerical Features
# =========================================================

NUMERICAL_FEATURES = [

    "temp",
    "atemp",
    "hum",
    "windspeed",
    "hr",
    "mnth"
]


# =========================================================
# Forecasting Features
# =========================================================

TIME_FEATURES = [

    "hr",
    "weekday",
    "mnth",
    "season"
]


# =========================================================
# Missing Value Strategy
# =========================================================

NUMERIC_MISSING_STRATEGY = "median"

CATEGORICAL_MISSING_STRATEGY = "most_frequent"


# =========================================================
# Scaling Configuration
# =========================================================

SCALING_METHOD = "StandardScaler"


# =========================================================
# Encoding Configuration
# =========================================================

ENCODING_METHOD = "OneHotEncoding"


# =========================================================
# Linear Regression Parameters
# =========================================================

LINEAR_REGRESSION_PARAMS = {

    "fit_intercept": True
}


# =========================================================
# Random Forest Parameters
# =========================================================

RANDOM_FOREST_PARAMS = {

    "n_estimators": 200,

    "max_depth": 15,

    "min_samples_split": 5,

    "min_samples_leaf": 2,

    "random_state": RANDOM_STATE,

    "n_jobs": -1
}


# =========================================================
# XGBoost Parameters
# =========================================================

XGBOOST_PARAMS = {

    "n_estimators": 300,

    "learning_rate": 0.05,

    "max_depth": 8,

    "subsample": 0.8,

    "colsample_bytree": 0.8,

    "objective": "reg:squarederror",

    "random_state": RANDOM_STATE
}


# =========================================================
# Evaluation Metrics
# =========================================================

EVALUATION_METRICS = [

    "MAE",
    "RMSE",
    "R2"
]


# =========================================================
# Streamlit Dashboard Configuration
# =========================================================

STREAMLIT_APP_TITLE = (

    "Bike Sharing Demand Forecasting Dashboard"
)

STREAMLIT_LAYOUT = "wide"


# =========================================================
# Visualization Configuration
# =========================================================

FIGURE_SIZE = (12, 6)

HEATMAP_SIZE = (16, 12)

PLOT_STYLE = "ggplot"

HEATMAP_CMAP = "coolwarm"

SAVE_DPI = 300


# =========================================================
# Graph Output Files
# =========================================================

HOURLY_DEMAND_GRAPH = (
    GRAPHS_DIR
    / "hourly_demand.png"
)

SEASONAL_TRENDS_GRAPH = (
    GRAPHS_DIR
    / "seasonal_trends.png"
)

FEATURE_IMPORTANCE_GRAPH = (
    GRAPHS_DIR
    / "feature_importance.png"
)

PREDICTION_GRAPH = (
    GRAPHS_DIR
    / "prediction_vs_actual.png"
)

ERROR_DISTRIBUTION_GRAPH = (
    GRAPHS_DIR
    / "error_distribution.png"
)

CORRELATION_HEATMAP_GRAPH = (
    GRAPHS_DIR
    / "correlation_heatmap.png"
)


# =========================================================
# Forecasting Configuration
# =========================================================

FORECAST_REFRESH_INTERVAL = "1-3 Hours"

FORECAST_HORIZON = "24-72 Hours"

RETRAINING_FREQUENCY = "Monthly"


# =========================================================
# Production Configuration
# =========================================================

ENABLE_LOGGING = True

ENABLE_MODEL_MONITORING = True

ENABLE_ERROR_TRACKING = True

ENABLE_DATA_VALIDATION = True


# =========================================================
# Weather Labels
# =========================================================

WEATHER_LABELS = {

    1: "Clear",

    2: "Mist",

    3: "Light Rain/Snow",

    4: "Heavy Rain/Snow"
}


# =========================================================
# Season Labels
# =========================================================

SEASON_LABELS = {

    1: "Spring",

    2: "Summer",

    3: "Fall",

    4: "Winter"
}


# =========================================================
# Business Insights
# =========================================================

BUSINESS_OBJECTIVES = [

    "Improve bicycle allocation",

    "Reduce operational shortages",

    "Optimize workforce planning",

    "Improve customer satisfaction",

    "Support logistics forecasting"
]


# =========================================================
# Operational Recommendations
# =========================================================

OPERATIONAL_RECOMMENDATIONS = [

    "Refresh forecasts every 1-3 hours.",

    "Monitor weather-driven demand changes.",

    "Retrain models seasonally.",

    "Use short-term forecasting horizons.",

    "Track model drift continuously."
]


# =========================================================
# Production Notes
# =========================================================

PRODUCTION_NOTES = """

This project is designed using production-ready
engineering practices including:

- Modular architecture
- Reusable pipelines
- Logging and monitoring
- Automated testing
- Exception handling
- Model persistence
- Forecast scalability
- Deployment readiness

"""


# =========================================================
# Display Configuration Summary
# =========================================================

def display_config_summary():
    """
    Display important project configuration details.
    """

    print("\n" + "=" * 60)
    print(" Bike Sharing Forecasting Configuration ")
    print("=" * 60)

    print(f"\nProject Root:")
    print(PROJECT_ROOT)

    print(f"\nRaw Dataset:")
    print(RAW_DATA_FILE)

    print(f"\nProcessed Data Directory:")
    print(PROCESSED_DATA_DIR)

    print(f"\nTarget Variable:")
    print(TARGET_COLUMN)

    print(f"\nForecast Horizon:")
    print(FORECAST_HORIZON)

    print(f"\nForecast Refresh:")
    print(FORECAST_REFRESH_INTERVAL)

    print(f"\nSelected Features:")

    for feature in FEATURE_COLUMNS:

        print(f"- {feature}")

    print("\nConfiguration loaded successfully.")


# =========================================================
# Run Configuration Preview
# =========================================================

if __name__ == "__main__":

    display_config_summary()


# =========================================================
# End of File
# =========================================================
