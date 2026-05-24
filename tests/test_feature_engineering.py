# =========================================================
# File: tests/test_feature_engineering.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

import unittest
from pathlib import Path

import pandas as pd
import numpy as np


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

MODELS_DIR = (

    PROJECT_ROOT
    / "models"
)


# =========================================================
# Define File Paths
# =========================================================

FEATURE_ENGINEERED_FILE = (

    PROCESSED_DATA_DIR
    / "feature_engineered_data.csv"
)

TRAIN_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

TEST_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)

SCALER_FILE = (

    MODELS_DIR
    / "scaler.pkl"
)


# =========================================================
# Test Class
# =========================================================

class TestFeatureEngineering(unittest.TestCase):

    # =====================================================
    # Setup Test Environment
    # =====================================================

    @classmethod
    def setUpClass(cls):

        print("\n========================================")
        print(" Setting Up Feature Engineering Tests ")
        print("========================================")

        cls.feature_df = pd.read_csv(

            FEATURE_ENGINEERED_FILE
        )

        cls.train_df = pd.read_csv(

            TRAIN_DATA_FILE
        )

        cls.test_df = pd.read_csv(

            TEST_DATA_FILE
        )

    # =====================================================
    # Test Required Files
    # =====================================================

    def test_feature_files_exist(self):
        """
        Verify feature engineering files exist.
        """

        print("\nChecking feature files...")

        required_files = [

            FEATURE_ENGINEERED_FILE,

            TRAIN_DATA_FILE,

            TEST_DATA_FILE
        ]

        for file in required_files:

            self.assertTrue(

                file.exists(),

                f"Missing required file: {file.name}"
            )

    # =====================================================
    # Test Feature Engineered Dataset
    # =====================================================

    def test_feature_engineered_dataset(self):
        """
        Validate feature engineered dataset.
        """

        print("\nValidating feature engineered dataset...")

        self.assertFalse(

            self.feature_df.empty,

            "Feature engineered dataset is empty."
        )

        required_features = [

            "is_weekend",

            "is_peak_hour",

            "season_label",

            "weather_label",

            "demand_category"
        ]

        dataset_columns = [

            column.lower()
            for column in self.feature_df.columns
        ]

        for feature in required_features:

            self.assertIn(

                feature.lower(),

                dataset_columns,

                f"Missing engineered feature: {feature}"
            )

    # =====================================================
    # Test Time Features
    # =====================================================

    def test_time_features(self):
        """
        Validate time-based features.
        """

        print("\nChecking time features...")

        required_columns = [

            "hr",

            "weekday",

            "mnth",

            "season"
        ]

        dataset_columns = [

            column.lower()
            for column in self.feature_df.columns
        ]

        for column in required_columns:

            self.assertIn(

                column.lower(),

                dataset_columns,

                f"Missing time feature: {column}"
            )

    # =====================================================
    # Test Weather Features
    # =====================================================

    def test_weather_features(self):
        """
        Validate weather-related features.
        """

        print("\nChecking weather features...")

        required_columns = [

            "temp",

            "atemp",

            "hum",

            "windspeed"
        ]

        dataset_columns = [

            column.lower()
            for column in self.feature_df.columns
        ]

        for column in required_columns:

            self.assertIn(

                column.lower(),

                dataset_columns,

                f"Missing weather feature: {column}"
            )

    # =====================================================
    # Test Missing Values
    # =====================================================

    def test_missing_values(self):
        """
        Verify feature datasets contain no missing values.
        """

        print("\nChecking missing values...")

        datasets = {

            "feature_df": self.feature_df,

            "train_df": self.train_df,

            "test_df": self.test_df
        }

        for dataset_name, dataset in datasets.items():

            missing_values = dataset.isnull().sum().sum()

            self.assertEqual(

                missing_values,

                0,

                f"Missing values found in {dataset_name}"
            )

    # =====================================================
    # Test Infinite Values
    # =====================================================

    def test_infinite_values(self):
        """
        Verify datasets contain no infinite values.
        """

        print("\nChecking infinite values...")

        datasets = {

            "feature_df": self.feature_df,

            "train_df": self.train_df,

            "test_df": self.test_df
        }

        for dataset_name, dataset in datasets.items():

            numeric_dataset = dataset.select_dtypes(

                include=[np.number]
            )

            infinite_values = np.isinf(

                numeric_dataset
            ).sum().sum()

            self.assertEqual(

                infinite_values,

                0,

                f"Infinite values found in {dataset_name}"
            )

    # =====================================================
    # Test Target Column
    # =====================================================

    def test_target_column(self):
        """
        Verify target column exists.
        """

        print("\nChecking target column...")

        target_column = "cnt"

        train_columns = [

            column.lower()
            for column in self.train_df.columns
        ]

        test_columns = [

            column.lower()
            for column in self.test_df.columns
        ]

        self.assertIn(

            target_column,

            train_columns,

            "Target column missing in train dataset."
        )

        self.assertIn(

            target_column,

            test_columns,

            "Target column missing in test dataset."
        )

    # =====================================================
    # Test Target Values
    # =====================================================

    def test_target_values(self):
        """
        Verify target values are valid.
        """

        print("\nChecking target values...")

        self.assertTrue(

            (self.train_df["cnt"] >= 0).all(),

            "Negative target values found in train dataset."
        )

        self.assertTrue(

            (self.test_df["cnt"] >= 0).all(),

            "Negative target values found in test dataset."
        )

    # =====================================================
    # Test Train-Test Consistency
    # =====================================================

    def test_train_test_consistency(self):
        """
        Verify train and test datasets match.
        """

        print("\nChecking train-test consistency...")

        train_columns = set(

            self.train_df.columns
        )

        test_columns = set(

            self.test_df.columns
        )

        self.assertEqual(

            train_columns,

            test_columns,

            "Train and test columns do not match."
        )

    # =====================================================
    # Test Peak Hour Feature
    # =====================================================

    def test_peak_hour_feature(self):
        """
        Validate peak-hour feature values.
        """

        print("\nChecking peak-hour feature...")

        if "is_peak_hour" in self.feature_df.columns:

            unique_values = set(

                self.feature_df["is_peak_hour"].unique()
            )

            valid_values = {

                0,

                1,

                True,

                False
            }

            self.assertTrue(

                unique_values.issubset(valid_values),

                "Invalid values found in is_peak_hour."
            )

    # =====================================================
    # Test Weekend Feature
    # =====================================================

    def test_weekend_feature(self):
        """
        Validate weekend feature values.
        """

        print("\nChecking weekend feature...")

        if "is_weekend" in self.feature_df.columns:

            unique_values = set(

                self.feature_df["is_weekend"].unique()
            )

            valid_values = {

                0,

                1,

                True,

                False
            }

            self.assertTrue(

                unique_values.issubset(valid_values),

                "Invalid values found in is_weekend."
            )

    # =====================================================
    # Test Dataset Shape
    # =====================================================

    def test_dataset_shape(self):
        """
        Verify feature dataset dimensions.
        """

        print("\nChecking dataset shape...")

        self.assertGreater(

            self.feature_df.shape[0],

            100,

            "Feature dataset contains too few rows."
        )

        self.assertGreater(

            self.feature_df.shape[1],

            20,

            "Feature dataset contains too few columns."
        )

    # =====================================================
    # Test Feature Variability
    # =====================================================

    def test_feature_variability(self):
        """
        Verify numerical features contain variability.
        """

        print("\nChecking feature variability...")

        numeric_columns = self.feature_df.select_dtypes(

            include=[np.number]
        ).columns

        for column in numeric_columns:

            unique_values = self.feature_df[column].nunique()

            self.assertGreater(

                unique_values,

                1,

                f"No variability found in feature: {column}"
            )

    # =====================================================
    # Test Scaler File
    # =====================================================

    def test_scaler_file_exists(self):
        """
        Verify scaler file exists.
        """

        print("\nChecking scaler file...")

        self.assertTrue(

            SCALER_FILE.exists(),

            "Scaler file not found."
        )


# =========================================================
# Run Unit Tests
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" Running Feature Engineering Tests ")
    print("========================================")

    unittest.main(

        verbosity=2
    )
