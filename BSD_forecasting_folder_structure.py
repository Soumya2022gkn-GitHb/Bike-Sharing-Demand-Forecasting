# =========================================================
# Project: Bike Sharing Demand Forecasting
# File: create_project_structure.py
# =========================================================

from pathlib import Path


# =========================================================
# Define Project Root
# =========================================================

PROJECT_NAME = "Bike_Sharing_Demand_Forecasting"

ROOT_DIR = Path(PROJECT_NAME)


# =========================================================
# Define Folder Structure
# =========================================================

FOLDERS = [

    # -----------------------------------------------------
    # Application
    # -----------------------------------------------------

    "app",

    # -----------------------------------------------------
    # Configuration
    # -----------------------------------------------------

    "config",

    # -----------------------------------------------------
    # Data Directories
    # -----------------------------------------------------

    "data/raw",

    "data/processed",

    # -----------------------------------------------------
    # Jupyter Notebooks
    # -----------------------------------------------------

    "notebooks",

    # -----------------------------------------------------
    # Data Ingestion
    # -----------------------------------------------------

    "data_ingestion",

    # -----------------------------------------------------
    # Feature Engineering
    # -----------------------------------------------------

    "feature_engineering",

    # -----------------------------------------------------
    # Training
    # -----------------------------------------------------

    "training",

    # -----------------------------------------------------
    # Evaluation
    # -----------------------------------------------------

    "evaluation",

    # -----------------------------------------------------
    # Visualization
    # -----------------------------------------------------

    "visualization",

    # -----------------------------------------------------
    # Models
    # -----------------------------------------------------

    "models",

    # -----------------------------------------------------
    # Graphs
    # -----------------------------------------------------

    "graphs",

    # -----------------------------------------------------
    # Reports
    # -----------------------------------------------------

    "reports",

    # -----------------------------------------------------
    # Tests
    # -----------------------------------------------------

    "tests",

    # -----------------------------------------------------
    # Utilities
    # -----------------------------------------------------

    "utils"
]


# =========================================================
# Define Empty Files
# =========================================================

FILES = [

    # -----------------------------------------------------
    # Main Files
    # -----------------------------------------------------

    "main.py",

    "requirements.txt",

    "README.md",


    # -----------------------------------------------------
    # App
    # -----------------------------------------------------

    "app/app.py",


    # -----------------------------------------------------
    # Config
    # -----------------------------------------------------

    "config/config.py",


    # -----------------------------------------------------
    # Notebooks
    # -----------------------------------------------------

    "notebooks/exploratory_data_analysis.ipynb",


    # -----------------------------------------------------
    # Data Files
    # -----------------------------------------------------

    "data/raw/hour.csv",

    "data/processed/cleaned_bike_data.csv",

    "data/processed/train_dataset.csv",

    "data/processed/test_dataset.csv",

    "data/processed/feature_engineered_data.csv",


    # -----------------------------------------------------
    # Data Ingestion
    # -----------------------------------------------------

    "data_ingestion/load_data.py",

    "data_ingestion/validate_data.py",

    "data_ingestion/preprocess_data.py",


    # -----------------------------------------------------
    # Feature Engineering
    # -----------------------------------------------------

    "feature_engineering/create_time_features.py",

    "feature_engineering/encode_features.py",

    "feature_engineering/scale_features.py",


    # -----------------------------------------------------
    # Training
    # -----------------------------------------------------

    "training/train_linear_regression.py",

    "training/train_random_forest.py",

    "training/train_xgboost.py",

    "training/save_models.py",


    # -----------------------------------------------------
    # Evaluation
    # -----------------------------------------------------

    "evaluation/evaluate_models.py",

    "evaluation/error_analysis.py",

    "evaluation/forecast_analysis.py",


    # -----------------------------------------------------
    # Visualization
    # -----------------------------------------------------

    "visualization/plot_demand_trends.py",

    "visualization/plot_feature_importance.py",

    "visualization/plot_predictions.py",

    "visualization/plot_error_distribution.py",


    # -----------------------------------------------------
    # Model Files
    # -----------------------------------------------------

    "models/linear_regression_model.pkl",

    "models/random_forest_model.pkl",

    "models/xgboost_model.pkl",

    "models/scaler.pkl",


    # -----------------------------------------------------
    # Graph Files
    # -----------------------------------------------------

    "graphs/hourly_demand.png",

    "graphs/seasonal_trends.png",

    "graphs/feature_importance.png",

    "graphs/prediction_vs_actual.png",

    "graphs/error_distribution.png",

    "graphs/correlation_heatmap.png",


    # -----------------------------------------------------
    # Reports
    # -----------------------------------------------------

    "reports/exploratory_data_analysis.pdf",

    "reports/model_evaluation_report.pdf",

    "reports/business_presentation.pptx",


    # -----------------------------------------------------
    # Tests
    # -----------------------------------------------------

    "tests/test_data_pipeline.py",

    "tests/test_feature_engineering.py",

    "tests/test_training.py",

    "tests/test_inference.py",


    # -----------------------------------------------------
    # Utilities
    # -----------------------------------------------------

    "utils/helpers.py",

    "utils/logger.py"
]


# =========================================================
# Create Project Root
# =========================================================

ROOT_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Create Folders
# =========================================================

print("\n========================================")
print(" Creating Folder Structure ")
print("========================================")

for folder in FOLDERS:

    folder_path = ROOT_DIR / folder

    folder_path.mkdir(

        parents=True,

        exist_ok=True
    )

    print(f"Created Folder: {folder_path}")


# =========================================================
# Create Files
# =========================================================

print("\n========================================")
print(" Creating Files ")
print("========================================")

for file in FILES:

    file_path = ROOT_DIR / file

    file_path.parent.mkdir(

        parents=True,

        exist_ok=True
    )

    file_path.touch(

        exist_ok=True
    )

    print(f"Created File: {file_path}")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Project Structure Created Successfully ")
print("========================================")

print(f"\nProject Location:")
print(ROOT_DIR.resolve())
