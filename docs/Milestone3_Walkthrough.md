# Milestone 3: Predictive Modeling - Walkthrough

---I trained 3 models - Linear Regression, Decision Tree, and Random Forest. Linear Regression performed best with MAE of 2.52 days (average error only 2.5 days) and 77% accuracy. The model uses the 15 features from Milestone 2 including risk score and seasonal index."

## What We Built

| Script | Purpose |
|--------|---------|
| `src/model_training.py` | Train and compare 3 models |
| `src/predict_demo.py` | Demo how to use saved model |

---

## Model Training Script Summary

### Step 1: Prepare Data
```python
# Load featured dataset (from Milestone 2)
df = pd.read_csv('visa_applications_featured.csv')

# Select 15 features we created
features = ['applicant_age', 'risk_score', 'express_processing', ...]

# Split: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

### Step 2: Train 3 Models
```python
# Model 1: Linear Regression - draw a line
lr = LinearRegression()
lr.fit(X_train, y_train)

# Model 2: Decision Tree - if-else rules
dt = DecisionTreeRegressor(max_depth=10)
dt.fit(X_train, y_train)

# Model 3: Random Forest - many trees combined
rf = RandomForestRegressor(n_estimators=100)
rf.fit(X_train, y_train)
```

### Step 3: Evaluate with Metrics
```python
# Calculate metrics for each model
mae = mean_absolute_error(y_test, y_pred)   # Average error
rmse = mean_squared_error(y_test, y_pred) ** 0.5  # Penalizes big errors
r2 = r2_score(y_test, y_pred)   # Accuracy (0-1)
```

---

## Results

| Model | MAE (Days) | RMSE | R² Score |
|-------|------------|------|----------|
| **Linear Regression** | **2.52** | **3.29** | **0.77** |
| Decision Tree | 3.14 | 4.34 | 0.60 |
| Random Forest | 2.63 | 3.48 | 0.74 |

### 🏆 Best Model: Linear Regression
- **MAE = 2.52 days** → Average error is only 2.5 days!
- **R² = 0.77** → Model explains 77% of the variation

---

## Output Files Created

| File | Description |
|------|-------------|
| `models/best_model.pkl` | Saved model file |
| `models/scaler.pkl` | Feature scaler |
| `reports/figures/model_comparison.png` | Comparison chart |
| `reports/figures/feature_importance.png` | Important features |
| `reports/model_results.csv` | Metrics table |

---

## Prediction Demo

```python
# Load saved model
model = joblib.load('models/best_model.pkl')

# Sample predictions:
Low Risk Application  → 2-3 days
Medium Risk          → 9 days
High Risk            → 29 days
```

---

## Demo Commands

```bash
# Navigate to project
cd "c:\Users\harsh\OneDrive\Desktop\infosys springboard\AI Enabled Visa Status Prediction and Processing Time Estimator"

# Train all models (shows all metrics)
python src/model_training.py

# Show predictions
python src/predict_demo.py

# View comparison chart
start reports\figures\model_comparison.png

# View feature importance
start reports\figures\feature_importance.png
```

---

## Explain to Sir (30 seconds)

> "For Milestone 3, I trained 3 regression models: Linear Regression, Decision Tree, and Random Forest.
>
> I used the 15 features we created in Milestone 2 including risk score, seasonal index, and country averages.
>
> Linear Regression performed best with MAE of 2.52 days - meaning our predictions are off by only 2.5 days on average. The R² score of 0.77 means the model explains 77% of the variation in processing time.
>
> The model is saved and can predict processing time for new applications."

---
