"""Tests for dataset loading and schema validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from sentinelbench.datasets import (
    IncidentValidationError,
    load_incident,
    validate_incident,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "data" / "schemas" / "examples" / "incident.example.json"


def test_load_example_incident() -> None:
    incident = load_incident(EXAMPLE)
    assert incident["incident_id"] == "sb-000123"
    assert incident["label"] == "malicious"


def test_invalid_incident_rejected() -> None:
    with pytest.raises(IncidentValidationError):
        validate_incident({"incident_id": "bad"})
