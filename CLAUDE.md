# CLAUDE.md

Instructions for Claude when contributing to this repository.

## What This Repo Is

A library of Claude AI skills. Each skill is a focused, self-contained capability for Claude Code in VS Code and Cursor.

## Structure

```
analyze-codebase/      # Security reasoning and intermediate finding production
operate-bevor/         # Bevor CLI lifecycle, synchronization, and findings transport
```

## Rules

- One skill, one purpose.
- Keep state-changing Bevor operations out of `analyze-codebase`.
- Keep vulnerability discovery and assessment out of `operate-bevor`.
- Regenerate `operate-bevor/references/cli-surface.md` from the CLI instead of editing it manually.
- No fabricated examples - outputs must reflect real model responses.
- No secrets, API keys, or personal data.
