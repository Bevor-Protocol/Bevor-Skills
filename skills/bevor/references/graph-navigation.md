# Graph navigation

Use this reference for graph queries, change impact, call paths, stable locations, and graph-backed tools.

Compatibility: native semantic graph behavior at API commit `591421f2963f6095d33521ff57ca3d60759333e3`, reviewed 2026-09-02.

## Current domain boundary

The current source types contain these language and framework values:

- Solidity: Foundry, Hardhat, Truffle, or pure Solidity on EVM.
- Rust: Anchor and Soroban type values exist.
- Platform values: EVM, Solana, and Stellar.

Only Solidity has the complete native parser, resolver, semantic edge builder, and SDK graph helpers at the pinned commit. Treat Anchor and Soroban native DSL graph support as future work until a release source shows their parser and edge registries.

SARIF or generic finding import can still support results from other ecosystems. That is different from native DSL graph support.

## Start narrow

1. Run `bevor context --json` and record the exact code ID.
2. Find a node with a narrow query:

```bash
bevor code node list --name NAME --json
bevor code node list --file PATH --node-type TYPE --json
bevor code node list --entrypoints --no-deps --json
```

3. Use `node get` for metadata.
4. Use `node content` only for the necessary source segment.
5. Follow one relation type and direction at a time.
6. Use `call-chain` for callable behavior.
7. Query findings for the node before calling the area new work.
8. Stop when more nodes no longer affect the question or attack path.

Do not load the whole graph into model context. Use the SDK for repeated traversal and keep raw data in memory or a file.

## Edge meanings

| Edge | Security use |
| --- | --- |
| `calls` | Internal callable flow. Follow out for callees and in for callers. |
| `calls_external` | External-call boundary and integration risk. |
| `reads` | State or value that can influence behavior. |
| `writes` | State that the node can change. |
| `inherits`, `overrides` | Effective behavior across contract hierarchy. |
| `modified_by` | Modifier or guard attached to callable behavior. |
| `has_access_control` | Access restriction represented by the graph. |
| `has_constraint`, `has_condition` | Preconditions and control conditions. |
| `emits`, `throws` | Observable events and error paths. |
| `defines`, `initializes`, `instantiates` | Ownership and construction relations. |
| `uses`, `typed_as`, `accesses` | Data, type, and member dependencies. |
| `implements`, `extends` | Interface and type-extension relationships. |
| `references`, `has_ref_comment` | Source reference and inherited documentation links. |

An edge is a structural fact. Its presence or absence is not a security verdict.

## Change-impact procedure

For each changed semantic node:

1. Record direct callers and callees.
2. Record state read and written by the node.
3. Find other nodes that read or write the same state.
4. Include modifiers, access controls, constraints, and conditions.
5. Include inheritance and overrides.
6. Mark external calls, emitted events, and error paths.
7. Follow transitive relations only while they can change an asset, invariant, authorization rule, or attack path.
8. Compare the selected code versions through SDK transitions when line changes are insufficient.

Report the affected scope with the relation path that caused inclusion. Do not report every reachable node.

## Source search fallback

Use targeted source search for:

- Exact identifiers and constants.
- Configuration or off-chain code that the graph does not cover.
- Confirmation of source evidence.
- Edits after the graph has selected scope.

Use broad source search only when the graph is unavailable, stale, incomplete, or unsupported. State the limitation.

## SDK graph selection

Use `Graph` or `AsyncGraph` for:

- Repeated or transitive traversal.
- Offline snapshots.
- Source reconstruction.
- Descendant and Merkle matching.
- Distance or call-chain queries.
- Code transitions across versions.
- Stable semantic locations for findings.

Do not build the full SDK graph for a one-file syntax check.
