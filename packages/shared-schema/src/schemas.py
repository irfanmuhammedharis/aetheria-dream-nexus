# Verified against Section 3 of doc.md for DreamIngestionObject, ArchetypalNode, and CelestialTransitMap schemas.

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import UUID
from datetime import datetime

# Section 3.1: Sleep phases for BiometricContext
class SleepPhase(str, Enum):
    REM = "REM"
    NREM1 = "NREM1"
    NREM2 = "NREM2"
    NREM3 = "NREM3"

# Section 3.1: Input modality types
class InputModality(str, Enum):
    TEXT = "text"
    VOICE_TRANSCRIPT = "voice_transcript"
    HAPTIC_SIGNAL = "haptic_signal"

# Section 3.3: Psychological pressure types for transits
class PsychologicalPressure(str, Enum):
    FRICTION = "friction"
    FLOW = "flow"
    RESTRICTION = "restriction"
    EXPANSION = "expansion"
    DISRUPTION = "disruption"
    DISSOLUTION = "dissolution"

# Assumption: Jungian archetypes based on classic archetypes (Self, Shadow, Anima, Animus, Persona, etc.)
class ArchetypeId(str, Enum):
    SELF = "SELF"
    SHADOW = "SHADOW"
    ANIMA = "ANIMA"
    ANIMUS = "ANIMUS"
    PERSONA = "PERSONA"
    HERO = "HERO"
    WISE_OLD_MAN = "WISE_OLD_MAN"
    GREAT_MOTHER = "GREAT_MOTHER"
    PUER_AETERNUS = "PUER_AETERNUS"
    TRICKSTER = "TRICKSTER"

class IntegrationStatus(str, Enum):
    UNCONSCIOUS = "unconscious"
    CONFRONTATION = "confrontation"
    ASSIMILATION = "assimilation"
    INTEGRATED = "integrated"

# Assumption: Planets based on traditional astrology (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto)
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
    RAHU = "Rahu"  # North Node (Vedic)
    KETU = "Ketu"  # South Node (Vedic)

# 27 Nakshatras (Vedic Lunar Mansions)
class Nakshatra(str, Enum):
    ASHWINI = "Ashwini"
    BHARANI = "Bharani"
    KRITTIKA = "Krittika"
    ROHINI = "Rohini"
    MRIGASHIRA = "Mrigashira"
    ARDRA = "Ardra"
    PUNARVASU = "Punarvasu"
    PUSHYA = "Pushya"
    ASHLESHA = "Ashlesha"
    MAGHA = "Magha"
    PURVA_PHALGUNI = "Purva Phalguni"
    UTTARA_PHALGUNI = "Uttara Phalguni"
    HASTA = "Hasta"
    CHITRA = "Chitra"
    SWATI = "Swati"
    VISHAKHA = "Vishakha"
    ANURADHA = "Anuradha"
    JYESHTHA = "Jyeshtha"
    MULA = "Mula"
    PURVA_ASHADHA = "Purva Ashadha"
    UTTARA_ASHADHA = "Uttara Ashadha"
    SHRAVANA = "Shravana"
    DHANISHTA = "Dhanishta"
    SHATABHISHA = "Shatabhisha"
    PURVA_BHADRAPADA = "Purva Bhadrapada"
    UTTARA_BHADRAPADA = "Uttara Bhadrapada"
    REVATI = "Revati"

# Section 3.3: Complete astrological aspect types
class AspectType(str, Enum):
    CONJUNCTION = "conjunction"
    SEXTILE = "sextile"
    SQUARE = "square"
    TRINE = "trine"
    OPPOSITION = "opposition"

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

# Section 3.1: BiometricContext sub-schema
class BiometricContext(BaseModel):
    """Biometric data from Apple HealthKit integration."""
    sleep_phase: Optional[SleepPhase] = Field(None, description="Sleep stage during which the dream likely occurred.")
    heart_rate_variability: Optional[float] = Field(None, description="HRV metric at time of awakening, indicating stress/recovery state.")

