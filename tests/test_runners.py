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
    path = write_report([result], output_path=out)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["n_incidents"] == 1
    assert payload["overall_score"] == 1.0
