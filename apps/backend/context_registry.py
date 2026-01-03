"""
Context Registry for Aetheria
Verified against Section 4 of doc.md
"""

import redis
import json
from typing import Optional
from schemas import RegistryEntry, UserContextTier, TemporalContext, SafetyConstraints

class ContextRegistry:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    def get_user_context(self, user_id: str) -> Optional[RegistryEntry]:
        key = f"user_context:{user_id}"
        data = self.redis.get(key)
        if data:
            parsed = json.loads(data)
            return RegistryEntry(
                user_context_tier=UserContextTier(**parsed['user_context_tier']),
                temporal_context=TemporalContext(**parsed['temporal_context']),
                active_narrative_threads=parsed['active_narrative_threads'],
                safety_constraints=SafetyConstraints(**parsed['safety_constraints'])
            )
        return None

    def update_temporal_state(self, user_id: str, timestamp: str):
        key = f"user_context:{user_id}"
        data = self.redis.get(key)
        if data:
            parsed = json.loads(data)
            parsed['temporal_context']['last_interaction_delta_hours'] = 0  # Update logic
            self.redis.set(key, json.dumps(parsed))

    def set_user_context(self, user_id: str, entry: RegistryEntry):
        key = f"user_context:{user_id}"
        data = {
            'user_context_tier': {
                'tier_level': entry.user_context_tier.tier_level,
                'access_grants': entry.user_context_tier.access_grants
            },
            'temporal_context': {
                'current_session_id': entry.temporal_context.current_session_id,
                'last_interaction_delta_hours': entry.temporal_context.last_interaction_delta_hours
            },
            'active_narrative_threads': entry.active_narrative_threads,
            'safety_constraints': {
                'trigger_warnings': entry.safety_constraints.trigger_warnings,
                'prohibited_topics': entry.safety_constraints.prohibited_topics
            }
        }
        self.redis.set(key, json.dumps(data))