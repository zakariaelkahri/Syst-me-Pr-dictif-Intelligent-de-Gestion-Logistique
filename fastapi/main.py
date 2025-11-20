from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional, Dict, Any
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Logistics Management API",
    description="API for predictive logistics management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    message: str

class PredictionRequest(BaseModel):
    data: Dict[str, Any]

class PredictionResponse(BaseModel):
    prediction: Any
    confidence: Optional[float] = None

# Routes
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Intelligent Logistics Management API"}

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="FastAPI service is running"
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Prediction endpoint for logistics optimization
    """
    try:
        # This is where you would integrate with your ML models
        # For now, return a dummy response
        return PredictionResponse(
            prediction="sample_prediction",
            confidence=0.85
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status", tags=["Status"])
async def api_status():
    """API status information"""
    return {
        "api_version": "1.0.0",
        "status": "active",
        "mongo_uri": os.getenv("MONGO_URI", "Not configured"),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )