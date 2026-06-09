"""Shared persistence helpers."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


def save_model(model, output_path: Path) -> Path:
    """Persist a trained model pipeline."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path


def load_model(model_path: Path):
    """Load a trained model pipeline."""

    return joblib.load(model_path)


def save_table(data: pd.DataFrame, output_path: Path) -> Path:
    """Persist a table as CSV."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)
    return output_path

