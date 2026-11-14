# Bevor Agent Skill

Give your coding agent the code graph, findings, and review history behind your next security decision.

[![Validate skill](https://github.com/Bevor-Protocol/Bevor-Skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Bevor-Protocol/Bevor-Skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-5865F2)](https://agentskills.io)

[Website](https://bevor.io) · [Docs](https://bevor.io/docs) · [Dashboard](https://app.bevor.io) · [Join the waitlist](https://www.bevor.io/waitlist) · [X](https://x.com/Bevor_io) · [LinkedIn](https://www.linkedin.com/company/bevor/)

Bevor connects security work to exact source versions. This skill helps agents navigate semantic code graphs, reuse earlier findings, review changes, and save results with their evidence and analysis history.

**Supported AI platforms:**
[![Claude Code](assets/badges/claude-code.svg)](https://code.claude.com/) [![Cursor](assets/badges/cursor.svg)](https://cursor.com) [![Codex](assets/badges/codex.svg)](https://openai.com/codex/) [![GitHub Copilot](assets/badges/github-copilot.svg)](https://github.com/features/copilot) [![Gemini CLI](assets/badges/gemini-cli.svg)](https://geminicli.com/)

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

Restart your coding agent after installation. For a manual install, copy the complete [`skills/bevor/`](skills/bevor/) directory into your client's skill directory, preserving its references and scripts. See the skills CLI's [client directory reference](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

### Connect your account

Remote operations need an authenticated Bevor account. Open the [dashboard](https://app.bevor.io), or [join the waitlist](https://www.bevor.io/waitlist) if you need access.

Public workflows use the production API and dashboard. Set both URLs before authentication or other remote calls:

```bash
export BEVOR_API_URL=https://api.bevor.io
export BEVOR_APP_URL=https://app.bevor.io
```

Check your CLI and account:

```bash
bevor --version
bevor whoami --json
```

If authentication is missing or expired, run `bevor login` and complete browser authorization. Then run `bevor status --json` from the target repository. The skill's [setup guide](skills/bevor/references/cli-workflows.md) covers selecting a workspace, linking a project, matching source, and creating an analysis.

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
| Findings exchange | Deduplicate and batch new findings through YAML, Bevor JSON, or external-tool SARIF. |
| Graph investigation | Follow calls, state access, inheritance, and related code to investigate a security question. |
| Tooling and CI | Use the CLI, Python SDK, or API while preserving existing tools, run identity, and security gates. |
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

CLI 0.2.1 finding writes apply immediately. Bulk import creates findings; existing records require edits. Prefer YAML or Bevor JSON when preserving recommendations and PoCs matters, because the tested SARIF converter drops those fields. See [finding exchange](skills/bevor/references/findings-exchange.md).

Code upload and analysis creation are separate from running Bevor's paid security pipeline. The skill follows the user's requested scope for remote operations and reports measured reuse without inventing token, time, or cost savings.

## Compatibility and reference

The reviewed CLI/SDK contract is **0.2.1**, with Python **3.13+**. The [release pin](tests/fixtures/cli-release.txt) records the package used by validation; it is not a claim that this is the newest release. See [supported smart contract languages](#supported-smart-contract-languages) for language availability. Graph operations and coverage can vary by target, particularly for experimental Soroban support.

| Reference | Use it for |
| --- | --- |
| [CLI workflows](skills/bevor/references/cli-workflows.md) | Setup, source selection, child versions, and recovery. |
| [Graph navigation](skills/bevor/references/graph-navigation.md) | Queries, relations, and released-command workarounds. |
| [Finding exchange](skills/bevor/references/findings-exchange.md) | Bulk payloads, SARIF limitations, and duplicate control. |
| [Generated CLI command tree](skills/bevor/references/cli-command-tree.md) | Released commands and options. |
| [Public documentation](https://bevor.io/docs) | Product, CLI, SDK, and API documentation. |

## Contributing

Help improve real workflows: clearer instructions, reproducible bug fixes, better examples, and checks that catch CLI drift. Start with [CONTRIBUTING.md](CONTRIBUTING.md) for the repository map, local validation, pull request process, and bug-report details.

For sensitive security issues, follow the [private reporting guidance](CONTRIBUTING.md#security-reports). Keep private source and credentials out of public issues.

## License

[MIT](LICENSE) · Copyright © 2026 Bevor.
