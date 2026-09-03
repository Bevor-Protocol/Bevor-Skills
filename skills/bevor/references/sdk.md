# Python SDK

Use the SDK for repeated Python operations, services, analyzers, graph traversal, typed models, pagination, or event streams.

Compatibility: package `bevor-sdk 0.1.0`, Python 3.13+, source commit `591421f2963f6095d33521ff57ca3d60759333e3`, reviewed 2026-09-02.

Do not use the old `bevor_security_sdk.SecurityClient` or `bevor_graph_sdk` preview packages.

## Imports and clients

```python
from bevor_sdk import AsyncBevorClient, AsyncGraph, BevorClient, Graph
```

Use the synchronous client in ordinary scripts:

```python
from bevor_sdk import BevorClient

with BevorClient(api_key) as client:
    code = client.codes.get(code_id)
    findings = client.findings.list({"code_id": code_id}).results
```

Use the asynchronous client inside an existing asynchronous application:

```python
from bevor_sdk import AsyncBevorClient

async with AsyncBevorClient(api_key) as client:
    code = await client.codes.get(code_id)
```

Do not wrap `AsyncBevorClient` in an improvised event loop. Reuse one client so it reuses its HTTP transport.

The default base URL is `https://api.bevor.io`. Pass `base_url` only for an explicitly selected environment.

## Resource map

The client exposes:

- `teams`: get, members, invites, and all teams.
- `projects`: get, list, create, and all projects.
- `codes`: list, get, transitions, edges, update, retry, upload, scan, paste, repository, files, nodes, and code chats.
- `analyses`: create, list, get, recent, update, delete, versions, remediations, and summaries.
- `findings`: list, add, get, edit, delete, revert, acknowledgement, comments.
- `chats`: create, list, get, messages, synchronous reply, and stream.

Prefer a bound resource for repeated work on one record:

```python
version = client.analyses.versions(version_id)
entrypoints = version.entrypoints()
findings = version.findings()
staged = version.diff_staged()
```

## Pagination and streams

List methods return `PaginatedResource` where the endpoint is paginated.

```python
page = client.analyses.list({"project_id": project_id})
items = list(page.results)
while page.has_more():
    page.fetch_next()
    items.extend(page.results)
```

Use the SDK event resource for analysis or chat streams. Do not build a custom SSE parser unless the SDK lacks the needed event.

## Graph

Build one graph per exact code ID:

```python
from bevor_sdk import Graph

graph = Graph(client, code_id)
graph.build()

for node in graph.get_all_nodes():
    if node.is_entrypoint:
        source = graph.reconstruct_chunk(node.id, with_docstring=True)
```

Useful graph methods include:

- `get_node`, `get_all_nodes`, `get_all_files`, and `get_nodes_in_file`.
- `get_edges` and `get_edges_for_node`.
- `get_call_chain`.
- `reconstruct_chunk` and lazy file-content retrieval.
- `get_distance` and `is_descendant`.
- Short-ID and full-ID conversion.
- Merkle descendant matching.
- `from_snapshot` for an already loaded snapshot.

The current graph's language-specific callable and declaration helpers are implemented for Solidity. Check the graph language before using them.

Use `client.codes.transitions(...)` to relate code versions. Use transitions for changed, matched, and removed semantic nodes.

## Finding conversion and fingerprints

Use the bundled helpers:

```python
from bevor_sdk.helpers.converters.sarif import bevor_to_sarif_sync, sarif_to_bevor
from bevor_sdk.helpers.source_fingerprint import folder_version_fingerprint
```

Fingerprint local source before upload. Search for an existing exact code version before creating another.

Use `sarif_to_bevor` at the result boundary, then perform semantic duplicate control before `client.findings.add(version_id, findings)`.

## Security pipeline choice

Use Bevor's security pipeline for hosted analysis, inherited scope, retries, remediations, graph-linked findings, and Dashboard work.

Use graph resources without the pipeline when another tool performs the analysis. Create or reuse exact code identity, record the external work where the API supports it, and import results later.

Before a mutating call, apply the same approval rules as the CLI. In particular:

- Upload needs transfer approval.
- `versions.run()` can start metered work.
- `findings.add()` stages remote changes.
- `versions.commit()` commits them.
- Delete, merge, set-head, and acknowledgement calls are sensitive.

## CLI as an example

The released CLI source is the most complete example of SDK use. Match the CLI and SDK release before copying a pattern.

Key source locations in the Bevor API repository are:

- `packages/cli/bevor_cli/client.py`
- `packages/cli/bevor_cli/commands/`
- `packages/bevor-sdk/bevor_sdk/_sync/resources/`
- `packages/bevor-sdk/bevor_sdk/_async/resources/`
