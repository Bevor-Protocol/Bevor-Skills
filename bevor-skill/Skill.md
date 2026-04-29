---
name: bevor-skill
description: Security analysis via the Bevor graph only (no raw working-tree code review). Trigger on "audit", "analyze", "check this contract", "review for security". Uses `bevor agent setup` + `bevor agent materialize`, `bevor codes nodes`, per-scope `.findings.md` and deduped `findings/`, and a single final `bevor agent submit --directory` on `findings/`.
---

# Smart Contract Security Audit (Bevor CLI)

Run the three phase files **in order**; each phase owns the details below.

---

## Banner

Print exactly:

```
██████╗ ███████╗██╗   ██╗ ██████╗ ██████╗
██╔══██╗██╔════╝██║   ██║██╔═══██╗██╔══██╗
██████╔╝█████╗  ██║   ██║██║   ██║██████╔╝
██╔══██╗██╔══╝  ╚██╗ ██╔╝██║   ██║██╔══██╗
██████╔╝███████╗ ╚████╔╝ ╚██████╔╝██║  ██║
╚═════╝ ╚══════╝  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝
```

---

## Steps

1. **`setup.md`**
2. **`analysis.md`**
3. **`findings.md`**

---

## Orchestrator constraints

- Keep all analysis artifacts under **`.bevor/analyses/{analysis_id}/`**.
- Use only **`bevor`** invocations described in this package; they are pre-approved—do not pause for permission between steps.
- Do not read project source from disk to write findings (graph-backed process only). Do not hand-edit **`*.raw.md`** after **`bevor agent materialize`**.
