# Setup

Working directory for bundles: **`.bevor/analyses/{analysis_id}/`**. Resolve **`analysis_id`** from **`bevor agent setup`** output or **`bevor analyses current -j`**.

```bash
bevor agent setup
bevor agent materialize
```

**`Scope keys`** — stems of **`*.raw.md`** in that folder (e.g. `AAAB` from `AAAB.raw.md`). Use this list to assign agents; do not re-derive scopes from API calls unless you truly need extra fields. Each key ties one **`*.raw.md`** to one **`{scope_key}.findings.md`**—see **`findings.md`** for staying on-scope when writing issues.

**Each `*.raw.md`:** graph **source** (plain text) → blank line → line **`call-chain:`** → human **call-chain tree** as the CLI would print (short ids in brackets). Bundles are canonical after materialize—do not rebuild them by hand or patch on disk.

Echo materialize’s file count and path in the run summary.
