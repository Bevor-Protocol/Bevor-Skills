# Graph-aware security review

Use this reference when the user asks for an audit, vulnerability review, threat model, exploit analysis, or remediation check.

Reviewed for the first skill release on 2026-09-02.

This is not the old graph-only audit process. The graph selects and explains scope. Source, tests, configuration, deployment facts, and security reasoning establish evidence.

## Start with preserved context

1. Resolve exact code identity.
2. Get existing findings, remediations, and validation decisions.
3. Identify inherited and new entrypoints.
4. Use graph relations to build the affected scope.
5. Run the cheapest useful deterministic checks.
6. Focus new reasoning on uncovered or changed risk.

Do not report an earlier validated finding as a new discovery. Do not suppress a distinct root cause because its title looks similar.

## Threat model

Identify:

- Assets and loss conditions.
- Trust boundaries and privileged roles.
- External actors and capabilities.
- Entrypoints and reachable state changes.
- External calls, integrations, and callback surfaces.
- Price, oracle, liquidity, timing, ordering, and governance assumptions.
- Upgrade, initialization, and lifecycle transitions.
- Invariants that protect funds, authorization, accounting, and solvency.

Tie each material claim to code, graph relations, configuration, tests, or deployment evidence.

## Validate a candidate finding

Try to refute the issue before reporting it:

1. Identify the exact vulnerable operation and location.
2. Trace a complete attacker-controlled path to it.
3. Check every guard, modifier, constraint, and state precondition.
4. Show that the required state can occur in the target environment.
5. Identify the affected asset and victim.
6. Explain the concrete effect and its bounds.
7. Reproduce with a test or proof of concept when proportionate.
8. Check existing and inherited findings for the same root cause.

Demote an unproven idea to a lead. Reject it when a specific control blocks the claimed path.

Do not use universal safe-pattern lists. Language versions, compiler behavior, tokens, integrations, and protocol assumptions can change the result.

## Finding quality

A reportable finding should contain:

- A short title based on the root cause.
- Severity with an explicit impact and likelihood basis.
- Exact affected code and semantic scope.
- Preconditions and attacker capabilities.
- A step-by-step exploit or failure path.
- Evidence and observed or reasoned impact.
- A concrete repair that preserves intended behavior.
- A regression test or verification method when practical.
- Source tool and discovery attribution.

Keep linter findings, style issues, gas micro-optimizations, and general centralization notes out of a vulnerability report unless they create a concrete security effect.

## Change review

Do not review only changed lines.

For each changed node, inspect callers, callees, shared state, modifiers, access controls, constraints, inheritance, overrides, and external calls. Follow transitive paths while they can affect an asset or invariant.

Compare earlier findings and remediations. State whether a change introduces, fixes, preserves, or reopens a risk.

## Completion

Report:

- Exact identity and reviewed scope.
- Existing, inherited, new, changed, and remediated findings.
- Confirmed findings and unverified leads separately.
- Important limitations and unreviewed surfaces.
- Reuse and supported savings.

Never state that no vulnerability exists only because the graph, Slither, or one model found nothing.
