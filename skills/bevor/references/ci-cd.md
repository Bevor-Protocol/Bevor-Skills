# Security CI integration

Reviewed for CLI 0.2.1 on 2026-11-14. Preserve the repository's existing tools, build, producer, and gate.

## Modes

- **Record:** retain exact source, tool configuration, result identity, and duration. Confirm an external-run endpoint exists before promising server-side recording.
- **Import:** upload an approved, deduplicated finding batch onto the exact analysis version.
- **Analyze:** run Bevor's metered pipeline only when requested.

## Capture, review, import, then gate

1. Check out the exact source revision.
2. Run the existing tool and retain its SARIF even when the tool reports findings.
3. Validate the artifact, exact code fingerprint, destination, and previous attempt.
4. Review locally unless an approved routine-write policy covers this producer and destination.
5. Record the run and import findings with the verified interface.
6. Enforce the repository's security gate.
7. Report accepted records and the Dashboard link.

CLI 0.2.1 imports write immediately. A stage-only policy must keep an artifact locally for review; it cannot import and rely on a later CLI commit. Do not invent a commit operation.

## Retry and identity

Retain repository, Git SHA, code fingerprint, analysis/version IDs, tool/version/config digest, workflow/run/attempt, artifact digest, and timing. Derive a repeat key from these inputs. The server does not promise to enforce it, so check prior accepted results before retrying.

## Authentication

CLI login is a user-session workflow. Public SDK API keys are project-scoped and suit noninteractive CI; use a verified SDK import adapter for that credential. Do not assume setting an API-key variable authenticates the CLI.

Use GitHub secrets, minimum permissions, and pinned third-party actions. Do not expose credentials to untrusted fork pull requests or combine untrusted checkout with privileged pull_request_target. Capture/import must precede the gate and should run after a producer's finding exit code, but not after cancellation.

## Verification

Parse and lint the workflow, test malformed/partial input and repeat attempts with an isolated fixture, and confirm all resource IDs and source filters. Live CI may create remote data or cost money, so run only within the user's authorized scope.
