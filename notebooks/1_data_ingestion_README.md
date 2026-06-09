# 1_data_ingestion_README.md

# Bike Sharing Demand Forecasting - Data Ingestion

## Purpose

`1_data_ingestion.ipynb` is the first notebook in the Bike Sharing Demand Forecasting pipeline. It prepares the raw UCI Bike Sharing Dataset for all later steps: feature engineering, model training, evaluation, plot generation, reports, and the Streamlit dashboard.

The goal of this notebook is simple but important:

- Load the hourly bike-sharing dataset.
- Validate that the data is usable.
- Preprocess dates and numeric weather columns.
- Save a clean dataset for downstream notebooks.
- Give a quick first view of the data shape, date range, schema, and summary statistics.

This notebook does not train models or create plots. It is the foundation that makes the rest of the workflow reliable.

---

## Position In The Project Pipeline

```text
1_data_ingestion.ipynb
        |
        v
2_feature_engineering.ipynb
        |
        v
3_training.ipynb
        |
        v
4_evaluation.ipynb
        |
        v
5_plot_generation.ipynb
        |
        v
6_Building_Streamlit_UI.ipynb
```

The ingestion notebook must run successfully before the later notebooks can use clean, validated data.

---

## Related Files

### Main Notebook

| File | Purpose |
|---|---|
| `notebooks/1_data_ingestion.ipynb` | Loads, validates, preprocesses, and profiles the hourly dataset. |

### Source Code Used

| File | Purpose |
|---|---|
| `src/bsdf/config.py` | Defines project paths such as `data/raw`, `data/processed`, `models`, and `reports/figures`. |
| `src/bsdf/data.py` | Contains reusable ingestion, validation, preprocessing, and loading functions. |

---

## Input Files

The notebook uses the UCI Bike Sharing Dataset. If the required raw file already exists, it is reused. If it is missing, the code downloads and extracts the official archive.

| Input File | Location | How It Is Used |
|---|---|---|
| `bike_sharing_dataset.zip` | `data/raw/bike_sharing_dataset.zip` | Official downloaded UCI dataset archive. Created only if missing. |
| `hour.csv` | `data/raw/hour.csv` | Main hourly dataset used in this project. |
| `day.csv` | `data/raw/day.csv` | Extracted from the archive but not used by this notebook. |
| `Readme.txt` | `data/raw/Readme.txt` | Dataset documentation from UCI. |

### External Dataset Source

```text
https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip
```

The project problem statement refers to:

```text
https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset
```

---

## Output Files Generated

This notebook creates the clean hourly dataset used by the rest of the project.

| Output File | Location | Purpose |
|---|---|---|
| `hourly_clean.csv` | `data/processed/hourly_clean.csv` | Cleaned and timestamp-enriched hourly dataset. Main output of the ingestion stage. |

### Important Note

The notebook may also leave raw extracted files in `data/raw/`, such as `hour.csv`, `day.csv`, and `Readme.txt`. These are raw dataset files, not processed modeling outputs.

---

## Plots Generated

No plots are generated in `1_data_ingestion.ipynb`.

Plot creation happens later in:

```text
notebooks/5_plot_generation.ipynb
```

Examples of plots generated later include:

- `reports/figures/demand_trends.png`
- `reports/figures/weather_demand_analysis.png`
- `reports/figures/correlation_heatmap.png`
- `reports/figures/model_comparison.png`
- `reports/figures/feature_importance.png`

---

## Key Functions Used

### `get_config(PROJECT_ROOT)`

Loads project configuration and creates required folders if needed.

It provides paths for:

- Raw data
- Processed data
- Model artifacts
- Report figures

### `ingest_data(CONFIG)`

Runs the full ingestion workflow:

1. Load or download raw hourly data.
2. Validate required columns and target quality.
3. Preprocess timestamps and numeric columns.
4. Save the clean dataset to `data/processed/hourly_clean.csv`.
5. Return the clean dataset as a Pandas DataFrame.

### `validate_hourly_data(hourly_data)`

Runs data-quality checks:

- Required columns must exist.
- Dataset must not be empty.
- Target column `cnt` must not contain missing values.
- Target column `cnt` must not contain negative values.

---

## Code Section Explanation

## 1. Notebook Introduction

