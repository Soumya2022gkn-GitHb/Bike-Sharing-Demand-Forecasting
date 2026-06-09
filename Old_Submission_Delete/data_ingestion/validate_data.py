# =========================================================
# File: data_ingestion/validate_data.py
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
# Define Dataset Path
# =========================================================

INPUT_FILE = (

    PROCESSED_DATA_DIR
    / "cleaned_bike_data.csv"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Validating Bike Sharing Dataset ")
print("========================================")


# =========================================================
# Check Dataset Exists
# =========================================================

print("\nDataset Path:")
print(INPUT_FILE)

if not INPUT_FILE.exists():

    print("\nERROR: Cleaned dataset not found.")

    print("\nExpected File:")
    print(INPUT_FILE)

    print("\nPlease run the following first:")

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
# Dataset Shape
# =========================================================

print("\n========================================")
print(" Dataset Information ")
print("========================================")

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(list(df.columns))


# =========================================================
# Required Columns
# =========================================================

required_columns = [

    "instant",

    "dteday",

    "season",

    "yr",

    "mnth",

    "hr",

    "holiday",

    "weekday",

    "workingday",

    "weathersit",

    "temp",

    "atemp",

    "hum",

    "windspeed",

    "cnt"
]


# =========================================================
# Validate Required Columns
# =========================================================

missing_columns = [

    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Missing Required Columns")
    print(missing_columns)

    raise SystemExit

else:

    print("\nAll required columns are available.")


# =========================================================
# Check Dataset Empty
# =========================================================

print("\n========================================")
print(" Checking Dataset Integrity ")
print("========================================")

if df.empty:

    print("\nERROR: Dataset is empty.")

    raise SystemExit

else:

    print("\nDataset contains records.")


# =========================================================
# Check Duplicate Rows
# =========================================================

duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows:")
print(duplicate_rows)

if duplicate_rows > 0:

    print("\nWARNING: Duplicate rows detected.")

else:

    print("\nNo duplicate rows found.")


# =========================================================
# Missing Value Analysis
# =========================================================

print("\n========================================")
print(" Missing Value Analysis ")
print("========================================")

missing_values = df.isnull().sum()

print("\nMissing Values Per Column:")
print(missing_values)

total_missing_values = missing_values.sum()

print("\nTotal Missing Values:")
print(total_missing_values)


# =========================================================
# Infinite Value Analysis
# =========================================================

print("\n========================================")
print(" Infinite Value Analysis ")
print("========================================")

numeric_df = df.select_dtypes(

    include=[np.number]
)

infinite_values = np.isinf(

    numeric_df.values
).sum()

print("\nTotal Infinite Values:")
print(infinite_values)

if infinite_values > 0:

    print("\nWARNING: Infinite values detected.")

else:

    print("\nNo infinite values found.")


# =========================================================
# Validate Target Column
# =========================================================

print("\n========================================")
print(" Validating Target Variable ")
print("========================================")

if "cnt" not in df.columns:

    print("\nERROR: Target column 'cnt' not found.")

    raise SystemExit


# =========================================================
# Check Negative Values
# =========================================================

negative_cnt = (

    df["cnt"] < 0
).sum()

print("\nNegative Target Values:")
print(negative_cnt)

if negative_cnt > 0:

    print("\nWARNING: Negative bike demand values detected.")

else:

    print("\nTarget values are valid.")


# =========================================================
# Validate Date Column
# =========================================================

print("\n========================================")
print(" Validating Date Column ")
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

        print("\nWARNING: Invalid date values found.")

    else:

        print("\nAll date values are valid.")

except Exception as error:

    print("\nERROR while validating dates:")
    print(error)

    raise SystemExit


# =========================================================
# Validate Numeric Columns
# =========================================================

print("\n========================================")
print(" Numeric Feature Validation ")
print("========================================")

numeric_columns = [

    "temp",

    "atemp",

    "hum",

    "windspeed",

    "cnt"
]

for column in numeric_columns:

    if column in df.columns:

        print(f"\nColumn: {column}")

        print(f"Minimum Value: {df[column].min()}")

        print(f"Maximum Value: {df[column].max()}")

        print(f"Mean Value: {round(df[column].mean(), 2)}")


# =========================================================
# Dataset Statistics
# =========================================================

print("\n========================================")
print(" Dataset Statistical Summary ")
print("========================================")

print(df.describe())


# =========================================================
# Final Validation Summary
# =========================================================

print("\n========================================")
print(" Validation Summary ")
print("========================================")

print("\nValidation Checks Completed:")

print("- Dataset existence check")

print("- Required column validation")

print("- Missing value analysis")

print("- Infinite value analysis")

print("- Duplicate row detection")

print("- Date validation")

print("- Target variable validation")

print("- Numeric feature validation")


# =========================================================
# Production Readiness Message
# =========================================================

print("\n========================================")
print(" Dataset Ready For Production Pipeline ")
print("========================================")

print("\nNext Recommended Steps:")

print("- Exploratory Data Analysis")

print("- Feature Engineering")

print("- Forecasting Model Training")

print("- Evaluation & Visualization")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Dataset Validation Completed Successfully ")
print("========================================")
