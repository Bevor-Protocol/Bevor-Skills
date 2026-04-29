# Findings

There are **two stages**: **per-scope intermediate** files (may hold **many** findings) and **`findings/`** (deduped only: **one finding per file**).

**Required on every finding** (each object in intermediate lists, and every deduped file):

- **`type`** ∈ `access_control`, `reentrancy`, `arithmetic`, `validation`, `logic`, `concurrency`, `economic`, `oracle`, `denial_of_service`, `upgradeability`, `data_exposure`, `cryptography`
- **`level`** ∈ `critical`, `high`, `medium`, `low`
- **`name`**
- **`location_id`**
- **`description`** (plain scalar, or **`|`** / **`>`** for longer Markdown)

**Optional (any stage):** **`scope_ids`** (list of **`short_id`**), **`reference`**, **`recommendation`**

**Voice:** report from **source**—no tooling or graph talk in **`name`** or **`description`**. **`location_id`** and **`scope_ids`** are the **only** places for graph **`short_id`**s—never hide ids in **`description`**.

## Per-scope intermediate

**Path:** **`.bevor/analyses/{analysis_id}/{scope_key}.findings.md`** (same **`{scope_key}`** as **`{scope_key}.raw.md`**).

**Format:** one YAML document whose root is a **`findings:`** list. Each list item is one finding and must include all **required** fields. **`scope_ids`** is usually omitted here (the file’s **`{scope_key}`** is the scope).

```yaml
findings:
  - type: logic
    level: medium
    name: One
    location_id: L1
    description: Explanation.
  - type: access_control
    level: low
    name: Another
    location_id: L2
    description: |
      Longer write-up in Markdown if needed.
```

A scope may contribute **zero, one, or many** list entries.

## Deduped — `findings/` only

**Path:** **`.bevor/analyses/{analysis_id}/findings/`**

**Only** submit-ready, **deduped** **`*.md`** belong here—no drafts, raw bundles, or other noise.

**Format:** each file is **exactly one** finding: a **single** YAML document **not** wrapped in a `findings:` list. Literal shape:

```yaml
type: logic
level: medium
name: One
location_id: L1
scope_ids: [s1]
description: Explanation.
```

After dedupe, set **`scope_ids`** when the same **`location_id` + `type`** came from multiple **`scope_key`** files.

## Dedupe

For every **`{scope_key}.findings.md`**, parse YAML, take **`findings:`** (must be a list). Flatten all items across scopes. Merge on **`location_id` + `type`** (strongest **`level`**, richest **`description`**, merge optionals). Emit each merged row into **`findings/`** as its own **`.md`** file, using the single-document shape above (one finding per file).

## Submit

When deduped **`findings/`** is **final**, run **once**:

```bash
bevor agent submit --dir .bevor/analyses/{analysis_id}/findings
```

Do not call **`bevor agent submit`** again mid-run or after partial dedupe. Report counts and errors verbatim.
