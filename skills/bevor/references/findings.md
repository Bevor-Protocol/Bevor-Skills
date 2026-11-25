# Findings

## 1. What counts as a finding

A finding needs a root cause, an attacker-reachable path to it, and a concrete effect. Before recording one, try to refute it: check every guard, modifier, and precondition on the path, and confirm the required state can occur. Leave out style issues, gas tweaks, and linter noise without a security effect.

Record suspected issues you couldn't confirm too: Bevor is the record a person reviews. Say in the `explanation` what's unconfirmed and what would confirm or rule it out.

## 2. Check what's already recorded

Before writing, compare against `bevor findings list --json` (`--level` and `--type` narrow it) by root cause, location, affected asset, and attack path, not by title. Don't record a finding twice. To correct one, pass only the fields that change:

```bash
bevor findings edit FINDING_ID --level medium --explanation "Updated text."
```

`--type`, `--level`, `--name`, `--explanation`, `--recommendation`, and `--poc` are each optional; `--recommendation ""` clears it. `--file edit.yaml` takes the same fields as YAML. A finding's location can't be edited: delete it (`bevor findings delete FINDING_ID`) and add it again.

## 3. Write them

Writes go to HEAD, or the version given with `--version`, as soon as they run, so you can record each finding as you validate it. Everything goes through `bevor findings add`:

| What you have | Command |
| --- | --- |
| Findings as YAML, written inline | `bevor findings add - --tool TOOL_NAME <<'EOF' ... EOF` |
| A YAML file with one or more findings | `bevor findings add findings.yaml --tool TOOL_NAME` |
| A directory of YAML files | `bevor findings add findings/ --tool TOOL_NAME` |
| JSON: a list of findings, or an object with a `findings` list | `bevor findings add findings.json --tool TOOL_NAME` |
| One finding as flags | `bevor findings add --tool TOOL_NAME --type TYPE --level LEVEL --name NAME --explanation TEXT --location NODE` |
| A static analyzer's SARIF output | `bevor findings add results.sarif` |

In YAML, each finding is one document; separate several with `---`. JSON uses the same fields.

```yaml
type: reentrancy
level: high
name: Withdraw sends ETH before updating balances
explanation: Preconditions, attack path, and effect.
recommendation: Update balances before the external call.
location: src/Vault.sol:42-50
entrypoint: Vault.withdraw
```

`location` and `entrypoint` take the same forms as the [graph commands](graph-navigation.md#questions-to-ask-it): a node id, a name, or a file and line. A name must match exactly one node. For columns or offsets, use a mapping with `strategy: physical`, `uri`, and the region keys (`startLine`/`endLine`, optionally `startColumn`/`endColumn`; or `charOffset`/`charLength`; or `byteOffset`/`byteLength`).

### Where a finding lands

A location must be reachable from an entrypoint: a function, modifier, or state variable on its call chain. A file and line resolves to the smallest node containing it; when that's a statement, it moves to the innermost enclosing node an entrypoint reaches, and a range that runs past the end of a function moves to the function it starts in. A contract, a pragma, or code no entrypoint reaches is rejected with the reason.

The finding goes on every entrypoint that reaches its location. With `entrypoint`, it goes on that one, which must reach it. Either way, those entrypoints are marked partially covered by the tool.

## 4. Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `type` | yes | The vulnerability class, such as `reentrancy` or `access-control`. |
| `level` | yes | `critical`, `high`, `medium`, or `low`. |
| `name` | yes | A short title naming the root cause. |
| `explanation` | yes | Preconditions, attacker capabilities, the step-by-step path, and the effect. |
| `recommendation` | no | A concrete fix. |
| `poc` | no | Reproduction steps or a test reference. |
| `location` | yes | A node id, a name, or a file and line range. |
| `entrypoint` | no | The one entrypoint to put the finding on ([where it lands](#where-a-finding-lands)). |

The tool isn't a field; it's `--tool` on the command ([naming the tool](../SKILL.md#naming-the-tool)).

## 5. SARIF

Add a static analyzer's SARIF output directly rather than rewriting it as YAML.

- **Tool name:** taken from each run's driver (`runs[].tool.driver.name`); `--tool` isn't accepted. If a driver name doesn't match how that analyzer already appears in Bevor, fix it in the file first.
- **Location:** a result is placed by its file region. One with only a symbol name goes on the node with that name, in its file when the result gives one. Results whose name matches no node or several are skipped, as are those with no location. The command prints how many results it read and skipped, with the reason for each skip.
- **Severity:** SARIF levels don't map exactly to Bevor's. Check them after adding.

## 6. What the command tells you

`bevor findings add` prints each stored finding's id, name, and the node it landed on. Pass `--json` for `{"results": [...], "skipped": [...]}` instead. Anything not stored is listed with the reason, and the command exits 1. The rest are stored, so fix the location or entrypoint of only the skipped ones and add those again; re-adding the whole file would duplicate the others.
