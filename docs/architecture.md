# Architecture

SentinelBench evaluates evidence-grounded SOC agents with a simple pipeline:

```mermaid
flowchart LR
  A[Incident JSON] --> B[ModelProvider.investigate]
  B --> C[AgentPrediction]
  C --> D[Deterministic scorers]
  D --> E[IncidentResult]
  E --> F[JSON + Markdown report]
```

## Components

| Package | Role |
|---------|------|
| `sentinelbench.datasets` | Load/validate incidents against `data/schemas/incident.schema.json` |
| `sentinelbench.models` | Provider interface (`MockProvider` + OpenAI/Anthropic/Gemini stubs) |
| `sentinelbench.scorers` | Exact/set-based metrics per `docs/methodology.md` |
| `sentinelbench.runners` | Orchestrate evaluate → score → write `results/` report |

## Offline path

`MockProvider(mode="oracle")` returns ground truth so CI and local demos run without API keys. Cloud adapters require env keys (see `.env.example`) and raise until implemented.
