# =========================================================
# File: training/train_linear_regression.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
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
# Define Dataset Paths
# =========================================================

TRAIN_FILE = (

    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

TEST_FILE = (

    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)

MODEL_FILE = (

    MODELS_DIR
    / "linear_regression_model.pkl"
)

REPORT_FILE = (

    REPORTS_DIR
    / "linear_regression_report.txt"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Training Linear Regression Model ")
print("========================================")


# =========================================================
# Check Dataset Files Exist
# =========================================================

print("\nTraining Dataset:")
print(TRAIN_FILE)

print("\nTesting Dataset:")
print(TEST_FILE)

if not TRAIN_FILE.exists():

    print("\nERROR: Training dataset not found.")

    print("\nPlease run:")

    print(
        "\npython feature_engineering/scale_features.py"
    )

    raise SystemExit

if not TEST_FILE.exists():

    print("\nERROR: Testing dataset not found.")

    raise SystemExit


# =========================================================
# Load Datasets
# =========================================================

try:

    train_df = pd.read_csv(

        TRAIN_FILE
    )

    test_df = pd.read_csv(

        TEST_FILE
    )

except Exception as error:

    print("\nERROR while loading datasets:")
    print(error)

    raise SystemExit


# =========================================================
# Dataset Information
# =========================================================

print("\n========================================")
print(" Dataset Information ")
print("========================================")

print("\nTraining Shape:")
print(train_df.shape)

print("\nTesting Shape:")
print(test_df.shape)


# =========================================================
# Define Target Column
# =========================================================

TARGET_COLUMN = "cnt"

if TARGET_COLUMN not in train_df.columns:

    print("\nERROR: Target column not found.")

    raise SystemExit


# =========================================================
# Separate Features & Target
# =========================================================

print("\n========================================")
print(" Separating Features & Target ")
print("========================================")

X_train = train_df.drop(

    columns=[TARGET_COLUMN]
)

y_train = train_df[TARGET_COLUMN]

X_test = test_df.drop(

    columns=[TARGET_COLUMN]
)

y_test = test_df[TARGET_COLUMN]

print("\nTraining Features Shape:")
print(X_train.shape)

print("\nTesting Features Shape:")
print(X_test.shape)


# =========================================================
# Initialize Model
# =========================================================

print("\n========================================")
print(" Initializing Linear Regression ")
print("========================================")

model = LinearRegression()

print("\nLinear Regression model initialized.")


# =========================================================
# Train Model
# =========================================================

print("\n========================================")
print(" Training Model ")
print("========================================")

try:

    model.fit(

        X_train,

        y_train
    )

    print("\nModel training completed successfully.")

except Exception as error:

    print("\nERROR during model training:")
    print(error)

    raise SystemExit


# =========================================================
# Generate Predictions
# =========================================================

print("\n========================================")
print(" Generating Predictions ")
print("========================================")

try:

    y_pred = model.predict(

        X_test
    )

    print("\nPredictions generated successfully.")

except Exception as error:

    print("\nERROR during prediction:")
    print(error)

    raise SystemExit


# =========================================================
# Evaluate Model
# =========================================================

print("\n========================================")
print(" Evaluating Model ")
print("========================================")

try:

    mae = mean_absolute_error(

        y_test,

        y_pred
    )

    mse = mean_squared_error(

        y_test,

        y_pred
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(

        y_test,

        y_pred
    )

    print(f"\nMAE  : {round(mae, 2)}")

    print(f"RMSE : {round(rmse, 2)}")

    print(f"R²   : {round(r2, 4)}")

except Exception as error:

    print("\nERROR during evaluation:")
    print(error)

    raise SystemExit


# =========================================================
# Create Output Directories
# =========================================================

MODELS_DIR.mkdir(

    parents=True,

    exist_ok=True
)

REPORTS_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Save Model
# =========================================================

print("\n========================================")
print(" Saving Model ")
print("========================================")

try:

    joblib.dump(

        model,

        MODEL_FILE
    )

    print("\nModel saved successfully.")

    print("\nSaved File:")
    print(MODEL_FILE)

except Exception as error:

    print("\nERROR while saving model:")
    print(error)

    raise SystemExit


# =========================================================
# Save Evaluation Report
# =========================================================

print("\n========================================")
print(" Saving Evaluation Report ")
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

            " Linear Regression Evaluation Report \n"
        )

        file.write(

            "========================================\n\n"
        )

        file.write(

            f"Training Shape : {train_df.shape}\n"
        )

        file.write(

            f"Testing Shape  : {test_df.shape}\n\n"
        )

        file.write(

            f"Mean Absolute Error (MAE) : {round(mae, 2)}\n"
        )

        file.write(

            f"Root Mean Squared Error (RMSE) : {round(rmse, 2)}\n"
        )

        file.write(

            f"R² Score : {round(r2, 4)}\n\n"
        )

        file.write(

            "Business Summary:\n"
        )

        file.write(

            "- Linear Regression provides a simple baseline forecasting model.\n"
        )

        file.write(

            "- Useful for understanding feature relationships.\n"
        )

        file.write(

            "- Fast training and easy interpretability.\n"
        )

        file.write(

            "- May underperform on complex seasonal demand patterns.\n"
        )

    print("\nEvaluation report saved successfully.")

    print("\nSaved File:")
    print(REPORT_FILE)

except Exception as error:

    print("\nERROR while saving report:")
    print(error)

    raise SystemExit


# =========================================================
# Feature Importance (Coefficients)
# =========================================================

print("\n========================================")
print(" Feature Coefficients ")
print("========================================")

coefficients = pd.DataFrame({

    "Feature": X_train.columns,

    "Coefficient": model.coef_
})

coefficients = coefficients.sort_values(

    by="Coefficient",

    ascending=False
)

print(coefficients.head(10))


# =========================================================
# Production Readiness Message
# =========================================================

print("\n========================================")
print(" Model Ready For Evaluation ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Train Random Forest Model")

print("- Train XGBoost Model")

print("- Compare Forecasting Accuracy")

print("- Generate Error Analysis")

print("- Create Business Presentation")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Linear Regression Training Completed ")
print("========================================")
