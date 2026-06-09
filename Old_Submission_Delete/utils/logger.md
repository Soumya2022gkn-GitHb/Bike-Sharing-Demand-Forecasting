# logger.py

## Project

```text
Bike_Sharing_Demand_Forecasting
```

---

# Overview

The `logger.py` file provides centralized logging functionality for the Bike Sharing Demand Forecasting project.

This module handles:
- pipeline logging,
- forecasting logs,
- error tracking,
- operational monitoring,
- debugging,
- deployment diagnostics,
- and production-grade logging management.

The goal is to improve:
```text
system observability, debugging, monitoring, and production reliability
```

This logger module supports:
- data ingestion,
- feature engineering,
- model training,
- evaluation,
- inference,
- and deployment pipelines.

---

# File Location

```text
Bike_Sharing_Demand_Forecasting/
│
├── utils/
│   └── logger.py
```

---

# Purpose

The purpose of this file is to:
- create centralized application logs,
- simplify debugging,
- track forecasting workflows,
- and support production-grade ML operations.

This module supports:
- operational monitoring,
- CI/CD systems,
- deployment diagnostics,
- and forecasting reliability.

---

# Workflow

```text
Initialize Logger
        ↓
Create Log File
        ↓
Attach Console Handler
        ↓
Attach File Handler
        ↓
Track Pipeline Events
        ↓
Track Forecast Metrics
        ↓
Track Predictions
        ↓
Track Exceptions
        ↓
Store Logs for Monitoring
```

---

# Key Functionalities

---

# 1. Log Directory Creation

## Functionality

Automatically creates:

```text
logs/
```

directory if it does not exist.

---

# Why It Matters

Automatic log directory creation:
- prevents runtime errors,
- simplifies deployment,
- and improves operational automation.

---

# 2. Timestamp-Based Log Files

## Functionality

Generates unique log file names using timestamps.

Example:

```text
bike_forecasting_2026-01-20_14-35-12.log
```

---

# Why It Matters

Timestamp-based logging supports:
- historical monitoring,
- debugging,
- audit tracking,
- and experiment traceability.

---

# 3. Rotating Log File Management

## Functionality

Uses:

```python
RotatingFileHandler
```

to manage log file size.

---

# Configuration

| Setting | Value |
|---|---|
| Max File Size | 5 MB |
| Backup Count | 5 |
| Encoding | UTF-8 |

---

# Why It Matters

Rotating logs:
- prevent oversized files,
- reduce storage issues,
- and improve production stability.

---

# 4. Console Logging

## Functionality

Displays logs directly in the terminal.

---

# Why It Matters

Improves:
- debugging,
- real-time monitoring,
- and operational visibility.

---

# 5. Log Formatting

## Functionality

Logs include:
- timestamp,
- log level,
- filename,
- function name,
- line number,
- and message.

---

# Example Log

```text
2026-01-20 14:35:12 | INFO | train_xgboost.py |
train_model | Line:120 | Model training completed.
```

---

# Why Structured Logging Matters

Structured logs improve:
- debugging,
- deployment diagnostics,
- and operational monitoring.

---

# 6. Duplicate Handler Prevention

## Functionality

Prevents duplicate logging handlers.

---

# Why It Matters

Avoids:
- repeated log entries,
- noisy logs,
- and monitoring confusion.

---

# 7. Informational Logging

## Function

```python
log_info()
```

---

# Purpose

Logs informational events.

Example:
- pipeline start,
- dataset loading,
- successful preprocessing.

---

# Why It Matters

Tracks:
- pipeline progress,
- forecasting workflow status,
- and operational health.

---

# 8. Warning Logging

## Function

```python
log_warning()
```

---

# Purpose

Logs non-critical warnings.

Example:
- missing optional columns,
- partial preprocessing issues,
- or unstable forecast segments.

---

# Why It Matters

Warnings help detect:
- early operational risks,
- data quality concerns,
- and deployment anomalies.

---

# 9. Error Logging

## Function

```python
log_error()
```

---

# Purpose

Logs operational errors.

Example:
- model failures,
- dataset loading failures,
- preprocessing errors.

---

# Why It Matters

Error logging improves:
- debugging efficiency,
- deployment reliability,
- and production monitoring.

---

# 10. Critical Logging

## Function

```python
log_critical()
```

---

# Purpose

Logs severe operational failures.

Example:
- forecasting system crash,
- corrupted model files,
- deployment failure.

---

# Why It Matters

Critical logs help trigger:
- operational alerts,
- monitoring systems,
- and rapid incident response.

---

# 11. Debug Logging

## Function

```python
log_debug()
```

---

# Purpose

Logs debugging information for developers.

---

# Why It Matters

Supports:
- debugging,
- development testing,
- and pipeline troubleshooting.

---

# 12. Pipeline Start Logging

## Function

```python
log_pipeline_start()
```

---

# Purpose

Tracks pipeline execution start.

Example:

```text
Starting Pipeline: Bike Demand Forecasting
```

---

# Why It Matters

Helps monitor:
- forecasting execution,
- deployment timing,
- and operational workflows.

---

# 13. Pipeline Completion Logging

## Function

```python
log_pipeline_end()
```

---

# Purpose

Tracks pipeline completion.

---

# Why It Matters

Supports:
- operational monitoring,
- workflow validation,
- and execution tracking.

