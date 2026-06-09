# =========================================================
# File: data_ingestion/load_data.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd


# =========================================================
# Define Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

RAW_DATA_DIR = (

    PROJECT_ROOT
    / "data"
    / "raw"
)

PROCESSED_DATA_DIR = (

    PROJECT_ROOT
    / "data"
    / "processed"
)


# =========================================================
# Define Dataset Paths
# =========================================================

INPUT_FILE = (

    RAW_DATA_DIR
    / "hour.csv"
)

OUTPUT_FILE = (

    PROCESSED_DATA_DIR
    / "cleaned_bike_data.csv"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Loading Bike Sharing Dataset ")
print("========================================")


# =========================================================
# Check Dataset Exists
# =========================================================

print("\nDataset Path:")
print(INPUT_FILE)

if not INPUT_FILE.exists():

    print("\nERROR: Dataset file not found.")

    print("\nExpected File:")
    print(INPUT_FILE)

    print("\nDownload Dataset From:")
    print(
        "https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset"
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
# Display Dataset Information
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
# Remove Duplicate Rows
# =========================================================

duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows Found:")
print(duplicate_rows)

if duplicate_rows > 0:

    df.drop_duplicates(

        inplace=True
    )

    print("\nDuplicate rows removed.")


# =========================================================
# Convert Date Column
# =========================================================

try:

    df["dteday"] = pd.to_datetime(

        df["dteday"],

        errors="coerce"
    )

    invalid_dates = df["dteday"].isnull().sum()

    print("\nInvalid Dates Found:")
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
# Check Missing Values
# =========================================================

print("\n========================================")
print(" Missing Value Analysis ")
print("========================================")

missing_values = df.isnull().sum()

print("\nMissing Values Per Column:")
print(missing_values)


# =========================================================
# Fill Missing Numeric Values
# =========================================================

numeric_columns = df.select_dtypes(

    include=["int64", "float64"]

).columns

df[numeric_columns] = df[

    numeric_columns

].fillna(

    df[numeric_columns].median()
)


# =========================================================
# Fill Missing Object Values
# =========================================================

object_columns = df.select_dtypes(

    include=["object"]

).columns

for column in object_columns:

    df[column] = df[column].fillna(

        "Unknown"
    )


# =========================================================
# Create Processed Data Directory
# =========================================================

PROCESSED_DATA_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Save Cleaned Dataset
# =========================================================

try:

    df.to_csv(

        OUTPUT_FILE,

        index=False
    )

    print("\n========================================")
    print(" Dataset Saved Successfully ")
    print("========================================")

    print("\nSaved File:")
    print(OUTPUT_FILE)

except Exception as error:

    print("\nERROR while saving dataset:")
    print(error)

    raise SystemExit


# =========================================================
# Final Dataset Summary
# =========================================================

print("\n========================================")
print(" Final Dataset Summary ")
print("========================================")

print("\nFinal Shape:")
print(df.shape)

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

print("\nDataset Ready For:")
print("- Exploratory Data Analysis")
print("- Feature Engineering")
print("- Forecasting Model Training")
print("- Business Demand Forecasting")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Bike Sharing Dataset Loaded Successfully ")
print("========================================")
