# Data Preprocessing Script for Indian Visa Application Dataset
# Author: Harsh
# Infosys Springboard Project - Milestone 1
# Handles missing values, encodes categorical variables, prepares clean data
#section-1
import pandas as pd 
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


def load_data(filepath):
    """Load the raw visa dataset"""
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records with {len(df.columns)} columns")
    return df

#section-2
def analyze_missing_values(df):
    """Check and show missing value stats"""
    print("\n--- Missing Value Analysis ---")
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    missing_info = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Missing %': missing_pct.values
    })
    
    # show only columns with missing values
    missing_info = missing_info[missing_info['Missing Count'] > 0]
    missing_info = missing_info.sort_values('Missing Count', ascending=False)
    
    if len(missing_info) > 0:
        print(missing_info.to_string(index=False))
        print(f"\nTotal missing cells: {df.isnull().sum().sum()}")
    else:
        print("No missing values found!")
    
    return missing_info


def handle_missing_values(df):
    """
    Fill missing values:
    - Numeric cols: median
    - Categorical cols: mode
    """
    print("\n--- Handling Missing Values ---")
    df_clean = df.copy()
    
    # numeric columns
    numeric_cols = ['applicant_age', 'financial_proof_usd', 'num_previous_visits', 
                    'processing_time_days', 'documents_complete']
    
    # categorical columns  
    categorical_cols = ['education_level', 'occupation']
    
    # fill numeric with median-section-3
    for col in numeric_cols:
        if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
            median_val = df_clean[col].median()
            count = df_clean[col].isnull().sum()
            df_clean[col].fillna(median_val, inplace=True)
            print(f"  {col}: filled {count} nulls with median = {median_val:.1f}")
    
    #section-4
    for col in categorical_cols:
        if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
            mode_val = df_clean[col].mode()[0]
            count = df_clean[col].isnull().sum()
            df_clean[col].fillna(mode_val, inplace=True)
            print(f"  {col}: filled {count} nulls with mode = '{mode_val}'")
    
    print("\nMissing value handling done!")
    return df_clean

#section-5
def label_encode_column(series):
   
    unique_vals = series.unique()
    mapping = {val: idx for idx, val in enumerate(sorted(unique_vals))}
    return series.map(mapping), mapping


def encode_categorical_variables(df):
    """
    Encode categorical variables:
    - Label encoding for categories
    - One-hot for visa_type
    """
    print("\n--- Encoding Categorical Variables ---")
    df_encoded = df.copy()
    encodings = {}
    
    # education level has natural order-section-6
    edu_order = {'10th Pass': 0, '12th Pass': 1, 'Graduate': 2, 'Post Graduate': 3, 'Doctorate': 4}
    if 'education_level' in df_encoded.columns:
        df_encoded['education_encoded'] = df_encoded['education_level'].map(edu_order)
        encodings['education_level'] = edu_order
        print(f"  education_level: ordinal encoded (0-4)")
    
    # label encode other categorical columns
    label_cols = ['visa_type', 'gender', 'nationality', 'occupation', 
                  'processing_center', 'visit_purpose', 'previous_visa']
    
    for col in label_cols:
        if col in df_encoded.columns:
            encoded_col, mapping = label_encode_column(df_encoded[col].astype(str))
            df_encoded[f'{col}_encoded'] = encoded_col
            encodings[col] = mapping
            print(f"  {col}: label encoded ({len(mapping)} categories)")
    
    # one-hot encode visa_type-section-7
    if 'visa_type' in df_encoded.columns:
        visa_dummies = pd.get_dummies(df_encoded['visa_type'], prefix='visa_type')
        df_encoded = pd.concat([df_encoded, visa_dummies], axis=1)
        print(f"  visa_type: one-hot encoded ({len(visa_dummies.columns)} new columns)")
    
    print("\nEncoding complete!")
    return df_encoded, encodings


def process_target_labels(df):
    """
    Process target variables:
    - processing_time_days: ensure integer
    - visa_status: encode as numeric
    """
    print("\n--- Processing Target Labels ---")
    df_out = df.copy()
    
    # processing time to integer-section-8
    df_out['processing_time_days'] = df_out['processing_time_days'].astype(int)
    print(f"  processing_time_days: converted to int")
    print(f"    Min: {df_out['processing_time_days'].min()} days")
    print(f"    Max: {df_out['processing_time_days'].max()} days")
    print(f"    Mean: {df_out['processing_time_days'].mean():.1f} days")
    
    # encode visa status
    status_map = {'Rejected': 0, 'Pending': 1, 'Approved': 2}
    df_out['visa_status_encoded'] = df_out['visa_status'].map(status_map)
    print(f"  visa_status: encoded (Rejected=0, Pending=1, Approved=2)")
    
    # show distribution
    print("\n  Status distribution:")
    for status, count in df_out['visa_status'].value_counts().items():
        pct = count / len(df_out) * 100
        print(f"    {status}: {count} ({pct:.1f}%)")
    
    return df_out


