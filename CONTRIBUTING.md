# Contributing to Bevor Agent Skill

Contributions should help an agent complete a real security workflow accurately, with less unnecessary discovery and repeated work. A useful change explains the problem, demonstrates the resulting behavior, and includes enough evidence for another person to verify it.

Read [README.md](README.md) for setup and [CLAUDE.md](CLAUDE.md) for repository conventions.

## What to contribute

| Contribution | Useful evidence |
| --- | --- |
| Workflow fixes | A prompt or command that fails, the expected result, and a minimal reproduction. |
| Security guidance | A concrete review scenario showing better reasoning, coverage, or false-positive handling. |
| Finding exchange | Parser fixtures or readbacks demonstrating preserved metadata, correct locations, and duplicate handling. |
| CLI compatibility | The released package version, executable command metadata, and examples that pass against it. |
| Documentation | A real setup or usage ambiguity and a concise, working replacement. |
| Evaluations | Recorded inputs and outputs, verification criteria, and an explicit account of what the test establishes. |

Open an [issue](https://github.com/Bevor-Protocol/Bevor-Skills/issues/new) before a substantial redesign so the intended behavior can be discussed. Small corrections and focused fixes can go directly to a pull request.

## Request language support

Bevor supports Solidity, Anchor Rust, and GenLayer Intelligent Python Contracts, with experimental support for Soroban Rust.

We'd love developers and security researchers to request support for other major smart contract languages through [GitHub issues](https://github.com/Bevor-Protocol/Bevor-Skills/issues/new) or the [Bevor waitlist](https://www.bevor.io/waitlist). These requests help us prioritize what to support next.

Tell us the language and framework, your development or security use case, and the capabilities you need. A public example project is helpful when available; a language request does not require an implementation or pull request.

## Repository map

```text
skills/bevor/
├── SKILL.md                     # Selection, shared workflow, and boundaries
├── agents/openai.yaml           # Codex display and invocation metadata
├── references/                  # Focused workflow guidance
└── scripts/                     # CLI contract and documentation checks

tests/
├── fixtures/                    # Release pin, dependencies, generated contract
├── trigger_cases.json           # Selection scenarios
├── workflow_cases.json          # Expected workflow decisions
├── test_skill.py                # Structure and contract checks
└── test_cli_examples.py         # Released parser and example checks

.github/workflows/
├── validate.yml                 # Pull request and main-branch checks
└── cli-release-drift.yml         # Scheduled/manual latest-release comparison
```

Keep shared decisions in `SKILL.md` and task-specific detail in the corresponding reference. Prefer one maintained explanation over repeating the same procedure across files. Generated snapshots belong in the update process below.

## Pull request process

1. Fork the repository, or use a branch if you have write access. Start from current `main`.
2. Keep the change focused on one problem. Preserve unrelated work and existing user-intent boundaries.
3. Update the affected instructions, examples, and meaningful tests together. Use the released CLI/SDK contract for exact behavior.
4. Run the checks below. For behavior changes, exercise the relevant workflow and record the verified outcome.
5. Bring your branch up to date with `main`, resolve conflicts, and open a pull request with the description format below.
6. Respond to review and keep the final description aligned with the implementation.

Reserve release-pin and skill-version changes for intentional, reviewed compatibility updates. Ordinary prose corrections do not need a version bump.

### Pull request description

Explain the user-visible problem and resulting behavior first. Include a concrete before/after example when it makes the fix easier to assess.

```markdown
## Change
What failed or was unclear, and what now happens?

## Evidence
Reproduction, relevant CLI/SDK versions, and the observed result.

## Validation
Checks run and their results. Identify any behavior not exercised.

## Compatibility
Affected clients, package versions, or remote semantics, if applicable.
```

### Before submitting

- [ ] The change is scoped and all linked files exist.
- [ ] Commands, payloads, and platform claims match verified behavior.
- [ ] Examples use synthetic or shareable data; no credentials or private source are included.
- [ ] Required local checks pass, and relevant behavior changes have evidence.
- [ ] Generated references were regenerated where required.
- [ ] The description identifies limitations and separates measured results from assumptions.

## Local validation

Use an active Python **3.13+** virtual environment. From the repository root:

```bash
python -m pip install "bevor-cli==$(cat tests/fixtures/cli-release.txt)" -r tests/fixtures/cli-dependencies.txt
python -m unittest discover -s tests -v
python skills/bevor/scripts/check_cli_contract.py
python skills/bevor/scripts/check_docs_links.py
git diff --check
```

The tests and contract check do not require Bevor credentials or make remote Bevor requests. The link checker accesses public documentation. Run the suite with the CLI installed: otherwise the released-parser tests can be skipped, which is not a complete validation result.

For workflow changes, also run [Actionlint](https://github.com/rhysd/actionlint). For agent-facing behavior, test a realistic prompt with the changed skill and report the client, model, effort setting where available, and result. Name the clients actually tested; compatibility with the skill format is not evidence of identical behavior across all clients.

Fixtures describe expected decisions. Passing a static check does not establish audit quality, successful remote writes, or correct finding inheritance.

## Updating the CLI contract

Exact command paths, flags, choices, and defaults come from the installed CLI's executable command tree. Do not manually patch `cli_contract.json`, `cli_commands.txt`, or the generated command-tree reference to make a failing check pass.

1. Install the intended **released** CLI and compatible renderer dependencies in an isolated environment.
2. Regenerate the reviewed contract:

   ```bash
   python skills/bevor/scripts/check_cli_contract.py --update
   ```

3. Review the generated diff, including the CLI release pin and Typer/Click dependency pins. Update affected recipes and parser examples.
4. Run the complete local checks. If write behavior or lineage semantics changed, run a small authorized reproduction with an isolated fixture and verify the stored result.

The scheduled drift workflow installs the latest published CLI, compares its contract, and provides an update artifact on failure. It has read-only repository permissions and does not publish documentation automatically. Source main and a published wheel can report the same package version while exposing different behavior; record which artifact was tested.

The vendored exporter is `scripts/cli_contract.py` inside the skill. It was developed from `bevorai-api/scripts/codegen/python/cli_contract.py` at source base `a4593aad271d911cd8868670fa568a745e7e050d`, with SHA-256 `535e18dc094123ad87af715557071879b552091c211248600a20ff522fa9000b`. Refresh it from the reviewed CLI release-reference artifact when the exporter changes, and update this provenance.

## Testing remote workflows

Use an isolated fixture and an explicitly authorized workspace/project. Public workflows use the production API and dashboard:

```bash
export BEVOR_API_URL=https://api.bevor.io
export BEVOR_APP_URL=https://app.bevor.io
```

Keep upload, finding writes, lineage changes, and paid pipeline runs within the task's authorized scope. Finding writes in CLI 0.2.1 apply immediately, so review the local batch before importing. A syntax check cannot replace verification of the resulting remote state.

For a setup/import/lineage change, capture the code fingerprint and processing status, selected analysis/version, expected parent, accepted finding fields, and origin preservation where applicable. After an ambiguous failure, inspect the existing result before retrying. Distinguish automatically matched transitions from verified security fixes.

Use synthetic or explicitly shareable source. Redact account identifiers when unnecessary and never include credentials, token-bearing responses, or private contract content in public logs or pull requests.

## Reporting bugs

[Open a bug report](https://github.com/Bevor-Protocol/Bevor-Skills/issues/new) with a minimal reproduction and these details:

```text
Skill revision or installation date:
Coding agent and version:
Model and reasoning effort, if known:
CLI and SDK versions:
OS and execution context (CLI, CI, or offline):
Prompt or command:
Expected behavior:
Observed behavior and redacted output:
Reproduction steps or shareable fixture:
```

Say whether the failure involves instructions, command parsing, upload processing, finding conversion, or lineage. Include relevant resource states rather than entire private sessions. If reporting a performance change, distinguish complete task time from command time, state the comparison conditions, and include verified outcomes alongside counts. Do not present invented model responses or estimated savings as measured evidence.

## Security reports

Do not disclose live vulnerabilities, private repository contents, or credentials in public issues. Contact the Bevor team through [the website](https://bevor.io) or [X](https://x.com/Bevor_io) to arrange a private reporting channel before sharing sensitive details.

For ordinary skill bugs with a synthetic reproduction, use the public issue process above. Keep reviews respectful and specific: discuss the behavior and evidence, and make proposed corrections actionable.

## Community and license

[Website](https://bevor.io) · [Docs](https://bevor.io/docs) · [Dashboard](https://app.bevor.io) · [Waitlist](https://www.bevor.io/waitlist) · [X](https://x.com/Bevor_io) · [LinkedIn](https://www.linkedin.com/company/bevor/)

This repository is licensed under [MIT](LICENSE). Preserve applicable attribution and include only material you have the right to contribute.
