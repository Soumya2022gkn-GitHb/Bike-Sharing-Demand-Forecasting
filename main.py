# =========================================================
# File: main.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

"""
=========================================================
 Bike Sharing Demand Forecasting Pipeline
=========================================================

This script executes the complete machine learning
forecasting pipeline for hourly bike rental demand.

Pipeline Includes:
---------------------------------------------------------
1. Data Loading
2. Data Validation
3. Data Preprocessing
4. Feature Engineering
5. Feature Encoding
6. Feature Scaling
7. Model Training
8. Model Evaluation
9. Error Analysis
10. Forecast Visualization
11. Business Reporting
12. Streamlit App Launch

Target Variable:
---------------------------------------------------------
cnt -> Hourly Bike Rental Demand

Forecasting Model:
---------------------------------------------------------
XGBoost Regressor

=========================================================
"""


# =========================================================
# Import Libraries
# =========================================================

import subprocess
import sys
import time

from pathlib import Path


# =========================================================
# Import Utility Functions
# =========================================================

from utils.helpers import (

    print_header,

    create_directories
)

from utils.logger import (

    log_info,

    log_error,

    log_pipeline_start,

    log_pipeline_end
)


# =========================================================
# Define Project Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent


# =========================================================
# Define Pipeline Scripts
# =========================================================

PIPELINE_SCRIPTS = [

    # =====================================================
    # Data Ingestion
    # =====================================================

    "data_ingestion/load_data.py",

    "data_ingestion/validate_data.py",

    "data_ingestion/preprocess_data.py",


    # =====================================================
    # Feature Engineering
    # =====================================================

    "feature_engineering/create_time_features.py",

    "feature_engineering/encode_features.py",

    "feature_engineering/scale_features.py",


    # =====================================================
    # Model Training
    # =====================================================

    "training/train_linear_regression.py",

    "training/train_random_forest.py",

    "training/train_xgboost.py",

    "training/save_models.py",


    # =====================================================
    # Evaluation
    # =====================================================

    "evaluation/evaluate_models.py",

    "evaluation/error_analysis.py",

    "evaluation/forecast_analysis.py",


    # =====================================================
    # Visualization
    # =====================================================

    "visualization/plot_demand_trends.py",

    "visualization/plot_feature_importance.py",

    "visualization/plot_predictions.py",

    "visualization/plot_error_distribution.py",
]


# =========================================================
# Execute Python Script
# =========================================================

def execute_script(script_path):
    """
    Execute individual pipeline script.
    """

    full_script_path = (

        PROJECT_ROOT
        / script_path
    )

    print_header(

        f"Running: {script_path}"
    )

    log_info(

        f"Executing script: {script_path}"
    )

    try:

        subprocess.run(

            [sys.executable, str(full_script_path)],

            check=True
        )

        print(

            f"\nSUCCESS: {script_path}"
        )

        log_info(

            f"Completed script: {script_path}"
        )

    except subprocess.CalledProcessError as error:

        print(

            f"\nFAILED: {script_path}"
        )

        log_error(

            f"Script failed: {script_path}"
        )

        log_error(

            str(error)
        )

        raise error


# =========================================================
# Execute Complete Pipeline
# =========================================================

def run_pipeline():
    """
    Execute complete forecasting pipeline.
    """

    pipeline_start_time = time.time()

    print_header(

        "Bike Sharing Demand Forecasting Pipeline"
    )

    log_pipeline_start(

        "Bike Sharing Demand Forecasting"
    )

    print(

        "\nInitializing project directories..."
    )

    create_directories()

    print(

        "\nStarting pipeline execution..."
    )

    # =====================================================
    # Run Pipeline Scripts
    # =====================================================

    for script in PIPELINE_SCRIPTS:

        execute_script(script)

    # =====================================================
    # Pipeline Completion
    # =====================================================

    total_execution_time = (

        time.time()
        - pipeline_start_time
    )

    print_header(

        "Pipeline Completed Successfully"
    )

    print(

        f"\nTotal Execution Time: "
        f"{round(total_execution_time, 2)} seconds"
    )

    log_info(

        f"Pipeline execution completed "
        f"in {round(total_execution_time, 2)} seconds"
    )

    log_pipeline_end(

        "Bike Sharing Demand Forecasting"
    )


# =========================================================
# Launch Streamlit App
# =========================================================

def launch_streamlit_app():
    """
    Launch forecasting dashboard.
    """

    print_header(

        "Launching Streamlit Dashboard"
    )

    log_info(

        "Launching Streamlit dashboard..."
    )

    streamlit_script = (

        PROJECT_ROOT
        / "app"
        / "app.py"
    )

    try:

        subprocess.run(

            [

                "streamlit",

                "run",

                str(streamlit_script)
            ]
        )

    except Exception as error:

        log_error(

            f"Streamlit launch failed: {error}"
        )

        print(

            f"\nUnable to launch Streamlit app: {error}"
        )


# =========================================================
# Display Business Summary
# =========================================================

def display_business_summary():
    """
    Display forecasting business summary.
    """

    print_header(

        "Business Forecasting Summary"
    )

    summary_points = [

        "Forecast hourly bicycle demand.",

        "Optimize bike inventory allocation.",

        "Improve operational planning.",

        "Reduce bicycle shortages.",

        "Support weather-aware forecasting.",

        "Improve staffing efficiency.",

        "Enable data-driven logistics decisions."
    ]

    for point in summary_points:

        print(f"\n- {point}")


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

        "Retrain models seasonally.",

        "Monitor weather-driven demand spikes.",

        "Track forecasting drift regularly.",

        "Validate production predictions daily."
    ]

    for recommendation in recommendations:

        print(

            f"\n- {recommendation}"
        )


# =========================================================
# Main Function
# =========================================================

def main():
    """
    Main execution function.
    """

    try:

        # =================================================
        # Execute Forecasting Pipeline
        # =================================================

        run_pipeline()

        # =================================================
        # Display Business Insights
        # =================================================

        display_business_summary()

        display_operational_recommendations()

        # =================================================
        # Ask User to Launch Dashboard
        # =================================================

        print_header(

            "Launch Dashboard"
        )

        user_choice = input(

            "\nDo you want to launch "
            "the Streamlit dashboard? "
            "(yes/no): "
        ).strip().lower()

        if user_choice == "yes":

            launch_streamlit_app()

        else:

            print(

                "\nDashboard launch skipped."
            )

        # =================================================
        # Final Message
        # =================================================

        print_header(

            "Project Execution Completed"
        )

        print(

            "\nBike Sharing Demand Forecasting "
            "pipeline executed successfully."
        )

        print(

            "\nProject outputs generated:"
        )

        outputs = [

            "Processed datasets",

            "Feature-engineered datasets",

            "Trained forecasting models",

            "Forecast evaluation reports",

            "Visualization graphs",

            "Business insights",

            "Operational forecasting analysis"
        ]

        for output in outputs:

            print(f"\n- {output}")

    except Exception as error:

        log_error(

            f"Pipeline execution failed: {error}"
        )

        print_header(

            "Pipeline Failed"
        )

        print(

            f"\nError: {error}"
        )


# =========================================================
# Script Entry Point
# =========================================================

if __name__ == "__main__":

    main()


# =========================================================
# End of File
# =========================================================
