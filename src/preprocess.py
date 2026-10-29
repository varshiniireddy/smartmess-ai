"""
Preprocessing and Feature Engineering Pipeline for Food Waste Prediction
"""

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split


CATEGORICAL_FEATURES = [
    "meal_type",
    "academic_status",
    "weather",
    "day_of_week",
    "dish_category"
]

NUMERICAL_FEATURES = [
    "dish_popularity_rating",
    "hostel_registered_count",
    "estimated_diners",
    "std_portion_kg",
    "food_prepared_kg",
    "is_weekend"
]

TARGET_COLUMN = "food_waste_kg"


def load_dataset(csv_path: str) -> pd.DataFrame:
    """Loads and standardizes canteen waste dataset."""
    df = pd.read_csv(csv_path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month
        df["day_of_month"] = df["date"].dt.day
    return df


def build_preprocessor() -> ColumnTransformer:
    """Creates a Scikit-Learn ColumnTransformer for numerical and categorical features."""
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                NUMERICAL_FEATURES
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES
            )
        ],
        remainder="drop"
    )
    return preprocessor


def prepare_train_test_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """Splits dataset into train and test feature matrices and targets."""
    features = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
    
    # Ensure missing columns are handled safely
    for col in features:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' is missing from the dataset.")

    X = df[features].copy()
    y = df[TARGET_COLUMN].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test
