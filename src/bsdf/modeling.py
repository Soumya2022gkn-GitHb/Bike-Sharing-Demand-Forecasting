"""Model training utilities."""

from __future__ import annotations

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from bsdf.features import build_preprocessor

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None


def build_candidate_models(random_state: int) -> dict[str, Pipeline]:
    """Create candidate regression pipelines for model comparison."""

    models = {
        "linear_regression": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(scale_numeric=True)),
                ("model", LinearRegression()),
            ],
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(scale_numeric=False)),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=180,
                        max_depth=18,
                        min_samples_leaf=2,
                        random_state=random_state,
                        n_jobs=1,
                    ),
                ),
            ],
        ),
        "gradient_boosting": Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(scale_numeric=False)),
                (
                    "model",
                    GradientBoostingRegressor(
                        learning_rate=0.06,
                        n_estimators=350,
                        max_depth=4,
                        min_samples_leaf=5,
                        random_state=random_state,
                    ),
                ),
            ],
        ),
    }

    if XGBRegressor is not None:
        models["xgboost"] = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(scale_numeric=False)),
                (
                    "model",
                    XGBRegressor(
                        objective="reg:squarederror",
                        n_estimators=350,
                        learning_rate=0.05,
                        max_depth=5,
                        subsample=0.85,
                        colsample_bytree=0.85,
                        random_state=random_state,
                        n_jobs=1,
                    ),
                ),
            ],
        )

    return models


def train_models(models: dict[str, Pipeline], X_train, y_train) -> dict[str, Pipeline]:
    """Fit every candidate model and return trained pipelines."""

    trained_models: dict[str, Pipeline] = {}
    for model_name, pipeline in models.items():
        trained_models[model_name] = pipeline.fit(X_train, y_train)
    return trained_models
