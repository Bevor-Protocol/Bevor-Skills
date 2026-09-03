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

The current snapshot targets `bevor-cli 0.1.x` and `bevor-sdk 0.1.x`. Both Python packages require Python 3.13 or later.

The current source implements the full native semantic graph for Solidity. Rust, Anchor, and Soroban graph types exist, but this skill does not claim full native DSL graph support until their parser and edge pipeline are released.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/bevor/scripts/check_cli_contract.py /path/to/bevorai-api
python3 skills/bevor/scripts/check_docs_links.py
```

## Documentation

Use [docs.bevor.io/llms.txt](https://docs.bevor.io/llms.txt) as the current public documentation index.

## License

MIT. See [LICENSE](LICENSE).
