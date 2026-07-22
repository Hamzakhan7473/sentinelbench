"""Optional cloud provider stubs (implement when API keys are configured)."""

from __future__ import annotations

from typing import Any, Mapping

from sentinelbench.models.base import ModelProvider
from sentinelbench.types import AgentPrediction


class _UnimplementedProvider(ModelProvider):
    def investigate(self, incident: Mapping[str, Any]) -> AgentPrediction:
        raise NotImplementedError(
            f"{self.name} provider is not implemented yet. "
            "Use MockProvider for offline evaluation, or contribute an adapter."
        )


class OpenAIProvider(_UnimplementedProvider):
    name = "openai"


class AnthropicProvider(_UnimplementedProvider):
    name = "anthropic"


class GeminiProvider(_UnimplementedProvider):
    name = "gemini"
