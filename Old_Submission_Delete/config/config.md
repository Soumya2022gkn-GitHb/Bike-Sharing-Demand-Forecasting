# config.py

## Project

```text
Bike_Sharing_Demand_Forecasting
```

---

# Overview

The `config.py` file is the centralized configuration module for the Bike Sharing Demand Forecasting project.

It stores:
- project paths,
- dataset locations,
- model settings,
- forecasting parameters,
- feature lists,
- visualization settings,
- and production configurations.

This file ensures:
- maintainability,
- scalability,
- consistency,
- and production-ready engineering practices.

---

# File Location

```text
Bike_Sharing_Demand_Forecasting/
│
├── config/
│   └── config.py
```

---

# Purpose

The purpose of `config.py` is to:
- avoid hardcoded values,
- centralize configuration management,
- simplify collaboration,
- improve maintainability,
- and support scalable deployment.

---

# Why Configuration Files Matter

In production-grade machine learning systems:
- settings should not be scattered across files,
- paths should be reusable,
- and parameters should be centrally managed.

This improves:
- debugging,
- deployment,
- testing,
- and collaboration.

---

# Main Responsibilities

The `config.py` module manages:

| Category | Purpose |
|---|---|
| File Paths | Centralized project directories |
| Dataset Configurations | Data locations |
| Model Parameters | ML model hyperparameters |
| Forecasting Settings | Forecast refresh and horizon |
| Visualization Settings | Plot styles and image exports |
| Feature Lists | ML input features |
| Logging Configuration | Monitoring and debugging |
| Business Settings | Operational recommendations |

---

# Project Root Configuration

## Purpose

Defines the main project directory.

---

# Code Section

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
```

---

# Why It Matters

Provides:
- portable file handling,
- OS-independent paths,
- and scalable project structure.

---

# Data Directory Configuration

## Purpose

Stores all dataset-related paths.

---

# Configured Paths

```python
DATA_DIR
RAW_DATA_DIR
PROCESSED_DATA_DIR
```

---

# Example Structure

```text
data/
│
├── raw/
│   └── hour.csv
│
└── processed/
    ├── cleaned_bike_data.csv
    ├── train_dataset.csv
    └── test_dataset.csv
