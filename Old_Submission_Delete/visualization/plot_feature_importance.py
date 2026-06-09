# =========================================================
# File: visualization/plot_feature_importance.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import joblib


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

GRAPHS_DIR = (

    PROJECT_ROOT
    / "graphs"
)


# =========================================================
# Define File Paths
# =========================================================

TRAIN_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

XGBOOST_MODEL_FILE = (

    MODELS_DIR
    / "xgboost_model.pkl"
)

FEATURE_IMPORTANCE_FILE = (

    REPORTS_DIR
    / "xgboost_feature_importance.csv"
)

FEATURE_IMPORTANCE_PLOT = (

    GRAPHS_DIR
    / "feature_importance.png"
)

TOP_FEATURES_PLOT = (

    GRAPHS_DIR
    / "top_10_features.png"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Plotting Feature Importance ")
print("========================================")


# =========================================================
# Validate Required Files
# =========================================================

print("\n========================================")
print(" Validating Required Files ")
print("========================================")

required_files = [

    TRAIN_DATA_FILE,

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
# Load Training Dataset
# =========================================================

print("\n========================================")
print(" Loading Training Dataset ")
print("========================================")

try:

    train_df = pd.read_csv(

        TRAIN_DATA_FILE
    )

    print("\nTraining dataset loaded successfully.")

except Exception as error:

    print("\nERROR while loading dataset:")
    print(error)

    raise SystemExit


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
print(" Separating Features ")
print("========================================")

X_train = train_df.drop(

    columns=[TARGET_COLUMN]
)

print("\nFeature Shape:")
print(X_train.shape)


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
# Extract Feature Importance
# =========================================================

print("\n========================================")
print(" Extracting Feature Importance ")
print("========================================")

try:

    feature_importance_df = pd.DataFrame({

        "Feature": X_train.columns,

        "Importance": model.feature_importances_
    })

    feature_importance_df = feature_importance_df.sort_values(

        by="Importance",

        ascending=False
    )

    print("\nFeature importance extracted successfully.")

except Exception as error:

    print("\nERROR while extracting feature importance:")
    print(error)

    raise SystemExit


# =========================================================
# Save Feature Importance CSV
# =========================================================

print("\n========================================")
print(" Saving Feature Importance CSV ")
print("========================================")

try:

    feature_importance_df.to_csv(

        FEATURE_IMPORTANCE_FILE,

        index=False
    )

    print("\nFeature importance CSV saved successfully.")

    print("\nSaved File:")
    print(FEATURE_IMPORTANCE_FILE)

except Exception as error:

    print("\nERROR while saving feature importance:")
    print(error)


# =========================================================
# Plot Complete Feature Importance
# =========================================================

print("\n========================================")
print(" Plotting Feature Importance ")
print("========================================")

try:

    plt.figure(

        figsize=(14, 10)
    )

    plt.barh(

        feature_importance_df["Feature"],

        feature_importance_df["Importance"]
    )

    plt.title(

        "XGBoost Feature Importance"
    )

    plt.xlabel(

        "Importance Score"
    )

    plt.ylabel(

        "Features"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.savefig(

        FEATURE_IMPORTANCE_PLOT
    )

    plt.close()

    print("\nFeature importance plot saved.")

    print("\nSaved File:")
    print(FEATURE_IMPORTANCE_PLOT)

except Exception as error:

    print("\nERROR while plotting feature importance:")
    print(error)


# =========================================================
# Plot Top 10 Important Features
# =========================================================

print("\n========================================")
print(" Plotting Top 10 Features ")
print("========================================")

try:

    top_features = feature_importance_df.head(10)

    plt.figure(

        figsize=(12, 6)
    )

    plt.bar(

        top_features["Feature"],

        top_features["Importance"]
    )

    plt.title(

        "Top 10 Important Features"
    )

    plt.xlabel(

        "Feature"
    )

    plt.ylabel(

        "Importance Score"
    )

    plt.xticks(

        rotation=45
    )

    plt.tight_layout()

    plt.savefig(

        TOP_FEATURES_PLOT
    )

    plt.close()

    print("\nTop feature plot saved.")

    print("\nSaved File:")
    print(TOP_FEATURES_PLOT)

except Exception as error:

    print("\nERROR while plotting top features:")
    print(error)


# =========================================================
# Display Top Features
# =========================================================

print("\n========================================")
print(" Top Important Features ")
print("========================================")

print(

    feature_importance_df.head(10)
)


# =========================================================
# Business Insights
# =========================================================

print("\n========================================")
print(" Business Insights ")
print("========================================")

print("\nKey Forecasting Drivers:")

top_5_features = (

    feature_importance_df["Feature"]

    .head(5)

    .tolist()
)

for feature in top_5_features:

    print(f"- {feature}")


print("\nOperational Observations:")

print("- Time-based features strongly influence demand.")

print("- Weather impacts forecasting accuracy.")

print("- Rush-hour patterns are highly predictive.")

print("- Seasonal variables improve operational planning.")

print("- Demand forecasting supports inventory optimization.")


# =========================================================
# Production Recommendations
# =========================================================

print("\n========================================")
print(" Operational Recommendations ")
print("========================================")

print("\nRecommended Actions:")

print("- Monitor top forecasting features regularly.")

print("- Update forecasts during weather changes.")

print("- Retrain models seasonally.")

print("- Use feature importance for business planning.")

print("- Prioritize operational staffing during peak hours.")


# =========================================================
# Generated Files Summary
# =========================================================

print("\n========================================")
print(" Generated Visualization Files ")
print("========================================")

print(f"\n- {FEATURE_IMPORTANCE_FILE}")

print(f"- {FEATURE_IMPORTANCE_PLOT}")

print(f"- {TOP_FEATURES_PLOT}")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Feature Importance Visualization Completed ")
print("========================================")
