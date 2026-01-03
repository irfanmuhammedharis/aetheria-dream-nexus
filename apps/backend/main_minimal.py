# apps/backend/main_minimal.py
"""
Minimal FastAPI server with only DecagonAnalysis routes.
Use this to test the Aetheria Nexus Dashboard without legacy dependencies.
"""
import os
import sys
from datetime import datetime

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create app
app = FastAPI(
    title="Aetheria Nexus API",
    version="1.0.0",
    description="10-Dimensional Psycho-Astrological Analysis System"
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include DecagonAnalysis routes
try:
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(backend_dir, 'routes'))
    from analysis_routes import router as analysis_router
    app.include_router(analysis_router)
    print("[OK] DecagonAnalysis routes loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load analysis routes: {e}")
    import traceback
    traceback.print_exc()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Aetheria Nexus API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "analyze": "POST /api/v1/analyze",
            "birth_chart": "GET/POST /api/v1/birth-chart/{user_id}",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "swiss_ephemeris": "available",
            "analysis_engine": "ready"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("[AETHERIA] Starting Nexus API Server")
    print("=" * 80)
    print("Endpoints:")
    print("   - POST http://127.0.0.1:8001/api/v1/analyze")
    print("   - GET  http://127.0.0.1:8001/api/v1/birth-chart/{user_id}")
    print("   - GET  http://127.0.0.1:8001/health")
    print("=" * 80)
    uvicorn.run(app, host="127.0.0.1", port=8001)
