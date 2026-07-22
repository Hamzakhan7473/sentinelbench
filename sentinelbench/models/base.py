"""Model provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from sentinelbench.types import AgentPrediction


class ModelProvider(ABC):
    """Common interface for OpenAI, Anthropic, Gemini, and local/mock backends."""

    name: str

    @abstractmethod
    def investigate(self, incident: Mapping[str, Any]) -> AgentPrediction:
        """Return a structured investigation prediction for one incident."""


def build_investigation_prompt(incident: Mapping[str, Any]) -> str:
    """Build a neutral prompt from incident evidence (no ground-truth labels)."""
    events = incident.get("raw_events", [])
    source = incident.get("event_source", {})
    lines = [
        "You are a SOC analyst. Investigate the following incident evidence.",
        "Respond with structured findings: label (benign|malicious), severity,",
        "ATT&CK technique IDs, supporting event IDs, investigation steps, and containment actions.",
        "",
        f"Incident ID: {incident.get('incident_id', 'unknown')}",
        f"Event source: {source.get('type', 'unknown')} / {source.get('name', 'unknown')}",
        "",
        "Raw events:",
    ]
    for event in events:
        lines.append(
            f"- {event.get('event_id')}: {event.get('timestamp')} :: {event.get('raw')}"
        )
    return "\n".join(lines)
