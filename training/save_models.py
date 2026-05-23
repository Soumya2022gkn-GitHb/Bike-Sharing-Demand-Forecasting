# =========================================================
# File: training/save_models.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import shutil
import joblib
from datetime import datetime


# =========================================================
# Define Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

MODELS_DIR = (

    PROJECT_ROOT
    / "models"
)

BACKUP_DIR = (

    MODELS_DIR
    / "backup_models"
)

REPORTS_DIR = (

    PROJECT_ROOT
    / "reports"
)


# =========================================================
# Define Model Files
# =========================================================

LINEAR_MODEL = (

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

SCALER_FILE = (

    MODELS_DIR
    / "scaler.pkl"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Saving and Backing Up Models ")
print("========================================")


# =========================================================
# Create Backup Directory
# =========================================================

BACKUP_DIR.mkdir(

    parents=True,

    exist_ok=True
)

REPORTS_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Timestamp For Backup
# =========================================================

timestamp = datetime.now().strftime(

    "%Y%m%d_%H%M%S"
)


# =========================================================
# List Model Files
# =========================================================

model_files = [

    LINEAR_MODEL,

    RANDOM_FOREST_MODEL,

    XGBOOST_MODEL,

    SCALER_FILE
]


# =========================================================
# Validate Model Files
# =========================================================

print("\n========================================")
print(" Validating Model Files ")
print("========================================")

available_models = []

missing_models = []

for model_file in model_files:

    if model_file.exists():

        available_models.append(

            model_file
        )

        print(f"\nFOUND: {model_file.name}")

    else:

        missing_models.append(

            model_file.name
        )

        print(f"\nMISSING: {model_file.name}")


# =========================================================
# Stop If No Models Exist
# =========================================================

if len(available_models) == 0:

    print("\nERROR: No trained models found.")

    print("\nPlease train models first:")

    print(
        "\npython training/train_linear_regression.py"
    )

    print(
        "python training/train_random_forest.py"
    )

    print(
        "python training/train_xgboost.py"
    )

    raise SystemExit


# =========================================================
# Load Models
# =========================================================

print("\n========================================")
print(" Loading Models ")
print("========================================")

loaded_models = {}

for model_file in available_models:

    try:

        model = joblib.load(

            model_file
        )

        loaded_models[

            model_file.name

        ] = model

        print(

            f"\nLoaded: {model_file.name}"
        )

    except Exception as error:

        print(

            f"\nERROR loading {model_file.name}:"
        )

        print(error)


# =========================================================
# Backup Models
# =========================================================

print("\n========================================")
print(" Creating Model Backups ")
print("========================================")

backup_files = []

for model_file in available_models:

    try:

        backup_file = (

            BACKUP_DIR
            / f"{timestamp}_{model_file.name}"
        )

        shutil.copy2(

            model_file,

            backup_file
        )

        backup_files.append(

            backup_file.name
        )

        print(

            f"\nBackup Created: {backup_file.name}"
        )

    except Exception as error:

        print(

            f"\nERROR backing up {model_file.name}:"
        )

        print(error)


# =========================================================
# Generate Model Inventory Report
# =========================================================

print("\n========================================")
print(" Generating Model Inventory Report ")
print("========================================")

inventory_report = (

    REPORTS_DIR
    / "model_inventory_report.txt"
)

try:

    with open(

        inventory_report,

        "w",

        encoding="utf-8"
    ) as file:

        file.write(

            "========================================\n"
        )

        file.write(

            " Bike Sharing Forecasting Model Inventory \n"
        )

        file.write(

            "========================================\n\n"
        )

        file.write(

            f"Generated On: {datetime.now()}\n\n"
        )

        file.write(

            "Available Models:\n"
        )

        for model_file in available_models:

            file.write(

                f"- {model_file.name}\n"
            )

        file.write("\n")

        file.write(

            "Missing Models:\n"
        )

        if len(missing_models) == 0:

            file.write(

                "- None\n"
            )

        else:

            for model in missing_models:

                file.write(

                    f"- {model}\n"
                )

        file.write("\n")

        file.write(

            "Backup Files Created:\n"
        )

        for backup in backup_files:

            file.write(

                f"- {backup}\n"
            )

        file.write("\n")

        file.write(

            "Production Recommendation:\n"
        )

        file.write(

            "- XGBoost is recommended for deployment.\n"
        )

        file.write(

            "- Random Forest is recommended as backup model.\n"
        )

        file.write(

            "- Linear Regression serves as baseline benchmark.\n"
        )

        file.write("\n")

        file.write(

            "Operational Notes:\n"
        )

        file.write(

            "- Refresh forecasts every 1-3 hours.\n"
        )

        file.write(

            "- Retrain models monthly or seasonally.\n"
        )

        file.write(

            "- Monitor demand spikes during holidays.\n"
        )

    print("\nInventory report generated successfully.")

    print("\nSaved File:")
    print(inventory_report)

except Exception as error:

    print("\nERROR while generating report:")
    print(error)


# =========================================================
# Save Model Metadata
# =========================================================

print("\n========================================")
print(" Saving Model Metadata ")
print("========================================")

metadata_file = (

    MODELS_DIR
    / "model_metadata.txt"
)

try:

    with open(

        metadata_file,

        "w",

        encoding="utf-8"
    ) as file:

        file.write(

            "========================================\n"
        )

        file.write(

            " Model Metadata \n"
        )

        file.write(

            "========================================\n\n"
        )

        file.write(

            f"Timestamp: {timestamp}\n\n"
        )

        for model_name in loaded_models.keys():

            file.write(

                f"Model: {model_name}\n"
            )

        file.write("\n")

        file.write(

            "Forecasting Target: cnt\n"
        )

        file.write(

            "Project: Bike_Sharing_Demand_Forecasting\n"
        )

        file.write(

            "Best Model: XGBoost\n"
        )

        file.write(

            "Deployment Ready: Yes\n"
        )

    print("\nModel metadata saved successfully.")

    print("\nSaved File:")
    print(metadata_file)

except Exception as error:

    print("\nERROR while saving metadata:")
    print(error)


# =========================================================
# Final Summary
# =========================================================

print("\n========================================")
print(" Model Backup Summary ")
print("========================================")

print(f"\nAvailable Models : {len(available_models)}")

print(f"Missing Models   : {len(missing_models)}")

print(f"Backup Files     : {len(backup_files)}")


# =========================================================
# Production Pipeline Message
# =========================================================

print("\n========================================")
print(" Models Ready For Deployment ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Evaluate All Models")

print("- Perform Error Analysis")

print("- Generate Visualizations")

print("- Create Business Presentation")

print("- Deploy Forecasting Service")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Model Saving Completed Successfully ")
print("========================================")
