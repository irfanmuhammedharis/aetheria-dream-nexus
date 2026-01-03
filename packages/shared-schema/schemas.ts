// Shared Schemas for Aetheria Project
// Verified against Section 3 of doc.md

// Enums inferred from context
export enum SleepPhase {
  REM = "REM",
  NREM = "NREM",
  AWAKE = "awake",
  LIGHT = "light",
  DEEP = "deep"
}

export enum ArchetypeId {
  HERO = "HERO",
  SHADOW = "SHADOW",
  ANIMA = "ANIMA",
  ANIMUS = "ANIMUS",
  TRICKSTER = "TRICKSTER",
  WISE_OLD_MAN = "WISE_OLD_MAN",
  GREAT_MOTHER = "GREAT_MOTHER",
  PUER_AETERNUS = "PUER_AETERNUS",
  SENEX = "SENEX",
  PERSONA = "PERSONA",
  SELF = "SELF"
}

export enum IntegrationStatus {
  UNCONSCIOUS = "unconscious",
  CONFRONTATION = "confrontation",
  ASSIMILATION = "assimilation",
  INTEGRATED = "integrated"
}

export enum Planet {
  SUN = "Sun",
  MOON = "Moon",
  MERCURY = "Mercury",
  VENUS = "Venus",
  MARS = "Mars",
  JUPITER = "Jupiter",
  SATURN = "Saturn",
  URANUS = "Uranus",
  NEPTUNE = "Neptune",
  PLUTO = "Pluto"
}

export enum AspectType {
  CONJUNCTION = "conjunction",
  OPPOSITION = "opposition",
  TRINE = "trine",
  SQUARE = "square",
  SEXTILE = "sextile"
}

export enum PsychologicalPressure {
  FRICTION = "friction",
  FLOW = "flow",
  RESTRICTION = "restriction",
  EXPANSION = "expansion",
  DISRUPTION = "disruption",
  DISSOLUTION = "dissolution"
}

export enum InputModality {
  TEXT = "text",
  VOICE_TRANSCRIPT = "voice_transcript",
  HAPTIC_SIGNAL = "haptic_signal"
}

// Interfaces
export interface BiometricContext {
  sleep_phase: SleepPhase;
  heart_rate_variability: number;
}

export interface DreamIngestionObject {
  dream_id: string;
  user_id: string;
  timestamp_ingested: string; // ISO date-time
  timestamp_experience: string; // ISO date-time
  input_modality: InputModality;
  content_raw: string;
  biometric_context?: BiometricContext;
}

export interface ArchetypalNode {
  archetype_id: ArchetypeId;
  valence: number; // -1.0 to 1.0
  integration_status: IntegrationStatus;
  symbolic_manifestations: string[];
  vector_embedding_ref: string;
}

export interface ActiveAspect {
  transit_planet: Planet;
  natal_planet: Planet;
  aspect_type: AspectType;
  orb_degrees: number; // <=10.0
  psychological_pressure: PsychologicalPressure;
}

export interface CelestialTransitMap {
  transit_id: string;
  active_aspects: ActiveAspect[];
  lunar_phase: number; // 0.0 to 1.0
}

export interface CloudEvent {
  specversion: string;
  type: string;
  source: string;
  id: string;
  time: string; // ISO date-time
  datacontenttype: string;
  data: Record<string, any>;
}

export interface UserContextTier {
  tier_level: string;
  access_grants: string[];
}

export interface TemporalContext {
  current_session_id: string;
  last_interaction_delta_hours: number;
}

export interface SafetyConstraints {
  trigger_warnings: string[];
  prohibited_topics: string[];
}

export interface RegistryEntry {
  user_context_tier: UserContextTier;
  temporal_context: TemporalContext;
  active_narrative_threads: string[]; // Placeholder
  safety_constraints: SafetyConstraints;
}