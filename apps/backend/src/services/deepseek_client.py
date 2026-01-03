from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


class DeepSeekClient:
    """Minimal DeepSeek client using the OpenAI-compatible Chat Completions API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout_s: float = 30.0,
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")

        self.base_url = (base_url or os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com").rstrip(
            "/"
        )
        self.model = model or os.getenv("DEEPSEEK_MODEL") or "deepseek-chat"
        self.timeout_s = timeout_s

    def chat(
        self,
        *,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> str:
        if not self.api_key:
            # Offline mode: return deterministic fallback instead of raising exception
            return "[OFFLINE_MODE] DeepSeek API key not configured. Using deterministic fallback response."

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                raw = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            raise RuntimeError(f"DeepSeek API error: {exc.code} {body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"DeepSeek API connection error: {exc}") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"DeepSeek response was not valid JSON: {raw[:500]}") from exc
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError(f"DeepSeek response missing choices: {data}")

        message = (choices[0].get("message") or {})
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(f"DeepSeek response missing content: {data}")

        return content.strip()
