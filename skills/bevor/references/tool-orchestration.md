# Security-tool orchestration and attribution

Use this reference when choosing, ordering, comparing, or combining security tools.

Reviewed against the Bevor product workflow and finding model on 2026-09-02.

“Throw everything at the problem” means that diverse tools, agents, models, and people can contribute to one history. It does not mean blind repeated runs.

## Default cheap-first order

For Solidity, use Slither as the default first security tool unless the target or user requires another baseline.

1. Resolve the exact code version and earlier findings.
2. Run a pinned build and Slither configuration.
3. Produce and retain SARIF before applying the security gate.
4. Import the SARIF into the matching Bevor record.
5. Deduplicate and match earlier findings.
6. Apply the approved Slither gate.
7. If the gate fails, stop expensive AI stages by default and triage or repair the baseline findings.
8. If it passes, give later tools the affected graph scope and known-finding brief.
9. Ask later tools to seek risks beyond known Slither results.
10. Record each result with source, duration, code identity, and available cost data.

Slither findings are the first duplicate anchors for that code version. A later tool does not get discovery credit for the same root cause.

A later tool can improve the existing finding with stronger evidence, a proof of concept, a wider attack path, or a supported severity correction.

A passing static-analysis gate does not establish security. Use heavyweight tools and people for business logic, economic risk, cross-contract behavior, and unexplained graph paths.

## Attribution stages

Preserve these roles separately:

- Discovery: first source that reports the unique root cause.
- Corroboration: independent source that matches it.
- Proof: source that supplies executable or repeatable exploit evidence.
- Validation: independent accepted decision that the issue and proof are valid.
- Remediation: source or person that repairs or verifies the repair.

A validated proof of concept is repeatable evidence accepted by an independent check. A tool's own claim is not independent validation.

## Compare useful performance

Do not rank tools by raw finding count. Duplicates and false positives must not improve rank.

Use these measures when data exists:

- Unique findings discovered.
- Unique findings with validated proofs of concept.
- False-positive and duplicate rates.
- Severity and affected-asset distribution.
- New affected scope examined.
- Time to first useful finding.
- Duration, input tokens, compute, and monetary cost.
- Cost and time per unique validated finding.
- Failure and incomplete-run rates.

Compare tools only on similar code, scope, vulnerability classes, and review conditions. Show sample size and missing data.

Use prior performance to choose tools for similar work. Do not turn one global score into a universal ranking.

Keep enough tool diversity to cover different failure classes. A run with no findings is not proof of safety.

## Downstream prompt contract

Give a later tool:

```text
Target: <exact code ID and fingerprint>
New scope: <nodes and relation paths that still need work>
Known findings: <IDs, root causes, locations, validation state>
Static baseline: <tool/version/config/result>
Do not rediscover: <matched root causes>
Focus on: <logic, economics, cross-contract effects, or unexplained paths>
Return: <SARIF or normalized findings with source and evidence>
```

Keep the brief small. Link or retain detailed evidence outside the active model context.
