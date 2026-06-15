# Analysis Findings Contract

The analysis skill produces findings. It does not submit them.

## Direct Output

When no Bevor-managed analysis is supplied, write one YAML document whose root is a `findings` list.
Use the user-provided output path or default to:

```text
security-findings.yaml
```

## Bevor-Managed Per-Scope Output

When `operate-bevor` supplies an analysis and scope manifest, write one YAML file per analyzed scope:

```text
.bevor/analyses/{analysis_id}/{scope_key}.findings.yaml
```

The root is a `findings` list. A scope may contain zero, one, or many findings.

```yaml
findings:
  - type: logic
    level: medium
    name: Incorrect accounting permits excess withdrawal
    location_id: a1b2
    description: |
      The withdrawal path decreases shares after transferring assets, allowing...
    recommendation: Update accounting before the external transfer.
```

## Required Fields

- `type`: one of `access_control`, `reentrancy`, `arithmetic`, `validation`, `logic`,
  `concurrency`, `economic`, `oracle`, `denial_of_service`, `upgradeability`,
  `data_exposure`, `cryptography`
- `level`: one of `critical`, `high`, `medium`, `low`
- `name`
- `description`
- At least one of `scope_id` or `location_id`

Optional fields accepted by the Bevor CLI are `recommendation`, `reference`, and `source`.

Use singular `scope_id`. The CLI accepts legacy `scope_ids` only when it contains exactly one ID.

## Quality Rules

- Report source behavior, not graph or tooling behavior.
- Put node IDs only in `scope_id` and `location_id`.
- Tie each finding to the scope's entry, call chain, shared state, or a clearly explained causal
  bridge.
- Do not deduplicate or submit here. That is owned by `operate-bevor`.
