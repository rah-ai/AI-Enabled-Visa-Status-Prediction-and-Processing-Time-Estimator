# Code Explanation Guide
## AI Enabled Visa Status Prediction - Milestone 1

**Author:** Harsh  
**Project:** Infosys Springboard Internship  
**Date:** January 2026

---

# Table of Contents

1. [Overview](#overview)
2. [generate_synthetic_data.py](#generate_synthetic_datapy)
3. [data_preprocessing.py](#data_preprocessingpy)
4. [Key Concepts Summary](#key-concepts-summary)

---

# Overview

This project has two main Python scripts for Milestone 1:

| Script | Purpose |
|--------|---------|
| `generate_synthetic_data.py` | Creates 2000 fake visa applications with realistic patterns |
| `data_preprocessing.py` | Cleans the data by filling missing values and encoding categories |

Both scripts work together:
```
generate_synthetic_data.py → visa_applications_raw.csv → data_preprocessing.py → visa_applications_cleaned.csv
```

---

# generate_synthetic_data.py

## Purpose
This script generates synthetic (fake but realistic) Indian visa application data. We use synthetic data because real government visa data is difficult to obtain.

---

## Section 1: Imports

```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
```

| Library | What It Does |
|---------|--------------|
| `pandas` | Creates DataFrames (tables) and saves to CSV files |
| `numpy` | Generates random numbers with probability weights |
| `random` | Basic random number generation and random choices |
| `os` | Handles file paths (works on Windows, Mac, Linux) |

---

## Section 2: Random Seed

```python
np.random.seed(42)
random.seed(42)
```

### What is a Random Seed?
- Computers generate "pseudo-random" numbers using an algorithm
- The seed is the starting point for this algorithm
- **Same seed = Same random numbers every time**

### Why Use It?
- **Reproducibility**: If you run the script again, you get the exact same data
- **Testing**: Others can verify your results
- **Debugging**: Easier to find bugs when data is consistent

### Why 42?
- It's a pop culture reference to "The Hitchhiker's Guide to the Galaxy"
- Any number works, 42 is just commonly used

---

## Section 3: Define Possible Values

```python
visa_types = ['Tourist', 'Business', 'Employment', 'Student', 'Medical', 
              'Conference', 'Research', 'Entry']

education_levels = ['10th Pass', '12th Pass', 'Graduate', 'Post Graduate', 'Doctorate']

countries = ['USA', 'UK', 'Germany', 'France', 'Canada', 'Australia', 
             'Japan', 'South Korea', 'China', 'Russia', 'Brazil',
             'Bangladesh', 'Nepal', 'Sri Lanka', 'UAE', 'Singapore',
             'Thailand', 'Malaysia', 'South Africa', 'Italy']
```

These lists define all possible values for each categorical column. When generating data, we randomly pick from these lists.

---

## Section 4: Weighted Random Selection

```python
visa_weights = [0.35, 0.25, 0.12, 0.10, 0.06, 0.04, 0.04, 0.04]
visa_type = np.random.choice(visa_types, p=visa_weights)
```

### What is Weighted Selection?
Instead of each option having equal probability, we assign different probabilities:

| Visa Type | Weight | Meaning |
|-----------|--------|---------|
| Tourist | 0.35 | 35% of applications are Tourist visas |
| Business | 0.25 | 25% are Business visas |
| Employment | 0.12 | 12% are Employment visas |
| Student | 0.10 | 10% are Student visas |
| Medical | 0.06 | 6% are Medical visas |
| Others | 0.04 each | 4% each for Conference, Research, Entry |

### Why Use Weights?
In real life, tourist and business visas are much more common than research visas. This makes our data realistic.

---

## Section 5: Conditional Logic for Age

```python
if visa_type == 'Student':
    age = random.randint(17, 35)      # Students are younger
elif visa_type == 'Employment':
    age = random.randint(22, 55)      # Working professionals
elif visa_type == 'Medical':
    age = random.randint(25, 75)      # Medical can be older
else:
    age = random.randint(20, 70)      # General range
```

### Logic Explanation:
- **Students** (F1 visa): Typically 17-35 years old
- **Employment** (work visa): Must be working age, 22-55
- **Medical** (treatment visa): Can include elderly people
- **Others**: General adult age range

This creates **correlated data** - the age makes sense based on visa type.

---

## Section 6: Processing Time Calculation (Target Variable)

```python
# Base processing times by visa type
base_days = {
    'Tourist': 5, 'Business': 7, 'Employment': 15, 'Student': 12,
    'Medical': 3, 'Conference': 5, 'Research': 20, 'Entry': 4
}
processing_days = base_days[visa_type]
```

### Why Different Base Times?
- **Medical (3 days)**: Urgent, processed quickly
- **Tourist (5 days)**: Simple, fast processing
- **Research (20 days)**: Complex, requires verification
- **Employment (15 days)**: Background checks needed

---

## Section 7: Adjustments to Processing Time

```python
# Express/Tatkal processing
if express_processing:
    processing_days = max(2, processing_days - 3)

# Incomplete documents cause delays
if docs_complete == 0:
    processing_days += random.randint(5, 15)

# Returning visitors processed faster
if prev_visa == 'Yes' and num_prev_visits > 2:
    processing_days -= 1

# Some countries have longer processing
if country in ['China', 'Russia', 'Bangladesh']:
    processing_days += random.randint(2, 5)

# Peak season delays
if app_month in [10, 11, 12, 1, 2, 3] and visa_type == 'Tourist':
    processing_days += random.randint(1, 4)
```

### Adjustment Logic:

| Factor | Effect | Real-World Reason |
|--------|--------|-------------------|
| Express processing | Faster (-3 days) | Paid extra for priority |
| Incomplete docs | Slower (+5-15 days) | Need to request more info |
| Repeat visitors | Faster (-1 day) | Already verified before |
| Certain countries | Slower (+2-5 days) | Additional security checks |
| Peak tourist season | Slower (+1-4 days) | High application volume |

---

## Section 8: Visa Status Decision

```python
approval_prob = 0.82  # Base 82% approval rate

if docs_complete == 0:
    approval_prob -= 0.25   # Incomplete docs: -25%
if prev_visa == 'Yes':
    approval_prob += 0.05   # Previous visa: +5%
if financial_proof > 20000:
    approval_prob += 0.05   # Good finances: +5%
if has_sponsor:
    approval_prob += 0.03   # Has sponsor: +3%

# Final decision
rand_val = random.random()  # Random number 0-1
if rand_val < approval_prob:
    status = 'Approved'
elif rand_val < approval_prob + 0.05:
    status = 'Pending'
else:
    status = 'Rejected'
```

### How Probability Works:
If `approval_prob = 0.85`:
- 85% chance of "Approved"
- 5% chance of "Pending" 
- 10% chance of "Rejected"

---

## Section 9: Introducing Missing Values

```python
def introduce_missing_values(df, missing_pct=0.08):
    for col in cols_for_missing:
        n_missing = int(n_rows * missing_pct * random.uniform(0.4, 0.8))
        missing_idx = random.sample(range(n_rows), n_missing)
        df_copy.loc[missing_idx, col] = np.nan
```

### Why Add Missing Values?
Real-world data ALWAYS has missing values:
- People skip questions on forms
- Data entry errors
- System glitches

By adding ~8% missing values, we can demonstrate how to handle them in preprocessing.

---

# data_preprocessing.py

## Purpose
This script takes the raw data (with missing values and text categories) and converts it into a clean format ready for machine learning.

---

## Section 1: Imports

```python
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
```

### Why `warnings.filterwarnings('ignore')`?
- Pandas sometimes shows warning messages that clutter the output
- These warnings are informational, not errors
- We hide them to keep output clean

---

## Section 2: Analyzing Missing Values

```python
def analyze_missing_values(df):
    missing = df.isnull().sum()           # Count nulls per column
    missing_pct = (missing / len(df)) * 100   # Convert to percentage
```

### Example Output:
```
Column              Missing Count    Missing %
education_level           95           4.75%
financial_proof_usd      112           5.60%
occupation                87           4.35%
```

This tells us which columns need fixing before we can use the data.

---

## Section 3: Handling Missing Values - MEDIAN Imputation

```python
for col in numeric_cols:
    if df_clean[col].isnull().sum() > 0:
        median_val = df_clean[col].median()
        df_clean[col].fillna(median_val, inplace=True)
```

### What is Median?
The middle value when data is sorted.

**Example:**
```
Ages: [22, 25, 28, 30, 35, 40, 45, 50, 55]
Median = 35 (the middle value)

Ages with outlier: [22, 25, 28, 30, 35, 40, 45, 50, 150]
Mean = 47.2 (affected by 150)
Median = 35 (not affected by 150)
```

### Why Median Instead of Mean?
- **Median is robust to outliers**
- One extreme value doesn't skew the result
- Better represents "typical" value

---

## Section 4: Handling Missing Values - MODE Imputation

```python
for col in categorical_cols:
    if df_clean[col].isnull().sum() > 0:
        mode_val = df_clean[col].mode()[0]
        df_clean[col].fillna(mode_val, inplace=True)
```

### What is Mode?
The most frequently occurring value.

**Example:**
```
Education: ['Graduate', 'Graduate', 'PhD', 'Graduate', '12th Pass', null]
Mode = 'Graduate' (appears 3 times)
After filling: ['Graduate', 'Graduate', 'PhD', 'Graduate', '12th Pass', 'Graduate']
```

### Why Mode for Categories?
- Can't calculate mean/median for text
- Most common value is the safest assumption

---

## Section 5: Label Encoding

```python
def label_encode_column(series):
    unique_vals = series.unique()
    mapping = {val: idx for idx, val in enumerate(sorted(unique_vals))}
    return series.map(mapping), mapping
```

### What is Label Encoding?
Converting text categories to numbers.

**Example:**
```
Before: ['Tourist', 'Business', 'Student', 'Tourist', 'Medical']
        
Step 1 - Get unique & sort: ['Business', 'Medical', 'Student', 'Tourist']
Step 2 - Assign numbers:     [0,          1,         2,         3]

After:  [3, 0, 2, 3, 1]
```

### Why Encode?
- Machine learning algorithms only understand numbers
- Text data cannot be used directly in mathematical calculations

---

## Section 6: Ordinal Encoding for Education

```python
edu_order = {
    '10th Pass': 0, 
    '12th Pass': 1, 
    'Graduate': 2, 
    'Post Graduate': 3, 
    'Doctorate': 4
}
df_encoded['education_encoded'] = df_encoded['education_level'].map(edu_order)
```

### What is Ordinal Encoding?
Like label encoding, but **preserves natural order**.

### Why Special Treatment for Education?
Education has a clear hierarchy:
```
10th Pass < 12th Pass < Graduate < Post Graduate < Doctorate
     0    <     1     <    2     <      3        <     4
```

Regular label encoding might assign:
```
10th Pass=0, 12th Pass=1, Doctorate=2, Graduate=3, Post Graduate=4
```
This breaks the logical order!

---

## Section 7: One-Hot Encoding

```python
visa_dummies = pd.get_dummies(df_encoded['visa_type'], prefix='visa_type')
df_encoded = pd.concat([df_encoded, visa_dummies], axis=1)
```

### What is One-Hot Encoding?
Creating separate binary (0/1) columns for each category.

**Before (1 column):**
```
visa_type
---------
Tourist
Business
Student
Tourist
Medical
```

**After (8 columns):**
```
visa_type_Business | visa_type_Medical | visa_type_Student | visa_type_Tourist | ...
        0          |        0          |        0          |        1          |
        1          |        0          |        0          |        0          |
        0          |        0          |        1          |        0          |
        0          |        0          |        0          |        1          |
        0          |        1          |        0          |        0          |
```

### Why Use One-Hot?
With label encoding (Tourist=7, Business=0), the algorithm might think:
- "Tourist (7) is greater than Business (0)"
- "Tourist is 7x more important than Business"

This is **wrong** - these are just categories with no mathematical relationship!

One-hot encoding treats each category as **equally independent**.

---

## Section 8: Target Label Processing

```python
# Processing time - already numeric, just ensure integer type
df_out['processing_time_days'] = df_out['processing_time_days'].astype(int)

# Visa status - encode for classification
status_map = {'Rejected': 0, 'Pending': 1, 'Approved': 2}
df_out['visa_status_encoded'] = df_out['visa_status'].map(status_map)
```

### Two Target Variables:
1. **processing_time_days** (Regression target): Predict exact number of days
2. **visa_status_encoded** (Classification target): Predict category (0, 1, or 2)

---

## Section 9: Main Pipeline

```python
def main():
    # 1. Load raw data
    df = load_data(raw_path)
    
    # 2. Show missing values BEFORE
    analyze_missing_values(df)
    
    # 3. Handle missing values
    df_clean = handle_missing_values(df)
    
    # 4. Encode categorical variables
    df_encoded, enc_maps = encode_categorical_variables(df_clean)
    
    # 5. Process target labels
    df_final = process_target_labels(df_encoded)
    
    # 6. Verify no nulls AFTER
    analyze_missing_values(df_final)
    
    # 7. Save cleaned data
    save_data(df_final, clean_path)
```

### Pipeline Flow:
```
Raw Data (2000 rows, ~8% missing)
         ↓
    Fill Missing Values
         ↓
    Encode Categories
         ↓
    Process Targets
         ↓
Clean Data (2000 rows, 0% missing, all numeric)
```

---

# Key Concepts Summary

## Missing Value Handling

| Data Type | Method | Example |
|-----------|--------|---------|
| Numeric | Median | Age: [25, null, 30] → [25, **27**, 30] |
| Categorical | Mode | Edu: [Grad, null, Grad] → [Grad, **Grad**, Grad] |

## Encoding Methods

| Method | When to Use | Example |
|--------|-------------|---------|
| Label Encoding | Nominal categories | Country: India→0, USA→1 |
| Ordinal Encoding | Ordered categories | Education: 10th→0, PhD→4 |
| One-Hot Encoding | ML algorithms | visa_type → 8 binary columns |

## Why Preprocessing is Important

1. **ML algorithms need numbers** - Can't calculate with text
2. **Missing values cause errors** - Most algorithms crash on nulls
3. **Encoding preserves information** - Categories become usable features
4. **Clean data = Better models** - Garbage in, garbage out

---

# How to Run the Scripts

```bash
# Step 1: Navigate to project folder
cd "c:\Users\harsh\OneDrive\Desktop\infosys springboard\AI Enabled Visa Status Prediction and Processing Time Estimator"

# Step 2: Generate raw data
python src/generate_synthetic_data.py

# Step 3: Preprocess the data
python src/data_preprocessing.py
```

---

# Output Files

| File | Location | Description |
|------|----------|-------------|
| `visa_applications_raw.csv` | data/raw/ | 2000 records with ~8% missing values |
| `visa_applications_cleaned.csv` | data/processed/ | 2000 records, 0 missing, encoded |
| `encoding_mappings.txt` | data/processed/ | Category → Number mappings |
| `data_summary.txt` | reports/ | Statistics and distributions |

---

*End of Code Explanation Guide*

---

# APPENDIX A: Output Files Explained

---

## File 1: encoding_mappings.txt

**Location:** `data/processed/encoding_mappings.txt`

### What is This File?
This file shows how text categories were converted to numbers. It's like a "dictionary" to translate between human-readable text and machine-readable numbers.

### Why Do We Need It?
When we build a prediction model later (Milestone 2), the model will output a number like `7`. We need this file to know that `7` means "Tourist" visa.

---

### Complete Encoding Mappings Explained:

#### Education Level (Ordinal Encoding)
```
education_level:
  0 = 10th Pass
  1 = 12th Pass
  2 = Graduate
  3 = Post Graduate
  4 = Doctorate
```
**Logic:** Numbers preserve order (0 < 1 < 2 < 3 < 4), just like education levels increase.

---

#### Visa Type (Label Encoding - Alphabetical)
```
visa_type:
  0 = Business
  1 = Conference
  2 = Employment
  3 = Entry
  4 = Medical
  5 = Research
  6 = Student
  7 = Tourist
```
**Logic:** Sorted alphabetically. No meaningful order - just for identification.

---

#### Gender
```
gender:
  0 = Female
  1 = Male
```
**Logic:** Simple binary encoding. Alphabetical (F before M).

---

#### Nationality (20 Countries)
```
nationality:
  0 = Australia
  1 = Bangladesh
  2 = Brazil
  3 = Canada
  4 = China
  5 = France
  6 = Germany
  7 = Italy
  8 = Japan
  9 = Malaysia
  10 = Nepal
  11 = Russia
  12 = Singapore
  13 = South Africa
  14 = South Korea
  15 = Sri Lanka
  16 = Thailand
  17 = UAE
  18 = UK
  19 = USA
```
**Logic:** Alphabetical order. If model predicts `19`, we know it's USA.

---

#### Occupation (8 Types)
```
occupation:
  0 = Academic
  1 = Business Owner
  2 = Government Employee
  3 = Homemaker
  4 = Professional
  5 = Retired
  6 = Self Employed
  7 = Student
```

---

#### Processing Center (8 Indian Cities)
```
processing_center:
  0 = Ahmedabad
  1 = Bengaluru
  2 = Chennai
  3 = Hyderabad
  4 = Kolkata
  5 = Mumbai
  6 = New Delhi
  7 = Pune
```

---

#### Visit Purpose (40 Purposes)
```
visit_purpose:
  0 = Academic Conference
  1 = Academic Research
  2 = Beach Holiday
  ...
  30 = Sightseeing
  ...
  38 = Wildlife Safari
  39 = Workshop
```
**Note:** This has **40 unique values** because each visa type has multiple specific purposes.

---

#### Previous Visa
```
previous_visa:
  0 = No
  1 = Yes
```
**Logic:** Binary - either had visa before (1) or not (0).

---

### How to Use This File:

**Example 1: Decoding a Model Prediction**
```python
# Model predicts visa_type_encoded = 7
# Look up: 7 = Tourist
print("Predicted visa type: Tourist")
```

**Example 2: Understanding the Data**
```python
# You see nationality_encoded = 4 in the data
# Look up: 4 = China
# This applicant is from China
```

---

## File 2: data_summary.txt

**Location:** `reports/data_summary.txt`

### What is This File?
A summary report showing key statistics about the cleaned dataset. Used to quickly verify data quality and understand distributions.

---

### Complete Summary Explained:

#### Basic Statistics
```
============================================================
INDIAN VISA APPLICATION DATASET - SUMMARY
============================================================

Total Records: 2000          ← Number of visa applications
Total Columns: 37            ← Original columns + encoded columns
Missing Values: 0            ← Confirms preprocessing worked!
```

---

#### Column Information
```
--- Columns ---
  application_id: object               ← Text (string)
  visa_type: object                    ← Text category
  applicant_age: float64               ← Decimal number (float because of imputation)
  gender: object                       ← Text
  education_level: object              ← Text
  nationality: object                  ← Text
  occupation: object                   ← Text
  processing_center: object            ← Text
  visit_purpose: object                ← Text
  duration_requested_days: int64       ← Whole number
  application_month: int64             ← Whole number (1-12)
  application_year: int64              ← Whole number (2020-2024)
  previous_visa: object                ← Text (Yes/No)
  num_previous_visits: float64         ← Decimal (float because of imputation)
  financial_proof_usd: float64         ← Decimal
  has_sponsor: int64                   ← Binary (0/1)
  documents_complete: float64          ← Binary (float due to imputation)
  express_processing: int64            ← Binary (0/1)
  processing_time_days: int64          ← TARGET 1: Whole number
  visa_status: object                  ← Text (Approved/Rejected/Pending)
```

**Why some are `float64` instead of `int64`?**
When we fill missing values with median, pandas converts to float. Example: median of [1, 2, 3] = 2.0 (float).

---

#### Encoded Columns
```
  education_encoded: int64             ← 0-4
  visa_type_encoded: int64             ← 0-7
  gender_encoded: int64                ← 0-1
  nationality_encoded: int64           ← 0-19
  occupation_encoded: int64            ← 0-7
  processing_center_encoded: int64     ← 0-7
  visit_purpose_encoded: int64         ← 0-39
  previous_visa_encoded: int64         ← 0-1
```

---

#### One-Hot Encoded Columns
```
  visa_type_Business: bool             ← True/False (0/1)
  visa_type_Conference: bool
  visa_type_Employment: bool
  visa_type_Entry: bool
  visa_type_Medical: bool
  visa_type_Research: bool
  visa_type_Student: bool
  visa_type_Tourist: bool
  visa_status_encoded: int64           ← TARGET 2: 0/1/2
```

---

#### Target Variable Statistics
```
--- Target Variable: processing_time_days ---
  Min: 2                  ← Fastest processing (express medical visa)
  Max: 38                 ← Slowest processing
  Mean: 11.10             ← Average is ~11 days
  Std: 6.33               ← Standard deviation (spread of data)
```

**What does Standard Deviation (Std) mean?**
- Most values fall within Mean ± Std
- Mean = 11.10, Std = 6.33
- Most visas processed in 11.10 ± 6.33 = **4.77 to 17.43 days**

---

#### Visa Status Distribution
```
--- Visa Status Distribution ---
  Approved: 1701 (85.0%)     ← 85% of applications approved
  Rejected: 193 (9.7%)       ← ~10% rejected
  Pending: 106 (5.3%)        ← ~5% still pending
```

**Insight:** Our data is **imbalanced** - Approved >> Rejected >> Pending. This is realistic but may need handling in Milestone 2.

---

#### Visa Type Distribution
```
--- Visa Type Distribution ---
  Tourist: 701 (35.0%)       ← Most common
  Business: 497 (24.9%)      ← Second most common
  Employment: 245 (12.2%)
  Student: 202 (10.1%)
  Medical: 114 (5.7%)
  Research: 85 (4.2%)
  Entry: 82 (4.1%)
  Conference: 74 (3.7%)      ← Least common
```

**This matches our weight distribution:**
- Tourist was given 35% weight → got 35% of data ✓
- Business was given 25% weight → got 24.9% of data ✓

---

## File 3: Data Dictionary (data/README.md)

**Location:** `data/README.md`

### What is This File?
A comprehensive documentation of all columns in both raw and cleaned datasets. Essential for:
- Understanding what each column means
- Knowing which preprocessing was applied
- Reference for Milestone 2 model building

---

### Key Sections:

#### Section 1: Raw Dataset Columns
Documents all 20 original columns with:
- Column name
- Data type
- Description
- Example values

#### Section 2: Cleaned Dataset - New Columns
Documents the 17 new columns added during preprocessing:
- 8 label-encoded columns (`*_encoded`)
- 8 one-hot columns (`visa_type_*`)
- 1 target encoding (`visa_status_encoded`)

#### Section 3: Missing Value Handling
Documents which method was used for each column:
```
| Column                | Method Used       |
|-----------------------|-------------------|
| applicant_age         | Median imputation |
| financial_proof_usd   | Median imputation |
| education_level       | Mode imputation   |
| occupation            | Mode imputation   |
```

---

## Summary: When to Use Each File

| File | Use When... |
|------|-------------|
| `encoding_mappings.txt` | Decoding model predictions, understanding encoded values |
| `data_summary.txt` | Checking data quality, understanding distributions |
| `data/README.md` | Understanding column meanings, documenting for others |

---

*End of Appendix A*
