# Findings

## 1. What counts as a finding

A finding needs a root cause, an attacker-reachable path to it, and a concrete effect. Before recording one, try to refute it: check every guard, modifier, and precondition on the path, and confirm the required state can occur. Leave out style issues, gas tweaks, and linter noise without a security effect.

Record suspected issues you couldn't confirm too: Bevor is the record a person reviews. Say in the `explanation` what's unconfirmed and what would confirm or rule it out.

## 2. Check what's already recorded

Before writing, compare against `bevor findings list --json` (`--level` and `--type` narrow it) by root cause, location, affected asset, and attack path, not by title. Don't record a finding twice. To correct one, write its fields to a YAML file and edit it:

```bash
bevor findings edit FINDING_ID --file finding.yaml
```

The file needs every required field (`type`, `level`, `name`, `explanation`), not only the ones you're changing, and no `location` or `entrypoint`. Without `--file`, `edit` prompts interactively.

## 3. Write them

Writes go to HEAD, or the version given with `--version`, as soon as they run, so you can record each finding as you validate it. When you have several ready at once, one import is a single call instead of one `findings add` each.

| What you have | Command |
| --- | --- |
| One finding | `bevor findings add --tool TOOL_NAME --type TYPE --level LEVEL --name NAME --explanation TEXT --node NODE_ID` |
| One finding in a YAML file | `bevor findings add --tool TOOL_NAME --file finding.yaml` |
| Several findings in one YAML file | `bevor findings import findings.yaml --tool TOOL_NAME` |
| A directory of YAML files | `bevor findings import findings/ --tool TOOL_NAME` |
| JSON with a top-level `findings` list | `bevor findings import findings.json --tool TOOL_NAME` |
| A static analyzer's SARIF output | `bevor findings import results.sarif` |

With flags, each [field](#4-fields) is its own flag (`--recommendation`, `--poc`, `--entrypoint ENTRYPOINT_ID`, ...), and the location is exactly one of `--node NODE_ID`, `--uri FILE` with `--start-line` and `--end-line`, or `--fqn NAME`.

In YAML, each finding is one document; separate several with `---`. JSON uses the same fields.

```yaml
type: reentrancy
level: high
name: Withdraw sends ETH before updating balances
explanation: Preconditions, attack path, and effect.
recommendation: Update balances before the external call.
location:
  strategy: node_id
  node_id: NODE_ID
entrypoint:
  strategy: node_id
  node_id: ENTRYPOINT_NODE_ID
```

`location` and `entrypoint` take a `strategy`: `node_id` with `node_id` (preferred), `physical` with `uri` and `startLine`/`endLine`, or `logical` with `fully_qualified_name`.

## 4. Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `type` | yes | The vulnerability class, such as `reentrancy` or `access-control`. |
| `level` | yes | `critical`, `high`, `medium`, or `low`. |
| `name` | yes | A short title naming the root cause. |
| `explanation` | yes | Preconditions, attacker capabilities, the step-by-step path, and the effect. |
| `recommendation` | no | A concrete fix. |
| `poc` | no | Reproduction steps or a test reference. |
| `location` | yes | A graph node (preferred), a file and line range, or a fully qualified name. |
| `entrypoint` | no | The entrypoint the finding is reached through. Without it, the finding goes on every entrypoint that reaches the location. Either way, those entrypoints are marked partially covered by the tool. |

The tool isn't a field; it's `--tool` on the command ([naming the tool](../SKILL.md#naming-the-tool)).

## 5. SARIF

Import a static analyzer's SARIF output directly rather than rewriting it as YAML.

- **Tool name:** taken from each run's driver (`runs[].tool.driver.name`); `--tool` isn't accepted. If a driver name doesn't match how that analyzer already appears in Bevor, fix it in the file first.
- **Location:** results are matched to graph nodes by file location. One outside the parsed source may end up without a node.
- **Severity:** SARIF levels don't map exactly to Bevor's. Check them after importing.

## 6. Confirm what was stored

After every write, run `bevor findings list --json` and compare the count, severity, and location of each finding with what you wrote. Fix mismatches with `bevor findings edit`. After an uncertain or failed write, list before retrying, so you don't create duplicates.
