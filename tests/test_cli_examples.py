"""Checks the skill's examples against the installed CLI's own parser; no credentials or requests."""
from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HAS_CLI = importlib.util.find_spec("bevor_cli") is not None


def _yaml_examples(path: Path) -> list[str]:
    text = path.read_text()
    fenced = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)
    heredocs = re.findall(r"<<'EOF'\n(.*?)\nEOF", text, re.DOTALL)
    return fenced + heredocs


@unittest.skipUnless(HAS_CLI, "Install the Bevor CLI to check the examples against its parser")
class CliExamples(unittest.TestCase):
    def test_finding_yaml_examples_parse(self) -> None:
        from bevor_cli.findings_yaml import FindingYamlParser

        examples = _yaml_examples(ROOT / "skills/bevor/SKILL.md") + _yaml_examples(
            ROOT / "skills/bevor/references/findings.md"
        )
        self.assertEqual(len(examples), 2)
        with patch("bevor_cli.configuration.creds.Credentials.load", side_effect=AssertionError("credential access")):
            findings = [f for example in examples for f in FindingYamlParser.from_text(example).parse_many()]
        self.assertEqual(len(findings), 3)
        for finding in findings:
            self.assertIsInstance(finding["location"], str)
        self.assertEqual(findings[0]["level"], "high")


if __name__ == "__main__":
    unittest.main()
