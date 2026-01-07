# Data Dictionary

## Indian Visa Application Dataset

This document describes all columns in the dataset.

---

## Raw Dataset (visa_applications_raw.csv)

Contains 2000 records with intentional missing values (~8%) to simulate real-world data.

### Columns

| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| application_id | String | Unique identifier | IND20200000001 |
| visa_type | Categorical | Type of visa applied for | Tourist, Business, Employment, Student, Medical, Conference, Research, Entry |
| applicant_age | Integer | Age of applicant | 18-75 |
| gender | Categorical | Gender | Male, Female |
| education_level | Categorical | Highest education | 10th Pass, 12th Pass, Graduate, Post Graduate, Doctorate |
| nationality | Categorical | Country of citizenship | USA, UK, Germany, Japan, etc. (20 countries) |
| occupation | Categorical | Job type | Professional, Business Owner, Student, Retired, etc. |
| processing_center | Categorical | Indian city handling application | New Delhi, Mumbai, Chennai, Kolkata, Hyderabad, Bengaluru, Ahmedabad, Pune |
| visit_purpose | Categorical | Specific reason for visit | Sightseeing, Client Meeting, Surgery, etc. |
| duration_requested_days | Integer | Visa duration requested | 30, 60, 90, 180, 365, etc. |
| application_month | Integer | Month of application | 1-12 |
| application_year | Integer | Year of application | 2020-2024 |
| previous_visa | Categorical | Had Indian visa before | Yes, No |
| num_previous_visits | Integer | Number of prior visits | 0-8 |
| financial_proof_usd | Integer | Bank statement amount (USD) | 1000-100000 |
| has_sponsor | Binary | Has sponsoring organization | 0 or 1 |
| documents_complete | Binary | All documents submitted | 0 or 1 |
| express_processing | Binary | Paid for express/tatkal | 0 or 1 |
| processing_time_days | Integer | **TARGET 1**: Days to process | 2-45 |
| visa_status | Categorical | **TARGET 2**: Final decision | Approved, Rejected, Pending |

---

## Cleaned Dataset (visa_applications_cleaned.csv)

Missing values filled, categories encoded. Additional columns:

| New Column | Description |
|------------|-------------|
| education_encoded | 0-4 (ordinal: 10th Pass to Doctorate) |
| visa_type_encoded | 0-7 (label encoded) |
| gender_encoded | 0-1 |
| nationality_encoded | 0-19 |
| occupation_encoded | 0-7 |
| processing_center_encoded | 0-7 |
| visit_purpose_encoded | 0-39 |
| previous_visa_encoded | 0-1 |
| visa_status_encoded | 0=Rejected, 1=Pending, 2=Approved |
| visa_type_Business | One-hot column (0/1) |
| visa_type_Conference | One-hot column (0/1) |
| ... | (one column per visa type) |

---

## Missing Value Handling

| Column | Method Used |
|--------|-------------|
| applicant_age | Median imputation |
| financial_proof_usd | Median imputation |
| num_previous_visits | Median imputation |
| processing_time_days | Median imputation |
| documents_complete | Median imputation |
| education_level | Mode imputation |
| occupation | Mode imputation |

---

## Data Sources

This is a **synthetic dataset** generated to simulate realistic Indian visa applications.
Patterns are based on publicly available information about Indian visa processing.
