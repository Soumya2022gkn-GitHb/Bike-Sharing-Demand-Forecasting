"""Data ingestion, validation, and preprocessing utilities."""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

from bsdf.config import ProjectConfig

LOGGER = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
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
    "casual",
    "registered",
    "cnt",
}


def download_dataset(config: ProjectConfig) -> Path:
    """Download and extract the UCI Bike Sharing Dataset if it is missing."""

    hour_csv = config.raw_dir / "hour.csv"
    if hour_csv.exists():
        LOGGER.info("Using existing dataset at %s", hour_csv)
        return hour_csv

    archive_path = config.raw_dir / "bike_sharing_dataset.zip"
    LOGGER.info("Downloading dataset from %s", config.dataset_url)
    urlretrieve(config.dataset_url, archive_path)

    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(config.raw_dir)

    if not hour_csv.exists():
        raise FileNotFoundError("Expected hour.csv after extracting the UCI archive.")
    return hour_csv


def load_hourly_data(config: ProjectConfig) -> pd.DataFrame:
    """Load the hourly data extract."""

    csv_path = download_dataset(config)
    return pd.read_csv(csv_path)


def validate_hourly_data(data: pd.DataFrame) -> None:
    """Validate schema and basic target quality before preprocessing."""

    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    if data.empty:
        raise ValueError("Hourly bike-sharing data is empty.")

    if data["cnt"].isna().any():
        raise ValueError("Target column cnt contains missing values.")

    if (data["cnt"] < 0).any():
        raise ValueError("Target column cnt contains negative values.")


def preprocess_hourly_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich raw hourly bike-sharing observations."""

    clean_data = data.copy()
    clean_data["dteday"] = pd.to_datetime(clean_data["dteday"], errors="raise")
    clean_data["timestamp"] = clean_data["dteday"] + pd.to_timedelta(clean_data["hr"], unit="h")
    clean_data = clean_data.sort_values("timestamp").reset_index(drop=True)

    numeric_columns = ["temp", "atemp", "hum", "windspeed"]
    clean_data[numeric_columns] = clean_data[numeric_columns].apply(pd.to_numeric, errors="coerce")
    clean_data[numeric_columns] = clean_data[numeric_columns].ffill().bfill()
    return clean_data


def ingest_data(config: ProjectConfig) -> pd.DataFrame:
    """Load, validate, preprocess, and persist the hourly dataset."""

    raw_data = load_hourly_data(config)
    validate_hourly_data(raw_data)
    clean_data = preprocess_hourly_data(raw_data)
    clean_data.to_csv(config.processed_dir / "hourly_clean.csv", index=False)
    return clean_data


def split_time_ordered_data(
    data: pd.DataFrame,
    test_fraction: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split observations chronologically to mimic future forecasting."""

    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1.")

    split_index = int(len(data) * (1 - test_fraction))
    train_data = data.iloc[:split_index].copy()
    test_data = data.iloc[split_index:].copy()
    return train_data, test_data


def load_processed_data(config: ProjectConfig) -> pd.DataFrame:
    """Load processed data, creating it first if needed."""

    processed_path = config.processed_dir / "hourly_clean.csv"
    if processed_path.exists():
        data = pd.read_csv(processed_path)
        data["dteday"] = pd.to_datetime(data["dteday"])
        data["timestamp"] = pd.to_datetime(data["timestamp"])
        return data
    return ingest_data(config)
