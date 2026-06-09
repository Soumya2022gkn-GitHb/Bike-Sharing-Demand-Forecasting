# =========================================================
# File: training/train_xgboost.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor


# =========================================================
# Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

DATA_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

MODELS_DIRECTORY = (
    PROJECT_ROOT
    / "models"
)

REPORTS_DIRECTORY = (
    PROJECT_ROOT
    / "reports"
)

TRAIN_DATA_FILE = (
    DATA_DIRECTORY
    / "train_dataset.csv"
)

TEST_DATA_FILE = (
    DATA_DIRECTORY
    / "test_dataset.csv"
)

MODEL_OUTPUT_FILE = (
    MODELS_DIRECTORY
    / "xgboost_model.pkl"
)

FEATURE_IMPORTANCE_FILE = (
    REPORTS_DIRECTORY
    / "xgboost_feature_importance.csv"
)

REPORT_FILE = (
    REPORTS_DIRECTORY
    / "xgboost_report.txt"
)

TARGET_COLUMN = "cnt"


# =========================================================
# Expected Features
# MUST MATCH app.py EXACTLY
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
# Utility Functions
# =========================================================

def print_section(
    title: str
) -> None:

    separator = "=" * 60

    print(f"\n{separator}")

    print(f" {title}")

    print(separator)


# =========================================================
# Validate Dataset
# =========================================================

def validate_dataset(
    file_path: Path
) -> None:

    if not file_path.exists():

        raise FileNotFoundError(

            f"""
Dataset file not found.

Expected:
{file_path}
"""
        )


# =========================================================
# Load Dataset
# =========================================================

def load_dataset(
    file_path: Path
) -> pd.DataFrame:

    dataframe = pd.read_csv(
        file_path
    )

    return dataframe


# =========================================================
# Feature Engineering
# =========================================================

def engineer_features(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Create EXACT SAME features as app.py
    """

    dataframe = dataframe.copy()

    # =====================================================
    # Default Features
    # =====================================================

    if "instant" not in dataframe.columns:

        dataframe["instant"] = 0

    if "casual" not in dataframe.columns:

        dataframe["casual"] = 0

    if "registered" not in dataframe.columns:

        dataframe["registered"] = 0

    if "day" not in dataframe.columns:

        dataframe["day"] = 1

    # =====================================================
    # Time Features
    # =====================================================

    dataframe["year"] = (
        2011 + dataframe["yr"]
    )

    dataframe["quarter"] = (
        ((dataframe["mnth"] - 1) // 3) + 1
    )

    dataframe["week_of_year"] = 1

    dataframe["day_of_year"] = 1

    # =====================================================
    # Weekend
    # =====================================================

    dataframe["is_weekend"] = (

        dataframe["weekday"].isin([0, 6])

    ).astype(int)

    # =====================================================
    # Peak Hour
    # =====================================================

    dataframe["is_peak_hour"] = (

        dataframe["hr"].isin(
            [7, 8, 9, 17, 18, 19]
        )

    ).astype(int)

    # =====================================================
    # Business Hours
    # =====================================================

    dataframe["business_hours"] = (

        dataframe["hr"].between(9, 17)

    ).astype(int)

    # =====================================================
    # Late Night
    # =====================================================

    dataframe["late_night"] = (

        dataframe["hr"].between(0, 5)

    ).astype(int)

    # =====================================================
    # Rush Hour
    # =====================================================

    dataframe["rush_hour"] = (

        dataframe["hr"].isin(
            [7, 8, 9, 17, 18, 19]
        )

    ).astype(int)

    # =====================================================
    # Seasonal Flags
    # =====================================================

    dataframe["is_summer"] = (

        dataframe["season"] == 2

    ).astype(int)

    dataframe["is_winter"] = (

        dataframe["season"] == 4

    ).astype(int)

    dataframe["is_fall"] = (

        dataframe["season"] == 3

    ).astype(int)

    dataframe["is_spring"] = (

        dataframe["season"] == 1

    ).astype(int)

    # =====================================================
    # Weather Severity
    # =====================================================

    dataframe["weather_severity"] = (
        dataframe["weathersit"]
    )

    # =====================================================
    # Cyclical Features
    # =====================================================

    dataframe["hr_sin"] = np.sin(
        2 * np.pi * dataframe["hr"] / 24
    )

    dataframe["hr_cos"] = np.cos(
        2 * np.pi * dataframe["hr"] / 24
    )

    dataframe["mnth_sin"] = np.sin(
        2 * np.pi * dataframe["mnth"] / 12
    )

    dataframe["mnth_cos"] = np.cos(
        2 * np.pi * dataframe["mnth"] / 12
    )

    return dataframe


# =========================================================
# Split Features & Target
# =========================================================

def split_features_target(
    dataframe: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.Series]:

    dataframe = engineer_features(
        dataframe
    )

    features = dataframe[
        EXPECTED_COLUMNS
    ]

    target = dataframe[
        TARGET_COLUMN
    ]

    return features, target


# =========================================================
# Prepare Training Data
# =========================================================

def prepare_training_data(
    train_dataframe: pd.DataFrame,
    test_dataframe: pd.DataFrame
):

    print_section(
        "Preparing Training Data"
    )

    x_train, y_train = (
        split_features_target(
            train_dataframe
        )
    )

    x_test, y_test = (
        split_features_target(
            test_dataframe
        )
    )

    print("\nTraining Features:")

    print(
        x_train.columns.tolist()
    )

    print(
        f"\nTraining Shape: "
        f"{x_train.shape}"
    )

    print(
        f"Testing Shape: "
        f"{x_test.shape}"
    )

    return (
        x_train,
        y_train,
        x_test,
        y_test
    )


# =========================================================
# Initialize Model
# =========================================================

def initialize_model():

    print_section(
        "Initializing XGBoost Model"
    )

    model = XGBRegressor(

        n_estimators=300,

        learning_rate=0.05,

        max_depth=8,

        subsample=0.8,

        colsample_bytree=0.8,

        objective="reg:squarederror",

        random_state=42,

        n_jobs=-1
    )

    return model


# =========================================================
# Train Model
# =========================================================

def train_model(
    model,
    x_train,
    y_train
):

    print_section(
        "Training XGBoost Model"
    )

    model.fit(
        x_train,
        y_train
    )

    return model


# =========================================================
# Predict
# =========================================================

def generate_predictions(
    model,
    x_test
):

    predictions = model.predict(
        x_test
    )

    return predictions


# =========================================================
# Evaluate Model
# =========================================================

def evaluate_model(
    y_test,
    predictions
) -> Dict:

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(

        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    metrics = {

        "MAE": round(mae, 2),

        "RMSE": round(rmse, 2),

        "R2_SCORE": round(r2, 4)
    }

    return metrics


# =========================================================
# Display Metrics
# =========================================================

def display_metrics(
    metrics: Dict
):

    print_section(
        "Model Evaluation"
    )

    print(
        f"\nMAE: {metrics['MAE']}"
    )

    print(
        f"RMSE: {metrics['RMSE']}"
    )

    print(
        f"R² Score: {metrics['R2_SCORE']}"
    )


# =========================================================
# Feature Importance
# =========================================================

def generate_feature_importance(
    model,
    feature_columns
):

    dataframe = pd.DataFrame({

        "Feature": feature_columns,

        "Importance":
        model.feature_importances_
    })

    dataframe = dataframe.sort_values(

        by="Importance",

        ascending=False
    )

    return dataframe


# =========================================================
# Save Model
# =========================================================

def save_model(
    model
):

    print_section(
        "Saving Model"
    )

    MODELS_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True
    )

    joblib.dump(

        model,

        MODEL_OUTPUT_FILE
    )

    print(
        f"\nModel Saved:\n"
        f"{MODEL_OUTPUT_FILE}"
    )


# =========================================================
# Save Feature Importance
# =========================================================

def save_feature_importance(
    dataframe: pd.DataFrame
):

    REPORTS_DIRECTORY.mkdir(

        parents=True,

        exist_ok=True
    )

    dataframe.to_csv(

        FEATURE_IMPORTANCE_FILE,

        index=False
    )

    print(
        f"\nFeature Importance Saved:\n"
        f"{FEATURE_IMPORTANCE_FILE}"
    )


# =========================================================
# Save Report
# =========================================================

def save_report(
    metrics: Dict
):

    with open(

        REPORT_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(
            "=====================================\n"
        )

        file.write(
            " XGBoost Model Evaluation Report\n"
        )

        file.write(
            "=====================================\n\n"
        )

        file.write(
            f"MAE: {metrics['MAE']}\n"
        )

        file.write(
            f"RMSE: {metrics['RMSE']}\n"
        )

        file.write(
            f"R² Score: {metrics['R2_SCORE']}\n"
        )

    print(
        f"\nReport Saved:\n"
        f"{REPORT_FILE}"
    )


# =========================================================
# Main Pipeline
# =========================================================

def run_pipeline():

    print_section(
        "Bike Sharing XGBoost Training"
    )

    validate_dataset(
        TRAIN_DATA_FILE
    )

    validate_dataset(
        TEST_DATA_FILE
    )

    train_dataframe = load_dataset(
        TRAIN_DATA_FILE
    )

    test_dataframe = load_dataset(
        TEST_DATA_FILE
    )

    (
        x_train,
        y_train,
        x_test,
        y_test

    ) = prepare_training_data(

        train_dataframe,
        test_dataframe
    )

    model = initialize_model()

    trained_model = train_model(

        model,

        x_train,

        y_train
    )

    predictions = generate_predictions(

        trained_model,

        x_test
    )

    metrics = evaluate_model(

        y_test,

        predictions
    )

    display_metrics(metrics)

    feature_importance_dataframe = (
        generate_feature_importance(

            trained_model,

            x_train.columns
        )
    )

    save_model(
        trained_model
    )

    save_feature_importance(
        feature_importance_dataframe
    )

    save_report(
        metrics
    )

    print_section(
        "Training Completed Successfully"
    )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":

    run_pipeline()
