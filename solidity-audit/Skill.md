---
name: solidity-auditor
description: Security audit of Solidity code using the Bevor CLI. Trigger on "audit", "check this contract", "review for security". Modes - default (full repo) or a specific filename. Supports --poc flag to validate findings in the test suite.
---

# Smart Contract Security Audit

You are the orchestrator of a parallelized smart contract security audit driven by the `bevor` CLI.

**Flags:**

- `--poc` (off by default): after producing findings, attempt to validate each HIGH/CRITICAL finding by writing or running a test in the project's test suite. Label validated findings as `[VERIFIED]` and demote those that cannot be reproduced to LEAD.
- `--file-output` (off by default): write the final report to `bevor-audit-report.md` in the current working directory.

## Banner

Before doing anything else, print this exactly:

```

██████╗ ███████╗██╗   ██╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝██║   ██║██╔═══██╗██╔══██╗
██████╔╝█████╗  ██║   ██║██║   ██║██████╔╝
██╔══██╗██╔══╝  ╚██╗ ██╔╝██║   ██║██╔══██╗
██████╔╝███████╗ ╚████╔╝ ╚██████╔╝██║  ██║
╚═════╝ ╚══════╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝

```

---

## Turn 1 — Init & Discover

In a single message, make these parallel tool calls:

a. Bash `mktemp -d /tmp/audit-XXXXXX` → store result as `{bundle_dir}`  
b. Glob for `**/references/attack-vectors/attack-vectors.md` — extract the `references/` directory (two levels up) as `{resolved_path}`  
c. ToolSearch `select:Agent`

Then run `bevor init` in the project root:

```
bevor init
```

`bevor init` will:
- Scan the working directory for Solidity source files
- Search for an existing Bevor project matching this repo (by remote URL or project name)
- If a match is found: prompt to select or reuse the existing code version, or create a new one; capture the **project ID** and **code version ID**
- If no match: create a new project, upload the source files as a new code version, and return the **project ID** and **code version ID**

Store the output values as `{project_id}` and `{version_id}`.

If `bevor init` fails (no Solidity files found, auth error, network error) — stop and surface the error to the user verbatim.

---

## Turn 2 — Fetch Entrypoints & Call Chains

Run the following to get every auditable entrypoint for this code version:

```
bevor entrypoints list --version-id {version_id} --json
```

This returns a JSON array of entrypoint objects. Each object has the shape:
```json
{ "id": "<entrypoint_id>", "name": "<function>", "contract": "<Contract>", "file": "<path>", "file_id": "<file_id>" }
```
Store the full list as `{entrypoints}`, keyed by `id`. Use `contract` + `name` as the human-readable label (e.g. `Vault.deposit`).

Then fetch the call chain for **every** entrypoint in parallel, writing each to its own dedicated file:

```
# Run all of these concurrently (& ... wait)
bevor callchain --entrypoint {id_for_Vault.deposit} --version-id {version_id} > {bundle_dir}/Vault.deposit.md
bevor callchain --entrypoint {id_for_ERC20.transfer} --version-id {version_id} > {bundle_dir}/ERC20.transfer.md
# ... one command per entrypoint, using the id from the JSON output
```

Each output file contains:
- The function source in a fenced solidity block
- A `**Call chain:**` section with `calls`, `reads`, `writes`, `emits`, and `throws` annotations
- Static analysis signatures

Print: `Fetched {N} entrypoint call chains → {bundle_dir}/`

---

## Turn 3 — Prune & Assign Entrypoints to Agents

Before building bundles, assign each entrypoint to one or more agents based on relevance to their specialty. Every entrypoint must appear in at least one agent's bundle.

**Assignment rules:**

| Agent | Specialty | Route entrypoints that... |
|---|---|---|
| Agent 1 (Vector Scan) | Known attack vectors + delegatecall/proxy | ...match any pattern in `attack-vectors.md` (reentrancy, flash loan, signature replay, etc.), OR use `delegatecall`, implement a proxy/upgrade pattern, or call into untrusted external addresses |
| Agent 2 (Math & Precision) | Arithmetic bugs | ...perform division, multiplication, exponentiation, token amount math, or fee calculations |
| Agent 3 (Access Control) | Authorization | ...have admin/owner/role modifiers, upgrade paths, privileged setters, or pausability |
| Agent 4 (Economic Security) | Incentive/value flow | ...move tokens, ETH, or affect prices, liquidity, or collateral ratios |
| Agent 5 (Invariant) | State integrity | ...write to core accounting state (balances, shares, totals, reserves) |
| Agent 6 (Periphery) | Integration surface | ...interact with external protocols, oracles, routers, or off-chain inputs |
| Agent 7 (First Principles) | Catch-all / novel bugs | ALL entrypoints — Agent 7 always receives the full set |

**Full coverage guarantee:** after assigning by specialty, scan the list for any entrypoint not yet assigned to agents 1–6. Add each unassigned entrypoint to the agent whose specialty is the broadest match — if truly ambiguous, assign to Agent 1. Agent 7 always has all entrypoints, so coverage is always 100%.

**Output the assignment table** before building bundles:

```
Entrypoint assignment:
  Vault.deposit        → Agents 1, 4, 5
  Vault.withdraw       → Agents 1, 4, 5
  ERC20.transfer       → Agents 2, 5, 7
  ...
  Total: {N} entrypoints across 7 agents
```

---

## Turn 4 — Build Agent Bundles

In one message, make parallel tool calls: (a) Read `{resolved_path}/report-formatting.md`, (b) Read `{resolved_path}/judging.md`.

