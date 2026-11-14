# CLI workflows and state

Reviewed against released CLI 0.2.1 on 2026-11-14. The command tree is generated from the installed Typer application.

## Identity and local state

Workspace → project → code versions and analyses → analysis versions (one HEAD) → findings and entrypoints.

A code ID, analysis ID, and analysis-version ID are different identifiers. Local selection lives in `.bevor/config.json`. Changing workspace/project clears downstream selections. Selecting code preserves the analysis so a child can use its current HEAD.

## Connect an existing Dashboard project

Use direct IDs to avoid interactive selection in agents and CI:

```bash
bevor workspaces list --json
bevor workspaces select WORKSPACE_ID
bevor projects list --json
bevor projects select PROJECT_ID
bevor status --json
```

For human interactive setup, `bevor link` chooses a workspace and project. It resets local linkage. It does not upload source.

Create a project only when requested. All fields below avoid prompts:

```bash
bevor projects create --name "Audit project" --description "Security review" --kind standard --yes
bevor status --json
```

Project creation selects the new project. The command has no JSON-output flag. Read IDs from status afterward.

Selecting a project clears any previously selected analysis. To resume existing work in this project:

```bash
bevor analyses list --json
bevor analyses select ANALYSIS_ID
bevor status --json
```

Verify the analysis and HEAD before importing findings. Match/select the target code separately and check local source identity.

## First code and analysis

Resolve matching existing versions first:

```bash
bevor codes list --json
bevor codes select CODE_ID
bevor status --json
```

Verify `working_tree.matches_code` and `code.status`. A failed code upload can still match the fingerprint. Do not create analysis work until code processing succeeds.

When an authorized source upload is needed, run from the target root:

```bash
bevor codes push --yes
bevor analyses create --new --name "Audit" --yes --json
bevor status --json
```

Keep finding files, reports, and temporary output outside the source tree before fingerprinting. Source uploads can include UTF-8 files beyond contract source.

An existing exact version can cause a collision result even with a successful exit code. Inspect the response type and returned candidates. Select the intended existing analysis; use `--collision force` only for an intentionally separate lineage. Do not blindly retry.

Creating an analysis does not run the paid pipeline. `bevor analyses run` is separate and requires authorization for that work.

## Continue a lineage after a branch change

Record the current analysis and parent HEAD before selecting the new exact code:

```bash
bevor analyses view --json
bevor codes select NEW_CODE_ID
bevor status --json
bevor analyses create --yes --json
bevor analyses lineage --json
bevor analyses transitions --json
bevor analyses entrypoints --json
bevor findings list --json
```

With an analysis selected, create adds a child version and moves HEAD. Do not pass `--new`, which starts another analysis. Confirm the returned child has the expected parent and code.

If code is new, replace code selection with an authorized `bevor codes push --yes`. `bevor sync --yes` combines source upload and child creation, so use it only when both are intended.

Review carried findings and purported remediations before starting new audit work. Rename or hash mismatch can hide surviving findings. Check node ownership as well as function bodies.

To read a specific version, use supported commands' `--version VERSION_ID`. To move shared HEAD, use `bevor analyses set-head VERSION_ID` only when that change is intended. Fork and merge also change remote history.

## Failure handling

- On an authentication error, check the account once and reauthorize if needed.
- On unknown command/option, consult that command's help once. Do not repeat full setup.
- On rate limits, use bounded backoff and sequential requests. Stop repeated failures with evidence.
- On a stream timeout or ambiguous write, inspect remote state before retrying.
- On import failure, read accepted records before resubmitting.
- On JSON serialization failure, use supported text output or a narrow released-SDK query. Report the defect.
