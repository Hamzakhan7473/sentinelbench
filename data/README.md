# Data

This directory holds **approved public datasets** and related assets for SentinelBench. No security datasets are shipped in the initial scaffold.

## Where datasets will come from

Approved public datasets will be sourced from:

1. **Curated public benchmarks** with clear licenses (for example, established open evaluation suites for robustness, safety, or security-relevant behaviors).
2. **Explicitly licensed open corpora** published by research groups, standards bodies, or community projects that permit redistribution or documented download.
3. **SentinelBench-authored scenarios** released under this repository’s license, after review against [SECURITY.md](../SECURITY.md).

Datasets will **not** include:

- Proprietary or confidential incident data
- Unlicensed scraped content
- Live malware, weaponized exploit code, or credentials from real systems

## Layout

| Path | Purpose |
|------|---------|
| `scenarios/` | Scenario definitions and fixtures (added when approved) |
| `schemas/` | JSON/YAML schemas for scenario and result formats |

## Adding data

Before adding any dataset:

1. Confirm public availability and license compatibility.
2. Document provenance, version, and citation in this README or a per-dataset note.
3. Prefer references/download scripts over committing large binary blobs when appropriate.

Until then, `scenarios/` and `schemas/` remain empty placeholders.
