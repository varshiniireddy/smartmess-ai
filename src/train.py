"""
Model Training and Evaluation Pipeline for Food Waste Prediction
Trains multiple regression models, compares evaluation metrics,
and serializes the best performing pipeline.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ensure project root directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocess import (
    load_dataset,
    build_preprocessor,
    prepare_train_test_data,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
)
from data.generate_data import generate_hostel_waste_data


def train_and_evaluate(data_path: str = None, models_dir: str = None):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    if data_path is None:
        data_path = os.path.join(base_dir, "data", "raw", "mess_waste_dataset.csv")
    if models_dir is None:
        models_dir = os.path.join(base_dir, "models")

    os.makedirs(models_dir, exist_ok=True)

    # If dataset doesn't exist or is small, auto-generate full 450-day dataset (~1350 records)
    if not os.path.exists(data_path) or len(pd.read_csv(data_path)) < 100:
        print("Populating dataset with 450 days of realistic hostel canteen operational records...")
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        df_generated = generate_hostel_waste_data(days=450, total_hostel_students=650)
        df_generated.to_csv(data_path, index=False)
        df = df_generated
    else:
        df = load_dataset(data_path)

    print(f"Loaded dataset containing {len(df)} meal logs.")

    X_train, X_test, y_train, y_test = prepare_train_test_data(df)
    preprocessor = build_preprocessor()

    candidate_models = {
        "Ridge Regression (Baseline)": Ridge(alpha=1.0),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)
    }

    results = {}
    best_model_name = None
    best_mae = float("inf")
    best_pipeline = None

    print("\n--- Training and Evaluating Models ---")
    for name, regressor in candidate_models.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", regressor)
        ])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        results[name] = {
            "MAE_kg": round(float(mae), 3),
            "RMSE_kg": round(float(rmse), 3),
            "R2_Score": round(float(r2), 4)
        }
        print(f"[{name}] -> MAE: {mae:.2f} kg | RMSE: {rmse:.2f} kg | R²: {r2:.4f}")

        if mae < best_mae:
            best_mae = mae
            best_model_name = name
            best_pipeline = pipeline

    print(f"\nBest Model Selected: {best_model_name} (MAE = {best_mae:.2f} kg)")

    # Save model pipeline
    model_save_path = os.path.join(models_dir, "waste_prediction_model.joblib")
    joblib.dump(best_pipeline, model_save_path)
    print(f"Saved best model pipeline to: {model_save_path}")

    # Extract feature importance if available
    feature_importance_dict = {}
    model_step = best_pipeline.named_steps["model"]
    prep_step = best_pipeline.named_steps["preprocessor"]
    
    if hasattr(model_step, "feature_importances_"):
        cat_encoder = prep_step.named_transformers_["cat"]
        cat_names = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
        all_feature_names = NUMERICAL_FEATURES + cat_names
        importances = model_step.feature_importances_
        sorted_idx = np.argsort(importances)[::-1]
        for idx in sorted_idx[:15]:
            feature_importance_dict[all_feature_names[idx]] = round(float(importances[idx]), 4)

    metrics_payload = {
        "best_model": best_model_name,
        "metrics_comparison": results,
        "top_feature_importance": feature_importance_dict,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "features": {
            "numerical": NUMERICAL_FEATURES,
            "categorical": CATEGORICAL_FEATURES
        }
    }

    metrics_save_path = os.path.join(models_dir, "metrics.json")
    with open(metrics_save_path, "w") as f:
        json.dump(metrics_payload, f, indent=4)
    print(f"Saved metrics summary to: {metrics_save_path}")

    return best_pipeline, metrics_payload


if __name__ == "__main__":
    train_and_evaluate()
