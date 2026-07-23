"""Optional Anthropic provider stub."""

from __future__ import annotations

import os
from typing import Any, Mapping

from sentinelbench.models.base import ModelProvider
from sentinelbench.types import AgentPrediction


class AnthropicProvider(ModelProvider):
    """Anthropic adapter placeholder."""

    name = "anthropic"

    def __init__(self, *, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

    def investigate(self, incident: Mapping[str, Any]) -> AgentPrediction:
        if not self.api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Use MockProvider for offline runs."
            )
        raise NotImplementedError(
            "AnthropicProvider adapter is not implemented yet. "
            "Use MockProvider for offline evaluation."
        )
