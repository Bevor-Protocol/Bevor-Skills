# CLI command tree

Generated from installed bevor-cli 0.2.1 (released package).
Regenerate with `python skills/bevor/scripts/check_cli_contract.py --update`.
No authentication or command callback runs during generation.

This is syntax metadata, not a guarantee of remote behavior. See the workflow references for write boundaries and verified recipes.
The release help can still say staged even though the finding writes apply immediately.

| Command | Available options |
| --- | --- |
| `bevor analyses` |  |
| `bevor analyses create` | `--new`, `--name`, `--version`, `--collision`, `--yes`, `--json`, `--force` |
| `bevor analyses delete` |  |
| `bevor analyses delete full` |  |
| `bevor analyses delete version` |  |
| `bevor analyses deselect` |  |
| `bevor analyses entrypoints` | `--version`, `--json` |
| `bevor analyses fork` | `--version` |
| `bevor analyses lineage` | `--limit`, `-n`, `--oneline`, `--json` |
| `bevor analyses list` | `--page`, `--page-size`, `--order`, `--order-by`, `--project`, `--user`, `--is-owner`, `--json` |
| `bevor analyses materialize` |  |
| `bevor analyses merge` | `--from-version`, `--to` |
| `bevor analyses run` | `--version`, `--all`, `--no-wait`, `--silent` |
| `bevor analyses select` | `--page`, `--page-size`, `--recent` |
| `bevor analyses set-head` |  |
| `bevor analyses transitions` | `--page`, `--page-size`, `--order`, `--order-by`, `--kind`, `--version`, `--project-wide`, `--json` |
| `bevor analyses view` | `--version`, `--json` |
| `bevor chats` |  |
| `bevor chats list` | `--page`, `--page-size`, `--order`, `--order-by`, `--project`, `--json` |
| `bevor chats messages` | `--json` |
| `bevor chats new` |  |
| `bevor chats resume` |  |
| `bevor chats view` | `--json` |
| `bevor codes` |  |
| `bevor codes list` | `--page`, `--page-size`, `--order`, `--order-by`, `--project`, `--network`, `--identifier`, `--status`, `--json` |
| `bevor codes nodes` |  |
| `bevor codes nodes call-chain` | `--code`, `--json` |
| `bevor codes nodes content` | `--code` |
| `bevor codes nodes edges` | `--code`, `--direction`, `--type`, `--json` |
| `bevor codes nodes interactive` | `--code` |
| `bevor codes nodes list` | `--code`, `--entrypoints`, `--file`, `--no-deps`, `--name`, `--node-type`, `--json` |
| `bevor codes nodes view` | `--code`, `--json` |
| `bevor codes push` | `--path`, `--no-wait`, `--yes` |
| `bevor codes select` |  |
| `bevor codes view` | `--json` |
| `bevor findings` |  |
| `bevor findings acknowledge` |  |
| `bevor findings add` | `--version`, `--file`, `--interactive`, `--type`, `--level`, `--name`, `--explanation`, `--recommendation`, `--poc`, `--tool`, `--node`, `--location`, `--uri`, `--start-line`, `--start-column`, `--end-line`, `--end-column`, `--char-offset`, `--char-length`, `--byte-offset`, `--byte-length`, `--fqn` |
| `bevor findings delete` |  |
| `bevor findings edit` | `--file`, `-f` |
| `bevor findings import` | `--version` |
| `bevor findings list` | `--project-wide`, `--version`, `--interactive`, `--sarif`, `--type`, `--level`, `--acknowledged`, `--page`, `--page-size`, `--order`, `--order-by`, `--project`, `--self`, `--user`, `--code`, `--analyses`, `--created-by-self`, `--created-by`, `--json` |
| `bevor findings unacknowledge` |  |
| `bevor findings undo` |  |
| `bevor findings view` | `--json` |
| `bevor help` |  |
| `bevor link` |  |
| `bevor login` |  |
| `bevor logout` |  |
| `bevor projects` |  |
| `bevor projects create` | `--name`, `--description`, `--kind`, `--yes` |
| `bevor projects list` | `--json` |
| `bevor projects select` |  |
| `bevor projects view` | `--json` |
| `bevor reflog` | `--limit`, `-n`, `--json` |
| `bevor sessions` |  |
| `bevor sessions list` |  |
| `bevor sessions revoke` |  |
| `bevor status` | `--json` |
| `bevor sync` | `--run`, `--yes` |
| `bevor upgrade` |  |
| `bevor whoami` | `--json` |
| `bevor workspaces` |  |
| `bevor workspaces list` | `--json` |
| `bevor workspaces select` |  |
| `bevor workspaces view` | `--json` |
