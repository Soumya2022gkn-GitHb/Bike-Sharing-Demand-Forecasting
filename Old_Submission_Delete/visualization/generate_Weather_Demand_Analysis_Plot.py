# =========================================================
# File: visualization/generate_Weather_Demand_Analysis_Plot.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

"""
Weather vs Demand Analysis Plot
---------------------------------------------------------

This script generates business-focused visualizations
to analyze how weather conditions impact bike rental
demand in the Bike Sharing Dataset.

Generated Plots:
1. Average Bike Demand by Weather Situation
2. Temperature vs Bike Demand
3. Humidity vs Bike Demand
4. Windspeed vs Bike Demand

The plots help stakeholders understand:

- Weather-sensitive demand fluctuations
- Operational demand planning
- Seasonal logistics management
- Rental risk during adverse weather

Author:
Bike_Sharing_Demand_Forecasting Team
"""

# =========================================================
# Imports
# =========================================================

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# =========================================================
# Project Paths
# =========================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "hour.csv"
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "reports"
    / "figures"
)

OUTPUT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# Plot Style Configuration
# =========================================================

sns.set_style("whitegrid")

plt.rcParams["figure.figsize"] = (12, 6)

plt.rcParams["axes.titlesize"] = 16

plt.rcParams["axes.labelsize"] = 13


# =========================================================
# Utility Functions
# =========================================================

def print_section(title: str) -> None:
    """
    Print formatted console section.
    """

    separator = "=" * 60

    print(f"\n{separator}")

    print(f" {title}")

    print(separator)


def validate_dataset() -> None:
    """
    Validate dataset existence.
    """

    if not DATA_PATH.exists():

        raise FileNotFoundError(

            f"""
Dataset not found.

Expected:
{DATA_PATH}
"""
        )


def load_dataset() -> pd.DataFrame:
    """
    Load bike sharing dataset.
    """

    validate_dataset()

    dataframe = pd.read_csv(DATA_PATH)

    return dataframe


# =========================================================
# Data Preparation
# =========================================================

def map_weather_labels(
    dataframe: pd.DataFrame
) -> pd.DataFrame:
    """
    Map weather situation labels.
    """

    dataframe = dataframe.copy()

    weather_mapping = {

        1: "Clear",

        2: "Mist / Cloudy",

        3: "Light Rain / Snow",

        4: "Heavy Rain / Storm"
    }

    dataframe["weather_label"] = (
        dataframe["weathersit"]
        .map(weather_mapping)
    )

    return dataframe


# =========================================================
# Plot Functions
# =========================================================

def plot_weather_vs_demand(
    dataframe: pd.DataFrame
) -> None:
    """
    Plot average bike demand by weather condition.
    """

    print_section(
        "Generating Weather vs Demand Plot"
    )

    plt.figure(figsize=(12, 6))

    average_demand = (

        dataframe
        .groupby("weather_label")["cnt"]
        .mean()
        .reset_index()
    )

    sns.barplot(

        data=average_demand,

        x="weather_label",

        y="cnt"
    )

    plt.title(
        "Average Bike Demand by Weather Condition"
    )

    plt.xlabel(
        "Weather Condition"
    )

    plt.ylabel(
        "Average Bike Rentals"
    )

    output_path = (
        OUTPUT_DIRECTORY
        / "weather_vs_demand.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"\nSaved:\n{output_path}"
    )


def plot_temperature_vs_demand(
    dataframe: pd.DataFrame
) -> None:
    """
    Plot temperature vs bike demand.
    """

    print_section(
        "Generating Temperature Analysis Plot"
    )

    plt.figure(figsize=(12, 6))

    sns.scatterplot(

        data=dataframe,

        x="temp",

        y="cnt",

        alpha=0.5
    )

    plt.title(
        "Temperature vs Bike Demand"
    )

    plt.xlabel(
        "Normalized Temperature"
    )

    plt.ylabel(
        "Bike Rental Count"
    )

    output_path = (
        OUTPUT_DIRECTORY
        / "temperature_vs_demand.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"\nSaved:\n{output_path}"
    )


def plot_humidity_vs_demand(
    dataframe: pd.DataFrame
) -> None:
    """
    Plot humidity vs bike demand.
    """

    print_section(
        "Generating Humidity Analysis Plot"
    )

    plt.figure(figsize=(12, 6))

    sns.scatterplot(

        data=dataframe,

        x="hum",

        y="cnt",

        alpha=0.5
    )

    plt.title(
        "Humidity vs Bike Demand"
    )

    plt.xlabel(
        "Humidity"
    )

    plt.ylabel(
        "Bike Rental Count"
    )

    output_path = (
        OUTPUT_DIRECTORY
        / "humidity_vs_demand.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"\nSaved:\n{output_path}"
    )


def plot_windspeed_vs_demand(
    dataframe: pd.DataFrame
) -> None:
    """
    Plot windspeed vs bike demand.
    """

    print_section(
        "Generating Windspeed Analysis Plot"
    )

    plt.figure(figsize=(12, 6))

    sns.scatterplot(

        data=dataframe,

        x="windspeed",

        y="cnt",

        alpha=0.5
    )

    plt.title(
        "Windspeed vs Bike Demand"
    )

    plt.xlabel(
        "Windspeed"
    )

    plt.ylabel(
        "Bike Rental Count"
    )

    output_path = (
        OUTPUT_DIRECTORY
        / "windspeed_vs_demand.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300
    )

    plt.close()

    print(
        f"\nSaved:\n{output_path}"
    )


# =========================================================
# Main Pipeline
# =========================================================

def run_weather_analysis_pipeline() -> None:
    """
    Execute complete weather-demand analysis pipeline.
    """

    print_section(
        "Bike Sharing Weather Demand Analysis"
    )

    dataframe = load_dataset()

    dataframe = map_weather_labels(
        dataframe
    )

    plot_weather_vs_demand(
        dataframe
    )

    plot_temperature_vs_demand(
        dataframe
    )

    plot_humidity_vs_demand(
        dataframe
    )

    plot_windspeed_vs_demand(
        dataframe
    )

    print_section(
        "Weather Demand Analysis Completed"
    )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":

    run_weather_analysis_pipeline()
