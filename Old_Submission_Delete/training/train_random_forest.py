# =========================================================
# File: training/train_random_forest.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor

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
    / "random_forest_model.pkl"
)

FEATURE_IMPORTANCE_FILE = (

    REPORTS_DIR
    / "random_forest_feature_importance.csv"
)

REPORT_FILE = (

    REPORTS_DIR
    / "random_forest_report.txt"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Training Random Forest Model ")
print("========================================")


# =========================================================
# Validate Dataset Files
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
# Initialize Random Forest Model
# =========================================================

print("\n========================================")
print(" Initializing Random Forest ")
print("========================================")

model = RandomForestRegressor(

    n_estimators=200,

    max_depth=20,

    min_samples_split=5,

    min_samples_leaf=2,

    random_state=42,

    n_jobs=-1
)

print("\nRandom Forest initialized successfully.")


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

    print("\nRandom Forest training completed.")

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
# Feature Importance
# =========================================================

print("\n========================================")
print(" Calculating Feature Importance ")
print("========================================")

feature_importance_df = pd.DataFrame({

    "Feature": X_train.columns,

    "Importance": model.feature_importances_
})

feature_importance_df = feature_importance_df.sort_values(

    by="Importance",

    ascending=False
)

print("\nTop Important Features:")

print(

    feature_importance_df.head(10)
)


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
# Save Feature Importance
# =========================================================

print("\n========================================")
print(" Saving Feature Importance ")
print("========================================")

try:

    feature_importance_df.to_csv(

        FEATURE_IMPORTANCE_FILE,

        index=False
    )

    print("\nFeature importance saved successfully.")

    print("\nSaved File:")
    print(FEATURE_IMPORTANCE_FILE)

except Exception as error:

    print("\nERROR while saving feature importance:")
    print(error)


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

            " Random Forest Evaluation Report \n"
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

            "- Random Forest captures complex demand relationships.\n"
        )

        file.write(

            "- Handles seasonality and weather effects effectively.\n"
        )

        file.write(

            "- Robust against outliers and nonlinear behavior.\n"
        )

        file.write(

            "- Suitable for operational bike demand forecasting.\n"
        )

    print("\nEvaluation report saved successfully.")

    print("\nSaved File:")
    print(REPORT_FILE)

except Exception as error:

    print("\nERROR while saving report:")
    print(error)


# =========================================================
# Production Pipeline Message
# =========================================================

print("\n========================================")
print(" Random Forest Model Ready ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Train XGBoost Model")

print("- Compare Model Performance")

print("- Perform Error Analysis")

print("- Generate Forecast Visualizations")

print("- Create Business Presentation")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Random Forest Training Completed ")
print("========================================")
