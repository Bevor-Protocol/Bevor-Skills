# Bring Your Own Security Agent

Use this workflow when a selected security analyzer performs the scan and Bevor provides code
synchronization, prior-run context, scope identity, analysis lineage, and finding storage. The
analyzer may be another skill or an external tool.

The selected analyzer is the scan engine. Do not run `bevor analyses run` as part of this workflow
unless the user also wants Bevor's own scanner to run.

Read `analyzer-adapter.md` first. The selected analyzer may be an external command, the local
`analyze-codebase` skill, or another installed security skill.

## Contract

The workflow has four phases:

```text
prepare Bevor analysis
  -> give scoped code and optional prior findings to selected analyzer
  -> normalize external output to Bevor finding YAML
  -> record findings with Bevor CLI
```

An analyzer adapter should accept:

- The repository or materialized `.raw.md` scope bundles
- A scope manifest from `bevor scopes list --json`
- Optional prior findings from `bevor findings list --no-draft --json`
- A scan instruction describing the requested security focus
- An output location

The adapter should emit either:

- One Bevor-compatible YAML mapping per finding, preferred; or
- Tool-native results that can be normalized according to `findings-handoff.md`

Set each normalized finding's optional `source` field to the selected tool or skill name.

After creating the new analysis, use this working layout:

```text
.bevor/analyses/{analysis_id}/
├── *.raw.md
├── byos/
│   ├── context/
│   │   ├── scopes.json
│   │   └── prior-findings.json
│   └── raw-output/
└── findings/
    └── one-normalized-finding.yaml
```

`prior-findings.json` is optional. Keep tool-native output under `byos/raw-output/`; never put it in
the final `findings/` directory.

## Phase 1: Choose Context Mode

### Fresh, Independent Run

Use when prior findings must not influence the scan or analysis lineage:

```bash
bevor status --json
bevor codes push
bevor analyses create --no-parent
```

### Prior-Informed Run

Use when the external agent should see findings from an earlier Bevor run.

1. Find and select the prior analysis:

```bash
bevor analyses list --json
bevor analyses select <prior-analysis-id>
```

2. Capture prior findings before creating the new analysis:

```bash
bevor findings list --no-draft --json > <temporary-prior-findings-json>
```

Keep that JSON as the external agent's prior context. It contains findings recorded in Bevor and
surfaced through the CLI.

3. Synchronize current code and create the new child analysis:

```bash
bevor codes push
bevor analyses create
```

Because the prior analysis remains active when `analyses create` runs, the new analysis records it
as its parent. Do not pass `--no-parent` in this mode.

Use prior findings as leads, not automatically confirmed findings. The external agent must
revalidate them against the current code.

After creation, resolve the new analysis ID and place the captured prior findings under its BYOS
context directory:

```bash
bevor analyses current --json
mkdir -p .bevor/analyses/{analysis_id}/byos/context
mkdir -p .bevor/analyses/{analysis_id}/byos/raw-output
mkdir -p .bevor/analyses/{analysis_id}/findings
```

Move the temporary prior-findings JSON to
`.bevor/analyses/{analysis_id}/byos/context/prior-findings.json`.

For a fresh run, create the same directories after resolving the new analysis ID, but omit
`prior-findings.json`.

## Phase 2: Choose Scan Scope

Choose exactly one scope mode after creating the analysis.

### All First-Party Entry Points

```bash
bevor scopes set --mode first_party
```

### Entire Graph

```bash
bevor scopes set --mode all
```

### Explicit Scoped Scan

Discover candidate entry points, then add only the requested IDs:

```bash
bevor nodes list --entrypoints --json
bevor scopes clear
bevor scopes add <comma-separated-node-ids>
```

Verify and materialize the chosen scope:

```bash
bevor scopes list --json > .bevor/analyses/{analysis_id}/byos/context/scopes.json
bevor agent materialize
```

Materialization writes one `.raw.md` evidence bundle per waiting or failed scope under
`.bevor/analyses/{analysis_id}/`.

## Phase 3: Run The Selected Analyzer

Print the single preflight announcement required by `analyzer-adapter.md` after context and scope
are resolved, immediately before invoking the analyzer.

Invoke the selected analyzer with the prepared inputs. For an external command, adapt the flags to
the actual tool:

```text
<security-agent> scan \
  --scope-manifest <scopes-json> \
  --evidence-dir .bevor/analyses/{analysis_id}/ \
  --prior-findings <optional-prior-findings-json> \
  --output <tool-output>
```

For agents that inspect the working tree directly, still provide the Bevor scope manifest and
require every reported finding to include a matching `scope_id` or graph-backed `location_id`.

For agents that consume materialized evidence, provide only the selected `.raw.md` bundles and
optional prior findings.

Do not let the operations skill invent, strengthen, weaken, or reclassify security claims while
adapting output.

## Phase 4: Record Findings In Bevor

Normalize results using `findings-handoff.md`. Final bulk-import files belong under:

```text
.bevor/analyses/{analysis_id}/findings/
```

Choose one recording mode.

### Reviewed Draft Workflow

Use when findings need human or agent review before publication:

```bash
bevor findings add --file <finding.yaml>
bevor findings list --json
bevor analyses commit
```

Repeat `findings add --file` for each finding. Draft operations stage changes; `analyses commit`
publishes them. The current staged-add path does not transport the optional `source` field; preserve
tool attribution in the completion report or use one-shot import when `source` must be stored.

### One-Shot External Import

Use when the normalized directory is final:

```bash
bevor agent submit --dir .bevor/analyses/{analysis_id}/findings
```

This validates every YAML file before making the import request, imports the directory in one
operation, preserves the optional `source` field, and marks the analysis completed. Run it once,
only after the directory is final.

## Required Completion Report

Report:

- Selected analyzer name and scan instruction
- Fresh or prior-informed mode
- Parent analysis ID when prior-informed
- New analysis ID and code version
- Scope mode and selected scope IDs
- Number of normalized, rejected, and recorded findings
- Recording mode and CLI errors verbatim
