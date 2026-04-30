---
name: bevor-skill
description: Security analysis via the Bevor graph only (no raw working-tree code review). Trigger on "audit", "analyze", "check this contract", "review for security". Uses `bevor agent setup` + `bevor agent materialize`, `bevor codes nodes`, per-scope `.findings.md` and deduped `findings/`, a single final `bevor agent submit --dir` on `findings/`, and lean prompts from `references/`.
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
- Do not hand-edit **`*.raw.md`** after **`bevor agent materialize`**.
- For **how to think about security** (roles, shared rules, optional judging/report templates), use this skill’s **`references/`**—thin slices per agent, not whole-library pastes (**`analysis.md`**).

## ABSOLUTELY FORBIDDEN — no exceptions

Applies to the **repository under audit**. The only filesystem zones you may use for reads/listing **implementation** context are **`./.bevor/`** and **this skill package** (the tree that contains **`SKILL.md`**, **`references/`**, and the phase **`*.md`** files).

- **`Read`** (or any file tool) on **`.sol`**, **`.ts`**, **`.js`**, **`.json`**, or other **project source** under the audit repo **outside** **`./.bevor/`**
- **Shell / CLI:** **`find`**, **`cat`**, **`grep`**, **`ls`**, or shell **glob**/wildcard expansion targeting **project source** outside **`./.bevor/`**
- **Any** access to paths **outside** **`./.bevor/`** and **outside this skill package** when the purpose is reading **audited codebase** contents (not Bevor artifacts, not skill prompts)
- Do not `cat` files you just wrote. Read the output directly from the command that produced it.

**Solid source for a graph node — only:**

```text
bevor codes nodes content <short_id>
```

(plus other **`bevor codes nodes`** subcommands this package allows.)

Break these rules and the run is **invalid**. If you reach for an audit-repo source path, **stop** and use the CLI.
