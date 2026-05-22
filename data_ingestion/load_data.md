# Data Ingestion — load_data.py

## Overview

The `load_data.py` script is the first stage of the Bike Sharing Demand Forecasting pipeline. It is responsible for loading the raw Bike Sharing dataset, validating its structure, cleaning basic data quality issues, and generating a processed dataset ready for Exploratory Data Analysis (EDA), feature engineering, and machine learning model training.

The script is designed using production-ready practices such as:
- modular structure,
- dataset validation,
- error handling,
- logging-style outputs,
- missing value handling,
- duplicate removal,
- and automated processed file generation.

---

# Purpose

The primary objective of this script is to:

- load the raw Bike Sharing dataset,
- validate required columns,
- clean invalid or duplicate records,
- handle missing values,
- convert date columns into datetime format,
- and save a cleaned dataset for downstream forecasting tasks.

---

# Input Dataset

The script expects the following file:

```text
data/raw/hour.csv
```

Dataset Source:

```text
https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset
```

---

# Output Dataset

After successful execution, the script generates:

```text
data/processed/cleaned_bike_data.csv
```

This cleaned dataset is used in:
- feature engineering,
- exploratory analysis,
- forecasting model training,
- and evaluation.

---

# Folder Structure

```text
Bike_Sharing_Demand_Forecasting/
│
├── data/
│   ├── raw/
│   │   └── hour.csv
│   │
│   └── processed/
│       └── cleaned_bike_data.csv
│
├── data_ingestion/
│   └── load_data.py
```

---

# Key Functionalities

## 1. Dataset Loading

The script reads the raw CSV dataset using:

```python
pd.read_csv()
```

and verifies whether the file exists before loading.

---

## 2. Dataset Validation

The script validates important columns required for bike demand forecasting.

### Required Columns

| Column | Description |
|---|---|
| instant | Record index |
| dteday | Date |
| season | Season category |
| yr | Year |
| mnth | Month |
| hr | Hour |
| holiday | Holiday indicator |
| weekday | Day of week |
| workingday | Working day flag |
| weathersit | Weather condition |
| temp | Temperature |
| atemp | Feels-like temperature |
| hum | Humidity |
| windspeed | Wind speed |
| cnt | Total bike rentals |

---

## 3. Duplicate Removal

The script automatically:
- detects duplicate rows,
- removes duplicates,
- and reports duplicate counts.

---

## 4. Date Conversion

The `dteday` column is converted into datetime format using:

```python
pd.to_datetime()
```

Invalid dates are detected and removed automatically.

---

## 5. Missing Value Handling

### Numeric Columns
Missing numeric values are filled using:
```python
median()
```

### Object Columns
Missing categorical values are replaced with:
```text
Unknown
```

---

## 6. Processed File Generation

The script automatically creates the processed data directory if it does not exist and saves:

```text
cleaned_bike_data.csv
```

---

# Workflow

```text
Raw Bike Sharing Dataset
            ↓
Dataset Validation
            ↓
Duplicate Removal
            ↓
Date Conversion
            ↓
Missing Value Handling
            ↓
Processed Dataset Generation
            ↓
Ready for Feature Engineering & ML
```

---

# Production-Ready Design

This script follows production-quality software engineering practices:

## Maintainability
- modular code structure,
- descriptive variable names,
- section-based organization.

## Reliability
- input validation,
- exception handling,
- automatic directory creation.

## Reusability
- reusable project path management,
- scalable ingestion logic.

## Collaboration Friendly
- readable code formatting,
- detailed console outputs,
- easy debugging for teammates.

---

# Running the Script

From the project root:

```bash
python data_ingestion/load_data.py
```

---

# Example Console Output

```text
========================================
 Loading Bike Sharing Dataset
========================================

Dataset Shape:
(17379, 17)

All required columns are available.

Duplicate Rows Found:
0

Dataset Saved Successfully

Saved File:
data/processed/cleaned_bike_data.csv
```

---

# Business Impact

Accurate and clean data ingestion is critical because:
- forecasting quality depends on data quality,
- operational planning requires reliable hourly predictions,
- and downstream ML models rely on properly validated datasets.

This script ensures the forecasting pipeline begins with:
- validated,
- clean,
- and production-ready data.

---

# Next Pipeline Step

After running:

```bash
python data_ingestion/load_data.py
```

the next step is:

```bash
python data_ingestion/validate_data.py
```

or:

```bash
python feature_engineering/create_time_features.py
```

depending on the pipeline flow.

---

# Summary

The `load_data.py` script forms the foundation of the Bike Sharing Demand Forecasting pipeline by transforming raw bike rental records into a clean, validated, and ML-ready dataset. It ensures robustness, maintainability, and production-level data quality for accurate hourly demand forecasting.