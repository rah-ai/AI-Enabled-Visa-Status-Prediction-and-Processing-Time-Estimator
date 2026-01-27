# Model Training Script
# Author: Harsh
# Infosys Springboard Project - Milestone 3
# Trains regression models to predict visa processing time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')


def load_data():
    """Load the featured dataset"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'processed', 'visa_applications_featured.csv')
    
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    return df, base_dir


def prepare_features(df):
    """
    Select and prepare features for modeling.
    We use the engineered features we created in Milestone 2.
    """
    print("\n--- Preparing Features ---")
    
    # features to use for prediction
    feature_cols = [
        'applicant_age',
        'duration_requested_days',
        'num_previous_visits',
        'financial_proof_usd',
        'has_sponsor',
        'documents_complete',
        'express_processing',
        'is_peak_season',
        'education_encoded',
        'visa_type_encoded',
        'nationality_encoded',
        'occupation_encoded',
        'risk_score',
        'country_avg_processing_time',
        'visa_type_avg_time'
    ]
    
    # filter to available columns
    available_cols = [col for col in feature_cols if col in df.columns]
    print(f"Using {len(available_cols)} features:")
    for col in available_cols:
        print(f"  - {col}")
    
    # target variable
    target_col = 'processing_time_days'
    
    X = df[available_cols]
    y = df[target_col]
    
    return X, y, available_cols


def split_data(X, y):
    """Split data into training (80%) and testing (20%) sets"""
    print("\n--- Splitting Data ---")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Testing set: {len(X_test)} samples")
    
    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test):
    """Standardize features for better model performance"""
    print("\n--- Scaling Features ---")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Features standardized (mean=0, std=1)")
    
    return X_train_scaled, X_test_scaled, scaler


def train_models(X_train, y_train):
    """Train multiple regression models"""
    print("\n--- Training Models ---")
    
    models = {}
    
    # Model 1: Linear Regression
    print("\n1. Training Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    models['Linear Regression'] = lr_model
    print("   Done!")
    
    # Model 2: Decision Tree
    print("\n2. Training Decision Tree...")
    dt_model = DecisionTreeRegressor(max_depth=10, random_state=42)
    dt_model.fit(X_train, y_train)
    models['Decision Tree'] = dt_model
    print("   Done!")
    
    # Model 3: Random Forest
    print("\n3. Training Random Forest...")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)
    models['Random Forest'] = rf_model
    print("   Done!")
    
    return models


def evaluate_models(models, X_test, y_test):
    """Evaluate all models and compare performance"""
    print("\n--- Evaluating Models ---")
    
    results = []
    
    for name, model in models.items():
        # make predictions
        y_pred = model.predict(X_test)
        
        # calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            'Model': name,
            'MAE': mae,
            'RMSE': rmse,
            'R2 Score': r2
        })
        
        print(f"\n{name}:")
        print(f"  MAE: {mae:.2f} days (average error)")
        print(f"  RMSE: {rmse:.2f} days")
        print(f"  R² Score: {r2:.4f} ({r2*100:.1f}% accuracy)")
    
    results_df = pd.DataFrame(results)
    return results_df


def plot_model_comparison(results_df, save_path):
    """Create comparison visualization"""
    print("\n--- Creating Comparison Chart ---")
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    # MAE comparison
    axes[0].bar(results_df['Model'], results_df['MAE'], color=colors)
    axes[0].set_ylabel('MAE (Days)')
    axes[0].set_title('Mean Absolute Error\n(Lower is Better)')
    axes[0].tick_params(axis='x', rotation=15)
    for i, v in enumerate(results_df['MAE']):
        axes[0].text(i, v + 0.1, f'{v:.2f}', ha='center', fontsize=10)
    
    # RMSE comparison
    axes[1].bar(results_df['Model'], results_df['RMSE'], color=colors)
    axes[1].set_ylabel('RMSE (Days)')
    axes[1].set_title('Root Mean Squared Error\n(Lower is Better)')
    axes[1].tick_params(axis='x', rotation=15)
    for i, v in enumerate(results_df['RMSE']):
        axes[1].text(i, v + 0.1, f'{v:.2f}', ha='center', fontsize=10)
    
    # R2 comparison
    axes[2].bar(results_df['Model'], results_df['R2 Score'], color=colors)
    axes[2].set_ylabel('R² Score')
    axes[2].set_title('R² Score\n(Higher is Better)')
    axes[2].set_ylim(0, 1)
    axes[2].tick_params(axis='x', rotation=15)
    for i, v in enumerate(results_df['R2 Score']):
        axes[2].text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=10)
    
    plt.suptitle('Model Performance Comparison', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Chart saved to: {save_path}")


def plot_feature_importance(model, feature_names, save_path):
    """Plot feature importance from Random Forest"""
    print("\n--- Generating Feature Importance ---")
    
    importance = model.feature_importances_
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance
    }).sort_values('Importance', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(importance_df)))
    ax.barh(importance_df['Feature'], importance_df['Importance'], color=colors)
    ax.set_xlabel('Importance Score')
    ax.set_title('Feature Importance (Random Forest)\nWhat factors affect processing time most?', 
                 fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Chart saved to: {save_path}")
    
    # print top 5 features
    print("\nTop 5 Most Important Features:")
    top5 = importance_df.tail(5)[::-1]
    for idx, row in top5.iterrows():
        print(f"  {row['Feature']}: {row['Importance']:.4f}")


def save_best_model(models, results_df, scaler, base_dir):
    """Save the best performing model"""
    print("\n--- Saving Best Model ---")
    
    # find best model (lowest MAE)
    best_idx = results_df['MAE'].idxmin()
    best_model_name = results_df.loc[best_idx, 'Model']
    best_model = models[best_model_name]
    
    print(f"Best Model: {best_model_name}")
    
    # save model
    model_path = os.path.join(base_dir, 'models', 'best_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"Model saved to: {model_path}")
    
    # save scaler
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to: {scaler_path}")
    
    return best_model_name, best_model


def print_summary(results_df, best_model_name):
    """Print final summary"""
    print("\n" + "=" * 60)
    print("MODEL TRAINING SUMMARY")
    print("=" * 60)
    
    print("\nModel Comparison:")
    print(results_df.to_string(index=False))
    
    print(f"\n🏆 Best Model: {best_model_name}")
    
    best_row = results_df[results_df['Model'] == best_model_name].iloc[0]
    print(f"   - Average Error: {best_row['MAE']:.2f} days")
    print(f"   - Accuracy: {best_row['R2 Score']*100:.1f}%")
    
    print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("PREDICTIVE MODELING - VISA PROCESSING TIME")
    print("Infosys Springboard - Milestone 3")
    print("=" * 60)
    
    # step 1: load data
    df, base_dir = load_data()
    
    # step 2: prepare features
    X, y, feature_names = prepare_features(df)
    
    # step 3: split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # step 4: scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    
    # step 5: train models
    models = train_models(X_train_scaled, y_train)
    
    # step 6: evaluate models
    results_df = evaluate_models(models, X_test_scaled, y_test)
    
    # step 7: create visualizations
    figures_dir = os.path.join(base_dir, 'reports', 'figures')
    plot_model_comparison(results_df, os.path.join(figures_dir, 'model_comparison.png'))
    plot_feature_importance(models['Random Forest'], feature_names, 
                           os.path.join(figures_dir, 'feature_importance.png'))
    
    # step 8: save best model
    best_name, best_model = save_best_model(models, results_df, scaler, base_dir)
    
    # step 9: print summary
    print_summary(results_df, best_name)
    
    # save results to file
    results_path = os.path.join(base_dir, 'reports', 'model_results.csv')
    results_df.to_csv(results_path, index=False)
    print(f"\nResults saved to: {results_path}")
    
    print("\nMILESTONE 3 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
