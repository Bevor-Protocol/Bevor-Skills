# Shared Scan Rules

## Reading

Your bundle has two sections:

1. **Core source** (inline) — structured as per-function chunks separated by `---`. Each chunk:
   - Header: `### path :: Contract.function`
   - Fenced `solidity` block with the function source
   - `**Call chain:**` — pre-traced call graph with `calls`, `reads`, `writes`, `emits`, `throws` annotations
   - `Static Analysis:` — fully-qualified signatures of every function in the chain

   Read in parallel chunks (offset + limit); compute offsets from the line count in your prompt.

2. **Agent instructions** — your specialty rules follow the source.

The call chain is pre-built: do not re-trace what is already annotated. Use `writes` to identify state mutation, `throws` to identify guards, and the call graph to identify entry-to-impact paths directly.

When matching function names, check both `functionName` and `_functionName` (Solidity convention).

## Cross-contract patterns

When you find a bug in one contract, **weaponize that pattern across every other contract in the bundle.** Search by function name AND by code pattern. Finding native/ERC20 confusion in `ContractA.onRevert` means you check every other contract's `onRevert` — missing a repeat instance is an audit failure.

After scanning: escalate every finding to its worst exploitable variant (DoS may hide fund theft). Then revisit every function where you found something and attack the other branches.

## Do not report

Admin-only functions doing admin things. Standard DeFi tradeoffs (MEV, rounding dust, first-depositor with MINIMUM_LIQUIDITY). Self-harm-only bugs. "Admin can rug" without a concrete mechanism.

## Output

Return structured blocks only — no preamble, no narration. Exception: vector scan agent outputs its classification block first.

FINDINGs have concrete, unguarded, exploitable attack paths. LEADs have real code smells with partial paths — default to LEAD over dropping.

**Every FINDING must have a `proof:` field** — concrete values, traces, or state sequences from the actual code. No proof = LEAD, no exceptions.

**One vulnerability per item.** Same root cause = one item. Different fixes needed = separate items.

```
FINDING | contract: Name | function: func | bug_class: kebab-tag | group_key: Contract | function | bug-class
path: caller → function → state change → impact
proof: concrete values/trace demonstrating the bug
description: one sentence
fix: one-sentence suggestion

LEAD | contract: Name | function: func | bug_class: kebab-tag | group_key: Contract | function | bug-class
code_smells: what you found
description: one sentence explaining trail and what remains unverified
```

The `group_key` enables deduplication: `ContractName | functionName | bug_class`. Agents may add custom fields.
