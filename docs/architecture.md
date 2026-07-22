# Architecture

SentinelBench evaluates evidence-grounded SOC agents with a simple pipeline:

```text
incident JSON  →  ModelProvider.investigate()  →  AgentPrediction
                         ↓
              deterministic scorers  →  IncidentResult / report JSON
```

## Components

| Package | Role |
|---------|------|
| `sentinelbench.datasets` | Load/validate incidents against `data/schemas/incident.schema.json` |
| `sentinelbench.models` | Provider interface (`MockProvider` + stubs for OpenAI/Anthropic/Gemini) |
| `sentinelbench.scorers` | Exact/set-based metrics (classification, severity, event IDs, ATT&CK, schema validity) |
| `sentinelbench.runners` | Orchestrate evaluate → score → write `results/` report |

## Offline path

`MockProvider(mode="oracle")` returns ground truth so CI and local demos run without API keys. Cloud adapters raise `NotImplementedError` until implemented.