```markdown
# 1. Data Ingestion

Load, validate, and preprocess the hourly UCI Bike Sharing Dataset for the cnt forecasting task.
```

### What This Section Does

This section explains the role of the notebook. It tells the reader that the notebook is focused on getting the hourly demand data ready for forecasting.

### What It Tries To Achieve

It sets expectations: this is not a modeling notebook. It is a data preparation and validation notebook.

---

## 2. Import Libraries And Project Modules

```python
from pathlib import Path
import sys

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from bsdf.config import get_config
from bsdf.data import ingest_data, validate_hourly_data

CONFIG = get_config(PROJECT_ROOT)
```

### What This Section Does

This block prepares the Python environment so the notebook can import project modules from `src/bsdf`.

### Why It Is Needed

Jupyter notebooks can be opened from different working directories. This code makes the notebook more robust by detecting whether it is being run from the project root or from the `notebooks` folder.

### What It Tries To Get

It creates a `CONFIG` object that stores important project paths and settings.

### Clean Code Benefit

Instead of hardcoding paths throughout the notebook, path logic is centralized in `src/bsdf/config.py`.

---

## 3. Folder Structure Documentation

```text
Bike-Sharing-Demand-Forecasting/
|-- app/
|-- data/
|   |-- raw/
|   `-- processed/
|-- models/
|-- notebooks/
|-- reports/
|-- src/
`-- tests/
```

### What This Section Does

This markdown section shows the overall project layout.

### What It Tries To Communicate

It helps the reader understand where raw data, processed data, notebooks, source code, model files, reports, and tests belong.

### Why It Matters

The problem statement asks us to assume that the code may be used in production and maintained by colleagues. A clean folder structure makes the project easier to maintain and extend.

---

## 4. Load, Validate, And Preview Data

```python
hourly_data = ingest_data(CONFIG)
validate_hourly_data(hourly_data)

print(f"Rows: {len(hourly_data):,}")
print(f"Date range: {hourly_data['timestamp'].min()} to {hourly_data['timestamp'].max()}")
hourly_data.head()
```

### What This Section Does

This is the main execution section of the notebook. It loads the dataset, validates it, prints high-level information, and previews the first rows.

### What It Tries To Get

It tries to answer three immediate questions:

1. Did the data load successfully?
2. How many records are available?
3. What time period does the dataset cover?

### Current Output

```text
Rows: 17,379
Date range: 2011-01-01 00:00:00 to 2012-12-31 23:00:00
```

### Data Preview

The notebook displays the first five records. This helps confirm that:

- Expected columns exist.
- Date parsing works.
- The target variable `cnt` is present.
- The generated `timestamp` column is present.

---

## 5. Dataset Schema And Statistical Profile

```python
hourly_data.info()
hourly_data.describe().T
```

### What This Section Does

This section prints the structure and summary statistics of the clean data.

### `hourly_data.info()` Provides

- Number of rows
- Number of columns
- Column names
- Non-null counts
- Data types
- Memory usage

### `hourly_data.describe().T` Provides

- Count
- Mean
- Minimum
- 25th percentile
- Median
- 75th percentile
- Maximum
- Standard deviation

### What It Tries To Get

This section checks whether the dataset looks complete and reasonable before feature engineering begins.

### Current Data Shape

```text
Rows: 17,379
Columns: 18
```

### Important Summary Values

| Field | Value |
|---|---:|
| Average hourly demand `cnt` | 189.46 |
| Median hourly demand `cnt` | 142 |
| Maximum hourly demand `cnt` | 977 |
| Minimum hourly demand `cnt` | 1 |

These values are useful early signals for the forecasting problem. They show that demand is variable and sometimes reaches high peaks, which matters for bicycle readiness planning.

---

## 6. Ingestion Notes

```markdown
- The raw data is downloaded once into data/raw.
- Validation checks required columns, empty data, missing target values, and negative target values.
- Preprocessing parses timestamps, sorts observations chronologically, and fills numeric weather fields if missing.
- Clean data is saved to data/processed/hourly_clean.csv.
```

### What This Section Does

This section summarizes the practical behavior of the ingestion stage.

### What It Tries To Make Clear

It explains what files are created, what validation happens, and how the cleaned data is prepared for downstream steps.

---

## What Happens Inside `ingest_data()`

The notebook calls one high-level function, but that function performs several smaller steps.

