"""Tests for evaluation runner."""

from __future__ import annotations

import json
from pathlib import Path

from sentinelbench.datasets import load_incident
from sentinelbench.models import MockProvider
from sentinelbench.runners import evaluate_incident, write_report

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "data" / "schemas" / "examples" / "incident.example.json"


def test_evaluate_and_write_report(tmp_path: Path) -> None:
    incident = load_incident(EXAMPLE)
    result = evaluate_incident(incident, MockProvider(mode="oracle"))
    assert result.incident_id == "sb-000123"
    assert result.to_dict()["overall_score"] == 1.0

    out = tmp_path / "report.json"
    path = write_report([result], output_path=out, incidents=[incident])
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["n_incidents"] == 1
    assert payload["overall_score"] == 1.0
    assert "phishing" in payload["by_attack_category"]
    assert payload["failure_examples"] == []
    assert payload["cost_and_latency"]["mean_latency_ms"] >= 0.0
    assert payload["confidence_intervals"] is None
    markdown = out.with_suffix(".md")
    assert markdown.exists()
    assert "Overall score" in markdown.read_text(encoding="utf-8")


def test_report_includes_failures(tmp_path: Path) -> None:
    incident = load_incident(EXAMPLE)
    result = evaluate_incident(incident, MockProvider(mode="empty"))
    path = write_report(
        [result],
        output_path=tmp_path / "fail.json",
        incidents=[incident],
    )
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["failure_examples"]
    assert payload["overall_score"] < 1.0
