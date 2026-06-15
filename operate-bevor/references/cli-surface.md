# Bevor CLI Surface

> Generated from `bevor_cli.main:app`; do not edit manually.

Regenerate with `operate-bevor/scripts/generate_cli_reference.py` after CLI registration or
option changes.

## Global Options

- `--quiet, -q`: Suppress informational output; useful for scripting.
- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.

## Finding Import Values

- Types: `access_control`, `reentrancy`, `arithmetic`, `validation`, `logic`, `concurrency`, `economic`, `oracle`, `denial_of_service`, `upgradeability`, `data_exposure`, `cryptography`
- Levels: `critical`, `high`, `medium`, `low`

## `bevor agent`

Audit agent workflow shorthands.

## `bevor agent materialize`

Write each scope to ``.bevor/analyses/{analysis_id}/{scope_short_id}.raw.md`` (source + server call-chain text).

## `bevor agent setup`

Assumes user has ran `bevor init`. After that, running the setup will sync code, generate an analysis, and set the original scopes to first-party only.

## `bevor agent submit`

Import every YAML file in this directory as a separate submitted finding.

Parameters:

- `--dir, -d PATH`: Directory containing one ``.yaml`` / ``.yml`` mapping per finding. Default: ``.bevor/analyses/<analysis_id>/findings`` relative to cwd. See packages/cli/examples/findings_dir/.

## `bevor analyses`

Manage analyses.

## `bevor analyses commit`

Commit staged findings for an analysis.

Parameters:

- `--json, -j`: Print API response as JSON.

## `bevor analyses create`

Create a new analysis for the current code version and set it as active.

Parameters:

- `--no-parent`: Do not set parent_version_id (ignore config.analysis_id).
- `--force, -f`: Skip the local sync check (and the confirmation prompt). Not recommended.
- `--json, -j`: Print API response as JSON.

## `bevor analyses current`

Print details for the analysis selected in ``.bevor`` config.

Parameters:

- `--json, -j`: Output raw JSON.

## `bevor analyses fork`

Fork an analysis and set the new node as active in ``.bevor``.

Parameters:

- `--json, -j`: Print new analysis id as JSON.

## `bevor analyses import`

Import external findings (closes the analysis per server rules).

Parameters:

- `FILE` (required): JSON file: {"findings": [FindingBody, ...]}.
- `--json, -j`: Print API response as JSON.

## `bevor analyses latest`

Point ``.bevor`` ``analysis_id`` at the latest analysis for the current code version.

Parameters:

- `--json, -j`: Print chosen analysis as JSON.

## `bevor analyses list`

List analyses for the active project.

Parameters:

- `--project, -p TEXT`: Project ID (defaults to .bevor config).
- `--page-size, -n INTEGER`: Results per page.
- `--json, -j`: Output raw JSON.

## `bevor analyses run`

Start a run for the analysis in ``.bevor`` (``config.analysis_id``).

Parameters:

- `--no-wait`: Return immediately after starting the run instead of streaming SSE until completion.
- `--json, -j`: Print the run API response as JSON (machine-readable).
- `--silent`: No per-scope or status lines; if the event stream ends early, only one status fetch (no long poll).

## `bevor analyses select`

Set the active analysis for this directory.

Parameters:

- `ANALYSIS_ID`: Analysis ID (optional if interactive).
- `--analysis, -a TEXT`: Analysis ID to select directly.
- `--page-size, -n INTEGER`: Max analyses to fetch.
- `--yes, -y`: Non-interactive; fail if no analysis id given.

## `bevor chats`

Chat threads for the active analysis (start new, list, or resume).

## `bevor chats list`

List chat threads for the active analysis (``.bevor`` ``analysis_id`` only).

Parameters:

- `--page-size, -n INTEGER`: Results per page.
- `--json, -j`: Output raw JSON.

## `bevor chats new`

Create a chat thread and open the streaming terminal session.

Parameters:

- `--analysis-id TEXT`: Analysis id for the new thread (default: analysis_id from `.bevor`).

## `bevor chats resume`

Open the streaming session for an existing thread.

Parameters:

- `CHAT_ID` (required): Thread id (`bevor chats list --json`, field id).

## `bevor codes`

List, inspect, and upload code versions for the active project.

## `bevor codes current`

Print details for the code version selected in ``.bevor`` config.

Parameters:

- `--json, -j`: Output raw JSON.

## `bevor codes list`

List code versions for the active project.

Parameters:

- `--page-size, -n INTEGER`: Results per page.
- `--json, -j`: Output raw JSON.

## `bevor codes push`

Zip and upload the current directory as a new code version.

Parameters:

- `--private`: Mark this version as private.

## `bevor findings`

Draft findings for the active analysis.

## `bevor findings add`

Stage a new finding. ``--file`` is YAML; otherwise prompts interactively.

Parameters:

- `--file, -f PATH`: YAML file containing exactly one finding mapping (`type`, `level`, …, `description`).

## `bevor findings bulk`

Import every YAML file in this directory as a separate submitted finding.

Parameters:

- `--dir, -d PATH`: Directory containing one ``.yaml`` / ``.yml`` mapping per finding. Default: ``.bevor/analyses/<analysis_id>/findings`` relative to cwd. See packages/cli/examples/findings_dir/.

## `bevor findings delete`

