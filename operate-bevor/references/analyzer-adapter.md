# Analyzer Adapter Protocol

`operate-bevor` may orchestrate any security analyzer that follows this protocol. An analyzer may
be:

- The local `analyze-codebase` skill
- Another installed security skill
- An external agent or CLI such as Mythos
- A human-led process that returns structured findings

The analyzer owns security reasoning. `operate-bevor` owns preparation, context transport, and
recording.

## Required Preflight Announcement

Before scanning begins, print exactly one concise analyzer announcement. Do not ask for confirmation
when the selection is unambiguous.

Direct analyzer:

```text
Security analyzer: analyze-codebase | mode: direct | scope: requested codebase
```

Bevor-managed analyzer:

```text
Security analyzer: mythos | mode: Bevor-managed, prior-informed | scope: 3 explicit entry points
```

The announcement must name:

- The selected analyzer
- Direct or Bevor-managed mode
- Fresh or prior-informed context for Bevor-managed runs
- The requested scope in a short human-readable form

If `operate-bevor` defaults to `analyze-codebase`, say so in the same line:

```text
Security analyzer: analyze-codebase (default) | mode: Bevor-managed, fresh | scope: first-party
```

Do not print repeated analyzer banners during the run. Ask the user to choose only when multiple
analyzers were requested ambiguously, the named analyzer is unavailable, or selecting one would
materially change the requested scope or security methodology.

## Invocation Modes

### Direct Analyzer

Use the analyzer without Bevor orchestration:

```text
Use $analyze-codebase to audit this repository.
```

The analyzer scans and produces local findings. It does not synchronize with or record results in
Bevor.

### Bevor-Managed Analyzer

Invoke `operate-bevor` and name the analyzer:

```text
Use $operate-bevor with $analyze-codebase to run a scoped audit and record the findings.
Use $operate-bevor with Mythos, using prior Bevor findings as context.
Use $operate-bevor with $pashov to run a fresh first-party scan and record the findings.
```

The orchestrator follows `byos-workflow.md`, prepares the request, invokes the selected analyzer,
and records normalized findings.

Skills do not create universal slash commands or Bevor CLI flags. A host or plugin may expose
shortcuts such as `/bevor mythos`, but the shortcut must translate into the same Bevor-managed
analyzer request. Do not pretend the current Bevor CLI has an analyzer-selection flag.

## Analyzer Request

Represent the handoff with these logical fields, whether passed as a file, prompt, or tool
arguments:

```yaml
schema_version: "1"
analyzer: mythos
context_mode: prior_informed
scan_instruction: Review authorization and withdrawal paths.
analysis_id: <new-bevor-analysis-id>
code_version_id: <active-code-version-id>
scope_manifest: .bevor/analyses/<analysis-id>/byos/context/scopes.json
evidence_dir: .bevor/analyses/<analysis-id>/
prior_findings: .bevor/analyses/<analysis-id>/byos/context/prior-findings.json
raw_output_dir: .bevor/analyses/<analysis-id>/byos/raw-output/
normalized_findings_dir: .bevor/analyses/<analysis-id>/findings/
```

`prior_findings` is omitted for fresh runs. The orchestrator must provide the scan instruction and
scope. The analyzer must not silently broaden either.

## Analyzer Response

Preferred response:

- One Bevor-compatible `.yaml` file per finding in `normalized_findings_dir`
- `source` set to the selected analyzer name
- Every finding tied to `scope_id` or graph-backed `location_id`

Accepted fallback:

- Tool-native output in `raw_output_dir`
- Enough stable location and scope information for `operate-bevor` to normalize it without changing
  the security claim

If the analyzer cannot provide a supported location or a complete claim, reject the item or return
it as an unrecorded lead. Do not fabricate missing evidence to make an import pass.

## Selection Rule

- If only an analyzer is invoked, run it directly.
- If `operate-bevor` and an analyzer are invoked together, use Bevor-managed mode.
- If `operate-bevor` is invoked for a security scan without an analyzer name, default to
  `analyze-codebase`.
- If multiple analyzers are requested, create and record a distinct Bevor analysis for each unless
  the user explicitly requests a combined run.
- Always print the required preflight announcement before invoking the analyzer.
