# Bevor Workflows

## Prepare A Codebase Analysis

Use when another skill will perform the analysis:

```bash
bevor status
bevor agent setup
bevor agent materialize
```

`agent setup` assumes `bevor init` has already been run. It synchronizes code, creates an analysis,
and sets first-party scopes. `agent materialize` writes evidence bundles under
`.bevor/analyses/{analysis_id}/`.

If setup should not use the shorthand, use the explicit flow:

```bash
bevor codes push
bevor analyses create
bevor scopes set --mode first_party
bevor agent materialize
```

## Keep A Codebase In Sync

```bash
bevor status
bevor codes current
bevor codes push
```

`codes push` fingerprints and uploads the current directory, then updates `.bevor` context. It skips
the upload when no changes are detected.

## Record Findings From A Codebase Run

1. Read `findings-handoff.md`.
2. Validate required fields and normalize to one finding mapping per `.yaml` file.
3. Deduplicate equivalent findings before import.
4. Put final files under `.bevor/analyses/{analysis_id}/findings/`.
5. Run exactly one final import:

```bash
bevor agent submit --dir .bevor/analyses/{analysis_id}/findings
```

`bevor agent submit` aliases the same bulk import used by `bevor findings bulk`. A successful bulk
import marks the analysis completed.

## Bring Your Own Security Tool

Read and follow `byos-workflow.md`. It is the canonical workflow for running a third-party security
agent with fresh or prior-run context, selecting scan scope, and recording its findings in Bevor.

## Stage And Commit Individual Finding Changes

Use `bevor findings add|edit|delete` for draft changes, inspect with `bevor findings list`, then:

```bash
bevor analyses commit
```
