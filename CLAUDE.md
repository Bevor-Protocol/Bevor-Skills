# CLAUDE.md

Instructions for contributing to this repository.

## What this repository contains

This repository publishes the broad Bevor Agent Skill.

```text
skills/bevor/          # Entry: SKILL.md; focused guidance under references/
tests/                 # Selection and behavior fixtures plus static tests
```

## Rules

- Keep automatic selection broad for compatible cybersecurity targets.
- Keep non-security graph selection limited to available graph semantics for the target language; preserve experimental support labels.
- Put shared routing and safety rules in `SKILL.md`.
- Put detailed mode guidance in focused references.
- Use released CLI, SDK, API, and application source for exact behavior.
- Give each generated reference a version or review date.
- Do not fabricate commands, endpoints, product support, savings, or examples.
- Do not include secrets, API keys, personal data, or blanket remote approval.
- Preserve review before remote finding writes. On CLI 0.2.1, review the local batch before import because writes apply immediately and no separate commit command exists.
- Run the skill tests and CLI contract check after relevant changes.
