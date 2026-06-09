# =========================================================
# File: utils/helpers.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (

    mean_absolute_error,

    mean_squared_error,

    r2_score
)


# =========================================================
# Define Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

DATA_DIR = (

    PROJECT_ROOT
    / "data"
)

PROCESSED_DATA_DIR = (

    DATA_DIR
    / "processed"
)

MODELS_DIR = (

    PROJECT_ROOT
    / "models"
)

REPORTS_DIR = (

    PROJECT_ROOT
    / "reports"
)

GRAPHS_DIR = (

    PROJECT_ROOT
    / "graphs"
)


# =========================================================
# Create Directories
# =========================================================

def create_directories():
    """
    Create required project directories.
    """

    directories = [

        DATA_DIR,

        PROCESSED_DATA_DIR,

        MODELS_DIR,

        REPORTS_DIR,

        GRAPHS_DIR
    ]

    for directory in directories:

        directory.mkdir(

            parents=True,

            exist_ok=True
        )

    print("\nProject directories verified successfully.")


# =========================================================
# Print Section Header
# =========================================================

def print_header(title):
    """
    Print formatted console header.
    """

    print("\n========================================")

    print(f" {title} ")

    print("========================================")


# =========================================================
# Validate File Existence
# =========================================================

def validate_file_exists(file_path):
    """
    Verify file exists.
    """

    file_path = Path(file_path)

    if not file_path.exists():

        raise FileNotFoundError(

            f"Required file not found: {file_path}"
        )

    return True


# =========================================================
# Load CSV Dataset
# =========================================================

def load_csv_dataset(file_path):
    """
    Load CSV dataset safely.
    """

    validate_file_exists(file_path)

    try:

        dataframe = pd.read_csv(

            file_path
        )

        return dataframe

    except Exception as error:

        raise RuntimeError(

            f"Error loading dataset: {error}"
        )


# =========================================================
# Save CSV Dataset
# =========================================================

def save_csv_dataset(dataframe, file_path):
    """
    Save dataframe as CSV.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(

        parents=True,

        exist_ok=True
    )

    try:

        dataframe.to_csv(

            file_path,

            index=False
        )

        print(f"\nDataset saved: {file_path}")

    except Exception as error:

        raise RuntimeError(

            f"Error saving dataset: {error}"
        )


# =========================================================
# Display Dataset Information
# =========================================================

def display_dataset_info(dataframe, dataset_name="Dataset"):
    """
    Display dataset details.
    """

    print_header(

        f"{dataset_name} Information"
    )

    print("\nShape:")

    print(dataframe.shape)

    print("\nColumns:")

    print(list(dataframe.columns))

    print("\nMissing Values:")

    print(

        dataframe.isnull().sum()
    )


# =========================================================
# Check Missing Values
# =========================================================

def check_missing_values(dataframe):
    """
    Return missing value count.
    """

    missing_values = (

        dataframe.isnull()
        .sum()
        .sum()
    )

    return missing_values


# =========================================================
# Check Infinite Values
# =========================================================

def check_infinite_values(dataframe):
    """
    Return infinite value count.
    """

    numeric_dataframe = dataframe.select_dtypes(

        include=[np.number]
    )

    infinite_values = np.isinf(

        numeric_dataframe
    ).sum().sum()

    return infinite_values


# =========================================================
# Validate Target Column
# =========================================================

def validate_target_column(

    dataframe,

    target_column="cnt"
):
    """
    Validate forecasting target column.
    """

    columns = [

        column.lower()
        for column in dataframe.columns
    ]

    if target_column.lower() not in columns:

        raise ValueError(

            f"Target column missing: {target_column}"
        )

    return True


# =========================================================
# Split Features & Target
# =========================================================

def split_features_target(

    dataframe,

    target_column="cnt"
):
    """
    Split dataset into features and target.
    """

    validate_target_column(

        dataframe,

        target_column
    )

    X = dataframe.drop(

        columns=[target_column]
    )

    y = dataframe[target_column]

    return X, y


# =========================================================
# Save Trained Model
# =========================================================

def save_model(

    model,

    file_path
):
    """
    Save machine learning model.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(

        parents=True,

        exist_ok=True
    )

    try:

        joblib.dump(

            model,

            file_path
        )

        print(f"\nModel saved: {file_path}")

    except Exception as error:

        raise RuntimeError(

            f"Error saving model: {error}"
        )


# =========================================================
# Load Trained Model
# =========================================================

def load_model(file_path):
    """
    Load machine learning model.
    """

    validate_file_exists(file_path)

    try:

        model = joblib.load(

            file_path
        )

        return model

    except Exception as error:

        raise RuntimeError(

            f"Error loading model: {error}"
        )


# =========================================================
# Calculate Forecast Metrics
# =========================================================