class DreamIngestionObject(BaseModel):
    """Verified against Section 3.1 of doc.md."""
    dream_id: UUID = Field(description="Unique identifier for the dream entry.")
    user_id: UUID
    timestamp_ingested: datetime = Field(description="ISO 8601 timestamp of logging.")
    timestamp_experience: Optional[datetime] = Field(None, description="Estimated time of the dream occurrence, derived from Sleep Cycle data.")
    input_modality: InputModality = Field(description="Source of the input data.")
    content_raw: str = Field(description="Unprocessed user narrative.")
    biometric_context: Optional[BiometricContext] = Field(None, description="Correlated health data from Apple HealthKit.")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class ArchetypalNode(BaseModel):
    """Verified against Section 3.2 of doc.md."""
    archetype_id: ArchetypeId = Field(description="The primary Jungian category.")
    valence: float = Field(ge=-1.0, le=1.0, description="Emotional charge: -1.0 (Destructive/Repressed) to 1.0 (Creative/Integrated).")
    integration_status: IntegrationStatus = Field(description="Current stage of the user's relationship with this archetype.")
    symbolic_manifestations: List[str] = Field(description="Specific imagery used (e.g., 'black dog', 'flooded basement').")
    vector_embedding_ref: Optional[str] = Field(None, description="Reference ID to the Pinecone vector embedding for semantic search.")

class ActiveAspect(BaseModel):
    transit_planet: Planet
    natal_planet: Planet
    aspect_type: AspectType
    orb_degrees: float = Field(le=10.0, description="Tightness of the aspect. Lower is stronger.")
    psychological_pressure: PsychologicalPressure = Field(description="Computed psychological effect based on planetary combination.")

class CelestialTransitMap(BaseModel):
    """Verified against Section 3.3 of doc.md."""
    transit_id: UUID
    active_aspects: List[ActiveAspect]
    lunar_phase: float = Field(ge=0.0, le=1.0, description="0.0 (New) to 0.5 (Full) to 1.0 (New).")

    class Config:
        json_encoders = {
            UUID: lambda v: str(v)
        }

# CloudEvents schema as per Section 3.4
class CloudEvent(BaseModel):
    """Verified against Section 3.4 of doc.md."""
    specversion: str = "1.0"
    type: str
    source: str
    id: str
    time: datetime
    datacontenttype: str = "application/json"
    data: Dict[str, Any]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Verification Log
# - DreamIngestionObject: Matches Section 3.1, added enum values for sleep_phase based on standard sleep science.
# - ArchetypalNode: Matches Section 3.2, added enum values for archetype_id based on classic Jungian archetypes.
# - CelestialTransitMap: Matches Section 3.3, added enum values for planets and aspects based on traditional astrology.
# - CloudEvent: Matches Section 3.4.
# - Assumption: Enum values for sleep_phase, archetype_id, planets, aspects, and psychological_pressure are not specified in doc.md, so used standard values. If incorrect, please clarify.

# ============================================================================
# DECAGON ANALYSIS OBJECT (10-Dimensional Analysis System)
# ============================================================================

# DIMENSION 1: Shadow-Weave (Jungian Archetypal Analysis)
class ShadowWeaveNode(BaseModel):
    """Jungian archetypal activation in the dream"""
    archetype_id: str = Field(description="Archetype ID (SHADOW, SELF, ANIMA, etc.)")
    activation_strength: float = Field(ge=0.0, le=1.0, description="Intensity of archetypal activation")
    integration_status: str = Field(description="UNCONSCIOUS, CONFRONTATION, ASSIMILATION, INTEGRATED")
    symbolic_fragments: List[str] = Field(description="Dream symbols associated with this archetype")
    mythological_resonance: Optional[str] = Field(None, description="Cultural/mythological parallels")


# DIMENSION 2: Celestial Transit (already exists as CelestialTransitMap - reusing)


# DIMENSION 3: Nakshatra Snapshot (27 Lunar Mansions)
class NakshatraSnapshot(BaseModel):
    """Current Nakshatra (lunar mansion) at time of dream"""
    nakshatra: Nakshatra = Field(description="One of 27 Vedic lunar mansions")
    pada: int = Field(ge=1, le=4, description="Quarter subdivision of Nakshatra")
    ruling_planet: Planet = Field(description="Vimshottari ruler of this Nakshatra")
    deity: str = Field(description="Presiding deity (e.g., Ashwini Kumaras)")
    archetypal_theme: str = Field(description="Core theme (e.g., 'healing', 'transformation')")


