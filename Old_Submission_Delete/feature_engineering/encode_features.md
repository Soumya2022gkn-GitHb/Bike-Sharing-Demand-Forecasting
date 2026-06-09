# encode_features.py

## Project

```text
Bike_Sharing_Demand_Forecasting
```

---

# Overview

The `encode_features.py` script is responsible for transforming categorical variables into machine-learning-compatible numerical representations for the Bike Sharing Demand Forecasting project.

Machine learning models such as:
- Linear Regression,
- Random Forest,
- and XGBoost

cannot directly process categorical text values like:

```text
Morning
Summer
Good
Weekend
```

This script converts those categorical features into numeric labels using:

```python
LabelEncoder
```

The encoded dataset becomes fully compatible with:
- feature scaling,
- machine learning model training,
- evaluation,
- and forecasting deployment.

The script follows production-quality engineering practices including:
- validation,
- exception handling,
- missing value management,
- encoding mapping generation,
- and maintainable modular structure.

---

# File Location

```text
Bike_Sharing_Demand_Forecasting/
│
├── feature_engineering/
│   └── encode_features.py
```

---

# Purpose

The purpose of this script is to:
- identify categorical features,
- encode them into numerical values,
- preserve encoding mappings,
- and prepare the forecasting dataset for machine learning pipelines.

This stage ensures forecasting models can learn efficiently from:
- seasonal labels,
- weather descriptions,
- hour groups,
- demand categories,
- and business-related categorical features.

---

# Input Dataset

The script expects:

```text
data/processed/time_feature_engineered_data.csv
```

Generated from:

```bash
python feature_engineering/create_time_features.py
```

---

# Output Dataset

The script generates:

```text
data/processed/encoded_feature_data.csv
```

Additional output:

```text
models/label_encoding_mappings.txt
```

---

# Workflow

```text
Time Feature Dataset
        ↓
Detect Categorical Columns
        ↓
Remove Non-Training Columns
        ↓
Apply Label Encoding
        ↓
Handle Missing Values
        ↓
Remove Infinite Values
        ↓
Validate Dataset
        ↓
Save Encoded Dataset
        ↓
Save Encoding Mappings
```

---

# Key Functionalities

---

# 1. Categorical Column Detection

The script automatically detects categorical features using:

```python
select_dtypes(include=["object", "category"])
```

Examples:
- month_name
- day_name
- hour_group
- weather_severity
- demand_category

---

# 2. Remove Non-Training Columns

Columns that should not be used for training are removed.

## Removed Columns

| Column | Reason |
|---|---|
| dteday | Raw datetime not directly usable |

This helps:
- reduce data leakage,
- simplify training,
- and improve model efficiency.

---

# 3. Label Encoding

The script uses:

```python
LabelEncoder()
```

to transform categorical values into integers.

## Example

| Original Value | Encoded Value |
|---|---|
| Morning | 2 |
| Evening | 1 |
| Night | 3 |

---

# 4. Missing Value Handling

Before encoding:
- missing categorical values are replaced with:
```text
Unknown
```

This prevents:
- encoding failures,
- inconsistent mappings,
- and model training issues.

---

# 5. Infinite Value Removal

The script safely removes:

```text
+∞
-∞
```

using:

```python
replace([np.inf, -np.inf], np.nan)
```

This ensures:
- stable scaling,
- clean training data,
- and reliable forecasting.

---

# 6. Duplicate Row Validation

The pipeline checks for duplicate rows and removes them automatically.

This prevents:
- biased learning,
- duplicated forecasting signals,
- and evaluation distortion.

---

# 7. Encoding Mapping Storage

The script saves label mappings into:

```text
models/label_encoding_mappings.txt
```

This is extremely important for:
- inference pipelines,
- production deployment,
- debugging,
- and teammate collaboration.

---

# Example Encoding Mapping

```text
Column: hour_group

Morning -> 2
Afternoon -> 0
Evening -> 1
Night -> 3
```

---

# Dataset Validation

The script validates:
- missing values,
- duplicate rows,
- dataset shape,
- and encoded feature quality.

This ensures the dataset is:
```text
production-ready
```

before scaling and model training.

---

# Production-Ready Design

The script follows production-quality software engineering principles.

## Maintainability
- modular sections,
- descriptive naming,
- readable formatting.

## Reliability
- safe exception handling,
- validation checks,
- encoding consistency.

## Scalability
- reusable encoding pipeline,
- future feature support.

## Collaboration Friendly
The encoding mappings allow teammates to:
- understand transformations,
- debug predictions,
- and maintain inference pipelines.

---

# Running the Script

From project root:

```bash
python feature_engineering/encode_features.py
```

---

# Example Console Output

```text
========================================
 Encoding Categorical Features
========================================

Categorical Columns:
['month_name', 'day_name', 'hour_group']

Encoded Column: month_name

Encoded Column: day_name

Encoded Column: hour_group

Dataset saved successfully.

Encoding mappings saved successfully.
```

---

# Business Importance

Encoding categorical variables helps forecasting models understand:
- commuting behavior,
- seasonal demand,
- weather conditions,
- and operational demand cycles.

Without encoding:
- ML models cannot process business categories,
- forecasting quality decreases,
- and deployment becomes unreliable.

This step improves:
- model learning,
- operational forecasting,
- and prediction consistency.

---

# Forecasting Impact

Proper encoding improves:
- feature representation,
- model training stability,
- forecasting accuracy,
- and operational planning performance.

These encoded features are especially useful for:
- Random Forest,
- XGBoost,
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

After encoding:

```bash
python feature_engineering/scale_features.py
```

or continue with:
- feature normalization,
- model training,
- evaluation,
- and forecasting visualization.

---

# Summary

The `encode_features.py` script converts categorical business and temporal features into machine-learning-compatible numerical representations. It ensures the Bike Sharing Demand Forecasting dataset is fully prepared for scalable, production-ready forecasting models while preserving maintainability, interpretability, and deployment reliability.