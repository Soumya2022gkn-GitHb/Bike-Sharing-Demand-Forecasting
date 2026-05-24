# =========================================================
# File: tests/test_inference.py
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

REPORTS_DIR = (

    PROJECT_ROOT
    / "reports"
)


# =========================================================
# Define File Paths
# =========================================================

TEST_DATA_FILE = (

    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)

XGBOOST_MODEL_FILE = (

    MODELS_DIR
    / "xgboost_model.pkl"
)

SCALER_FILE = (

    MODELS_DIR
    / "scaler.pkl"
)

INFERENCE_RESULTS_FILE = (

    REPORTS_DIR
    / "inference_results.csv"
)


# =========================================================
# Test Class
# =========================================================

class TestInferencePipeline(unittest.TestCase):

    # =====================================================
    # Setup Test Environment
    # =====================================================

    @classmethod
    def setUpClass(cls):

        print("\n========================================")
        print(" Setting Up Inference Tests ")
        print("========================================")

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

        cls.model = joblib.load(

            XGBOOST_MODEL_FILE
        )

        cls.scaler = joblib.load(

            SCALER_FILE
        )

    # =====================================================
    # Test Required Files
    # =====================================================

    def test_required_files_exist(self):
        """
        Verify required inference files exist.
        """

        print("\nChecking required inference files...")

        required_files = [

            TEST_DATA_FILE,

            XGBOOST_MODEL_FILE,

            SCALER_FILE
        ]

        for file in required_files:

            self.assertTrue(

                file.exists(),

                f"Missing required file: {file.name}"
            )

    # =====================================================
    # Test Model Loading
    # =====================================================

    def test_model_loading(self):
        """
        Verify model loads successfully.
        """

        print("\nChecking model loading...")

        self.assertIsNotNone(

            self.model,

            "Model failed to load."
        )

    # =====================================================
    # Test Scaler Loading
    # =====================================================

    def test_scaler_loading(self):
        """
        Verify scaler loads successfully.
        """

        print("\nChecking scaler loading...")

        self.assertIsNotNone(

            self.scaler,

            "Scaler failed to load."
        )

    # =====================================================
    # Test Target Column
    # =====================================================

    def test_target_column_exists(self):
        """
        Verify target column exists.
        """

        print("\nChecking target column...")

        dataset_columns = [

            column.lower()
            for column in self.test_df.columns
        ]

        self.assertIn(

            self.target_column,

            dataset_columns,

            "Target column missing."
        )

    # =====================================================
    # Test Inference Predictions
    # =====================================================

    def test_prediction_generation(self):
        """
        Verify inference predictions are generated.
        """

        print("\nGenerating inference predictions...")

        predictions = self.model.predict(

            self.X_test
        )

        self.assertEqual(

            len(predictions),

            len(self.X_test),

            "Prediction length mismatch."
        )

    # =====================================================
    # Test Prediction Values
    # =====================================================

    def test_prediction_values(self):
        """
        Verify prediction values are valid.
        """

        print("\nChecking prediction values...")

        predictions = self.model.predict(

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
    # Test Prediction Metrics
    # =====================================================

    def test_prediction_metrics(self):
        """
        Validate forecasting performance.
        """

        print("\nCalculating inference metrics...")

        predictions = self.model.predict(

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

        print(f"\nInference MAE  : {round(mae, 2)}")

        print(f"Inference RMSE : {round(rmse, 2)}")

        print(f"Inference R²   : {round(r2, 4)}")

        self.assertLess(

            mae,

            60,

            "Inference MAE too high."
        )

        self.assertGreater(

            r2,

            0.75,

            "Inference R² score too low."
        )

    # =====================================================
    # Test Positive Predictions
    # =====================================================

    def test_positive_predictions(self):
        """
        Verify predictions are non-negative.
        """

        print("\nChecking prediction positivity...")

        predictions = self.model.predict(

            self.X_test
        )

        self.assertTrue(

            (predictions >= 0).all(),

            "Negative predictions detected."
        )

    # =====================================================
    # Test Inference Consistency
    # =====================================================

    def test_inference_consistency(self):
        """
        Verify inference consistency.
        """

        print("\nChecking inference consistency...")

        predictions_1 = self.model.predict(

            self.X_test
        )

        predictions_2 = self.model.predict(

            self.X_test
        )

        consistency = np.allclose(

            predictions_1,

            predictions_2
        )

        self.assertTrue(

            consistency,

            "Inference predictions are inconsistent."
        )

    # =====================================================
    # Test Feature Consistency
    # =====================================================

    def test_feature_consistency(self):
        """
        Verify input feature consistency.
        """

        print("\nChecking feature consistency...")

        self.assertGreater(

            self.X_test.shape[1],

            10,

            "Too few input features."
        )

        self.assertGreater(

            self.X_test.shape[0],

            100,

            "Too few inference records."
        )

    # =====================================================
    # Test Dataset Missing Values
    # =====================================================

    def test_missing_values(self):
        """
        Verify inference dataset contains no missing values.
        """

        print("\nChecking missing values...")

        missing_values = self.X_test.isnull().sum().sum()

        self.assertEqual(

            missing_values,

            0,

            "Missing values detected in inference dataset."
        )

    # =====================================================
    # Test Infinite Values
    # =====================================================

    def test_infinite_values(self):
        """
        Verify inference dataset contains no infinite values.
        """

        print("\nChecking infinite values...")

        numeric_dataset = self.X_test.select_dtypes(

            include=[np.number]
        )

        infinite_values = np.isinf(

            numeric_dataset
        ).sum().sum()

        self.assertEqual(

            infinite_values,

            0,

            "Infinite values detected in inference dataset."
        )

    # =====================================================
    # Test Save Inference Results
    # =====================================================

    def test_save_inference_results(self):
        """
        Verify inference results are saved successfully.
        """

        print("\nSaving inference results...")

        predictions = self.model.predict(

            self.X_test
        )

        REPORTS_DIR.mkdir(

            parents=True,

            exist_ok=True
        )

        results_df = pd.DataFrame({

            "Actual_Demand": self.y_test,

            "Predicted_Demand": predictions
        })

        results_df.to_csv(

            INFERENCE_RESULTS_FILE,

            index=False
        )

        self.assertTrue(

            INFERENCE_RESULTS_FILE.exists(),

            "Inference results file was not created."
        )

    # =====================================================
    # Test Operational Forecast Readiness
    # =====================================================

    def test_operational_forecast_readiness(self):
        """
        Validate deployment readiness.
        """

        print("\nChecking operational readiness...")

        predictions = self.model.predict(

            self.X_test
        )

        average_prediction = np.mean(

            predictions
        )

        self.assertGreater(

            average_prediction,

            0,

            "Average prediction is invalid."
        )


# =========================================================
# Run Unit Tests
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print(" Running Inference Pipeline Tests ")
    print("========================================")

    unittest.main(

        verbosity=2
    )
