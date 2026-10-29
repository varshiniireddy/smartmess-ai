"""
Quickstart Verification Script
Runs end-to-end:
1. Verifies dataset and trains machine learning models
2. Evaluates performance
3. Runs sample predictions and prints kitchen preparation advisories
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from src.train import train_and_evaluate
from src.predict import FoodWastePredictor


def main():
    print("=" * 65)
    print("      FOOD WASTE PREDICTION & KITCHEN ADVISORY SYSTEM")
    print("=" * 65)

    print("\n[Step 1] Training & evaluating machine learning pipeline...")
    pipeline, metrics = train_and_evaluate()

    print("\n[Step 2] Testing Inference & Kitchen Preparation Advisor...")
    predictor = FoodWastePredictor()

    scenarios = [
        {
            "label": "Scenario A: Regular Monday Lunch (Paneer Butter Masala - High Popularity)",
            "meal_type": "Lunch",
            "academic_status": "Regular",
            "weather": "Sunny",
            "day_of_week": "Monday",
            "dish_category": "North Indian Veg",
            "dish_popularity_rating": 4.8,
            "hostel_registered_count": 650,
            "estimated_diners": 520,
            "std_portion_kg": 0.48
        },
        {
            "label": "Scenario B: Sunday Dinner (Khichdi & Kadhi - Low Popularity on Weekend)",
            "meal_type": "Dinner",
            "academic_status": "Weekend",
            "weather": "Sunny",
            "day_of_week": "Sunday",
            "dish_category": "Light Dinner",
            "dish_popularity_rating": 2.6,
            "hostel_registered_count": 650,
            "estimated_diners": 380,
            "std_portion_kg": 0.35
        },
        {
            "label": "Scenario C: Exam Season Lunch (Biryani - Peak Attendance)",
            "meal_type": "Lunch",
            "academic_status": "Exam",
            "weather": "Rainy",
            "day_of_week": "Wednesday",
            "dish_category": "Special / Biryani",
            "dish_popularity_rating": 4.9,
            "hostel_registered_count": 650,
            "estimated_diners": 610,
            "std_portion_kg": 0.52
        }
    ]

    for sc in scenarios:
        print("\n" + "-" * 65)
        print(f"📌 {sc['label']}")
        print("-" * 65)
        result = predictor.recommend_kitchen_prep(
            meal_type=sc["meal_type"],
            academic_status=sc["academic_status"],
            weather=sc["weather"],
            day_of_week=sc["day_of_week"],
            dish_category=sc["dish_category"],
            dish_popularity_rating=sc["dish_popularity_rating"],
            hostel_registered_count=sc["hostel_registered_count"],
            estimated_diners=sc["estimated_diners"],
            std_portion_kg=sc["std_portion_kg"]
        )

        print(f"  • Unoptimized Prep (Traditional) : {result['unoptimized_prep_kg']} kg")
        print(f"  • Predicted Waste (Unoptimized)  : {result['predicted_waste_kg']} kg ({result['waste_percentage']}%)")
        print(f"  • Recommended AI Prep Quantity   : {result['recommended_prep_kg']} kg")
        print(f"  • Food Saved From Waste          : {result['potential_waste_saved_kg']} kg")
        print(f"  • Estimated Money Saved          : ₹ {result['estimated_cost_savings_inr']:,.2f}")
        print(f"  • Alert Level & Advice           : [{result['risk_level']}] {result['advisory_message']}")

    print("\n" + "=" * 65)
    print("✅ System verification complete! Launch dashboard with:")
    print("   streamlit run app.py")
    print("=" * 65)


if __name__ == "__main__":
    main()
