---
name: bevor-skill
description: Security audit via the Bevor graph only (no raw working-tree code review). Trigger on "audit", "check this contract", "review for security". Uses `bevor analyses scopes materialize` for per-scope `*.raw.md`, then `bevor graph *` in agents, and `*.findings.md` under `.bevor/analyses/{analysis_id}/`.
---

# Smart Contract Security Audit (Bevor CLI)

You orchestrate a parallelized smart contract security audit using the **`bevor`** CLI. The model is: push code → create an **analysis** (container) → set **scopes** → run **`bevor analyses scopes materialize`** once to generate all **`.raw.md`** bundles under **`.bevor/analyses/{analysis_id}/`** → run **multiple security sub-agents** on those bundles in parallel → append **findings** to **`.bevor/analyses/{analysis_id}/{scope_key}.findings.md`** per scope. **Success is:** those findings files exist and every line is valid NDJSON for **`bevor analyses findings add -f`**.

**All generated folders and files** MUST live under **`.bevor/analyses/{analysis_id}/`** — never at repo root.

---

## CRITICAL RULES — READ BEFORE DOING ANYTHING

### 1. Scope bundles: use `materialize` — do not hand-build `.raw.md`

**`.raw.md` files** come only from:

```bash
bevor analyses scopes materialize
```

(Use **`-a <analysis_id>`** if the active analysis in `.bevor` is not the one you want.) This writes every scope in one go; do not run per-scope `bevor graph` yourself for **Part C**, and do not copy CLI output into context then paste with the **Write** tool.

For **findings** and any **extra** graph exploration in **Part D**, still **append to disk** with `>>` (or the CLI’s file flags) when you are not using a dedicated subcommand that writes the file for you. Never hold large graph output in chat only to re-emit it.

### 2. Scopes after `materialize` come from the directory — do not `scopes list` for Part D

After **`bevor analyses scopes materialize`**, the scope set is **exactly** the **`*.raw.md`** files the command wrote. **`{scope_key}`** = the filename with **`.raw.md` removed** (e.g. `AAAB` from `AAAB.raw.md`).

**Do not** run **`bevor analyses scopes list -j`** to discover which scopes exist or to assign agents in Part D — that duplicates work, wastes approvals, and is redundant. List **`.bevor/analyses/{analysis_id}/`** (e.g. `ls` / glob) and use those basenames. Optional: **`bevor analyses scopes list -j`** only if you truly need API-only fields and cannot proceed otherwise.

### 3. Use SHORT IDs everywhere — never full IDs

Every `bevor graph` command accepts a **`short_id`** (minimum 4 characters, e.g. `AAAB`). **Always use `short_id`**, never the full UUID. Short IDs are scoped to the graph and unambiguous within it.

**WRONG:** `bevor graph content BkWHMxha1DtfqQPL1qI9fC`
**CORRECT:** `bevor graph content AAAB`

### 4. Run with permissions — do not ask for approval on every command

All `bevor` CLI commands are pre-approved for this skill. Do not pause to request permission before each invocation. Execute the command sequence continuously.

### 5. Only run commands listed in this skill — do not improvise

Do **not** run `bevor --help`, `bevor <anything> --help`, or any undocumented subcommand. Do **not** read raw `.sol` files from the working tree. **Do not** edit or append to `*.raw.md` after **`materialize`** (they are the canonical bundle). Further graph context lives in agent-only **`bevor graph`** calls in **Part D**, not in patched `.raw.md` files. If a command errors, report the exact command and error — do not substitute or explore.

### 6. Parallelize where it matters — do not over-spawn agents

**Part C (materialize)** is a **single** `bevor analyses scopes materialize` (it materializes all scopes). **Part D (agents):** sub-agents are **optional**; use **3–4 concurrent agents** on small codebases by default, or fewer — each agent is a **full** model + tool budget. **Do not** launch “all 7” by default on tiny projects; that multiplies cost and is a common cause of **rate / usage limits** even when the **repo** is small (context and parallel tool use are what scale).

### 7. What goes into an agent (token budget)

Each Part D agent’s prompt must be **lean**:

- The assigned **`.raw.md`** file(s) for its scopes only
- **Exactly one** `references/hacking-agents/<agent>.md` for that role
- **`references/hacking-agents/shared-rules.md`**

