"""Deterministic mock provider for offline tests and demos."""

from __future__ import annotations

from typing import Any, Mapping

from sentinelbench.models.base import ModelProvider
from sentinelbench.types import AgentPrediction, Label, Severity


class MockProvider(ModelProvider):
    """
    Local provider that needs no API keys.

    Modes:
    - ``oracle``: return ground truth from the incident (perfect score baseline).
    - ``fixed``: return a caller-supplied prediction for every incident.
    - ``empty``: return a minimal benign/informational prediction (weak baseline).
    """

    name = "mock"

    def __init__(
        self,
        *,
        mode: str = "oracle",
        fixed_prediction: AgentPrediction | None = None,
    ) -> None:
        if mode not in {"oracle", "fixed", "empty"}:
            raise ValueError(f"Unsupported mock mode: {mode}")
        if mode == "fixed" and fixed_prediction is None:
            raise ValueError("fixed mode requires fixed_prediction")
        self.mode = mode
        self.fixed_prediction = fixed_prediction

    def investigate(self, incident: Mapping[str, Any]) -> AgentPrediction:
        if self.mode == "fixed":
            assert self.fixed_prediction is not None
            return self.fixed_prediction
        if self.mode == "empty":
            return AgentPrediction(
                label="benign",
                severity="informational",
                attack_technique_ids=[],
                supporting_event_ids=[],
                investigation_steps=[],
                containment_actions=[],
            )
        return self._from_ground_truth(incident)

    @staticmethod
    def _from_ground_truth(incident: Mapping[str, Any]) -> AgentPrediction:
        techniques = incident.get("attack_techniques") or []
        steps = incident.get("expected_investigation_steps") or []
        actions = incident.get("expected_containment_actions") or []
        label: Label = incident["label"]
        severity: Severity = incident["severity"]
        technique_ids = [t["technique_id"] for t in techniques]
        event_ids = list(incident.get("supporting_event_ids") or [])
        investigation_steps = [s["step"] for s in steps]
        containment_actions = [a["action"] for a in actions]
        raw = {
            "label": label,
            "severity": severity,
            "attack_technique_ids": technique_ids,
            "supporting_event_ids": event_ids,
            "investigation_steps": investigation_steps,
            "containment_actions": containment_actions,
        }
        return AgentPrediction(
            label=label,
            severity=severity,
            attack_technique_ids=technique_ids,
            supporting_event_ids=event_ids,
            investigation_steps=investigation_steps,
            containment_actions=containment_actions,
            raw=raw,
        )
