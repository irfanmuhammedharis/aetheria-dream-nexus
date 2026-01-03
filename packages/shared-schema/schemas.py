"""
Shared Schemas for Aetheria Project
Verified against Section 3 of doc.md
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

# Enums inferred from context, as doc has placeholders
class SleepPhase(str, Enum):
    REM = "REM"
    NREM = "NREM"
    AWAKE = "awake"
    LIGHT = "light"
    DEEP = "deep"

class ArchetypeId(str, Enum):
    HERO = "HERO"
    SHADOW = "SHADOW"
    ANIMA = "ANIMA"
    ANIMUS = "ANIMUS"
    TRICKSTER = "TRICKSTER"
    WISE_OLD_MAN = "WISE_OLD_MAN"
    GREAT_MOTHER = "GREAT_MOTHER"
    PUER_AETERNUS = "PUER_AETERNUS"
    SENEX = "SENEX"
    PERSONA = "PERSONA"
    SELF = "SELF"

class IntegrationStatus(str, Enum):
    UNCONSCIOUS = "unconscious"
    CONFRONTATION = "confrontation"
    ASSIMILATION = "assimilation"
    INTEGRATED = "integrated"

class Planet(str, Enum):
    SUN = "Sun"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    PLUTO = "Pluto"

class AspectType(str, Enum):
    CONJUNCTION = "conjunction"
    OPPOSITION = "opposition"
    TRINE = "trine"
    SQUARE = "square"
    SEXTILE = "sextile"

class PsychologicalPressure(str, Enum):
    FRICTION = "friction"
    FLOW = "flow"
    RESTRICTION = "restriction"
    EXPANSION = "expansion"
    DISRUPTION = "disruption"
    DISSOLUTION = "dissolution"

class InputModality(str, Enum):
    TEXT = "text"
    VOICE_TRANSCRIPT = "voice_transcript"
    HAPTIC_SIGNAL = "haptic_signal"

# DreamIngestionObject
class BiometricContext:
    def __init__(self, sleep_phase: SleepPhase, heart_rate_variability: float):
        self.sleep_phase = sleep_phase
        self.heart_rate_variability = heart_rate_variability

class DreamIngestionObject:
    def __init__(
        self,
        dream_id: str,
        user_id: str,
        timestamp_ingested: datetime,
        timestamp_experience: datetime,
        input_modality: InputModality,
        content_raw: str,
        biometric_context: Optional[BiometricContext] = None
    ):
        self.dream_id = dream_id
        self.user_id = user_id
        self.timestamp_ingested = timestamp_ingested
        self.timestamp_experience = timestamp_experience
        self.input_modality = input_modality
        self.content_raw = content_raw
        self.biometric_context = biometric_context

# ArchetypalNode
class ArchetypalNode:
    def __init__(
        self,
        archetype_id: ArchetypeId,
        valence: float,
        integration_status: IntegrationStatus,
        symbolic_manifestations: List[str],
        vector_embedding_ref: str
    ):
        self.archetype_id = archetype_id
        self.valence = valence
        self.integration_status = integration_status
        self.symbolic_manifestations = symbolic_manifestations
        self.vector_embedding_ref = vector_embedding_ref

# CelestialTransitMap
class ActiveAspect:
    def __init__(
        self,
        transit_planet: Planet,
        natal_planet: Planet,
        aspect_type: AspectType,
        orb_degrees: float,
        psychological_pressure: PsychologicalPressure
    ):
        self.transit_planet = transit_planet
        self.natal_planet = natal_planet
        self.aspect_type = aspect_type
        self.orb_degrees = orb_degrees
        self.psychological_pressure = psychological_pressure

class CelestialTransitMap:
    def __init__(
        self,
        transit_id: str,
        active_aspects: List[ActiveAspect],
        lunar_phase: float
    ):
        self.transit_id = transit_id
        self.active_aspects = active_aspects
        self.lunar_phase = lunar_phase

# CloudEvent
class CloudEvent:
    def __init__(
        self,
        specversion: str,
        type_: str,
        source: str,
        id_: str,
        time: datetime,
        datacontenttype: str,
        data: Dict[str, Any]
    ):
        self.specversion = specversion
        self.type = type_
        self.source = source
        self.id = id_
        self.time = time
        self.datacontenttype = datacontenttype
        self.data = data

# Context Registry
class UserContextTier:
    def __init__(self, tier_level: str, access_grants: List[str]):
        self.tier_level = tier_level
        self.access_grants = access_grants

class TemporalContext:
    def __init__(self, current_session_id: str, last_interaction_delta_hours: float):
        self.current_session_id = current_session_id
        self.last_interaction_delta_hours = last_interaction_delta_hours

class SafetyConstraints:
    def __init__(self, trigger_warnings: List[str], prohibited_topics: List[str]):
        self.trigger_warnings = trigger_warnings
        self.prohibited_topics = prohibited_topics

class RegistryEntry:
    def __init__(
        self,
        user_context_tier: UserContextTier,
        temporal_context: TemporalContext,
        active_narrative_threads: List[str],  # Placeholder, doc has incomplete
        safety_constraints: SafetyConstraints
    ):
        self.user_context_tier = user_context_tier
        self.temporal_context = temporal_context
        self.active_narrative_threads = active_narrative_threads
        self.safety_constraints = safety_constraints