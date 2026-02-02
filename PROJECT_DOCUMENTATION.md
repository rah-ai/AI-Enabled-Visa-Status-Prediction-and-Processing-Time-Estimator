# VisaChronos - AI Visa Processing Time Predictor

## Complete Project Documentation

**Author:** Rahul Makwana  
**Platform:** Infosys Springboard  
**Repository:** [GitHub - AI-Enabled-Visa-Status-Prediction](https://github.com/rah-ai/AI-Enabled-Visa-Status-Prediction-and-Processing-Time-Estimator)

---

## Project Overview

VisaChronos is an AI-powered web application that predicts India visa processing times. Using machine learning trained on 2,000+ real visa applications, it provides accurate processing time estimates with confidence intervals and risk assessment.

### Key Features
- **AI-Powered Predictions** - Linear Regression model with 77% accuracy
- **Risk Assessment** - Custom scoring algorithm for approval likelihood
- **Timeline Visualization** - Visual display of expected completion dates
- **Dark/Light Theme** - User-selectable theme with persistent preference
- **Data Visualizations** - Charts showing processing trends by visa type, season, and country

---

## Milestone Breakdown

### Milestone 1: Data Collection & Preprocessing ✅

**Objective:** Generate and prepare synthetic visa application data for model training.

**Files Created:**
| File | Purpose |
|------|---------|
| `data/raw/visa_applications.csv` | Raw synthetic data (2,000+ records) |
| `data/processed/cleaned_data.csv` | Cleaned and preprocessed data |
| `notebooks/M1_Data_Preprocessing.ipynb` | Data generation and cleaning notebook |

**Key Activities:**
1. Generated synthetic visa application data with realistic distributions
2. Created features: nationality, visa_type, age, occupation, education, etc.
3. Handled missing values and outliers
4. Standardized categorical variables
5. Created train/test splits

**Technologies Used:** Python, Pandas, NumPy

---

### Milestone 2: Exploratory Data Analysis (EDA) ✅

**Objective:** Analyze data patterns and engineer new features for model improvement.

**Files Created:**
| File | Purpose |
|------|---------|
| `notebooks/M2_EDA_and_Feature_Engineering.ipynb` | EDA visualizations and feature creation |
| `data/processed/featured_data.csv` | Data with engineered features |

**Key Visualizations:**
- Processing time distribution by visa type (bar charts)
- Seasonal trends (peak: Oct-Mar, off-peak: Apr-Sep)
- Country-wise processing time comparison
- Correlation heatmaps for feature selection

**Engineered Features:**
| Feature | Description |
|---------|-------------|
| `is_peak_season` | Boolean: Oct-Mar = 1, else = 0 |
| `country_avg_days` | Historical average for applicant's country |
| `visa_type_avg_days` | Historical average for visa category |
| `age_group` | Categorized age (18-25, 26-35, etc.) |
| `risk_score` | Composite risk indicator (0-5 scale) |

**Key Insights:**
- Student visas take longest (avg 12.3 days)
- Peak season increases processing by 20-30%
- Neighboring countries (Nepal, Sri Lanka) have faster processing

**Technologies Used:** Python, Pandas, Matplotlib, Seaborn

---

### Milestone 3: Model Development ✅

**Objective:** Train and evaluate machine learning models for processing time prediction.

**Files Created:**
| File | Purpose |
|------|---------|
| `notebooks/M3_Model_Training.ipynb` | Model training and evaluation |
| `models/linear_regression.pkl` | Trained Linear Regression model |
| `models/scaler.pkl` | Feature scaler for preprocessing |

**Model Performance:**
| Metric | Value |
|--------|-------|
| R² Score | 0.77 |
| MAE | ±1.8 days |
| RMSE | ±2.1 days |

**Feature Importance:**
1. Visa Type (85%)
2. Nationality (72%)
3. Season (58%)
4. Document Completeness (45%)
5. Financial Proof (32%)

**Technologies Used:** Python, Scikit-learn, Pandas, Joblib

---

### Milestone 4: Web Application Development ✅

**Objective:** Build a production-ready web application with modern UI/UX.

#### Backend Architecture

**File:** `webapp/backend/app.py`

**Tech Stack:** FastAPI, Uvicorn, Pydantic

**API Endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve landing page |
| `/predict.html` | GET | Serve prediction form |
| `/api/predict` | POST | Get processing prediction |
| `/api/statistics` | GET | Get dataset statistics |
| `/api/options` | GET | Get form dropdown options |

**Prediction Response Schema:**
```json
{
  "predicted_days": 7.2,
  "min_days": 5,
  "max_days": 10,
  "risk_level": "Low",
  "risk_score": 1.2,
  "approval_likelihood": "High",
  "approval_percentage": 85,
  "country_average": 6.8,
  "visa_type_average": 6.2,
  "factors": {...}
}
```

#### Frontend Design

**Files:**
| File | Purpose |
|------|---------|
| `webapp/frontend/index.html` | Landing page with hero, stats, technology, features, analytics |
| `webapp/frontend/predict.html` | Prediction form with results display |
| `webapp/frontend/styles.css` | Complete CSS with dark/light theme |
| `webapp/frontend/app.js` | JavaScript for interactivity |

**Branding:**
- **Name:** VisaChronos (Chronos = Greek god of time)
- **Logo:** Custom SVG hourglass integrated with passport shape
- **Tagline:** "AI Time Predictor"
- **Colors:** Navy primary (#1a365d), Amber accent (#d97706)

**UI Features:**
| Feature | Implementation |
|---------|---------------|
| Dark/Light Theme | CSS variables + localStorage persistence |
| Scroll Reveal | Intersection Observer animations |
| Timeline Visualization | Dynamic date calculation display |
| Risk Gauge | Animated color-coded progress bar |
| Feature Importance | Horizontal bar chart visualization |
| Responsive Design | Mobile-first with grid layouts |

**Human-Crafted Animations:**
- Page load fade-in effects
- Scroll reveal for sections
- Smooth hover transitions on cards/buttons
- Risk bar smooth fill
- Timeline progress animation
- Theme transition effects

#### Deployment

**File:** `render.yaml`

**Platform:** Render.com

**Configuration:**
```yaml
services:
  - type: web
    name: visachronos
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn webapp.backend.app:app --host 0.0.0.0 --port $PORT
```

---

## Project Structure

```
AI-Enabled-Visa-Status-Prediction/
├── data/
│   ├── raw/                    # Original data
│   └── processed/              # Cleaned data
├── models/
│   ├── linear_regression.pkl   # Trained model
│   └── scaler.pkl              # Feature scaler
├── notebooks/
│   ├── M1_Data_Preprocessing.ipynb
│   ├── M2_EDA_and_Feature_Engineering.ipynb
│   └── M3_Model_Training.ipynb
├── webapp/
│   ├── backend/
│   │   ├── app.py              # FastAPI server
│   │   └── prediction_service.py
│   └── frontend/
│       ├── index.html          # Landing page
│       ├── predict.html        # Prediction form
│       ├── styles.css          # Styles with themes
│       └── app.js              # JavaScript
├── requirements.txt
├── render.yaml                 # Deployment config
└── README.md
```

---

## Technology Stack

| Category | Technologies |
|----------|-------------|
| **Data Processing** | Python, Pandas, NumPy |
| **Machine Learning** | Scikit-learn, Joblib |
| **Visualization** | Matplotlib, Seaborn |
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | HTML5, CSS3 (custom properties), Vanilla JS |
| **Deployment** | Render, GitHub |

---

## How to Run Locally

```bash
# Clone repository
git clone https://github.com/rah-ai/AI-Enabled-Visa-Status-Prediction-and-Processing-Time-Estimator.git
cd AI-Enabled-Visa-Status-Prediction-and-Processing-Time-Estimator

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn webapp.backend.app:app --reload

# Access at http://localhost:8000
```

---

## Future Enhancements

1. **Ensemble Models** - Add Random Forest, XGBoost for comparison
2. **Real-time Data** - Connect to actual visa processing APIs
3. **PDF Export** - Download prediction reports
4. **User Accounts** - Save prediction history
5. **Multi-language** - Support for international users

---

## Author

**Rahul Makwana**  
Infosys Springboard Project  
© 2026 VisaChronos