---

# 14. Dataset Information Logging

## Function

```python
log_dataset_info()
```

---

# Purpose

Logs:
- dataset shape,
- columns,
- and missing values.

---

# Why It Matters

Supports:
- exploratory analysis,
- debugging,
- and data quality validation.

---

# 15. Forecast Metric Logging

## Function

```python
log_regression_metrics()
```

---

# Logged Metrics

| Metric | Description |
|---|---|
| MAE | Mean Absolute Error |
| RMSE | Root Mean Squared Error |
| R² | Variance Explained |

---

# MAE Formula

:contentReference[oaicite:0]{index=0}

Measures:
```text
average forecasting error
```

---

# RMSE Formula

:contentReference[oaicite:1]{index=1}

Measures:
```text
forecasting stability
```

---

# R² Formula

:contentReference[oaicite:2]{index=2}

Measures:
```text
model explanatory power
```

---

# Why Metric Logging Matters

Metrics help monitor:
- forecasting quality,
- operational reliability,
- and production performance.

---

# 16. Model Saving Logs

## Function

```python
log_model_saved()
```

---

# Purpose

Tracks saved forecasting models.

---

# Why It Matters

Supports:
- deployment traceability,
- model versioning,
- and operational auditing.

---

# 17. Dataset Saving Logs

## Function

```python
log_dataset_saved()
```

---

# Purpose

Tracks saved datasets.

---

# Why It Matters

Improves:
- reproducibility,
- auditability,
- and pipeline monitoring.

---

# 18. Prediction Summary Logging

## Function

```python
log_prediction_summary()
```

---

# Purpose

Logs:
- prediction count,
- average demand,
- minimum demand,
- maximum demand.

---

# Why It Matters

Supports:
- operational forecasting monitoring,
- anomaly detection,
- and deployment validation.

---

# 19. Exception Logging

## Function

```python
log_exception()
```

---

# Purpose

Captures complete exception traces.

---

# Why It Matters

Improves:
- debugging,
- production monitoring,
- and incident analysis.

---

# 20. Operational Recommendation Logging

## Function

```python
log_operational_recommendations()
```

---

# Purpose

Logs deployment recommendations.

Examples:
- forecast refresh intervals,
- retraining frequency,
- demand monitoring.

---

# Why It Matters

Supports:
- operational forecasting planning,
- deployment optimization,
- and stakeholder communication.

---

# 21. Business Insight Logging

## Function

```python
log_business_insights()
```

---

# Purpose

Logs business forecasting insights.

Examples:
- peak-hour demand behavior,
- weather impact,
- seasonality trends.

---

# Why It Matters

Supports:
- business reporting,
- operational planning,
- and executive presentations.

---

# 22. System Information Logging

## Function

```python
log_system_info()
```

---

# Purpose

Logs:
- operating system,
- OS version,
- Python version.

---

# Why It Matters

Supports:
- deployment debugging,
- environment tracking,
- and operational diagnostics.

---

# 23. Example Logger Execution

## Functionality

The module includes a runnable test example.

Run:

```bash
python utils/logger.py
```

---

# Example Output

```text
============================================================
Starting Pipeline: Bike Demand Forecasting
============================================================

INFO | Logger initialized successfully.

WARNING | This is a sample warning.

ERROR | This is a sample error.
```

---

# Logging Importance in Production ML Systems

Logging is critical for:
- monitoring forecasting systems,
- debugging deployment failures,
- detecting operational issues,
- and maintaining ML pipelines.

---

# Why Logging Matters

Without logging:
- debugging becomes difficult,
- forecasting failures become invisible,
- and operational monitoring weakens.

Logging enables:
```text
production-grade observability and operational reliability
```

---

# Production-Ready Design

The logger module follows production-quality engineering principles.

---

# Maintainability

The code is:
- modular,
- reusable,
- readable,
- and scalable.

---

# Reliability

The module includes:
- exception-safe logging,
- rotating log management,
- and operational safeguards.

---

# Scalability

The logger system supports:
- larger forecasting systems,
- deployment expansion,
- cloud monitoring,
- and CI/CD integration.

---

# Collaboration Friendly

The logging framework enables teammates to:
- debug forecasting systems,
- monitor deployments,
- track operational performance,
- and maintain production pipelines.

---

# Operational Forecasting Importance

The logger module supports:
- forecasting monitoring,
- operational reliability,
- deployment diagnostics,
- and business forecasting stability.

This directly improves:
```text
production-grade bike demand forecasting systems
```

---

# Pipeline Position

```text
utils/logger.py
        ↓
data_ingestion/
        ↓
feature_engineering/
        ↓
model_training/
        ↓
evaluation/
        ↓
deployment/
```

---

# Example Usage

## Import Logger

```python
from utils.logger import log_info
```

---

## Log Information

```python
log_info("Dataset loaded successfully.")
```

---

## Log Errors

```python
log_error("Model training failed.")
```

---

## Log Metrics

```python
log_regression_metrics(metrics)
```

---

# Summary

The `logger.py` module provides centralized logging functionality for the Bike Sharing Demand Forecasting project. It supports operational monitoring, forecasting diagnostics, error tracking, deployment logging, prediction monitoring, and production-grade observability. The module improves debugging efficiency, deployment reliability, maintainability, and operational forecasting stability across the complete machine learning pipeline.