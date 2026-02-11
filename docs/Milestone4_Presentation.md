# Milestone 4 — Presentation Talking Points
## VisaChronos — AI Visa Processing Time Estimator
**Rahul Makwana | Infosys Springboard | Feb 10, 2026**

---

## 🗣️ Opening Statement

> "This is **VisaChronos** — an AI-powered web app that predicts how long it takes to process an India visa. It uses a **Linear Regression model trained on 2,000+ records** with **77% accuracy**. It supports **45+ countries** and **7 visa types**."

---

## 🛠️ Tech Stack (Mention While Opening)

- **Backend:** FastAPI (Python) — serves API + static files
- **ML Model:** Scikit-learn Linear Regression, saved with Joblib
- **Frontend:** HTML5, CSS3, Vanilla JavaScript — no frameworks
- **Styling:** CSS Variables for dark/light theme, 3,286 lines of CSS
- **Data:** Pandas, NumPy for preprocessing; Matplotlib, Seaborn for EDA
- **Deployment:** Render.com + GitHub

---

## Screen 1: Homepage (`index.html`)

**What to show:** Scroll slowly from top to bottom

**Say this:**
- "This is our landing page with the **VisaChronos branding** — custom SVG logo with clock + V element"
- "Here's the **hero section** — gradient background, CTA buttons to go to prediction or visa info"
- "**Stats bar** shows our key numbers — 2,000+ applications analyzed, 77% accuracy, 15+ ML features, 45+ countries"
- "**Technology section** — explains we use Linear Regression with 15+ engineered features"
- "**Features section** — 6 cards showing key capabilities like risk assessment, timeline prediction"
- "These are **3 interactive bar charts** — processing time by visa type, by season, and by nationality"
- "**Dark/light theme toggle** — click the moon icon — uses CSS variables so entire theme changes instantly, saved in localStorage"

---

## Screen 2: Prediction Page (`predict.html`)

**What to show:** Fill the form and submit

**Say this:**
- "This is the **prediction form** — user selects nationality, visa type, age, previous visits, etc."
- "**12 input fields** — all validated by Pydantic on the backend (age must be 18–100, etc.)"
- "When I click **Get Estimate**, it sends a POST request to `/api/predict`"
- "The backend runs the ML model — loads `best_model.pkl`, encodes features, scales them, and predicts"

**After result loads, say:**
- "Here's the **predicted days** with min/max range"
- "This **risk gauge** — animated bar that turns green/amber/red based on our risk score algorithm (0–5 scale)"
- "**Approval likelihood** — calculated from risk: low risk = 85% approval, medium = 70%, high = 50%"
- "**Feature importance chart** — shows visa type matters most (85%), then nationality (72%), season (58%)"
- "**Timeline visualization** — shows application date → expected completion → latest date"
- "**Comparison chart** — compares your estimate vs visa type average vs country average"
- "This **PDF export button** — lets you download the report"
- "**Prediction history** at the bottom — auto-saves last 10 predictions in localStorage"

---

## Screen 3: Country Comparison (`compare.html`)

**What to show:** Select 2–3 countries, click Compare

**Say this:**
- "This page lets you **compare processing times across countries**"
- "Select 2 to 4 countries — I'll pick USA, Japan, and China"
- "Click Compare — it shows an **animated bar chart** with average days"
- "Below that, a **detailed table** — avg, min, max days, risk level, peak season"
- "**Key insights panel** — auto-calculates fastest country, slowest, time difference, risk distribution"

---

## Screen 4: Visa Info Page (`visa-info.html`)

**What to show:** Scroll through the page

**Say this:**
- "This is our **visa documentation page** — links to official Indian visa portals"
- "**6 visa categories** — Tourist, Business, Student, Medical, Employment, Conference — each with duration and processing info"
- "**45 country cards** — organized by region (Americas, Europe, Asia Pacific, South Asia, Middle East & Africa)"
- "Each card shows flag, country name, average processing time, and direct link to Indian Embassy website"

---

## 🗣️ Backend Code Walkthrough (If Asked)

**Open `app.py` and say:**
- "`VisaApplication` class — Pydantic model that validates all 12 input fields with type checking"
- "`PredictionResponse` — defines exact JSON structure returned to frontend"
- "`/api/predict` endpoint — converts input to dict, calls prediction service, returns result"
- "CORS middleware allows frontend-backend communication"

**Open `prediction_service.py` and say:**
- "Loads trained model and scaler using Joblib on startup (singleton pattern)"
- "`_setup_encodings()` — maps text categories (USA, Tourist) to numbers for the model"
- "`calculate_risk_score()` — custom formula: incomplete docs +2, first-time +1, no sponsor +1, low funds +1"
- "`predict()` method — builds 15-feature vector → scales → predicts → calculates confidence interval (±15% or ±2 days)"

---

## 🗣️ Closing Statement

> "So to summarize — across 4 milestones we went from **raw data → EDA → trained ML model → full-stack web app**. The model has **77% accuracy**, the app has **4 pages, 5+ API endpoints, dark/light theme, interactive charts, PDF export, and prediction history**. Built with **Python, FastAPI, Scikit-learn, HTML, CSS, and JavaScript**."

---

## Quick Reference — Key Numbers

| What | Value |
|------|-------|
| Countries | 45+ |
| Visa Types | 7 |
| ML Features | 15+ |
| Training Data | 2,000+ records |
| Accuracy (R²) | 77% |
| Error | ±2.1 days |
| Pages | 4 |
| API Endpoints | 5+ |
| CSS Lines | 3,286 |
| Themes | Light + Dark |
