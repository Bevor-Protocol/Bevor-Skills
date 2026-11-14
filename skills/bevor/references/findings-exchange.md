# Finding exchange and duplicate control

Reviewed against released CLI/SDK 0.2.1 on 2026-11-14.

## Review before the write

Finding add, import, edit, and delete operate directly on HEAD or an explicit version. There is no separate CLI commit operation. Preserve the review boundary by validating and reviewing the local batch before the authorized write.

Resolve exact code identity, fetch existing findings, deduplicate by root cause and semantic location, and submit once. Retain accepted IDs and read back the result. Do not retry an uncertain import without checking what already exists.

## Supported import formats

`bevor findings import` accepts a YAML file, a directory of YAML files, a SARIF file, or JSON with a top-level `findings` array. YAML supports multiple mappings separated by `---`.

For new findings authored by the agent, collect the reviewed batch and import it once. Prefer multi-document YAML or Bevor JSON when preserving exact node IDs, recommendations, and PoCs matters. Avoid a loop of one `findings add` call per new finding.

Use nested YAML, not the obsolete flat shape:

```yaml
tool: independent-review
location:
  strategy: node_id
  node_id: ENTRYPOINT_NODE_ID
  location_id: EVIDENCE_NODE_ID
metadata:
  type: access-control
  level: high
  name: Unauthorized state change
  explanation: Evidence, preconditions, attack path, and effect.
  recommendation: Enforce the required permission at this entrypoint.
  poc: Reproduction steps or a test reference.
```

The parser requires a location. Metadata, when present, requires type, level, name, and nonempty explanation. Levels are critical, high, medium, and low. Omit optional keys rather than substituting unsupported fields.

Locations:

- `node_id`: supply `node_id`, `location_id`, or both. A location-only record can fan out to every reachable entrypoint.
- `physical`: supply `uri` and a complete pair: `startLine/endLine`, `charOffset/charLength`, or `byteOffset/byteLength`.
- `logical`: supply `fully_qualified_name`.

Prefer graph-node locations. Non-Solidity files may lack a resolvable graph location.

```bash
bevor findings list --json
bevor findings import findings.yaml
bevor findings list --json
```

For one YAML mapping use `bevor findings add --file finding.yaml`. For SARIF use `bevor findings import results.sarif`. Neither write command accepts `--json`. Use the list command to read back results.

Validate local YAML without authentication:

```python
from pathlib import Path
from bevor_cli.findings_yaml import FindingYamlParser

records = FindingYamlParser.from_file(Path("findings.yaml")).parse_many()
assert records
```

This checks shape, not semantic duplicates, node existence, or finding validity.

## SARIF boundaries in release 0.2.1

Use SARIF for external tools that already emit it. Validate the conversion locally with `from bevor_sdk.helpers.sarif import sarif_to_bevor`, then compare the converted records with the source results before upload.

- Severity maps as `error → critical`, `warning → high`, `note → medium`, and `none → low`. An omitted level becomes high. Review this against the producer's severity meaning.
- Import reads only the first physical or logical location. Bevor node-ID properties do not override it.
- Import does not preserve recommendation or PoC properties. Native Bevor SARIF export followed by import also changes title/explanation fields. It is not a lossless backup or replay format.
- Physical locations can resolve to multiple entrypoints or no finding. Read back the results and compare counts, metadata, severity, and resolved locations. A successful import exit alone is insufficient.

Prefer YAML or Bevor JSON for full-fidelity replay of your own findings. SARIF import success establishes transport compatibility, not preservation of every original field.

## Review marks without findings

Omit metadata to mark a reviewed location:

```yaml
tool: independent-review
location:
  strategy: node_id
  node_id: REVIEWED_ENTRYPOINT_ID
```

Batch review marks with findings in one import. Count them separately from vulnerabilities. Never mark unreviewed code clean merely to improve coverage statistics.

Direct flags have an all-or-nothing metadata contract. Supply all four metadata fields to record a finding. Partial metadata may be interpreted as a review mark, so prefer validated YAML for automation.

## Duplicate control

Compare the batch with existing and inherited findings by origin identity, root cause, semantic location, affected asset, and attack path. Titles alone are insufficient. Preserve discovery attribution and add corroboration to the existing finding rather than duplicating it. The server does not promise semantic deduplication.

Bulk import creates findings; it does not replace edits to existing identities. Batch new additions, then use `bevor findings edit` for required updates to existing finding IDs. Serial edits can be necessary even when serial additions are avoidable. Never re-import an edited finding as a new record solely to reduce call count.

## Acknowledgement

CLI 0.2.1 exposes explicit acknowledge and unacknowledge operations. These read the current state and invoke the underlying toggle only when needed. Use the requested desired state, confirm the target, and read back the result. Do not call a raw SDK toggle repeatedly.
