"""Optional OpenAI provider stub."""

from __future__ import annotations

import os
from typing import Any, Mapping

from sentinelbench.models.base import ModelProvider
from sentinelbench.types import AgentPrediction


class OpenAIProvider(ModelProvider):
    """OpenAI adapter placeholder. Full implementation tracked in issue #11."""

    name = "openai"

    def __init__(self, *, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def investigate(self, incident: Mapping[str, Any]) -> AgentPrediction:
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Use MockProvider for offline runs."
            )
        raise NotImplementedError(
            "OpenAIProvider adapter is not implemented yet "
            "(see GitHub issue #11). Use MockProvider for offline evaluation."
        )
