"""
Flask Web Application Backend (AIML + Web Technologies)
Connects HTML, CSS, JavaScript frontend with Scikit-learn ML models.
Run via: python server.py
"""

import os
import sys
import json
import pandas as pd
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

# Ensure project root in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predict import FoodWastePredictor
from src.train import train_and_evaluate
from src.auth import register_user, authenticate_user
from data.generate_data import MENU_ITEMS, WEATHER_CONDITIONS, generate_hostel_waste_data


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "smartmess_secret_key_2026_aiml_webtech"
CORS(app)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "mess_waste_dataset.csv")
METRICS_PATH = os.path.join(PROJECT_ROOT, "models", "metrics.json")
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "waste_prediction_model.joblib")

predictor = FoodWastePredictor(model_path=MODEL_PATH)


# --- Authentication Routes ---
@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    """Registers a new user and sets Flask session."""
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    role = data.get("role", "Kitchen Staff")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    res = register_user(username, email, password, role)
    if res["success"]:
        session["user"] = res["user"]
        return jsonify({"success": True, "user": res["user"]})
    return jsonify(res), 400


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    """Authenticates credentials and establishes session."""
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    res = authenticate_user(username, password)
    if res["success"]:
        session["user"] = res["user"]
        return jsonify({"success": True, "user": res["user"]})
    return jsonify(res), 401


@app.route("/api/auth/me", methods=["GET"])
def auth_me():
    """Returns currently authenticated session user."""
    user = session.get("user")
    if user:
        return jsonify({"authenticated": True, "user": user})
    return jsonify({"authenticated": False})


@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    """Logs out current user session."""
    session.pop("user", None)
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.route("/")
def index():
    """Serves the primary HTML5 dashboard."""
    return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def get_status():
    """Returns system and model availability status."""
    return jsonify({
        "status": "online",
        "model_ready": predictor.is_model_ready(),
        "has_data": os.path.exists(DATA_PATH)
    })


@app.route("/api/menu-options", methods=["GET"])
def get_menu_options():
    """Returns available menu dishes and weather categories for dropdowns."""
    return jsonify({
        "menu_items": MENU_ITEMS,
        "weather_conditions": WEATHER_CONDITIONS
    })


@app.route("/api/recommend", methods=["POST"])
def get_recommendation():
    """
    Receives JSON payload from JavaScript frontend and computes
    ML-driven waste prediction and recommended preparation quantity.
    """
    try:
        data = request.get_json() or {}

        meal_type = data.get("meal_type", "Lunch")
        academic_status = data.get("academic_status", "Regular")
        weather = data.get("weather", "Sunny")
        day_of_week = data.get("day_of_week", "Monday")
        dish_category = data.get("dish_category", "North Indian Veg")
        dish_popularity = float(data.get("dish_popularity_rating", 4.5))
        hostel_capacity = int(data.get("hostel_registered_count", 650))
        estimated_diners = int(data.get("estimated_diners", 510))
        std_portion = float(data.get("std_portion_kg", 0.48))
        cost_per_kg = float(data.get("avg_cost_per_kg", 65.0))

        # Check if model is initialized; if not, train baseline on first request
        if not predictor.is_model_ready():
            print("Model not found on first request. Auto-training initial model...")
            train_and_evaluate()
            predictor._load_model()

        result = predictor.recommend_kitchen_prep(
            meal_type=meal_type,
            academic_status=academic_status,
            weather=weather,
            day_of_week=day_of_week,
            dish_category=dish_category,
            dish_popularity_rating=dish_popularity,
            hostel_registered_count=hostel_capacity,
            estimated_diners=estimated_diners,
            std_portion_kg=std_portion,
            avg_cost_per_kg=cost_per_kg
        )

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/historical", methods=["GET"])
def get_historical_data():
    """Returns aggregated summary data for Chart.js visualizations."""
    if not os.path.exists(DATA_PATH):
        # Generate initial data if not present
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df_gen = generate_hostel_waste_data(days=450, total_hostel_students=650)
        df_gen.to_csv(DATA_PATH, index=False)

    df = pd.read_csv(DATA_PATH)

    # Aggregations for charts
    by_meal = df.groupby("meal_type")["food_waste_kg"].mean().round(2).to_dict()

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    by_day_series = df.groupby("day_of_week")["food_waste_kg"].mean().round(2)
    by_day = {d: float(by_day_series.get(d, 0.0)) for d in days_order}

    by_academic = df.groupby("academic_status")["waste_percentage"].mean().round(1).to_dict()

    summary = {
        "total_meals": int(len(df)),
        "avg_waste_kg": round(float(df["food_waste_kg"].mean()), 2),
        "total_waste_kg": round(float(df["food_waste_kg"].sum()), 1),
        "avg_waste_pct": round(float(df["waste_percentage"].mean()), 1),
        "by_meal": by_meal,
        "by_day": by_day,
        "by_academic": by_academic
    }

    return jsonify(summary)


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """Returns Scikit-learn model evaluation metrics and feature importance."""
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        # Auto-train to produce metrics
        _, payload = train_and_evaluate()
        return jsonify(payload)


@app.route("/api/train", methods=["POST"])
def retrain_model():
    """Triggers ML model retraining via AJAX."""
    try:
        pipeline, metrics = train_and_evaluate()
        predictor._load_model()
        return jsonify({
            "success": True,
            "message": "Model retrained successfully!",
            "best_model": metrics.get("best_model")
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/log-shift", methods=["POST"])
def log_shift():
    """Logs shift records into the dataset."""
    try:
        payload = request.get_json() or {}
        # Append to CSV if exists
        if os.path.exists(DATA_PATH):
            df_new = pd.DataFrame([payload])
            df_new.to_csv(DATA_PATH, mode="a", header=False, index=False)
        return jsonify({"success": True, "message": "Shift logged successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("  🍲 Food Waste Prediction Web Application (AIML + Web Tech)")
    print("  Server running at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
