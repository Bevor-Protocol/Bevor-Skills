# references

Shared context files loaded by the audit skills at runtime. These are not skill entry points — they are injected into agent bundles during orchestration.

## Files

| Path | Purpose |
|---|---|
| `attack-vectors/attack-vectors.md` | **Large** reference library. **Do not inject the full file** into agent prompts (token / rate-limit risk). Use **`vector-scan-agent.md`** and materialized **`.raw.md`**; link or excerpt attack vectors only if the orchestrator explicitly needs a small slice. |
| `hacking-agents/` | Per-agent instruction files. Each file tells an agent what to look for and how to report it. See `hacking-agents/README.md`. |
| `judging.md` | Four-gate evaluation criteria applied during deduplication to determine whether a finding is valid. |
