"""Shared types for SentinelBench evaluations."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Mapping, Sequence

Label = Literal["benign", "malicious"]
Severity = Literal["informational", "low", "medium", "high", "critical"]


@dataclass(frozen=True)
class AgentPrediction:
    """Structured investigation output produced by a model provider."""

    label: Label
    severity: Severity
    attack_technique_ids: Sequence[str] = field(default_factory=list)
    supporting_event_ids: Sequence[str] = field(default_factory=list)
    investigation_steps: Sequence[str] = field(default_factory=list)
    containment_actions: Sequence[str] = field(default_factory=list)
    raw: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if payload["raw"] is None:
            del payload["raw"]
        return payload


@dataclass(frozen=True)
class ScoreResult:
    """Single metric result from a scorer."""

    name: str
    score: float
    detail: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "score": self.score, "detail": dict(self.detail)}


@dataclass(frozen=True)
class IncidentResult:
    """Full evaluation result for one incident."""

    incident_id: str
    provider: str
    prediction: AgentPrediction
    scores: Sequence[ScoreResult]
    latency_ms: float
    cost_usd: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "provider": self.provider,
            "prediction": self.prediction.to_dict(),
            "scores": [s.to_dict() for s in self.scores],
            "latency_ms": self.latency_ms,
            "cost_usd": self.cost_usd,
            "overall_score": overall_score(self.scores),
        }


def overall_score(scores: Sequence[ScoreResult]) -> float:
    if not scores:
        return 0.0
    return sum(s.score for s in scores) / len(scores)
