# Script to generate synthetic Indian visa application data
# Author: Harsh
# For Infosys Springboard Project - Milestone 1

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# setting random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_visa_dataset(num_records=2000):
    """
    Generate synthetic Indian visa application data with realistic patterns.
    Based on Indian visa categories and processing requirements.
    """
    
    # Indian visa types
    visa_types = ['Tourist', 'Business', 'Employment', 'Student', 'Medical', 
                  'Conference', 'Research', 'Entry']
    
    education_levels = ['10th Pass', '12th Pass', 'Graduate', 'Post Graduate', 'Doctorate']
    
    # countries that commonly apply for Indian visas
    countries = ['USA', 'UK', 'Germany', 'France', 'Canada', 'Australia', 
                 'Japan', 'South Korea', 'China', 'Russia', 'Brazil',
                 'Bangladesh', 'Nepal', 'Sri Lanka', 'UAE', 'Singapore',
                 'Thailand', 'Malaysia', 'South Africa', 'Italy']
    
    # Indian cities for visa processing
    processing_centers = ['New Delhi', 'Mumbai', 'Chennai', 'Kolkata', 
                          'Hyderabad', 'Bengaluru', 'Ahmedabad', 'Pune']
    
    # purpose of visit details
    visit_purposes = {
        'Tourist': ['Sightseeing', 'Heritage Tour', 'Wildlife Safari', 'Beach Holiday', 'Hill Station'],
        'Business': ['Client Meeting', 'Conference', 'Trade Fair', 'Partnership Discussion', 'Site Visit'],
        'Employment': ['IT Services', 'Manufacturing', 'Consulting', 'Teaching', 'Healthcare'],
        'Student': ['Undergraduate', 'Postgraduate', 'PhD Research', 'Exchange Program', 'Short Course'],
        'Medical': ['Surgery', 'Treatment', 'Consultation', 'Follow-up', 'Check-up'],
        'Conference': ['Tech Summit', 'Business Conference', 'Academic Conference', 'Workshop', 'Seminar'],
        'Research': ['Scientific Study', 'Academic Research', 'Field Work', 'Collaboration', 'Data Collection'],
        'Entry': ['Returning Resident', 'PIO Visit', 'OCI Holder', 'Family Visit', 'Emergency']
    }
    
    occupation_types = ['Professional', 'Business Owner', 'Student', 'Retired', 
                        'Homemaker', 'Government Employee', 'Self Employed', 'Academic']
    
    # lists to store generated data
    data = []
    
    print(f"Generating {num_records} Indian visa application records...")
    
    for i in range(num_records):
        # generate application ID (Indian visa format style)
        app_year = random.randint(2020, 2024)
        app_id = f"IND{app_year}{str(i+1).zfill(7)}"
        
        # randomly select visa type with realistic distribution
        # tourist and business are most common
        visa_weights = [0.35, 0.25, 0.12, 0.10, 0.06, 0.04, 0.04, 0.04]
        visa_type = np.random.choice(visa_types, p=visa_weights)
        
        # generate applicant age based on visa type
        if visa_type == 'Student':
            age = random.randint(17, 35)
        elif visa_type == 'Employment':
            age = random.randint(22, 55)
        elif visa_type == 'Medical':
            age = random.randint(25, 75)
        else:
            age = random.randint(20, 70)
        
        # gender
        gender = random.choice(['Male', 'Female'])
        
        # education level
        if visa_type == 'Student':
            edu_weights = [0.05, 0.30, 0.40, 0.20, 0.05]
        elif visa_type in ['Employment', 'Research']:
            edu_weights = [0.02, 0.08, 0.35, 0.40, 0.15]
        else:
            edu_weights = [0.10, 0.20, 0.40, 0.25, 0.05]
        education = np.random.choice(education_levels, p=edu_weights)
        
        # country of origin
        country = random.choice(countries)
        
        # occupation
        if visa_type == 'Student':
            occupation = 'Student'
        elif visa_type == 'Business':
            occ_weights = [0.30, 0.40, 0.05, 0.05, 0.02, 0.08, 0.08, 0.02]
            occupation = np.random.choice(occupation_types, p=occ_weights)
        else:
            occupation = random.choice(occupation_types)
        
        # processing center
        center = random.choice(processing_centers)
        
        # visit purpose
        purpose = random.choice(visit_purposes[visa_type])
        
        # duration requested (in days)
        if visa_type == 'Tourist':
            duration = random.choice([30, 60, 90, 180])
        elif visa_type == 'Business':
            duration = random.choice([30, 60, 90, 180, 365])
        elif visa_type == 'Employment':
            duration = random.choice([365, 730, 1825])  # 1, 2, or 5 years
        elif visa_type == 'Student':
            duration = random.choice([365, 730, 1095, 1460])  # 1-4 years
        elif visa_type == 'Medical':
            duration = random.choice([30, 60, 90, 180])
        else:
            duration = random.choice([30, 60, 90])
        
        # application month and year
        app_month = random.randint(1, 12)
        
        # previous visa to India
        if age > 35:
            prev_visa = random.choice(['Yes', 'Yes', 'No'])  # older more likely to have visited
        else:
            prev_visa = random.choice(['Yes', 'No', 'No'])
        
        # number of previous visits
        if prev_visa == 'Yes':
            num_prev_visits = random.randint(1, 8)
        else:
            num_prev_visits = 0
        
        # financial proof amount (in USD for standardization)
        if visa_type == 'Employment':
            financial_proof = random.randint(5000, 50000)
        elif visa_type == 'Student':
            financial_proof = random.randint(10000, 80000)
        elif visa_type == 'Business':
            financial_proof = random.randint(3000, 100000)
        else:
            financial_proof = random.randint(1000, 30000)
        
        # sponsorship
        if visa_type in ['Employment', 'Business', 'Conference']:
            has_sponsor = random.choice([1, 1, 1, 0])  # more likely to have sponsor
        elif visa_type == 'Student':
            has_sponsor = random.choice([1, 1, 0])
        else:
            has_sponsor = random.choice([1, 0, 0])
        
        # complete documents submitted
        docs_complete = random.choice([1, 1, 1, 1, 0])  # 80% have complete docs
        
        # express/tatkal processing
        express_processing = random.choice([0, 0, 0, 1])  # 25% opt for express
        
        # calculate processing time (target variable)
        # base times in days by visa type
        base_days = {
            'Tourist': 5, 'Business': 7, 'Employment': 15, 'Student': 12,
            'Medical': 3, 'Conference': 5, 'Research': 20, 'Entry': 4
        }
        
        processing_days = base_days[visa_type]
        
        # factors affecting processing time
        if express_processing:
            processing_days = max(2, processing_days - 3)
        
        if docs_complete == 0:
            processing_days += random.randint(5, 15)  # incomplete docs cause delays
        
        if prev_visa == 'Yes' and num_prev_visits > 2:
            processing_days -= 1  # returning visitors processed faster
        
        # some countries have longer processing
        if country in ['China', 'Russia', 'Bangladesh']:
            processing_days += random.randint(2, 5)
        
        # peak season delays (Oct-Mar is tourist season)
        if app_month in [10, 11, 12, 1, 2, 3] and visa_type == 'Tourist':
            processing_days += random.randint(1, 4)
        
        # add random variation
        processing_days += random.randint(-2, 5)
        processing_days = max(2, min(processing_days, 45))  # keep realistic
        
        # visa status outcome
        approval_prob = 0.82
        
        if docs_complete == 0:
            approval_prob -= 0.25
        if prev_visa == 'Yes':
            approval_prob += 0.05
        if financial_proof > 20000:
            approval_prob += 0.05
        if has_sponsor:
            approval_prob += 0.03
        if education in ['Post Graduate', 'Doctorate']:
            approval_prob += 0.03
        
        approval_prob = min(0.95, max(0.50, approval_prob))
        
        rand_val = random.random()
        if rand_val < approval_prob:
            status = 'Approved'
        elif rand_val < approval_prob + 0.05:
            status = 'Pending'
        else:
            status = 'Rejected'
        
        # create the record
        record = {
            'application_id': app_id,
            'visa_type': visa_type,
            'applicant_age': age,
            'gender': gender,
            'education_level': education,
            'nationality': country,
            'occupation': occupation,
            'processing_center': center,
            'visit_purpose': purpose,
            'duration_requested_days': duration,
            'application_month': app_month,
            'application_year': app_year,
            'previous_visa': prev_visa,
            'num_previous_visits': num_prev_visits,
            'financial_proof_usd': financial_proof,
            'has_sponsor': has_sponsor,
            'documents_complete': docs_complete,
            'express_processing': express_processing,
            'processing_time_days': processing_days,
            'visa_status': status
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    return df


def introduce_missing_values(df, missing_pct=0.08):
    """
    Introduce missing values to simulate real-world data.
    Around 8% missing values in some columns.
    """
    df_copy = df.copy()
    
    # columns that can have missing values
    cols_for_missing = ['applicant_age', 'education_level', 'occupation',
                        'financial_proof_usd', 'num_previous_visits', 'documents_complete']
    
    n_rows = len(df_copy)
    
    for col in cols_for_missing:
        # randomly select rows to make null
        n_missing = int(n_rows * missing_pct * random.uniform(0.4, 0.8))
        missing_idx = random.sample(range(n_rows), n_missing)
        df_copy.loc[missing_idx, col] = np.nan
    
    # add some missing in processing_time_days (incomplete records)
    n_missing_target = int(n_rows * 0.04)
    missing_idx = random.sample(range(n_rows), n_missing_target)
    df_copy.loc[missing_idx, 'processing_time_days'] = np.nan
    
    return df_copy


def main():
    # generate the dataset
    print("=" * 55)
    print("Indian Visa Application Data Generator")
    print("=" * 55)
    
    df = generate_visa_dataset(2000)
    
    print(f"\nGenerated {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    # show visa type distribution
    print("\nVisa Type Distribution:")
    for vtype, count in df['visa_type'].value_counts().items():
        print(f"  {vtype}: {count} ({count/len(df)*100:.1f}%)")
    
    # add missing values
    print("\nIntroducing missing values to simulate real data...")
    df_with_missing = introduce_missing_values(df)
    
    # count missing values
    missing_counts = df_with_missing.isnull().sum()
    print("\nMissing values per column:")
    for col, count in missing_counts.items():
        if count > 0:
            print(f"  {col}: {count} ({count/len(df)*100:.1f}%)")
    
    # save to CSV
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'visa_applications_raw.csv')
    output_path = os.path.normpath(output_path)
    
    df_with_missing.to_csv(output_path, index=False)
    print(f"\nDataset saved to: {output_path}")
    
    # show sample
    print("\nSample records (first 3):")
    print(df_with_missing[['application_id', 'visa_type', 'nationality', 'visa_status', 'processing_time_days']].head(3).to_string())
    
    print("\n" + "=" * 55)
    print("Data generation complete!")
    print("=" * 55)


if __name__ == "__main__":
    main()
