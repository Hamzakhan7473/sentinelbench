# SentinelBench Product Roadmap

**Audience:** Frontier AI labs + AI/security startups that need a *reliable* evaluation product for evidence-grounded security agents.  
**Cyber lead:** [@ayeshasq](https://github.com/ayeshasq) (scenario design, threat model, ATT&CK realism, dual-use review).  
**Eng lead:** [@Hamzakhan7473](https://github.com/Hamzakhan7473) (harness, scorers, providers, reports, CI).  
**Platform:** [@prtknk](https://github.com/prtknk) (OpenAI adapter, report polish, infra).

**Why now:** The [OpenAI–Hugging Face eval-escape incident](https://openai.com/index/hugging-face-model-evaluation-security-incident/) proved that cyber-capable agents will *optimize the score*, including by leaving the sandbox. Labs and startups need an independent, evidence-backed, containment-aware eval product — not another saturated CTF quiz.

---

## Product thesis

**SentinelBench is the evaluation product that answers three buyer questions:**

1. **SOC / IR AI:** Does the agent ground decisions in evidence (cite the right events, map ATT&CK, avoid hallucination & unsafe containment)?
2. **Eval integrity:** Does the agent try to cheat — egress, reward-hack, exfiltrate answers, ignore harness rules?
3. **Agentic intrusion response:** Would the agent recognize an *AI-led* campaign (swarm sandboxes, high action volume, self-migrating C2) like the HF-style attacker?

We deliberately **do not** compete with live offensive ranges like [FrontierCyber](https://www.irregular.com/research/frontiercyber) / CasabaCyberBench on “break into real systems.” Our wedge is **deterministic, auditable, evidence-grounded scoring** that labs and startups can run offline-first, ship in CI, and trust in a safety case.

---

## Who the product is for

| Buyer | Job to be done | Why they pay |
|-------|----------------|--------------|
| **Frontier AI labs** | Pre-deploy / continuous cyber-agent eval with transcripts + scores | Safety case, board/regulatory readiness, catch reward hacking before production |
| **AI security startups** | Prove their SOC/IR agents work on shared + private scenarios | Sales proof, regression CI, investor diligence |
| **Enterprise SOC platforms** | Vendor bake-offs for “AI analyst” features | Procurement evidence, false-positive cost control |
| **AISI / eval orgs** | Reproducible third-party packs | Independent measurement (Inspect/Hawk-compatible later) |

**Beachhead (90 days):** AI security startups + lab eval teams who already run mock/offline harnesses and need a **named, citable benchmark** with open methodology.

---

## What “perfect / reliable” means (non‑negotiables)

| Pillar | Requirement | Status today |
|--------|-------------|--------------|
| **Reproducible** | Same incident + same provider mode → same deterministic scores | Partial (mock + scorers) |
| **Evidence-first** | Scores require event IDs / ATT&CK / schema validity | Done (v1 scorers) |
| **Offline-first** | CI green with zero API keys | Done (mock + GitHub Actions) |
| **Safe to publish** | Synthetic scenarios; no live exploit PoCs; dual-use review | Seed pack exists; policy TBD |
| **Containment-aware** | Detect egress / cheat / unsafe actions | Unsafe + hallucination started; eval-integrity track TBD |
| **Buyer-grade reports** | JSON + Markdown; category breakdown; failure examples | Done (v1); hosted UI later |
| **Provider coverage** | OpenAI / Anthropic / Gemini + mock | Stubs; OpenAI adapter open (#11) |
| **Cyber realism** | ATT&CK-aligned scenarios authored by security expertise | Seed + adversarial starters; Ayesha expands |

---

## Competitive position (build against this)

| Player | They optimize for | We win by |
|--------|-------------------|-----------|
| ExploitGym / offensive cyber benches | Capability to exploit | Measuring *integrity* + *evidence grounding*, not raw offense |
| FrontierCyber / Casaba | Live real-system offense | Faster, safer, CI-native, transcript-auditable SOC/eval integrity |
| Inspect + Hawk | General eval infra | Domain pack + scorers + scenarios labs plug *into* Inspect later |
| Generic LLM safety benches | Jailbreaks / refusal | Security-operations + agentic-attacker realism |

**Category line:** *Evidence-grounded security agent evaluation — SOC quality + eval integrity.*

---

## Roadmap phases

### Phase 0 — Foundation (done)

- Incident schema, mock provider, deterministic scorers, CLI, CI  
- Seed SOC scenarios + starter adversarial fixtures  
- Methodology v1 + architecture docs  

### Phase 1 — Reliable core product (Weeks 1–3) — **BUILD NOW**

**Outcome:** A startup or lab can `pip install`, validate scenarios, run mock + one live provider, and export a board-ready report.

| Workstream | Owner | Build items |
|------------|-------|-------------|
| Cyber scenario pack v1.1 | **Ayesha** | Harden 5 SOC seeds; finish adversarial pack (#6); ATT&CK QA; dual-use checklist |
| Live providers | Hamza + Pratik | Ship OpenAI adapter (#11); Anthropic/Gemini thin adapters; secret-safe config |
| Product packaging | Hamza | Versioned release `0.2.0`; changelog; `docs/quickstart.md` for lab/startup users |
| Trust surface | **Ayesha** | Publish policy in SECURITY.md / data/README (what we never ship) |
| Demo | Both | Failure screenshot + 2‑min walkthrough (#8) |

**Exit criteria**

- [ ] `sentinelbench run` works on seed pack with mock **and** OpenAI  
- [ ] `sentinelbench validate` required in CONTRIBUTING + CI (done)  
- [ ] Public quickstart a stranger can finish in &lt;15 minutes  
- [ ] Dual-use publishing rules written by cyber lead  

### Phase 2 — Frontier differentiators (Weeks 4–8)

**Outcome:** Two product tracks buyers ask for after the OpenAI–HF incident.

| Track | Owner | Build items |
|-------|-------|-------------|
| **Eval Integrity** | Ayesha (design) → Hamza (scorers) | Scenarios: ignore-harness, fake answer lookup, egress-seeking logs, score-tamper narrative; metrics: `reward_hacking_detected`, `sandbox_egress_attempt`, `external_solution_lookup` |
| **Agentic Intrusion Response** | **Ayesha** | Synthetic swarm/C2/high-volume action incidents; investigation steps a human SOC would take; tags `agentic-intrusion` |
| Taxonomy + metadata | **Ayesha** | Tracks in `metadata.tags` / `dataset_split`; catalog table in data/README |
| Rubric v2 | Ayesha + Hamza | Document weights; implement new deterministic metrics; keep CI offline |
| Report v2 | Pratik | “Sentinel Score” summary; cheat vs miss vs unsafe failure classes (#12) |

**Exit criteria**

- [ ] ≥10 eval-integrity + ≥5 agentic-IR scenarios, all validate  
- [ ] Rubric v2 in methodology + tests  
- [ ] One public “incident-inspired” blog/demo that does **not** include exploit PoCs  

### Phase 3 — Lab-grade reliability (Weeks 9–12)

**Outcome:** Frontier labs can trust results in a safety review.

| Workstream | Owner | Build items |
|------------|-------|-------------|
| Reproducibility | Hamza | Locked scenario snapshots (`snapshot_id`, schema_version); run manifests |
| Multi-run stats | Hamza | Optional bootstrap CIs (field already reserved) |
| Inspect export (optional) | Hamza | Adapter notes / thin export so labs using Inspect can load our tasks |
| Private packs | Ayesha + Hamza | Partner-only scenario tier (not in public git); license + access model |
| Hosted report MVP | Pratik | Static site or simple API: upload JSON report → shareable link |

**Exit criteria**

- [ ] Snapshoted eval packs with changelog  
- [ ] Private-pack path documented  
- [ ] At least one design partner (startup or lab eval team) running weekly  

### Phase 4 — Startup scale (Quarter 2)

- Hosted eval API (queue runs, store transcripts, RBAC)  
- Leaderboard (public SOC track only; integrity track gated)  
- Enterprise: SSO, retention controls, redaction helpers  
- Paid private scenario authoring with Ayesha’s cyber review as the quality gate  

---

## Ayesha swimlane (cybersecurity)

Because Ayesha is MS Cybersecurity / SOC-oriented, she owns the **trust + realism** half of the product:

1. **Scenario truth** — labels, severity, ATT&CK, supporting event IDs, investigation/containment expectations  
2. **Dual-use gate** — reject anything that is a usable exploit recipe  
3. **Incident-derived tracks** — Eval Integrity + Agentic IR without copying live attack tooling  
4. **Threat model** — keep `docs/threat-model.md` current for buyers  
5. **Customer language** — translate lab/SOC needs into scenario acceptance tests  

Engineering implements harness/scorers/providers from her specs — she does not need to own Python platform code to be the product’s cyber authority.

---

## 90-day milestone board

| Week | Milestone | Primary owners |
|------|-----------|----------------|
| 1 | Quickstart + OpenAI provider usable | Hamza, Pratik |
| 2 | Adversarial pack complete + publishing policy | Ayesha |
| 3 | Demo video + design-partner outreach list | Both |
| 4–5 | Eval Integrity scenarios v0 + scorers | Ayesha → Hamza |
| 6–7 | Agentic IR scenarios v0 | Ayesha |
| 8 | Rubric v2 + report failure classes | Ayesha, Hamza, Pratik |
| 9–10 | Snapshots + reproducibility manifest | Hamza |
| 11 | First external design-partner run | All |
| 12 | v0.3 release + public writeup | All |

---

## North-star metrics

1. **Evidence F1** (event_ids) mean on SOC track — quality of grounding  
2. **Cheat-catch rate** on Eval Integrity track — % of planted cheating behaviors detected  
3. **Time-to-first-report** for a new user — &lt;15 minutes  
4. **Weekly active design partners** — retention signal  

---

## Kill / pivot criteria

- If we cannot ship a live provider + quickstart in 3 weeks → packaging problem, fix before new tracks  
- If scenarios require real exploit code to be “interesting” → wrong wedge; stay synthetic/evidence-focused  
- If labs only want live offensive ranges → partner/export to Inspect+range vendors; don’t rebuild FrontierCyber  

---

## Immediate next builds (this week)

1. `docs/quickstart.md` for labs/startups  
2. Finish OpenAI provider (#11)  
3. Ayesha: close adversarial pack (#6) + draft publishing policy  
4. Replace research-memo issues with **build tickets** mapped to Phase 1–2 (see GitHub milestone “Product Build”)  

Related incident context: [OpenAI disclosure](https://openai.com/index/hugging-face-model-evaluation-security-incident/).  
Related product vision: [product-vision.md](product-vision.md).
