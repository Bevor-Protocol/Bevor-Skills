# references

Shared context files loaded by the audit skills at runtime. These are not skill entry points — they are injected into agent bundles during orchestration.

## Files

| Path | Purpose |
|---|---|
| `attack-vectors/attack-vectors.md` | Library of known smart contract attack classes. Injected into Agent 1 (Vector Scan) bundles. |
| `hacking-agents/` | Per-agent instruction files. Each file tells an agent what to look for and how to report it. See `hacking-agents/README.md`. |
| `judging.md` | Four-gate evaluation criteria applied during deduplication to determine whether a finding is valid. |
| `report-formatting.md` | Output format specification for the final audit report. |
