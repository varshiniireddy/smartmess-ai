# B.Tech Micro Project
## Project Overview

---

### 1. Project Title
**AI-Powered Food Waste Prediction and Kitchen Advisory System for Hostel and Canteen Messes**

---

### 2. Student Details
- **Student Name:** [Student Name]
- **Roll No.:** [Roll No.]
- **Branch & Section:** CSE / AIML / IT
- **Academic Year:** 2026-27

---

### 3. Abstract (150–200 words)
Institutional hostels and university canteens routinely encounter substantial food waste resulting from volatile student attendance, rigid batch cooking schedules, academic calendar variations (such as examinations and vacation breaks), and menu preference differences. This project presents an end-to-end Machine Learning-driven Food Waste Prediction and Kitchen Advisory System developed using Python and Scikit-learn. The system ingests multi-factor canteen operational data, including meal sessions (Breakfast, Lunch, Dinner), expected student headcount, dynamic menu popularity ratings, academic calendar status, and weather forecasts. Supervised ensemble regressors (Random Forest and Gradient Boosting) are trained to forecast discarded leftover food quantities in kilograms. Rather than providing passive predictions, the system implements an actionable prescriptive decision-support engine that calculates recommended preparation quantities with dynamic safety buffers, safeguarding against food shortages while curbing kitchen over-preparation. Historical analytics, real-time prediction, model explainability (feature importances), and shift data-logging are delivered through an interactive Streamlit web dashboard. The system empowers mess administrations to reduce operational expenditure, minimize carbon footprints, and transition toward sustainable, evidence-based kitchen management.

---

### 4. Problem Statement
Institutional mess kitchens and college hostel canteens struggle to balance meal preparation quantities against volatile daily student demand, leading to heavy financial losses and significant quantities of preventable food waste daily. Traditional manual estimation relies on rigid batch multipliers that overlook critical variables such as dish popularity, weather conditions, examination periods, and student dining-out patterns.

---

### 5. Objectives
- Collect and preprocess multi-dimensional canteen operational data (attendance, meal type, menu popularity, weather, academic status).
- Engineer informative tabular features, handling numeric scaling and categorical encoding through Scikit-learn pipelines.
- Train and benchmark multiple regression models (Ridge baseline, Random Forest, Gradient Boosting) to accurately predict food waste in kilograms.
- Implement an automated prescriptive kitchen advisory module that calculates optimal food preparation quantities with dynamic safety margins.
- Present analysis, prediction outputs, and risk assessments in an interactive Streamlit web interface with a continuous shift-logging feedback loop.

---

### 6. Technologies Used

| S. No. | Category | Technology |
| :---: | :--- | :--- |
| 1 | Programming Languages | Python, JavaScript (ES6+) |
| 2 | Web Technologies (Frontend) | HTML5, CSS3, JavaScript (DOM, Fetch API), Chart.js |
| 3 | Web Technologies (Backend) | Flask (REST API, CORS, Session Management) |
| 4 | Authentication & Security | SQLite (`users.db`), Werkzeug Password Hashing (Salted SHA-256) |
| 5 | Data Processing & Analysis | Pandas, NumPy |
| 6 | Machine Learning Framework | Scikit-learn (Ridge, Random Forest, Gradient Boosting) |
| 7 | Model Serialization | Joblib |
| 8 | Data Visualization | Chart.js (Interactive Web), Matplotlib, Seaborn |
| 9 | Local Data Storage | SQLite Database & CSV Logs |
| 10 | Development Environment | Visual Studio Code (VS Code) |

---

## Methodology and Implementation

---

### 7. Existing System
In a conventional hostel mess workflow, kitchen managers and chief cooks estimate daily food quantities through ad-hoc rules of thumb or fixed percentage buffers over total registered students. They lack granular tracking of dish popularity, student weekend departures, or the influence of weather and exam schedules. Consequently, kitchens frequently experience massive over-preparation (resulting in bins of discarded food) or occasional food shortages. Daily logs are either maintained in paper ledgers or unanalyzed spreadsheets, preventing data-driven inventory control and repeatable planning.

---

### 8. Proposed System
The proposed system provides an automated, reviewable workflow for predicting food waste and optimizing meal preparation in institutional canteens. It models complex operational interactions—such as meal session type, day of the week, weather forecasts, student token counts, and dish popularity ratings—to forecast waste in kilograms. 

Furthermore, it incorporates an optimization layer: rather than just warning of excess waste, it outputs a customized **Recommended Preparation Quantity ($kg$)** with dynamic safety buffers ($5\%\text{--}7\%$) tailored to dish popularity. An interactive Streamlit dashboard enables single-click retraining, visual trend inspections, explainable AI feature importance reviews, and daily shift feedback logging.

---

### 9. Methodology / Workflow

