---
name: operate-bevor
description: Operate the Bevor CLI for agents and external security systems. Use to initialize or inspect Bevor context, synchronize code, create and manage analyses, materialize evidence, record findings produced by codebase runs or external tools, and submit or commit findings. Do not independently discover or assess vulnerabilities.
---

# Operate Bevor

Own the Bevor control plane and findings transport. Do not own security analysis.

## Boundary

Use this skill for:

- Authentication, project linking, status, and context selection
- Keeping the current codebase synchronized with Bevor
- Creating analyses and configuring scopes
- Materializing analysis evidence for another skill
- Normalizing and recording findings from codebase runs or external security tools
- Importing, staging, committing, and submitting findings

Do not inspect source to discover vulnerabilities, assign severity based on independent analysis, or
rewrite the substance of a finding. Ask the analysis producer to resolve unsupported or malformed
claims.

## Workflow Selection

For any external or third-party security agent, read and follow `references/byos-workflow.md`
completely. It defines prior-context retrieval, fresh versus inherited analysis lineage, scope
selection, external-agent invocation, and findings recording.

When a security scan names another skill, agent, or tool, read `references/analyzer-adapter.md` and
treat that analyzer as the scan engine. If no analyzer is named, default to `analyze-codebase`.
Before scanning, print the protocol's single analyzer preflight announcement. Do not add a
confirmation prompt for an unambiguous selection.

For other operations, read `references/workflows.md` and follow the smallest matching workflow.

Before using an unfamiliar command or option, consult `references/cli-surface.md`. That file is
generated from the Typer command tree and is the source of truth for the installed CLI surface.

For finding formats and handoff rules, read `references/findings-handoff.md`.

## Safety

- Treat `codes push`, analysis creation, scope mutation, imports, commits, and submissions as
  state-changing operations.
- Prefer JSON output for machine-to-machine inspection when a command supports `--json`.
- Do not use `--force` to bypass code synchronization checks unless the user explicitly requests
  that behavior.
- Validate and deduplicate findings before bulk import.
- Run a final bulk import or `bevor agent submit` once, after the findings directory is complete.

## Maintaining The CLI Reference

After CLI command registration or options change, regenerate the reference:

```bash
python operate-bevor/scripts/generate_cli_reference.py \
  --cli-root /path/to/bevorai-api/packages/cli \
  --output operate-bevor/references/cli-surface.md
```

The generator imports `bevor_cli.main:app` and walks Typer's registered Click command tree. Keep
workflow guidance handwritten; do not manually maintain a duplicate command catalog. Only commands
mounted into the root CLI are included.

Use the same command with `--check` in CI to fail when the committed reference is stale.
