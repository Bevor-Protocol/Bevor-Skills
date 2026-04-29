# Analysis

**Graph** = active code version (**`bevor codes current`**). Expand **only** with **`bevor codes nodes`**: **`get`**, **`content`**, **`edges`** (`-j`, optional **`--direction in|out`**), **`call-chain`**. Use **`short_id`** (≥4 chars) everywhere—never full UUIDs. Do not mix incompatible **`call-chain`** flags.

**Typical expansion:** **`edges`** → **`content`** on needed ids → **`call-chain`** when the bundle tree is insufficient → **`get`** for missing metadata.

---

## Agents

- **Queue:** every **`{scope_key}.raw.md`** under **`.bevor/analyses/{analysis_id}/`** appears in at least one agent; **`{scope_key}`** = basename minus **`.raw.md`**.
- **Prompts:** assigned bundle text + one thin role file + small shared instructions the orchestrator picks. No whole-book pastes. Default **~3–4** concurrent agents on small repos unless you scale down further.
- **Reads:** okay under **`.bevor/analyses/.../`** only. Do not **`grep`/walk** project source for Solidity context. Do not edit **`*.raw.md`** after materialize.
- **Proof of graph use:** if an agent did not run **`bevor codes nodes`** when the bundle was incomplete, treat the run as failed—do not substitute working-tree source for them.

Spill large CLI output to disk (**`>>`**) instead of pasting walls into chat.