Then build each agent bundle by concatenating only the entrypoint files assigned to that agent plus the agent's instruction files. Use `cat` (not shell variables or heredocs).

For agent N assigned entrypoints `[A.foo, B.bar, ...]`:

```
cat {bundle_dir}/A.foo.md \
    {bundle_dir}/B.bar.md \
    ... \
    {resolved_path}/hacking-agents/<agent-file>.md \
    {resolved_path}/hacking-agents/shared-rules.md \
    > {bundle_dir}/agent-N-bundle.md
```

| Bundle              | Agent-specific file (relative to `{resolved_path}`)                        |
| ------------------- | --------------------------------------------------------------------------- |
| `agent-1-bundle.md` | `attack-vectors/attack-vectors.md` + `hacking-agents/vector-scan-agent.md` |
| `agent-2-bundle.md` | `hacking-agents/math-precision-agent.md`                                    |
| `agent-3-bundle.md` | `hacking-agents/access-control-agent.md`                                    |
| `agent-4-bundle.md` | `hacking-agents/economic-security-agent.md`                                 |
| `agent-5-bundle.md` | `hacking-agents/invariant-agent.md`                                         |
| `agent-6-bundle.md` | `hacking-agents/periphery-agent.md`                                         |
| `agent-7-bundle.md` | `hacking-agents/first-principles-agent.md`                                  |

All bundles append `hacking-agents/shared-rules.md` last.

Print line counts for every bundle. Do NOT inline file content into agent prompts.

---

## Turn 5 — Spawn Agents

In one message, spawn all 7 agents as parallel foreground Agent calls. Use this prompt for every agent (substitute real values for `{bundle_dir}`, `{N}`, `{M}`, and `{version_id}`):

```
Your bundle file is {bundle_dir}/agent-N-bundle.md ({N} lines).
Read it fully before producing findings. The bundle contains {M} entrypoints followed by your agent instructions.

Bundle format — each entrypoint is a section with:
- `### path :: Contract.function` header
- Fenced solidity block (the function source)
- `**Call chain:**` — pre-traced graph with `calls`, `reads`, `writes`, `emits`, `throws` annotations
- `Static Analysis:` — fully-qualified signatures of every function in the chain

THE CALL CHAIN IS YOUR PRIMARY ANALYSIS SURFACE. Source code is secondary confirmation only.
Do not re-trace what the chain already annotates. Use the graph nodes directly:
- `writes <var>` → the storage slot mutated and when in the execution order
- `throws <Error>` → a guard exists at that position in the chain
- `calls <fn>` / `calls external` → a callee exists; the indentation gives you ordering
- `reads <var>` → the value consumed at that point

Your chain protocol and agent instructions are at the end of your bundle.

**Dynamic entrypoint access:** If your analysis requires a call chain not in your bundle, run:
  bevor callchain --entrypoint <id> --version-id {version_id}
Use only when a cross-contract dependency cannot be inferred from existing chains.
```

---

## Turn 6 — Deduplicate, Validate & Output

Single-pass: deduplicate all agent results, gate-evaluate, and produce the final report. Do NOT print an intermediate dedup list.

### 6a. Deduplicate

Parse every FINDING and LEAD from all 7 agents. Group by `group_key` (format: `Contract | function | bug-class`). Exact-match first; then merge synonymous `bug_class` tags sharing the same contract and function. Keep the best version per group, number sequentially, annotate `[agents: N]`.

Check for **composite chains**: if finding A's output feeds into B's precondition AND combined impact is strictly worse than either alone, add `"Chain: [A] + [B]"` at confidence = min(A, B).

### 6b. Gate Evaluation

Run each deduplicated finding through the four gates in `judging.md` (do not skip or reorder). Evaluate each finding exactly once.

**Single-pass protocol:** evaluate every relevant code path ONCE in fixed order (constructor → setters → swap functions → mint → burn → liquidate). One-line verdict per path: `BLOCKS`, `ALLOWS`, `IRRELEVANT`, or `UNCERTAIN`. Commit after all paths. `UNCERTAIN` = `ALLOWS`.

### 6c. Lead Promotion & Rejection Guardrails

- Promote LEAD → FINDING (confidence 75) if: complete exploit chain traced in source, OR `[agents: 2+]` demoted (not rejected) the same issue.
- `[agents: 2+]` does NOT override a concrete refutation.
- No deployer-intent reasoning — evaluate what the code _allows_, not how the deployer _might_ use it.

### 6d. Fix Verification (confidence ≥ 80 only)

Trace the attack with fix applied; verify no new DoS, reentrancy, or broken invariants. List all locations if the pattern repeats. If no safe fix exists, omit it with a note.

### 6e. POC Validation (`--poc` flag only)

For every FINDING rated HIGH or CRITICAL:

1. Check if the project has an existing test suite (`foundry.toml`, `hardhat.config.*`, `truffle-config.js`).
2. Write a minimal proof-of-concept test that reproduces the exploit path described in the finding.
3. Run the test:
   - Foundry: `forge test --match-test <test_name> -vvvv`
   - Hardhat: `npx hardhat test --grep "<test_name>"`
4. If the test **passes** (exploit confirmed): label the finding `[VERIFIED]`.
5. If the test **fails** (exploit not reproducible): demote to LEAD with a note explaining why. Do NOT discard — preserve the attempted POC.
6. If no test framework is detected: skip POC with a note per finding.

### 6f. Format & Print

Format and print per `report-formatting.md`. Exclude rejected items. Prepend `[VERIFIED]` to any POC-confirmed findings.

If `--file-output`: write the full report to `bevor-audit-report.md` in the current working directory.
