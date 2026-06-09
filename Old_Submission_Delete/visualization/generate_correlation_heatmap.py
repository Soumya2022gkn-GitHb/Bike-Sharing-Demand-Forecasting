# =========================================================
# File: visualization/generate_correlation_heatmap.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

"""
=========================================================
 Generate Correlation Heatmap
=========================================================

This script generates a correlation heatmap for the
Bike Sharing Dataset to identify relationships between
features and hourly bike rental demand.

Target Variable:
---------------------------------------------------------
cnt -> Hourly Bike Rental Demand

The generated heatmap helps:
---------------------------------------------------------
1. Identify important forecasting features
2. Detect multicollinearity
3. Analyze weather impact
4. Understand seasonal patterns
5. Support feature selection
6. Improve business forecasting insights

Output:
---------------------------------------------------------
graphs/correlation_heatmap.png

=========================================================
"""


# =========================================================
# Import Required Libraries
# =========================================================

from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


# =========================================================
# Configure Visualization Style
# =========================================================

plt.style.use("ggplot")
sns.set(font_scale=1.0)


# =========================================================
# Define Project Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "hour.csv"
)

GRAPH_PATH = (
    PROJECT_ROOT
    / "graphs"
)

GRAPH_PATH.mkdir(
    exist_ok=True
)


# =========================================================
# Display Section Header
# =========================================================

def print_header(title):
    """
    Display formatted console headers.
    """

    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


# =========================================================
# Load Dataset
# =========================================================

print_header(
    "Loading Bike Sharing Dataset"
)

try:

    df = pd.read_csv(DATA_PATH)

    print(
        f"\nDataset loaded successfully."
    )

    print(
        f"\nDataset Shape: {df.shape}"
    )

except FileNotFoundError:

    print(
        f"\nERROR: Dataset not found."
    )

    print(
        f"\nExpected Location:\n{DATA_PATH}"
    )

    raise

except Exception as error:

    print(
        f"\nUnexpected Error: {error}"
    )

    raise


# =========================================================
# Dataset Overview
# =========================================================

print_header(
    "Dataset Information"
)

print("\nColumns:")

for column in df.columns:

    print(f"- {column}")


# =========================================================
# Generate Correlation Matrix
# =========================================================

print_header(
    "Generating Correlation Matrix"
)

try:

    # =====================================================
    # Select Numeric Columns
    # =====================================================

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    # =====================================================
    # Compute Correlation Matrix
    # =====================================================

    correlation_matrix = numeric_df.corr()

    print(
        "\nCorrelation matrix generated successfully."
    )

except Exception as error:

    print(
        f"\nERROR while generating correlation matrix:"
    )

    print(error)

    raise


# =========================================================
# Create Heatmap Visualization
# =========================================================

print_header(
    "Creating Correlation Heatmap"
)

try:

    plt.figure(
        figsize=(18, 14)
    )

    sns.heatmap(

        correlation_matrix,

        annot=False,

        cmap="coolwarm",

        linewidths=0.5,

        square=False,

        cbar=True
    )

    plt.title(

        "Bike Sharing Dataset Correlation Heatmap",

        fontsize=20,

        fontweight="bold"
    )

    plt.xticks(

        rotation=45,

        ha="right"
    )

    plt.yticks(

        rotation=0
    )

    plt.tight_layout()

    print(
        "\nHeatmap created successfully."
    )

except Exception as error:

    print(
        f"\nERROR while creating heatmap:"
    )

    print(error)

    raise


# =========================================================
# Save Heatmap
# =========================================================

print_header(
    "Saving Correlation Heatmap"
)

try:

    output_file = (

        GRAPH_PATH
        / "correlation_heatmap.png"
    )

    plt.savefig(

        output_file,

        dpi=300,

        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nHeatmap saved successfully."
    )

    print(
        f"\nSaved Location:\n{output_file}"
    )

except Exception as error:

    print(
        f"\nERROR while saving heatmap:"
    )

    print(error)

    raise


# =========================================================
# Business Insights
# =========================================================

print_header(
    "Business Forecasting Insights"
)

print("""

Key observations from the correlation heatmap:

1. Temperature positively influences bike demand.

2. Weather conditions negatively impact rentals.

3. Humidity reduces hourly bike usage.

4. Seasonal patterns strongly affect demand.

5. Hourly demand shows strong temporal behavior.

6. Working days impact commuting demand patterns.

7. Feature correlations help improve forecasting models.

""")


# =========================================================
# Feature Importance Recommendations
# =========================================================

print_header(
    "Recommended Forecasting Features"
)

recommended_features = [

    "temp",
    "atemp",
    "hum",
    "windspeed",
    "season",
    "weathersit",
    "hr",
    "workingday",
    "holiday"
]

for feature in recommended_features:

    print(f"- {feature}")


# =========================================================
# Forecasting Recommendation
# =========================================================

print_header(
    "Operational Forecasting Recommendations"
)

recommendations = [

    "Refresh forecasts every 1-3 hours.",

    "Monitor weather-driven demand changes.",

    "Retrain forecasting models seasonally.",

    "Use short-term forecasting horizons.",

    "Track feature drift in production."
]

for recommendation in recommendations:

    print(f"- {recommendation}")


# =========================================================
# Completion Message
# =========================================================

print_header(
    "Correlation Heatmap Generation Completed"
)

print("""

The correlation heatmap was successfully generated.

Output File:
---------------------------------------------------------
graphs/correlation_heatmap.png

This visualization can now be used for:

- Exploratory Data Analysis (EDA)
- Business Presentations
- Forecasting Reports
- Feature Selection
- Model Analysis
- Streamlit Dashboard Visualization

""")


# =========================================================
# End of File
# =========================================================
