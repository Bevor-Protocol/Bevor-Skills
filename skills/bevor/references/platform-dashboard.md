# Platform and Dashboard

Use the Dashboard for interactive review, team decisions, graph exploration, and project-level trends.

Behavior basis: web application commit `a1ba17fe7aa769fb6f163b79d84a4343f9956cdd`, reviewed 2026-09-02. Public product guidance can change independently.

## Choose the Dashboard for

- Reviewing findings by severity and staged state.
- Reading evidence, recommendation, references, and related code.
- Moving between the finding list and entrypoint scope views.
- Viewing findings on source files and graph nodes.
- Comparing the full graph with the reanalysis view.
- Distinguishing inherited and reanalyzed scopes.
- Reviewing borrowed findings and remediation history.
- Adding, editing, reverting, or staging deletion of a finding.
- Collaborating through finding comments and analysis chats.
- Reviewing project finding history, network breakdown, and user activity.

Use the CLI, SDK, or API for automation and bulk operations.

## Review procedure

1. Confirm the team, project, code version, analysis, and selected HEAD.
2. Start with staged changes if a submission awaits review.
3. Filter by severity and status.
4. Open a finding and inspect its code or graph location.
5. Check the related entrypoint and relation path.
6. Compare inherited and reanalyzed scope.
7. Read comments, validation state, and remediation history.
8. Reject duplicates or attach stronger evidence to the existing identity.
9. Commit only after the staged difference is understood and approved.

The UI can stage a finding addition, edit, or deletion. Staging is not a commit.

Acknowledgement changes validation state. Confirm the current value and intended new value before changing it.

## Graph view

The application marks findings and analysis entrypoints on the graph. The reanalysis view focuses on nodes reachable from reanalyzed entrypoints.

Use it to understand scope and navigate evidence. Do not infer that every reachable node is vulnerable or that a dimmed node is safe.

## Project analytics

Use project analytics to compare history, not to reward output volume.

When attribution data exists, prefer:

- Unique validated findings.
- Duplicate and false-positive rates.
- Validated proofs of concept.
- Time and cost per unique validated finding.
- Remediation outcomes.
- Tool performance on similar code and vulnerability classes.

Raw finding count alone is not a quality measure.

## Source differences

If the public docs describe the Dashboard as coming soon but the application is available, state the environment and source date. Use the live application for exact UI behavior and current public docs for product guidance.
