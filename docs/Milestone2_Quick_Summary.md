# Milestone 2: Quick Summary

**Time to read: 5 minutes**

---

## What We Did

| Task | What It Means |
|------|---------------|
| **EDA** | Looked at data, made 8 charts |
| **Feature Engineering** | Created 11 new columns to help ML model |

---

## Script 1: `eda_analysis.py`

### Purpose
Create visualizations to understand data patterns.

### 8 Charts Created

| # | Chart | Key Finding |
|---|-------|-------------|
| 1 | Processing Time Histogram | Average = 11 days, range 2-38 days |
| 2 | Visa Type Bar Chart | Tourist (35%) and Business (25%) most common |
| 3 | Status Pie Chart | 85% approved, 10% rejected, 5% pending |
| 4 | Box Plot by Visa Type | Research slowest (18 days), Medical fastest (4 days) |
| 5 | Correlation Heatmap | Express processing reduces time |
| 6 | Monthly Trends | Peak season = Oct-Mar (tourist season) |
| 7 | Country Analysis | Russia/China take longer to process |
| 8 | Age Distribution | Students youngest, Medical applicants oldest |

### Key Code Concepts

```python
# Histogram - shows distribution of values
sns.histplot(data=df, x='processing_time_days')

# Bar chart - compares categories
ax.bar(visa_counts.index, visa_counts.values)

# Pie chart - shows percentages
ax.pie(values, labels=labels, autopct='%1.1f%%')

# Box plot - shows range and outliers
sns.boxplot(data=df, x='visa_type', y='processing_time_days')

# Heatmap - shows correlations (-1 to +1)
sns.heatmap(corr_matrix, annot=True)
```

---

## Script 2: `feature_engineering.py`

### Purpose
Create new columns that help ML model predict better.

### 11 New Features Created

| Feature | How It's Made | Why Useful |
|---------|---------------|------------|
| `season` | Oct-Mar = Peak, Apr-Sep = Off-Peak | Tourist season affects processing |
| `is_peak_season` | 1 if Peak, 0 if Off-Peak | Binary version for ML |
| `country_avg_processing_time` | Average time for each country | Some countries take longer |
| `country_time_deviation` | Actual - Country average | Shows if faster/slower than usual |
| `visa_type_avg_time` | Average time for each visa type | Baseline expectation |
| `age_group` | Young/Adult/Middle-Aged/Senior | Age patterns |
| `age_group_encoded` | 0/1/2/3 | Numeric version |
| `risk_score` | Sum of risk factors (0-5) | Higher = more risk |
| `expected_processing_time` | Standard time per visa type | What we expect |
| `processing_efficiency` | Actual ÷ Expected | <1 = fast, >1 = slow |
| `efficiency_category` | Fast/Normal/Slow | Categorized efficiency |

### Risk Score Breakdown

| Factor | Points |
|--------|--------|
| Incomplete documents | +2 |
| First time applicant | +1 |
| No sponsor | +1 |
| Low finances (<$10K) | +1 |
| Complex visa type | +1 |
| **Max possible** | **6** |

---

## Final Output

| File | Location | Description |
|------|----------|-------------|
| 8 PNG charts | `reports/figures/` | Visualizations |
| Enhanced dataset | `data/processed/visa_applications_featured.csv` | 48 columns (was 37) |

---

## Commands to Run

```powershell
# Run EDA
python src/eda_analysis.py

# Run Feature Engineering
python src/feature_engineering.py

# View charts
start reports\figures
```

---

## 30-Second Explanation

> "In Milestone 2, I did EDA and Feature Engineering. 
>
> For EDA, I created 8 charts showing that tourist visas are most common, 85% get approved, and average processing is 11 days.
>
> For Feature Engineering, I created 11 new features including seasonal index, country averages, and a risk score. The dataset now has 48 columns ready for ML."

---

*End of Summary*
