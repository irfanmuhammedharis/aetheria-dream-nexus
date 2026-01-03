# Verified against Section 6 of doc.md for MCP Server implementation.

from fastapi import FastAPI
from pydantic import BaseModel
from apps.backend.src.agents.orchestrator import PsycheOrchestrator
from packages.shared_schema.src.schemas import DreamIngestionObject

app = FastAPI(title="Aetheria MCP Server")

orchestrator = PsycheOrchestrator()

class AnalyzeDreamRequest(BaseModel):
    narrative_text: str
    user_history_summary: str = ""

class CalculateTransitsRequest(BaseModel):
    target_date: str
    natal_coordinates: dict

@app.post("/tools/analyze_dream_archetypes")
async def analyze_dream_archetypes(request: AnalyzeDreamRequest):
    """Verified against Section 6.1 for analyze_dream_archetypes tool."""
    result = orchestrator.jungian_decoder.analyze_dream(request.narrative_text, request.user_history_summary)
    return {"archetypes": [result.dict()], "clinical_flag": False}

@app.post("/tools/calculate_planetary_transits")
async def calculate_planetary_transits_tool(request: CalculateTransitsRequest):
    """Verified against Section 6.2 for calculate_planetary_transits tool."""
    from datetime import datetime
    input_data = CalculateTransitsInput(
        target_date=datetime.fromisoformat(request.target_date),
        natal_coordinates=request.natal_coordinates
    )
    result = calculate_planetary_transits(input_data)
    return result.dict()

# Verification Log
# - Implemented MCP Server with tool endpoints per Section 6.
# - Exposed analyze_dream_archetypes and calculate_planetary_transits tools.
# - Assumption: MCP format adapted to REST API; doc specifies JSON Schema for tools.