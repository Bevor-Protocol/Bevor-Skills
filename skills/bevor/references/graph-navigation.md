# Graph navigation

Bevor parses the whole codebase into a graph: every function, modifier, state variable, and contract, and how they relate. The `bevor graph` commands query HEAD's code. Edges come from parsing, not name matching, so a query is complete (it covers files you haven't opened), exact (overloads and inheritance resolve correctly), and repeatable. Querying it first means you only read source for the nodes that matter.

## Questions to ask it

`graph nodes` and `graph edges` show 10 results by default; pass `--limit 0` when you need all of them.

| Question | Query |
| --- | --- |
| What can an outside caller reach? | `bevor graph nodes --entrypoint --no-deps --limit 0 --json` |
| Where is a function or variable? | `bevor graph nodes --name NAME --json` |
| What does this node look like? | `bevor graph show NODE_ID --source --json` |
| What does this function call? | `bevor graph edges --node NODE_ID --type calls --direction out --json` |
| Who calls it? | `bevor graph edges --node NODE_ID --type calls --direction in --json` |
| What state does it change? | `bevor graph edges --node NODE_ID --type writes --direction out --json` |
| What else writes this variable? | `bevor graph edges --node VARIABLE_ID --type writes --direction in --json` |
| Which guards protect it? | `bevor graph edges --node NODE_ID --type modified_by --json` |
| Where does it call other contracts? | `bevor graph edges --node NODE_ID --type calls_external --json` |

If you've already run `bevor analyses coverage --json`, it lists the same entrypoints with their coverage; `graph nodes --entrypoint` is for filtering them, by `--file` or `--name`, or for when you have no analysis selected. `--no-deps` leaves out dependency code. Follow one relation at a time, and stop when further nodes can't change the asset, invariant, or attack path you're examining. Don't dump the whole graph into context.

`bevor graph call-chain NODE_ID --json` is also available: the pre-computed execution path from a function through everything it calls, annotated with the state each step reads and writes, resolved to the storage it actually touches. It's the function's full execution context as one retrievable result, instead of context you'd rebuild by recursively following calls and searching source.

## Relations

| Relation | Meaning |
| --- | --- |
| `calls` | Internal call flow. |
| `calls_external` | Calls to other contracts: external-call boundaries and callback surfaces. |
| `reads`, `writes` | State the node reads or changes. |
| `inherits`, `overrides` | Effective behavior across the contract hierarchy. |
| `modified_by` | Modifiers and guards. |
| `has_constraint`, `has_condition` | Preconditions and control conditions. |
| `emits`, `throws` | Events and error paths. |

`bevor graph edges --help` lists the rest.

## When to read source directly

To confirm what a node does, for exact identifiers and constants, and for code the graph doesn't cover (configuration, off-chain code). Fall back to broad search only when the graph doesn't cover the target, and say so.
