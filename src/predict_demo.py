# Prediction Demo Script
# Author: Harsh
# Shows how to use the trained model to make predictions

import pandas as pd
import numpy as np
import joblib
import os


def load_model_and_scaler():
    """Load the saved model and scaler"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    model_path = os.path.join(base_dir, 'models', 'best_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    print("Model and scaler loaded successfully!")
    return model, scaler


def create_sample_application():
    """Create a sample visa application for demo"""
    
    # sample application data
    sample = {
        'applicant_age': 28,
        'duration_requested_days': 90,
        'num_previous_visits': 2,
        'financial_proof_usd': 15000,
        'has_sponsor': 1,
        'documents_complete': 1,
        'express_processing': 0,
        'is_peak_season': 1,
        'education_encoded': 2,  # Graduate
        'visa_type_encoded': 7,  # Tourist
        'nationality_encoded': 19,  # USA
        'occupation_encoded': 4,  # Professional
        'risk_score': 1,
        'country_avg_processing_time': 8.5,
        'visa_type_avg_time': 6.0
    }
    
    return sample


def predict_processing_time(model, scaler, application):
    """Predict processing time for a visa application"""
    
    # convert to dataframe
    df = pd.DataFrame([application])
    
    # scale features
    df_scaled = scaler.transform(df)
    
    # make prediction
    prediction = model.predict(df_scaled)[0]
    
    return prediction


def main():
    print("=" * 50)
    print("VISA PROCESSING TIME PREDICTION DEMO")
    print("=" * 50)
    
    # load model
    model, scaler = load_model_and_scaler()
    
    # create sample applications
    print("\n--- Sample Visa Application ---")
    
    # Application 1: Low risk
    app1 = {
        'applicant_age': 28,
        'duration_requested_days': 30,
        'num_previous_visits': 3,
        'financial_proof_usd': 25000,
        'has_sponsor': 1,
        'documents_complete': 1,
        'express_processing': 1,
        'is_peak_season': 0,
        'education_encoded': 3,  # Post Graduate
        'visa_type_encoded': 7,  # Tourist
        'nationality_encoded': 18,  # UK
        'occupation_encoded': 4,  # Professional
        'risk_score': 0,
        'country_avg_processing_time': 7.5,
        'visa_type_avg_time': 6.0
    }
    
    # Application 2: Medium risk
    app2 = {
        'applicant_age': 35,
        'duration_requested_days': 180,
        'num_previous_visits': 0,
        'financial_proof_usd': 12000,
        'has_sponsor': 0,
        'documents_complete': 1,
        'express_processing': 0,
        'is_peak_season': 1,
        'education_encoded': 2,  # Graduate
        'visa_type_encoded': 0,  # Business
        'nationality_encoded': 4,  # China
        'occupation_encoded': 1,  # Business Owner
        'risk_score': 3,
        'country_avg_processing_time': 12.0,
        'visa_type_avg_time': 9.0
    }
    
    # Application 3: High risk
    app3 = {
        'applicant_age': 40,
        'duration_requested_days': 365,
        'num_previous_visits': 0,
        'financial_proof_usd': 8000,
        'has_sponsor': 0,
        'documents_complete': 0,
        'express_processing': 0,
        'is_peak_season': 1,
        'education_encoded': 1,  # 12th Pass
        'visa_type_encoded': 2,  # Employment
        'nationality_encoded': 11,  # Russia
        'occupation_encoded': 6,  # Self Employed
        'risk_score': 5,
        'country_avg_processing_time': 14.0,
        'visa_type_avg_time': 17.0
    }
    
    # make predictions
    applications = [
        ("Low Risk (Tourist, UK, Express)", app1),
        ("Medium Risk (Business, China)", app2),
        ("High Risk (Employment, Russia)", app3)
    ]
    
    print("\nPredictions:")
    print("-" * 50)
    
    for name, app in applications:
        pred = predict_processing_time(model, scaler, app)
        risk = app['risk_score']
        print(f"\n{name}")
        print(f"  Risk Score: {risk}")
        print(f"  Predicted Processing Time: {pred:.1f} days")
    
    print("\n" + "=" * 50)
    print("DEMO COMPLETE!")
    print("=" * 50)


if __name__ == "__main__":
    main()
