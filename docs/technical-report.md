# SentinelBench Technical Report (draft)

## Abstract

SentinelBench is an open-source benchmark for evaluating whether AI agents investigating security-operations incidents remain **evidence-grounded**: correct classification and severity, accurate ATT&CK mapping, faithful event citations, low hallucination, and safe containment recommendations.

## System overview

See [`architecture.md`](architecture.md). The offline path uses `MockProvider` so unit tests and demos require no API keys.

## Data model

Canonical incident schema: [`../data/schemas/incident.schema.json`](../data/schemas/incident.schema.json). Design rationale: [`../data/schemas/README.md`](../data/schemas/README.md).

## Scoring

Official rubric and aggregation: [`methodology.md`](methodology.md).

## Current results (fixture)

On the synthetic phishing → PowerShell → C2 example:

- Oracle mock: overall score `1.0`
- Empty mock: overall score low (classification/evidence failures), illustrating failure-example reporting

## Limitations / next steps

- Expand SOC scenario pack (Issue 2)
- Real model providers (Issue 10 / OpenAI adapter)
- Adversarial log cases (Issue 6)
- Confidence intervals in reports (later)
- Demo video and failure screenshots (Issue 8)
