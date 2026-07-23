# Project demonstration checklist

Tracks Issue 8 deliverables.

| Deliverable | Status | Location |
|-------------|--------|----------|
| Architecture diagram | Done (Mermaid) | [`docs/architecture.md`](architecture.md) |
| Example investigation | Done | [`docs/example-investigation.md`](example-investigation.md) |
| Technical report (draft) | In progress | [`docs/technical-report.md`](technical-report.md) |
| Failure-analysis screenshot | TODO | Capture from `sentinelbench --mode empty` report Markdown/JSON |
| Two-minute video | TODO | Record walkthrough: schema → mock eval → failure contrast → report |

## Suggested video outline (2:00)

1. Problem (0:20) — SOC agents must cite evidence, not hallucinate  
2. Schema (0:20) — incident fields / evidence grounding  
3. Offline eval (0:40) — `run_mock_eval.py` perfect oracle  
4. Failure mode (0:25) — empty mock + report failure examples  
5. Roadmap (0:15) — scenarios, real providers, adversarial cases  
