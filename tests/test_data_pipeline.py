# =========================================================
# File: tests/test_data_pipeline.py
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

RAW_DATA_DIR = (

    PROJECT_ROOT
    / "data"
    / "raw"
)

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

RAW_DATA_FILE = (

    RAW_DATA_DIR
    / "hour.csv"
)

CLEANED_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "cleaned_bike_data.csv"
)

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

class TestDataPipeline(unittest.TestCase):

    # =====================================================
    # Setup Test Environment
    # =====================================================

    @classmethod
    def setUpClass(cls):

        print("\n========================================")
        print(" Setting Up Data Pipeline Tests ")
        print("========================================")

        cls.raw_df = pd.read_csv(

            RAW_DATA_FILE
        )

        cls.cleaned_df = pd.read_csv(

            CLEANED_DATA_FILE
        )

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
    # Test File Existence
    # =====================================================

    def test_required_files_exist(self):
        """
        Verify all required files exist.
        """

        print("\nChecking required files...")

        required_files = [

            RAW_DATA_FILE,

            CLEANED_DATA_FILE,

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
    # Test Raw Dataset
    # =====================================================

    def test_raw_dataset(self):
        """
        Validate raw dataset.
        """

        print("\nValidating raw dataset...")

        self.assertFalse(

            self.raw_df.empty,

            "Raw dataset is empty."
        )

        required_columns = [

            "instant",

            "dteday",

            "season",

            "yr",

            "mnth",

            "hr",

            "temp",

            "hum",

            "windspeed",

            "cnt"
        ]

        dataset_columns = [

            column.lower()
            for column in self.raw_df.columns
        ]

        for column in required_columns:

            self.assertIn(

                column,

                dataset_columns,

                f"Missing raw dataset column: {column}"
            )

    # =====================================================
    # Test Cleaned Dataset
    # =====================================================

    def test_cleaned_dataset(self):
        """
        Validate cleaned dataset.
        """

        print("\nValidating cleaned dataset...")

        self.assertFalse(

            self.cleaned_df.empty,

            "Cleaned dataset is empty."
        )

        self.assertGreater(

            len(self.cleaned_df.columns),

            10,

            "Insufficient columns in cleaned dataset."
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

        expected_features = [

            "is_weekend",

            "is_peak_hour",

            "season_label",

            "weather_label"
        ]

        dataset_columns = [

            column.lower()
            for column in self.feature_df.columns
        ]

        for feature in expected_features:

            self.assertIn(

                feature.lower(),

                dataset_columns,

                f"Missing feature engineered column: {feature}"
            )

    # =====================================================
    # Test Missing Values
    # =====================================================

    def test_missing_values(self):
        """
        Verify datasets contain no missing values.
        """

        print("\nChecking missing values...")

        datasets = {

            "cleaned_df": self.cleaned_df,

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

            "cleaned_df": self.cleaned_df,

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
    # Test Train-Test Split
    # =====================================================

    def test_train_test_split(self):
        """
        Validate train-test datasets.
        """

        print("\nChecking train-test split...")

        self.assertGreater(

            len(self.train_df),

            len(self.test_df),

            "Train dataset should be larger than test dataset."
        )

        self.assertGreater(

            len(self.test_df),

            0,

            "Test dataset is empty."
        )

    # =====================================================
    # Test Dataset Consistency
    # =====================================================

    def test_dataset_consistency(self):
        """
        Verify train and test columns match.
        """

        print("\nChecking dataset consistency...")

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
    # Test Scaler File
    # =====================================================

    def test_scaler_file(self):
        """
        Verify scaler model exists.
        """

        print("\nChecking scaler file...")

        self.assertTrue(

            SCALER_FILE.exists(),

            "Scaler file not found."
        )

    # =====================================================
    # Test Dataset Shape
    # =====================================================

    def test_dataset_shape(self):
        """
        Verify dataset dimensions are valid.
        """

        print("\nChecking dataset shapes...")

        self.assertGreater(

            self.train_df.shape[0],

            100,

            "Train dataset contains too few records."
        )

        self.assertGreater(

            self.feature_df.shape[1],

            15,

            "Feature engineered dataset contains too few columns."
        )

    # =====================================================
    # Test Target Value Validity
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


# =========================================================
# Run Unit Tests
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" Running Data Pipeline Tests ")
    print("========================================")

    unittest.main(

        verbosity=2
    )
