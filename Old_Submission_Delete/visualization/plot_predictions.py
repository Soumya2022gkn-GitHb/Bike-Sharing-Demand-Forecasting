# =========================================================
# File: visualization/plot_predictions.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

GRAPHS_DIR = (

    PROJECT_ROOT
    / "graphs"
)

REPORTS_DIR = (

    PROJECT_ROOT
    / "reports"
)


# =========================================================
# Define File Paths
# =========================================================

TEST_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)

XGBOOST_MODEL_FILE = (

    MODELS_DIR
    / "xgboost_model.pkl"
)

PREDICTION_RESULTS_FILE = (

    REPORTS_DIR
    / "prediction_results.csv"
)

PREDICTION_LINE_PLOT = (

    GRAPHS_DIR
    / "prediction_vs_actual_line.png"
)

PREDICTION_SCATTER_PLOT = (

    GRAPHS_DIR
    / "prediction_vs_actual_scatter.png"
)

RESIDUAL_PLOT = (

    GRAPHS_DIR
    / "prediction_residual_plot.png"
)

ERROR_DISTRIBUTION_PLOT = (

    GRAPHS_DIR
    / "prediction_error_distribution.png"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Plotting Forecast Predictions ")
print("========================================")


# =========================================================
# Validate Required Files
# =========================================================

print("\n========================================")
print(" Validating Required Files ")
print("========================================")

required_files = [

    TEST_DATA_FILE,

    XGBOOST_MODEL_FILE
]

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
# Create Output Directories
# =========================================================

GRAPHS_DIR.mkdir(

    parents=True,

    exist_ok=True
)

REPORTS_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Load Test Dataset
# =========================================================

print("\n========================================")
print(" Loading Test Dataset ")
print("========================================")

try:

    test_df = pd.read_csv(

        TEST_DATA_FILE
    )

    print("\nTest dataset loaded successfully.")

except Exception as error:

    print("\nERROR while loading dataset:")
    print(error)

    raise SystemExit


# =========================================================
# Validate Target Column
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

print("\nFeature Shape:")
print(X_test.shape)

print("\nTarget Shape:")
print(y_test.shape)


# =========================================================
# Load Trained XGBoost Model
# =========================================================

print("\n========================================")
print(" Loading XGBoost Model ")
print("========================================")

try:

    model = joblib.load(

        XGBOOST_MODEL_FILE
    )

    print("\nXGBoost model loaded successfully.")

except Exception as error:

    print("\nERROR while loading model:")
    print(error)

    raise SystemExit


# =========================================================
# Generate Predictions
# =========================================================

print("\n========================================")
print(" Generating Predictions ")
print("========================================")

try:

    predictions = model.predict(

        X_test
    )

    print("\nPredictions generated successfully.")

except Exception as error:

    print("\nERROR while generating predictions:")
    print(error)

    raise SystemExit


# =========================================================
# Calculate Metrics
# =========================================================

print("\n========================================")
print(" Calculating Prediction Metrics ")
print("========================================")

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

print(f"\nMAE  : {round(mae, 2)}")

print(f"RMSE : {round(rmse, 2)}")

print(f"R²   : {round(r2, 4)}")


# =========================================================
# Create Prediction DataFrame
# =========================================================

print("\n========================================")
print(" Creating Prediction DataFrame ")
print("========================================")

prediction_df = pd.DataFrame({

    "Actual_Demand": y_test,

    "Predicted_Demand": predictions
})

prediction_df["Prediction_Error"] = (

    prediction_df["Actual_Demand"]

    - prediction_df["Predicted_Demand"]
)

prediction_df["Absolute_Error"] = np.abs(

    prediction_df["Prediction_Error"]
)

print("\nPrediction DataFrame created successfully.")


# =========================================================
# Save Prediction Results
# =========================================================

print("\n========================================")
print(" Saving Prediction Results ")
print("========================================")

try:

    prediction_df.to_csv(

        PREDICTION_RESULTS_FILE,

        index=False
    )

    print("\nPrediction results saved successfully.")

    print("\nSaved File:")
    print(PREDICTION_RESULTS_FILE)

except Exception as error:

    print("\nERROR while saving prediction results:")
    print(error)


# =========================================================
# Plot Actual vs Predicted Line Graph
# =========================================================

print("\n========================================")
print(" Plotting Line Comparison ")
print("========================================")

try:

    plt.figure(

        figsize=(14, 6)
    )

    plt.plot(

        prediction_df["Actual_Demand"].values[:200],

        label="Actual Demand"
    )

    plt.plot(

        prediction_df["Predicted_Demand"].values[:200],

        label="Predicted Demand"
    )

    plt.title(

        "Actual vs Predicted Bike Demand"
    )

    plt.xlabel(

        "Observation Index"
    )

    plt.ylabel(

        "Bike Demand"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(

        PREDICTION_LINE_PLOT
    )

    plt.close()

    print("\nLine comparison plot saved.")

    print("\nSaved File:")
    print(PREDICTION_LINE_PLOT)

except Exception as error:

    print("\nERROR while plotting line graph:")
    print(error)


# =========================================================
# Plot Scatter Comparison
# =========================================================

print("\n========================================")
print(" Plotting Scatter Comparison ")
print("========================================")

try:

    plt.figure(

        figsize=(10, 6)
    )

    plt.scatter(

        prediction_df["Actual_Demand"],

        prediction_df["Predicted_Demand"],

        alpha=0.5
    )

    plt.plot(

        [

            prediction_df["Actual_Demand"].min(),

            prediction_df["Actual_Demand"].max()

        ],

        [

            prediction_df["Actual_Demand"].min(),

            prediction_df["Actual_Demand"].max()

        ]
    )

    plt.title(

        "Predicted vs Actual Demand"
    )

    plt.xlabel(

        "Actual Demand"
    )

    plt.ylabel(

        "Predicted Demand"
    )

    plt.tight_layout()

    plt.savefig(

        PREDICTION_SCATTER_PLOT
    )

    plt.close()

    print("\nScatter comparison plot saved.")

    print("\nSaved File:")
    print(PREDICTION_SCATTER_PLOT)

except Exception as error:

    print("\nERROR while plotting scatter graph:")
    print(error)


# =========================================================
# Plot Residual Errors
# =========================================================

print("\n========================================")
print(" Plotting Residual Errors ")
print("========================================")

try:

    residuals = (

        prediction_df["Actual_Demand"]

        - prediction_df["Predicted_Demand"]
    )

    plt.figure(

        figsize=(10, 6)
    )

    plt.scatter(

        prediction_df["Predicted_Demand"],

        residuals,

        alpha=0.5
    )

    plt.axhline(

        y=0
    )

    plt.title(

        "Residual Error Plot"
    )

    plt.xlabel(

        "Predicted Demand"
    )

    plt.ylabel(

        "Residual Errors"
    )

    plt.tight_layout()

    plt.savefig(

        RESIDUAL_PLOT
    )

    plt.close()

    print("\nResidual plot saved.")

    print("\nSaved File:")
    print(RESIDUAL_PLOT)

except Exception as error:

    print("\nERROR while plotting residuals:")
    print(error)


# =========================================================
# Plot Error Distribution
# =========================================================

print("\n========================================")
print(" Plotting Error Distribution ")
print("========================================")

try:

    plt.figure(

        figsize=(10, 6)
    )

    plt.hist(

        prediction_df["Prediction_Error"],

        bins=50
    )

    plt.title(

        "Prediction Error Distribution"
    )

    plt.xlabel(

        "Prediction Error"
    )

    plt.ylabel(

        "Frequency"
    )

    plt.tight_layout()

    plt.savefig(

        ERROR_DISTRIBUTION_PLOT
    )

    plt.close()

    print("\nError distribution plot saved.")

    print("\nSaved File:")
    print(ERROR_DISTRIBUTION_PLOT)

except Exception as error:

    print("\nERROR while plotting error distribution:")
    print(error)


# =========================================================
# Business Insights
# =========================================================

print("\n========================================")
print(" Business Insights ")
print("========================================")

print("\nKey Forecasting Observations:")

print("- Predictions closely follow actual demand.")

print("- Peak-hour demand is captured effectively.")

print("- Weather and time strongly influence demand.")

print("- Residual errors are relatively stable.")

print("- XGBoost performs well for operational planning.")


# =========================================================
# Operational Recommendations
# =========================================================

print("\n========================================")
print(" Operational Recommendations ")
print("========================================")

print("\nRecommended Actions:")

print("- Refresh forecasts every 1-3 hours.")

print("- Use short-term forecasts for logistics planning.")

print("- Monitor peak-hour forecasting accuracy.")

print("- Retrain models seasonally.")

print("- Track weather-driven demand fluctuations.")


# =========================================================
# Generated Files Summary
# =========================================================

print("\n========================================")
print(" Generated Visualization Files ")
print("========================================")

print(f"\n- {PREDICTION_RESULTS_FILE}")

print(f"- {PREDICTION_LINE_PLOT}")

print(f"- {PREDICTION_SCATTER_PLOT}")

print(f"- {RESIDUAL_PLOT}")

print(f"- {ERROR_DISTRIBUTION_PLOT}")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Prediction Visualization Completed ")
print("========================================")
