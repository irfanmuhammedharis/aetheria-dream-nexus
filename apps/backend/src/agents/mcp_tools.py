# Verified against Section 6 (Model Context Protocol Tool Definitions)

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class MCPToolSchema(BaseModel):
    """Base schema for MCP tool definitions per Section 6."""
    name: str
    description: str
    inputSchema: Dict[str, Any]
    outputSchema: Dict[str, Any]


# Section 6.1: analyze_dream_archetypes (Jungian Decoder)
ANALYZE_DREAM_ARCHETYPES = {
    "name": "analyze_dream_archetypes",
    "description": "Extracts Jungian motifs and emotional valence from a dream narrative.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "narrative_text": {
                "type": "string",
                "description": "The full text of the dream report."
            },
            "user_history_summary": {
                "type": "string",
                "description": "Compressed context of previous archetypal encounters."
            }
        },
        "required": ["narrative_text"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "archetypes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "archetype_id": {"type": "string"},
                        "valence": {"type": "number"},
                        "integration_status": {"type": "string"},
                        "symbolic_manifestations": {"type": "array", "items": {"type": "string"}},
                        "vector_embedding_ref": {"type": "string"}
                    }
                }
            },
            "clinical_flag": {
                "type": "boolean",
                "description": "True if content requires safety intervention."
            }
        }
    }
}


# Section 6.2: calculate_planetary_transits (Celestial Engine)
CALCULATE_PLANETARY_TRANSITS = {
    "name": "calculate_planetary_transits",
    "description": "Calculates geometric relationships between current planets and natal chart.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target_date": {
                "type": "string",
                "format": "date-time",
                "description": "ISO 8601 timestamp for transit calculation"
            },
            "natal_coordinates": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number", "minimum": -90, "maximum": 90},
                    "longitude": {"type": "number", "minimum": -180, "maximum": 180},
                    "birth_time_utc": {"type": "string", "format": "date-time"}
                },
                "required": ["latitude", "longitude", "birth_time_utc"]
            }
        },
        "required": ["target_date", "natal_coordinates"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "transit_id": {"type": "string", "format": "uuid"},
            "active_aspects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "transit_planet": {"type": "string"},
                        "natal_planet": {"type": "string"},
                        "aspect_type": {"type": "string"},
                        "orb_degrees": {"type": "number"},
                        "psychological_pressure": {"type": "string"}
                    }
                }
            },
            "lunar_phase": {"type": "number", "minimum": 0.0, "maximum": 1.0}
        }
    }
}


# Section 6.3: query_resonance_map (Search Worker / RAG)
QUERY_RESONANCE_MAP = {
    "name": "query_resonance_map",
    "description": "Finds similar dreams in the global database based on archetypal signature.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "archetype_tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of archetype IDs to search for"
            },
            "transit_filter": {
                "type": "string",
                "description": "Filter by planetary event (e.g., 'Saturn_Return')."
            },
            "top_k": {
                "type": "integer",
                "default": 5,
                "description": "Number of similar dreams to retrieve"
            }
        },
        "required": ["archetype_tags"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "cohort_dreams": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "dream_id": {"type": "string", "format": "uuid"},
                        "similarity_score": {"type": "number"},
                        "archetypes": {"type": "array", "items": {"type": "string"}},
                        "anonymized_snippet": {"type": "string"}
                    }
                }
            }
        }
    }
}


# Section 6: Validate Content Safety (Safety Sentinel)
VALIDATE_CONTENT_SAFETY = {
    "name": "validate_content_safety",
    "description": "Scans content for safety violations, crisis indicators, and PII.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Raw content to validate"
            },
            "user_id": {
                "type": "string",
                "description": "User ID for audit logging"
            }
        },
        "required": ["content"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "is_safe": {"type": "boolean"},
            "safety_level": {"type": "string"},
            "violations": {"type": "array", "items": {"type": "string"}},
            "scrubbed_content": {"type": "string"},
            "resources": {"type": "object"},
            "action_required": {"type": "string"}
        }
    }
}


# Section 6: Generate Narrative (Narrative Weaver)
SYNTHESIZE_NARRATIVE = {
    "name": "synthesize_narrative",
    "description": "Synthesizes poetic narrative from archetypal analysis and celestial transits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "archetypes": {
                "type": "array",
                "items": {"type": "object"}
            },
            "transits": {
                "type": "object"
            },
            "user_context": {
                "type": "object",
                "description": "Context Registry entry for personalization"
            }
        },
        "required": ["archetypes", "transits"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "narrative_text": {"type": "string"},
            "shadow_weave_threads": {"type": "array", "items": {"type": "string"}},
            "ui_directives": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string"},
                        "target": {"type": "string"},
                        "payload": {"type": "object"}
                    }
                }
            }
        }
    }
}


# Tool Registry: All MCP-compliant tool definitions
MCP_TOOL_REGISTRY: Dict[str, Dict] = {
    "analyze_dream_archetypes": ANALYZE_DREAM_ARCHETYPES,
    "calculate_planetary_transits": CALCULATE_PLANETARY_TRANSITS,
    "query_resonance_map": QUERY_RESONANCE_MAP,
    "validate_content_safety": VALIDATE_CONTENT_SAFETY,
    "synthesize_narrative": SYNTHESIZE_NARRATIVE,
}


def get_tool_schema(tool_name: str) -> Dict:
    """Retrieve MCP tool schema by name."""
    return MCP_TOOL_REGISTRY.get(tool_name, {})


def list_available_tools() -> List[str]:
    """List all available MCP tools."""
    return list(MCP_TOOL_REGISTRY.keys())


# Verification Log:
# - Implements Section 6 MCP tool definitions
# - Provides strict JSON schemas for all worker agent interfaces
# - Supports "Agents-as-Tools" pattern per ADR-01
# - Enables orchestrator to discover and invoke agent capabilities
# - Each tool has explicit input/output schemas per spec
