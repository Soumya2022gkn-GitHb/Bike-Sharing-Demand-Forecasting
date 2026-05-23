# =========================================================
# File: training/train_xgboost.py
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
    / "xgboost_model.pkl"
)

FEATURE_IMPORTANCE_FILE = (

    REPORTS_DIR
    / "xgboost_feature_importance.csv"
)

REPORT_FILE = (

    REPORTS_DIR
    / "xgboost_report.txt"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Training XGBoost Model ")
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
# Initialize XGBoost Model
# =========================================================

print("\n========================================")
print(" Initializing XGBoost ")
print("========================================")

model = XGBRegressor(

    n_estimators=300,

    learning_rate=0.05,

    max_depth=8,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="reg:squarederror",

    random_state=42,

    n_jobs=-1
)

print("\nXGBoost initialized successfully.")


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

    print("\nXGBoost training completed successfully.")

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
# Calculate Feature Importance
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

            " XGBoost Evaluation Report \n"
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

            "- XGBoost provides high forecasting accuracy.\n"
        )

        file.write(

            "- Effectively captures nonlinear demand behavior.\n"
        )

        file.write(

            "- Handles seasonality and weather dependencies.\n"
        )

        file.write(

            "- Strong candidate for production deployment.\n"
        )

    print("\nEvaluation report saved successfully.")

    print("\nSaved File:")
    print(REPORT_FILE)

except Exception as error:

    print("\nERROR while saving report:")
    print(error)


# =========================================================
# Model Recommendation
# =========================================================

print("\n========================================")
print(" Business Recommendation ")
print("========================================")

print("\nXGBoost is recommended for production use because:")

print("- High forecasting accuracy")

print("- Handles complex seasonal patterns")

print("- Captures nonlinear relationships")

print("- Strong performance on structured datasets")

print("- Reliable for operational demand forecasting")


# =========================================================
# Production Pipeline Message
# =========================================================

print("\n========================================")
print(" XGBoost Model Ready ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Compare All Models")

print("- Perform Error Analysis")

print("- Generate Forecast Visualizations")

print("- Create Business Presentation")

print("- Deploy Forecasting Pipeline")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" XGBoost Training Completed ")
print("========================================")
