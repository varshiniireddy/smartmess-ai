"""
Synthetic Data Generator for Hostel/Canteen Food Waste Prediction
Generates realistic multi-year operational mess data with real-world dynamics:
- Academic calendar effects (exams, holidays, weekends)
- Dish popularity impact on consumption
- Weather impacts on dining out vs eating in
- Cook over-preparation patterns
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


MENU_ITEMS = {
    "Breakfast": [
        {"item": "Idli Sambhar", "category": "South Indian", "popularity": 4.2, "portion_kg": 0.30},
        {"item": "Poha & Jalebi", "category": "North Indian", "popularity": 3.9, "portion_kg": 0.28},
        {"item": "Poori Bhaji", "category": "North Indian", "popularity": 4.5, "portion_kg": 0.35},
        {"item": "Aloo Paratha", "category": "North Indian", "popularity": 4.7, "portion_kg": 0.38},
        {"item": "Upma & Chutney", "category": "South Indian", "popularity": 2.8, "portion_kg": 0.25},
        {"item": "Masala Dosa", "category": "South Indian", "popularity": 4.8, "portion_kg": 0.33},
        {"item": "Oats Porridge", "category": "Continental", "popularity": 2.2, "portion_kg": 0.22},
    ],
    "Lunch": [
        {"item": "Paneer Butter Masala & Roti", "category": "North Indian Veg", "popularity": 4.8, "portion_kg": 0.48},
        {"item": "Rajma Chawal", "category": "North Indian Veg", "popularity": 4.4, "portion_kg": 0.45},
        {"item": "Chole Bhature", "category": "North Indian Veg", "popularity": 4.7, "portion_kg": 0.50},
        {"item": "South Indian Veg Thali", "category": "South Indian Veg", "popularity": 3.8, "portion_kg": 0.46},
        {"item": "Mix Veg Curry & Dal Rice", "category": "Everyday Veg", "popularity": 3.2, "portion_kg": 0.42},
        {"item": "Kadhi Pakora & Steamed Rice", "category": "North Indian Veg", "popularity": 3.6, "portion_kg": 0.44},
        {"item": "Lauki Chana Dal & Roti", "category": "Everyday Veg", "popularity": 2.3, "portion_kg": 0.38},
        {"item": "Chicken Biryani / Veg Biryani", "category": "Special / Biryani", "popularity": 4.9, "portion_kg": 0.52},
    ],
    "Dinner": [
        {"item": "Dal Makhani & Naan", "category": "North Indian Veg", "popularity": 4.6, "portion_kg": 0.45},
        {"item": "Egg Curry / Malai Kofta & Roti", "category": "Special Dinner", "popularity": 4.5, "portion_kg": 0.47},
        {"item": "Khichdi & Kadhi", "category": "Light Dinner", "popularity": 2.6, "portion_kg": 0.35},
        {"item": "Veg Pulao & Raita", "category": "Rice Special", "popularity": 3.9, "portion_kg": 0.42},
        {"item": "Bhindi Masala & Phulka", "category": "Everyday Veg", "popularity": 3.4, "portion_kg": 0.40},
        {"item": "Baingan Bharta & Dal Tadka", "category": "Everyday Veg", "popularity": 2.7, "portion_kg": 0.39},
        {"item": "Pav Bhaji & Pulao", "category": "Fast Food Style", "popularity": 4.7, "portion_kg": 0.48},
    ]
}

WEATHER_CONDITIONS = ["Sunny", "Rainy", "Overcast", "Cold"]


def generate_hostel_waste_data(
    start_date="2024-01-01",
    days=450,
    total_hostel_students=650,
    seed=42
):
    """Generates synthetic dataset of meal attendance, preparation, consumption, and waste."""
    random.seed(seed)
    np.random.seed(seed)

    records = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")

    for day_idx in range(days):
        dt = current_date + timedelta(days=day_idx)
        date_str = dt.strftime("%Y-%m-%d")
        day_of_week = dt.strftime("%A")
        is_weekend = 1 if day_of_week in ["Saturday", "Sunday"] else 0
        month = dt.month

        # Academic season dynamics
        # May-June: Summer vacation, Nov/Dec: Exams & winter break
        if month in [5, 6]:
            session_status = "Vacation"
            base_occupancy = random.uniform(0.15, 0.30)
        elif month in [4, 11]:
            session_status = "Exam"
            base_occupancy = random.uniform(0.90, 0.98)
        elif is_weekend:
            session_status = "Weekend"
            base_occupancy = random.uniform(0.55, 0.75)
        else:
            session_status = "Regular"
            base_occupancy = random.uniform(0.82, 0.95)

        # Weather impacts hostelers eating outside
        weather = random.choices(WEATHER_CONDITIONS, weights=[0.55, 0.20, 0.15, 0.10])[0]
        weather_dine_out_penalty = -0.08 if weather == "Rainy" else (0.05 if weather == "Sunny" and is_weekend else 0.0)

        effective_headcount = int(total_hostel_students * base_occupancy)

        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            # Pick menu item
            dish_info = random.choice(MENU_ITEMS[meal_type])
            menu_item = dish_info["item"]
            dish_category = dish_info["category"]
            popularity = dish_info["popularity"]
            standard_portion = dish_info["portion_kg"]

            # Meal specific attendance factors
            if meal_type == "Breakfast":
                # Students often skip breakfast, especially on weekends
                meal_attendance_factor = random.uniform(0.50, 0.70) if is_weekend else random.uniform(0.70, 0.85)
            elif meal_type == "Lunch":
                meal_attendance_factor = random.uniform(0.75, 0.90)
            else: # Dinner
                # Weekend dinner many students eat out
                if is_weekend:
                    meal_attendance_factor = random.uniform(0.50, 0.70)
                else:
                    meal_attendance_factor = random.uniform(0.80, 0.95)

            # Adjust for weather & popularity
            meal_attendance_factor = np.clip(
                meal_attendance_factor - weather_dine_out_penalty + (popularity - 3.5) * 0.04,
                0.20,
                1.0
            )

            expected_demand_tokens = int(effective_headcount * meal_attendance_factor)
            
            # Actual attendance varies slightly from tokens booked
            attendance_noise = random.randint(-15, 12)
            actual_attendance = max(10, expected_demand_tokens + attendance_noise)

            # Kitchen preparation behavior:
            # Cooks often prepare based on standard capacity or slight overestimation buffer (8-18%)
            buffer_pct = random.uniform(0.08, 0.18)
            planned_attendance = int(expected_demand_tokens * (1.0 + buffer_pct))
            
            # Low popularity dishes get consumed less per person; high popularity dishes get consumed more
            consumption_factor = np.clip(standard_portion * (0.85 + 0.06 * popularity + random.uniform(-0.03, 0.03)), 0.18, 0.60)

            food_prepared_kg = round(planned_attendance * standard_portion, 2)
            actual_consumed_kg = round(min(food_prepared_kg, actual_attendance * consumption_factor), 2)
            
            # Actual waste
            food_waste_kg = round(max(0.0, food_prepared_kg - actual_consumed_kg), 2)
            waste_percentage = round((food_waste_kg / food_prepared_kg) * 100.0, 2) if food_prepared_kg > 0 else 0.0

            records.append({
                "date": date_str,
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "academic_status": session_status,
                "weather": weather,
                "meal_type": meal_type,
                "menu_item": menu_item,
                "dish_category": dish_category,
                "dish_popularity_rating": popularity,
                "hostel_registered_count": total_hostel_students,
                "estimated_diners": expected_demand_tokens,
                "actual_attendance": actual_attendance,
                "std_portion_kg": standard_portion,
                "food_prepared_kg": food_prepared_kg,
                "food_consumed_kg": actual_consumed_kg,
                "food_waste_kg": food_waste_kg,
                "waste_percentage": waste_percentage
            })

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "mess_waste_dataset.csv")
    
    print("Generating canteen & hostel mess waste dataset...")
    df = generate_hostel_waste_data(days=450, total_hostel_students=650)
    df.to_csv(csv_path, index=False)
    print(f"Dataset successfully generated at: {csv_path}")
    print(f"Total records: {len(df)}")
    print(f"Average food waste per meal: {df['food_waste_kg'].mean():.2f} kg ({df['waste_percentage'].mean():.1f}%)")
