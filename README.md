# Bevor Skills

> AI-powered Solidity security skills — built by [Bevor](https://bevor.io/).

---

## Skills

| Skill | Description |
| ----- | ----------- |
| [solidity-audit](solidity-audit/) | Parallelized smart contract security audit powered by ***Bevor Graph*** |

---

## Usage

```
audit this contract
check this contract for security issues
review for security
```

---

## Requirements

- **`bevor` CLI** installed and authenticated ([Bevor](https://bevor.io/)). The skill flow uses `bevor codes push`, `bevor analyses create`, `bevor analyses scopes set`, `bevor graph …`, and related commands — see [solidity-audit/Skill.md](solidity-audit/Skill.md).
- A **`.bevor`** project config in the target repo (from `bevor init`).
- Optional env overrides if your CLI uses them (e.g. API base URL); see `bevor` docs for your version.

The skill materializes under **`.bevor/analyses/{analysis_id}/`** (per-scope `*.raw.md` / `*.findings.md`) and may write **`.bevor/bevor-audit-report.md`**. Add `.bevor/analyses/` and/or those filenames to `.gitignore` in target repos if you do not want them committed.
