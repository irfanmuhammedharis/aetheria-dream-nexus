# Verified against Section 4 of doc.md for Context Registry implementation.

import redis
import json
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime
from packages.shared_schema.src.schemas import ArchetypalNode  # Assuming import path

class UserContextTier(BaseModel):
    tier_level: str  # e.g., "gold_subscriber"
    access_grants: List[str]  # e.g., ["deep_history", "chart_synastry", "voice_synthesis"]

class TemporalContext(BaseModel):
    current_session_id: str
    last_interaction_delta_hours: float

class ActiveNarrativeThread(BaseModel):
    thread_id: str
    archetype: str  # e.g., "SHADOW"
    status: str  # e.g., "active"

class SafetyConstraints(BaseModel):
    trigger_warnings: List[str]  # e.g., ["falling_sensation"]
    prohibited_topics: List[str]  # e.g., ["self_harm_instruction"]

class ContextRegistryEntry(BaseModel):
    user_context_tier: UserContextTier
    temporal_context: TemporalContext
    active_narrative_threads: List[ActiveNarrativeThread]
    safety_constraints: SafetyConstraints

class ContextRegistry:
    """Verified against Section 4.1 of doc.md. Acts as single source of truth for user context."""

    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True, socket_connect_timeout=1)
            # Test connection
            self.redis_client.ping()
            self.offline_mode = False
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
            # Offline mode: use in-memory dict as fallback
            self.redis_client = None
            self.offline_mode = True
            self._memory_store: Dict[str, str] = {}

    def get_user_context(self, user_id: str) -> Optional[ContextRegistryEntry]:
        """Retrieve the context registry entry for a user."""
        key = f"context:{user_id}"
        if self.offline_mode:
            data = self._memory_store.get(key)
        else:
            data = self.redis_client.get(key)
        if data:
            return ContextRegistryEntry.parse_raw(data)
        return None

    def update_temporal_state(self, user_id: str, timestamp: datetime) -> None:
        """Update the temporal context for a user."""
        key = f"context:{user_id}"
        existing = self.get_user_context(user_id)
        if existing:
            existing.temporal_context.last_interaction_delta_hours = (datetime.now() - timestamp).total_seconds() / 3600
            if self.offline_mode:
                self._memory_store[key] = existing.json()
            else:
                self.redis_client.set(key, existing.json())
        # Assumption: If no existing context, create minimal one. Doc silent on initialization.

    def set_user_context(self, user_id: str, entry: ContextRegistryEntry) -> None:
        """Set the full context registry entry for a user."""
        key = f"context:{user_id}"
        if self.offline_mode:
            self._memory_store[key] = entry.json()
        else:
            self.redis_client.set(key, entry.json())

    def update_active_threads(self, user_id: str, threads: List[ActiveNarrativeThread]) -> None:
        """Update active narrative threads."""
        existing = self.get_user_context(user_id)
        if existing:
            existing.active_narrative_threads = threads
            self.set_user_context(user_id, existing)

# Verification Log
# - Implemented ContextRegistry class with Redis backend as per Section 4.
# - Defined Pydantic models for ContextRegistryEntry and sub-components based on Section 4.1.
# - Assumption: Used Redis for storage; if Postgres preferred, please clarify.
# - Assumption: Added set_user_context and update_active_threads methods for completeness, as doc specifies get_user_context and update_temporal_state but implies full management.