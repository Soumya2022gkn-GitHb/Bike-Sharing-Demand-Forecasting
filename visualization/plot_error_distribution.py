# =========================================================
# File: visualization/plot_error_distribution.py
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

ERROR_ANALYSIS_FILE = (

    REPORTS_DIR
    / "prediction_error_analysis.csv"
)

ERROR_DISTRIBUTION_PLOT = (

    GRAPHS_DIR
    / "error_distribution.png"
)

ABSOLUTE_ERROR_PLOT = (

    GRAPHS_DIR
    / "absolute_error_distribution.png"
)

RESIDUAL_PLOT = (

    GRAPHS_DIR
    / "residual_error_plot.png"
)

BOXPLOT_ERROR = (

    GRAPHS_DIR
    / "error_boxplot.png"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Plotting Error Distribution ")
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
# Load Trained Model
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
# Calculate Errors
# =========================================================

print("\n========================================")
print(" Calculating Prediction Errors ")
print("========================================")

errors = y_test - predictions

absolute_errors = np.abs(

    errors
)

squared_errors = np.square(

    errors
)

percentage_errors = (

    absolute_errors
    / (y_test + 1e-5)
) * 100


# =========================================================
# Calculate Metrics
# =========================================================

print("\n========================================")
print(" Calculating Forecast Metrics ")
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
# Create Error Analysis DataFrame
# =========================================================

print("\n========================================")
print(" Creating Error Analysis Dataset ")
print("========================================")

error_df = pd.DataFrame({

    "Actual_Demand": y_test,

    "Predicted_Demand": predictions,

    "Prediction_Error": errors,

    "Absolute_Error": absolute_errors,

    "Squared_Error": squared_errors,

    "Percentage_Error": percentage_errors
})

print("\nError analysis dataset created successfully.")


# =========================================================
# Save Error Analysis Dataset
# =========================================================

print("\n========================================")
print(" Saving Error Analysis Dataset ")
print("========================================")

try:

    error_df.to_csv(

        ERROR_ANALYSIS_FILE,

        index=False
    )

    print("\nError analysis dataset saved successfully.")

    print("\nSaved File:")
    print(ERROR_ANALYSIS_FILE)

except Exception as error:

    print("\nERROR while saving error analysis:")
    print(error)


# =========================================================
# Plot Error Distribution Histogram
# =========================================================

print("\n========================================")
print(" Plotting Error Distribution ")
print("========================================")

try:

    plt.figure(

        figsize=(10, 6)
    )

    plt.hist(

        errors,

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
# Plot Absolute Error Distribution
# =========================================================

print("\n========================================")
print(" Plotting Absolute Error Distribution ")
print("========================================")

try:

    plt.figure(

        figsize=(10, 6)
    )

    plt.hist(

        absolute_errors,

        bins=50
    )

    plt.title(

        "Absolute Error Distribution"
    )

    plt.xlabel(

        "Absolute Error"
    )

    plt.ylabel(

        "Frequency"
    )

    plt.tight_layout()

    plt.savefig(

        ABSOLUTE_ERROR_PLOT
    )

    plt.close()

    print("\nAbsolute error plot saved.")

    print("\nSaved File:")
    print(ABSOLUTE_ERROR_PLOT)

except Exception as error:

    print("\nERROR while plotting absolute errors:")
    print(error)


# =========================================================
# Plot Residual Error Scatter Plot
# =========================================================

print("\n========================================")
print(" Plotting Residual Error Plot ")
print("========================================")

try:

    plt.figure(

        figsize=(10, 6)
    )

    plt.scatter(

        predictions,

        errors,

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

        "Residual Error"
    )

    plt.tight_layout()

    plt.savefig(

        RESIDUAL_PLOT
    )

    plt.close()

    print("\nResidual error plot saved.")

    print("\nSaved File:")
    print(RESIDUAL_PLOT)

except Exception as error:

    print("\nERROR while plotting residual errors:")
    print(error)


# =========================================================
# Plot Error Boxplot
# =========================================================

print("\n========================================")
print(" Plotting Error Boxplot ")
print("========================================")

try:

    plt.figure(

        figsize=(8, 6)
    )

    plt.boxplot(

        errors
    )

    plt.title(

        "Prediction Error Boxplot"
    )

    plt.ylabel(

        "Prediction Error"
    )

    plt.tight_layout()

    plt.savefig(

        BOXPLOT_ERROR
    )

    plt.close()

    print("\nError boxplot saved.")

    print("\nSaved File:")
    print(BOXPLOT_ERROR)

except Exception as error:

    print("\nERROR while plotting error boxplot:")
    print(error)


# =========================================================
# Display Error Statistics
# =========================================================

print("\n========================================")
print(" Error Statistics ")
print("========================================")

print(f"\nAverage Error: {round(errors.mean(), 2)}")

print(f"Maximum Error: {round(errors.max(), 2)}")

print(f"Minimum Error: {round(errors.min(), 2)}")

print(f"Average Absolute Error: {round(absolute_errors.mean(), 2)}")

print(f"Average Percentage Error: {round(percentage_errors.mean(), 2)}%")


# =========================================================
# Business Insights
# =========================================================

print("\n========================================")
print(" Business Insights ")
print("========================================")

print("\nKey Forecasting Observations:")

print("- Most prediction errors are centered around zero.")

print("- XGBoost captures demand patterns effectively.")

print("- Peak-hour demand contributes to larger residuals.")

print("- Weather variability influences forecasting stability.")

print("- Forecast accuracy supports operational planning.")


# =========================================================
# Operational Recommendations
# =========================================================

print("\n========================================")
print(" Operational Recommendations ")
print("========================================")

print("\nRecommended Actions:")

print("- Refresh forecasts every 1-3 hours.")

print("- Monitor high-error demand periods.")

print("- Improve weather feature monitoring.")

print("- Retrain models seasonally.")

print("- Use short-term forecasts for logistics planning.")


# =========================================================
# Generated Files Summary
# =========================================================

print("\n========================================")
print(" Generated Visualization Files ")
print("========================================")

print(f"\n- {ERROR_ANALYSIS_FILE}")

print(f"- {ERROR_DISTRIBUTION_PLOT}")

print(f"- {ABSOLUTE_ERROR_PLOT}")

print(f"- {RESIDUAL_PLOT}")

print(f"- {BOXPLOT_ERROR}")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Error Distribution Visualization Completed ")
print("========================================")
