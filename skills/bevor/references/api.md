# REST API and OpenAPI

Use the raw API for non-Python services, generated clients, small HTTP integrations, or an endpoint that SDK 0.1.x does not expose.

Compatibility basis: API and SDK source commit `591421f2963f6095d33521ff57ca3d60759333e3`, reviewed 2026-09-02.

## Source selection

1. Compare the deployed OpenAPI description with the intended environment.
2. Prefer the split current specifications:
   - `https://docs.bevor.io/api-reference/business.json`
   - `https://docs.bevor.io/api-reference/graph.json`
   - `https://docs.bevor.io/api-reference/security.json`
3. Use `https://api.bevor.io` as the production base URL unless the user selects another environment.
4. Treat older `/v1/audits` examples as obsolete.

The public narrative pages can contain preview warnings that differ from the deployed API and released SDK. For exact endpoints, use the matching OpenAPI or release source.

## Authentication

Use:

```http
Authorization: Bearer BEVOR_API_KEY
```

Read the credential from a secret store or environment variable. Do not place it in source, client-side code, logs, prompts, or examples with a real value.

Uploads and streams can use single-use keys returned by an authenticated API operation. Do not replace them with the bearer token in a URL.

## Resource identity

Keep these identifiers separate:

- Team ID: access and ownership boundary.
- Project ID: container for code and security history.
- Code ID: one Bevor code version with a source fingerprint.
- Analysis ID: one analysis lineage or container.
- Analysis-version ID: one point in that lineage.
- Analysis HEAD: the selected current version of an analysis.
- Node ID: semantic code location within a code version.
- Finding ID: one finding identity across its history.

A Git commit SHA is metadata for source identity. It is not a Bevor ID.

## API areas

| Area | Main resources |
| --- | --- |
| Business | Projects and team activity. Some team operations require a session rather than API key. |
| Graph | Code versions, uploads, files, nodes, edges, call chains, transitions, and code chats. |
| Security | Analyses, analysis versions, entrypoints, findings, diffs, commits, retries, remediations, summaries, and analysis chats. |
| Chat | Synchronous responses and streamed sessions tied to code or analysis versions. |

Use the endpoint descriptions in [docs-map.md](docs-map.md) instead of guessing paths or request bodies.

## Pages and streams

Paginated responses contain a result page and page metadata. Preserve server page size and ordering semantics from OpenAPI.

For event streams:

- Use the stream-token endpoint first.
- Reconnect only when the endpoint documents safe resumption.
- Inspect final resource state after an interrupted stream.
- Do not repeat the operation only because the client missed the final event.

## Errors and retries

Expected structured errors use:

```json
{
  "message": "Human-readable description",
  "code": "error.code"
}
```

Capture the response request ID for support and diagnostics. Never include a credential in a support bundle.

Retry reads and documented idempotent operations with bounded exponential backoff. Before retrying a create, upload, analysis start, import, or commit:

1. Inspect the target resource.
2. Check whether the first request succeeded.
3. Use an idempotency or repeat key when the endpoint supports it.
4. Do not resubmit accepted findings.

Do not assume a generic HTTP status is safe to retry. Use the endpoint contract and structured error code.

## Staged findings

Adding, editing, or deleting findings changes the staged view of an analysis version. It does not complete the version commit.

The safe sequence is:

1. Resolve an exact code and analysis version.
2. Read committed and staged findings.
3. Deduplicate.
4. Submit one staged change set.
5. Read the staged diff.
6. Show it to the user.
7. Get commit approval.
8. Commit once.

## Current integration gap

The pinned public contract does not clearly define a record-only external security run with a stable CI repeat key. Do not fake this by starting Bevor-managed analysis.

For a CI implementation, confirm the deployed contract first. If the operation is absent, implement or document the API and SDK contract before promising record-only mode.
