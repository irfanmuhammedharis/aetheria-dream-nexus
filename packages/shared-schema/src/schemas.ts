// Verified against Section 3 of doc.md for TypeScript schemas.

import { z } from 'zod';

// Assumption: Same enums as Python version
export const SleepPhaseEnum = z.enum(['REM', 'NREM1', 'NREM2', 'NREM3']);
export const ArchetypeIdEnum = z.enum(['SELF', 'SHADOW', 'ANIMA', 'ANIMUS', 'PERSONA', 'HERO', 'WISE_OLD_MAN', 'GREAT_MOTHER', 'PUER_AETERNUS', 'TRICKSTER']);
export const IntegrationStatusEnum = z.enum(['unconscious', 'confrontation', 'assimilation', 'integrated']);
export const PlanetEnum = z.enum(['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']);
export const AspectTypeEnum = z.enum(['conjunction', 'sextile', 'square', 'trine', 'opposition']);
export const PsychologicalPressureEnum = z.enum(['friction', 'flow', 'restriction', 'expansion', 'disruption', 'dissolution']);
export const InputModalityEnum = z.enum(['text', 'voice_transcript', 'haptic_signal']);

export const DreamIngestionObjectSchema = z.object({
  dream_id: z.string().uuid(),
  user_id: z.string().uuid(),
  timestamp_ingested: z.string().datetime(),
  timestamp_experience: z.string().datetime().optional(),
  input_modality: InputModalityEnum,
  content_raw: z.string(),
  biometric_context: z.record(z.any()).optional(),
});

export const ArchetypalNodeSchema = z.object({
  archetype_id: ArchetypeIdEnum,
  valence: z.number().min(-1.0).max(1.0),
  integration_status: IntegrationStatusEnum,
  symbolic_manifestations: z.array(z.string()),
  vector_embedding_ref: z.string().optional(),
});

export const ActiveAspectSchema = z.object({
  transit_planet: PlanetEnum,
  natal_planet: PlanetEnum,
  aspect_type: AspectTypeEnum,
  orb_degrees: z.number().max(10.0),
  psychological_pressure: PsychologicalPressureEnum,
});

export const CelestialTransitMapSchema = z.object({
  transit_id: z.string().uuid(),
  active_aspects: z.array(ActiveAspectSchema),
  lunar_phase: z.number().min(0.0).max(1.0),
});

export const CloudEventSchema = z.object({
  specversion: z.literal('1.0'),
  type: z.string(),
  source: z.string(),
  id: z.string(),
  time: z.string().datetime(),
  datacontenttype: z.literal('application/json'),
  data: z.record(z.any()),
});

// Type exports
export type DreamIngestionObject = z.infer<typeof DreamIngestionObjectSchema>;
export type ArchetypalNode = z.infer<typeof ArchetypalNodeSchema>;
export type ActiveAspect = z.infer<typeof ActiveAspectSchema>;
export type CelestialTransitMap = z.infer<typeof CelestialTransitMapSchema>;
export type CloudEvent = z.infer<typeof CloudEventSchema>;

// Verification Log
// - Implemented Zod schemas matching Python Pydantic models.
// - Verified against Section 3.1-3.4 of doc.md.
// - Assumption: Used Zod for runtime validation; if interfaces only preferred, please clarify.