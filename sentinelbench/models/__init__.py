"""Provider registry."""

from __future__ import annotations

from sentinelbench.models.anthropic_provider import AnthropicProvider
from sentinelbench.models.base import ModelProvider, build_investigation_prompt
from sentinelbench.models.gemini_provider import GeminiProvider
from sentinelbench.models.mock import MockProvider
from sentinelbench.models.openai_provider import OpenAIProvider

__all__ = [
    "AnthropicProvider",
    "GeminiProvider",
    "MockProvider",
    "ModelProvider",
    "OpenAIProvider",
    "build_investigation_prompt",
    "get_provider",
]


def get_provider(name: str, **kwargs: object) -> ModelProvider:
    """Construct a provider by name."""
    key = name.lower().strip()
    if key in {"mock", "local"}:
        mode = str(kwargs.get("mode", "oracle"))
        fixed = kwargs.get("fixed_prediction")
        return MockProvider(mode=mode, fixed_prediction=fixed)  # type: ignore[arg-type]
    if key == "openai":
        return OpenAIProvider(
            api_key=kwargs.get("api_key"),  # type: ignore[arg-type]
            model=kwargs.get("model"),  # type: ignore[arg-type]
        )
    if key == "anthropic":
        return AnthropicProvider(
            api_key=kwargs.get("api_key"),  # type: ignore[arg-type]
            model=kwargs.get("model"),  # type: ignore[arg-type]
        )
    if key == "gemini":
        return GeminiProvider(
            api_key=kwargs.get("api_key"),  # type: ignore[arg-type]
            model=kwargs.get("model"),  # type: ignore[arg-type]
        )
    raise ValueError(f"Unknown provider: {name}")
