# Exploratory Data Analysis Script
# Author: Harsh
# Infosys Springboard Project - Milestone 2
# This script analyzes the visa dataset and creates visualizations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# set plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def load_data():
    """Load the cleaned dataset"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'visa_applications_cleaned.csv')
    
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    return df, base_dir


def create_output_folder(base_dir):
    """Create folder for saving figures"""
    figures_dir = os.path.join(base_dir, 'reports', 'figures')
    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)
    return figures_dir


def plot_processing_time_distribution(df, save_path):
    """
    Plot 1: Distribution of processing times
    Shows how long visa processing typically takes
    """
    print("\n--- Creating Processing Time Distribution ---")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # histogram with KDE curve
    sns.histplot(data=df, x='processing_time_days', bins=30, kde=True, ax=ax, color='steelblue')
    
    # add mean and median lines
    mean_val = df['processing_time_days'].mean()
    median_val = df['processing_time_days'].median()
    
    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f} days')
    ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.1f} days')
    
    ax.set_xlabel('Processing Time (Days)', fontsize=12)
    ax.set_ylabel('Number of Applications', fontsize=12)
    ax.set_title('Distribution of Visa Processing Times', fontsize=14, fontweight='bold')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '01_processing_time_distribution.png'), dpi=150)
    plt.close()
    
    print(f"  Mean processing time: {mean_val:.1f} days")
    print(f"  Median processing time: {median_val:.1f} days")
    print(f"  Min: {df['processing_time_days'].min()} days, Max: {df['processing_time_days'].max()} days")


def plot_visa_type_distribution(df, save_path):
    """
    Plot 2: Visa type distribution
    Shows which visa types are most common
    """
    print("\n--- Creating Visa Type Distribution ---")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    visa_counts = df['visa_type'].value_counts()
    colors = sns.color_palette("husl", len(visa_counts))
    
    bars = ax.bar(visa_counts.index, visa_counts.values, color=colors)
    
    # add value labels on bars
    for bar, val in zip(bars, visa_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                str(val), ha='center', va='bottom', fontsize=10)
    
    ax.set_xlabel('Visa Type', fontsize=12)
    ax.set_ylabel('Number of Applications', fontsize=12)
    ax.set_title('Distribution of Visa Types', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '02_visa_type_distribution.png'), dpi=150)
    plt.close()
    
    print("  Top 3 visa types:")
    for vtype, count in visa_counts.head(3).items():
        pct = count / len(df) * 100
        print(f"    {vtype}: {count} ({pct:.1f}%)")


def plot_visa_status_pie(df, save_path):
    """
    Plot 3: Visa status pie chart
    Shows approval vs rejection rates
    """
    print("\n--- Creating Visa Status Pie Chart ---")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    status_counts = df['visa_status'].value_counts()
    colors = ['#2ecc71', '#e74c3c', '#f39c12']  # green, red, orange
    
    wedges, texts, autotexts = ax.pie(status_counts.values, 
                                       labels=status_counts.index,
                                       autopct='%1.1f%%',
                                       colors=colors,
                                       explode=(0.02, 0.02, 0.02),
                                       shadow=True,
                                       startangle=90)
    
    # make text bigger
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    ax.set_title('Visa Application Status Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '03_visa_status_pie.png'), dpi=150)
    plt.close()
    
    print("  Status breakdown:")
    for status, count in status_counts.items():
        pct = count / len(df) * 100
        print(f"    {status}: {count} ({pct:.1f}%)")


def plot_processing_time_by_visa_type(df, save_path):
    """
    Plot 4: Box plot of processing times by visa type
    Shows how processing time varies across visa types
    """
    print("\n--- Creating Processing Time by Visa Type ---")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # order by median processing time
    order = df.groupby('visa_type')['processing_time_days'].median().sort_values().index
    
    sns.boxplot(data=df, x='visa_type', y='processing_time_days', order=order, ax=ax, palette='Set2')
    
    ax.set_xlabel('Visa Type', fontsize=12)
    ax.set_ylabel('Processing Time (Days)', fontsize=12)
    ax.set_title('Processing Time by Visa Type', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '04_processing_by_visa_type.png'), dpi=150)
    plt.close()
    
    # print insights
    avg_times = df.groupby('visa_type')['processing_time_days'].mean().sort_values()
    print("  Average processing time by visa type:")
    print(f"    Fastest: {avg_times.index[0]} ({avg_times.iloc[0]:.1f} days)")
    print(f"    Slowest: {avg_times.index[-1]} ({avg_times.iloc[-1]:.1f} days)")


def plot_correlation_heatmap(df, save_path):
    """
    Plot 5: Correlation heatmap
    Shows relationships between numerical features
    """
    print("\n--- Creating Correlation Heatmap ---")
    
    # select numeric columns only
    numeric_cols = ['applicant_age', 'duration_requested_days', 'num_previous_visits',
                    'financial_proof_usd', 'has_sponsor', 'documents_complete',
                    'express_processing', 'processing_time_days', 'visa_status_encoded']
    
    # filter to existing columns
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    corr_matrix = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, 
                fmt='.2f', linewidths=0.5, ax=ax,
                annot_kws={'size': 9})
    
    ax.set_title('Correlation Heatmap of Numerical Features', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '05_correlation_heatmap.png'), dpi=150)
    plt.close()
    
    # find features most correlated with processing time
    proc_corr = corr_matrix['processing_time_days'].drop('processing_time_days').abs().sort_values(ascending=False)
    print("  Top correlations with processing time:")
    for feature, corr in proc_corr.head(3).items():
        print(f"    {feature}: {corr:.3f}")


def plot_monthly_trends(df, save_path):
    """
    Plot 6: Monthly application trends
    Shows seasonal patterns
    """
    print("\n--- Creating Monthly Trends ---")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # monthly application counts
    monthly_counts = df.groupby('application_month').size()
    axes[0].plot(monthly_counts.index, monthly_counts.values, marker='o', linewidth=2, markersize=8)
    axes[0].set_xlabel('Month', fontsize=12)
    axes[0].set_ylabel('Number of Applications', fontsize=12)
    axes[0].set_title('Monthly Application Volume', fontsize=13, fontweight='bold')
    axes[0].set_xticks(range(1, 13))
    axes[0].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    # monthly average processing time
    monthly_avg = df.groupby('application_month')['processing_time_days'].mean()
    axes[1].plot(monthly_avg.index, monthly_avg.values, marker='s', linewidth=2, 
                 markersize=8, color='coral')
    axes[1].set_xlabel('Month', fontsize=12)
    axes[1].set_ylabel('Avg Processing Time (Days)', fontsize=12)
    axes[1].set_title('Average Processing Time by Month', fontsize=13, fontweight='bold')
    axes[1].set_xticks(range(1, 13))
    axes[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '06_monthly_trends.png'), dpi=150)
    plt.close()
    
    # identify peak months
    peak_month = monthly_counts.idxmax()
    slow_month = monthly_avg.idxmax()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    print(f"  Peak application month: {months[peak_month-1]} ({monthly_counts.max()} apps)")
    print(f"  Slowest processing month: {months[slow_month-1]} ({monthly_avg.max():.1f} days avg)")


def plot_country_analysis(df, save_path):
    """
    Plot 7: Country-wise analysis
    Shows top countries by application count and processing time
    """
    print("\n--- Creating Country Analysis ---")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # top 10 countries by applications
    country_counts = df['nationality'].value_counts().head(10)
    axes[0].barh(country_counts.index[::-1], country_counts.values[::-1], color='teal')
    axes[0].set_xlabel('Number of Applications', fontsize=12)
    axes[0].set_title('Top 10 Countries by Application Volume', fontsize=13, fontweight='bold')
    
    # average processing time by country (top 10)
    country_avg = df.groupby('nationality')['processing_time_days'].mean().sort_values(ascending=False).head(10)
    axes[1].barh(country_avg.index[::-1], country_avg.values[::-1], color='salmon')
    axes[1].set_xlabel('Avg Processing Time (Days)', fontsize=12)
    axes[1].set_title('Top 10 Countries by Processing Time', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '07_country_analysis.png'), dpi=150)
    plt.close()
    
    print(f"  Most applications from: {country_counts.index[0]} ({country_counts.iloc[0]})")
    print(f"  Slowest processing for: {country_avg.index[0]} ({country_avg.iloc[0]:.1f} days)")


def plot_age_distribution(df, save_path):
    """
    Plot 8: Age distribution by visa type
    Shows age patterns for different visas
    """
    print("\n--- Creating Age Distribution ---")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # violin plot for age by visa type
    sns.violinplot(data=df, x='visa_type', y='applicant_age', ax=ax, palette='muted')
    
    ax.set_xlabel('Visa Type', fontsize=12)
    ax.set_ylabel('Applicant Age', fontsize=12)
    ax.set_title('Age Distribution by Visa Type', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, '08_age_distribution.png'), dpi=150)
    plt.close()
    
    avg_age = df.groupby('visa_type')['applicant_age'].mean()
    print(f"  Youngest applicants: {avg_age.idxmin()} ({avg_age.min():.1f} years avg)")
    print(f"  Oldest applicants: {avg_age.idxmax()} ({avg_age.max():.1f} years avg)")


def generate_key_insights(df):
    """Print summary of key insights from EDA"""
    
    print("\n" + "=" * 60)
    print("KEY INSIGHTS FROM EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    
    # insight 1: processing time
    print("\n1. PROCESSING TIME INSIGHTS:")
    print(f"   - Average: {df['processing_time_days'].mean():.1f} days")
    print(f"   - 50% of applications processed within {df['processing_time_days'].median():.0f} days")
    print(f"   - Express processing reduces time significantly")
    
    # insight 2: approval rates
    approval_rate = (df['visa_status'] == 'Approved').mean() * 100
    print(f"\n2. APPROVAL RATE: {approval_rate:.1f}%")
    print(f"   - Rejection rate: {(df['visa_status'] == 'Rejected').mean() * 100:.1f}%")
    
    # insight 3: visa types
    top_visa = df['visa_type'].value_counts().index[0]
    print(f"\n3. MOST COMMON VISA TYPE: {top_visa}")
    print(f"   - Makes up {df['visa_type'].value_counts().iloc[0] / len(df) * 100:.1f}% of applications")
    
    # insight 4: document impact
    complete_docs_time = df[df['documents_complete'] == 1]['processing_time_days'].mean()
    incomplete_docs_time = df[df['documents_complete'] == 0]['processing_time_days'].mean()
    print(f"\n4. DOCUMENT COMPLETION IMPACT:")
    print(f"   - Complete docs: {complete_docs_time:.1f} days avg")
    print(f"   - Incomplete docs: {incomplete_docs_time:.1f} days avg")
    
    # insight 5: express processing
    express_time = df[df['express_processing'] == 1]['processing_time_days'].mean()
    normal_time = df[df['express_processing'] == 0]['processing_time_days'].mean()
    print(f"\n5. EXPRESS PROCESSING IMPACT:")
    print(f"   - Express: {express_time:.1f} days avg")
    print(f"   - Normal: {normal_time:.1f} days avg")
    print(f"   - Saves approximately {normal_time - express_time:.1f} days")
    
    print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS - VISA DATASET")
    print("Infosys Springboard - Milestone 2")
    print("=" * 60)
    
    # load data
    df, base_dir = load_data()
    
    # create output folder
    figures_dir = create_output_folder(base_dir)
    print(f"\nSaving figures to: {figures_dir}")
    
    # generate all plots
    plot_processing_time_distribution(df, figures_dir)
    plot_visa_type_distribution(df, figures_dir)
    plot_visa_status_pie(df, figures_dir)
    plot_processing_time_by_visa_type(df, figures_dir)
    plot_correlation_heatmap(df, figures_dir)
    plot_monthly_trends(df, figures_dir)
    plot_country_analysis(df, figures_dir)
    plot_age_distribution(df, figures_dir)
    
    # generate insights summary
    generate_key_insights(df)
    
    print("\n" + "=" * 60)
    print("EDA COMPLETE!")
    print(f"8 visualizations saved to: {figures_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
