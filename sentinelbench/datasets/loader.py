"""Dataset loading and incident schema validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator, Mapping

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "incident.schema.json"
DEFAULT_SCENARIOS_DIR = REPO_ROOT / "data" / "scenarios"


class IncidentValidationError(ValueError):
    """Raised when an incident fails schema validation."""


def load_schema(schema_path: Path | str | None = None) -> dict[str, Any]:
    path = Path(schema_path) if schema_path else DEFAULT_SCHEMA_PATH
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_incident(
    incident: Mapping[str, Any],
    *,
    schema: Mapping[str, Any] | None = None,
    schema_path: Path | str | None = None,
) -> None:
    """Validate an incident against the canonical JSON Schema."""
    resolved = dict(schema) if schema is not None else load_schema(schema_path)
    validator = Draft202012Validator(resolved)
    errors = sorted(validator.iter_errors(incident), key=lambda e: list(e.path))
    if errors:
        messages = "; ".join(
            f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
            for err in errors
        )
        raise IncidentValidationError(messages)


def load_incident(
    path: Path | str,
    *,
    validate: bool = True,
    schema_path: Path | str | None = None,
) -> dict[str, Any]:
    """Load one incident JSON file."""
    file_path = Path(path)
    with file_path.open(encoding="utf-8") as handle:
        incident = json.load(handle)
    if validate:
        validate_incident(incident, schema_path=schema_path)
    return incident


def iter_incidents(
    directory: Path | str | None = None,
    *,
    validate: bool = True,
    schema_path: Path | str | None = None,
) -> Iterator[dict[str, Any]]:
    """Yield validated incidents from a scenarios directory (``*.json``)."""
    root = Path(directory) if directory else DEFAULT_SCENARIOS_DIR
    for path in sorted(root.glob("*.json")):
        yield load_incident(path, validate=validate, schema_path=schema_path)


def load_incidents(
    directory: Path | str | None = None,
    *,
    validate: bool = True,
    schema_path: Path | str | None = None,
) -> list[dict[str, Any]]:
    return list(
        iter_incidents(directory, validate=validate, schema_path=schema_path)
    )
