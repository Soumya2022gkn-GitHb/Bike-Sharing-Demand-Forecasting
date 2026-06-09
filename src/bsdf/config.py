"""Project configuration for the bike-sharing forecasting workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """Centralized file paths and modeling defaults."""

    project_root: Path
    dataset_url: str = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"
    random_state: int = 42
    test_fraction: float = 0.20

    @property
    def raw_dir(self) -> Path:
        return self.project_root / "data" / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.project_root / "data" / "processed"

    @property
    def model_dir(self) -> Path:
        return self.project_root / "models"

    @property
    def figure_dir(self) -> Path:
        return self.project_root / "reports" / "figures"


def find_project_root(start: Path | None = None) -> Path:
    """Find the repository root from a notebook, script, or test path."""

    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "data").exists() and (candidate / "src").exists():
            return candidate
    return current


def get_config(start: Path | None = None) -> ProjectConfig:
    """Build the default project configuration."""

    config = ProjectConfig(project_root=find_project_root(start))
    for directory in [config.raw_dir, config.processed_dir, config.model_dir, config.figure_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    return config

