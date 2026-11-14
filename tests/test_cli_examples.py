"""Behavioral checks against the released CLI parser; no credentials or requests."""
from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/bevor/scripts"))
HAS_CLI = importlib.util.find_spec("bevor_cli") is not None


@unittest.skipUnless(HAS_CLI, "Install the tested CLI release to validate executable examples")
class ReleasedCliExamples(unittest.TestCase):
    def test_nested_yaml_and_review_marks_parse_without_authentication(self):
        from bevor_cli.findings_yaml import FindingYamlParser

        text = (ROOT / "skills/bevor/references/findings-exchange.md").read_text()
        examples = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)
        self.assertEqual(len(examples), 2)
        with patch("bevor_cli.configuration.creds.Credentials.load", side_effect=AssertionError("Unexpected credential access")):
            finding, reviewed = [FindingYamlParser.from_text(example).parse() for example in examples]
        self.assertEqual(finding["metadata"]["level"], "high")
        self.assertEqual(finding["location"]["strategy"], "node_id")
        self.assertNotIn("metadata", reviewed)
        self.assertEqual(reviewed["tool"], "independent-review")

    def test_contract_detects_old_commands_and_invalid_options(self):
        from cli_contract import check_command, export_contract

        contract = export_contract()
        for command in (
            "bevor context --json",
            "bevor analysis commit",
            "bevor findings import findings.yaml --json",
            "bevor projects create --kind invented",
        ):
            with self.subTest(command=command):
                self.assertIsNotNone(check_command(command.split(), contract))
        for command in (
            "bevor analyses create --json",
            "bevor projects create --name Test --description Test --kind standard --yes",
            "bevor findings import findings.yaml",
        ):
            self.assertIsNone(check_command(command.split(), contract))

    def test_multi_document_yaml_preserves_full_finding_metadata(self):
        from bevor_cli.findings_yaml import FindingYamlParser

        text = (ROOT / "skills/bevor/references/findings-exchange.md").read_text()
        example = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)[0]
        second = example.replace("Unauthorized state change", "Separate state change")
        records = FindingYamlParser.from_text(example + "\n---\n" + second).parse_many()
        self.assertEqual(len(records), 2)
        self.assertNotEqual(records[0]["metadata"]["name"], records[1]["metadata"]["name"])
        for record in records:
            self.assertEqual(record["location"]["node_id"], "ENTRYPOINT_NODE_ID")
            self.assertEqual(record["location"]["location_id"], "EVIDENCE_NODE_ID")
            self.assertEqual(record["metadata"]["recommendation"], "Enforce the required permission at this entrypoint.")
            self.assertEqual(record["metadata"]["poc"], "Reproduction steps or a test reference.")

    def test_released_sarif_conversion_limits_are_explicit(self):
        from bevor_sdk.helpers.sarif import sarif_to_bevor

        document = {
            "version": "2.1.0",
            "runs": [{
                "tool": {"driver": {"name": "external-tool", "rules": [
                    {"id": "access-control", "name": "Original title"}
                ]}},
                "results": [{
                    "ruleId": "access-control",
                    "level": "note",
                    "message": {"text": "Original evidence"},
                    "locations": [{"physicalLocation": {
                        "artifactLocation": {"uri": "src/Example.sol"},
                        "region": {"byteOffset": 10, "byteLength": 20},
                    }}],
                    "properties": {"bevor": {
                        "nodeId": "IGNORED_NODE_ID",
                        "recommendation": "Required check",
                        "poc": "Reproduction",
                    }},
                }],
            }],
        }
        [record] = sarif_to_bevor(document)
        self.assertEqual(record["metadata"], {
            "type": "access-control", "name": "Original title",
            "level": "medium", "explanation": "Original evidence",
        })
        expected_location = {
            "strategy": "physical", "uri": "src/Example.sol",
            "byteOffset": 10, "byteLength": 20,
        }
        self.assertEqual({key: record["location"][key] for key in expected_location}, expected_location)
        self.assertNotIn("node_id", record["location"])
        self.assertEqual(record["tool"], "external-tool")


if __name__ == "__main__":
    unittest.main()