**Do not** inject **`references/attack-vectors/attack-vectors.md`** in full (it is huge). Do not bulk-read the project tree, `lib/`, or general `.sol` files for “context.” The Vector / pattern agent uses **its own** `vector-scan-agent.md` instructions plus bundles — not a 1000+ line library in the same prompt. Do not attach `judging.md` or `report-formatting.md` to every sub-agent unless a pass explicitly needs them.

### 8. Sub-agents must expand via `bevor graph`, not the repo

When an agent needs code beyond the **`.raw.md`**, it must use **`bevor graph edges` → `bevor graph content` / `bevor graph call-chain`** (see Part D). If you cannot see evidence in the user transcript that the agent used those commands for expansion, treat that as a failure of the run — the orchestrator should **not** “help” by reading `src/**/*.sol` for them.

---

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

## Part A — Link repo to Bevor (if not already)

```bash
bevor init
```

Skip if already initialized.

---

## Part B — Setup: code version + analysis + scopes

Run in order:

```bash
bevor codes push
printf 'y\n' | bevor analyses create -j
bevor analyses scopes set --first-party -j
```

- **`bevor codes push`** — registers current code, sets active code version in `.bevor` config.
- **`bevor analyses create -j`** — creates the analysis container. Pipe `y` to suppress interactive prompt. Parse nothing from output — the active analysis is stored in `.bevor` config automatically.
- **`bevor analyses scopes set --first-party -j`** — sets scope mode. No further action needed.

---

## Part C — Materialize scope bundles (one command)

**Work directory** — all artifacts use:

`.bevor/analyses/{analysis_id}/`  

**If you do not already have `{analysis_id}`** (e.g. from Part B, the `materialize` success line, or prior context), resolve it with:

```bash
bevor analyses current -j
```

Parse the **`id`** field. You never need to `mkdir` that path yourself — **`materialize` creates** `.bevor/analyses/{analysis_id}/` when it runs.

```bash
bevor analyses scopes materialize
```

Use **`-a` / `--analysis <analysis_id>`** only if you are not using the default active analysis in `.bevor`. Do not hand-run `bevor graph content` or `bevor graph call-chain` to build `*.raw.md` — the CLI does it.

**Output layout**

For each analysis scope, the command writes a file:

**`.bevor/analyses/{analysis_id}/{scope_key}.raw.md`**

where **`{scope_key}`** is the scope’s **short_id** (e.g. `AAAB` — **never the full node UUID** in filenames).

**Inside each `*.raw.md`**

1. **Source** — the node’s source text as returned by the graph (plain text, not fenced).
2. A **blank line**.
3. The literal line **`call-chain:`**
4. The **call-chain tree** in the same shape as the non-JSON **`bevor graph call-chain <short_id>`** output (line-drawn tree, not JSON): root line, then `├──` / `└──` children, with node names and **short** ids in brackets on each line, matching the interactive CLI tree (colors stripped in the file).

If there is no chain, the file still contains the `call-chain:` section with an empty / “Empty call chain” style message as the CLI would show — **do not** improvise a different format.

**Scope keys for the rest of the skill** — enumerate **`*.raw.md`** in that directory; each stem is a **`{scope_key}`**. The **source** at the top of each file and the call-chain tree are enough to audit; you do not need a separate API response to know “which” scopes to run.

When finished, the CLI prints how many files were written and the directory — echo that in your run summary (e.g. `Materialized N scope bundles under .bevor/analyses/{analysis_id}/`).

---

## Part D — Security agents (PARALLEL)

