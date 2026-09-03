# CI/CD integration

Use this reference when a web3 repository has a security job or the user asks to add one.

Reviewed against the Bevor API, SDK, CLI, and Action source available on 2026-09-02.

The primary goal is to preserve each security run and its exact code version. Bevor-managed analysis is optional.

## Inspect before editing

Inspect:

- `.github/workflows/` and other CI configuration.
- Build, compiler, dependency, and cache setup.
- Existing security tools and their versions.
- SARIF, JSON, XML, and report artifacts.
- Existing pass/fail policy and branch protection.
- Fork behavior and secret availability.

Keep the repository's triggers, build matrix, cache, compiler setup, tool behavior, and reporting unless the user asks to change them.

If any web3 security job exists, offer to record its run in Bevor. If it emits SARIF, prefer finding import.

## Choose a mode

| Mode | Use when | Required result |
| --- | --- | --- |
| Record | The existing tool has no structured findings or only run metadata is wanted. | Exact code identity, external-run identity, tool metadata, duration, and status. |
| Import | The existing tool emits SARIF or another supported result. | Record data plus normalized and deduplicated staged findings. |
| Analyze | The user wants the Bevor security pipeline in CI. | Code upload or reuse, analysis run, findings, policy result, and links. |

Do not replace an existing job with Bevor analysis. Add the smallest useful integration.

The pinned API does not yet document a record-only external-run operation. Verify the deployed API before implementing `record`. If absent, report the product gap. Do not fake a record by starting paid analysis.

## Required run identity

Record these values when available:

- Repository owner and name.
- Commit SHA and Bevor source fingerprint.
- Branch, tag, pull request, base SHA, and head SHA.
- CI provider, workflow, job, run ID, run attempt, and event.
- Tool name, tool version, configuration digest, and target path.
- Start time, duration, exit status, and gate status.
- Result format, artifact digest, and SARIF path.
- Bevor team, project, code, analysis, and analysis-version IDs.

Use a repeat key from repository, commit, workflow, job, tool, configuration digest, and artifact digest. A retry must not create another code version, run record, or finding set.

## Capture, import, then gate

Order a finding-producing job this way:

1. Check out the exact source revision.
2. Install a pinned compiler and security tool.
3. Run the tool without ending the job before its result file exists.
4. Validate and retain the result artifact.
5. Resolve or reuse the exact Bevor code version.
6. Record the run and import findings.
7. Deduplicate against staged, committed, and inherited findings.
8. Apply the approved `stage-only` or `auto-commit` policy.
9. Enforce the repository's security gate.
10. Publish a concise CI summary and Bevor link.

The import step must use `if: always() && !cancelled()` or an equivalent condition when the producer can return a finding exit code. Do not run it after cancellation.

## Slither Action capture pattern

Verify the current Slither Action release and pinning policy before use. This example shows ordering, not a Bevor import endpoint:

```yaml
permissions:
  contents: read

steps:
  - uses: actions/checkout@<approved-pin>

  - name: Run Slither and retain SARIF
    id: slither
    uses: crytic/slither-action@<approved-pin>
    with:
      sarif: results/slither.sarif
      fail-on: none

  - name: Record Slither result in Bevor
    if: ${{ always() && !cancelled() && hashFiles('results/slither.sarif') != '' }}
    env:
      BEVOR_API_KEY: ${{ secrets.BEVOR_API_KEY }}
      BEVOR_PROJECT_ID: ${{ vars.BEVOR_PROJECT_ID }}
      BEVOR_SARIF: results/slither.sarif
    run: <verified SDK or API import command for the deployed Bevor contract>

  - name: Enforce Slither gate
    if: ${{ always() && !cancelled() }}
    run: <repository-approved gate over results/slither.sarif>
```

Never leave the placeholder commands in a committed workflow. Implement them only after verifying the deployed Bevor import and gate interface.

If direct Slither is already installed, preserve that command and add its SARIF option. Do not replace it with the Action only for style.

## GitHub Actions safety

- Use GitHub secrets for `BEVOR_API_KEY`.
- Prefer repository or environment variables for non-secret IDs.
- Use minimum permissions. Add `pull-requests: write` only when a comment is requested.
- Do not pass Bevor secrets to untrusted fork pull requests.
- Avoid `pull_request_target` with untrusted checkout and secrets.
- Pin third-party actions to the repository's required form, preferably a full commit SHA.
- Do not print request headers or secrets in debug output.

Show the user the uploaded data, destination, trigger, and retention behavior before enabling the workflow.

## Finding commit policy

Use `stage-only` by default. The workflow imports findings, shows counts, and leaves review and commit to a person.

An approved `auto-commit` policy must state:

- Allowed producer tools and versions.
- Repository, event, branch, and target paths.
- Destination team and project.
- Severity and validation requirements.
- Duplicate and partial-failure behavior.
- Who owns rollback and acknowledgement decisions.

## Verification after an edit

1. Parse the workflow YAML.
2. Run the repository's workflow linter if available.
3. Confirm all referenced step IDs and result paths.
4. Confirm the result step runs before the gate.
5. Confirm fork jobs do not receive a Bevor secret.
6. Confirm a retry uses the same repeat key.
7. Do not trigger a live CI run without approval.

## Result summary

```text
Bevor CI
- Identity: <repository/commit/code/analysis>, match=<exact|related|stale|unknown>
- Run: <provider/workflow/job/run/attempt>, mode=<record|import|analyze>
- Tools: <name/version/config>, gate=<pass|fail|not-applied>
- Findings: <input/new/combined/duplicate/validated>, staged=<count>, committed=<count>
- Reuse: <code reused/findings inherited/scopes skipped>
- Cost: <measured tokens/time/money or unavailable>
- Links: <CI run/Bevor analysis>
- Limits: <missing data, unsupported mode, or assumptions>
```
