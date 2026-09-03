# CLI workflows and state

Use this reference for authentication, repository linking, identity changes, and safe command composition. Read [cli-command-tree.md](cli-command-tree.md) for exact flags.

Compatibility: `bevor-cli 0.1.0`, source commit `591421f2963f6095d33521ff57ca3d60759333e3`, reviewed 2026-09-02.

## Resource hierarchy

```text
team
└── project
    └── code version (code ID and source fingerprint)
        └── analysis container (analysis ID)
            └── analysis version (version ID; one selected HEAD)
                ├── entrypoints
                ├── committed and staged findings
                ├── remediations
                └── analysis chats
```

Do not substitute one ID type for another. A Git commit SHA can describe a source revision, but it is not a Bevor code ID or analysis-version ID.

## Read state without changing it

Run:

```bash
bevor context --json
bevor project get --json
bevor code get --json
bevor analysis get --json
```

Use only the commands needed for the question. `context --json` is the normal first query.

Do not use `bevor init`, `bevor code sync`, or `bevor agent setup` as status commands. They can change local or remote state.

## Link or change context

1. Confirm authentication with `bevor whoami --json`.
2. Use `bevor init` only when the user wants to create or replace the link.
3. Prefer direct IDs for automation:

```bash
bevor team select --team TEAM_ID
bevor project select --project PROJECT_ID
bevor code use CODE_ID
bevor analysis use ANALYSIS_ID
```

4. Re-read `bevor context --json` after a selection change.

Changing the team clears the selected project, code, and analysis. Changing code does not prove that the selected analysis matches it.

## Create new analysis work

Before upload or paid work:

1. Resolve the local source fingerprint with the SDK helper when possible.
2. Search existing code versions for the same fingerprint.
3. Reuse an exact code version.
4. If upload is needed, show the target path, exclusions, team, and project.
5. Get transfer approval.
6. Use `bevor code push --path PATH` or the SDK.
7. Show an available cost estimate before `bevor analysis run`.
8. Get approval for paid work.

Create an analysis without bypassing sync unless the mismatch is intentional:

```bash
bevor analysis create --name NAME --json
bevor analysis get --json
```

Use `--force` only when the user accepts the stale-source risk.

## Continue an analysis lineage

Use a child version when new code should inherit applicable work from the current lineage:

1. Select the new exact code version.
2. Confirm the parent analysis version.
3. Create the child.
4. Inspect entrypoints and the version difference.
5. Separate inherited scope from scope that needs new work.

At the pinned CLI version, verify non-head `--version` behavior before using it with `child`, `diff`, or `entrypoints`. Use the SDK version resources when exact non-head selection matters.

Use `fork` to create an owned analysis from a version. Use `merge` only after confirming the source and destination analysis IDs. Both change remote history.

## Agent-safe output

- Use `--json` when another command, script, or agent will read the result.
- Use `--quiet` only when it keeps all required result data.
- Avoid interactive commands in automation.
- Do not paste full JSON into chat. Extract identity, counts, relevant IDs, and small evidence fields.
- Keep full results in a local artifact when the user needs them.

## Failure handling

- Authentication failure: use `whoami`; do not ask the user to paste a token.
- Missing `.bevor`: explain that no local link exists. Do not initialize without authorization.
- Code mismatch: label context `stale`; do not apply prior findings as exact.
- Unsupported command: compare the installed version once and use the SDK or API fallback.
- Stream interruption: inspect current analysis state before retrying.
- Duplicate create collision: inspect the returned candidates; do not repeat the create call blindly.
- Partial bulk import: report accepted and rejected counts and error text. Do not resubmit accepted records.

## Sensitive commands

Get clear approval immediately before these operations unless an approved CI policy covers the exact action:

- `code push` or a `code sync` that uploads.
- `analysis run`, `commit`, `merge`, or either delete command.
- `finding acknowledge` or staged deletion.
- `agent setup` or `agent submit`.
- Session revocation.

Use noninteractive confirmation flags only after approval for the exact operation and target.