def save_data(df, path):
    """Save cleaned data to CSV"""
    df.to_csv(path, index=False)
    print(f"\nSaved to: {path}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")


def generate_summary_report(df, path):
    """Create a summary of the preprocessed data"""
    lines = []
    lines.append("=" * 60)
    lines.append("INDIAN VISA APPLICATION DATASET - SUMMARY")
    lines.append("=" * 60)
    lines.append(f"\nTotal Records: {len(df)}")
    lines.append(f"Total Columns: {len(df.columns)}")
    lines.append(f"Missing Values: {df.isnull().sum().sum()}")
    
    lines.append("\n--- Columns ---")
    for col in df.columns:
        lines.append(f"  {col}: {df[col].dtype}")
    
    lines.append("\n--- Target Variable: processing_time_days ---")
    lines.append(f"  Min: {df['processing_time_days'].min()}")
    lines.append(f"  Max: {df['processing_time_days'].max()}")
    lines.append(f"  Mean: {df['processing_time_days'].mean():.2f}")
    lines.append(f"  Std: {df['processing_time_days'].std():.2f}")
    
    lines.append("\n--- Visa Status Distribution ---")
    for status, count in df['visa_status'].value_counts().items():
        lines.append(f"  {status}: {count} ({count/len(df)*100:.1f}%)")
    
    lines.append("\n--- Visa Type Distribution ---")
    for vtype, count in df['visa_type'].value_counts().items():
        lines.append(f"  {vtype}: {count} ({count/len(df)*100:.1f}%)")
    
    lines.append("\n" + "=" * 60)
    
    report = "\n".join(lines)
    print(report)
    
    with open(path, 'w') as f:
        f.write(report)
    
    return report

#section-9
def main():
    print("=" * 60)
    print("INDIAN VISA DATA PREPROCESSING PIPELINE")
    print("Infosys Springboard - Milestone 1")
    print("=" * 60)
    
    # paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'raw', 'visa_applications_raw.csv')
    clean_path = os.path.join(base_dir, 'data', 'processed', 'visa_applications_cleaned.csv')
    report_path = os.path.join(base_dir, 'reports', 'data_summary.txt')
    encoding_path = os.path.join(base_dir, 'data', 'processed', 'encoding_mappings.txt')
    
    # step 1: load data
    df = load_data(raw_path)
    
    # step 2: analyze missing (before)
    print("\n" + "=" * 40)
    print("BEFORE PREPROCESSING")
    print("=" * 40)
    analyze_missing_values(df)
    
    # step 3: handle missing values
    df_clean = handle_missing_values(df)
    
    # step 4: encode categorical
    df_encoded, enc_maps = encode_categorical_variables(df_clean)
    
    # step 5: process targets
    df_final = process_target_labels(df_encoded)
    
    # step 6: verify no missing
    print("\n" + "=" * 40)
    print("AFTER PREPROCESSING")
    print("=" * 40)
    analyze_missing_values(df_final)
    
    # step 7: save
    save_data(df_final, clean_path)
    
    # step 8: save encodings
    with open(encoding_path, 'w') as f:
        f.write("ENCODING MAPPINGS\n")
        f.write("=" * 40 + "\n\n")
        for name, mapping in enc_maps.items():
            f.write(f"{name}:\n")
            for k, v in sorted(mapping.items(), key=lambda x: x[1]):
                f.write(f"  {v} = {k}\n")
            f.write("\n")
    print(f"\nEncoding mappings saved to: {encoding_path}")
    
    # step 9: summary report
    print("\n" + "=" * 40)
    print("GENERATING SUMMARY REPORT")
    print("=" * 40)
    generate_summary_report(df_final, report_path)
    print(f"\nSummary saved to: {report_path}")
    
    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETE!")
    print("=" * 60)
    print("\nOutput files:")
    print(f"  1. {clean_path}")
    print(f"  2. {report_path}")
    print(f"  3. {encoding_path}")


if __name__ == "__main__":
    main()