```

---

# Dataset File Configuration

## Purpose

Defines dataset file locations.

---

# Files Managed

| File | Purpose |
|---|---|
| hour.csv | Raw dataset |
| cleaned_bike_data.csv | Cleaned data |
| feature_engineered_data.csv | Engineered dataset |
| train_dataset.csv | Training data |
| test_dataset.csv | Testing data |

---

# Why It Matters

Centralized file management:
- improves maintainability,
- reduces duplication,
- and prevents path errors.

---

# Model Directory Configuration

## Purpose

Stores trained machine learning models.

---

# Managed Models

| Model | Purpose |
|---|---|
| linear_regression_model.pkl | Baseline model |
| random_forest_model.pkl | Ensemble model |
| xgboost_model.pkl | Final production model |
| scaler.pkl | Feature scaler |

---

# Why It Matters

Supports:
- model persistence,
- deployment,
- and reproducibility.

---

# Forecasting Target Configuration

## Purpose

Defines the prediction target.

---

# Target Variable

```python
TARGET_COLUMN = "cnt"
```

---

# Meaning

```text
Hourly Bike Rental Demand
```

---

# Feature Configuration

## Purpose

Stores all forecasting features.

---

# Example Features

```python
FEATURE_COLUMNS = [
    "season",
    "hr",
    "temp",
    "hum",
    "windspeed"
]
```

---

# Why It Matters

Improves:
- feature consistency,
- pipeline reuse,
- and forecasting stability.

---

# Categorical Features

## Purpose

Defines categorical variables.

---

# Example

```python
CATEGORICAL_FEATURES = [
    "season",
    "holiday",
    "workingday"
]
```

---

# Why It Matters

Required for:
- encoding,
- preprocessing,
- and ML pipeline compatibility.

---

# Numerical Features

## Purpose

Defines continuous variables.

---

# Example

```python
NUMERICAL_FEATURES = [
    "temp",
    "hum",
    "windspeed"
]
```

---

# Why It Matters

Used for:
- scaling,
- normalization,
- and statistical analysis.

---

# Model Hyperparameter Configuration

## Purpose

Stores machine learning parameters.

---

# Random Forest Parameters

Example:

```python
RANDOM_FOREST_PARAMS = {
    "n_estimators": 200
}
```

---

# XGBoost Parameters

Example:

```python
XGBOOST_PARAMS = {
    "learning_rate": 0.05
}
```

---

# Why It Matters

Supports:
- reproducibility,
- tuning,
- and maintainability.

---

# Evaluation Metrics Configuration

## Purpose

Defines forecasting evaluation metrics.

---

# Metrics Used

| Metric | Purpose |
|---|---|
| MAE | Average prediction error |
| RMSE | Penalizes large errors |
| R² | Model explanatory power |

---

# Why These Metrics Matter

These metrics help evaluate:
- forecasting accuracy,
- operational reliability,
- and business readiness.

---

# Visualization Configuration

## Purpose

Stores plotting and visualization settings.

---

# Example Configurations

```python
FIGURE_SIZE = (12, 6)
SAVE_DPI = 300
```

---

# Why It Matters

Ensures:
- consistent visualizations,
- report-quality graphics,
- and dashboard compatibility.

---

# Graph Output Configuration

## Purpose

Defines visualization export paths.

---

# Example Files

| File | Purpose |
|---|---|
| hourly_demand.png | Demand trend analysis |
| seasonal_trends.png | Seasonal forecasting insights |
| correlation_heatmap.png | Feature correlation analysis |

---

# Why It Matters

Improves:
- report generation,
- business presentations,
- and EDA reproducibility.

---

# Streamlit Dashboard Configuration

## Purpose

Stores Streamlit UI settings.

---

# Example

```python
STREAMLIT_APP_TITLE
STREAMLIT_LAYOUT
```

---

# Why It Matters

Supports:
- dashboard consistency,
- deployment,
- and UI maintainability.

---

# Forecasting Configuration

## Purpose

Stores operational forecasting settings.

---

# Configurations

| Setting | Value |
|---|---|
| Forecast Refresh | 1–3 Hours |
| Forecast Horizon | 24–72 Hours |
| Retraining Frequency | Monthly |

---

# Why These Settings Matter

They improve:
- operational planning,
- forecast reliability,
- and production performance.

---

# Logging Configuration

## Purpose

Stores log file settings.

---

# Example

```python
LOG_FILE
ENABLE_LOGGING
```

---

# Why Logging Matters

Logging supports:
- debugging,
- monitoring,
- error tracking,
- and production reliability.

---

# Weather Label Mapping

## Purpose

Converts weather codes into readable labels.

---

# Example

```python
WEATHER_LABELS = {
    1: "Clear",
    2: "Mist"
}
```

---

# Why It Matters

Improves:
- readability,
- reporting,
- and dashboard usability.

---

# Season Label Mapping

## Purpose

Converts season codes into business-friendly names.

---

# Example

```python
SEASON_LABELS = {
    1: "Spring",
    2: "Summer"
}
```

---

# Business Objectives Configuration

## Purpose

Stores project business goals.

---

# Example Objectives

- Improve bicycle allocation
- Reduce operational shortages
- Optimize workforce planning
- Improve customer satisfaction

---

# Why It Matters

Keeps:
- business goals,
- forecasting objectives,
- and deployment priorities aligned.

---

# Operational Recommendations

## Purpose

Stores production forecasting recommendations.

---

# Example Recommendations

- Refresh forecasts every 1–3 hours
- Retrain models seasonally
- Track model drift continuously

---

# Why It Matters

Supports:
- operational forecasting,
- production maintenance,
- and reliability.

---

# Production-Ready Engineering Practices

The configuration module supports:

- modular architecture,
- scalable pipelines,
- reusable configurations,
- logging,
- monitoring,
- and deployment readiness.

---

# Benefits of Centralized Configuration

| Benefit | Description |
|---|---|
| Maintainability | Easier updates |
| Scalability | Supports deployment |
| Consistency | Shared project settings |
| Reusability | Avoids duplication |
| Collaboration | Cleaner engineering workflows |

---

# Running the Configuration File

Execute:

```bash
python config/config.py
```

---

# Expected Console Output

```text
============================================================
 Bike Sharing Forecasting Configuration
============================================================

Project Root:
...

Target Variable:
cnt

Forecast Horizon:
24-72 Hours
```

---

# Dependencies

## Required Libraries

- pathlib

---

# Installation

```bash
pip install pathlib
```

(Note: pathlib is included in modern Python versions.)

---

# Future Improvements

Potential future enhancements:
- environment variable support,
- YAML/JSON configuration files,
- cloud deployment configuration,
- API configuration management,
- and multi-environment support.

---

# Summary

The `config.py` module centralizes all configurations for the Bike Sharing Demand Forecasting project. It manages project paths, datasets, machine learning settings, forecasting parameters, visualization configurations, and operational recommendations. The module improves maintainability, scalability, collaboration, deployment readiness, and production-grade engineering practices for the forecasting system.