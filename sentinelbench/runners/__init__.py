"""Evaluation runners and report writers."""

from __future__ import annotations

import json
import time
from collections import defaultdict
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


def _categories_for_incident(incident: Mapping[str, Any]) -> list[str]:
    metadata = incident.get("metadata") or {}
    tags = metadata.get("tags") or []
    if tags:
        return [str(tag) for tag in tags]
    techniques = incident.get("attack_techniques") or []
    tactics = [
        str(technique.get("tactic"))
        for technique in techniques
        if technique.get("tactic")
    ]
    if tactics:
        return sorted(set(tactics))
    if incident.get("label") == "benign":
        return ["benign"]
    return ["uncategorized"]


def build_report_payload(
    results: Sequence[IncidentResult],
    *,
    incidents: Sequence[Mapping[str, Any]] | None = None,
    failure_limit: int = 5,
) -> dict[str, Any]:
    """Build the machine-readable evaluation report structure."""
    incident_map = {
        str(incident.get("incident_id")): incident for incident in (incidents or [])
    }
    overall = (
        sum(overall_score(result.scores) for result in results) / len(results)
        if results
        else 0.0
    )
    by_category_scores: dict[str, list[float]] = defaultdict(list)
    for result in results:
        incident = incident_map.get(result.incident_id, {})
        for category in _categories_for_incident(incident):
            by_category_scores[category].append(overall_score(result.scores))

    by_attack_category = {
        category: {
            "n_incidents": len(scores),
            "mean_score": sum(scores) / len(scores) if scores else 0.0,
        }
        for category, scores in sorted(by_category_scores.items())
    }

    ranked = sorted(results, key=lambda item: overall_score(item.scores))
    failure_examples = [
        {
            "incident_id": result.incident_id,
            "overall_score": overall_score(result.scores),
            "scores": {score.name: score.score for score in result.scores},
            "prediction_summary": {
                "label": result.prediction.label,
                "severity": result.prediction.severity,
                "attack_technique_ids": list(result.prediction.attack_technique_ids),
                "supporting_event_ids": list(result.prediction.supporting_event_ids),
            },
        }
        for result in ranked[:failure_limit]
        if overall_score(result.scores) < 1.0
    ]

    metric_names = sorted(
        {score.name for result in results for score in result.scores}
    )
    metric_means = {
        name: (
            sum(
                next(s.score for s in result.scores if s.name == name)
                for result in results
                if any(s.name == name for s in result.scores)
            )
            / max(
                1,
                sum(1 for result in results if any(s.name == name for s in result.scores)),
            )
        )
        for name in metric_names
    }

    return {
        "provider": results[0].provider if results else None,
        "n_incidents": len(results),
        "overall_score": overall,
        "metric_means": metric_means,
        "by_attack_category": by_attack_category,
        "failure_examples": failure_examples,
        "cost_and_latency": {
            "mean_latency_ms": (
                sum(result.latency_ms for result in results) / len(results)
                if results
                else 0.0
            ),
            "total_latency_ms": sum(result.latency_ms for result in results),
            "total_cost_usd": sum(result.cost_usd for result in results),
            "mean_cost_usd": (
                sum(result.cost_usd for result in results) / len(results)
                if results
                else 0.0
            ),
        },
        "confidence_intervals": None,  # reserved for later
        "incidents": [result.to_dict() for result in results],
    }


def render_report_markdown(payload: Mapping[str, Any]) -> str:
    """Render a short human-readable summary of an evaluation report."""
    lines = [
        "# SentinelBench Evaluation Report",
        "",
        f"- Provider: `{payload.get('provider')}`",
        f"- Incidents: {payload.get('n_incidents', 0)}",
        f"- Overall score: {float(payload.get('overall_score') or 0.0):.3f}",
        "",
        "## Cost and latency",
        "",
    ]
    cost = payload.get("cost_and_latency") or {}
    lines.extend(
        [
            f"- Mean latency (ms): {float(cost.get('mean_latency_ms') or 0.0):.2f}",
            f"- Total cost (USD): {float(cost.get('total_cost_usd') or 0.0):.4f}",
            "",
            "## Results by attack category",
            "",
        ]
    )
    categories = payload.get("by_attack_category") or {}
    if not categories:
        lines.append("_No category breakdown available (pass incidents into write_report)._")
    else:
        for name, stats in categories.items():
            lines.append(
                f"- `{name}`: mean={float(stats['mean_score']):.3f} "
                f"(n={stats['n_incidents']})"
            )

    lines.extend(["", "## Failure examples", ""])
    failures = payload.get("failure_examples") or []
    if not failures:
        lines.append("_No failures (all incidents scored 1.0)._")
    else:
        for failure in failures:
            lines.append(
                f"- `{failure['incident_id']}` overall={float(failure['overall_score']):.3f}"
            )
            scores = failure.get("scores") or {}
            detail = ", ".join(f"{k}={float(v):.2f}" for k, v in scores.items())
            lines.append(f"  - scores: {detail}")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Confidence intervals are reserved for a later revision.",
            "- Failure examples are synthetic-safe summaries (no raw secrets).",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(
    results: Sequence[IncidentResult],
    *,
    output_path: Path | str | None = None,
    results_dir: Path | str | None = None,
    incidents: Sequence[Mapping[str, Any]] | None = None,
    write_markdown: bool = True,
) -> Path:
    """Write machine-readable JSON (and optional Markdown) evaluation reports."""
    if output_path is None:
        directory = Path(results_dir) if results_dir else DEFAULT_RESULTS_DIR
        directory.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        provider = results[0].provider if results else "unknown"
        output_path = directory / f"report-{provider}-{stamp}.json"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = build_report_payload(results, incidents=incidents)
    with Path(output_path).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")

    if write_markdown:
        markdown_path = Path(output_path).with_suffix(".md")
        markdown_path.write_text(render_report_markdown(payload), encoding="utf-8")

    return Path(output_path)
