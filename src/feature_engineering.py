# Feature Engineering Script
# Author: Harsh
# Infosys Springboard Project - Milestone 2
# Creates new features to improve model performance

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


def load_data():
    """Load the cleaned dataset"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'visa_applications_cleaned.csv')
    
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Original shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    return df, base_dir


def create_seasonal_feature(df):
    """
    Feature 1: Seasonal Index
    Peak season (Oct-Mar) vs Off-peak (Apr-Sep)
    Tourist season in India is typically winter months
    """
    print("\n--- Creating Seasonal Feature ---")
    
    # define peak months (tourist season in India: October to March)
    peak_months = [10, 11, 12, 1, 2, 3]
    
    # create season column
    df['season'] = df['application_month'].apply(
        lambda x: 'Peak' if x in peak_months else 'Off-Peak'
    )
    
    # binary encoding
    df['is_peak_season'] = (df['season'] == 'Peak').astype(int)
    
    # check impact on processing time
    peak_time = df[df['is_peak_season'] == 1]['processing_time_days'].mean()
    offpeak_time = df[df['is_peak_season'] == 0]['processing_time_days'].mean()
    
    print(f"  Peak season avg time: {peak_time:.2f} days")
    print(f"  Off-peak avg time: {offpeak_time:.2f} days")
    print(f"  Created: 'season' and 'is_peak_season'")
    
    return df


def create_country_avg_feature(df):
    """
    Feature 2: Country-specific average processing time
    Some countries historically have longer processing times
    """
    print("\n--- Creating Country Average Feature ---")
    
    # calculate average processing time for each country
    country_avg = df.groupby('nationality')['processing_time_days'].mean()
    
    # map to each row
    df['country_avg_processing_time'] = df['nationality'].map(country_avg)
    
    # also create deviation from country average
    df['country_time_deviation'] = df['processing_time_days'] - df['country_avg_processing_time']
    
    # show top 5 countries with highest avg time
    top_countries = country_avg.sort_values(ascending=False).head(5)
    print("  Top 5 countries by avg processing time:")
    for country, time in top_countries.items():
        print(f"    {country}: {time:.2f} days")
    
    print(f"  Created: 'country_avg_processing_time' and 'country_time_deviation'")
    
    return df


def create_visa_type_avg_feature(df):
    """
    Feature 3: Visa type average processing time
    Different visa types have different processing requirements
    """
    print("\n--- Creating Visa Type Average Feature ---")
    
    # calculate average for each visa type
    visa_avg = df.groupby('visa_type')['processing_time_days'].mean()
    
    # map to each row
    df['visa_type_avg_time'] = df['visa_type'].map(visa_avg)
    
    # show averages
    print("  Visa type average times:")
    for vtype, time in visa_avg.sort_values().items():
        print(f"    {vtype}: {time:.2f} days")
    
    print(f"  Created: 'visa_type_avg_time'")
    
    return df


def create_age_group_feature(df):
    """
    Feature 4: Age group buckets
    Categorizes applicants into age groups
    """
    print("\n--- Creating Age Group Feature ---")
    
    # define age bins and labels
    bins = [0, 25, 35, 50, 100]
    labels = ['Young', 'Adult', 'Middle-Aged', 'Senior']
    
    # create age group
    df['age_group'] = pd.cut(df['applicant_age'], bins=bins, labels=labels)
    
    # encode for ML
    age_group_map = {'Young': 0, 'Adult': 1, 'Middle-Aged': 2, 'Senior': 3}
    df['age_group_encoded'] = df['age_group'].map(age_group_map)
    
    # show distribution
    print("  Age group distribution:")
    for group, count in df['age_group'].value_counts().sort_index().items():
        pct = count / len(df) * 100
        print(f"    {group}: {count} ({pct:.1f}%)")
    
    print(f"  Created: 'age_group' and 'age_group_encoded'")
    
    return df


def create_risk_score_feature(df):
    """
    Feature 5: Risk Score
    Combines multiple factors that might affect visa processing/approval
    Higher score = higher risk of longer processing or rejection
    """
    print("\n--- Creating Risk Score Feature ---")
    
    # initialize risk score
    df['risk_score'] = 0
    
    # factor 1: incomplete documents (+2 points)
    df['risk_score'] += (df['documents_complete'] == 0).astype(int) * 2
    
    # factor 2: first time applicant (+1 point)
    df['risk_score'] += (df['previous_visa'] == 'No').astype(int) * 1
    
    # factor 3: no sponsor (+1 point)
    df['risk_score'] += (df['has_sponsor'] == 0).astype(int) * 1
    
    # factor 4: low financial proof (+1 point if below 10000)
    df['risk_score'] += (df['financial_proof_usd'] < 10000).astype(int) * 1
    
    # factor 5: certain visa types are more complex (+1 point)
    complex_visas = ['Research', 'Employment']
    df['risk_score'] += df['visa_type'].isin(complex_visas).astype(int) * 1
    
    # show risk score distribution
    print("  Risk score distribution:")
    for score in sorted(df['risk_score'].unique()):
        count = (df['risk_score'] == score).sum()
        avg_time = df[df['risk_score'] == score]['processing_time_days'].mean()
        print(f"    Score {score}: {count} applications, avg {avg_time:.1f} days")
    
    # calculate correlation with processing time
    corr = df['risk_score'].corr(df['processing_time_days'])
    print(f"  Correlation with processing time: {corr:.3f}")
    
    print(f"  Created: 'risk_score'")
    
    return df


def create_processing_efficiency_feature(df):
    """
    Feature 6: Processing efficiency indicator
    Compares actual time vs expected time based on visa type
    """
    print("\n--- Creating Processing Efficiency Feature ---")
    
    # expected base times (from domain knowledge)
    expected_times = {
        'Tourist': 5, 'Business': 7, 'Employment': 15, 'Student': 12,
        'Medical': 3, 'Conference': 5, 'Research': 20, 'Entry': 4
    }
    
    # map expected time
    df['expected_processing_time'] = df['visa_type'].map(expected_times)
    
    # calculate efficiency ratio
    df['processing_efficiency'] = df['processing_time_days'] / df['expected_processing_time']
    
    # categorize efficiency
    df['efficiency_category'] = pd.cut(df['processing_efficiency'], 
                                        bins=[0, 0.8, 1.2, float('inf')],
                                        labels=['Fast', 'Normal', 'Slow'])
    
    print("  Efficiency distribution:")
    for cat, count in df['efficiency_category'].value_counts().items():
        pct = count / len(df) * 100
        print(f"    {cat}: {count} ({pct:.1f}%)")
    
    print(f"  Created: 'expected_processing_time', 'processing_efficiency', 'efficiency_category'")
    
    return df


def save_featured_data(df, base_dir):
    """Save the dataset with new features"""
    output_path = os.path.join(base_dir, 'data', 'processed', 'visa_applications_featured.csv')
    df.to_csv(output_path, index=False)
    print(f"\nSaved to: {output_path}")
    print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
    return output_path


def print_feature_summary(df, original_cols):
    """Print summary of all new features created"""
    new_cols = [col for col in df.columns if col not in original_cols]
    
    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING SUMMARY")
    print("=" * 60)
    print(f"\nOriginal columns: {len(original_cols)}")
    print(f"New features created: {len(new_cols)}")
    print(f"Total columns: {len(df.columns)}")
    
    print("\nNew features:")
    for i, col in enumerate(new_cols, 1):
        dtype = df[col].dtype
        print(f"  {i}. {col} ({dtype})")
    
    print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("FEATURE ENGINEERING - VISA DATASET")
    print("Infosys Springboard - Milestone 2")
    print("=" * 60)
    
    # load data
    df, base_dir = load_data()
    original_cols = list(df.columns)
    
    # create features one by one
    df = create_seasonal_feature(df)
    df = create_country_avg_feature(df)
    df = create_visa_type_avg_feature(df)
    df = create_age_group_feature(df)
    df = create_risk_score_feature(df)
    df = create_processing_efficiency_feature(df)
    
    # save enhanced dataset
    save_featured_data(df, base_dir)
    
    # print summary
    print_feature_summary(df, original_cols)
    
    print("\nFEATURE ENGINEERING COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
