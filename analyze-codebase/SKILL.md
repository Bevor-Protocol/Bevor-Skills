---
name: analyze-codebase
description: Analyze a Solidity codebase for security vulnerabilities and produce structured, evidence-backed findings. Use for audits, vulnerability reviews, attack-path analysis, and security assessment. May use read-only Bevor graph commands for evidence, but never synchronizes code, creates or changes analyses, changes scopes, or submits findings.
---

# Analyze A Codebase

Own security reasoning and finding production. Do not own Bevor lifecycle operations.

## Invocation Modes

- When invoked alone, analyze directly and produce `security-findings.yaml` or the user-requested
  output without Bevor lifecycle actions.
- When invoked together with `operate-bevor`, act as the selected analyzer: consume the supplied
  scan instruction, scope manifest, materialized evidence, and optional prior findings; produce
  findings; then stop so `operate-bevor` can record them.
- Treat prior findings as leads that must be revalidated against the current code.
- Do not silently broaden a supplied scan scope.
- Immediately before a direct scan, print one concise line:
  `Security analyzer: analyze-codebase | mode: direct | scope: <requested scope>`.
- In Bevor-managed mode, let `operate-bevor` print the analyzer announcement; do not repeat it.

## Boundary

Allowed Bevor commands are read-only graph evidence operations:

```text
bevor nodes list|get|content|edges|call-chain
```

Use `operate-bevor` whenever setup, context inspection, synchronization, materialization, analysis
creation, scope mutation, finding import, or submission is needed.

Do not invoke:

```text
bevor init
bevor codes push
bevor analyses create|run|import|fork|commit
bevor scopes set|add|remove|clear
bevor findings add|bulk|edit|delete
bevor agent setup|materialize|submit
```

## Workflow

1. Determine the evidence source.
   - Prefer existing `.bevor/analyses/{analysis_id}/*.raw.md` bundles when provided.
   - Use read-only `bevor nodes` commands to expand incomplete graph evidence.
   - Read working-tree source only when the requested audit is not constrained to Bevor graph
     evidence.
2. Assign every scope bundle to at least one analysis pass.
3. Load only the relevant specialist prompts from `references/hacking-agents/`.
4. Validate candidate findings using `references/judging.md`.
5. Write per-scope intermediate findings using `references/findings-contract.md`.
6. Stop after producing findings. Let `operate-bevor` record or submit them.

## Graph Evidence Rules

- Use short node IDs of at least four characters.
- Expand context with `edges`, then `content`, then `call-chain` when needed.
- Follow outbound behavior and inbound edges on shared state.
- Ignore `defines` edges; container nodes add little security signal.
- Keep findings tied to the assigned scope unless a causal bridge is demonstrated.

When operating in graph-only mode, audited source may only come from:

```text
.bevor/analyses/{analysis_id}/*.raw.md
bevor nodes content <short-id>
```

Do not substitute working-tree source for missing graph evidence in graph-only mode.

## References

- Read `references/findings-contract.md` before writing findings.
- Read `references/judging.md` before finalizing findings.
- Read small, relevant slices from `references/hacking-agents/`.
- Use `references/attack-vectors/attack-vectors.md` only when a broad vector scan is warranted.
