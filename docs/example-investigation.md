# Example investigation (demo)

Synthetic example based on `data/schemas/examples/incident.example.json`.

## Evidence (abbreviated)

| Event | Signal |
|-------|--------|
| `evt-1` | `powershell.exe` spawned by `winword.exe` with encoded command line |
| `evt-2` | Outbound connection from PowerShell to `185.220.101.7:443` |

## Expected grounded finding

- **Label:** malicious  
- **Severity:** high  
- **ATT&CK:** `T1566.001`, `T1059.001`  
- **Supporting evidence:** `evt-1`, `evt-2`  
- **Containment:** isolate host; reset user credentials  

## Mock oracle run

```bash
pip install -e ".[dev]"
python examples/run_mock_eval.py
```

With `MockProvider(mode="oracle")`, deterministic scorers return `1.0` on all rubric dimensions for this fixture.

## Failure contrast

```bash
sentinelbench --incident data/schemas/examples/incident.example.json --mode empty
```

The empty mock returns benign/informational with no evidence citations, producing low overall score and a non-empty `failure_examples` section in the report — useful for demo screenshots.
