# FastAPI Server for Visa Processing Time Estimator
# Author: Harsh
# Infosys Springboard Project - Milestone 4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import os

from prediction_service import get_prediction_service

# Initialize FastAPI app
app = FastAPI(
    title="India Visa Processing Estimator API",
    description="AI-powered visa processing time prediction",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize prediction service
prediction_service = None


@app.on_event("startup")
async def startup_event():
    """Load the prediction service on startup"""
    global prediction_service
    prediction_service = get_prediction_service()
    print("✓ API server started successfully!")


# Request/Response Models
class VisaApplication(BaseModel):
    """Input model for visa application prediction"""
    applicant_age: int = Field(..., ge=18, le=100, description="Applicant age in years")
    nationality: str = Field(..., description="Applicant's country")
    visa_type: str = Field(..., description="Type of visa being applied for")
    occupation: str = Field(default="Professional", description="Applicant's occupation")
    education_level: str = Field(default="Graduate", description="Highest education")
    duration_requested_days: int = Field(default=30, ge=1, le=365, description="Visa duration requested")
    num_previous_visits: int = Field(default=0, ge=0, description="Previous India visits")
    financial_proof_usd: float = Field(default=15000, ge=0, description="Financial proof in USD")
    has_sponsor: bool = Field(default=False, description="Has sponsor in India")
    documents_complete: bool = Field(default=True, description="All documents submitted")
    express_processing: bool = Field(default=False, description="Express processing requested")
    application_month: int = Field(default=1, ge=1, le=12, description="Application month (1-12)")


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    predicted_days: float
    min_days: float
    max_days: float
    risk_score: int
    risk_level: str
    approval_likelihood: str
    approval_percentage: int
    country_average: float
    visa_type_average: float
    is_peak_season: bool
    factors: dict


# API Endpoints
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "visa-estimator-api"}


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_processing_time(application: VisaApplication):
    """
    Predict visa processing time based on application details.
    
    Returns predicted days with confidence interval, risk assessment,
    and approval likelihood.
    """
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Prediction service not initialized")
    
    try:
        # Convert to dict for prediction service
        app_dict = application.model_dump()
        
        # Get prediction
        result = prediction_service.predict(app_dict)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/api/statistics")
async def get_statistics():
    """
    Get overall statistics from the visa dataset.
    
    Returns average processing times, approval rates, and available options.
    """
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    return prediction_service.get_statistics()


@app.get("/api/visa-types")
async def get_visa_types():
    """Get list of available visa types with statistics"""
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    return prediction_service.get_visa_type_stats()


@app.get("/api/countries")
async def get_countries():
    """Get list of supported countries with statistics"""
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    return prediction_service.get_country_stats()


@app.get("/api/options")
async def get_options():
    """Get all form options (nationalities, visa types, etc.)"""
    if prediction_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    stats = prediction_service.get_statistics()
    return {
        "nationalities": stats['nationalities'],
        "visa_types": stats['visa_types'],
        "occupations": stats['occupations'],
        "education_levels": stats['education_levels']
    }


# Serve frontend static files
# Resolve the absolute path to the frontend folder
_backend_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.normpath(os.path.join(_backend_dir, "..", "frontend"))

# Debug: print path on startup
print(f"Looking for frontend at: {frontend_path}")
print(f"Frontend exists: {os.path.exists(frontend_path)}")
if os.path.exists(frontend_path):
    print(f"Frontend files: {os.listdir(frontend_path)}")

if os.path.exists(frontend_path):
    # Helper function to create response with no-cache headers
    def create_file_response(file_path: str, media_type: str = None):
        """Create FileResponse with no-cache headers"""
        response = FileResponse(file_path, media_type=media_type)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    
    @app.get("/styles.css")
    async def serve_css():
        """Serve CSS file"""
        return create_file_response(
            os.path.join(frontend_path, "styles.css"), 
            media_type="text/css"
        )
    
    @app.get("/app.js")
    async def serve_js():
        """Serve JavaScript file"""
        return create_file_response(
            os.path.join(frontend_path, "app.js"), 
            media_type="application/javascript"
        )
    
    @app.get("/")
    async def serve_home():
        """Serve the home page"""
        return create_file_response(
            os.path.join(frontend_path, "index.html"),
            media_type="text/html"
        )
    
    @app.get("/predict")
    async def serve_predict():
        """Serve the prediction page"""
        return create_file_response(
            os.path.join(frontend_path, "predict.html"),
            media_type="text/html"
        )
    
    @app.get("/predict.html")
    async def serve_predict_html():
        """Serve the prediction page (with .html extension)"""
        return create_file_response(
            os.path.join(frontend_path, "predict.html"),
            media_type="text/html"
        )
    
    @app.get("/visa-info")
    async def serve_visa_info():
        """Serve the visa information page"""
        return create_file_response(
            os.path.join(frontend_path, "visa-info.html"),
            media_type="text/html"
        )
    
    @app.get("/visa-info.html")
    async def serve_visa_info_html():
        """Serve the visa information page (with .html extension)"""
        return create_file_response(
            os.path.join(frontend_path, "visa-info.html"),
            media_type="text/html"
        )


# Run with: uvicorn app:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

