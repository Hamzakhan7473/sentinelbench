"""Optional Gemini provider stub."""

from __future__ import annotations

import os
from typing import Any, Mapping

from sentinelbench.models.base import ModelProvider
from sentinelbench.types import AgentPrediction


class GeminiProvider(ModelProvider):
    """Gemini adapter placeholder."""

    name = "gemini"

    def __init__(self, *, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv(
            "GOOGLE_API_KEY"
        )
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    def investigate(self, incident: Mapping[str, Any]) -> AgentPrediction:
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY (or GOOGLE_API_KEY) is not set. "
                "Use MockProvider for offline runs."
            )
        raise NotImplementedError(
            "GeminiProvider adapter is not implemented yet. "
            "Use MockProvider for offline evaluation."
        )
