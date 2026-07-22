"""Example: run a mock evaluation against the schema example incident."""

from __future__ import annotations

from pathlib import Path

from sentinelbench.datasets import load_incident
from sentinelbench.models import MockProvider
from sentinelbench.runners import evaluate_incident, write_report

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "data" / "schemas" / "examples" / "incident.example.json"


def main() -> None:
    incident = load_incident(EXAMPLE)
    provider = MockProvider(mode="oracle")
    result = evaluate_incident(incident, provider)
    report_path = write_report([result], output_path=ROOT / "results" / "example-mock.json")
    print(f"incident_id={result.incident_id}")
    for score in result.scores:
        print(f"  {score.name}: {score.score:.3f}")
    print(f"overall={result.to_dict()['overall_score']:.3f}")
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
