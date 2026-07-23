"""Tests for mock provider and stubs."""

from __future__ import annotations

from pathlib import Path

import pytest

from sentinelbench.datasets import load_incident
from sentinelbench.models import (
    AnthropicProvider,
    GeminiProvider,
    MockProvider,
    OpenAIProvider,
    get_provider,
)
from sentinelbench.types import AgentPrediction

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "data" / "schemas" / "examples" / "incident.example.json"


def test_mock_oracle_matches_ground_truth() -> None:
    incident = load_incident(EXAMPLE)
    prediction = MockProvider(mode="oracle").investigate(incident)
    assert prediction.label == incident["label"]
    assert prediction.severity == incident["severity"]
    assert list(prediction.attack_technique_ids) == [
        "T1566.001",
        "T1059.001",
    ]


def test_mock_empty_baseline() -> None:
    incident = load_incident(EXAMPLE)
    prediction = MockProvider(mode="empty").investigate(incident)
    assert prediction.label == "benign"
    assert prediction.supporting_event_ids == []


def test_get_provider_mock() -> None:
    provider = get_provider("mock", mode="oracle")
    assert isinstance(provider, MockProvider)


def test_cloud_stubs_require_keys_or_are_unimplemented() -> None:
    incident = load_incident(EXAMPLE)
    for cls in (OpenAIProvider, AnthropicProvider, GeminiProvider):
        with pytest.raises(RuntimeError):
            cls(api_key=None).investigate(incident)
        with pytest.raises(NotImplementedError):
            cls(api_key="test-key").investigate(incident)


def test_fixed_mode_requires_prediction() -> None:
    with pytest.raises(ValueError):
        MockProvider(mode="fixed")


def test_fixed_mode() -> None:
    fixed = AgentPrediction(label="benign", severity="low")
    provider = MockProvider(mode="fixed", fixed_prediction=fixed)
    incident = load_incident(EXAMPLE)
    assert provider.investigate(incident).label == "benign"
