"""Minimal CLI for offline mock evaluations."""

from __future__ import annotations

import argparse
from pathlib import Path

from sentinelbench.datasets import load_incident, load_incidents
from sentinelbench.models import get_provider
from sentinelbench.runners import evaluate_incidents, write_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sentinelbench",
        description="Run SentinelBench evaluations (mock provider by default).",
    )
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
    args = parser.parse_args(argv)

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


if __name__ == "__main__":
    raise SystemExit(main())
