# SentinelBench

An open-source benchmark for evaluating evidence-grounded AI agents in security operations.

## Overview

SentinelBench provides datasets, scorers, and runners for measuring how well agents ground decisions in evidence under security-operations scenarios.

## Status

**Core evaluation loop is runnable offline** with a mock provider (no API keys). Incident schema lives under `data/schemas/`. SOC scenarios and cloud providers are still in progress.

## Repository layout

```
sentinelbench/
├── docs/           # Architecture, methodology, and threat model
├── data/           # Scenarios and schemas
├── sentinelbench/  # Python package (models, scorers, datasets, runners)
├── tests/
├── examples/
└── results/
```

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run unit tests (mock provider, no API keys)
pytest

# Evaluate the example incident
python examples/run_mock_eval.py

# Validate seed scenarios (schema + event-id references)
sentinelbench validate --also-example

# Run mock eval over all scenarios
sentinelbench run --provider mock --mode oracle

# Or a single incident
sentinelbench run --incident data/schemas/examples/incident.example.json
```

Copy `.env.example` to `.env` before wiring real model providers.

## Documentation

- [Architecture](docs/architecture.md)
- [Methodology / scoring rubric](docs/methodology.md)
- [Threat model](docs/threat-model.md)
- [Example investigation](docs/example-investigation.md)
- [Demo checklist](docs/demo.md)
- [Technical report (draft)](docs/technical-report.md)
- [Data guidelines](data/README.md)
- [Incident schema](data/schemas/README.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please read [SECURITY.md](SECURITY.md) before reporting vulnerabilities or contributing security-related content.

## License

See [LICENSE](LICENSE).
