# =========================================================
# File: data_ingestion/preprocess_data.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import numpy as np


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


# =========================================================
# Define Input & Output Files
# =========================================================

INPUT_FILE = (

    PROCESSED_DATA_DIR
    / "cleaned_bike_data.csv"
)

OUTPUT_FILE = (

    PROCESSED_DATA_DIR
    / "feature_engineered_data.csv"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Preprocessing Bike Sharing Dataset ")
print("========================================")


# =========================================================
# Check Dataset Exists
# =========================================================

print("\nInput Dataset:")
print(INPUT_FILE)

if not INPUT_FILE.exists():

    print("\nERROR: Cleaned dataset not found.")

    print("\nPlease run:")

    print("\npython data_ingestion/load_data.py")

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
# Convert Date Column
# =========================================================

print("\n========================================")
print(" Date Conversion ")
print("========================================")

try:

    df["dteday"] = pd.to_datetime(

        df["dteday"],

        errors="coerce"
    )

    invalid_dates = df["dteday"].isnull().sum()

    print("\nInvalid Dates:")
    print(invalid_dates)

    if invalid_dates > 0:

        df.dropna(

            subset=["dteday"],

            inplace=True
        )

        print("\nInvalid dates removed.")

except Exception as error:

    print("\nERROR while converting dates:")
    print(error)

    raise SystemExit


# =========================================================
# Create Time-Based Features
# =========================================================

print("\n========================================")
print(" Creating Time Features ")
print("========================================")

try:

    # -----------------------------------------------------
    # Day Feature
    # -----------------------------------------------------

    df["day"] = df["dteday"].dt.day

    # -----------------------------------------------------
    # Month Name
    # -----------------------------------------------------

    df["month_name"] = df["dteday"].dt.month_name()

    # -----------------------------------------------------
    # Day Name
    # -----------------------------------------------------

    df["day_name"] = df["dteday"].dt.day_name()

    # -----------------------------------------------------
    # Weekend Feature
    # -----------------------------------------------------

    df["is_weekend"] = df["weekday"].apply(

        lambda x: 1 if x in [0, 6] else 0
    )

    # -----------------------------------------------------
    # Peak Hour Feature
    # -----------------------------------------------------

    df["is_peak_hour"] = df["hr"].apply(

        lambda x: 1 if x in [7, 8, 9, 17, 18, 19] else 0
    )

    print("\nTime-based features created successfully.")

except Exception as error:

    print("\nERROR while creating time features:")
    print(error)

    raise SystemExit


# =========================================================
# Handle Missing Values
# =========================================================

print("\n========================================")
print(" Handling Missing Values ")
print("========================================")

# ---------------------------------------------------------
# Numeric Columns
# ---------------------------------------------------------

numeric_columns = df.select_dtypes(

    include=[np.number]

).columns

df[numeric_columns] = df[

    numeric_columns

].fillna(

    df[numeric_columns].median()
)

# ---------------------------------------------------------
# Object Columns
# ---------------------------------------------------------

object_columns = df.select_dtypes(

    include=["object"]

).columns

for column in object_columns:

    df[column] = df[column].fillna(

        "Unknown"
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
# Remove Duplicate Rows
# =========================================================

print("\n========================================")
print(" Removing Duplicate Rows ")
print("========================================")

duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows Found:")
print(duplicate_rows)

if duplicate_rows > 0:

    df.drop_duplicates(

        inplace=True
    )

    print("\nDuplicate rows removed.")

else:

    print("\nNo duplicate rows found.")


# =========================================================
# Encode Seasonal Features
# =========================================================

print("\n========================================")
print(" Encoding Seasonal Features ")
print("========================================")

season_mapping = {

    1: "Spring",

    2: "Summer",

    3: "Fall",

    4: "Winter"
}

weather_mapping = {

    1: "Clear",

    2: "Mist",

    3: "Light_Rain",

    4: "Heavy_Rain"
}

df["season_label"] = df["season"].map(

    season_mapping
)

df["weather_label"] = df["weathersit"].map(

    weather_mapping
)

print("\nSeasonal labels encoded successfully.")


# =========================================================
# Create Demand Categories
# =========================================================

print("\n========================================")
print(" Creating Demand Categories ")
print("========================================")

try:

    df["demand_category"] = pd.qcut(

        df["cnt"],

        q=4,

        labels=[

            "Low",

            "Medium",

            "High",

            "Very_High"
        ]
    )

    print("\nDemand categories created successfully.")

except Exception as error:

    print("\nERROR while creating demand categories:")
    print(error)

    raise SystemExit


# =========================================================
# Dataset Summary
# =========================================================

print("\n========================================")
print(" Processed Dataset Summary ")
print("========================================")

print("\nFinal Shape:")
print(df.shape)

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

print("\nColumns:")
print(list(df.columns))


# =========================================================
# Save Processed Dataset
# =========================================================

print("\n========================================")
print(" Saving Processed Dataset ")
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
# Production Pipeline Message
# =========================================================

print("\n========================================")
print(" Dataset Ready For Feature Engineering ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Exploratory Data Analysis")

print("- Feature Scaling")

print("- Model Training")

print("- Forecast Evaluation")

print("- Visualization")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Data Preprocessing Completed Successfully ")
print("========================================")
