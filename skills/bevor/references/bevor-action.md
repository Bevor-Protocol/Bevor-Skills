# Bevor GitHub Action

Use this reference before adding or updating the Bevor Action.

Reviewed local repository: `Bevor-Action` commit `22925966a59c445d9050c002ed4938b4e0db4405`, 2026-09-02.

## Current behavior

The current Action:

1. Packages the target directory.
2. Uploads it as a new code version.
3. Creates and runs Bevor AI analysis.
4. Polls for completion.
5. Fetches findings.
6. Optionally comments on a pull request.
7. Optionally fails on a severity threshold.

It is not a general record or import Action.

## Current blockers

Do not recommend the current Action as the default until these issues are fixed:

- It has no record-only mode.
- It cannot import SARIF from an earlier CI step.
- It uploads source on every run instead of reusing an exact fingerprint.
- It uses vendored `bevor_graph_sdk` and `bevor_security_sdk` preview packages.
- Its Dashboard link is hard-coded to the staging application.
- Its `diff` mode matches changed file paths, not semantic blast radius.
- It can fall back from `diff` to full analysis.
- It does not use a stable retry key.
- It does not output code or analysis-version IDs.
- Its README omits the `scope_mode` input.
- The documented owner and `@v1` release do not match the inspected local repository state.
- The repository has no visible automated test suite for these flows.

Until these blockers are resolved, use the current SDK or deployed API for custom record and import jobs. Use the Action only when the user explicitly wants its current managed-analysis behavior and accepts the limitations.

## Required replacement interface

The updated Action must have explicit modes:

- `record`: store external tool-run identity against an exact code version.
- `import`: record a run and import one SARIF path or narrow file pattern.
- `analyze`: run Bevor-managed analysis.

It must:

- Use current `bevor-sdk` models and resources.
- Compute a source fingerprint before upload.
- Reuse an exact code version and result artifact.
- Keep capture and import separate from gate enforcement.
- Accept tool name, version, configuration digest, scope, and status.
- Record GitHub workflow, job, run, attempt, event, and commit identity.
- Use a stable repeat key.
- Report input, invalid, duplicate, combined, new, staged, and committed counts.
- Output code, analysis, analysis-version, and Dashboard identifiers.
- Use the selected environment for API and Dashboard links.
- Name changed-file scope accurately. Do not call it semantic impact.
- Document permissions, secrets, forks, retries, and commit policy.

## Release requirements

Before the skill recommends the Action:

1. Resolve the public repository owner, action name, and release tag.
2. Publish a compatibility table for Action, CLI, SDK, and API versions.
3. Add unit tests for inputs, repeat keys, filters, and summaries.
4. Add integration tests for record, SARIF import, and analysis modes.
5. Add retry and duplicate fixtures.
6. Add fork tests that prove secrets are unavailable.
7. Add a SARIF-before-gate test.
8. Remove the old vendored clients and staging URL.

Do not fabricate an Action version or mode that is not released.
