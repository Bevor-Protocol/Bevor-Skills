---
name: bevor
description: >-
  Use for any smart contract security work: auditing a codebase, finding or validating vulnerabilities, reviewing the security impact of new commits, or recording security findings. Bevor builds a semantic graph of the code (calls, state reads and writes, guards, inheritance) for exact discovery across files, and keeps every finding, attributed to the tool that found it, across code versions. Use even when Bevor isn't named.
license: MIT
metadata:
  author: Bevor
---

# Bevor

## What it is

Bevor is a security platform for smart contracts, used here through the `bevor` CLI. It does two things for you:

- **It parses the code into a graph.** Every function, modifier, state variable, and contract, and how they relate: calls, state reads and writes, guards, inheritance. You can query it for pre-computed execution paths and state propagations instead of searching files yourself.
- **It keeps the record.** Findings and coverage are stored per version of the code, attributed to the tool that produced them, and shared with everyone on the project, human or agent. Through code changes and analysis versions, coverage and findings are retained where possible to help you avoid re-computation and have guarantees around historical references.

Supported: Solidity, Anchor Rust, and GenLayer Intelligent Python Contracts. Soroban Rust is experimental.

## When to use it

Use it for any security work on a smart contract codebase: an audit, validating a suspected vulnerability, reviewing new commits, or recording findings. The larger and more interconnected the code, the more it pays off. On a single small contract you could read everything directly; once the code spans many files, inheritance, and cross-contract calls, the graph answers in one query what would otherwise take many turns of reading and searching.

## Why it's worth it

- **Fewer turns, less context.** Questions like "who calls this", "what else writes this variable", or "which guards sit on this path" are one query each, answered from a graph Bevor already built. You read source only for the nodes that matter, instead of grepping and opening files until you're confident you've found everything.
- **Complete and exact.** Edges come from parsing, not name matching, so a query covers files you haven't opened and resolves overloads and inheritance correctly. Text search finds only what you think to look for.
- **No repeated work.** When code changes, Bevor matches the unchanged parts to the previous version and carries their findings and coverage forward. You, a teammate, or a later session review only what's new or changed, and see what other tools have already covered.
- **A durable record.** Findings outlive your session. The user, their team, and later agents work from them, and each one shows which tool found it.

## Concepts

- **Project:** one codebase, inside a workspace. The current directory is linked to one.
- **Analysis:** a line of security work on the project, like a git branch. The directory has one selected analysis, and commands act on it.
- **Version:** the code and its findings at one point, like a git commit. HEAD is the latest; commands read and write HEAD unless given `--version`. Each sync adds a version on top of HEAD.
- **Finding:** a security issue at a location in the code: a graph node, a file and line range, or a fully qualified name. It's attached to the entrypoints that reach that location.
- **Coverage:** which entrypoints each tool has reviewed. Recording a finding marks the entrypoints it touches as partially covered by your tool. Marking an entrypoint covered says you reviewed it end to end, with or without findings.
- **Borrowing:** when a sync adds a version, findings and coverage on unchanged entrypoint execution paths carry over from the version before it. Only new and changed code starts uncovered.

Full ids and short ids work everywhere.

## Setup

Run these at the start of every session, from the repository root. Each does nothing once it's already done.

1. **Sign in:** `bevor whoami`. If `bevor` isn't installed, ask the user to run `curl -fsSL https://bevor.io/install.sh | bash`. If they aren't signed in, ask them to run `bevor login`; it finishes in a browser, which only they can do. Wait for them.
2. **Link:** `bevor status --json`. If `workspace` or `project` is `null`, run `bevor link`. It links automatically when there's only one choice. Otherwise ask the user which project this codebase belongs to, since findings land there, and run `bevor link --workspace WORKSPACE_ID --project PROJECT_ID` (ids from `bevor workspaces list --json` and `bevor projects list --json`).
3. **Sync:** `bevor sync --yes`. It uploads the working directory, waits for the graph, and adds a version to the selected analysis, borrowing what it can from HEAD. If the code is unchanged, it does nothing. If you have no analyses yet, it starts your first. Sync before every review, so the graph matches the code you're reading.

