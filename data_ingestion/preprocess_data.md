# preprocess_data.py

## Project

```text
Bike_Sharing_Demand_Forecasting
```

---

# Overview

The `preprocess_data.py` script is responsible for transforming the validated Bike Sharing dataset into a feature-engineered, machine-learning-ready dataset for hourly bike demand forecasting.

This script performs:
- date conversion,
- time-based feature creation,
- missing value handling,
- infinite value removal,
- duplicate removal,
- categorical encoding,
- and demand categorization.

The final processed dataset is saved for:
- exploratory data analysis (EDA),
- feature engineering,
- forecasting model training,
- evaluation,
- and deployment.

The preprocessing pipeline is designed using production-quality software engineering principles to ensure:
- maintainability,
- reliability,
- scalability,
- and team collaboration.

---

# File Location

```text
Bike_Sharing_Demand_Forecasting/
│
├── data_ingestion/
│   └── preprocess_data.py
```

---

# Purpose

The purpose of this script is to prepare the bike-sharing dataset for forecasting models by:
- engineering meaningful time-based features,
- cleaning remaining data quality issues,
- and generating business-relevant demand indicators.

This script bridges the gap between:
```text
raw cleaned data
```

and:
```text
machine learning forecasting pipeline
```

---

# Input Dataset

The script expects:

```text
data/processed/cleaned_bike_data.csv
```

Generated from:

```bash
python data_ingestion/load_data.py
```

---

# Output Dataset

The script generates:

```text
data/processed/feature_engineered_data.csv
```

This dataset is used for:
- model training,
- evaluation,
- visualization,
- and forecasting.

---

# Workflow

```text
Validated Dataset
        ↓
Date Conversion
        ↓
Time Feature Engineering
        ↓
Missing Value Handling
        ↓
Infinite Value Removal
        ↓
Duplicate Row Removal
        ↓
Seasonal Feature Encoding
        ↓
Demand Categorization
        ↓
Feature Engineered Dataset
```

---

# Key Functionalities

---

# 1. Date Conversion

The script converts:

```text
dteday
```

into datetime format using:

```python
pd.to_datetime()
```

Invalid dates are automatically detected and removed.

---

# 2. Time-Based Feature Engineering

The script creates business-relevant temporal features.

## Generated Features

| Feature | Description |
|---|---|
| day | Day of month |
| month_name | Month name |
| day_name | Weekday name |
| is_weekend | Weekend indicator |
| is_peak_hour | Peak rental hour indicator |

---

# 3. Peak Hour Detection

The script identifies high-demand commuting hours:

```text
7 AM – 9 AM
5 PM – 7 PM
```

These are labeled using:

```python
is_peak_hour
```

This improves forecasting accuracy.

---

# 4. Missing Value Handling

## Numeric Columns
Missing numeric values are filled using:
```python
median()
```

## Object Columns
Missing categorical values are replaced with:
```text
Unknown
```

---

# 5. Infinite Value Removal

The preprocessing pipeline removes:

```text
+∞
-∞
```

using:

```python
replace([np.inf, -np.inf], np.nan)
```

Infinite values are replaced safely before model training.

---

# 6. Duplicate Row Removal

Duplicate records are automatically:
- detected,
- counted,
- and removed.

This prevents:
- biased forecasting,
- duplicate training signals,
- and inaccurate demand estimation.

---

# 7. Seasonal Feature Encoding

The script converts encoded seasonal values into readable business labels.

## Season Mapping

| Code | Label |
|---|---|
| 1 | Spring |
| 2 | Summer |
| 3 | Fall |
| 4 | Winter |

---

## Weather Mapping

| Code | Label |
|---|---|
| 1 | Clear |
| 2 | Mist |
| 3 | Light_Rain |
| 4 | Heavy_Rain |

This improves:
- interpretability,
- business reporting,
- and visualization quality.

---

# 8. Demand Categorization

The script creates demand segments using:

```python
pd.qcut()
```

## Demand Categories

| Category | Meaning |
|---|---|
| Low | Low rental demand |
| Medium | Moderate rental demand |
| High | High rental demand |
| Very_High | Peak rental demand |

These categories support:
- business reporting,
- demand analysis,
- and future classification extensions.

---

# Dataset Summary

The preprocessing pipeline reports:
- final dataset shape,
- missing value counts,
- generated features,
- and processed columns.

---

# Production-Ready Design

The script follows production-grade software engineering practices.

## Maintainability
- section-based organization,
- descriptive variable names,
- modular workflow.

## Reliability
- input validation,
- exception handling,
- safe preprocessing steps.

## Scalability
- reusable preprocessing logic,
- future feature expansion support.

## Collaboration Friendly
- readable console outputs,
- easy debugging,
- and teammate maintainability.

---

# Running the Script

From project root:

```bash
python data_ingestion/preprocess_data.py
```

---

# Example Console Output

```text
========================================
 Preprocessing Bike Sharing Dataset
========================================

Time-based features created successfully.

Missing values handled successfully.

Infinite values removed successfully.

Seasonal labels encoded successfully.

Demand categories created successfully.

Dataset saved successfully.

Saved File:
data/processed/feature_engineered_data.csv
```

---

# Business Importance

Preprocessing directly impacts forecasting quality.

Well-engineered features help forecasting models:
- identify peak demand patterns,
- learn seasonal behavior,
- understand commuting trends,
- and improve operational planning accuracy.

For a bicycle rental company, this supports:
- bicycle allocation,
- logistics planning,
- staffing optimization,
- and demand forecasting.

---

# Pipeline Position

```text
load_data.py
        ↓
validate_data.py
        ↓
preprocess_data.py
        ↓
feature_engineering/
        ↓
training/
        ↓
evaluation/
```

---

# Next Recommended Step

After preprocessing:

```bash
python feature_engineering/create_time_features.py
```

or continue with:
- scaling,
- model training,
- evaluation,
- and visualization.

---

# Summary

The `preprocess_data.py` script transforms validated bike-sharing data into a feature-engineered forecasting dataset optimized for machine learning and business demand analysis. It creates meaningful temporal and seasonal features while ensuring data quality, reliability, and production readiness for hourly bike rental forecasting.