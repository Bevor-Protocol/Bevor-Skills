# Shared rules (Bevor graph audit)

## ABSOLUTELY FORBIDDEN — no exceptions

For the **repository under audit** (not **`.bevor/`**, not this **skill package**):

- **`Read`**, **`cat`**, **`ls`**, **`grep`**, **`find`**, or globbing to load **`.sol`**, **`.ts`**, **`.js`**, **`.json`**, or other **implementation files**
- Any tool access to **audited project source paths** outside **`./.bevor/`** when the goal is reading code for this audit

**You may read:** **`./.bevor/`** (bundles, findings, analyses) and files under **this skill** (e.g. **`references/`** instructions) only.

**Solidity for a node — only:**

```text
bevor nodes content <short_id>
```

Violations invalidate the run. If you open an audit-repo source path, **stop**; use the graph CLI.

---

## What you are given

Each assignment is one or more files under **`.bevor/analyses/{analysis_id}/`** named **`{short_id}.raw.md`**, produced by **`bevor agent materialize`**. Real layout:

1. **Source** — graph-sourced snippet for that scope node (plain text at the top).
2. A blank line, then the line **`call-chain:`**
3. A **text call tree** (same shape as **`bevor nodes call-chain`** human-tree output, not JSON): root line, then `├──` / `└──` lines, with **short ids** in brackets. This is your pre-traced slice; start from it.

There is **no** `### path :: Contract.function` header, no fenced Solidity blocks, no separate “Static Analysis” section unless your prompt added it.

## How you may get more code (graph only)

If you need another function’s source, callees, or structure **not** fully covered in the bundle:

1. **`bevor nodes edges <short_id> -j`** — discover neighbor nodes (use `--direction in` or `out` as needed). Read `short_src_id` / `short_dst_id` (or equivalent) from JSON.
2. **`bevor nodes content <short_id>`** — source for that node only.
3. **`bevor nodes call-chain <short_id>`** — JSON or formatted tree per flags; refresh a chain for a specific node you are investigating (follow CLI rules — do not combine incompatible flags).

**That is the only way** to read additional Solidity from the audited codebase. If it is not reachable through **`bevor nodes`** from ids in the bundle or from **edges** expansion, it is out of scope for you.

`short_id` is always the **short** id (e.g. `AAAB`), never the long UUID, in all `bevor nodes` arguments.

Use **`bevor nodes get <short_id>`** when you need node metadata not present in **edges** / **content**.

## Economy

- Do not re-fetch **`bevor nodes content`** for a node whose source is **already in your `.raw.md`** unless you are verifying after a code-version change.
- Expand with **edges** in small steps; do not fan out to “every node in the project.”
- Every substantive claim about behavior must be traceable to a **node short_id** and either the bundle or a **`bevor nodes`** result.

## Do not report

Admin-only admin behavior; pure DeFi tradeoff nits; self-harm-only; “admin can rug” with no concrete mechanism.

## Output

Return structured blocks only — no preamble, no narration, unless a specialty file says otherwise.

FINDINGs need concrete, exploitable paths. LEADs: real code smells, partial path — default LEAD over dropping.

**Every FINDING should have a `proof:`** — trace or values grounded in the graph-sourced view (bundle + `bevor nodes` as above). No proof → LEAD.

**One vulnerability per item.** Same root cause → one item.

```
FINDING | contract: Name | function: func | bug_class: kebab-tag | group_key: Contract | function | bug-class
path: caller → function → state change → impact
proof: …
description: one sentence
fix: one-sentence suggestion

LEAD | contract: Name | function: func | bug_class: kebab-tag | group_key: Contract | function | bug-class
code_smells: …
description: one sentence
```

`group_key` is for dedup: `ContractName | functionName | bug_class`.
