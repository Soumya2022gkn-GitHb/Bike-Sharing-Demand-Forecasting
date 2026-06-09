# =========================================================
# File: evaluation/evaluate_models.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (

    mean_absolute_error,

    mean_squared_error,

    r2_score
)


# =========================================================
# Check XGBoost Installation
# =========================================================

try:

    from xgboost import XGBRegressor

except ImportError:

    print("\n========================================")
    print(" XGBoost Not Installed ")
    print("========================================")

    print("\nInstall xgboost using:\n")

    print("pip install xgboost")

    raise SystemExit


# =========================================================
# Define Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

PROCESSED_DATA_DIR = (

    PROJECT_ROOT
    / "data"
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


# =========================================================
# Define Dataset & Model Paths
# =========================================================

TEST_FILE = (

    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)

LINEAR_MODEL_FILE = (

    MODELS_DIR
    / "linear_regression_model.pkl"
)

RANDOM_FOREST_MODEL_FILE = (

    MODELS_DIR
    / "random_forest_model.pkl"
)

XGBOOST_MODEL_FILE = (

    MODELS_DIR
    / "xgboost_model.pkl"
)

REPORT_FILE = (

    REPORTS_DIR
    / "model_comparison_report.txt"
)

COMPARISON_FILE = (

    REPORTS_DIR
    / "model_comparison_metrics.csv"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Evaluating Forecasting Models ")
print("========================================")


# =========================================================
# Validate Required Files
# =========================================================

required_files = [

    TEST_FILE,

    LINEAR_MODEL_FILE,

    RANDOM_FOREST_MODEL_FILE,

    XGBOOST_MODEL_FILE
]

print("\n========================================")
print(" Validating Required Files ")
print("========================================")

missing_files = []

for file in required_files:

    if file.exists():

        print(f"\nFOUND: {file.name}")

    else:

        print(f"\nMISSING: {file.name}")

        missing_files.append(

            file.name
        )

if len(missing_files) > 0:

    print("\nERROR: Missing required files.")

    raise SystemExit


# =========================================================
# Load Test Dataset
# =========================================================

print("\n========================================")
print(" Loading Test Dataset ")
print("========================================")

try:

    test_df = pd.read_csv(

        TEST_FILE
    )

    print("\nDataset loaded successfully.")

except Exception as error:

    print("\nERROR while loading dataset:")
    print(error)

    raise SystemExit


# =========================================================
# Define Target Variable
# =========================================================

TARGET_COLUMN = "cnt"

if TARGET_COLUMN not in test_df.columns:

    print("\nERROR: Target column not found.")

    raise SystemExit


# =========================================================
# Separate Features & Target
# =========================================================

print("\n========================================")
print(" Separating Features & Target ")
print("========================================")

X_test = test_df.drop(

    columns=[TARGET_COLUMN]
)

y_test = test_df[TARGET_COLUMN]

print("\nTesting Features Shape:")
print(X_test.shape)

print("\nTesting Target Shape:")
print(y_test.shape)


# =========================================================
# Load Models
# =========================================================

print("\n========================================")
print(" Loading Trained Models ")
print("========================================")

models = {}

try:

    models["Linear Regression"] = joblib.load(

        LINEAR_MODEL_FILE
    )

    models["Random Forest"] = joblib.load(

        RANDOM_FOREST_MODEL_FILE
    )

    models["XGBoost"] = joblib.load(

        XGBOOST_MODEL_FILE
    )

    print("\nAll models loaded successfully.")

except Exception as error:

    print("\nERROR while loading models:")
    print(error)

    raise SystemExit


# =========================================================
# Evaluate Models
# =========================================================

print("\n========================================")
print(" Evaluating Models ")
print("========================================")

evaluation_results = []

best_model = None

best_mae = float("inf")

for model_name, model in models.items():

    print(f"\nEvaluating: {model_name}")

    try:

        # -------------------------------------------------
        # Generate Predictions
        # -------------------------------------------------

        predictions = model.predict(

            X_test
        )

        # -------------------------------------------------
        # Calculate Metrics
        # -------------------------------------------------

        mae = mean_absolute_error(

            y_test,

            predictions
        )

        mse = mean_squared_error(

            y_test,

            predictions
        )

        rmse = np.sqrt(mse)

        r2 = r2_score(

            y_test,

            predictions
        )

        # -------------------------------------------------
        # Save Results
        # -------------------------------------------------

        evaluation_results.append({

            "Model": model_name,

            "MAE": round(mae, 2),

            "RMSE": round(rmse, 2),

            "R2_Score": round(r2, 4)
        })

        print(f"MAE  : {round(mae, 2)}")

        print(f"RMSE : {round(rmse, 2)}")

        print(f"R²   : {round(r2, 4)}")

        # -------------------------------------------------
        # Track Best Model
        # -------------------------------------------------

        if mae < best_mae:

            best_mae = mae

            best_model = model_name

    except Exception as error:

        print(f"\nERROR evaluating {model_name}:")
        print(error)


# =========================================================
# Create Comparison DataFrame
# =========================================================

comparison_df = pd.DataFrame(

    evaluation_results
)

comparison_df = comparison_df.sort_values(

    by="MAE"
)

print("\n========================================")
print(" Model Comparison ")
print("========================================")

print(comparison_df)


# =========================================================
# Create Output Directory
# =========================================================

REPORTS_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Save Comparison Metrics
# =========================================================

print("\n========================================")
print(" Saving Comparison Metrics ")
print("========================================")

try:

    comparison_df.to_csv(

        COMPARISON_FILE,

        index=False
    )

    print("\nComparison metrics saved successfully.")

    print("\nSaved File:")
    print(COMPARISON_FILE)

except Exception as error:

    print("\nERROR while saving metrics:")
    print(error)


# =========================================================
# Generate Evaluation Report
# =========================================================

print("\n========================================")
print(" Generating Evaluation Report ")
print("========================================")

try:

    with open(

        REPORT_FILE,

        "w",

        encoding="utf-8"
    ) as file:

        file.write(

            "========================================\n"
        )

        file.write(

            " Bike Sharing Forecasting Evaluation Report \n"
        )

        file.write(

            "========================================\n\n"
        )

        file.write(

            f"Test Dataset Shape: {test_df.shape}\n\n"
        )

        file.write(

            "Model Performance Summary:\n\n"
        )

        for _, row in comparison_df.iterrows():

            file.write(

                f"Model: {row['Model']}\n"
            )

            file.write(

                f"MAE  : {row['MAE']}\n"
            )

            file.write(

                f"RMSE : {row['RMSE']}\n"
            )

            file.write(

                f"R²   : {row['R2_Score']}\n\n"
            )

        file.write(

            "========================================\n"
        )

        file.write(

            " Best Forecasting Model \n"
        )

        file.write(

            "========================================\n\n"
        )

        file.write(

            f"Recommended Model: {best_model}\n\n"
        )

        file.write(

            "Business Recommendation:\n"
        )

        if best_model == "XGBoost":

            file.write(

                "- XGBoost provides the best forecasting accuracy.\n"
            )

            file.write(

                "- Captures complex nonlinear demand patterns.\n"
            )

            file.write(

                "- Highly suitable for operational deployment.\n"
            )

        elif best_model == "Random Forest":

            file.write(

                "- Random Forest provides stable forecasting.\n"
            )

            file.write(

                "- Handles seasonality effectively.\n"
            )

            file.write(

                "- Suitable for production forecasting systems.\n"
            )

        else:

            file.write(

                "- Linear Regression provides interpretable forecasts.\n"
            )

            file.write(

                "- Useful as a business baseline model.\n"
            )

        file.write("\n")

        file.write(

            "Operational Recommendation:\n"
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

    print("\nEvaluation report generated successfully.")

    print("\nSaved File:")
    print(REPORT_FILE)

except Exception as error:

    print("\nERROR while generating report:")
    print(error)


# =========================================================
# Final Recommendation
# =========================================================

print("\n========================================")
print(" Final Business Recommendation ")
print("========================================")

print(f"\nBest Model: {best_model}")

print(f"Best MAE : {round(best_mae, 2)}")

print("\nRecommended For Production Deployment.")


# =========================================================
# Production Pipeline Message
# =========================================================

print("\n========================================")
print(" Evaluation Completed ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Perform Error Analysis")

print("- Generate Feature Importance Plots")

print("- Create Forecast Visualizations")

print("- Prepare Business Presentation")

print("- Deploy Forecasting API")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Model Evaluation Completed Successfully ")
print("========================================")
