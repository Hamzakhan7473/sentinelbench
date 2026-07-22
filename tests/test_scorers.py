"""Tests for deterministic scorers."""

from __future__ import annotations

from pathlib import Path

from sentinelbench.datasets import load_incident
from sentinelbench.models import MockProvider
from sentinelbench.scorers import score_incident
from sentinelbench.types import AgentPrediction

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "data" / "schemas" / "examples" / "incident.example.json"


def test_oracle_scores_perfect() -> None:
    incident = load_incident(EXAMPLE)
    prediction = MockProvider(mode="oracle").investigate(incident)
    scores = {s.name: s.score for s in score_incident(prediction, incident)}
    assert scores["classification"] == 1.0
    assert scores["severity"] == 1.0
    assert scores["event_ids"] == 1.0
    assert scores["attack_techniques"] == 1.0
    assert scores["json_schema_validity"] == 1.0


def test_partial_event_id_overlap() -> None:
    incident = load_incident(EXAMPLE)
    prediction = AgentPrediction(
        label="malicious",
        severity="high",
        attack_technique_ids=["T1059.001"],
        supporting_event_ids=["evt-1", "evt-999"],
        raw={
            "label": "malicious",
            "severity": "high",
            "attack_technique_ids": ["T1059.001"],
            "supporting_event_ids": ["evt-1", "evt-999"],
        },
    )
    scores = {s.name: s for s in score_incident(prediction, incident)}
    assert scores["classification"].score == 1.0
    assert 0.0 < scores["event_ids"].score < 1.0
    assert scores["event_ids"].detail["precision"] == 0.5
    assert scores["event_ids"].detail["recall"] == 0.5
    assert scores["attack_techniques"].detail["recall"] == 0.5
