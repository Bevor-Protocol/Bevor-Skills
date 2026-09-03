# Exact-version context reuse

Use this reference before a new security scan, security-agent run, change review, or context handoff.

Reviewed against `bevor-cli 0.1.0` and `bevor-sdk 0.1.0` on 2026-09-02.

## Identity states

- `exact`: the target source fingerprint or Bevor code ID matches.
- `related`: a code transition or analysis lineage connects the target and stored version.
- `stale`: local Bevor state selects a different source version.
- `unknown`: the version cannot be resolved with current access.

Apply an earlier finding without a version warning only for `exact`. For `related`, separate inherited findings from findings that need review.

## Reuse procedure

1. Read `bevor context --json`.
2. Identify the target commit and local source fingerprint.
3. Compare the fingerprint with the selected code record.
4. If needed, list code versions and match `version_fingerprint`.
5. Identify the analysis container and selected HEAD version.
6. Get findings on the selected version.
7. Get team findings only with a code or project filter.
8. Get entrypoints and distinguish inherited scope from new scope.
9. Get the version difference for finding changes.
10. Use SDK code transitions if lineage or semantic matching needs more detail.
11. Select only scopes that require new work.
12. Give downstream tools the security brief and selected source segments.

The CLI cannot list recent analyses or filter team findings by code at the pinned version. Use:

- `BevorClient.analyses.recent(...)` for recent analysis context.
- `BevorClient.analyses.list(...)` for analysis search.
- `BevorClient.findings.list({"code_id": code_id, ...})` for code-filtered findings.
- `BevorClient.codes.transitions(...)` for code transitions.

## Minimum context queries

Use the smallest set that answers the question:

```bash
bevor context --json
bevor analysis get --json
bevor analysis entrypoints --json
bevor finding list --json
bevor analysis diff --json
bevor analysis remediations --json
```

Do not run every command by default. For a single suspicious node, add only its metadata, content, relations, and findings.

## Security brief

```text
Bevor context
- Identity: <team/project/code/analysis/head>, match=<exact|related|stale|unknown>
- Change scope: <new/matched/removed symbols or unavailable>
- Reuse: <inherited scopes>/<total>, <borrowed findings>, <remediations>
- Existing risk: <counts by severity/status/source>, <relevant finding IDs/titles>
- Graph focus: <entrypoints/nodes>, <relevant calls/state/guards>
- Limits: <missing function, stale data, or assumptions>
```

Keep full results outside chat. Preserve code, analysis, version, node, and finding IDs for follow-up queries.

## Downstream tool handoff

Tell the next tool:

- The exact code identity and selected scope.
- The relevant nodes and source segments.
- Known findings and their root causes.
- Remediations and validation state.
- Which paths are new, changed, inherited, or already reviewed.
- What the new tool should add beyond known results.

Do not use earlier findings to suppress a different cause, asset, attack path, or repair.

## Savings

Report one terse line only when reuse occurred:

```text
Bevor reuse: 42/50 scopes inherited (~84%), ~118k fewer input tokens, ~18 min less work, and ~$1.42 lower cost (tool baseline).
```

Rules:

- Identify each value as measured, tool-estimated, or calculated.
- Subtract actual work from a stated full-scan baseline.
- If token or cost data does not exist, report scope reuse only.
- Use `characters / 4` only for measurable omitted text.
- Label that conversion as approximate input tokens.
- Use model prices reported by the tool or a current authoritative source.
- Do not convert graph reuse into money without a defensible baseline.
