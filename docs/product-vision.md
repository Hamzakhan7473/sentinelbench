# Product Vision — SentinelBench

## One-liner

**The evaluation product frontier AI labs and security startups rely on to prove their agents are evidence-grounded, cheat-resistant, and ready for real SOC workflows — without running unsafe live offense.**

## Problem

Frontier models are increasingly **agentic and cyber-capable**. Internal evals with guardrails disabled can produce catastrophic side effects (sandbox escape, external cheating), while SOC copilots still hallucinate evidence and recommend unsafe containment. Buyers need:

- Scores they can defend in a safety review  
- Transcripts tied to evidence IDs  
- Offline/CI runs that do not require a cyber range  
- Scenario packs authored with real security expertise  

## Solution

SentinelBench ships:

1. **Canonical incident schema** — evidence, labels, ATT&CK, expected investigation/containment  
2. **Deterministic scorers** — classification, evidence F1, ATT&CK, severity, hallucination, unsafe actions (+ integrity metrics next)  
3. **Providers** — mock (CI) + OpenAI/Anthropic/Gemini  
4. **Tracks** — SOC evidence · Eval integrity · Agentic intrusion response · Adversarial injection  
5. **Reports** — JSON + Markdown buyers can attach to diligence / model cards  

## Why startups and labs can rely on us

| Need | How we meet it |
|------|----------------|
| Reproducibility | Versioned schema + scenario snapshots + deterministic metrics |
| Safety | Synthetic fixtures; dual-use review by cybersecurity lead |
| Speed | `pip install` + CLI; green CI without keys |
| Credibility | Open methodology; ATT&CK-aligned scenarios |
| Extensibility | Private packs + future Inspect export |

## What we are not

- Not a live penetration platform  
- Not a jailbreak meme leaderboard  
- Not a replacement for lab-internal red teams — we are the **shared yardstick** and **regression harness**

## Brand promise

> If it passes SentinelBench’s SOC + Eval Integrity tracks, you have auditable evidence it cites real events, avoids unsafe actions, and does not treat your harness as something to escape.
