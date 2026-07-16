# Contributing to SentinelBench

Thanks for your interest in contributing. This project is in early scaffolding; contributions that improve structure, docs, and tooling are welcome.

## Before you start

1. Read [SECURITY.md](SECURITY.md) and [data/README.md](data/README.md).
2. Do **not** commit proprietary, private, or unapproved security datasets.
3. Prefer small, focused pull requests.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Guidelines

- Follow existing package layout under `sentinelbench/`.
- Add or update tests under `tests/` for new behavior.
- Document user-facing changes in `docs/` when relevant.
- Keep secrets out of the repo; use `.env` (see `.env.example`).

## Pull requests

- Describe what changed and why.
- Note any new dependencies or configuration.
- Confirm no unapproved datasets or secrets are included.

## Questions

Open an issue for design discussion before large changes.
