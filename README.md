[![Bevor — Harness your smart contract security](https://bevor.io/images/og.png)](https://bevor.io)

# Bevor Skills

Give your coding agent the code graph, findings, and review history behind your next security decision.

[![Validate skill](https://github.com/Bevor-Protocol/Bevor-Skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Bevor-Protocol/Bevor-Skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-5865F2)](https://agentskills.io)

[![Website](assets/badges/link-website.svg)](https://bevor.io) [![Docs](assets/badges/link-docs.svg)](https://bevor.io/docs) [![Dashboard](assets/badges/link-dashboard.svg)](https://app.bevor.io) [![Join the waitlist](assets/badges/link-waitlist.svg)](https://www.bevor.io/waitlist) [![X](assets/badges/link-x.svg)](https://x.com/Bevor_io) [![LinkedIn](assets/badges/link-linkedin.svg)](https://www.linkedin.com/company/bevor/)

Bevor connects security work to exact source versions. This skill helps agents navigate semantic code graphs, reuse earlier findings, review changes, and save results with their evidence and analysis history.

[![Claude Code](assets/badges/claude-code.svg)](https://code.claude.com/) [![Cursor](assets/badges/cursor.svg)](https://cursor.com) [![Codex](assets/badges/codex.svg)](https://openai.com/codex/)

These clients can load the shared [Agent Skills format](https://agentskills.io).

## Supported smart contract languages

| Language / framework | Support |
| --- | --- |
| Solidity | Supported |
| Anchor Rust | Supported |
| GenLayer Intelligent Python Contracts | Supported |
| Soroban Rust | Experimental |

We'd love to hear from developers and security researchers working with other major smart contract languages. [Request language support in GitHub issues](https://github.com/Bevor-Protocol/Bevor-Skills/issues/new) or tell us what you need through the [Bevor waitlist](https://www.bevor.io/waitlist) so we can prioritize accordingly. Include the language or framework and the development or security workflow you'd like Bevor to support.

## Install, run, and update

### Ask your agent

**Install and start a review**

```text
Install the Bevor skill from https://github.com/Bevor-Protocol/Bevor-Skills
and use it to audit this repository. Reuse existing Bevor project context
where available, and link the resulting analysis in the dashboard.
```

**Continue an existing review**

```text
Use Bevor to review the security impact of this branch. Create a child
version of the current analysis, verify inherited findings against the
new source, and audit the changed scope.
```

**Update the skill**

```text
Update the Bevor skill to the latest version from
https://github.com/Bevor-Protocol/Bevor-Skills using its installation method.
Check the CLI version separately and report any compatibility mismatch.
```

The skill can also activate automatically for compatible security tasks. Explicitly naming Bevor makes your intended workflow clear.

### Install from your terminal

**CLI and skill on macOS/Linux:** the official installer installs or updates the CLI globally for your user through `uv`, without `sudo`, and copies the skill into personal skill directories for the compatible clients listed above.

```bash
curl -LsSf https://bevor.io/install.sh | sh
```

Open a new shell if `bevor` is not on your PATH after installation.

**Skill only:** if you already have the CLI, use the [skills CLI](https://github.com/vercel-labs/skills). This route requires Node.js 22.20+ and npm.

```bash
# Install for this project; select your coding agent when prompted.
npx skills add Bevor-Protocol/Bevor-Skills --skill bevor

# Or install for your user across projects.
npx skills add Bevor-Protocol/Bevor-Skills --skill bevor -g
```

Restart your coding agent after installation. For a manual install, copy the complete [`skills/bevor/`](skills/bevor/) directory into your client's skill directory, preserving its references. See the skills CLI's [client directory reference](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

### Connect your account

Remote operations need an authenticated Bevor account. Open the [dashboard](https://app.bevor.io), or [join the waitlist](https://www.bevor.io/waitlist) if you need access.

Check your CLI and account:

```bash
bevor --version
bevor whoami --json
```

If authentication is missing or expired, run `bevor login` and complete browser authorization. Then run `bevor status --json` from the target repository.

### Keep the CLI and skill current

```bash
# Update the CLI package.
bevor upgrade

# Check and update a skill installed through the skills CLI.
npx skills check
npx skills update bevor
```

`bevor upgrade` updates the CLI, not skill files. Rerun the official installer to refresh installer-managed copies of both. For manual skill installations, replace the skill directory from the reviewed repository revision.

## One skill, connected workflows

| Workflow | What the skill helps your agent do |
| --- | --- |
| Security review | Establish exact code identity, inspect relevant execution paths, and attach findings to semantic locations. |
| Review across versions | Create child analysis versions, inspect carryover, and check what needs another review. |
| Findings | Deduplicate and batch new findings through YAML, Bevor JSON, or analyzer SARIF, attributed to the tool that found them. |
| Graph investigation | Follow calls, state access, inheritance, and related code to investigate a security question. |
| Team review | Keep findings, evidence, and analysis history available in the Bevor dashboard. |

The entry point is [`bevor`](skills/bevor/SKILL.md). It loads the focused references needed for each task.

## Example requests

```text
Review findings.yaml and import the new findings as one batch into the selected analysis.

Import this Slither SARIF, check for duplicates, and verify the stored findings.

Use the Bevor graph to investigate which entrypoints can reach this state write.
```

## How reviews stay grounded

1. **Match the source.** Check workspace, project, code fingerprint, processing status, analysis, and version before reusing context.
2. **Investigate the relevant scope.** Query the graph and confirm security behavior in source. Reachability alone does not establish a vulnerability.
3. **Review inherited findings.** Carryover informs the next review. An automatic remediation label still needs verification against the changed code.
4. **Save a reviewed batch.** Preserve finding identity, avoid duplicates, and read back accepted results before reporting completion.

Finding writes apply as soon as they run, so the skill reviews the batch first. Every write names the tool that produced it. See [findings](skills/bevor/references/findings.md).

Code upload and analysis creation are separate from running Bevor's paid security pipeline. The skill follows the user's requested scope for remote operations and reports measured reuse without inventing token, time, or cost savings.

## Reference

| Reference | Use it for |
| --- | --- |
| [Graph navigation](skills/bevor/references/graph-navigation.md) | Scoping a review with calls, state, guards, and change impact. |
| [Findings](skills/bevor/references/findings.md) | What to report, the file formats, where findings land, and duplicates. |

The skill works through the `bevor` CLI. `bevor --help` and `bevor <command> --help` give exact commands and flags. Graph operations and coverage can vary by language, particularly for experimental Soroban support.

## Contributing

Help improve real workflows: clearer instructions, reproducible bug fixes, and better examples. Start with [CONTRIBUTING.md](CONTRIBUTING.md) for the repository map, local validation, pull request process, and bug-report details.

For sensitive security issues, follow the [private reporting guidance](CONTRIBUTING.md#security-reports). Keep private source and credentials out of public issues.

## License

[MIT](LICENSE) · Copyright © 2026 Bevor.
