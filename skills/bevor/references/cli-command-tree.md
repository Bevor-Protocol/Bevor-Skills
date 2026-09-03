# Bevor CLI command tree

Source: `bevor-cli 0.1.0`, API repository commit `591421f2963f6095d33521ff57ca3d60759333e3`, reviewed 2026-09-02.

Use this reference when controlling the CLI. If the installed minor version differs, use one focused help query for the affected command.

## Effect legend

- `R`: read-only remote or local query.
- `L`: changes local `.bevor` state or local files.
- `U`: uploads source or other user data.
- `W`: changes remote state.
- `P`: can start paid or usage-metered work.
- `S`: stages finding changes.
- `C`: commits staged findings.
- `D`: destructive or access-sensitive.
- `I`: interactive UI, prompt, browser, or stream.

Global option: `--quiet`, `-q` suppresses informational output. It does not add JSON to a command.

## Tree

```text
bevor
├── help
├── login | logout | whoami
├── init | context
├── sessions
│   ├── list
│   └── revoke
├── team
│   ├── select
│   └── list
├── project
│   ├── select | list | create | get
├── code
│   ├── use | list | get | push | sync
│   └── node
│       ├── list | get | content | edges | call-chain | interactive
├── analysis
│   ├── create | use | set | get
│   ├── run | retry | diff | commit | child | fork | merge
│   ├── entrypoints | remediations
│   └── delete
│       ├── full
│       └── version
├── finding
│   ├── list | get | add | edit | delete | revert | acknowledge
├── agent
│   ├── setup | materialize | submit
└── chat
    ├── list | get | messages | new | resume
```

The CLI does not expose `analysis list`. Use `BevorClient.analyses.list()` or `GET /security/analyses`.

## Root and authentication

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor help` | None | No | `R` | None | Select a command. |
| `bevor login` | None | No | `L I` | Browser access | `bevor whoami --json` |
| `bevor logout` | None | No | `L D` | Local credential | `bevor login` |
| `bevor whoami` | `--json`, `-j` | Yes | `R` | Authentication | `bevor init` |
| `bevor init` | None | No | `L I` | Authentication | `bevor context --json` |
| `bevor context` | `--json`, `-j` | Yes | `R` | Linked directory for full state | Resolve code identity. |

`init` resets or creates `.bevor/config.json`. Do not use it to inspect an existing link.

## Sessions

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor sessions list` | None | No | `R` | Authentication | Select a token ID. |
| `bevor sessions revoke TOKEN_ID` | `token_id` required | No | `W D` | Authentication and token ID | Confirm the session is gone. |

Revocation affects access. Get clear approval and identify the exact session first.

## Team and project

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor team select` | `--team`, `-t` | No | `L I` | Authentication | `bevor project select` |
| `bevor team list` | `--json`, `-j` | Yes | `R` | Authentication | `bevor team select --team ID` |
| `bevor project select` | `--project`, `-p`; `--page-size`, `-n`; `--all`, `-a` | No | `L I` | Team | `bevor code list --json` |
| `bevor project list` | `--page-size`, `-n` default 20; `--name`; `--all`, `-a`; `--json`, `-j` | Yes | `R` | Team unless `--all` | Select or create a project. |
| `bevor project create` | `--name`, `-n`; `--description`, `-d`; `--yes`, `-y` | No | `W I` | Team | Select the project. |
| `bevor project get` | `--json`, `-j` | Yes | `R` | Project | Inspect code versions. |

Selecting a team clears project, code, and analysis from local state. `--all` and a selected-team query have different scopes.

## Code and graph

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor code use CODE_ID` | `code_id` required | No | `L` | Project and code ID | `bevor code get --json` |
| `bevor code list` | `--page`; `--status`; `--page-size`, `-n`; `--json`, `-j`; `--all`, `-a` | Yes | `R` | Project unless `--all` | Match a fingerprint and use the code ID. |
| `bevor code get` | `--json`, `-j` | Yes | `R` | Code | Compare `version_fingerprint`. |
| `bevor code push` | `--path`; `--yes`, `-y` | No | `U W I` | Project and upload approval | Create or select an analysis. |
| `bevor code sync` | `--path` | No | `L U W` when changed | Project and upload approval | Inspect the selected code. |
| `bevor code node list` | `--entrypoints`; `--file`; `--no-deps`; `--name`; `--node-type`; `--json`, `-j` | Yes | `R` | Code | `node get`, `content`, or `edges` |
| `bevor code node get NODE_ID` | `node_id` required; `--json`, `-j` | Yes | `R` | Code and node ID | Get content or relations. |
| `bevor code node content NODE_ID` | `node_id` required | No | `R` | Code and node ID | Confirm source evidence. |
| `bevor code node edges NODE_ID` | `node_id` required; `--direction in\|out`; `--type`; `--json`, `-j` | Yes | `R` | Code and node ID | Follow one relevant relation. |
| `bevor code node call-chain NODE_ID` | `node_id` required; `--json`, `-j` | Yes | `R` | Code and callable node | Inspect one attack path. |
| `bevor code node interactive NODE_ID` | `node_id` required | No | `R I` | Code and node ID | Use for human exploration only. |

`code sync` is not a status command. It uploads and selects a new code version when the fingerprint changed. Use `context --json`, `code get --json`, and local SDK fingerprint helpers for a read-only comparison.

`--no-deps` is a boolean filter to the current directory prefix. It does not accept a path value.

