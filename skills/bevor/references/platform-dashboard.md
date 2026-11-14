# Platform and Dashboard

Reviewed against app source b2525415 on 2026-11-14. Use the Dashboard for findings, source and graph evidence, lineage, and collaboration.

## Identity and links

Confirm workspace, project, analysis owner, analysis ID, and selected version. A deep link must set workspace/project context:

```text
https://app.bevor.io/project/users/USER_ID/analyses/ANALYSIS_ID?workspace=WORKSPACE_ID&project=PROJECT_ID
```

Add `&version=VERSION_ID` to preserve historical context. Public workflows pair this Dashboard with `https://api.bevor.io`. The owner ID belongs to the analysis user, not necessarily the currently authenticated user. Prefer a copied Dashboard URL when available.

## Review

1. Verify exact code and selected HEAD.
2. Inspect each finding's evidence, semantic node, severity, and recommendation.
3. Compare inherited findings and entrypoints with changed scope.
4. Verify purported remediations against source, especially after renames.
5. Review local proposed changes before writing them remotely.

CLI 0.2.1 writes findings immediately. Do not promise a staged review or commit button without verifying that the deployed UI supplies that workflow.

## Analytics

Prefer unique validated findings, accepted proofs, false-positive rates, reviewed scope, and remediation outcomes. Raw finding count alone is not a quality measure. Report time and cost only with a defensible baseline and matching experiment conditions.
