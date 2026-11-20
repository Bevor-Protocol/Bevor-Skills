# New commits

When the code changes after an earlier review (new commits, a branch switch, edits), add it to the same analysis instead of starting over. Findings and coverage carry forward for the code that didn't change.

1. `bevor sync --yes` adds the working directory as a new version and moves HEAD to it.
2. `bevor analyses coverage --tool TOOL_NAME --no-covered --json` now lists the entrypoints that reach new or changed code, since their coverage didn't carry over. Review those as usual ([review](../SKILL.md#review)).
3. `bevor analyses diffs --json` shows how findings changed from the previous version to HEAD: added, removed, or modified. It's about findings, not code.
4. Recheck carried-over findings in the code you reviewed against the new source.

If `sync` can't add a version, it says why. Report that to the user instead of starting a separate analysis.

Tell the user what carried over and what you reviewed again.
