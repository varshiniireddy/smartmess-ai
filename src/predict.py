"""
Inference and Kitchen Preparation Advisory Module
Loads the trained pipeline to predict food waste and provide
actionable food preparation quantity recommendations for hostel/canteen staff.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class FoodWastePredictor:
    def __init__(self, model_path: str = None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            model_path = os.path.join(base_dir, "models", "waste_prediction_model.joblib")
        
        self.model_path = model_path
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        """Loads trained pipeline from disk, or alerts user if not trained yet."""
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            self.pipeline = None

    def is_model_ready(self) -> bool:
        return self.pipeline is not None

    def predict_waste(self, input_data: dict or pd.DataFrame) -> np.ndarray:
        """
        Predicts expected food waste in kilograms.
        """
        if not self.is_model_ready():
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. Please run train.py first."
            )

        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        else:
            df = input_data.copy()

        predictions = self.pipeline.predict(df)
        # Waste cannot be negative
        return np.maximum(0.0, np.round(predictions, 2))

    def recommend_kitchen_prep(
        self,
        meal_type: str,
        academic_status: str,
        weather: str,
        day_of_week: str,
        dish_category: str,
        dish_popularity_rating: float,
        hostel_registered_count: int,
        estimated_diners: int,
        std_portion_kg: float,
        avg_cost_per_kg: float = 65.0
    ) -> dict:
        """
        Core decision-support engine:
        1. Estimates baseline preparation (traditional unoptimized canteen preparation)
        2. Predicts waste under baseline preparation
        3. Recommends optimized cooking quantity with safety buffer
        4. Calculates potential kg saved and financial savings
        """
        is_weekend = 1 if day_of_week in ["Saturday", "Sunday"] else 0

        # Traditional cook habit: prepares for estimated diners + 14% buffer
        unoptimized_buffer = 0.14
        unoptimized_prep_kg = round(estimated_diners * (1 + unoptimized_buffer) * std_portion_kg, 2)

        input_payload = {
            "meal_type": meal_type,
            "academic_status": academic_status,
            "weather": weather,
            "day_of_week": day_of_week,
            "dish_category": dish_category,
            "dish_popularity_rating": dish_popularity_rating,
            "hostel_registered_count": hostel_registered_count,
            "estimated_diners": estimated_diners,
            "std_portion_kg": std_portion_kg,
            "food_prepared_kg": unoptimized_prep_kg,
            "is_weekend": is_weekend
        }

        # Predict waste under traditional approach
        if self.is_model_ready():
            expected_waste_kg = float(self.predict_waste(input_payload)[0])
        else:
            # Fallback heuristic if model is not yet compiled
            expected_waste_kg = round(unoptimized_prep_kg * (0.22 - 0.03 * dish_popularity_rating), 2)
            expected_waste_kg = max(2.0, expected_waste_kg)

        waste_pct = round((expected_waste_kg / unoptimized_prep_kg) * 100, 1) if unoptimized_prep_kg > 0 else 0.0

        # Popularity-adjusted consumption factor (e.g., 4.5 rating -> eats ~105% standard portion; 2.5 rating -> eats ~85%)
        consumption_multiplier = 0.85 + (dish_popularity_rating - 2.0) * 0.07
        expected_consumption_kg = round(estimated_diners * std_portion_kg * consumption_multiplier, 2)

        # Smart Safety Buffer: 5% for highly popular dishes, 7% for others to prevent food shortage
        safety_buffer_pct = 0.05 if dish_popularity_rating >= 4.0 else 0.07
        recommended_prep_kg = round(expected_consumption_kg * (1 + safety_buffer_pct), 2)

        # Prevent recommending more than traditional unoptimized preparation
        recommended_prep_kg = min(recommended_prep_kg, unoptimized_prep_kg)

        potential_waste_saved_kg = round(max(0.0, unoptimized_prep_kg - recommended_prep_kg), 2)
        estimated_cost_savings = round(potential_waste_saved_kg * avg_cost_per_kg, 2)

        # Risk Classification
        if waste_pct > 15.0:
            risk_level = "High Waste Risk"
            alert_color = "red"
            advice = f"High risk of excess leftovers! The dish has a modest popularity rating ({dish_popularity_rating}/5.0). Strongly reduce over-preparation to avoid throwing away ~{expected_waste_kg} kg."
        elif waste_pct >= 8.0:
            risk_level = "Moderate Waste Risk"
            alert_color = "yellow"
            advice = f"Standard leftover margin expected. Prepare ~{recommended_prep_kg} kg with the recommended 6% safety buffer."
        else:
            risk_level = "Optimal / Low Waste"
            alert_color = "green"
            advice = f"High demand and low waste expected! Prepare the full ~{recommended_prep_kg} kg to avoid student shortages."

        return {
            "unoptimized_prep_kg": unoptimized_prep_kg,
            "predicted_waste_kg": expected_waste_kg,
            "waste_percentage": waste_pct,
            "recommended_prep_kg": recommended_prep_kg,
            "potential_waste_saved_kg": potential_waste_saved_kg,
            "estimated_cost_savings_inr": estimated_cost_savings,
            "risk_level": risk_level,
            "alert_color": alert_color,
            "advisory_message": advice
        }


if __name__ == "__main__":
    predictor = FoodWastePredictor()
    sample = predictor.recommend_kitchen_prep(
        meal_type="Lunch",
        academic_status="Regular",
        weather="Sunny",
        day_of_week="Monday",
        dish_category="North Indian Veg",
        dish_popularity_rating=4.8,
        hostel_registered_count=650,
        estimated_diners=500,
        std_portion_kg=0.48
    )
    print("Sample Kitchen Recommendation:")
    for k, v in sample.items():
        print(f"  {k}: {v}")
