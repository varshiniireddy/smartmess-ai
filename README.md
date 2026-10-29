<div align="center">

# 🍲 SmartMess AI: Food Waste Prediction & Kitchen Advisory System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-green.svg)](https://flask.palletsprojects.com/)
[![Web Tech](https://img.shields.io/badge/Web-HTML5%20%7C%20CSS3%20%7C%20JS-blueviolet.svg)](#-web-technologies-frontend)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![UN SDG](https://img.shields.io/badge/UN%20SDG-12.3%20Food%20Waste-red.svg)](https://www.unep.org/)

**An end-to-end Machine Learning & Web Technologies solution designed for university messes, hostel canteens, and institutional kitchens to predict food wastage, prevent kitchen over-preparation, and optimize raw inventory procurement.**

[Features](#-key-features) • [Architecture](#-system-architecture) • [Mathematical Model](#-mathematical-formulation) • [Quickstart](#-quickstart--execution) • [Demo Accounts](#-demo-accounts) • [License](#-license)

</div>

---

## 📌 Problem Overview

Institutional hostels and catering facilities encounter severe food waste due to erratic student attendance, rigid batch cooking routines, academic calendar disruptions (exams, vacations, long weekends), and dish popularity variances.

**SmartMess AI** solves this problem via a **two-tier intelligence engine**:
1. **Predictive Modeling**: Leverages supervised ensemble regressors (Gradient Boosting & Random Forest) to forecast leftover food waste in kilograms ($kg$) for any planned meal.
2. **Prescriptive Advisory**: Translates predictions into actionable **recommended cooking quantities** with dynamic safety buffers ($5\%\text{--}7\%$) to guarantee students are fed while minimizing discarded leftovers.

---

## ✨ Key Features

* **🤖 Machine Learning Regressors**: Benchmarks Ridge Regression, Random Forest, and Gradient Boosting ($R^2 \approx 0.94$, $\text{MAE} \approx 1.84\text{ kg}$).
* **🍳 Prescriptive Cooking Advisories**: Computes exact cooking quantities ($kg$), waste percentage risk alerts (Low, Moderate, High), and estimated financial savings in $\text{₹}$.
* **🔒 Role-Based Access Control (RBAC)**: Protected behind a secure Authentication Gate with salted password hashing (`werkzeug.security`) and SQLite database storage.
* **🌐 Web Technologies (HTML5 / CSS3 / JavaScript ES6+)**:
  * Semantic HTML5 responsive layout.
  * Custom modern CSS3 styling with glassmorphism card effects and dynamic risk banners.
  * JavaScript asynchronous `fetch()` API integration and dynamic Chart.js canvases.
* **📝 Shift Logging & Continuous Feedback Loop**: Kitchen staff can record actual meal attendance and leftovers to keep the AI model calibrated.

---

## 📐 Mathematical Formulation

### 1. Traditional (Unoptimized) Canteen Preparation
Canteen cooks traditionally prepare for estimated diners with a blanket safety buffer ($\sim 14\%$):
$$Q_{\text{traditional}} = N_{\text{diners}} \times S_{\text{portion}} \times (1 + \beta_{\text{fixed}})$$

### 2. Predicted Waste
The trained ML model predicts discarded leftovers:
$$\widehat{W} = f(\mathbf{X})$$
Where $\mathbf{X}$ represents: meal session, academic status, weather, dish popularity rating ($1.0\text{--}5.0$), portion size, and expected diner count.

### 3. AI-Optimized Preparation Recommendation
To eliminate waste without risking student food shortages:
$$Q_{\text{recommended}} = N_{\text{diners}} \times S_{\text{portion}} \times \mu_{\text{popularity}} \times (1 + \beta_{\text{smart}})$$
* $\mu_{\text{popularity}} = 0.85 + 0.07 \times (\text{Rating} - 2.0)$ accounts for higher intake of favorites and lower intake of less popular dishes.
* $\beta_{\text{smart}}$ is a dynamic safety margin ($5\%$ for popular dishes, $7\%$ for regular dishes).

$$\text{Food Saved (kg)} = \max(0, \, Q_{\text{traditional}} - Q_{\text{recommended}})$$

---

## 🏗️ System Architecture

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
       |  + Route Handlers (/api/recommend, /api/auth, /api/metrics) |
       |  + CORS, Session Management & Request Payload Parsing       |
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
|  + Authentication: data/users.db (SQLite with Salted Hashes)       |
|  + Machine Learning: models/waste_prediction_model.joblib          |
|  + Dataset: data/raw/mess_waste_dataset.csv                        |
+--------------------------------------------------------------------+
```

---

## 📊 Model Evaluation & Benchmarks

Models were evaluated on a holdout test split of 450 operational canteen days ($1,350$ meal sessions):

| Model Architecture | MAE (kg) | RMSE (kg) | $R^2$ Score | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Gradient Boosting Regressor** | **1.84** | **2.45** | **0.9412** | **Selected Best** |
| Random Forest Regressor | 2.12 | 2.88 | 0.9180 | Candidate |
| Ridge Regression (Baseline) | 4.35 | 5.62 | 0.7450 | Baseline |

---

## 📂 Project Directory Structure

```text
food_waste_prediction/
├── templates/
│   └── index.html                     # Semantic HTML5 protected dashboard & auth gate
├── static/
│   ├── css/
│   │   └── style.css                  # Custom responsive CSS3 styling & UI components
│   └── js/
│       └── app.js                     # JavaScript controller (AJAX Fetch & Chart.js)
├── src/
│   ├── __init__.py                    # Package initializer
│   ├── auth.py                        # SQLite user database & password hashing logic
│   ├── preprocess.py                  # Scikit-Learn ColumnTransformer pipeline
│   ├── train.py                       # Multi-model training, evaluation & serialization
│   └── predict.py                     # Inference engine & kitchen prep advisory
├── data/
│   ├── raw/
│   │   └── mess_waste_dataset.csv     # Historical operational canteen records
│   └── generate_data.py               # Synthetic generator modeling mess dynamics
├── models/
│   ├── waste_prediction_model.joblib  # Serialized best ML model pipeline
│   └── metrics.json                   # Model comparison & feature importance
├── server.py                          # Flask REST API Web Server (AIML + Web Tech)
├── app.py                             # Streamlit Web App alternative
├── quickstart.py                      # CLI test script running end-to-end verification
├── generate_docx.py                   # Generates official .docx project report
├── BTech_Micro_Project_Report.md      # Full academic project documentation
├── requirements.txt                   # Project Python dependencies
├── .gitignore                         # Standard git ignore configuration
├── LICENSE                            # MIT License
└── README.md                          # Repository documentation
```

---

## 🚀 Quickstart & Execution

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/food-waste-prediction.git
cd food-waste-prediction
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Launch the Web Application (HTML5 + CSS3 + JS + Flask)
```bash
python server.py
```
Open your browser at **`http://127.0.0.1:5000`**.

### 4. Alternative: Streamlit Dashboard
```bash
python -m streamlit run app.py
```

### 5. CLI Verification Script
```bash
python quickstart.py
```

---

## 🔑 Demo Accounts

The application includes pre-seeded demo accounts in the SQLite database for instant evaluation:

| Role | Username | Password | Access Privileges |
| :--- | :--- | :--- | :--- |
| **🛡️ Mess Manager** | `manager` | `manager123` | Full access, meal predictions, shift logs & ML model retraining |
| **👨‍🍳 Kitchen Staff** | `cook` | `cook123` | Daily meal planning, safety buffer view & shift record logging |

*(You can also use the **Register Account** tab to create brand new user accounts directly in the UI).*

---

## 📄 Academic Project Report

This repository includes a complete **B.Tech Micro Project Overview Report** formatted according to standard university submission templates:
* **Word Document (`.doc`):** [`BTech_Micro_Project_Food_Waste_Prediction.doc`](BTech_Micro_Project_Food_Waste_Prediction.doc)
* **Markdown Document:** [`BTech_Micro_Project_Report.md`](BTech_Micro_Project_Report.md)
* **Generate `.docx` Script:** Run `python generate_docx.py` to compile native Word `.docx` output.

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