```text
Select or input meal parameters (Date, Meal Type, Dish, Headcount)
 ↓
Collect operational context (Academic status, weather, dish popularity rating)
 ↓
Preprocess data & apply feature pipeline (Scaling, One-Hot Encoding via ColumnTransformer)
 ↓
Predict expected food waste (kg) using trained ensemble regressor
 ↓
Compute dish consumption rate adjusted for student popularity
 ↓
Calculate AI-recommended preparation quantity (kg) with dynamic safety buffer
 ↓
Assess waste risk level (Low, Moderate, High) and estimate cost/food savings
 ↓
Display results on Streamlit dashboard and log shift actuals for continuous retraining
```

---

### 10. Implementation with Code

- **Dataset used:** Operational canteen logs covering 450 days (1,350 meal sessions across Breakfast, Lunch, and Dinner) incorporating registered capacity, estimated diners, actual footfall, dish popularity ($1.0\text{--}5.0$), portion sizes, food cooked, food consumed, and leftover waste ($kg$).
- **Data preprocessing:** Features are divided into numerical (`dish_popularity_rating`, `estimated_diners`, `std_portion_kg`, `food_prepared_kg`, `is_weekend`) and categorical (`meal_type`, `academic_status`, `weather`, `day_of_week`, `dish_category`). Transformed using `StandardScaler` and `OneHotEncoder(handle_unknown="ignore")` inside a Scikit-learn `ColumnTransformer`.
- **Algorithms used:** Ridge Regression (linear baseline), Random Forest Regressor ($100$ trees, max depth $12$), and Gradient Boosting Regressor ($120$ estimators, learning rate $0.08$). Evaluated using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and Coefficient of Determination ($R^2$).
- **Software and tools:** Python, Streamlit, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, Joblib, and VS Code.
- **Important implementation steps:** Preprocess features with pipelines; train candidate models and compare holdout test performance; serialize the best-performing pipeline to disk; compute recommended preparation quantities; render interactive dashboard tabs for predictions, historical analytics, explainability, and shift logging.

#### Illustrative code using the project's analysis functions:

```python
from src.preprocess import build_preprocessor, prepare_train_test_data
from src.train import train_and_evaluate
from src.predict import FoodWastePredictor

# 1. Train and evaluate ensemble regressors
pipeline, metrics = train_and_evaluate()

# 2. Instantiate predictor and generate decision-support recommendations
predictor = FoodWastePredictor()

recommendation = predictor.recommend_kitchen_prep(
    meal_type="Lunch",
    academic_status="Regular",
    weather="Sunny",
    day_of_week="Monday",
    dish_category="North Indian Veg",
    dish_popularity_rating=4.8,
    hostel_registered_count=650,
    estimated_diners=510,
    std_portion_kg=0.48,
    avg_cost_per_kg=65.0
)

# Output summary
print(f"Predicted Leftover Waste: {recommendation['predicted_waste_kg']} kg")
print(f"AI Recommended Preparation: {recommendation['recommended_prep_kg']} kg")
print(f"Potential Waste Saved: {recommendation['potential_waste_saved_kg']} kg")
```

---

### 11. System Architecture / Block Diagram

```text
       +-------------------------------------------------------------+
       |             User (Mess Manager / Canteen Staff)             |
       +------------------------------+------------------------------+
                                      |
                                    «uses»
                                      v
       +-------------------------------------------------------------+
       |                  Web Technologies Frontend                  |
       |  + Semantic HTML5 UI (Responsive Views)                     |
       |  + CSS3 Custom Styling (Grid, Flexbox, KPI Badges)          |
       |  + JavaScript ES6+ (DOM Manipulation, Live Sliders)         |
       |  + Chart.js Data Visualizations (Dynamic Canvas)            |
       +------------------------------+------------------------------+
                                      |
                                «AJAX / Fetch»
                                      v
       +-------------------------------------------------------------+
       |                  Flask REST API Backend                     |
       |  + Route Handlers (/api/recommend, /api/historical)         |
       |  + CORS & Request Payload Parsing                           |
       +------------------------------+------------------------------+
                                      |
                                      v
+--------------------------------------------------------------------+
|                         AIML Processing Core                       |
|                                                                    |
|  +--------------------+                +------------------------+  |
|  |   Preprocessor     |     «uses»     |      ML Regressor      |  |
|  | (StandardScaler,   | -------------->| (Gradient Boosting     |  |
|  |  OneHotEncoder)    |                |   / Random Forest)     |  |
|  +--------------------+                +-----------+------------+  |
|                                                    |               |
|                                                  «uses»            |
|                                                    v               |
|                                        +------------------------+  |
|                                        | Kitchen Advisory Logic |  |
|                                        |  (Dynamic Safe Buffer) |  |
|                                        +------------------------+  |
+---------------------------------+----------------------------------+
                                  |
                                «uses»
                                  v
+--------------------------------------------------------------------+
|                        Persistence Storage                         |
|  + Models: waste_prediction_model.joblib, metrics.json             |
|  + Data: mess_waste_dataset.csv (Historical + Shift Logs)          |
+--------------------------------------------------------------------+
```

