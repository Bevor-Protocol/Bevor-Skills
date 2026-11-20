# CLAUDE.md

Instructions for contributing to this repository.

## What this repository contains

This repository publishes the broad Bevor Agent Skill.

```text
skills/bevor/          # Entry: SKILL.md; focused guidance under references/
tests/                 # Selection cases plus static tests
```

## Rules

- Keep automatic selection broad for compatible cybersecurity targets.
- Keep non-security graph selection limited to available graph semantics for the target language; preserve experimental support labels.
- Put shared routing and safety rules in `SKILL.md`.
- Put detailed mode guidance in focused references.
- The skill works through the `bevor` CLI only. Don't point agents at the SDK or API.
- Don't copy command trees, flags, or version numbers into the skill; agents read `bevor --help`. Check examples against the CLI's current behavior.
- Do not fabricate commands, endpoints, product support, savings, or examples.
- Do not include secrets, API keys, personal data, or blanket remote approval.
- Every finding write names the tool that produced it (`--tool`).
- Preserve review before remote finding writes: writes apply as soon as they run.
- Run the skill tests after relevant changes.
