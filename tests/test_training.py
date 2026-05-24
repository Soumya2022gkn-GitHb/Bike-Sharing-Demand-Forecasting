# =========================================================
# File: tests/test_training.py
# Project: Bike_Sharing_Demand_Forecasting
# =========================================================

import unittest
from pathlib import Path

import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import (

    mean_absolute_error,

    mean_squared_error,

    r2_score
)


# =========================================================
# Check XGBoost Installation
# =========================================================

try:

    from xgboost import XGBRegressor

except ImportError:

    print("\n========================================")
    print(" XGBoost Not Installed ")
    print("========================================")

    print("\nInstall xgboost using:\n")

    print("pip install xgboost")

    raise SystemExit


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

TRAIN_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

TEST_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)

LINEAR_MODEL_FILE = (

    MODELS_DIR
    / "linear_regression_model.pkl"
)

RANDOM_FOREST_MODEL_FILE = (

    MODELS_DIR
    / "random_forest_model.pkl"
)

XGBOOST_MODEL_FILE = (

    MODELS_DIR
    / "xgboost_model.pkl"
)

SCALER_FILE = (

    MODELS_DIR
    / "scaler.pkl"
)


# =========================================================
# Test Class
# =========================================================

class TestTrainingPipeline(unittest.TestCase):

    # =====================================================
    # Setup Test Environment
    # =====================================================

    @classmethod
    def setUpClass(cls):

        print("\n========================================")
        print(" Setting Up Training Tests ")
        print("========================================")

        cls.train_df = pd.read_csv(

            TRAIN_DATA_FILE
        )

        cls.test_df = pd.read_csv(

            TEST_DATA_FILE
        )

        cls.target_column = "cnt"

        cls.X_test = cls.test_df.drop(

            columns=[cls.target_column]
        )

        cls.y_test = cls.test_df[

            cls.target_column
        ]

    # =====================================================
    # Test Model Files
    # =====================================================

    def test_model_files_exist(self):
        """
        Verify trained model files exist.
        """

        print("\nChecking trained model files...")

        required_files = [

            LINEAR_MODEL_FILE,

            RANDOM_FOREST_MODEL_FILE,

            XGBOOST_MODEL_FILE,

            SCALER_FILE
        ]

        for file in required_files:

            self.assertTrue(

                file.exists(),

                f"Missing model file: {file.name}"
            )

    # =====================================================
    # Test Dataset Availability
    # =====================================================

    def test_training_datasets_exist(self):
        """
        Verify training datasets exist.
        """

        print("\nChecking training datasets...")

        required_files = [

            TRAIN_DATA_FILE,

            TEST_DATA_FILE
        ]

        for file in required_files:

            self.assertTrue(

                file.exists(),

                f"Missing dataset file: {file.name}"
            )

    # =====================================================
    # Test Target Column
    # =====================================================

    def test_target_column_exists(self):
        """
        Verify target column exists.
        """

        print("\nChecking target column...")

        train_columns = [

            column.lower()
            for column in self.train_df.columns
        ]

        test_columns = [

            column.lower()
            for column in self.test_df.columns
        ]

        self.assertIn(

            self.target_column,

            train_columns,

            "Target column missing in train dataset."
        )

        self.assertIn(

            self.target_column,

            test_columns,

            "Target column missing in test dataset."
        )

    # =====================================================
    # Test Linear Regression Model
    # =====================================================

    def test_linear_regression_model(self):
        """
        Validate Linear Regression model.
        """

        print("\nTesting Linear Regression model...")

        model = joblib.load(

            LINEAR_MODEL_FILE
        )

        predictions = model.predict(

            self.X_test
        )

        mae = mean_absolute_error(

            self.y_test,

            predictions
        )

        self.assertLess(

            mae,

            150,

            "Linear Regression MAE too high."
        )

    # =====================================================
    # Test Random Forest Model
    # =====================================================

    def test_random_forest_model(self):
        """
        Validate Random Forest model.
        """

        print("\nTesting Random Forest model...")

        model = joblib.load(

            RANDOM_FOREST_MODEL_FILE
        )

        predictions = model.predict(

            self.X_test
        )

        mae = mean_absolute_error(

            self.y_test,

            predictions
        )

        self.assertLess(

            mae,

            80,

            "Random Forest MAE too high."
        )

    # =====================================================
    # Test XGBoost Model
    # =====================================================

    def test_xgboost_model(self):
        """
        Validate XGBoost model.
        """

        print("\nTesting XGBoost model...")

        model = joblib.load(

            XGBOOST_MODEL_FILE
        )

        predictions = model.predict(

            self.X_test
        )

        mae = mean_absolute_error(

            self.y_test,

            predictions
        )

        rmse = np.sqrt(

            mean_squared_error(

                self.y_test,

                predictions
            )
        )

        r2 = r2_score(

            self.y_test,

            predictions
        )

        print(f"\nXGBoost MAE  : {round(mae, 2)}")

        print(f"XGBoost RMSE : {round(rmse, 2)}")

        print(f"XGBoost R²   : {round(r2, 4)}")

        self.assertLess(

            mae,

            60,

            "XGBoost MAE too high."
        )

        self.assertGreater(

            r2,

            0.75,

            "XGBoost R² score too low."
        )

    # =====================================================
    # Test Prediction Shape
    # =====================================================

    def test_prediction_shape(self):
        """
        Verify prediction output shape.
        """

        print("\nChecking prediction shape...")

        model = joblib.load(

            XGBOOST_MODEL_FILE
        )

        predictions = model.predict(

            self.X_test
        )

        self.assertEqual(

            len(predictions),

            len(self.y_test),

            "Prediction shape mismatch."
        )

    # =====================================================
    # Test Prediction Values
    # =====================================================

    def test_prediction_values(self):
        """
        Verify prediction values are valid.
        """

        print("\nChecking prediction values...")

        model = joblib.load(

            XGBOOST_MODEL_FILE
        )

        predictions = model.predict(

            self.X_test
        )

        self.assertFalse(

            np.isnan(predictions).any(),

            "NaN predictions detected."
        )

        self.assertFalse(

            np.isinf(predictions).any(),

            "Infinite predictions detected."
        )

    # =====================================================
    # Test Train-Test Consistency
    # =====================================================

    def test_train_test_consistency(self):
        """
        Verify train-test dataset consistency.
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

            "Train and test columns mismatch."
        )

    # =====================================================
    # Test Dataset Size
    # =====================================================

    def test_dataset_size(self):
        """
        Verify dataset size is sufficient.
        """

        print("\nChecking dataset size...")

        self.assertGreater(

            len(self.train_df),

            1000,

            "Training dataset too small."
        )

        self.assertGreater(

            len(self.test_df),

            100,

            "Test dataset too small."
        )

    # =====================================================
    # Test Feature Variability
    # =====================================================

    def test_feature_variability(self):
        """
        Verify features contain variability.
        """

        print("\nChecking feature variability...")

        numeric_columns = self.train_df.select_dtypes(

            include=[np.number]
        ).columns

        for column in numeric_columns:

            unique_values = self.train_df[column].nunique()

            self.assertGreater(

                unique_values,

                1,

                f"No variability found in: {column}"
            )

    # =====================================================
    # Test Target Distribution
    # =====================================================

    def test_target_distribution(self):
        """
        Verify target distribution validity.
        """

        print("\nChecking target distribution...")

        self.assertTrue(

            (self.train_df["cnt"] >= 0).all(),

            "Negative values found in target."
        )

        self.assertGreater(

            self.train_df["cnt"].std(),

            0,

            "Target variable has no variability."
        )


# =========================================================
# Run Unit Tests
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" Running Training Pipeline Tests ")
    print("========================================")

    unittest.main(

        verbosity=2
    )
