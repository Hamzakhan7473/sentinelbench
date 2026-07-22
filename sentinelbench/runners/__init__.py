"""Evaluation runners."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

from sentinelbench.models.base import ModelProvider
from sentinelbench.scorers import score_incident
from sentinelbench.types import IncidentResult, overall_score

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = REPO_ROOT / "results"


def evaluate_incident(
    incident: Mapping[str, Any],
    provider: ModelProvider,
    *,
    scorers: Sequence[Any] | None = None,
) -> IncidentResult:
    """Run one incident through a provider and deterministic scorers."""
    started = time.perf_counter()
    prediction = provider.investigate(incident)
    latency_ms = (time.perf_counter() - started) * 1000.0
    scores = score_incident(prediction, incident, scorers=scorers)
    return IncidentResult(
        incident_id=str(incident.get("incident_id", "unknown")),
        provider=provider.name,
        prediction=prediction,
        scores=scores,
        latency_ms=latency_ms,
        cost_usd=0.0,
    )


def evaluate_incidents(
    incidents: Sequence[Mapping[str, Any]],
    provider: ModelProvider,
    *,
    scorers: Sequence[Any] | None = None,
) -> list[IncidentResult]:
    return [
        evaluate_incident(incident, provider, scorers=scorers)
        for incident in incidents
    ]


def write_report(
    results: Sequence[IncidentResult],
    *,
    output_path: Path | str | None = None,
    results_dir: Path | str | None = None,
) -> Path:
    """Write a machine-readable evaluation report to ``results/``."""
    if output_path is None:
        directory = Path(results_dir) if results_dir else DEFAULT_RESULTS_DIR
        directory.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        provider = results[0].provider if results else "unknown"
        output_path = directory / f"report-{provider}-{stamp}.json"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "provider": results[0].provider if results else None,
        "n_incidents": len(results),
        "overall_score": (
            sum(overall_score(r.scores) for r in results) / len(results)
            if results
            else 0.0
        ),
        "mean_latency_ms": (
            sum(r.latency_ms for r in results) / len(results) if results else 0.0
        ),
        "total_cost_usd": sum(r.cost_usd for r in results),
        "incidents": [r.to_dict() for r in results],
    }
    with Path(output_path).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return Path(output_path)
