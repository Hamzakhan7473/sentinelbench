# Schemas

This directory holds JSON Schemas for SentinelBench data formats.

## `incident.schema.json`

The canonical incident record used by scenarios and scorers. Every SentinelBench
scenario is one or more incidents conforming to this schema.

### Field summary

| Field | Purpose |
|---|---|
| `incident_id` | Unique ID for the incident. |
| `event_source` | Provenance of the raw events (type, name, license, source URL). |
| `raw_events` | The evidence itself — an ordered list of events, each with an `event_id` and `timestamp`. Payload shape (`raw`) is intentionally loose since source formats vary (EDR, SIEM, cloud audit logs, etc.). |
| `label` | Ground truth: `benign` or `malicious`. |
| `severity` | Ground truth severity on a 5-level scale (`informational` → `critical`). |
| `attack_techniques` | MITRE ATT&CK technique IDs/names/tactics relevant to the incident. Empty for benign incidents with no adversarial technique. |
| `supporting_event_ids` | The subset of `raw_events` that justifies the label/severity/techniques — the evidence trail. |
| `expected_investigation_steps` | Ordered, evidence-grounded steps a correct investigation should include, each with a `rationale` and optional `supporting_event_ids`. This is what evidence-grounding scorers check agents against. |
| `expected_containment_actions` | Expected remediation actions once confirmed. Can be empty for benign incidents (correct action = no action). |

### Design notes

- **Evidence-grounding is first-class.** `supporting_event_ids` appears at the
  top level *and* inside each investigation step, so scorers can check not
  just *whether* an agent reached the right conclusion, but whether it cited
  the right evidence for each step along the way — the core thing this
  benchmark measures.
- **`raw_events[].raw` is loosely typed on purpose.** Real event sources (EDR
  telemetry, Zeek logs, CloudTrail, syslog) have wildly different native
  shapes. Forcing a single normalized event schema now would either lose
  information or require a lossy adapter layer before we've even picked our
  first data sources. `event_id` + `timestamp` are the only hard requirements
  so events stay referenceable and orderable.
- **Benign incidents are fully supported, not bolted on.** `attack_techniques`
  and `expected_containment_actions` both default to `[]`, since a benign
  incident may have zero relevant techniques and the "correct" containment
  action is legitimately "do nothing." This matters for scoring false-positive
  behavior, not just detection.
- **Licensing is enforced at the schema level.** `event_source.license` exists
  so every dataset built on this schema documents its license inline,
  consistent with the "approved public datasets only" rule in
  [`data/README.md`](../README.md).
- **`schema_version` is separate from the repo's version.** Scenario data will
  likely outlive individual schema revisions; this field lets scorers detect
  and handle older records without breaking.

### Validating an incident file

\`\`\`bash
pip install jsonschema
python3 -c "
import json, jsonschema
schema = json.load(open('data/schemas/incident.schema.json'))
instance = json.load(open('path/to/incident.json'))
jsonschema.validate(instance=instance, schema=schema)
print('OK')
"
\`\`\`

See [`examples/incident.example.json`](examples/incident.example.json) for a
worked example (a phishing → PowerShell → C2 incident).

### Open questions for `docs/methodology.md`

These are flagged here so they can be resolved when methodology is drafted,
rather than silently baked into the schema:

- Whether `severity` should be scenario-defined or standardized against a
  published rubric (e.g. NIST, CVSS-adjacent) across all datasets.
- Whether scorers need partial-credit semantics for
  `expected_investigation_steps` order (strict sequence vs. unordered set).
