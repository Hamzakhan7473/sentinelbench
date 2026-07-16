# SentinelBench

An open-source benchmark for evaluating evidence-grounded AI agents in security operations.

## Overview

SentinelBench provides datasets, scorers, and runners for measuring how well agents ground decisions in evidence under security-operations scenarios. This repository currently contains the project skeleton only — approved public datasets will be added later.

## Status

**Early scaffolding.** Structure and documentation placeholders are in place. No evaluation datasets or scoring implementations have been shipped yet.

## Repository layout

```
sentinelbench/
├── docs/           # Architecture, methodology, and threat model
├── data/           # Scenarios and schemas (datasets added later)
├── sentinelbench/  # Python package (models, scorers, datasets, runners)
├── tests/
├── examples/
└── results/
```

## Getting started

```bash
# Install in editable mode (once dependencies are defined)
pip install -e .
```

Copy `.env.example` to `.env` and fill in any required values before running evaluations.

## Documentation

- [Architecture](docs/architecture.md)
- [Methodology](docs/methodology.md)
- [Threat model](docs/threat-model.md)
- [Data guidelines](data/README.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please read [SECURITY.md](SECURITY.md) before reporting vulnerabilities or contributing security-related content.

## License

See [LICENSE](LICENSE).
