"""Tests for scenario QA validation."""

from __future__ import annotations

from pathlib import Path

from sentinelbench.datasets import (
    load_incident,
    validate_scenario_file,
    validate_scenarios,
)

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "data" / "scenarios"
EXAMPLE = ROOT / "data" / "schemas" / "examples" / "incident.example.json"


def test_seed_scenarios_validate() -> None:
    report = validate_scenarios(SCENARIOS, extra_paths=[EXAMPLE])
    assert report.checked >= 6
    assert report.ok, [issue.message for issue in report.issues]


def test_missing_event_id_detected(tmp_path: Path) -> None:
    incident = load_incident(EXAMPLE)
    incident["supporting_event_ids"] = ["evt-does-not-exist"]
    bad = tmp_path / "bad.json"
    import json

    bad.write_text(json.dumps(incident), encoding="utf-8")
    issues = validate_scenario_file(bad)
    assert issues
    assert "evt-does-not-exist" in issues[0].message
