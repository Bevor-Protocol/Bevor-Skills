# Bevor documentation map

Use `https://docs.bevor.io/llms.txt` as the live index. The links below were checked against that index on 2026-09-02.

Prefer `.md` pages when available. Load only the page needed for the task.

## Product and platform

- [Introduction](https://docs.bevor.io/getting-started/introduction.md)
- [How Bevor works](https://docs.bevor.io/features/overview.md)
- [Graph-native analysis](https://docs.bevor.io/features/graph-native-analysis.md)
- [Project analytics](https://docs.bevor.io/features/project-analytics.md)
- [Integrations](https://docs.bevor.io/getting-started/integrations.md)
- [Dashboard](https://docs.bevor.io/features/dashboard.md)
- [CI/CD](https://docs.bevor.io/features/cicd.md)
- [Bevor Skills](https://docs.bevor.io/features/bevor-skills.md)

## CLI

- [CLI overview](https://docs.bevor.io/cli-reference/overview.md)
- [Root commands](https://docs.bevor.io/cli-reference/root-commands.md)
- [Sessions](https://docs.bevor.io/cli-reference/sessions.md)
- [Team](https://docs.bevor.io/cli-reference/team.md)
- [Project](https://docs.bevor.io/cli-reference/project.md)
- [Code and graph](https://docs.bevor.io/cli-reference/code.md)
- [Analysis](https://docs.bevor.io/cli-reference/analysis.md)
- [Findings](https://docs.bevor.io/cli-reference/finding.md)
- [Agent shorthands](https://docs.bevor.io/cli-reference/agent.md)
- [Chat](https://docs.bevor.io/cli-reference/chat.md)

Use the installed CLI or matching release source for exact behavior. Public CLI pages can lag a release.

## Python SDK

- [SDK overview](https://docs.bevor.io/sdk-reference/python/overview.md)
- [Analyses](https://docs.bevor.io/sdk-reference/python/analyses.md)
- [Versions](https://docs.bevor.io/sdk-reference/python/versions.md)
- [Findings](https://docs.bevor.io/sdk-reference/python/findings.md)
- [Remediations](https://docs.bevor.io/sdk-reference/python/remediations.md)
- [Summary](https://docs.bevor.io/sdk-reference/python/summary.md)
- [Chats](https://docs.bevor.io/sdk-reference/python/chats.md)

Use the released `bevor-sdk` source for imports and typed methods. Do not copy preview package names from stale pages.

## API and OpenAPI

- [API overview](https://docs.bevor.io/api-reference/overview.md)
- [Concepts](https://docs.bevor.io/api-reference/concepts.md)
- [Error handling](https://docs.bevor.io/api-reference/error-handling.md)
- [Error codes](https://docs.bevor.io/api-reference/error-codes.md)
- [Business OpenAPI](https://docs.bevor.io/api-reference/business.json)
- [Graph OpenAPI](https://docs.bevor.io/api-reference/graph.json)
- [Security OpenAPI](https://docs.bevor.io/api-reference/security.json)

Useful endpoint pages include:

- [List code versions](https://docs.bevor.io/api-reference/graph/code/list-code-versions.md)
- [Get code version](https://docs.bevor.io/api-reference/graph/code/get-code-version.md)
- [List nodes](https://docs.bevor.io/api-reference/graph/graph/list-nodes.md)
- [List node edges](https://docs.bevor.io/api-reference/graph/graph/list-nodes-edges.md)
- [Get call chains](https://docs.bevor.io/api-reference/graph/graph/get-call-chains.md)
- [List analyses](https://docs.bevor.io/api-reference/security/analysis/list-analyses.md)
- [Get recent analysis](https://docs.bevor.io/api-reference/security/analysis/get-most-recent-analysis.md)
- [Get version entrypoints](https://docs.bevor.io/api-reference/security/analysis-version/get-version-entrypoints.md)
- [Get version findings](https://docs.bevor.io/api-reference/security/analysis-version/get-version-findings.md)
- [Get staged difference](https://docs.bevor.io/api-reference/security/analysis-version/get-staged-diff.md)
- [Get version difference](https://docs.bevor.io/api-reference/security/analysis-version/get-version-diff.md)
- [Commit staged changes](https://docs.bevor.io/api-reference/security/analysis-version/commit-staged-changes.md)
- [List findings](https://docs.bevor.io/api-reference/security/finding/list-findings.md)
- [Add findings](https://docs.bevor.io/api-reference/security/finding/add-findings.md)
- [List remediations](https://docs.bevor.io/api-reference/security/remediation/list-remediations.md)

## Builders and auditors

- [Creating agents and tools](https://docs.bevor.io/developers/custom-agents.md)
- [Protocol integrations](https://docs.bevor.io/developers/protocol-integration.md)
- [Auditor overview](https://docs.bevor.io/auditors/overview.md)
- [Improving audit process](https://docs.bevor.io/auditors/improving-process.md)
- [Privacy for NDA clients](https://docs.bevor.io/auditors/privacy-for-nda-clients.md)
- [Audit competitions](https://docs.bevor.io/auditors/win-more-audit-competitions.md)

## Known documentation gaps

Until corrected, watch for:

- Preview warnings that conflict with released CLI and SDK packages.
- Old `/v1/audits` examples.
- Old package names and imports.
- A CI page that does not yet explain record-only and SARIF-import modes.
- Missing Bevor Action compatibility and retry guidance.
- Missing external-run and tool-attribution contracts.
- Dashboard labels that differ from the deployed application.
- Domain claims that do not separate released Solidity graph support from planned Rust graphs.

Report a mismatch. Do not silently combine incompatible examples.
