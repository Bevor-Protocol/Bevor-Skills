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
└── references/                  # Graph navigation, new commits, findings

tests/
├── trigger_cases.json           # Selection scenarios
├── test_skill.py                # Structure and scope checks
└── test_cli_examples.py         # Examples checked against the CLI's parser

.github/workflows/
└── validate.yml                 # Pull request and main-branch checks
```

Keep shared decisions in `SKILL.md` and task-specific detail in the corresponding reference. Prefer one maintained explanation over repeating the same procedure across files. Don't copy command trees, flags, or version numbers into the skill; agents get those from `bevor --help`.

## Pull request process

1. Fork the repository, or use a branch if you have write access. Start from current `main`.
2. Keep the change focused on one problem. Preserve unrelated work and existing user-intent boundaries.
3. Update the affected instructions, examples, and meaningful tests together. Check commands against the current CLI's `--help`.
4. Run the checks below. For behavior changes, exercise the relevant workflow and record the verified outcome.
5. Bring your branch up to date with `main`, resolve conflicts, and open a pull request with the description format below.
6. Respond to review and keep the final description aligned with the implementation.

### Pull request description

Explain the user-visible problem and resulting behavior first. Include a concrete before/after example when it makes the fix easier to assess.

```markdown
## Change
What failed or was unclear, and what now happens?

## Evidence
Reproduction, CLI version, and the observed result.

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
- [ ] The description identifies limitations and separates measured results from assumptions.

## Local validation

Use an active Python **3.13+** virtual environment. From the repository root:

```bash
python -m pip install bevor-cli
python -m unittest discover -s tests -v
git diff --check
```

The tests don't need Bevor credentials or make remote requests. Run them with the CLI installed; otherwise the example-parser test is skipped.

For workflow changes, also run [Actionlint](https://github.com/rhysd/actionlint). For agent-facing behavior, test a realistic prompt with the changed skill and report the client, model, effort setting where available, and result. Name the clients actually tested; compatibility with the skill format is not evidence of identical behavior across all clients.

Passing a static check does not establish audit quality, successful remote writes, or correct finding inheritance.

## Testing remote workflows

Use an isolated fixture and an explicitly authorized workspace/project. The CLI targets the production API and dashboard by default. To test against another deployment, set `BEVOR_API_URL` and `BEVOR_APP_URL` in that shell.

Keep upload, finding writes, lineage changes, and paid pipeline runs within the task's authorized scope. Finding writes apply as soon as they run, so review the local batch before importing. A syntax check cannot replace verification of the resulting remote state.

For a setup/import/lineage change, capture the code fingerprint and processing status, selected analysis/version, expected parent, accepted finding fields, and origin preservation where applicable. After an ambiguous failure, inspect the existing result before retrying. Distinguish automatically matched transitions from verified security fixes.

Use synthetic or explicitly shareable source. Redact account identifiers when unnecessary and never include credentials, token-bearing responses, or private contract content in public logs or pull requests.

## Reporting bugs

[Open a bug report](https://github.com/Bevor-Protocol/Bevor-Skills/issues/new) with a minimal reproduction and these details:

```text
Skill revision or installation date:
Coding agent and version:
Model and reasoning effort, if known:
CLI version:
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
