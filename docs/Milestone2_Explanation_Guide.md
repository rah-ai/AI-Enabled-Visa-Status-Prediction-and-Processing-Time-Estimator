# Milestone 2: EDA & Feature Engineering - Complete Explanation Guide

**Author:** Rahul 
**Project:** Infosys Springboard Internship  
**Date:** January 2026

---

# Table of Contents

1. [What is Milestone 2?](#what-is-milestone-2)
2. [EDA Analysis Script Explained](#eda-analysis-script-explained)
3. [Feature Engineering Script Explained](#feature-engineering-script-explained)
4. [Output Files](#output-files)
5. [Key Insights Summary](#key-insights-summary)
6. [How to Explain to Coordinator](#how-to-explain-to-coordinator)

---

# What is Milestone 2?

**Two Main Goals:**

1. **Exploratory Data Analysis (EDA)**: Look at the data, create charts, find patterns
2. **Feature Engineering**: Create new columns that will help the machine learning model

**Think of it like:**
- EDA = Looking at a car from all angles before driving it
- Feature Engineering = Adding upgrades to make the car faster

---

# EDA Analysis Script Explained

**File:** `src/eda_analysis.py`

## What This Script Does

This script creates 8 visualizations (charts) to understand the visa data.

---

## Section 1: Imports

```python
import pandas as pd           # Read and work with data tables
import matplotlib.pyplot as plt  # Create basic charts
import seaborn as sns         # Create beautiful charts
```

**Simple Explanation:**
- `pandas` = Excel but in Python
- `matplotlib` = Basic drawing tool for charts
- `seaborn` = Advanced drawing tool (makes prettier charts)

---

## Section 2: Processing Time Distribution (Chart 1)

```python
def plot_processing_time_distribution(df, save_path):
    # Create histogram
    sns.histplot(data=df, x='processing_time_days', bins=30, kde=True)
    
    # Add mean line
    mean_val = df['processing_time_days'].mean()
    ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.1f} days')
```

**What It Shows:**
![Processing Time Distribution](./reports/figures/01_processing_time_distribution.png)

**How to Explain:**
> "This chart shows how visa processing times are distributed. Most visas take around 10-12 days. The red line shows the average."

---

## Section 3: Visa Type Distribution (Chart 2)

```python
def plot_visa_type_distribution(df, save_path):
    visa_counts = df['visa_type'].value_counts()
    ax.bar(visa_counts.index, visa_counts.values)
```

**What It Shows:**
- Bar chart comparing how many applications each visa type gets

**How to Explain:**
> "Tourist visas are most popular (35%), followed by Business visas (25%). This helps us understand what types of visas people usually apply for."

---

## Section 4: Visa Status Pie Chart (Chart 3)

```python
def plot_visa_status_pie(df, save_path):
    status_counts = df['visa_status'].value_counts()
    ax.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
```

**What It Shows:**
- Approved vs Rejected vs Pending percentages

**How to Explain:**
> "About 85% of visa applications get approved, 10% get rejected, and 5% are still pending. This is our target variable that we want to predict."

---

## Section 5: Processing Time by Visa Type (Chart 4)

```python
def plot_processing_time_by_visa_type(df, save_path):
    sns.boxplot(data=df, x='visa_type', y='processing_time_days')
```

**What is a Box Plot?**
```
    Maximum ──┬──
              │
    75% ──────┼────── Upper quartile
              │
    50% ──────┼────── Median (middle value)
              │
    25% ──────┼────── Lower quartile
              │
    Minimum ──┴──
```

**How to Explain:**
> "Different visa types take different times. Research visas take longest (20+ days) because they need more verification. Medical visas are fastest because they're urgent."

---

## Section 6: Correlation Heatmap (Chart 5)

```python
def plot_correlation_heatmap(df, save_path):
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r')
```

**What is Correlation?**
- Correlation measures how two things are related
- Value between -1 and +1
- +1 = When A goes up, B goes up
- -1 = When A goes up, B goes down
- 0 = No relationship

**How to Explain:**
> "This heatmap shows which features are related. We can see that express processing has negative correlation with processing time - meaning express processing makes it faster."

---

## Section 7: Monthly Trends (Chart 6)

```python
def plot_monthly_trends(df, save_path):
    monthly_counts = df.groupby('application_month').size()
    ax.plot(monthly_counts.index, monthly_counts.values, marker='o')
```

**What It Shows:**
- How application volume changes by month
- How processing time changes by month

**How to Explain:**
> "More people apply during winter months (October-March) which is tourist season in India. Processing can be slower during peak times."

---

## Section 8: Country Analysis (Chart 7)

```python
def plot_country_analysis(df, save_path):
    country_counts = df['nationality'].value_counts().head(10)
    ax.barh(country_counts.index, country_counts.values)
```

**What It Shows:**
- Top countries by application volume
- Countries with longest processing times

**How to Explain:**
> "We can see which countries send the most visa applications and which countries take longer to process. This could be due to additional verification requirements."

---

## Section 9: Age Distribution (Chart 8)

```python
def plot_age_distribution(df, save_path):
    sns.violinplot(data=df, x='visa_type', y='applicant_age')
```

**What is a Violin Plot?**
- Like a box plot but shows the shape of data distribution
- Wider parts = more people at that age

**How to Explain:**
> "Student visa applicants are youngest (average 25 years), while Medical visa applicants tend to be older. This makes sense because students are young and medical treatment seekers can be older."

---

# Feature Engineering Script Explained

**File:** `src/feature_engineering.py`

## What is Feature Engineering?

**Simple Definition:** Creating new columns from existing data to help the ML model learn better.

**Analogy:** 
- Original data is like raw ingredients (flour, eggs, sugar)
- Feature engineering is like combining them into a cake mix
- The model can learn better from the cake mix than raw ingredients

---

## Feature 1: Seasonal Index

```python
def create_seasonal_feature(df):
    peak_months = [10, 11, 12, 1, 2, 3]  # Oct to March
    df['season'] = df['application_month'].apply(
        lambda x: 'Peak' if x in peak_months else 'Off-Peak'
    )
    df['is_peak_season'] = (df['season'] == 'Peak').astype(int)
```

**What It Creates:**
| Column | Values | Meaning |
|--------|--------|---------|
| `season` | Peak / Off-Peak | Tourist season or not |
| `is_peak_season` | 1 / 0 | Binary version |

**Why It's Useful:**
- Peak season = more applications = potentially slower processing
- Model can learn this pattern

**How to Explain:**
> "I created a season feature because tourist season in India is October to March. During peak season, there are more applications which might affect processing time."

---

## Feature 2: Country Average Processing Time

```python
def create_country_avg_feature(df):
    country_avg = df.groupby('nationality')['processing_time_days'].mean()
    df['country_avg_processing_time'] = df['nationality'].map(country_avg)
```

**What It Creates:**
| Column | Values | Meaning |
|--------|--------|---------|
| `country_avg_processing_time` | 5.2, 8.5, etc. | Historical avg for that country |
| `country_time_deviation` | -2.3, +1.5, etc. | Difference from country average |

**Why It's Useful:**
- Some countries historically take longer (additional checks)
- If model knows Russia averages 13 days, it can predict better

**How to Explain:**
> "Different countries have different average processing times. For example, Russia takes about 13 days on average. I created a feature that tells the model what the typical processing time is for each country."

---

## Feature 3: Visa Type Average Processing Time

```python
def create_visa_type_avg_feature(df):
    visa_avg = df.groupby('visa_type')['processing_time_days'].mean()
    df['visa_type_avg_time'] = df['visa_type'].map(visa_avg)
```

**What It Creates:**
| Column | Type | Meaning |
|--------|------|---------|
| `visa_type_avg_time` | Float | Average time for that visa type |

**Why It's Useful:**
- Research visas take ~18 days, Medical visas ~4 days
- Gives model a "baseline" for each visa type

**How to Explain:**
> "Similar to country averages, I calculated the average processing time for each visa type. Research visas take longest at 18 days, while Medical visas are fastest at 4 days."

---

## Feature 4: Age Group Buckets

```python
def create_age_group_feature(df):
    bins = [0, 25, 35, 50, 100]
    labels = ['Young', 'Adult', 'Middle-Aged', 'Senior']
    df['age_group'] = pd.cut(df['applicant_age'], bins=bins, labels=labels)
```

**What It Creates:**
| Age Range | Group |
|-----------|-------|
| 0-25 | Young |
| 26-35 | Adult |
| 36-50 | Middle-Aged |
| 51+ | Senior |

**Why It's Useful:**
- Easier for model to learn patterns by age groups
- "Young applicants tend to be students" is simpler than "22-year-olds tend to..."

**How to Explain:**
> "Instead of using exact ages, I grouped applicants into age categories like Young, Adult, Middle-Aged, and Senior. This helps the model identify patterns like 'young people are usually applying for student visas'."

---

## Feature 5: Risk Score

```python
def create_risk_score_feature(df):
    df['risk_score'] = 0
    
    # Incomplete documents = +2 points
    df['risk_score'] += (df['documents_complete'] == 0).astype(int) * 2
    
    # First time applicant = +1 point
    df['risk_score'] += (df['previous_visa'] == 'No').astype(int) * 1
    
    # No sponsor = +1 point
    df['risk_score'] += (df['has_sponsor'] == 0).astype(int) * 1
    
    # Low financial proof = +1 point
    df['risk_score'] += (df['financial_proof_usd'] < 10000).astype(int) * 1
    
    # Complex visa types = +1 point
    df['risk_score'] += df['visa_type'].isin(['Research', 'Employment']).astype(int) * 1
```

**What It Creates:**
| Score | Risk Level | Typical Outcome |
|-------|------------|-----------------|
| 0-1 | Low Risk | Fast processing, likely approval |
| 2-3 | Medium Risk | Normal processing |
| 4-5 | High Risk | Longer processing, possible rejection |

**Why It's Useful:**
- Combines multiple risk factors into one number
- Model can easily learn "high risk = longer processing"

**How to Explain:**
> "I created a risk score that combines multiple factors: incomplete documents (+2), first time applicant (+1), no sponsor (+1), low finances (+1), and complex visa type (+1). Higher score = higher risk of delays or rejection."

---

## Feature 6: Processing Efficiency

```python
def create_processing_efficiency_feature(df):
    expected_times = {
        'Tourist': 5, 'Business': 7, 'Employment': 15, ...
    }
    df['expected_processing_time'] = df['visa_type'].map(expected_times)
    df['processing_efficiency'] = df['processing_time_days'] / df['expected_processing_time']
```

**What It Creates:**
| Column | Meaning |
|--------|---------|
| `expected_processing_time` | Standard time for that visa type |
| `processing_efficiency` | Actual / Expected ratio |
| `efficiency_category` | Fast / Normal / Slow |

**Why It's Useful:**
- Shows if processing was faster or slower than expected
- Model can learn what factors make processing faster/slower

**How to Explain:**
> "I compared actual processing time to the expected time for each visa type. If efficiency is less than 1, it was faster than expected. If more than 1, it was slower. This helps identify unusual cases."

---

# Output Files

## Visualizations Created

| File | Description |
|------|-------------|
| `01_processing_time_distribution.png` | Histogram of processing times |
| `02_visa_type_distribution.png` | Bar chart of visa types |
| `03_visa_status_pie.png` | Pie chart of approval rates |
| `04_processing_by_visa_type.png` | Box plot comparison |
| `05_correlation_heatmap.png` | Feature correlations |
| `06_monthly_trends.png` | Seasonal patterns |
| `07_country_analysis.png` | Country comparisons |
| `08_age_distribution.png` | Age patterns |

## New Dataset Created

| File | Description |
|------|-------------|
| `visa_applications_featured.csv` | Original data + 11 new features |

---

# Key Insights Summary

## Top 5 Insights from EDA:

1. **Processing Time**: Average is 11 days, ranging from 2-38 days
2. **Approval Rate**: 85% of applications are approved
3. **Most Common Visa**: Tourist (35%) and Business (25%)
4. **Document Impact**: Incomplete documents add 5-10 days
5. **Express Processing**: Reduces time by ~5 days on average

## Top 5 New Features:

1. **Season**: Peak vs Off-Peak tourist season
2. **Country Avg**: Historical average for each nationality
3. **Visa Type Avg**: Baseline time for each visa category
4. **Age Group**: Young/Adult/Middle-Aged/Senior
5. **Risk Score**: Combined risk factors (0-5 scale)

---

# How to Explain to Coordinator

## Short Version (2 minutes):

> "For Milestone 2, I performed EDA and Feature Engineering on the visa dataset.
>
> For EDA, I created 8 visualizations including distribution charts, correlation heatmaps, and trend analysis. Key insights: 85% approval rate, average processing time is 11 days, tourist visas are most common.
>
> For Feature Engineering, I created 11 new features including seasonal index, country-specific averages, age groups, and a risk score. These features will help the machine learning model make better predictions.
>
> The dataset now has 48 columns instead of 37, and all code is documented with comments explaining each step."

## Detailed Version (5 minutes):

*Use the sections above to explain each visualization and feature in detail.*

---

# Commands to Run

```bash
# Navigate to project folder
cd "c:\Users\harsh\OneDrive\Desktop\infosys springboard\AI Enabled Visa Status Prediction and Processing Time Estimator"

# Run EDA (creates 8 charts)
python src/eda_analysis.py

# Run Feature Engineering (creates enhanced dataset)
python src/feature_engineering.py
```

---

*End of Milestone 2 Explanation Guide*
