# =========================================================
# File: utils/logger.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

import logging
from logging.handlers import RotatingFileHandler

from pathlib import Path
from datetime import datetime


# =========================================================
# Define Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

LOGS_DIR = (

    PROJECT_ROOT
    / "logs"
)

LOGS_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Generate Log File Name
# =========================================================

CURRENT_TIMESTAMP = datetime.now().strftime(

    "%Y-%m-%d_%H-%M-%S"
)

LOG_FILE_NAME = (

    f"bike_forecasting_{CURRENT_TIMESTAMP}.log"
)

LOG_FILE_PATH = (

    LOGS_DIR
    / LOG_FILE_NAME
)


# =========================================================
# Configure Logger Format
# =========================================================

LOG_FORMAT = (

    "%(asctime)s | "
    "%(levelname)s | "
    "%(filename)s | "
    "%(funcName)s | "
    "Line:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# =========================================================
# Create Logger
# =========================================================

LOGGER = logging.getLogger(

    "BikeSharingForecastLogger"
)

LOGGER.setLevel(

    logging.INFO
)


# =========================================================
# Prevent Duplicate Handlers
# =========================================================

if not LOGGER.handlers:

    # =====================================================
    # File Handler
    # =====================================================

    file_handler = RotatingFileHandler(

        LOG_FILE_PATH,

        maxBytes=5 * 1024 * 1024,

        backupCount=5,

        encoding="utf-8"
    )

    file_handler.setLevel(

        logging.INFO
    )

    # =====================================================
    # Console Handler
    # =====================================================

    console_handler = logging.StreamHandler()

    console_handler.setLevel(

        logging.INFO
    )

    # =====================================================
    # Formatter
    # =====================================================

    formatter = logging.Formatter(

        fmt=LOG_FORMAT,

        datefmt=DATE_FORMAT
    )

    file_handler.setFormatter(

        formatter
    )

    console_handler.setFormatter(

        formatter
    )

    # =====================================================
    # Attach Handlers
    # =====================================================

    LOGGER.addHandler(

        file_handler
    )

    LOGGER.addHandler(

        console_handler
    )


# =========================================================
# Logging Helper Functions
# =========================================================

def log_info(message):
    """
    Log informational messages.
    """

    LOGGER.info(message)


def log_warning(message):
    """
    Log warning messages.
    """

    LOGGER.warning(message)


def log_error(message):
    """
    Log error messages.
    """

    LOGGER.error(message)


def log_critical(message):
    """
    Log critical messages.
    """

    LOGGER.critical(message)


def log_debug(message):
    """
    Log debug messages.
    """

    LOGGER.debug(message)


# =========================================================
# Log Pipeline Start
# =========================================================

def log_pipeline_start(

    pipeline_name="Bike Sharing Forecasting Pipeline"
):
    """
    Log pipeline start message.
    """

    LOGGER.info(

        "=" * 60
    )

    LOGGER.info(

        f"Starting Pipeline: {pipeline_name}"
    )

    LOGGER.info(

        "=" * 60
    )


# =========================================================
# Log Pipeline End
# =========================================================

def log_pipeline_end(

    pipeline_name="Bike Sharing Forecasting Pipeline"
):
    """
    Log pipeline completion message.
    """

    LOGGER.info(

        "=" * 60
    )

    LOGGER.info(

        f"Completed Pipeline: {pipeline_name}"
    )

    LOGGER.info(

        "=" * 60
    )


# =========================================================
# Log Dataset Information
# =========================================================

def log_dataset_info(

    dataframe,

    dataset_name="Dataset"
):
    """
    Log dataset details.
    """

    LOGGER.info(

        f"{dataset_name} Shape: "
        f"{dataframe.shape}"
    )

    LOGGER.info(

        f"{dataset_name} Columns: "
        f"{list(dataframe.columns)}"
    )

    LOGGER.info(

        f"{dataset_name} Missing Values: "
        f"{dataframe.isnull().sum().sum()}"
    )


# =========================================================
# Log Forecast Metrics
# =========================================================

def log_regression_metrics(metrics):
    """
    Log forecasting evaluation metrics.
    """

    LOGGER.info(

        "=" * 40
    )

    LOGGER.info(

        "Forecast Evaluation Metrics"
    )

    LOGGER.info(

        "=" * 40
    )

    for metric_name, metric_value in metrics.items():

        LOGGER.info(

            f"{metric_name}: {metric_value}"
        )


# =========================================================
# Log Model Saving
# =========================================================

def log_model_saved(

    model_path
):
    """
    Log saved model information.
    """

    LOGGER.info(

        f"Model saved successfully: "
        f"{model_path}"
    )


# =========================================================
# Log Dataset Saving
# =========================================================

def log_dataset_saved(

    dataset_path
):
    """
    Log saved dataset information.
    """

    LOGGER.info(

        f"Dataset saved successfully: "
        f"{dataset_path}"
    )


# =========================================================
# Log Prediction Summary
# =========================================================

def log_prediction_summary(

    predictions
):
    """
    Log prediction statistics.
    """

    LOGGER.info(

        "=" * 40
    )

    LOGGER.info(

        "Prediction Summary"
    )

    LOGGER.info(

        "=" * 40
    )

    LOGGER.info(

        f"Total Predictions: {len(predictions)}"
    )

    LOGGER.info(

        f"Average Prediction: "
        f"{round(predictions.mean(), 2)}"
    )

    LOGGER.info(

        f"Minimum Prediction: "
        f"{round(predictions.min(), 2)}"
    )

    LOGGER.info(

        f"Maximum Prediction: "
        f"{round(predictions.max(), 2)}"
    )


# =========================================================
# Log Exception Details
# =========================================================

def log_exception(

    exception_message
):
    """
    Log exception details.
    """

    LOGGER.exception(

        f"Exception Occurred: "
        f"{exception_message}"
    )


# =========================================================
# Log Operational Recommendations
# =========================================================

def log_operational_recommendations():
    """
    Log deployment recommendations.
    """

    recommendations = [

        "Refresh forecasts every 1-3 hours.",

        "Monitor weather-driven demand spikes.",

        "Retrain models seasonally.",

        "Track prediction drift regularly.",

        "Validate operational forecasting daily."
    ]

    LOGGER.info(

        "=" * 40
    )

    LOGGER.info(

        "Operational Recommendations"
    )

    LOGGER.info(

        "=" * 40
    )

    for recommendation in recommendations:

        LOGGER.info(

            recommendation
        )


# =========================================================
# Log Business Insights
# =========================================================

def log_business_insights():
    """
    Log business forecasting insights.
    """

    insights = [

        "Peak-hour rentals drive demand growth.",

        "Weather significantly impacts bike usage.",

        "Weekend demand differs from weekdays.",

        "Seasonality affects operational planning.",

        "Short-term forecasts improve logistics."
    ]

    LOGGER.info(

        "=" * 40
    )

    LOGGER.info(

        "Business Insights"
    )

    LOGGER.info(

        "=" * 40
    )

    for insight in insights:

        LOGGER.info(

            insight
        )


# =========================================================
# Log System Information
# =========================================================

def log_system_info():
    """
    Log system environment details.
    """

    import platform

    LOGGER.info(

        "=" * 40
    )

    LOGGER.info(

        "System Information"
    )

    LOGGER.info(

        "=" * 40
    )

    LOGGER.info(

        f"Operating System: "
        f"{platform.system()}"
    )

    LOGGER.info(

        f"OS Version: "
        f"{platform.version()}"
    )

    LOGGER.info(

        f"Python Version: "
        f"{platform.python_version()}"
    )


# =========================================================
# Example Logger Test
# =========================================================

if __name__ == "__main__":

    log_pipeline_start(

        "Bike Demand Forecasting"
    )

    log_info(

        "Logger initialized successfully."
    )

    log_warning(

        "This is a sample warning."
    )

    log_error(

        "This is a sample error."
    )

    log_business_insights()

    log_operational_recommendations()

    log_system_info()

    log_pipeline_end(

        "Bike Demand Forecasting"
    )