Derive the list of **scopes to assign** from **`.bevor/analyses/{analysis_id}/*.raw.md`** (one `scope_key` per file — see **### 2** above). Do not call **`bevor analyses scopes list`** to build that list.

Spawn all agents concurrently. Each agent gets one or more scopes assigned by specialty. Every `*.raw.md` must appear in at least one agent's queue.

### What agents receive

Path to each bundle (resolve **`{analysis_id}`** with **`bevor analyses current -j`** if it is not already known):

**`.bevor/analyses/{analysis_id}/{scope_key}.raw.md`**

Each agent receives **only**:
- The **contents** of the assigned `*.raw.md` files (format: **source**, blank line, **`call-chain:`**, then the **text tree** — as in Part C; not JSON)
- **One** `references/hacking-agents/<this-agent>.md`
- `references/hacking-agents/shared-rules.md`

**Do not** add full-repo reads, do not pass **`references/attack-vectors/attack-vectors.md`** in full to any agent, and do not treat the `contracts/` or `src/` tree as a readable audit surface (see **### 7–8**).

### What agents may do (required pattern for new code)

When the bundle is insufficient, the **only** approved expansion is:

1. **`bevor graph edges <short_id> -j`** (optionally `--direction in` or `out`) — get neighbor **short** ids and edge types.
2. **`bevor graph content <short_id>`** on ids you need.
3. **`bevor graph call-chain <short_id> -j`** (or `call-chain formatted <short_id>`) if you need a full chain for a specific node not fully covered in the file.

**Commands:**

```bash
bevor graph content {short_id}               # source (no -j)
bevor graph call-chain {short_id} -j         # call chain JSON
bevor graph call-chain formatted {short_id}  # human tree (no -j; never combine with -j)
bevor graph edges {short_id} -j              # edges; --direction in or out. Use short ids from JSON
```

Agents must **not**:
- **`read` / `open` / `cat` / `grep` `*.sol` (or any project source) from disk** except files under **`.bevor/analyses/.../`** (bundles, findings) produced by this skill
- **Browse** `src/`, `contracts/`, `lib/`, or vendor folders for “more code”
- Run `bevor graph get` unless a specific field is missing from edges/content
- Add undocumented subcommands
- Preemptively re-read the entire repo “for context”

Agents should stop expanding when they can substantiate a finding; prefer **one edges hop** + **content** for callees over dumping whole directories.

---

## Part E — Findings output (per scope)

**File:** `.bevor/analyses/{analysis_id}/{scope_key}.findings.md`  

Use the same **`{analysis_id}`** as in Part C (from **`bevor analyses current -j`** if needed).

This file is **raw NDJSON** — one JSON object per line, nothing else. Despite the `.md` extension it is not a markdown document. Do not add headers, code fences, commentary, blank section dividers, or any non-JSON content. Every line must be independently parseable as JSON with no surrounding markup.

### Schema

Each line is a single raw JSON object — no code fences, no wrapping, no markdown. Required fields:

- `location_id` — the `short_id` of the node where the vulnerability exists. Always `short_id`, never full UUID
- `type` — one of: `access_control`, `reentrancy`, `arithmetic`, `validation`, `logic`, `concurrency`, `economic`, `oracle`, `denial_of_service`, `upgradeability`, `data_exposure`, `cryptography`
- `level` — one of: `critical`, `high`, `medium`, `low`
- `name` — short title
- `explanation` — description of the vulnerability

Optional fields:
- `recommendation` — how to fix it
- `reference` — external reference (e.g. SWC-107)

---

## Part F — Deduplication (orchestrator pass)

After all agents complete:

1. Collect all **`.bevor/analyses/{analysis_id}/{scope_key}.findings.md`** files for that analysis
2. Deduplicate by `location_id` + `type` — keep the strongest `level` and most complete `explanation` per group
3. For findings that appear across multiple scopes (same `location_id` + `type` found in more than one **`.bevor/analyses/{analysis_id}/{scope_key}.findings.md`**), populate `scope_ids` as an array of the **`scope short_id`** values from each file it appeared in. This is the only place `scope_ids` is meaningful — it has no meaning in per-scope files:

```json
{"location_id":"AAAB","scope_ids":["AAAB","AAAC"],"type":"reentrancy","level":"critical","name":"...","explanation":"..."}
```

4. Write deduplicated findings to **`.bevor/analyses/{analysis_id}/findings.deduped.md`** — raw NDJSON, one JSON object per line, no markdown, no code fences, no commentary

---

## Part G — Submit findings

```bash
bevor analyses findings bulk -f .bevor/analyses/{analysis_id}/findings.deduped.md
```

This closes the analysis. Report how many findings were submitted and any errors.

---

## Deprecated

- `bevor entrypoints list` — replaced by **scopes from `*.raw.md`** under **`.bevor/analyses/{analysis_id}/`**
- **`bevor analyses scopes list -j` as a prerequisite for Part D** — after `materialize`, the directory listing **is** the scope list; do not re-fetch
- **Hand-building** `*.raw.md` with echo / `bevor graph content` / `bevor graph call-chain` in the skill — replaced by **`bevor analyses scopes materialize`**
- Per-entrypoint `bevor callchain` — replaced by `bevor graph call-chain` (exploration) and `materialize` (bundles)
- Capturing large CLI output to variables then re-emitting when a **`materialize`** or **`>>` append** could write disk directly