Stage a finding deletion.

Parameters:

- `FINDING_ID` (required): Finding id to delete.
- `--json, -j`: Print API response as JSON.

## `bevor findings edit`

Stage an edit (`--file` YAML or interactive matching current metadata).

Parameters:

- `FINDING_ID` (required): Finding id to edit.
- `--file, -f PATH`: YAML with one mapping: ``type``, ``level``, ``name``, ``description``; optional ``recommendation`` / ``reference``.

## `bevor findings get`

Fetch a finding by wire id (runs against the authenticated project).

Parameters:

- `FINDING_ID` (required): Finding ID.
- `--json, -j`: Output raw JSON.

## `bevor findings list`

List findings (merged draft view for owners).

Parameters:

- `--node TEXT`: Only findings tied to this graph node id.
- `--no-draft`: Only on-run (published) findings, no staged draft rows in the same view.
- `--json, -j`: Output raw JSON.

## `bevor help`

Show root help text (alias for --help).

## `bevor init`

Link the current directory to a Bevor project.

Parameters:

- `--team, -t TEXT`: Team id.
- `--project, -p TEXT`: Project id to link directly (skips interactive picker).

## `bevor login`

Log in via browser.

## `bevor logout`

Remove stored credentials.

## `bevor nodes`

Inspect the code graph.

## `bevor nodes call-chain`

Call chain from a node. Use ``formatted`` as the first argument for server-rendered text.

Parameters:

- `NODE_ID` (required): Node id
- `--json, -j`: Output raw JSON (default mode only).

## `bevor nodes content`

Show the source code for a node.

Parameters:

- `NODE_ID` (required): Node short id (or full wire id).

## `bevor nodes edges`

List edges incident on a node.

Parameters:

- `NODE_ID` (required): Node short id or full wire id.
- `--direction TEXT`: Edge direction filter: in, out.
- `--type TEXT`: Edge type (e.g. calls, defines).
- `--json, -j`: Output raw JSON.

## `bevor nodes get`

Get a single node by short id (or full wire id).

Parameters:

- `NODE_ID` (required): Node short id (or full wire id).
- `--json, -j`: Output raw JSON.

## `bevor nodes interactive`

Explore the graph from a node: get, source, optional call-chain (callable nodes only), and edges.

Parameters:

- `NODE_ID` (required): Node to start from (short id or full id).

## `bevor nodes list`

List nodes for the active code version.

Parameters:

- `--entrypoints`: Only show auditable entry-point functions.
- `--file TEXT`: Filter to nodes in this file.
- `--no-deps`: Filter to nodes under this directory prefix.
- `--name TEXT`: Filter to nodes by name
- `--node-type TEXT`: Filter to nodes by type
- `--json, -j`: Output raw JSON.

## `bevor projects`

Manage projects.

## `bevor projects list`

List projects in a team.

Parameters:

- `--page-size, -n INTEGER`: Results per page.
- `--name TEXT`: Filter by name.
- `--all`: All projects across all teams
- `--json, -j`: Output raw JSON.

## `bevor projects select`

Interactively pick a project and save it as the active project.

Parameters:

- `PROJECT_ID`: Project id (optional if interactive).
- `--project, -p TEXT`: Project id to select directly (skips interactive picker).
- `--page-size, -n INTEGER`: Max projects to fetch for interactive selection.
- `--all`: All projects across all teams

## `bevor scopes`

Analysis scope nodes for the active analysis (see ``bevor analyses current``).

## `bevor scopes add`

Append nodes to the analysis scope (explicit mode).

Parameters:

- `IDS` (required): Comma-separated graph node ids to add.
- `--json, -j`: Print API response as JSON.

## `bevor scopes clear`

Clear explicit scopes on the active analysis (same as ``scopes set --mode unset``).

Parameters:

- `--json, -j`: Print API response as JSON.

## `bevor scopes list`

List scope nodes for an analysis.

Parameters:

- `--json, -j`: Output raw JSON.

## `bevor scopes remove`

Remove nodes from the analysis scope (explicit mode).

Parameters:

- `IDS` (required): Comma-separated graph node ids to remove.
- `--json, -j`: Print API response as JSON.

## `bevor scopes set`

Set how scope nodes are chosen (does not add/remove individual ids — use ``scopes add`` / ``scopes remove``).

Parameters:

- `--mode, -m [all|first_party|unset]` (required): Scope selection mode.
- `--json, -j`: Print API response as JSON.

## `bevor sessions`

List and revoke CLI sessions.

## `bevor sessions list`

List active CLI sessions.

## `bevor sessions revoke`

Revoke a CLI session by id.

Parameters:

- `TOKEN_ID` (required): CLI session id to revoke (from `bevor sessions`).

## `bevor status`

Derived state: linked team/project/code/analysis for this directory.

Parameters:

- `--json, -j`: Print structured status as JSON.

## `bevor teams`

Manage team context.

## `bevor teams list`

List teams you belong to.

Parameters:

- `--json, -j`: Output raw JSON.

## `bevor teams select`

Set the active team.

Parameters:

- `TEAM_ID`: Team id (optional if interactive).
- `--team, -t TEXT`: Team id to select directly.

## `bevor whoami`

Show the currently authenticated user.

Parameters:

- `--json, -j`: Print full user object as JSON.