```text
ingest_data(CONFIG)
    |
    |-- load_hourly_data(CONFIG)
    |     |
    |     `-- download_dataset(CONFIG), if hour.csv is missing
    |
    |-- validate_hourly_data(raw_data)
    |
    |-- preprocess_hourly_data(raw_data)
    |
    `-- save hourly_clean.csv
```

### Step A: Download Or Reuse Dataset

If `data/raw/hour.csv` exists, it is reused. If it does not exist, the UCI zip file is downloaded and extracted.

### Step B: Validate Raw Data

The raw file is checked before preprocessing. This catches serious issues early.

### Step C: Preprocess Hourly Data

The preprocessing function:

- Converts `dteday` into a datetime column.
- Creates a full hourly `timestamp` from `dteday + hr`.
- Sorts rows chronologically.
- Converts weather numeric columns to numeric type.
- Forward/backward fills numeric weather values if missing.

### Step D: Save Clean Data

The final clean dataset is written to:

```text
data/processed/hourly_clean.csv
```

---

## Column Guide

| Column | Meaning | Used Later? |
|---|---|---|
| `instant` | Record index | No, identifier only |
| `dteday` | Date | Used to create timestamp |
| `season` | Season code | Yes |
| `yr` | Year code | Yes |
| `mnth` | Month | Yes |
| `hr` | Hour of day | Yes |
| `holiday` | Holiday indicator | Yes |
| `weekday` | Day of week | Yes |
| `workingday` | Working day flag | Yes |
| `weathersit` | Weather situation code | Yes |
| `temp` | Normalized temperature | Yes |
| `atemp` | Normalized feels-like temperature | Yes |
| `hum` | Normalized humidity | Yes |
| `windspeed` | Normalized windspeed | Yes |
| `casual` | Casual rental count | No, leakage risk |
| `registered` | Registered rental count | No, leakage risk |
| `cnt` | Total hourly rentals | Target |
| `timestamp` | Full hourly timestamp | Used for splitting, reporting, plots |

---

## Data Quality Checks

The validation function checks:

| Check | Why It Matters |
|---|---|
| Required columns exist | Downstream code depends on a stable schema. |
| Data is not empty | A model cannot train on no rows. |
| `cnt` has no missing values | The target must be known for supervised learning. |
| `cnt` has no negative values | Negative rental counts are invalid. |

These checks are intentionally simple and production-friendly. They catch high-impact problems early without making the ingestion stage overly complex.

---

## Generated Files Summary

### Input Side

```text
data/raw/bike_sharing_dataset.zip
data/raw/hour.csv
data/raw/day.csv
data/raw/Readme.txt
```

### Output Side

```text
data/processed/hourly_clean.csv
```

### Plots

```text
No plots generated in this notebook.
```

---

## Why This Notebook Matters For The Business Problem

The business goal is to forecast hourly demand so a bicycle rental company can plan operations and logistics. Bad input data would create unreliable forecasts. This notebook reduces that risk by making sure the project starts from a clean, validated hourly dataset.

The created `timestamp` column is especially important because later stages use chronological train/test splitting. That better reflects a real forecasting service, where the model is trained on past observations and tested on future periods.

---

## Clean Code And Maintainability Notes

This notebook follows clean-code principles by:

- Keeping notebook cells short and readable.
- Moving reusable logic into `src/bsdf/data.py`.
- Using `CONFIG` instead of hardcoded paths.
- Validating data before saving processed outputs.
- Saving a reusable processed file for later notebooks.
- Keeping ingestion separate from feature engineering and modeling.

This design helps colleagues maintain the workflow and makes it easier to adapt into a scheduled daily prediction service.

---

## Expected Result After Running The Notebook

After running `1_data_ingestion.ipynb`, the project should have:

- A downloaded/extracted raw dataset in `data/raw`.
- A validated clean dataset in `data/processed/hourly_clean.csv`.
- A notebook output showing 17,379 rows.
- A notebook output showing date coverage from `2011-01-01 00:00:00` to `2012-12-31 23:00:00`.
- A schema and statistical profile confirming the data is ready for feature engineering.

---

## Next Step

Continue to:

```text
notebooks/2_feature_engineering.ipynb
```

That notebook creates time features, encoding-ready features, and scaled numeric inputs for model training.

