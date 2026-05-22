# =========================================================
# File: feature_engineering/create_time_features.py
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
    / "feature_engineered_data.csv"
)

OUTPUT_FILE = (

    PROCESSED_DATA_DIR
    / "time_feature_engineered_data.csv"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Creating Time-Based Features ")
print("========================================")


# =========================================================
# Check Input Dataset Exists
# =========================================================

print("\nInput Dataset:")
print(INPUT_FILE)

if not INPUT_FILE.exists():

    print("\nERROR: Feature engineered dataset not found.")

    print("\nPlease run:")

    print("\npython data_ingestion/preprocess_data.py")

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
print(" Converting Date Column ")
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
# Create Advanced Time Features
# =========================================================

print("\n========================================")
print(" Generating Advanced Time Features ")
print("========================================")

try:

    # -----------------------------------------------------
    # Year Feature
    # -----------------------------------------------------

    df["year"] = df["dteday"].dt.year

    # -----------------------------------------------------
    # Quarter Feature
    # -----------------------------------------------------

    df["quarter"] = df["dteday"].dt.quarter

    # -----------------------------------------------------
    # Week Of Year
    # -----------------------------------------------------

    df["week_of_year"] = df["dteday"].dt.isocalendar().week.astype(int)

    # -----------------------------------------------------
    # Day Of Year
    # -----------------------------------------------------

    df["day_of_year"] = df["dteday"].dt.dayofyear

    # -----------------------------------------------------
    # Hour Grouping
    # -----------------------------------------------------

    df["hour_group"] = pd.cut(

        df["hr"],

        bins=[0, 6, 12, 18, 24],

        labels=[

            "Night",

            "Morning",

            "Afternoon",

            "Evening"
        ],

        include_lowest=True
    )

    # -----------------------------------------------------
    # Business Hours
    # -----------------------------------------------------

    df["business_hours"] = df["hr"].apply(

        lambda x: 1 if 9 <= x <= 18 else 0
    )

    # -----------------------------------------------------
    # Late Night Indicator
    # -----------------------------------------------------

    df["late_night"] = df["hr"].apply(

        lambda x: 1 if x >= 22 or x <= 5 else 0
    )

    # -----------------------------------------------------
    # Rush Hour Indicator
    # -----------------------------------------------------

    df["rush_hour"] = df["hr"].apply(

        lambda x: 1 if x in [7, 8, 9, 17, 18, 19] else 0
    )

    print("\nAdvanced time features created successfully.")

except Exception as error:

    print("\nERROR while generating time features:")
    print(error)

    raise SystemExit


# =========================================================
# Create Seasonal Flags
# =========================================================

print("\n========================================")
print(" Creating Seasonal Flags ")
print("========================================")

try:

    df["is_summer"] = df["season"].apply(

        lambda x: 1 if x == 2 else 0
    )

    df["is_winter"] = df["season"].apply(

        lambda x: 1 if x == 4 else 0
    )

    df["is_fall"] = df["season"].apply(

        lambda x: 1 if x == 3 else 0
    )

    df["is_spring"] = df["season"].apply(

        lambda x: 1 if x == 1 else 0
    )

    print("\nSeasonal flags created successfully.")

except Exception as error:

    print("\nERROR while creating seasonal flags:")
    print(error)

    raise SystemExit


# =========================================================
# Create Weather Severity Feature
# =========================================================

print("\n========================================")
print(" Creating Weather Severity Feature ")
print("========================================")

try:

    weather_mapping = {

        1: "Good",

        2: "Moderate",

        3: "Poor",

        4: "Severe"
    }

    df["weather_severity"] = df["weathersit"].map(

        weather_mapping
    )

    print("\nWeather severity feature created successfully.")

except Exception as error:

    print("\nERROR while creating weather feature:")
    print(error)

    raise SystemExit


# =========================================================
# Create Cyclical Features
# =========================================================

print("\n========================================")
print(" Creating Cyclical Features ")
print("========================================")

try:

    # -----------------------------------------------------
    # Hour Cyclical Encoding
    # -----------------------------------------------------

    df["hr_sin"] = np.sin(

        2 * np.pi * df["hr"] / 24
    )

    df["hr_cos"] = np.cos(

        2 * np.pi * df["hr"] / 24
    )

    # -----------------------------------------------------
    # Month Cyclical Encoding
    # -----------------------------------------------------

    df["mnth_sin"] = np.sin(

        2 * np.pi * df["mnth"] / 12
    )

    df["mnth_cos"] = np.cos(

        2 * np.pi * df["mnth"] / 12
    )

    print("\nCyclical features created successfully.")

except Exception as error:

    print("\nERROR while creating cyclical features:")
    print(error)

    raise SystemExit


# =========================================================
# Handle Missing Values
# =========================================================

print("\n========================================")
print(" Handling Missing Values ")
print("========================================")

# ---------------------------------------------------------
# Fill Numeric Columns
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
# Fill Object & Category Columns
# ---------------------------------------------------------

categorical_columns = df.select_dtypes(

    include=["object", "category"]

).columns

for column in categorical_columns:

    # -----------------------------------------------------
    # Handle Category Columns
    # -----------------------------------------------------

    if str(df[column].dtype) == "category":

        df[column] = df[column].cat.add_categories(

            ["Unknown"]
        )

    # -----------------------------------------------------
    # Fill Missing Values
    # -----------------------------------------------------

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
# Dataset Summary
# =========================================================

print("\n========================================")
print(" Final Dataset Summary ")
print("========================================")

print("\nFinal Shape:")
print(df.shape)

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

print("\nColumns:")
print(list(df.columns))


# =========================================================
# Save Dataset
# =========================================================

print("\n========================================")
print(" Saving Time Feature Dataset ")
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
print(" Dataset Ready For Model Training ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Encode Categorical Features")

print("- Scale Features")

print("- Train Forecasting Models")

print("- Evaluate Prediction Accuracy")

print("- Generate Forecast Visualizations")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Time Feature Engineering Completed Successfully ")
print("========================================")
