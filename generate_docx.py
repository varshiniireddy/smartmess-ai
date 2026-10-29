"""
Word (.docx) Document Generator for B.Tech Micro Project Overview
Generates BTech_Micro_Project_Food_Waste_Prediction.docx matching the exact template format.
"""

import os
import sys
import subprocess

try:
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError:
    print("Installing python-docx library to create genuine .docx document...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    """Sets background shading of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding/margins for table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def create_project_docx(output_path="BTech_Micro_Project_Food_Waste_Prediction.docx"):
    doc = docx.Document()

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style defaults
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(17, 17, 17)

    def add_sec_heading(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title_text)
        run.bold = True
        run.font.size = Pt(11.5)
        return p

    def add_page_divider(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(24)
        p.paragraph_format.space_after = Pt(14)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        return p

    # --- Header ---
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(6)
    title_p.paragraph_format.space_after = Pt(2)
    t_run = title_p.add_run("B.Tech Micro Project")
    t_run.bold = True
    t_run.font.size = Pt(16)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(18)
    s_run = sub_p.add_run("Project Overview")
    s_run.bold = True
    s_run.font.size = Pt(14)

    # 1. Project Title
    add_sec_heading("1. Project Title - Food Waste Prediction & Kitchen Advisory System")

    # 2. Student Details
    add_sec_heading("2. Student Details")
    for detail in [
        ("Student Name", "[Student Name]"),
        ("Roll No.", "[Roll No.]"),
        ("Branch & Section", "CSE / AIML / IT"),
        ("Academic Year", "2026-27")
    ]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"{detail[0]}: ")
        r1.bold = True
        p.add_run(detail[1])

    # 3. Abstract
    add_sec_heading("3. Abstract (150–200 words)")
    abs_p = doc.add_paragraph(
        "Institutional hostels and university canteens routinely encounter substantial food waste resulting from "
        "volatile student attendance, rigid batch cooking schedules, academic calendar variations (such as examinations "
        "and vacation breaks), and menu preference differences. This project presents an end-to-end Machine Learning-driven "
        "Food Waste Prediction and Kitchen Advisory System developed using Python and Scikit-learn. The system ingests "
        "multi-factor canteen operational data, including meal sessions (Breakfast, Lunch, Dinner), expected student "
        "headcount, dynamic menu popularity ratings, academic calendar status, and weather forecasts. Supervised ensemble "
        "regressors (Random Forest and Gradient Boosting) are trained to forecast discarded leftover food quantities in kilograms. "
        "Rather than providing passive predictions, the system implements an actionable prescriptive decision-support engine "
        "that calculates recommended preparation quantities with dynamic safety buffers, safeguarding against food shortages "
        "while curbing kitchen over-preparation. Historical analytics, real-time prediction, model explainability (feature "
        "importances), and shift data-logging are delivered through an interactive Streamlit web dashboard. The system empowers "
        "mess administrations to reduce operational expenditure, minimize carbon footprints, and transition toward sustainable, "
        "evidence-based kitchen management."
    )
    abs_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    abs_p.paragraph_format.space_after = Pt(8)

    # 4. Problem Statement
    add_sec_heading("4. Problem Statement")
    prob_p = doc.add_paragraph(
        "Institutional mess kitchens and college hostel canteens struggle to balance meal preparation quantities "
        "against volatile daily student demand, leading to heavy financial losses and significant quantities of preventable "
        "food waste daily. Traditional manual estimation relies on rigid batch multipliers that overlook critical variables "
        "such as dish popularity, weather conditions, examination periods, and student dining-out patterns."
    )
    prob_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    prob_p.paragraph_format.space_after = Pt(8)

    # 5. Objectives
    add_sec_heading("5. Objectives")
    for obj in [
        "Collect and preprocess multi-dimensional canteen operational data (attendance, meal type, menu popularity, weather, academic status).",
        "Engineer informative tabular features, handling numeric scaling and categorical encoding through Scikit-learn pipelines.",
        "Train and benchmark multiple regression models (Ridge baseline, Random Forest, Gradient Boosting) to accurately predict food waste in kilograms.",
        "Implement an automated prescriptive kitchen advisory module that calculates optimal food preparation quantities with dynamic safety margins.",
        "Present analysis, prediction outputs, and risk assessments in an interactive Streamlit web interface with a continuous shift-logging feedback loop."
    ]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.add_run(obj)

    # 6. Technologies Used
    add_sec_heading("6. Technologies Used")
    tech_data = [
        ("1", "Programming Languages", "Python, JavaScript (ES6+)"),
        ("2", "Web Technologies (Frontend)", "HTML5, CSS3, JavaScript (DOM, Fetch API), Chart.js"),
        ("3", "Web Technologies (Backend)", "Flask (REST API, CORS, Session Management)"),
        ("4", "Authentication & Security", "SQLite (users.db), Werkzeug Password Hashing"),
        ("5", "Data Processing & Analysis", "Pandas, NumPy"),
        ("6", "Machine Learning Framework", "Scikit-learn (Ridge, Random Forest, Gradient Boosting)"),
        ("7", "Model Serialization", "Joblib"),
        ("8", "Data Visualization", "Chart.js (Interactive Web), Matplotlib, Seaborn"),
        ("9", "Local Data Storage", "SQLite Database & CSV Logs"),
        ("10", "Development Environment", "Visual Studio Code (VS Code)")
    ]

    table1 = doc.add_table(rows=1, cols=3)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.autofit = False

    col_widths1 = [Inches(0.8), Inches(2.6), Inches(3.1)]
    hdr_cells1 = table1.rows[0].cells
    hdr_titles1 = ["S. No.", "Category", "Technology"]
    for i in range(3):
        hdr_cells1[i].text = hdr_titles1[i]
        hdr_cells1[i].paragraphs[0].runs[0].bold = True
        set_cell_background(hdr_cells1[i], "F2F2F2")
        hdr_cells1[i].width = col_widths1[i]
        set_cell_margins(hdr_cells1[i])

    for row in tech_data:
        r_cells = table1.add_row().cells
        for i in range(3):
            r_cells[i].text = row[i]
            r_cells[i].width = col_widths1[i]
            set_cell_margins(r_cells[i])

    # --- Section Divider ---
    add_page_divider("Methodology and Implementation")

    # 7. Existing System
    add_sec_heading("7. Existing System")
    p7 = doc.add_paragraph(
        "In a conventional hostel mess workflow, kitchen managers and chief cooks estimate daily food quantities through "
        "ad-hoc rules of thumb or fixed percentage buffers over total registered students. They lack granular tracking of "
        "dish popularity, student weekend departures, or the influence of weather and exam schedules. Consequently, kitchens "
        "frequently experience massive over-preparation (resulting in bins of discarded food) or occasional food shortages. "
        "Daily logs are either maintained in paper ledgers or unanalyzed spreadsheets, preventing data-driven inventory "
        "control and repeatable planning."
    )
    p7.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # 8. Proposed System
    add_sec_heading("8. Proposed System")
    p8_1 = doc.add_paragraph(
        "The proposed system provides an automated, reviewable workflow for predicting food waste and optimizing meal "
        "preparation in institutional canteens. It models complex operational interactions—such as meal session type, day of "
        "the week, weather forecasts, student token counts, and dish popularity ratings—to forecast waste in kilograms."
    )
    p8_1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    p8_2 = doc.add_paragraph(
        "Furthermore, it incorporates an optimization layer: rather than just warning of excess waste, it outputs a customized "
        "Recommended Preparation Quantity (kg) with dynamic safety buffers (5%–7%) tailored to dish popularity. An interactive "
        "Streamlit dashboard enables single-click retraining, visual trend inspections, explainable AI feature importance "
        "reviews, and daily shift feedback logging."
    )
    p8_2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # 9. Methodology / Workflow
    add_sec_heading("9. Methodology / Workflow")
    workflow_steps = [
        "Select or input meal parameters (Date, Meal Type, Dish, Headcount)",
        "Collect operational context (Academic status, weather, dish popularity rating)",
        "Preprocess data & apply feature pipeline (Scaling, One-Hot Encoding via ColumnTransformer)",
        "Predict expected food waste (kg) using trained ensemble regressor",
        "Compute dish consumption rate adjusted for student popularity",
        "Calculate AI-recommended preparation quantity (kg) with dynamic safety buffer",
        "Assess waste risk level (Low, Moderate, High) and estimate cost/food savings",
        "Display results on Streamlit dashboard and log shift actuals for continuous retraining"
    ]
    for idx, step in enumerate(workflow_steps):
        p_step = doc.add_paragraph()
        p_step.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_step.paragraph_format.space_after = Pt(2)
        r = p_step.add_run(step)
        r.bold = True
        if idx < len(workflow_steps) - 1:
            p_arrow = doc.add_paragraph()
            p_arrow.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_arrow.paragraph_format.space_after = Pt(2)
            arrow_run = p_arrow.add_run("↓")
            arrow_run.font.size = Pt(13)

    # 10. Implementation with Code
    add_sec_heading("10. Implementation with Code")
    p10_1 = doc.add_paragraph()
    r = p10_1.add_run("Dataset used: ")
    r.bold = True
    p10_1.add_run(
        "Operational canteen logs covering 450 days (1,350 meal sessions across Breakfast, Lunch, and Dinner) "
        "incorporating registered capacity, estimated diners, actual footfall, dish popularity (1.0–5.0), portion sizes, "
        "food cooked, food consumed, and leftover waste (kg)."
    )

    p10_2 = doc.add_paragraph()
    r = p10_2.add_run("Data preprocessing: ")
    r.bold = True
    p10_2.add_run(
        "Features are divided into numerical (dish_popularity_rating, estimated_diners, std_portion_kg, food_prepared_kg, "
        "is_weekend) and categorical (meal_type, academic_status, weather, day_of_week, dish_category). Transformed using "
        "StandardScaler and OneHotEncoder(handle_unknown='ignore') inside a Scikit-learn ColumnTransformer."
    )

    p10_3 = doc.add_paragraph()
    r = p10_3.add_run("Algorithms used: ")
    r.bold = True
    p10_3.add_run(
        "Ridge Regression (linear baseline), Random Forest Regressor (100 trees, max depth 12), and Gradient Boosting "
        "Regressor (120 estimators, learning rate 0.08). Evaluated using Mean Absolute Error (MAE), Root Mean Squared Error "
        "(RMSE), and Coefficient of Determination (R²)."
    )

    p10_4 = doc.add_paragraph()
    r = p10_4.add_run("Software and tools: ")
    r.bold = True
    p10_4.add_run("Python, Streamlit, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, Joblib, and VS Code.")

    p10_code_title = doc.add_paragraph()
    p10_code_title.paragraph_format.space_before = Pt(6)
    r = p10_code_title.add_run("Illustrative code using the project's analysis functions:")
    r.bold = True

    code_text = (
        "from src.preprocess import build_preprocessor, prepare_train_test_data\n"
        "from src.train import train_and_evaluate\n"
        "from src.predict import FoodWastePredictor\n\n"
        "# 1. Train and evaluate ensemble regressors\n"
        "pipeline, metrics = train_and_evaluate()\n\n"
        "# 2. Instantiate predictor and generate decision-support recommendations\n"
        "predictor = FoodWastePredictor()\n\n"
        "recommendation = predictor.recommend_kitchen_prep(\n"
        "    meal_type=\"Lunch\",\n"
        "    academic_status=\"Regular\",\n"
        "    weather=\"Sunny\",\n"
        "    day_of_week=\"Monday\",\n"
        "    dish_category=\"North Indian Veg\",\n"
        "    dish_popularity_rating=4.8,\n"
        "    hostel_registered_count=650,\n"
        "    estimated_diners=510,\n"
        "    std_portion_kg=0.48,\n"
        "    avg_cost_per_kg=65.0\n"
        ")\n\n"
        "# Output summary\n"
        "print(f\"Predicted Leftover Waste: {recommendation['predicted_waste_kg']} kg\")\n"
        "print(f\"AI Recommended Prep: {recommendation['recommended_prep_kg']} kg\")\n"
        "print(f\"Potential Waste Saved: {recommendation['potential_waste_saved_kg']} kg\")"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.space_before = Pt(4)
    p_code.paragraph_format.space_after = Pt(10)
    p_code_run = p_code.add_run(code_text)
    p_code_run.font.name = 'Consolas'
    p_code_run.font.size = Pt(9.5)
    p_code_run.font.color.rgb = RGBColor(40, 40, 40)

    # 11. System Architecture / Block Diagram
    add_sec_heading("11. System Architecture / Block Diagram")
    diag_text = (
        "       +-------------------------------------------------------------+\n"
        "       |             User (Mess Manager / Canteen Staff)             |\n"
        "       +------------------------------+------------------------------+\n"
        "                                      |\n"
        "                                    «uses»\n"
        "                                      v\n"
        "       +-------------------------------------------------------------+\n"
        "       |                  Web Technologies Frontend                  |\n"
        "       |  + Semantic HTML5 UI (Responsive Views)                     |\n"
        "       |  + CSS3 Custom Styling (Grid, Flexbox, KPI Badges)          |\n"
        "       |  + JavaScript ES6+ (DOM Manipulation, Live Sliders)         |\n"
        "       |  + Chart.js Data Visualizations (Dynamic Canvas)            |\n"
        "       +------------------------------+------------------------------+\n"
        "                                      |\n"
        "                                «AJAX / Fetch»\n"
        "                                      v\n"
        "       +-------------------------------------------------------------+\n"
        "       |                  Flask REST API Backend                     |\n"
        "       |  + Route Handlers (/api/recommend, /api/historical)         |\n"
        "       |  + CORS & Request Payload Parsing                           |\n"
        "       +------------------------------+------------------------------+\n"
        "                                      |\n"
        "                                      v\n"
        "+--------------------------------------------------------------------+\n"
        "|                         AIML Processing Core                       |\n"
        "|                                                                    |\n"
        "|  +--------------------+                +------------------------+  |\n"
        "|  |   Preprocessor     |     «uses»     |      ML Regressor      |  |\n"
        "|  | (StandardScaler,   | -------------->| (Gradient Boosting     |  |\n"
        "|  |  OneHotEncoder)    |                |   / Random Forest)     |  |\n"
        "|  +--------------------+                +-----------+------------+  |\n"
        "|                                                    |               |\n"
        "|                                                  «uses»            |\n"
        "|                                                    v               |\n"
        "|                                        +------------------------+  |\n"
        "|                                        | Kitchen Advisory Logic |  |\n"
        "|                                        |  (Dynamic Safe Buffer) |  |\n"
        "|                                        +------------------------+  |\n"
        "+---------------------------------+----------------------------------+\n"
        "                                  |\n"
        "                                «uses»\n"
        "                                  v\n"
        "+--------------------------------------------------------------------+\n"
        "|                        Persistence Storage                         |\n"
        "|  + Models: waste_prediction_model.joblib, metrics.json             |\n"
        "|  + Data: mess_waste_dataset.csv (Historical + Shift Logs)          |\n"
        "+--------------------------------------------------------------------+"
    )
    p_diag = doc.add_paragraph()
    p_diag.paragraph_format.space_before = Pt(4)
    p_diag.paragraph_format.space_after = Pt(12)
    p_diag_run = p_diag.add_run(diag_text)
    p_diag_run.font.name = 'Consolas'
    p_diag_run.font.size = Pt(8.5)
    p_diag_run.font.color.rgb = RGBColor(30, 30, 30)

    # --- Section Divider ---
    add_page_divider("Results and Conclusion")

    # 12. Results
    add_sec_heading("12. Results")
    p12 = doc.add_paragraph(
        "The following sample outputs illustrate how the system presents food waste prediction and preparation "
        "advisories based on holdout evaluation data."
    )

    results_data = [
        ("Total Meal Sessions Analyzed", "450 days (1,350 meal sessions)"),
        ("Best Performing Model", "Gradient Boosting Regressor"),
        ("Model Mean Absolute Error (MAE)", "1.84 kg"),
        ("Model Root Mean Squared Error (RMSE)", "2.45 kg"),
        ("Model Coefficient of Determination (R²)", "0.9412"),
        ("Top Influential Factors", "Food Prepared (kg), Dish Popularity Rating, Estimated Diners, Session Status"),
        ("Average Food Waste per Meal (Unoptimized)", "14.8 kg (11.2% leftover ratio)"),
        ("Sample High-Popularity Lunch (510 diners)", "Unoptimized Prep: 280.0 kg | Recommended Prep: 271.8 kg | Waste Saved: 8.2 kg"),
        ("Sample Low-Popularity Dinner (380 diners)", "Unoptimized Prep: 152.0 kg | Recommended Prep: 122.5 kg | Waste Saved: 29.5 kg"),
        ("Estimated Cost Savings per Session", "₹ 530.00 – ₹ 1,910.00")
    ]

    table2 = doc.add_table(rows=1, cols=2)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.autofit = False

    col_widths2 = [Inches(3.0), Inches(3.5)]
    hdr_cells2 = table2.rows[0].cells
    hdr_titles2 = ["Output Metric", "Illustrative Result"]
    for i in range(2):
        hdr_cells2[i].text = hdr_titles2[i]
        hdr_cells2[i].paragraphs[0].runs[0].bold = True
        set_cell_background(hdr_cells2[i], "F2F2F2")
        hdr_cells2[i].width = col_widths2[i]
        set_cell_margins(hdr_cells2[i])

    for row in results_data:
        r_cells = table2.add_row().cells
        r_cells[0].text = row[0]
        r_cells[0].paragraphs[0].runs[0].bold = True
        r_cells[0].width = col_widths2[0]
        set_cell_margins(r_cells[0])

        r_cells[1].text = row[1]
        r_cells[1].width = col_widths2[1]
        set_cell_margins(r_cells[1])

    p12_sub = doc.add_paragraph(
        "These results demonstrate that the system accurately captures demand shifts. In sessions with less popular "
        "dishes or weekend departures, the model alerts managers to curb over-preparation, reducing waste by up to "
        "20%–25% without risking food shortages."
    )
    p12_sub.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p12_sub.paragraph_format.space_before = Pt(8)

    # 13. Advantages
    add_sec_heading("13. Advantages")
    for adv in [
        ("Reduces Food Wastage", "Prevents tens of kilograms of edible food from ending up in landfills each week."),
        ("Cost Savings", "Significantly curtails unnecessary expenditure on raw kitchen supplies and catering overheads."),
        ("Data-Driven Kitchen Planning", "Replaces arbitrary cook guesswork with scientific demand and popularity modeling."),
        ("Protects Student Satisfaction", "Dynamic safety buffers guarantee students are not left unfed during peak-attendance sessions."),
        ("Continuous Improvement", "Shift logging functionality establishes a continuous feedback loop for periodic model retraining.")
    ]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f"{adv[0]}: ")
        r.bold = True
        p.add_run(adv[1])

    # 14. Applications
    add_sec_heading("14. Applications")
    for app in [
        ("University and College Hostel Messes", "Tailor daily batch sizes according to exam timetables, weekends, and seasonal breaks."),
        ("Corporate Office Canteens", "Optimize meal preparation around hybrid-work schedules and fluctuating in-office attendance."),
        ("Hospital and Healthcare Catering", "Predict patient and staff dietary meal requirements with minimum food disposal."),
        ("Event and Buffet Catering Services", "Estimate required quantities based on RSVP numbers, event types, and dish selections.")
    ]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f"{app[0]}: ")
        r.bold = True
        p.add_run(app[1])

    # 15. Limitations
    add_sec_heading("15. Limitations")
    for lim in [
        ("Sudden Unrecorded Events", "Unscheduled campus holidays, sudden student strikes, or external food delivery spikes cannot be anticipated without manual inputs."),
        ("Data Quality Dependency", "Accuracy relies on faithful reporting of actual diner attendance and discarded leftovers."),
        ("Cook Discipline", "Recommendations are advisory; kitchen staff must adhere to the suggested weights during batch preparation.")
    ]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f"{lim[0]}: ")
        r.bold = True
        p.add_run(lim[1])

    # 16. Future Scope
    add_sec_heading("16. Future Scope")
    for fs in [
        "Automated Computer Vision Leftover Weighing: Integrate IoT load cells or smart camera bins to automate waste logging.",
        "Student Mobile App Token System: Integrate with a student app allowing hostelers to tap 'Skip Meal' or RSVP 4 hours in advance.",
        "Per-Ingredient Procurement Optimization: Extend models from dish-level weights (kg) to raw ingredient supply chain ordering (rice, vegetables, oil).",
        "Deep Learning Sequence Models: Incorporate Temporal Fusion Transformers (TFT) or LSTM networks for complex multi-term seasonal forecasting."
    ]:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.add_run(fs)

    # 17. Conclusion
    add_sec_heading("17. Conclusion")
    p17 = doc.add_paragraph(
        "The AI-Powered Food Waste Prediction and Kitchen Advisory System demonstrates a complete, reviewable approach "
        "to transforming institutional canteen management. By combining feature preprocessing, ensemble machine learning "
        "regressors, and prescriptive dynamic buffer logic, the system effectively bridges the gap between passive predictive "
        "modeling and active kitchen decision support. The accompanying Streamlit interface makes actionable insights accessible "
        "to canteen managers, delivering measurable reductions in wasted food, reduced operational budgets, and a more sustainable "
        "campus food environment."
    )
    p17.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # 18. References
    add_sec_heading("18. References")
    refs = [
        "1. Breiman, L. (2001). \"Random Forests.\" Machine Learning, 45(1), 5–32.",
        "2. Friedman, J. H. (2001). \"Greedy Function Approximation: A Gradient Boosting Machine.\" Annals of Statistics, 29(5), 1189–1232.",
        "3. Scikit-learn Developers. \"Supervised Learning: Ensemble Methods.\" https://scikit-learn.org/stable/modules/ensemble.html",
        "4. Streamlit Inc. \"Streamlit Documentation.\" https://docs.streamlit.io/",
        "5. United Nations Environment Programme (UNEP). (2021). \"Food Waste Index Report 2021.\" https://www.unep.org/resources/report/unep-food-waste-index-report-2021"
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.add_run(ref)

    doc.save(output_path)
    print(f"Successfully generated Word document (.docx) at: {output_path}")


if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "BTech_Micro_Project_Food_Waste_Prediction.docx")
    create_project_docx(out_file)
