# Bevor Skills

Two skills with an explicit findings handoff:

| Skill | Owns | Does not own |
| --- | --- | --- |
| [`analyze-codebase`](analyze-codebase/) | Security reasoning, graph evidence, judging, intermediate findings | Synchronization, analysis lifecycle, submission |
| [`operate-bevor`](operate-bevor/) | Bevor CLI operations, synchronization, lifecycle, external-tool integration, finding transport | Vulnerability discovery or assessment |

The intended composition is:

```text
codebase or Bevor graph
  -> analyze-codebase
  -> per-scope findings
  -> operate-bevor
  -> Bevor or an external security system
```

The analysis skill may use read-only Bevor graph commands. All state-changing Bevor operations are
owned by `operate-bevor`.

`operate-bevor/references/byos-workflow.md` defines the end-to-end Bring Your Own Security Agent
flow: retrieve optional prior-run findings, create a fresh or parented analysis, choose scope, run an
external agent, normalize its results, and record them with the CLI.

`operate-bevor/references/analyzer-adapter.md` makes analyzers interchangeable. `analyze-codebase`
can run directly, or `operate-bevor` can wrap it, Mythos, or another installed security skill and
record the selected analyzer's findings through the same BYOS flow.

Every scan prints one concise preflight line naming the selected analyzer, mode, and scope. Clear
defaults do not require confirmation; only ambiguous or unavailable analyzer selections interrupt
the flow.

## Maintaining CLI Accuracy

`operate-bevor/references/cli-surface.md` is generated from the CLI's registered Typer command tree:

```bash
python operate-bevor/scripts/generate_cli_reference.py \
  --cli-root /path/to/bevorai-api/packages/cli \
  --output operate-bevor/references/cli-surface.md
```

Pass `--check` to detect drift without rewriting the generated reference.
