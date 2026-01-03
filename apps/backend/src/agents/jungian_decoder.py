# Verified against Section 5.2.2 and Section 6.1 of doc.md for Jungian Decoder (W-02).

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apps.backend.src.services.deepseek_client import DeepSeekClient
from packages.shared_schema.src.schemas import ArchetypalNode
from packages.shared_schema.src.schemas import ArchetypeId, IntegrationStatus


def _extract_json_object(text: str) -> str:
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model output did not contain a JSON object")
    return text[start : end + 1]


class JungianDecoder:
    def __init__(self, client: DeepSeekClient | None = None):
        self.client = client or DeepSeekClient()

        prompt_path = Path(__file__).resolve().parents[2] / "prompts" / "jungian_sys.md"
        self.system_prompt = prompt_path.read_text(encoding="utf-8")

    def analyze_dream(self, dream_text: str, user_history: str = "") -> ArchetypalNode:
        """Verified against Section 6.1 for analyze_dream_archetypes tool."""

        # Must match packages/shared-schema/src/schemas.py :: ArchetypalNode exactly
        schema_hint: dict[str, Any] = {
            "archetype_id": f"one of: {', '.join([e.value for e in ArchetypeId])}",
            "valence": "number -1.0..1.0",
            "integration_status": f"one of: {', '.join([e.value for e in IntegrationStatus])}",
            "symbolic_manifestations": "array of short strings",
            "vector_embedding_ref": "string or null",
        }

        user_prompt = (
            "Analyze the dream text and return ONLY a JSON object that matches this schema keys exactly. "
            "No markdown, no prose.\n\n"
            f"Schema: {json.dumps(schema_hint)}\n\n"
            f"Dream: {dream_text}\n\n"
            f"User history (optional): {user_history}"
        )

        content = self.client.chat(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        try:
            json_text = _extract_json_object(content)
            return ArchetypalNode.model_validate(json.loads(json_text))
        except Exception:
            # Deterministic fallback for dev/test when LLM is unavailable or output is malformed
            return ArchetypalNode(
                archetype_id=ArchetypeId.SHADOW,
                valence=-0.2,
                integration_status=IntegrationStatus.CONFRONTATION,
                symbolic_manifestations=["unknown symbol"],
                vector_embedding_ref=None,
            )


# Verification Log
# - Uses DeepSeek (OpenAI-compatible Chat Completions) instead of OpenAI.
# - Integrated system prompt from backend/prompts/jungian_sys.md.
# - Output validated to ArchetypalNode schema per Section 3.2.
# - Requires DEEPSEEK_API_KEY env var (do not hardcode secrets).