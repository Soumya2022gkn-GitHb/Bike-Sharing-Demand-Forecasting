# =========================================================
# File: feature_engineering/encode_features.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


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
    / "time_feature_engineered_data.csv"
)

OUTPUT_FILE = (

    PROCESSED_DATA_DIR
    / "encoded_feature_data.csv"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Encoding Categorical Features ")
print("========================================")


# =========================================================
# Check Dataset Exists
# =========================================================

print("\nInput Dataset:")
print(INPUT_FILE)

if not INPUT_FILE.exists():

    print("\nERROR: Time feature dataset not found.")

    print("\nPlease run:")

    print(
        "\npython feature_engineering/create_time_features.py"
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
# Identify Categorical Columns
# =========================================================

print("\n========================================")
print(" Detecting Categorical Columns ")
print("========================================")

categorical_columns = df.select_dtypes(

    include=["object", "category"]

).columns.tolist()

print("\nCategorical Columns:")
print(categorical_columns)


# =========================================================
# Remove Target Leakage Columns
# =========================================================

print("\n========================================")
print(" Removing Non-Training Columns ")
print("========================================")

drop_columns = [

    "dteday"
]

existing_drop_columns = [

    column
    for column in drop_columns
    if column in df.columns
]

if existing_drop_columns:

    df.drop(

        columns=existing_drop_columns,

        inplace=True
    )

    print("\nDropped Columns:")
    print(existing_drop_columns)

else:

    print("\nNo columns dropped.")


# =========================================================
# Label Encode Categorical Features
# =========================================================

print("\n========================================")
print(" Applying Label Encoding ")
print("========================================")

label_encoders = {}

try:

    for column in categorical_columns:

        # -------------------------------------------------
        # Skip Removed Columns
        # -------------------------------------------------

        if column not in df.columns:

            continue

        # -------------------------------------------------
        # Fill Missing Values
        # -------------------------------------------------

        df[column] = df[column].fillna(

            "Unknown"
        )

        # -------------------------------------------------
        # Convert To String
        # -------------------------------------------------

        df[column] = df[column].astype(str)

        # -------------------------------------------------
        # Create Encoder
        # -------------------------------------------------

        encoder = LabelEncoder()

        # -------------------------------------------------
        # Encode Column
        # -------------------------------------------------

        df[column] = encoder.fit_transform(

            df[column]
        )

        # -------------------------------------------------
        # Store Encoder
        # -------------------------------------------------

        label_encoders[column] = encoder

        print(f"\nEncoded Column: {column}")

except Exception as error:

    print("\nERROR while encoding features:")
    print(error)

    raise SystemExit


# =========================================================
# Handle Missing Values
# =========================================================

print("\n========================================")
print(" Handling Missing Values ")
print("========================================")

numeric_columns = df.select_dtypes(

    include=[np.number]

).columns

df[numeric_columns] = df[

    numeric_columns

].fillna(

    df[numeric_columns].median()
)

print("\nMissing values handled successfully.")


# =========================================================
# Remove Infinite Values
# =========================================================

print("\n========================================")
print(" Removing Infinite Values ")
print("========================================")

df.replace(

    [np.inf, -np.inf],

    np.nan,

    inplace=True
)

df[numeric_columns] = df[

    numeric_columns

].fillna(0)

print("\nInfinite values removed successfully.")


# =========================================================
# Validate Dataset
# =========================================================

print("\n========================================")
print(" Validating Encoded Dataset ")
print("========================================")

total_missing = df.isnull().sum().sum()

print("\nTotal Missing Values:")
print(total_missing)

duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows:")
print(duplicate_rows)

if duplicate_rows > 0:

    df.drop_duplicates(

        inplace=True
    )

    print("\nDuplicate rows removed.")


# =========================================================
# Dataset Summary
# =========================================================

print("\n========================================")
print(" Encoded Dataset Summary ")
print("========================================")

print("\nFinal Shape:")
print(df.shape)

print("\nTotal Columns:")
print(len(df.columns))

print("\nEncoded Features Ready For:")
print("- Feature Scaling")
print("- Machine Learning")
print("- Forecasting Models")
print("- Evaluation Pipeline")


# =========================================================
# Create Output Directory
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
# Save Encoded Dataset
# =========================================================

print("\n========================================")
print(" Saving Encoded Dataset ")
print("========================================")

try:

    df.to_csv(

        OUTPUT_FILE,

        index=False
    )

    print("\nDataset saved successfully.")

    print("\nSaved File:")
    print(OUTPUT_FILE)

except Exception as error:

    print("\nERROR while saving dataset:")
    print(error)

    raise SystemExit


# =========================================================
# Save Encoders Mapping
# =========================================================

print("\n========================================")
print(" Saving Encoding Mappings ")
print("========================================")

try:

    mapping_file = (

        MODELS_DIR
        / "label_encoding_mappings.txt"
    )

    with open(

        mapping_file,

        "w",

        encoding="utf-8"
    ) as file:

        for column, encoder in label_encoders.items():

            file.write(

                f"\nColumn: {column}\n"
            )

            for index, label in enumerate(

                encoder.classes_
            ):

                file.write(

                    f"{label} -> {index}\n"
                )

    print("\nEncoding mappings saved successfully.")

    print("\nSaved File:")
    print(mapping_file)

except Exception as error:

    print("\nERROR while saving mappings:")
    print(error)


# =========================================================
# Production Pipeline Message
# =========================================================

print("\n========================================")
print(" Dataset Ready For Scaling ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Scale Features")

print("- Train Forecasting Models")

print("- Evaluate Models")

print("- Generate Forecast Visualizations")

print("- Deploy Forecasting Service")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Feature Encoding Completed Successfully ")
print("========================================")