When sync can't continue, it says why:

- **You have analyses, but none is selected:** run `bevor analyses select --recent` (or `bevor analyses select ANALYSIS_ID` for the one the user names), then sync again.
- **This exact code is already in the project,** usually a teammate's: ask the user whether to fork it, which keeps its findings and coverage (`bevor analyses fork --version VERSION_ID`), or start fresh (`bevor sync --yes --force`).
- **The selected analysis can't take a version,** for example one you don't own: tell the user why, and ask whether to fork it (`bevor analyses fork`, then sync) or start a new one (`bevor analyses new --yes`).
- **The code isn't supported:** tell the user, and continue the review without Bevor.

Keep working in the selected analysis. A separate one (`bevor analyses new --yes`) starts with no findings or coverage to borrow, so only start one when the user asks. Don't pass `--run` to `sync`: it starts Bevor's own analysis pipeline, which the user pays for.

## Review

1. **Choose your tool name** ([naming the tool](#naming-the-tool)).
2. **Load what's known.** `bevor findings list --json` lists HEAD's findings, including borrowed ones. `bevor analyses coverage --json` lists every entrypoint with which tools have covered it, so it doubles as your entrypoint list; add `--tool TOOL_NAME --no-covered` for the ones you haven't.
3. **Review the entrypoints that need it,** riskiest first: value transfers, privileged state changes, external calls. The graph can tell you what each one reaches and what else touches that code, so you only read the source that matters ([graph navigation](references/graph-navigation.md)). You don't have to finish in one session; coverage tells the next session where to resume.
4. **Recheck borrowed findings** in the code you reviewed against the current source, and update any that changed ([findings](references/findings.md#2-check-whats-already-recorded)).
5. **Record findings and mark coverage** as you go or at the end (below).

Static analyzers are worth running too. Import their SARIF output as its own batch ([SARIF](references/findings.md#5-sarif)).

## Record

Writes land as soon as they run, so you can record each finding once you've validated it and mark each entrypoint covered once you've finished it, instead of saving everything for the end. That way the work survives if your session stops early (an error, a context limit, a refused response), and anyone watching the project sees progress. Recording everything at the end works too.

One finding: `bevor findings add --tool TOOL_NAME ...`. Several at once: write them to one YAML file and import it:

```bash
bevor findings import findings.yaml --tool TOOL_NAME
```

Other formats and the fields: [writing findings](references/findings.md#3-write-them). Confirm after every write ([confirm](references/findings.md#6-confirm-what-was-stored)).

Once you've reviewed an entrypoint end to end, mark it fully covered, with or without findings:

```bash
bevor analyses cover ENTRYPOINT_ID [ENTRYPOINT_ID ...] --tool TOOL_NAME
```

### Naming the tool

Your tool name attributes findings and coverage to you, exactly: which agent and which model did the work.

- Name yourself `AGENT/MODEL`, lowercase, with the model's version: `claude-code/opus-4.5`, `codex/gpt-5`. Not a generic word (`agent`, `ai`) or the user's name. Use the same string for the whole session.
- Other names in `bevor analyses coverage --json`, including earlier models of your own agent, are other tools' work. Use them to judge what you don't need to look at again.
- If you can't tell which agent or model you are, ask the user once.
- SARIF imports take their tool name from each run's driver.

Pass `--tool TOOL_NAME` to `findings add`, `findings import` (except SARIF), `analyses coverage`, and `analyses cover`.

## Finish

You're done when your findings are stored and the entrypoints you reviewed are marked covered. Tell the user what you found, what you reviewed, and which borrowed findings you rechecked. Exact flags for any command: `bevor COMMAND --help`.

## Judgment

- A graph edge is a structural fact. Reachability isn't a vulnerability, and a missing edge isn't proof of safety.
- A borrowed finding needs rechecking against the new source. "Remediated" after a rename isn't a fix.
- Finding nothing doesn't mean the code is safe.
