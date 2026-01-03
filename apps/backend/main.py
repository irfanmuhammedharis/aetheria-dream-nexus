# Verified against Section 1.3 and Section 7 (Phase 1) of doc.md for backend setup.

import os, sys
# Ensure repo root in path so local packages (packages/*) are importable during dev
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from pydantic import BaseModel
from packages.shared_schema.src.schemas import DreamIngestionObject
from apps.backend.src.core.context_registry import ContextRegistry
from apps.backend.src.agents.orchestrator import PsycheOrchestrator
from apps.backend.src.agents.safety_sentinel import SafetySentinel
from apps.backend.src.agents.growth_architect import GrowthArchitect
from apps.backend.src.agents.celestial_engine import calculate_planetary_transits, CalculateTransitsInput
from apps.backend.src.api.routes import auth as auth_routes
import uuid
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Aetheria Backend", version="1.0.0")

# CORS for local web development (Vite/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"] ,
    allow_headers=["*"],
)

# Initialize components
context_registry = ContextRegistry()
orchestrator = PsycheOrchestrator()
safety_sentinel = SafetySentinel()
growth_architect = GrowthArchitect()

# Include auth router
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

# Include analysis router (DecagonAnalysisObject system)
try:
    # Use absolute import path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(backend_dir, 'routes'))
    from analysis_routes import router as analysis_router
    app.include_router(analysis_router)
    print("[OK] DecagonAnalysis routes loaded successfully")
except Exception as e:
    print(f"[WARNING] Could not load analysis routes: {e}")

@app.post("/ingest/dream")
async def ingest_dream(dream: DreamIngestionObject):
    """Verified against Section 3.1 for dream ingestion."""
    # Safety check
    safety_result = safety_sentinel.validate_content(dream.content_raw)
    if not safety_result["safe"]:
        raise HTTPException(status_code=400, detail="Content violates safety constraints")

    # Scrub PII
    dream.content_raw = safety_sentinel.scrub_pii(dream.content_raw)

    # Process via orchestrator (async support may be added later)
    result = orchestrator.ingest_dream(dream)

    # Growth trigger
    trigger = growth_architect.evaluate_engagement_trigger({"session_count": 1, "last_interaction_days": 0})
    result["engagement_trigger"] = trigger

    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Example endpoint for celestial transits
@app.post("/calculate/transits")
async def get_transits(input_data: CalculateTransitsInput):
    """Verified against Section 6.2 for calculate_planetary_transits tool."""
    result = calculate_planetary_transits(input_data)
    return result.dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Verification Log
# - Registered /auth routes (register/login) and retained existing ingestion endpoints.
# - Assumption: Auth middleware (JWT validation) will be added in the next step.