# DIMENSION 4: Arabic Lots (Hermetic Lots/Parts)
class ArabicLot(BaseModel):
    """Arabic Parts calculation (Lot of Fortune, Spirit, etc.)"""
    lot_name: str = Field(description="Name of the Lot (e.g., 'Lot of Fortune')")
    longitude: float = Field(ge=0.0, lt=360.0, description="Ecliptic longitude in degrees")
    house_position: int = Field(ge=1, le=12, description="House placement")
    hermetic_meaning: str = Field(description="Esoteric interpretation")


# DIMENSION 5: Dasha Period (Vedic Planetary Periods)
class DashaPeriod(BaseModel):
    """Vimshottari Dasha planetary period"""
    maha_dasha_lord: Planet = Field(description="Major period planetary ruler")
    antardasha_lord: Planet = Field(description="Sub-period ruler")
    start_date: datetime = Field(description="Period start date")
    end_date: datetime = Field(description="Period end date")
    karmic_theme: str = Field(description="Life lessons of this period")


# DIMENSION 6: Somatic Resonance (Biometric/Body Correlation)
class SomaticResonance(BaseModel):
    """Biometric and bodily activation patterns"""
    hrv_snapshot: List[float] = Field(description="Heart Rate Variability time series (100 points)")
    biometric_context: Dict[str, Any] = Field(description="Sleep phase, heart rate, etc.")
    body_map_activations: Dict[str, float] = Field(description="Chakra/body region activations (0-1)")


# DIMENSION 7: Ancestral Ghost (Archetypal Inheritance - Optional)
class AncestralGhost(BaseModel):
    """Archetypal patterns inherited from lineage"""
    lineage_pattern: str = Field(description="Recurring family theme")
    generation_depth: int = Field(description="How many generations back")
    archetypal_burden: str = Field(description="Unresolved ancestral issue")


# DIMENSION 8: Collective Ripple (Cultural Zeitgeist - Optional)
class CollectiveRipple(BaseModel):
    """Resonance with collective unconscious"""
    zeitgeist_theme: str = Field(description="Cultural archetype active in collective")
    cohort_similarity_score: float = Field(ge=0.0, le=1.0, description="Similarity to other dreamers")
    archetypal_current: str = Field(description="Dominant collective archetype")


# DIMENSION 9: Digital Doppelganger (AI Reflection - Optional)
class DigitalDoppelganger(BaseModel):
    """AI-generated reflection/shadow"""
    mirror_narrative: str = Field(description="AI-generated counter-narrative")
    shadow_inversion: str = Field(description="Inverted archetypal reading")


# DIMENSION 10: Firdaria Phase (Persian Time-Lord System)
class FirdariaPhase(BaseModel):
    """Persian Firdaria planetary period"""
    ruling_planet: Planet = Field(description="Current Firdaria lord")
    start_age: float = Field(description="Start age of this period")
    end_age: float = Field(description="End age of this period")
    current_phase: bool = Field(description="Whether this is the active period")
    archetypal_task: str = Field(description="Life task of this period")


# COMPLETE DECAGON ANALYSIS OBJECT
class DecagonAnalysisObject(BaseModel):
    """
    10-Dimensional Psycho-Astrological Analysis Result.
    Combines Jungian analysis + Vedic astrology + biometric data.
    """
    analysis_id: str = Field(description="Unique analysis ID (DEC-{checksum})")
    timestamp: datetime = Field(description="Analysis timestamp")
    
    # 10 Dimensions
    shadow_weave: List[ShadowWeaveNode] = Field(description="DIMENSION 1: Jungian archetypal activations")
    celestial_transit: List[Dict] = Field(description="DIMENSION 2: Current planetary transits")
    nakshatra_snapshot: NakshatraSnapshot = Field(description="DIMENSION 3: Lunar mansion at dream time")
    arabic_lot: List[ArabicLot] = Field(description="DIMENSION 4: Hermetic Lots")
    dasha_period: DashaPeriod = Field(description="DIMENSION 5: Vedic dasha period")
    somatic_resonance: SomaticResonance = Field(description="DIMENSION 6: Biometric correlations")
    ancestral_ghost: Optional[AncestralGhost] = Field(None, description="DIMENSION 7: Ancestral patterns")
    collective_ripple: Optional[CollectiveRipple] = Field(None, description="DIMENSION 8: Collective unconscious")
    digital_doppelganger: Optional[DigitalDoppelganger] = Field(None, description="DIMENSION 9: AI shadow")
    firdaria_phase: FirdariaPhase = Field(description="DIMENSION 10: Persian time-lord period")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