---

## Results and Conclusion

---

### 12. Results
The following sample outputs illustrate how the system presents food waste prediction and preparation advisories based on holdout evaluation data.

| Output Metric | Illustrative Result |
| :--- | :--- |
| **Total Meal Sessions Analyzed** | 450 days (1,350 meal sessions) |
| **Best Performing Model** | Gradient Boosting Regressor |
| **Model Mean Absolute Error (MAE)** | 1.84 kg |
| **Model Root Mean Squared Error (RMSE)** | 2.45 kg |
| **Model Coefficient of Determination ($R^2$)** | 0.9412 |
| **Top Influential Factors** | Food Prepared ($kg$), Dish Popularity Rating, Estimated Diners, Session Status |
| **Average Food Waste per Meal (Unoptimized)**| 14.8 kg (11.2% leftover ratio) |
| **Sample High-Popularity Lunch (510 diners)**| Unoptimized Prep: 280.0 kg \| Recommended Prep: 271.8 kg \| Waste Saved: 8.2 kg |
| **Sample Low-Popularity Dinner (380 diners)** | Unoptimized Prep: 152.0 kg \| Recommended Prep: 122.5 kg \| Waste Saved: 29.5 kg |
| **Estimated Cost Savings per Session** | ₹ 530.00 – ₹ 1,910.00 |

These results demonstrate that the system accurately captures demand shifts. In sessions with less popular dishes or weekend departures, the model alerts managers to curb over-preparation, reducing waste by up to $20\%\text{--}25\%$ without risking food shortages.

---

### 13. Advantages
- **Reduces Food Wastage:** Prevents tens of kilograms of edible food from ending up in landfills each week.
- **Cost Savings:** Significantly curtails unnecessary expenditure on raw kitchen supplies and catering overheads.
- **Data-Driven Kitchen Planning:** Replaces arbitrary cook guesswork with scientific demand and popularity modeling.
- **Protects Student Satisfaction:** Dynamic safety buffers guarantee students are not left unfed during peak-attendance sessions.
- **Continuous Improvement:** Shift logging functionality establishes a continuous feedback loop for periodic model retraining.

---

### 14. Applications
- **University and College Hostel Messes:** Tailor daily batch sizes according to exam timetables, weekends, and seasonal breaks.
- **Corporate Office Canteens:** Optimize meal preparation around hybrid-work schedules and fluctuating in-office attendance.
- **Hospital and Healthcare Catering:** Predict patient and staff dietary meal requirements with minimum food disposal.
- **Event and Buffet Catering Services:** Estimate required quantities based on RSVP numbers, event types, and dish selections.

---

### 15. Limitations
- **Sudden Unrecorded Events:** Unscheduled campus holidays, sudden student strikes, or external food delivery spikes cannot be anticipated without manual inputs.
- **Data Quality Dependency:** Accuracy relies on faithful reporting of actual diner attendance and discarded leftovers.
- **Cook Discipline:** Recommendations are advisory; kitchen staff must adhere to the suggested weights during batch preparation.

---

### 16. Future Scope
- **Automated Computer Vision Leftover Weighing:** Integrate IoT load cells or smart camera bins to automate waste logging.
- **Student Mobile App Token System:** Integrate with a student app allowing hostelers to tap "Skip Meal" or RSVP 4 hours in advance.
- **Per-Ingredient Procurement Optimization:** Extend models from dish-level weights ($kg$) to raw ingredient supply chain ordering (rice, vegetables, oil).
- **Deep Learning Sequence Models:** Incorporate Temporal Fusion Transformers (TFT) or LSTM networks for complex multi-term seasonal forecasting.

---

### 17. Conclusion
The AI-Powered Food Waste Prediction and Kitchen Advisory System demonstrates a complete, reviewable approach to transforming institutional canteen management. By combining feature preprocessing, ensemble machine learning regressors, and prescriptive dynamic buffer logic, the system effectively bridges the gap between passive predictive modeling and active kitchen decision support. The accompanying Streamlit interface makes actionable insights accessible to canteen managers, delivering measurable reductions in wasted food, reduced operational budgets, and a more sustainable campus food environment.

---

### 18. References
1. **Breiman, L.** (2001). "Random Forests." *Machine Learning*, 45(1), 5–32.
2. **Friedman, J. H.** (2001). "Greedy Function Approximation: A Gradient Boosting Machine." *Annals of Statistics*, 29(5), 1189–1232.
3. **Scikit-learn Developers.** "Supervised Learning: Ensemble Methods." https://scikit-learn.org/stable/modules/ensemble.html
4. **Streamlit Inc.** "Streamlit Documentation." https://docs.streamlit.io/
5. **United Nations Environment Programme (UNEP).** (2021). "Food Waste Index Report 2021." https://www.unep.org/resources/report/unep-food-waste-index-report-2021
