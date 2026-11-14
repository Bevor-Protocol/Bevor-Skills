# Bevor Skill

An Agent Skill for graph-aware cybersecurity work and Bevor ecosystem development.

The skill starts automatically for compatible cybersecurity targets, even when a request does not name Bevor. It uses exact code identity, semantic graph relations, earlier findings, and structured result exchange to reduce repeated work.

## Capabilities

- Control the Bevor CLI without repeated help discovery.
- Navigate the Solidity semantic graph and select affected scope.
- Reuse exact-version findings, remediations, and analysis history.
- Exchange SARIF and remove duplicate findings before submission.
- Build Python tools with `bevor-sdk` or non-Python tools with OpenAPI.
- Connect existing web3 security CI jobs to Bevor.
- Run a cheap static baseline before heavyweight AI security tools.
- Review findings, graphs, and project history in the Dashboard.

## Installation

Remote Bevor operations require the CLI and an authenticated account. Check setup once per session/environment and reuse it across audits. Documentation edits and offline contract tests need no login. See [CLI installation, updates, and authentication](skills/bevor/SKILL.md#cli-installation-updates-and-authentication).

With a compatible skills CLI:

```bash
npx skills add Bevor-Protocol/Bevor-Skills
```

For a manual installation, copy or link `skills/bevor/` into an agent skill directory:

| Agent | Project directory | Personal directory |
| --- | --- | --- |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| GitHub Copilot | `.github/skills/` or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` |
| Cursor | `.cursor/skills/` or `.agents/skills/` | `~/.cursor/skills/` or `~/.agents/skills/` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` |

The skill uses [`bevor-cli 0.2.1` from PyPI](https://pypi.org/project/bevor-cli/) (current as of 2026-11-13). The [official installer](https://bevor.io/install.sh) installs or upgrades the CLI and installs the Bevor skill:

```bash
curl -LsSf https://bevor.io/install.sh | bash
```

Use `bevor --version` to inspect the installed release and `bevor upgrade` to check PyPI and apply an available update.

## Example requests

```text
Audit this Cantina target.
What changed around this contract and which findings already exist?
Import this Slither SARIF and remove duplicate findings.
Record the existing security CI runs in Bevor.
Build a security analyzer with the Bevor graph.
Use the Bevor SDK from this Python service.
```

## Structure

```text
skills/bevor/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/

tests/
├── trigger_cases.json
├── workflow_cases.json
├── fixtures/cli_commands.txt
└── test_skill.py
```

The entry file contains shared routing and safety rules. Agents load a focused reference only when the task requires it.

## Compatibility

The tested release is `bevor-cli 0.2.1`, requiring Python 3.13+. Command paths and options come from its executable Typer application. Source main can contain unreleased changes even when its version string matches PyPI.

Finding writes apply immediately to the selected analysis version. The skill reviews local batches before submission and does not promise an unavailable staged-commit workflow.

The current source implements the full native semantic graph for Solidity. Rust, Anchor, and Soroban graph types exist, but this skill does not claim full native DSL graph support until their parser and edge pipeline are released.

## Validation

```bash
python3 -m pip install "bevor-cli==$(cat tests/fixtures/cli-release.txt)" -r tests/fixtures/cli-dependencies.txt
python3 -m unittest discover -s tests -v
python3 skills/bevor/scripts/check_cli_contract.py
python3 skills/bevor/scripts/check_docs_links.py
```

PR checks pin the CLI and Typer/Click metadata renderer versions. They validate the command contract, documented command/option examples, and YAML finding examples without authentication or network requests to Bevor. Link checks use public documentation only.

A scheduled/manual workflow installs the latest public CLI and fails on contract drift. It uploads a generated update patch, installed dependency versions, and validation output. It has read-only repository permissions and no Bevor credentials. After installing the intended release, regenerate with:

```bash
python3 skills/bevor/scripts/check_cli_contract.py --update
```

Review workflow prose and parser behavior after regeneration. The checker verifies syntax and metadata; it does not execute remote commands or prove semantic accuracy. Run short staging tests before accepting behavioral changes.

The vendored checker comes from `bevorai-api/scripts/codegen/python/cli_contract.py`, developed against source base `a4593aad271d911cd8868670fa568a745e7e050d`. Its SHA-256 is `535e18dc094123ad87af715557071879b552091c211248600a20ff522fa9000b`. Refresh it from the reviewed CLI release-reference artifact when that exporter changes.

## Documentation

Use [www.bevor.io/docs](https://www.bevor.io/docs) for current public documentation.

## License

MIT. See [LICENSE](LICENSE).
