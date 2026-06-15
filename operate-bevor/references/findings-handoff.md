# Findings Handoff

The Bevor CLI bulk importer reads a directory containing one YAML mapping per finding.

## Final Directory

```text
.bevor/analyses/{analysis_id}/findings/
```

Only `.yaml` and `.yml` files are imported. Hidden files, Markdown files, nested directories, and
other suffixes are ignored.

## Final File Shape

```yaml
type: logic
level: medium
name: Incorrect accounting permits excess withdrawal
scope_id: a1b2
location_id: c3d4
description: |
  The withdrawal path decreases shares after transferring assets, allowing...
recommendation: Update accounting before the external transfer.
source: external-tool-name
```

Required:

- `type`
- `level`
- `name`
- non-empty `description`
- at least one of `scope_id` or `location_id`

Optional:

- `recommendation`
- `reference`
- `source`

Accepted types and levels are generated from the CLI implementation in `cli-surface.md`.

Use singular `scope_id`. Legacy `scope_ids` is accepted only when it resolves to exactly one ID.

## Normalize Intermediate Findings

Analysis producers may emit a `findings:` list per scope. Flatten those lists, attach the originating
scope as `scope_id` when needed, deduplicate equivalent findings, then write one final mapping per
`.yaml` file.

Do not change the security claim during normalization. Reject malformed entries back to the
producer.

For third-party tools, set `source` to the tool or agent name. Preserve the original tool result
outside the final findings directory when traceability is needed; only normalized Bevor YAML belongs
in the final findings directory.
