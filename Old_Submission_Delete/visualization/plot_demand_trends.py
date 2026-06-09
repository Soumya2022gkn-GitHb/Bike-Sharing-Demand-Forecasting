# =========================================================
# File: visualization/plot_demand_trends.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# Define Project Paths
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

PROJECT_ROOT = CURRENT_FILE.parent.parent

PROCESSED_DATA_DIR = (

    PROJECT_ROOT
    / "data"
    / "processed"
)

GRAPHS_DIR = (

    PROJECT_ROOT
    / "graphs"
)


# =========================================================
# Define File Paths
# =========================================================

FEATURE_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "feature_engineered_data.csv"
)

HOURLY_DEMAND_PLOT = (

    GRAPHS_DIR
    / "hourly_demand.png"
)

SEASONAL_TREND_PLOT = (

    GRAPHS_DIR
    / "seasonal_trends.png"
)

WEEKDAY_TREND_PLOT = (

    GRAPHS_DIR
    / "weekday_demand_trends.png"
)

MONTHLY_TREND_PLOT = (

    GRAPHS_DIR
    / "monthly_demand_trends.png"
)


# =========================================================
# Print Header
# =========================================================

print("\n========================================")
print(" Plotting Demand Trends ")
print("========================================")


# =========================================================
# Validate Dataset File
# =========================================================

print("\n========================================")
print(" Validating Dataset ")
print("========================================")

if not FEATURE_DATA_FILE.exists():

    print("\nERROR: Feature engineered dataset not found.")

    print("\nExpected File:")
    print(FEATURE_DATA_FILE)

    raise SystemExit

print("\nDataset Found:")
print(FEATURE_DATA_FILE)


# =========================================================
# Create Output Directory
# =========================================================

GRAPHS_DIR.mkdir(

    parents=True,

    exist_ok=True
)


# =========================================================
# Load Dataset
# =========================================================

print("\n========================================")
print(" Loading Dataset ")
print("========================================")

try:

    df = pd.read_csv(

        FEATURE_DATA_FILE
    )

    print("\nDataset loaded successfully.")

except Exception as error:

    print("\nERROR while loading dataset:")
    print(error)

    raise SystemExit


# =========================================================
# Dataset Information
# =========================================================

print("\n========================================")
print(" Dataset Information ")
print("========================================")

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# =========================================================
# Validate Required Columns
# =========================================================

required_columns = [

    "hr",

    "cnt",

    "season",

    "weekday",

    "mnth"
]

missing_columns = [

    column
    for column in required_columns
    if column not in df.columns
]

if len(missing_columns) > 0:

    print("\nERROR: Missing required columns.")

    print(missing_columns)

    raise SystemExit


# =========================================================
# Plot Hourly Demand Trend
# =========================================================

print("\n========================================")
print(" Plotting Hourly Demand Trend ")
print("========================================")

