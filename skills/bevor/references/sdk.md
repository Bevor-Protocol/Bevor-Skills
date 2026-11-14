# Python SDK

Reviewed against SDK 0.2.1 on 2026-11-14. Use the SDK for repeated traversal, typed data, pagination, and batches.

```python
from bevor_sdk import AsyncBevorClient, AsyncGraph, BevorClient, Graph

with BevorClient(api_key, base_url=api_url) as client:
    code = client.codes.get(code_id)
    analysis = client.analyses.get(analysis_id)
```

Use a protected API key scoped to the intended project. Do not extract a browser or CLI credential into prompts or command arguments. The CLI uses its own authenticated user context for workspace/project selection.

Use the synchronous client for scripts and the asynchronous client inside an async application. Reuse one client and its transport.

Current resources include `projects`, `codes`, `analyses`, `analysis_versions`, `findings`, `transitions`, `summary`, and `chats`. Inspect installed types for exact signatures. Old team resources, nested analysis-version resources, and staged-commit examples do not describe this release.

## Graph and identity

Build one Graph per exact code ID only when repeated traversal justifies it. For a few queries, use the CLI. Retrieve selected nodes, relations, and source chunks rather than dumping the graph.

Use helpers from `bevor_sdk.helpers.source_fingerprint` to compare source before upload. The CLI is a maintained usage example in `packages/cli/bevor_cli/commands/`; SDK source lives under `packages/sdk-python/bevor_sdk/`.

## Findings

The released SARIF converter is `bevor_sdk.helpers.sarif.sarif_to_bevor`. Review severity mapping and deduplicate before import. Use typed request bodies from `bevor_sdk.types.requests`.

Adding findings to an analysis version is an immediate remote write. Review the local batch first. Consult [finding exchange](findings-exchange.md) for its exact shape.

Uploads, metered pipeline runs, merges, deletions, HEAD moves, and acknowledgement changes retain the same user-intent boundaries as the CLI.
