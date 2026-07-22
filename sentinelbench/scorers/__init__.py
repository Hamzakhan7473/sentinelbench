"""Deterministic scorers for classification, evidence, ATT&CK, severity, schema."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from sentinelbench.scorers.metrics import exact_match, set_precision_recall_f1
from sentinelbench.types import AgentPrediction, ScoreResult

PREDICTION_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "SentinelBench Agent Prediction",
    "type": "object",
    "additionalProperties": True,
    "required": [
        "label",
        "severity",
        "attack_technique_ids",
        "supporting_event_ids",
    ],
    "properties": {
        "label": {"type": "string", "enum": ["benign", "malicious"]},
        "severity": {
            "type": "string",
            "enum": ["informational", "low", "medium", "high", "critical"],
        },
        "attack_technique_ids": {
            "type": "array",
            "items": {"type": "string", "pattern": "^T\\d{4}(\\.\\d{3})?$"},
        },
        "supporting_event_ids": {
            "type": "array",
            "items": {"type": "string"},
        },
        "investigation_steps": {"type": "array", "items": {"type": "string"}},
        "containment_actions": {"type": "array", "items": {"type": "string"}},
    },
}


def score_classification(
    prediction: AgentPrediction,
    incident: Mapping[str, Any],
) -> ScoreResult:
    score = exact_match(prediction.label, incident["label"])
    return ScoreResult(
        name="classification",
        score=score,
        detail={"predicted": prediction.label, "expected": incident["label"]},
    )


def score_severity(
    prediction: AgentPrediction,
    incident: Mapping[str, Any],
) -> ScoreResult:
    score = exact_match(prediction.severity, incident["severity"])
    return ScoreResult(
        name="severity",
        score=score,
        detail={
            "predicted": prediction.severity,
            "expected": incident["severity"],
        },
    )


def score_event_ids(
    prediction: AgentPrediction,
    incident: Mapping[str, Any],
) -> ScoreResult:
    metrics = set_precision_recall_f1(
        prediction.supporting_event_ids,
        incident.get("supporting_event_ids") or [],
    )
    return ScoreResult(
        name="event_ids",
        score=metrics["f1"],
        detail=metrics,
    )


def score_attack_techniques(
    prediction: AgentPrediction,
    incident: Mapping[str, Any],
) -> ScoreResult:
    expected = [
        t["technique_id"] for t in (incident.get("attack_techniques") or [])
    ]
    metrics = set_precision_recall_f1(prediction.attack_technique_ids, expected)
    return ScoreResult(
        name="attack_techniques",
        score=metrics["f1"],
        detail=metrics,
    )


def score_prediction_schema(prediction: AgentPrediction) -> ScoreResult:
    payload = prediction.raw if prediction.raw is not None else prediction.to_dict()
    validator = Draft202012Validator(PREDICTION_SCHEMA)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    ok = not errors
    return ScoreResult(
        name="json_schema_validity",
        score=1.0 if ok else 0.0,
        detail={
            "valid": ok,
            "errors": [
                f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
                for err in errors
            ],
        },
    )


DEFAULT_SCORERS = (
    score_classification,
    score_severity,
    score_event_ids,
    score_attack_techniques,
    score_prediction_schema,
)


def score_incident(
    prediction: AgentPrediction,
    incident: Mapping[str, Any],
    *,
    scorers: Sequence[Any] | None = None,
) -> list[ScoreResult]:
    selected = scorers if scorers is not None else DEFAULT_SCORERS
    results: list[ScoreResult] = []
    for scorer in selected:
        if scorer is score_prediction_schema:
            results.append(scorer(prediction))
        else:
            results.append(scorer(prediction, incident))
    return results
