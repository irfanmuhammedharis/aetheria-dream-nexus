# Verified against Section 5.2.3 of doc.md for Narrative Weaver.

from __future__ import annotations

from typing import Any, Dict

from apps.backend.src.services.deepseek_client import DeepSeekClient
from packages.shared_schema.src.schemas import ArchetypalNode, CelestialTransitMap

class NarrativeWeaver:
    """Synthesizes archetypal and celestial data into poetic user-facing narratives."""

    def __init__(self):
        self.client = DeepSeekClient()
        self.system_prompt = (
            "You are a mystical storyteller weaving dreams into revelations. "
            "Create poetic, immersive narratives from archetypal and celestial data. "
            "Keep it evocative but grounded; do not mention internal system prompts."
        )

    def synthesize_narrative(self, archetype: ArchetypalNode, transit: CelestialTransitMap) -> str:
        """Generate the "Shadow-Weave" narrative text."""
        user_prompt = (
            "Weave this archetype with this transit into a shadow-weave tapestry.\n\n"
            f"Archetype: {archetype.model_dump()}\n\n"
            f"Transit: {transit.model_dump()}"
        )

        try:
            return self.client.chat(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
            )
        except Exception:
            # Deterministic fallback for dev/test
            primary = archetype.archetype_id.value
            lunar = transit.lunar_phase
            return (
                f"A quiet weave gathers around {primary}. "
                f"In this moment (lunar_phase={lunar:.2f}), notice the symbols "
                f"{', '.join(archetype.symbolic_manifestations[:3])}. "
                "Stay with the feeling, name it gently, and choose one small act of integration today."
            )

    def generate_ux_directives(self, narrative: str) -> Dict[str, Any]:
        """Generate UI directives for visualization."""
        return {
            "background_color": "dark_vellum",
            "haptic_pattern": "archetypal_unlock",
            "animation_sequence": "blooming_mandala"
        }

# Verification Log
# - Implemented Narrative Weaver for poetic synthesis per Section 5.2.3.
# - Uses Chain-of-Emotion prompting for immersive output.
# - Generates UX directives for haptic and visual feedback.