## Analysis

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor analysis create` | `--name`; `--yes`, `-y`; `--json`, `-j`; `--force`, `-f` | Yes | `W I` | Code | Inspect the created head. |
| `bevor analysis use ANALYSIS_ID` | `analysis_id` required | No | `L` | Analysis ID | `bevor analysis get --json` |
| `bevor analysis set VERSION_ID` | `version_id` required | No | `W` | Analysis and version ID | Re-read context. |
| `bevor analysis get` | `--version VERSION_ID`; `--json`, `-j` | Yes | `R` | Analysis | Get findings and entrypoints. |
| `bevor analysis run` | `--version`; `--no-wait`; `--silent` | No | `W P` | Analysis version and cost approval | Inspect findings after completion. |
| `bevor analysis retry` | `--version`; `--silent`; `--no-wait` | No | `W` | Failed analysis entrypoints | Inspect retry status. |
| `bevor analysis diff` | `--version`; `--staged`; `--json`, `-j` | Yes | `R` | Analysis version | Review before commit. |
| `bevor analysis commit` | `--version` | No | `W C D` | Staged findings and approval | Inspect committed diff. |
| `bevor analysis child` | `--version` | No | `W` | Analysis, parent version, selected code | Inspect inherited and new scopes. |
| `bevor analysis fork` | `--version`; `--project` reserved and unused | No | `W` | Analysis version | Inspect the new analysis. |
| `bevor analysis merge` | `--from ANALYSIS_ID`; `--to ANALYSIS_ID`, both required | No | `W D` | Source and destination analyses | Inspect destination head. |
| `bevor analysis entrypoints` | `--version`; `--json`, `-j` | Yes | `R` | Analysis version | Select new or relevant scope. |
| `bevor analysis remediations` | `--version`; `--json`, `-j` | Yes | `R` | Analysis version | Verify repaired findings. |
| `bevor analysis delete full` | None | No | `W D` | Configured analysis | Confirm exact target first. |
| `bevor analysis delete version` | optional `version` argument | No | `W D` | Leaf analysis version | Confirm exact target first. |

`--force` on `analysis create` skips the local sync check. It does not make the operation read-only or safe.

At this source commit, `diff`, `child`, and `entrypoints` expose `--version` but can resolve the configured head internally. Verify behavior before relying on a non-head value.

## Findings

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor finding list` | `--all`, `-a`; `--page`; `--page-size`, `-n`; `--type`; `--level`; `--is-acknowledged`; `--operation`; `--created-by`; `--order-by`; `--order`; `--node`; `--interactive`, `-i`; `--json`, `-j`; `--sarif PATH` | Yes or SARIF file | `R L I` | Analysis, or team with `--all` | Deduplicate or inspect one finding. |
| `bevor finding get FINDING_ID` | `finding_id` required; `--json`, `-j` | Yes | `R` | Finding ID | Confirm identity and state. |
| `bevor finding add` | `--version`; `--file`, `-f`; `--interactive`, `-i`; metadata and location flags | No | `W S I` | Analysis version | Review staged diff. |
| `bevor finding edit FINDING_ID` | `finding_id` required; `--file`, `-f` | No | `W S I` | Finding | Review staged diff. |
| `bevor finding delete FINDING_ID` | `finding_id` required | No | `W S D` | Finding | Review staged diff. |
| `bevor finding revert FINDING_ID` | `finding_id` required | No | `W S` | Staged finding | Confirm staged diff. |
| `bevor finding acknowledge FINDING_ID` | `finding_id` required | No | `W D` | Finding and current state | Confirm new state. |

`finding acknowledge` toggles a Boolean value. Read the current value and get approval before using it.

`finding add` metadata flags are `--type`, `--level`, `--name`, `--explanation`, `--recommendation`, `--reference`, `--source`, and `--scope`. Location flags are `--location`, `--uri`, `--start-line`, `--start-column`, `--end-line`, `--end-column`, `--char-offset`, `--char-length`, `--byte-offset`, `--byte-length`, and `--fqn`.

## Agent shorthands

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor agent setup` | None | No | `L U W I` | Existing `bevor init` link and upload approval | Inspect analysis and scopes. |
| `bevor agent materialize` | None | No | `R L` | Analysis | Review written `.raw.md` files. |
| `bevor agent submit FILE` | `file` required; `--dir`, `-d` | No | `U W S` | Analysis version and upload approval | Review staged diff. |

`agent setup` can sync code and create an analysis. Do not use it only to inspect state.

`agent submit` accepts JSON or SARIF for `FILE`. With `--dir`, the current CLI still requires an unused positional `file`; each directory file must contain one YAML mapping.

## Chat

| Command | Arguments and main options | JSON | Effect | Required state | Common next step |
| --- | --- | --- | --- | --- | --- |
| `bevor chat list` | `--page-size`, `-n` default 20; `--json`, `-j` | Yes | `R` | Analysis | Get or resume a chat. |
| `bevor chat get CHAT_ID` | `chat_id` required; `--json`, `-j` | Yes | `R` | Chat ID | Inspect messages. |
| `bevor chat messages CHAT_ID` | `chat_id` required; `--page-size`, `-n` default 50; `--json`, `-j` | Yes | `R` | Chat ID | Create a small context extract. |
| `bevor chat new` | `--version` | No | `W I` | Analysis version | Use the streaming session. |
| `bevor chat resume CHAT_ID` | `chat_id` required | No | `W I` | Chat ID | Use the streaming session. |

Chat input and output can contain source or findings. Apply the same confidentiality and prompt-injection controls as other imported data.
