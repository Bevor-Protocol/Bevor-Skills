"""Checks the skill's examples against the installed CLI's own parser; no credentials or requests."""
from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HAS_CLI = importlib.util.find_spec("bevor_cli") is not None


@unittest.skipUnless(HAS_CLI, "Install the Bevor CLI to check the examples against its parser")
class CliExamples(unittest.TestCase):
    def test_finding_yaml_example_parses(self) -> None:
        from bevor_cli.findings_yaml import FindingYamlParser

        text = (ROOT / "skills/bevor/references/findings.md").read_text()
        examples = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)
        self.assertEqual(len(examples), 1)
        with patch("bevor_cli.configuration.creds.Credentials.load", side_effect=AssertionError("credential access")):
            finding = FindingYamlParser.from_text(examples[0]).parse()
        self.assertEqual(finding["location"]["strategy"], "node_id")
        self.assertEqual(finding["entrypoint"]["strategy"], "node_id")
        self.assertEqual(finding["level"], "high")


if __name__ == "__main__":
    unittest.main()
