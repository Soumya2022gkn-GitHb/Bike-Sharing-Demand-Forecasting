# =========================================================
# File: feature_engineering/scale_features.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


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


# =========================================================
# Define Input & Output Files
# =========================================================

INPUT_FILE = (

    PROCESSED_DATA_DIR
    / "encoded_feature_data.csv"
)

SCALED_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "scaled_feature_data.csv"
)

TRAIN_FILE = (

    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

TEST_FILE = (

    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)

SCALER_FILE = (

    MODELS_DIR
    / "scaler.pkl"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Scaling Features ")
print("========================================")


# =========================================================
# Check Input File Exists
# =========================================================

print("\nInput Dataset:")
print(INPUT_FILE)

if not INPUT_FILE.exists():

    print("\nERROR: Encoded dataset not found.")

    print("\nPlease run:")

    print(
        "\npython feature_engineering/encode_features.py"
    )

    raise SystemExit


# =========================================================
# Load Dataset
# =========================================================

try:

    df = pd.read_csv(

        INPUT_FILE
    )

except Exception as error:

    print("\nERROR while loading dataset:")
    print(error)

    raise SystemExit


# =========================================================
# Dataset Information
# =========================================================

print("\n========================================")
print(" Dataset Information ")
print("========================================")

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(list(df.columns))


# =========================================================
# Check Target Variable
# =========================================================

TARGET_COLUMN = "cnt"

if TARGET_COLUMN not in df.columns:

    print("\nERROR: Target column not found.")

    raise SystemExit


# =========================================================
# Remove Missing Values
# =========================================================

print("\n========================================")
print(" Handling Missing Values ")
print("========================================")

df.replace(

    [np.inf, -np.inf],

    np.nan,

    inplace=True
)

numeric_columns = df.select_dtypes(

    include=[np.number]

).columns

df[numeric_columns] = df[

    numeric_columns

].fillna(

    df[numeric_columns].median()
)

print("\nMissing and infinite values handled.")


# =========================================================
# Separate Features & Target
# =========================================================

print("\n========================================")
print(" Separating Features & Target ")
print("========================================")

X = df.drop(

    columns=[TARGET_COLUMN]
)

y = df[TARGET_COLUMN]

print("\nFeature Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)


# =========================================================
# Train Test Split
# =========================================================

print("\n========================================")
print(" Creating Train-Test Split ")
print("========================================")

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42
)

print("\nTraining Shape:")
print(X_train.shape)

print("\nTesting Shape:")
print(X_test.shape)


# =========================================================
# Scale Features
# =========================================================

print("\n========================================")
print(" Applying Standard Scaling ")
print("========================================")

try:

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(

        X_train
    )

    X_test_scaled = scaler.transform(

        X_test
    )

    print("\nFeature scaling completed successfully.")

except Exception as error:

    print("\nERROR during feature scaling:")
    print(error)

    raise SystemExit


# =========================================================
# Convert Back To DataFrames
# =========================================================

X_train_scaled = pd.DataFrame(

    X_train_scaled,

    columns=X_train.columns
)

X_test_scaled = pd.DataFrame(

    X_test_scaled,

    columns=X_test.columns
)


# =========================================================
# Combine Features & Target
# =========================================================

train_df = pd.concat(

    [

        X_train_scaled.reset_index(drop=True),

        y_train.reset_index(drop=True)

    ],

    axis=1
)

test_df = pd.concat(

    [

        X_test_scaled.reset_index(drop=True),

        y_test.reset_index(drop=True)

    ],

    axis=1
)

scaled_df = pd.concat(

    [

        train_df,

        test_df

    ],

    axis=0
)


# =========================================================
# Create Output Directories
# =========================================================

PROCESSED_DATA_DIR.mkdir(

    parents=True,

    exist_ok=True
)

MODELS_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Save Scaled Dataset
# =========================================================

print("\n========================================")
print(" Saving Scaled Datasets ")
print("========================================")

try:

    scaled_df.to_csv(

        SCALED_DATA_FILE,

        index=False
    )

    train_df.to_csv(

        TRAIN_FILE,

        index=False
    )

    test_df.to_csv(

        TEST_FILE,

        index=False
    )

    print("\nScaled datasets saved successfully.")

except Exception as error:

    print("\nERROR while saving datasets:")
    print(error)

    raise SystemExit


# =========================================================
# Save Scaler
# =========================================================

print("\n========================================")
print(" Saving Scaler ")
print("========================================")

try:

    joblib.dump(

        scaler,

        SCALER_FILE
    )

    print("\nScaler saved successfully.")

    print("\nSaved File:")
    print(SCALER_FILE)

except Exception as error:

    print("\nERROR while saving scaler:")
    print(error)

    raise SystemExit


# =========================================================
# Dataset Validation
# =========================================================

print("\n========================================")
print(" Validating Scaled Dataset ")
print("========================================")

print("\nTotal Missing Values:")
print(scaled_df.isnull().sum().sum())

print("\nDuplicate Rows:")
print(scaled_df.duplicated().sum())

print("\nFinal Dataset Shape:")
print(scaled_df.shape)


# =========================================================
# Production Pipeline Message
# =========================================================

print("\n========================================")
print(" Dataset Ready For Model Training ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Train Linear Regression Model")

print("- Train Random Forest Model")

print("- Train XGBoost Model")

print("- Evaluate Forecasting Accuracy")

print("- Generate Forecast Visualizations")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Feature Scaling Completed Successfully ")
print("========================================")
