# hacking-agents

Per-agent instruction files. Each file is **one** of several possible parallel roles — the main skill entry (`SKILL.md`) caps parallelism by default (context and rate limits). Each file is concatenated with assigned **`.raw.md`** bundles.

## Agents

| File | Agent | Specialty |
|---|---|---|
| `vector-scan-agent.md` | Agent 1 | Known attack vectors (reentrancy, flash loan, signature replay, etc.) and delegatecall/proxy patterns |
| `math-precision-agent.md` | Agent 2 | Arithmetic bugs, precision loss, rounding errors, overflow/underflow |
| `access-control-agent.md` | Agent 3 | Authorization surface, role/ownership checks, upgrade paths, pausability |
| `economic-security-agent.md` | Agent 4 | Value flow, token accounting, incentive manipulation, collateral/price impact |
| `invariant-agent.md` | Agent 5 | State integrity, accounting invariants, storage slot consistency |
| `periphery-agent.md` | Agent 6 | External protocol integrations, oracle dependencies, router interfaces, off-chain inputs |
| `first-principles-agent.md` | Agent 7 | Catch-all; receives the full entrypoint set to catch novel or cross-cutting bugs |
