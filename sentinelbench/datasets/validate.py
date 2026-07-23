"""Scenario QA: schema + referential integrity checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from sentinelbench.datasets import (
    DEFAULT_SCENARIOS_DIR,
    IncidentValidationError,
    load_incident,
    load_incidents,
)


@dataclass
class ScenarioIssue:
    incident_id: str
    path: str
    message: str


@dataclass
class ScenarioValidationReport:
    checked: int = 0
    issues: list[ScenarioIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues


def _event_ids(incident: Mapping[str, Any]) -> set[str]:
    return {
        str(event["event_id"])
        for event in (incident.get("raw_events") or [])
        if event.get("event_id") is not None
    }


def check_referential_integrity(
    incident: Mapping[str, Any],
    *,
    path: str = "<memory>",
) -> list[ScenarioIssue]:
    """Ensure cited event IDs exist in raw_events."""
    incident_id = str(incident.get("incident_id", "unknown"))
    valid = _event_ids(incident)
    issues: list[ScenarioIssue] = []

    for event_id in incident.get("supporting_event_ids") or []:
        if str(event_id) not in valid:
            issues.append(
                ScenarioIssue(
                    incident_id=incident_id,
                    path=path,
                    message=f"supporting_event_ids references missing event_id '{event_id}'",
                )
            )

    for index, step in enumerate(incident.get("expected_investigation_steps") or []):
        for event_id in step.get("supporting_event_ids") or []:
            if str(event_id) not in valid:
                issues.append(
                    ScenarioIssue(
                        incident_id=incident_id,
                        path=path,
                        message=(
                            f"expected_investigation_steps[{index}].supporting_event_ids "
                            f"references missing event_id '{event_id}'"
                        ),
                    )
                )

    if len(valid) != len(incident.get("raw_events") or []):
        issues.append(
            ScenarioIssue(
                incident_id=incident_id,
                path=path,
                message="raw_events contains duplicate event_id values",
            )
        )

    return issues


def validate_scenario_file(path: Path | str) -> list[ScenarioIssue]:
    file_path = Path(path)
    try:
        incident = load_incident(file_path, validate=True)
    except (OSError, ValueError, IncidentValidationError) as exc:
        return [
            ScenarioIssue(
                incident_id=file_path.stem,
                path=str(file_path),
                message=f"schema/load error: {exc}",
            )
        ]
    return check_referential_integrity(incident, path=str(file_path))


def validate_scenarios(
    directory: Path | str | None = None,
    *,
    extra_paths: Sequence[Path | str] | None = None,
) -> ScenarioValidationReport:
    """Validate all `*.json` scenarios in a directory (plus optional extra files)."""
    report = ScenarioValidationReport()
    root = Path(directory) if directory else DEFAULT_SCENARIOS_DIR
    paths = sorted(root.glob("*.json")) if root.exists() else []
    for extra in extra_paths or []:
        paths.append(Path(extra))

    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen or not path.is_file():
            continue
        seen.add(resolved)
        report.checked += 1
        report.issues.extend(validate_scenario_file(path))
    return report
