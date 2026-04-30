# Analysis

Filesystem rules for the audited repo and agents: **`SKILL.md`** (**ABSOLUTELY FORBIDDEN**). Allowed zones: **`.bevor/`** and this skill package only; node source comes **only** from **`bevor codes nodes content <short_id>`** (and sibling **`bevor codes nodes`** commands below).

**Graph** = active code version (**`bevor codes current`**). Expand **only** with **`bevor codes nodes`**: **`get`**, **`content`**, **`edges`** (`-j`, optional **`--direction in|out`**), **`call-chain`**. Use **`short_id`** (≥4 chars) everywhere—never full UUIDs. Do not mix incompatible **`call-chain`** flags.

**Typical expansion:** **`edges`** → **`content`** on needed ids → **`call-chain`** when the bundle tree is insufficient → **`get`** for missing metadata.

**References (security task context):** This skill’s **`references/`** folder holds specialist prompts (**`references/hacking-agents/`**), and other optional guides (**`judging.md`**, **`report-formatting.md`**, **`references/README.md`** for the map). Give each agent its assigned **`*.raw.md`** plus **small** picks from here. Do not paste huge reference tomes into one prompt.

**Scope discipline:** Work **to** the assigned **`{scope_key}.raw.md`**—entry, source, and **call-chain** on that bundle. Graph expansion is for explaining **that** slice (callees, state it touches, guards on those paths). Do not use a **deposit** scope to collect **withdraw**-only bugs (or the reverse) unless you can show **causal linkage**: shared storage, mutual invariants, reentrancy or ordering **through** this entry, broken assumption this path relies on, etc. If there is no such link, the issue belongs under another **`{scope_key}`** or is out of this pass.

---

## Agents

- **Queue:** every **`{scope_key}.raw.md`** under **`.bevor/analyses/{analysis_id}/`** appears in at least one agent; **`{scope_key}`** = basename minus **`.raw.md`**.
- **Prompts:** bundle + thin role file from **`references/`**—see above. Default **~3–4** concurrent agents on small repos unless you scale down further.
- **Reads:** **`./.bevor/`** and this **skill package** only—never **`cat`/`ls`/`grep`/`find`** (or **`Read`**) on audited **`src/`**, **`contracts/`**, **`*.sol`**, etc. Do not edit **`*.raw.md`** after materialize.
- **Proof of graph use:** if an agent did not run **`bevor codes nodes`** when the bundle was incomplete, treat the run as failed—do not substitute working-tree source for them.

Spill large CLI output to disk (**`>>`**) instead of pasting walls into chat.

## Graph traversal rules

**Follow edges to expand context:**
- Outbound edges from the scope node — what it writes, reads, calls, emits
- Inbound edges on state variables — who else reads or writes the same state

**Never follow:**
- `defines` edges in either direction — leads to container nodes (contracts) which add no security signal

If an edge has `edge_type: "defines"`, ignore it entirely.