# Finding exchange and duplicate control

Use this reference to import, export, normalize, deduplicate, stage, review, or commit findings.

Compatibility: `bevor-cli 0.1.0` and `bevor-sdk 0.1.0`, source commit `591421f2963f6095d33521ff57ca3d60759333e3`, reviewed 2026-09-02.

## Select a format

1. Keep valid SARIF from a source tool as SARIF.
2. Use typed `FindingBodyDict` objects in Python.
3. Use JSON with a top-level `findings` array when a producer needs generic JSON.
4. For CLI directory import, use one YAML mapping per `.yaml` or `.yml` file.

Keep the producer name in `source`. Preserve rule IDs, original locations, evidence, and references.

## Bevor finding shape

A typed SDK finding uses:

```json
{
  "source": "tool-name",
  "metadata": {
    "type": "reentrancy",
    "level": "high",
    "name": "Short finding name",
    "explanation": "Evidence, exploit path, and effect",
    "recommendation": "Concrete repair",
    "reference": "https://example.com/rule"
  },
  "location": {
    "strategy": "node_id",
    "scope_id": "ENTRYPOINT_NODE_ID",
    "location_id": "EVIDENCE_NODE_ID"
  }
}
```

Location strategies are:

- `node_id`: `scope_id` and/or `location_id`.
- `physical`: `uri` plus optional line, column, character, or byte ranges.
- `logical`: `fully_qualified_name`.

The CLI YAML shape is flatter:

```yaml
type: reentrancy
level: high
name: Short finding name
description: Evidence, exploit path, and effect
recommendation: Concrete repair
reference: https://example.com/rule
source: slither
scope_id: ENTRYPOINT_NODE_ID
location_id: EVIDENCE_NODE_ID
```

Required YAML fields are `type`, `level`, `name`, and nonempty `description`. Supply at least one of `scope_id` or `location_id`.

Supported Bevor levels are `critical`, `high`, `medium`, and `low`.

## SARIF conversion

The SDK exposes:

```python
from bevor_sdk.helpers.converters.sarif import (
    bevor_to_sarif,
    bevor_to_sarif_sync,
    sarif_to_bevor,
)
```

At SDK 0.1.0, the default SARIF-to-Bevor level map is:

| SARIF | Bevor |
| --- | --- |
| `error` | `critical` |
| `warning` | `high` |
| `note` | `medium` |
| `none` | `low` |

Review this mapping against the producer's severity meaning. Do not raise severity only because the format converter maps a transport level.

## Duplicate procedure

Before submission:

1. Remove duplicates within the new batch.
2. Compare with staged findings on the exact analysis version.
3. Compare with committed and inherited findings.
4. Prefer `origin_finding_id` and graph identity when available.
5. Otherwise compare rule or type, semantic location, root cause, asset, and attack path.
6. Do not compare only the title.
7. Merge stronger evidence, references, affected scopes, and supported severity.
8. Preserve the first discovery source. Record later sources as corroboration or evidence.
9. Keep findings separate when cause, attack path, asset, or repair differs.

The bulk-import service does not promise semantic duplicate removal. The agent or producer must do it.

## Submission procedure

1. Require an `exact` code match.
2. Show source, record counts, and destination.
3. Get upload approval unless an approved CI policy covers it.
4. Validate the local exchange file.
5. Show input, invalid, duplicate, combined, and new counts.
6. Submit once.
7. Run `bevor analysis diff --staged --json`.
8. Show additions, edits, and deletions.
9. Get commit approval unless an approved CI policy covers it.
10. Run `bevor analysis commit` once.
11. Report committed counts and useful error text.

For SARIF or JSON:

```bash
bevor agent submit results.sarif
bevor analysis diff --staged --json
```

For a YAML directory, the pinned CLI has a known defect: it requires an unused positional file.

```bash
bevor agent submit placeholder.json --dir findings/
bevor analysis diff --staged --json
```

Do not use the placeholder flow without first confirming the installed CLI still has this defect.

## Acknowledgement

`bevor finding acknowledge FINDING_ID` toggles current state. It does not set an explicit desired value.

Read the current finding, state the resulting value, and get clear approval before using the command.
