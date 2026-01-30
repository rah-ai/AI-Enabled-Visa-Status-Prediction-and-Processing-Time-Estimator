# Prediction Service for Visa Processing Time Estimation
# Author: Harsh
# Connects to trained ML model and provides predictions

import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Tuple


class VisaPredictionService:
    """Service class to handle visa processing time predictions"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.data = None
        self.encoding_maps = {}
        self._load_resources()
    
    def _load_resources(self):
        """Load the trained model, scaler, and reference data"""
        # Get base directory (two levels up from webapp/backend)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Load model and scaler
        model_path = os.path.join(base_dir, 'models', 'best_model.pkl')
        scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        # Load featured dataset for reference statistics
        data_path = os.path.join(base_dir, 'data', 'processed', 'visa_applications_featured.csv')
        self.data = pd.read_csv(data_path)
        
        # Setup encoding maps
        self._setup_encodings()
        
        print("✓ Prediction service loaded successfully!")
        print(f"  - Model: {type(self.model).__name__}")
        print(f"  - Dataset: {len(self.data)} records")
    
    def _setup_encodings(self):
        """Setup encoding mappings for categorical variables"""
        
        # Education levels (ordinal)
        self.encoding_maps['education'] = {
            '10th Pass': 0, '12th Pass': 1, 'Graduate': 2, 
            'Post Graduate': 3, 'Doctorate': 4
        }
        
        # Visa types
        self.encoding_maps['visa_type'] = {
            'Business': 0, 'Conference': 1, 'Employment': 2, 'Entry': 3,
            'Medical': 4, 'Research': 5, 'Student': 6, 'Tourist': 7
        }
        
        # Nationalities
        self.encoding_maps['nationality'] = {
            'Australia': 0, 'Bangladesh': 1, 'Brazil': 2, 'Canada': 3,
            'China': 4, 'France': 5, 'Germany': 6, 'Italy': 7,
            'Japan': 8, 'Malaysia': 9, 'Nepal': 10, 'Russia': 11,
            'Singapore': 12, 'South Africa': 13, 'South Korea': 14,
            'Sri Lanka': 15, 'Thailand': 16, 'UAE': 17, 'UK': 18, 'USA': 19
        }
        
        # Occupations
        self.encoding_maps['occupation'] = {
            'Academic': 0, 'Business Owner': 1, 'Government Employee': 2,
            'Homemaker': 3, 'Professional': 4, 'Retired': 5,
            'Self Employed': 6, 'Student': 7
        }
    
    def get_country_avg_time(self, nationality: str) -> float:
        """Get average processing time for a country from historical data"""
        country_data = self.data[self.data['nationality'] == nationality]
        if len(country_data) > 0:
            return country_data['processing_time_days'].mean()
        return self.data['processing_time_days'].mean()  # fallback to overall avg
    
    def get_visa_type_avg_time(self, visa_type: str) -> float:
        """Get average processing time for a visa type from historical data"""
        visa_data = self.data[self.data['visa_type'] == visa_type]
        if len(visa_data) > 0:
            return visa_data['processing_time_days'].mean()
        return self.data['processing_time_days'].mean()
    
    def calculate_is_peak_season(self, month: int) -> int:
        """Determine if month is peak season (Oct-Mar)"""
        peak_months = [10, 11, 12, 1, 2, 3]
        return 1 if month in peak_months else 0
    
    def calculate_risk_score(self, application: Dict) -> int:
        """Calculate risk score based on application factors"""
        risk = 0
        
        # Incomplete documents (+2)
        if not application.get('documents_complete', True):
            risk += 2
        
        # First time applicant (+1)
        if application.get('num_previous_visits', 0) == 0:
            risk += 1
        
        # No sponsor (+1)
        if not application.get('has_sponsor', True):
            risk += 1
        
        # Low financial proof (+1)
        if application.get('financial_proof_usd', 20000) < 10000:
            risk += 1
        
        # Complex visa types (+1)
        if application.get('visa_type') in ['Research', 'Employment']:
            risk += 1
        
        return risk
    
    def predict(self, application: Dict) -> Dict:
        """
        Make a prediction for visa processing time
        
        Args:
            application: Dictionary with applicant details
        
        Returns:
            Dictionary with prediction results
        """
        # Extract and encode features
        nationality = application.get('nationality', 'USA')
        visa_type = application.get('visa_type', 'Tourist')
        
        # Calculate derived features
        country_avg = self.get_country_avg_time(nationality)
        visa_avg = self.get_visa_type_avg_time(visa_type)
        month = application.get('application_month', 1)
        is_peak = self.calculate_is_peak_season(month)
        risk_score = self.calculate_risk_score(application)
        
        # Prepare feature vector (must match training features)
        features = {
            'applicant_age': application.get('applicant_age', 30),
            'duration_requested_days': application.get('duration_requested_days', 30),
            'num_previous_visits': application.get('num_previous_visits', 0),
            'financial_proof_usd': application.get('financial_proof_usd', 15000),
            'has_sponsor': 1 if application.get('has_sponsor', False) else 0,
            'documents_complete': 1 if application.get('documents_complete', True) else 0,
            'express_processing': 1 if application.get('express_processing', False) else 0,
            'is_peak_season': is_peak,
            'education_encoded': self.encoding_maps['education'].get(
                application.get('education_level', 'Graduate'), 2),
            'visa_type_encoded': self.encoding_maps['visa_type'].get(visa_type, 7),
            'nationality_encoded': self.encoding_maps['nationality'].get(nationality, 19),
            'occupation_encoded': self.encoding_maps['occupation'].get(
                application.get('occupation', 'Professional'), 4),
            'risk_score': risk_score,
            'country_avg_processing_time': country_avg,
            'visa_type_avg_time': visa_avg
        }
        
        # Create DataFrame and scale
        df = pd.DataFrame([features])
        df_scaled = self.scaler.transform(df)
        
        # Make prediction
        predicted_days = self.model.predict(df_scaled)[0]
        
        # Calculate confidence interval (±15% or ±2 days, whichever is larger)
        margin = max(predicted_days * 0.15, 2.0)
        min_days = max(1, predicted_days - margin)
        max_days = predicted_days + margin
        
        # Determine status likelihood based on risk score
        if risk_score <= 1:
            approval_likelihood = "High"
            approval_percentage = 85
        elif risk_score <= 3:
            approval_likelihood = "Medium"
            approval_percentage = 70
        else:
            approval_likelihood = "Low"
            approval_percentage = 50
        
        return {
            'predicted_days': round(predicted_days, 1),
            'min_days': round(min_days, 1),
            'max_days': round(max_days, 1),
            'risk_score': risk_score,
            'risk_level': 'Low' if risk_score <= 1 else ('Medium' if risk_score <= 3 else 'High'),
            'approval_likelihood': approval_likelihood,
            'approval_percentage': approval_percentage,
            'country_average': round(country_avg, 1),
            'visa_type_average': round(visa_avg, 1),
            'is_peak_season': bool(is_peak),
            'factors': {
                'documents_complete': application.get('documents_complete', True),
                'has_sponsor': application.get('has_sponsor', False),
                'express_processing': application.get('express_processing', False),
                'previous_visits': application.get('num_previous_visits', 0)
            }
        }
    
    def get_statistics(self) -> Dict:
        """Get overall statistics from the dataset"""
        return {
            'total_applications': len(self.data),
            'avg_processing_time': round(self.data['processing_time_days'].mean(), 1),
            'min_processing_time': int(self.data['processing_time_days'].min()),
            'max_processing_time': int(self.data['processing_time_days'].max()),
            'approval_rate': round(
                (self.data['visa_status'] == 'Approved').mean() * 100, 1
            ),
            'visa_types': list(self.encoding_maps['visa_type'].keys()),
            'nationalities': list(self.encoding_maps['nationality'].keys()),
            'occupations': list(self.encoding_maps['occupation'].keys()),
            'education_levels': list(self.encoding_maps['education'].keys()),
            'model_accuracy': 76.9  # From model_results.csv (R2 score)
        }
    
    def get_visa_type_stats(self) -> Dict:
        """Get statistics by visa type"""
        stats = {}
        for visa_type in self.encoding_maps['visa_type'].keys():
            visa_data = self.data[self.data['visa_type'] == visa_type]
            if len(visa_data) > 0:
                stats[visa_type] = {
                    'count': len(visa_data),
                    'avg_days': round(visa_data['processing_time_days'].mean(), 1),
                    'approval_rate': round(
                        (visa_data['visa_status'] == 'Approved').mean() * 100, 1
                    )
                }
        return stats
    
    def get_country_stats(self) -> Dict:
        """Get statistics by country"""
        stats = {}
        for country in self.encoding_maps['nationality'].keys():
            country_data = self.data[self.data['nationality'] == country]
            if len(country_data) > 0:
                stats[country] = {
                    'count': len(country_data),
                    'avg_days': round(country_data['processing_time_days'].mean(), 1)
                }
        return stats


# Singleton instance
_service_instance = None

def get_prediction_service() -> VisaPredictionService:
    """Get or create the prediction service singleton"""
    global _service_instance
    if _service_instance is None:
        _service_instance = VisaPredictionService()
    return _service_instance
