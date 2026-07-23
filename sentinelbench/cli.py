"""CLI for offline evaluations and scenario QA."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sentinelbench.datasets import DEFAULT_SCHEMA_PATH, load_incident, load_incidents
from sentinelbench.datasets.validate import validate_scenarios
from sentinelbench.models import get_provider
from sentinelbench.runners import evaluate_incidents, write_report

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INCIDENT = (
    REPO_ROOT / "data" / "schemas" / "examples" / "incident.example.json"
)


def _add_run_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--incident",
        type=Path,
        help="Path to a single incident JSON file.",
    )
    parser.add_argument(
        "--scenarios-dir",
        type=Path,
        help="Directory of incident JSON files (default: data/scenarios).",
    )
    parser.add_argument(
        "--provider",
        default="mock",
        help="Provider name (default: mock).",
    )
    parser.add_argument(
        "--mode",
        default="oracle",
        choices=["oracle", "fixed", "empty"],
        help="Mock provider mode (default: oracle).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional report output path.",
    )


def _cmd_run(args: argparse.Namespace) -> int:
    if args.incident:
        incidents = [load_incident(args.incident)]
    else:
        incidents = load_incidents(args.scenarios_dir)

    if not incidents:
        raise SystemExit(
            "No incidents found. Pass --incident or add JSON files under data/scenarios/."
        )

    provider = get_provider(args.provider, mode=args.mode)
    results = evaluate_incidents(incidents, provider)
    path = write_report(results, output_path=args.output, incidents=incidents)
    overall = sum(r.to_dict()["overall_score"] for r in results) / len(results)
    print(f"Evaluated {len(results)} incident(s) with provider={provider.name}")
    print(f"Overall score: {overall:.3f}")
    print(f"Report written to: {path}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    extras: list[Path] = []
    if args.also_example:
        extras.append(EXAMPLE_INCIDENT)
    if args.incident:
        extras.append(args.incident)

    report = validate_scenarios(args.scenarios_dir, extra_paths=extras)
    print(
        f"Checked {report.checked} file(s) against {DEFAULT_SCHEMA_PATH.name} "
        "+ referential integrity"
    )
    if report.ok:
        print("OK: all scenarios valid")
        return 0

    for issue in report.issues:
        print(f"ERROR [{issue.incident_id}] {issue.path}: {issue.message}")
    print(f"FAILED: {len(report.issues)} issue(s)")
    return 1


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if not raw or raw[0] not in {"run", "validate"}:
        raw = ["run", *raw]

    parser = argparse.ArgumentParser(
        prog="sentinelbench",
        description="SentinelBench evaluation and scenario QA tools.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run", help="Evaluate incidents with a model provider."
    )
    _add_run_arguments(run_parser)
    run_parser.set_defaults(func=_cmd_run)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate scenario JSON files (schema + event-id references).",
    )
    validate_parser.add_argument(
        "--scenarios-dir",
        type=Path,
        help="Directory of incident JSON files (default: data/scenarios).",
    )
    validate_parser.add_argument(
        "--incident",
        type=Path,
        help="Also validate a specific incident file.",
    )
    validate_parser.add_argument(
        "--also-example",
        action="store_true",
        help="Also validate data/schemas/examples/incident.example.json.",
    )
    validate_parser.set_defaults(func=_cmd_validate)

    args = parser.parse_args(raw)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
