from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "bevor"
SKILL_MD = SKILL / "SKILL.md"
DOCS = [SKILL_MD, *(SKILL / "references").glob("*.md")]


def frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md has no valid frontmatter block")
    return match.group(1)


def folded_value(data: str, key: str) -> str:
    lines = data.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(f"{key}:"))
    first = lines[start].split(":", 1)[1].strip()
    if first not in {">-", ">", "|-", "|"}:
        return first.strip('"')
    value = []
    for line in lines[start + 1 :]:
        if line and not line.startswith(" "):
            break
        value.append(line.strip())
    return " ".join(part for part in value if part)


class SkillStructureTests(unittest.TestCase):
    def test_frontmatter(self) -> None:
        data = frontmatter(SKILL_MD.read_text())
        self.assertRegex(data, r"(?m)^name: bevor$")
        description = folded_value(data, "description")
        self.assertLessEqual(len(description), 1024)
        self.assertNotIn("<", description)
        self.assertNotIn(">", description)

    def test_implicit_invocation_is_enabled(self) -> None:
        metadata = (SKILL / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("$bevor", metadata)

    def test_references(self) -> None:
        actual = {path.name for path in (SKILL / "references").glob("*.md")}
        self.assertEqual({"graph-navigation.md", "new-commits.md", "findings.md"}, actual)

    def test_relative_markdown_links_resolve(self) -> None:
        for path in DOCS:
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                clean = target.split("#", 1)[0]
                self.assertTrue((path.parent / clean).exists(), f"broken link in {path}: {target}")


class ScopeTests(unittest.TestCase):
    """The skill works through the CLI only and never pins versions or deployments."""

    def test_no_version_pins(self) -> None:
        for path in DOCS:
            self.assertIsNone(re.search(r"\b\d+\.\d+\.\d+", path.read_text()), f"version pin in {path}")

    def test_no_sdk_or_api_pointers(self) -> None:
        for path in DOCS:
            text = path.read_text()
            for word in ("SDK", "bevor_sdk", "bevor-sdk", "REST API", "api.bevor.io"):
                self.assertNotIn(word, text, f"{word} in {path}")

    def test_no_deployment_overrides(self) -> None:
        for path in DOCS:
            text = path.read_text()
            self.assertNotIn("BEVOR_API_URL", text, path)
            self.assertNotIn("BEVOR_APP_URL", text, path)

    def test_finding_writes_name_their_tool(self) -> None:
        for path in DOCS:
            for command in re.findall(r"bevor findings (?:import|add)\b[^`\n]*", path.read_text()):
                if " --help" in command or command.rstrip().endswith(("add", "import")):
                    continue
                if "results.sarif" in command:  # SARIF carries its producer's name.
                    continue
                self.assertIn("--tool", command, f"{path}: {command}")


class TriggerDatasetTests(unittest.TestCase):
    def test_trigger_dataset_has_broad_unnamed_cases(self) -> None:
        cases = json.loads((ROOT / "tests" / "trigger_cases.json").read_text())
        positives = [case for case in cases if case["expected"]]
        negatives = [case for case in cases if not case["expected"]]
        unnamed = [case for case in positives if "bevor" not in case["prompt"].lower()]
        self.assertGreaterEqual(len(positives), 20)
        self.assertGreaterEqual(len(negatives), 10)
        self.assertGreaterEqual(len(unnamed), len(positives) // 2)


if __name__ == "__main__":
    unittest.main()
