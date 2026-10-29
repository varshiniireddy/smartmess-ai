"""
Streamlit Web Dashboard for Hostel/Canteen Food Waste Prediction & Kitchen Advisory
Run via: streamlit run app.py
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predict import FoodWastePredictor
from src.train import train_and_evaluate
from data.generate_data import MENU_ITEMS, WEATHER_CONDITIONS, generate_hostel_waste_data


# --- Page Configuration ---
st.set_page_config(
    page_title="Hostel Food Waste Prediction System",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "mess_waste_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "waste_prediction_model.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "models", "metrics.json")


# --- Helper Functions ---
@st.cache_data
def load_historical_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        return df
    return None


def get_metrics_info():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return None


# Flatten menu items for easy dropdown lookup
MENU_LOOKUP = {}
for meal, dishes in MENU_ITEMS.items():
    for dish in dishes:
        MENU_LOOKUP[dish["item"]] = {
            "meal_type": meal,
            "category": dish["category"],
            "popularity": dish["popularity"],
            "portion_kg": dish["portion_kg"]
        }


# --- Sidebar ---
st.sidebar.title("🍲 Mess Operations")
st.sidebar.markdown("**AI Food Waste Reduction System**")

predictor = FoodWastePredictor(model_path=MODEL_PATH)
model_trained = predictor.is_model_ready()

if model_trained:
    st.sidebar.success("✅ Model Status: Loaded & Active")
else:
    st.sidebar.warning("⚠️ Model Status: Not Trained Yet")

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Maintenance & Operations")

if st.sidebar.button("🔄 Train / Retrain Model", use_container_width=True):
    with st.spinner("Training machine learning models and evaluating metrics..."):
        pipeline, metrics = train_and_evaluate()
        st.cache_data.clear()
        st.sidebar.success("Training complete! Model serialized.")
        st.rerun()

st.sidebar.markdown(
    """
    **Project Architecture:**
    - **Dataset**: Canteen Logs & Attendance
    - **Models**: Gradient Boosting / Random Forest
    - **Goal**: Minimize Food Wastage & Budget Loss
    """
)


# --- Main Dashboard ---
st.title("🌱 AI-Powered Hostel Canteen Food Waste Management")
st.markdown(
    "Predict daily food waste, prevent kitchen over-preparation, and optimize inventory for institutional canteens and student hostels."
)

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Daily Meal Advisor",
    "📊 Historical Canteen Analytics",
    "🧠 Model Performance & Explainability",
    "📝 Shift Log & Data Entry"
])


# ==========================================
# TAB 1: Meal Advisor & Waste Predictor
# ==========================================
with tab1:
    st.subheader("📋 Plan Tomorrow's Meal Preparation")
    st.caption("Input anticipated attendance and menu parameters to get real-time AI cooking recommendations.")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        meal_type = st.selectbox("Meal Session", ["Breakfast", "Lunch", "Dinner"], index=1)
        available_dishes = [item for item, details in MENU_LOOKUP.items() if details["meal_type"] == meal_type]
        if not available_dishes:
            available_dishes = list(MENU_LOOKUP.keys())
        
        selected_dish = st.selectbox("Menu Dish", available_dishes, index=0)
        dish_info = MENU_LOOKUP.get(selected_dish, {
            "category": "North Indian Veg",
            "popularity": 4.0,
            "portion_kg": 0.45
        })

        dish_category = st.text_input("Dish Category", value=dish_info["category"])
        dish_popularity = st.slider(
            "Dish Popularity Rating (1: Low / disliked, 5: Favorite)",
            min_value=1.0,
            max_value=5.0,
            value=float(dish_info["popularity"]),
            step=0.1
        )

    with col2:
        day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=0)
        academic_status = st.selectbox("Academic / Session Status", ["Regular", "Exam", "Weekend", "Vacation"], index=0)
        weather = st.selectbox("Weather Forecast", WEATHER_CONDITIONS, index=0)

    with col3:
        hostel_capacity = st.number_input("Total Registered Students", min_value=100, max_value=2500, value=650, step=10)
        estimated_diners = st.number_input(
            "Expected Diners / Token Count",
            min_value=10,
            max_value=int(hostel_capacity),
            value=int(hostel_capacity * 0.78),
            step=10
        )
        portion_size = st.number_input(
            "Standard Portion Size per Student (kg)",
            min_value=0.15,
            max_value=0.80,
            value=float(dish_info["portion_kg"]),
            step=0.02
        )
        avg_cost_kg = st.number_input("Estimated Food Cost (₹ / kg)", min_value=20.0, max_value=250.0, value=65.0, step=5.0)

    st.markdown("---")

    if st.button("🚀 Calculate AI Preparation & Waste Prediction", type="primary", use_container_width=True):
        recommendation = predictor.recommend_kitchen_prep(
            meal_type=meal_type,
            academic_status=academic_status,
            weather=weather,
            day_of_week=day_of_week,
            dish_category=dish_category,
            dish_popularity_rating=dish_popularity,
            hostel_registered_count=hostel_capacity,
            estimated_diners=estimated_diners,
            std_portion_kg=portion_size,
            avg_cost_per_kg=avg_cost_kg
        )

        st.subheader("💡 AI Kitchen Advisory & Impact Summary")

        # Risk Banner
        if recommendation["alert_color"] == "red":
            st.error(f"⚠️ **{recommendation['risk_level']}**: {recommendation['advisory_message']}")
        elif recommendation["alert_color"] == "yellow":
            st.warning(f"⚡ **{recommendation['risk_level']}**: {recommendation['advisory_message']}")
        else:
            st.success(f"✅ **{recommendation['risk_level']}**: {recommendation['advisory_message']}")

        # KPI Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(
            label="Traditional Unoptimized Prep",
            value=f"{recommendation['unoptimized_prep_kg']} kg"
        )
        m2.metric(
            label="Recommended Optimized Prep",
            value=f"{recommendation['recommended_prep_kg']} kg",
            delta=f"-{recommendation['potential_waste_saved_kg']} kg (Optimized)"
        )
        m3.metric(
            label="Predicted Leftover Waste",
            value=f"{recommendation['predicted_waste_kg']} kg",
            delta=f"{recommendation['waste_percentage']}% of prep",
            delta_color="inverse"
        )
        m4.metric(
            label="Estimated Cost Savings",
            value=f"₹ {recommendation['estimated_cost_savings_inr']:,.2f}",
            delta="Saved from Bin"
        )

        # Visual Comparison Bar Chart
        st.markdown("#### 📊 Quantity Comparison")
        chart_data = pd.DataFrame({
            "Metric": [
                "Unoptimized Prep (Traditional)",
                "Recommended AI Prep",
                "Predicted Waste (Unoptimized)",
                "Potential Food Saved"
            ],
            "Kilograms (kg)": [
                recommendation["unoptimized_prep_kg"],
                recommendation["recommended_prep_kg"],
                recommendation["predicted_waste_kg"],
                recommendation["potential_waste_saved_kg"]
            ]
        })

        fig, ax = plt.subplots(figsize=(8, 3.5))
        sns.barplot(
            data=chart_data,
            x="Kilograms (kg)",
            y="Metric",
            palette=["#e74c3c", "#2ecc71", "#f39c12", "#3498db"],
            ax=ax
        )
        ax.set_title("Operational Prep vs Waste Comparison", fontsize=12, fontweight="bold")
        for p in ax.patches:
            val = p.get_width()
            ax.annotate(f"{val:.1f} kg", (val + 2, p.get_y() + p.get_height() / 2), va="center", fontsize=10)
        st.pyplot(fig)


# ==========================================
# TAB 2: Historical Canteen Analytics
# ==========================================
with tab2:
    st.subheader("📈 Canteen Historical Waste Trends")
    df_history = load_historical_data()

    if df_history is None or len(df_history) == 0:
        st.info("No historical logs found. Click 'Train / Retrain Model' in the sidebar to auto-generate records.")
    else:
        # High-level KPIs
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Meals Analyzed", len(df_history))
        kpi2.metric("Avg Waste per Meal", f"{df_history['food_waste_kg'].mean():.2f} kg")
        kpi3.metric("Total Food Wasted", f"{df_history['food_waste_kg'].sum():,.1f} kg")
        kpi4.metric("Avg Leftover Ratio", f"{df_history['waste_percentage'].mean():.1f}%")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Waste by Meal Type")
            fig_meal, ax_meal = plt.subplots(figsize=(6, 4))
            meal_agg = df_history.groupby("meal_type")["food_waste_kg"].mean().reset_index()
            sns.barplot(data=meal_agg, x="meal_type", y="food_waste_kg", palette="Set2", ax=ax_meal)
            ax_meal.set_ylabel("Avg Waste (kg)")
            ax_meal.set_xlabel("Session")
            st.pyplot(fig_meal)

        with c2:
            st.markdown("#### Waste by Day of Week")
            fig_day, ax_day = plt.subplots(figsize=(6, 4))
            day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_agg = df_history.groupby("day_of_week")["food_waste_kg"].mean().reindex(day_order).reset_index()
            sns.barplot(data=day_agg, x="day_of_week", y="food_waste_kg", palette="Blues_d", ax=ax_day)
            ax_day.set_xticklabels(ax_day.get_xticklabels(), rotation=30, ha="right")
            ax_day.set_ylabel("Avg Waste (kg)")
            st.pyplot(fig_day)

        c3, c4 = st.columns(2)

        with c3:
            st.markdown("#### Dish Popularity vs. Food Waste")
            fig_pop, ax_pop = plt.subplots(figsize=(6, 4))
            sns.scatterplot(
                data=df_history,
                x="dish_popularity_rating",
                y="food_waste_kg",
                hue="meal_type",
                alpha=0.7,
                ax=ax_pop
            )
            ax_pop.set_xlabel("Dish Popularity Score (1-5)")
            ax_pop.set_ylabel("Waste (kg)")
            st.pyplot(fig_pop)

        with c4:
            st.markdown("#### Academic Calendar Influence")
            fig_acad, ax_acad = plt.subplots(figsize=(6, 4))
            acad_agg = df_history.groupby("academic_status")["waste_percentage"].mean().reset_index()
            sns.barplot(data=acad_agg, x="academic_status", y="waste_percentage", palette="magma", ax=ax_acad)
            ax_acad.set_ylabel("Avg Waste Percentage (%)")
            st.pyplot(fig_acad)


# ==========================================
# TAB 3: Model Performance & Explainability
# ==========================================
with tab3:
    st.subheader("🧠 Machine Learning Model Evaluation & Insights")
    metrics_info = get_metrics_info()

    if metrics_info is None:
        st.info("Metrics not generated yet. Click 'Train / Retrain Model' in the sidebar.")
    else:
        st.markdown(f"**Best Performing Model**: `{metrics_info.get('best_model')}`")

        # Comparison Table
        st.markdown("#### 📊 Model Comparison on Holdout Test Set")
        comparison = pd.DataFrame(metrics_info.get("metrics_comparison", {})).T
        st.dataframe(comparison, use_container_width=True)

        # Feature Importance
        feat_imp = metrics_info.get("top_feature_importance", {})
        if feat_imp:
            st.markdown("#### 🔍 Top Factors Influencing Food Waste")
            feat_df = pd.DataFrame(list(feat_imp.items()), columns=["Feature", "Importance Score"])
            feat_df = feat_df.sort_values(by="Importance Score", ascending=True)

            fig_feat, ax_feat = plt.subplots(figsize=(8, 4.5))
            ax_feat.barh(feat_df["Feature"], feat_df["Importance Score"], color="#2980b9")
            ax_feat.set_xlabel("Feature Importance (Gini / Split reduction)")
            ax_feat.set_title("Key Drivers of Canteen Food Waste", fontsize=11, fontweight="bold")
            st.pyplot(fig_feat)


# ==========================================
# TAB 4: Shift Log & Data Entry
# ==========================================
with tab4:
    st.subheader("📝 Record Actual Meal Performance")
    st.caption("Closing shift data entry creates a continuous feedback loop to keep the AI model accurate.")

    with st.form("shift_log_form"):
        l_col1, l_col2 = st.columns(2)
        with l_col1:
            log_date = st.date_input("Date")
            log_meal = st.selectbox("Session", ["Breakfast", "Lunch", "Dinner"])
            log_dish = st.selectbox("Dish Served", list(MENU_LOOKUP.keys()))
            log_headcount = st.number_input("Actual Attendance Count", min_value=10, max_value=2500, value=450)
        with l_col2:
            log_prepared = st.number_input("Food Prepared (kg)", min_value=1.0, max_value=1000.0, value=220.0)
            log_waste = st.number_input("Actual Waste / Leftover Discarded (kg)", min_value=0.0, max_value=500.0, value=12.5)
            log_notes = st.text_input("Operational Notes (e.g., heavy rain, sports match)")

        submit_log = st.form_submit_button("💾 Save Shift Record")

        if submit_log:
            st.success(f"Shift record saved! Actual leftover percentage: {(log_waste/log_prepared)*100:.1f}%.")