try:

    hourly_demand = (

        df.groupby("hr")["cnt"]

        .mean()
    )

    plt.figure(

        figsize=(12, 6)
    )

    plt.plot(

        hourly_demand.index,

        hourly_demand.values,

        marker="o"
    )

    plt.title(

        "Average Hourly Bike Demand"
    )

    plt.xlabel(

        "Hour of Day"
    )

    plt.ylabel(

        "Average Bike Demand"
    )

    plt.xticks(

        range(0, 24)
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(

        HOURLY_DEMAND_PLOT
    )

    plt.close()

    print("\nHourly demand plot saved.")

    print("\nSaved File:")
    print(HOURLY_DEMAND_PLOT)

except Exception as error:

    print("\nERROR while plotting hourly demand:")
    print(error)


# =========================================================
# Plot Seasonal Demand Trend
# =========================================================

print("\n========================================")
print(" Plotting Seasonal Demand Trend ")
print("========================================")

try:

    seasonal_demand = (

        df.groupby("season")["cnt"]

        .mean()
    )

    season_labels = {

        1: "Spring",

        2: "Summer",

        3: "Fall",

        4: "Winter"
    }

    seasonal_demand.index = [

        season_labels.get(

            season,

            season
        )

        for season in seasonal_demand.index
    ]

    plt.figure(

        figsize=(10, 6)
    )

    plt.bar(

        seasonal_demand.index,

        seasonal_demand.values
    )

    plt.title(

        "Average Seasonal Bike Demand"
    )

    plt.xlabel(

        "Season"
    )

    plt.ylabel(

        "Average Bike Demand"
    )

    plt.tight_layout()

    plt.savefig(

        SEASONAL_TREND_PLOT
    )

    plt.close()

    print("\nSeasonal trend plot saved.")

    print("\nSaved File:")
    print(SEASONAL_TREND_PLOT)

except Exception as error:

    print("\nERROR while plotting seasonal trends:")
    print(error)


# =========================================================
# Plot Weekday Demand Trend
# =========================================================

print("\n========================================")
print(" Plotting Weekday Demand Trend ")
print("========================================")

try:

    weekday_demand = (

        df.groupby("weekday")["cnt"]

        .mean()
    )

    weekday_labels = {

        0: "Sunday",

        1: "Monday",

        2: "Tuesday",

        3: "Wednesday",

        4: "Thursday",

        5: "Friday",

        6: "Saturday"
    }

    weekday_demand.index = [

        weekday_labels.get(

            day,

            day
        )

        for day in weekday_demand.index
    ]

    plt.figure(

        figsize=(12, 6)
    )

    plt.plot(

        weekday_demand.index,

        weekday_demand.values,

        marker="o"
    )

    plt.title(

        "Average Weekday Bike Demand"
    )

    plt.xlabel(

        "Weekday"
    )

    plt.ylabel(

        "Average Bike Demand"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(

        WEEKDAY_TREND_PLOT
    )

    plt.close()

    print("\nWeekday trend plot saved.")

    print("\nSaved File:")
    print(WEEKDAY_TREND_PLOT)

except Exception as error:

    print("\nERROR while plotting weekday trends:")
    print(error)


# =========================================================
# Plot Monthly Demand Trend
# =========================================================

print("\n========================================")
print(" Plotting Monthly Demand Trend ")
print("========================================")

try:

    monthly_demand = (

        df.groupby("mnth")["cnt"]

        .mean()
    )

    month_labels = {

        1: "Jan",

        2: "Feb",

        3: "Mar",

        4: "Apr",

        5: "May",

        6: "Jun",

        7: "Jul",

        8: "Aug",

        9: "Sep",

        10: "Oct",

        11: "Nov",

        12: "Dec"
    }

    monthly_demand.index = [

        month_labels.get(

            month,

            month
        )

        for month in monthly_demand.index
    ]

    plt.figure(

        figsize=(12, 6)
    )

    plt.plot(

        monthly_demand.index,

        monthly_demand.values,

        marker="o"
    )

    plt.title(

        "Average Monthly Bike Demand"
    )

    plt.xlabel(

        "Month"
    )

    plt.ylabel(

        "Average Bike Demand"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(

        MONTHLY_TREND_PLOT
    )

    plt.close()

    print("\nMonthly trend plot saved.")

    print("\nSaved File:")
    print(MONTHLY_TREND_PLOT)

except Exception as error:

    print("\nERROR while plotting monthly trends:")
    print(error)


# =========================================================
# Business Insights
# =========================================================

print("\n========================================")
print(" Business Insights ")
print("========================================")

print("\nKey Demand Observations:")

print("- Peak demand occurs during commuting hours.")

print("- Summer and Fall show higher bike demand.")

print("- Weekday demand is higher than weekends.")

print("- Seasonal trends strongly influence rentals.")

print("- Demand forecasting helps optimize logistics.")


# =========================================================
# Production Recommendations
# =========================================================

print("\n========================================")
print(" Operational Recommendations ")
print("========================================")

print("\nRecommended Actions:")

print("- Refresh forecasts every 1-3 hours.")

print("- Increase bicycle inventory during peak seasons.")

print("- Allocate more bicycles during rush hours.")

print("- Monitor weather-driven demand changes.")

print("- Use short-term forecasts for daily planning.")


# =========================================================
# Generated Graph Summary
# =========================================================

print("\n========================================")
print(" Generated Visualization Files ")
print("========================================")

print(f"\n- {HOURLY_DEMAND_PLOT}")

print(f"- {SEASONAL_TREND_PLOT}")

print(f"- {WEEKDAY_TREND_PLOT}")

print(f"- {MONTHLY_TREND_PLOT}")


# =========================================================
# Completion Message
# =========================================================

print("\n========================================")
print(" Demand Trend Visualization Completed ")
print("========================================")
