# apps/backend/routes/analysis_routes.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import sys
import os

# Add packages to path - use absolute path resolution
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
repo_root = os.path.dirname(os.path.dirname(backend_dir))
sys.path.insert(0, os.path.join(repo_root, 'packages', 'shared-schema', 'src'))

from schemas import DecagonAnalysisObject

# Import analysis engine - use absolute path resolution
sys.path.insert(0, os.path.join(backend_dir, 'services'))
from analysis_engine import DecagonAnalyzer

router = APIRouter(prefix="/api/v1", tags=["analysis"])

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AnalyzeRequest(BaseModel):
    """Request body for /analyze endpoint"""
    dream_content: str
    user_id: str
    birth_datetime: datetime
    birth_latitude: float
    birth_longitude: float
    dream_datetime: Optional[datetime] = None  # Defaults to now if not provided


class BirthDataRequest(BaseModel):
    """Birth data for storing user profile"""
    user_id: str
    birth_datetime: datetime
    birth_latitude: float
    birth_longitude: float
    timezone: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/analyze", response_model=DecagonAnalysisObject)
async def analyze_dream(request: AnalyzeRequest):
    """
    Main analysis endpoint: Dream + Birth Data → 10-Dimensional Analysis
    
    Example Request:
    ```json
    {
        "dream_content": "I saw a black serpent in a flooded basement...",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "birth_datetime": "1990-05-15T03:30:00Z",
        "birth_latitude": 28.6139,
        "birth_longitude": 77.2090,
        "dream_datetime": "2026-01-03T06:45:00Z"
    }
    ```
    """
    try:
        analyzer = DecagonAnalyzer()
        
        # Use dream_datetime or default to now
        dream_dt = request.dream_datetime or datetime.utcnow()
        
        result = analyzer.analyze(
            dream_content=request.dream_content,
            birth_datetime=request.birth_datetime,
            birth_lat=request.birth_latitude,
            birth_lon=request.birth_longitude,
            current_datetime=dream_dt,
            user_id=request.user_id
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/birth-chart")
async def save_birth_data(request: BirthDataRequest):
    """Store user's birth data for future analyses"""
    # In production: Save to database
    # For now: Just acknowledge receipt
    return {
        "status": "success",
        "message": f"Birth data saved for user {request.user_id}",
        "user_id": request.user_id
    }


@router.get("/birth-chart/{user_id}")
async def get_birth_data(user_id: str):
    """Retrieve stored birth data"""
    # In production: Fetch from database
    # For now: Return stub
    return {
        "user_id": user_id,
        "birth_datetime": "1990-05-15T03:30:00Z",
        "birth_latitude": 28.6139,
        "birth_longitude": 77.2090,
        "timezone": "Asia/Kolkata",
        "message": "Stub data - replace with database query"
    }