def calculate_regression_metrics(

    actual_values,

    predicted_values
):
    """
    Calculate forecasting metrics.
    """

    mae = mean_absolute_error(

        actual_values,

        predicted_values
    )

    mse = mean_squared_error(

        actual_values,

        predicted_values
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(

        actual_values,

        predicted_values
    )

    metrics = {

        "MAE": round(mae, 4),

        "RMSE": round(rmse, 4),

        "R2_SCORE": round(r2, 4)
    }

    return metrics


# =========================================================
# Print Forecast Metrics
# =========================================================

def print_regression_metrics(metrics):
    """
    Display regression metrics.
    """

    print_header(

        "Forecast Metrics"
    )

    for metric_name, metric_value in metrics.items():

        print(f"\n{metric_name}: {metric_value}")


# =========================================================
# Generate Timestamp
# =========================================================

def generate_timestamp():
    """
    Generate formatted timestamp.
    """

    timestamp = datetime.now().strftime(

        "%Y-%m-%d_%H-%M-%S"
    )

    return timestamp


# =========================================================
# Validate Dataset Shape
# =========================================================

def validate_dataset_shape(

    dataframe,

    min_rows=100,

    min_columns=5
):
    """
    Validate dataset dimensions.
    """

    rows, columns = dataframe.shape

    if rows < min_rows:

        raise ValueError(

            "Dataset contains too few rows."
        )

    if columns < min_columns:

        raise ValueError(

            "Dataset contains too few columns."
        )

    return True


# =========================================================
# Validate Numerical Features
# =========================================================

def validate_numeric_features(dataframe):
    """
    Validate numeric columns.
    """

    numeric_columns = dataframe.select_dtypes(

        include=[np.number]
    ).columns

    if len(numeric_columns) == 0:

        raise ValueError(

            "No numeric features found."
        )

    return list(numeric_columns)


# =========================================================
# Remove Duplicate Records
# =========================================================

def remove_duplicates(dataframe):
    """
    Remove duplicate rows.
    """

    initial_shape = dataframe.shape[0]

    dataframe = dataframe.drop_duplicates()

    final_shape = dataframe.shape[0]

    removed_rows = initial_shape - final_shape

    print(f"\nRemoved duplicate rows: {removed_rows}")

    return dataframe


# =========================================================
# Normalize Column Names
# =========================================================

def normalize_column_names(dataframe):
    """
    Standardize dataframe column names.
    """

    dataframe.columns = [

        column.strip()
        .lower()
        .replace(" ", "_")

        for column in dataframe.columns
    ]

    return dataframe


# =========================================================
# Create Prediction DataFrame
# =========================================================

def create_prediction_dataframe(

    actual_values,

    predicted_values
):
    """
    Create prediction comparison dataset.
    """

    prediction_df = pd.DataFrame({

        "Actual_Demand": actual_values,

        "Predicted_Demand": predicted_values,

        "Prediction_Error":

            actual_values
            - predicted_values
    })

    return prediction_df


# =========================================================
# Save Prediction Results
# =========================================================

def save_prediction_results(

    dataframe,

    file_name="prediction_results.csv"
):
    """
    Save prediction results.
    """

    REPORTS_DIR.mkdir(

        parents=True,

        exist_ok=True
    )

    output_file = (

        REPORTS_DIR
        / file_name
    )

    dataframe.to_csv(

        output_file,

        index=False
    )

    print(f"\nPrediction results saved: {output_file}")

    return output_file


# =========================================================
# Validate Prediction Values
# =========================================================

def validate_predictions(predictions):
    """
    Validate prediction outputs.
    """

    if np.isnan(predictions).any():

        raise ValueError(

            "NaN predictions detected."
        )

    if np.isinf(predictions).any():

        raise ValueError(

            "Infinite predictions detected."
        )

    if (predictions < 0).any():

        raise ValueError(

            "Negative predictions detected."
        )

    return True


# =========================================================
# Display Business Insights
# =========================================================

def display_business_insights():
    """
    Display forecasting insights.
    """

    print_header(

        "Business Insights"
    )

    insights = [

        "Peak-hour demand drives rental growth.",

        "Weather strongly impacts bike usage.",

        "Weekends show different demand behavior.",

        "Seasonality affects operational planning.",

        "Short-term forecasting improves logistics."
    ]

    for insight in insights:

        print(f"\n- {insight}")


# =========================================================
# Display Operational Recommendations
# =========================================================

def display_operational_recommendations():
    """
    Display deployment recommendations.
    """

    print_header(

        "Operational Recommendations"
    )

    recommendations = [

        "Refresh forecasts every 1-3 hours.",

        "Monitor peak-demand forecasting accuracy.",

        "Retrain forecasting models seasonally.",

        "Integrate weather API updates.",

        "Track operational forecasting drift."
    ]

    for recommendation in recommendations:

        print(f"\n- {recommendation}")


# =========================================================
# End of File
# =========================================================
