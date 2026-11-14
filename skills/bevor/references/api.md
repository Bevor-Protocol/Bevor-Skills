# REST API and OpenAPI

Reviewed 2026-11-14. Use the API for non-Python clients or operations not exposed by the released CLI.

Use the current [API reference](https://www.bevor.io/docs/api-reference) and the selected deployment's OpenAPI. Verify the method, request body, authentication scope, and response type before coding. Historical staged-commit endpoints and old audit APIs are not a current contract.

## Authentication and scope

Use bearer authentication from a protected secret store. Keep credentials out of browser clients, source, logs, prompts, and command arguments. Production defaults to `https://api.bevor.io`; staging is `https://staging.api.bevor.io`.

Workspace/project navigation can require a user session, while API keys are project-scoped. Do not assume these credential types are interchangeable.

Distinguish workspace, project, code, analysis, version, node, and finding IDs. A Git SHA is source metadata, not a Bevor identifier.

## Writes and retry

Review a local finding batch before submission. Current finding operations change the selected analysis version immediately. Re-read remote state after a timeout before retrying create, upload, import, merge, or pipeline start.

Use bounded retries for reads and documented idempotent operations. Preserve pagination, request IDs, and error codes. Never resubmit accepted records blindly.

## Integration limits

Confirm whether the deployment supports a record-only external security run and a stable repeat key before implementing that workflow. Do not substitute a paid pipeline run for recording external results.
