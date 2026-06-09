# create_time_features.py

## Project

```text
Bike_Sharing_Demand_Forecasting
```

---

# Overview

The `create_time_features.py` script is responsible for generating advanced time-based and cyclical features for the Bike Sharing Demand Forecasting project.

Time-based feature engineering is one of the most important stages in forecasting hourly bicycle demand because bike rentals are highly dependent on:
- hour of day,
- weekdays,
- weekends,
- commuting hours,
- seasons,
- weather conditions,
- and yearly trends.

This script transforms the processed dataset into a forecasting-ready dataset optimized for machine learning models such as:
- Random Forest,
- XGBoost,
- and Linear Regression.

The generated features improve the model’s ability to capture:
- seasonal demand patterns,
- commuting behavior,
- peak-hour rentals,
- and cyclical time dependencies.

---

# File Location

```text
Bike_Sharing_Demand_Forecasting/
│
├── feature_engineering/
│   └── create_time_features.py
```

---

# Purpose

The purpose of this script is to:
- generate advanced time-based forecasting features,
- create cyclical encodings,
- engineer seasonal indicators,
- improve model learning capability,
- and prepare the dataset for production-grade forecasting models.

This script acts as the core feature engineering layer for bike demand forecasting.

---

# Input Dataset

The script expects:

```text
data/processed/feature_engineered_data.csv
```

Generated from:

```bash
python data_ingestion/preprocess_data.py
```

---

# Output Dataset

The script generates:

```text
data/processed/time_feature_engineered_data.csv
```

This dataset is used for:
- forecasting model training,
- evaluation,
- visualization,
- and deployment.

---

# Workflow

```text
Processed Dataset
        ↓
Date Conversion
        ↓
Advanced Time Feature Creation
        ↓
Seasonal Feature Engineering
        ↓
Weather Severity Mapping
        ↓
Cyclical Encoding
        ↓
Missing Value Handling
        ↓
Infinite Value Removal
        ↓
Final Forecasting Dataset
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

# 2. Advanced Time Feature Engineering

The script creates multiple temporal forecasting features.

## Generated Features

| Feature | Description |
|---|---|
| year | Calendar year |
| quarter | Quarter of year |
| week_of_year | Week number |
| day_of_year | Day number in year |
| business_hours | Office-hour indicator |
| late_night | Late-night rental indicator |
| rush_hour | Peak commuting hour indicator |

These features help forecasting models identify:
- daily demand cycles,
- weekly behavior,
- yearly seasonality,
- and operational demand spikes.

---

# 3. Hour Grouping

The script groups hours into business-relevant periods.

## Hour Groups

| Group | Hours |
|---|---|
| Night | 12 AM – 6 AM |
| Morning | 6 AM – 12 PM |
| Afternoon | 12 PM – 6 PM |
| Evening | 6 PM – 12 AM |

This improves:
- interpretability,
- business reporting,
- and demand segmentation.

---

# 4. Business Hour Detection

The script identifies standard business hours:

```text
9 AM – 6 PM
```

using:

```python
business_hours
```

This helps models capture:
- commuting demand,
- office travel patterns,
- and workday utilization.

---

# 5. Rush Hour Detection

Peak commuting periods are detected:

```text
7 AM – 9 AM
5 PM – 7 PM
```

using:

```python
rush_hour
```

This feature significantly improves forecasting performance for urban transportation patterns.

---

# 6. Seasonal Flags

The script creates binary seasonal indicators.

## Seasonal Features

| Feature | Description |
|---|---|
| is_summer | Summer season |
| is_winter | Winter season |
| is_fall | Fall season |
| is_spring | Spring season |

These flags help forecasting models learn:
- weather-driven demand,
- seasonal utilization changes,
- and yearly rental trends.

---

# 7. Weather Severity Feature

Weather conditions are converted into business-friendly labels.

## Weather Mapping

| Code | Severity |
|---|---|
| 1 | Good |
| 2 | Moderate |
| 3 | Poor |
| 4 | Severe |

This improves:
- business understanding,
- reporting quality,
- and visualization readability.

---

# 8. Cyclical Feature Engineering

Time variables such as:
- hours,
- months,
- weekdays

are cyclical by nature.

The script applies:
```python
sin()
cos()
```

transformations to preserve cyclical relationships.

## Generated Cyclical Features

| Feature | Purpose |
|---|---|
| hr_sin | Hour cyclic encoding |
| hr_cos | Hour cyclic encoding |
| mnth_sin | Month cyclic encoding |
| mnth_cos | Month cyclic encoding |

Example:
```text
23:00 and 00:00 are close in time
```

Cyclical encoding helps models understand this relationship.

---

# 9. Missing Value Handling

## Numeric Columns
Missing numeric values are filled using:
```python
median()
```

## Categorical Columns
Missing categorical values are safely filled using:
```text
Unknown
```

### Important Production Fix

Category columns require:

```python
cat.add_categories()
```

before adding new labels.

This prevents:

```text
TypeError:
Cannot setitem on a Categorical with a new category
```

---

# 10. Infinite Value Removal

The script safely removes:

```text
+∞
-∞
```

before model training.

This prevents:
- training failures,
- scaling issues,
- and unstable evaluation metrics.

---

# Production-Ready Design

The script follows production-quality software engineering practices.

## Maintainability
- modular sections,
- readable formatting,
- descriptive naming.

## Reliability
- exception handling,
- dataset validation,
- safe preprocessing.

## Scalability
- reusable feature engineering pipeline,
- future forecasting expansion support.

## Team Collaboration
The code is structured so teammates can:
- debug easily,
- extend features,
- and maintain forecasting pipelines.

---

# Running the Script

From project root:

```bash
python feature_engineering/create_time_features.py
```

---

# Example Console Output

```text
========================================
 Creating Time-Based Features
========================================

Advanced time features created successfully.

Seasonal flags created successfully.

Weather severity feature created successfully.

Cyclical features created successfully.

Missing values handled successfully.

Infinite values removed successfully.

Dataset saved successfully.
```

---

# Business Importance

Time-based features are critical for demand forecasting because bicycle rentals are strongly influenced by:
- commuting schedules,
- workdays,
- seasons,
- weather,
- and rush-hour behavior.

These engineered features help businesses:
- improve bicycle allocation,
- optimize logistics,
- reduce shortages,
- and improve customer satisfaction.

---

# Forecasting Impact

The generated features improve:
- MAE performance,
- forecasting stability,
- seasonal learning,
- and operational prediction quality.

These features are especially useful for:
- XGBoost,
- Random Forest,
- and Gradient Boosting models.

---

# Pipeline Position

```text
load_data.py
        ↓
validate_data.py
        ↓
preprocess_data.py
        ↓
create_time_features.py
        ↓
encode_features.py
        ↓
scale_features.py
        ↓
model_training/
```

---

# Next Recommended Step

After generating time-based features:

```bash
python feature_engineering/encode_features.py
```

or continue with:
- feature scaling,
- model training,
- evaluation,
- and forecasting analysis.

---

# Summary

The `create_time_features.py` script is a core feature engineering component of the Bike Sharing Demand Forecasting pipeline. It generates advanced temporal, seasonal, and cyclical features that significantly improve forecasting accuracy and business planning capabilities for bicycle rental demand prediction.