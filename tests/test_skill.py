from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "bevor"
SKILL_MD = SKILL / "SKILL.md"


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
    def test_frontmatter_and_selector_contract(self) -> None:
        text = SKILL_MD.read_text()
        data = frontmatter(text)
        self.assertRegex(data, r"(?m)^name: bevor$")
        description = folded_value(data, "description")
        self.assertTrue(description.startswith("Use when the user asks to"))
        self.assertLessEqual(len(description), 1024)
        self.assertIn("even if Bevor is not named", description)
        self.assertIn("web3 security CI/CD", description)
        self.assertIn("current Solidity graph", description)
        self.assertNotIn("<", description)
        self.assertNotIn(">", description)
        self.assertNotIn("TODO", text)

    def test_implicit_invocation_is_enabled(self) -> None:
        metadata = (SKILL / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("$bevor", metadata)

    def test_required_references_exist(self) -> None:
        required = {
            "cli-command-tree.md",
            "cli-workflows.md",
            "graph-navigation.md",
            "context-reuse.md",
            "findings-exchange.md",
            "sdk.md",
            "api.md",
            "ci-cd.md",
            "bevor-action.md",
            "tool-orchestration.md",
            "platform-dashboard.md",
            "docs-map.md",
            "security-review.md",
        }
        actual = {path.name for path in (SKILL / "references").glob("*.md")}
        self.assertEqual(required, actual)

    def test_relative_markdown_links_resolve(self) -> None:
        for path in [SKILL_MD, *(SKILL / "references").glob("*.md")]:
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                clean = target.split("#", 1)[0]
                self.assertTrue((path.parent / clean).exists(), f"broken link in {path}: {target}")

    def test_old_audit_only_contract_is_removed(self) -> None:
        text = SKILL_MD.read_text()
        self.assertNotIn("graph only", text.lower())
        self.assertNotIn("bevor codes", text)
        self.assertNotIn("pre-approved", text)
        self.assertNotIn("ABSOLUTELY FORBIDDEN", text)


class ContractTests(unittest.TestCase):
    def test_cli_snapshot_is_documented(self) -> None:
        commands = {
            line.strip()
            for line in (ROOT / "tests" / "fixtures" / "cli_commands.txt").read_text().splitlines()
            if line.strip() and not line.startswith("#")
        }
        reference = (SKILL / "references" / "cli-command-tree.md").read_text()
        missing = [
            command
            for command in sorted(commands)
            if not re.search(rf"`{re.escape(command)}(?:`|[ ])", reference)
        ]
        self.assertEqual([], missing)
        self.assertNotIn("bevor analysis list", commands)

    def test_remote_boundaries_are_explicit(self) -> None:
        text = SKILL_MD.read_text()
        for operation in ("upload", "paid analysis", "commit", "acknowledgement", "merge", "deletion"):
            self.assertIn(operation, text)
        self.assertIn("Automatic selection never authorizes", text)

    def test_ci_invariants_are_present(self) -> None:
        ci = (SKILL / "references" / "ci-cd.md").read_text()
        action = (SKILL / "references" / "bevor-action.md").read_text()
        tools = (SKILL / "references" / "tool-orchestration.md").read_text()
        self.assertIn("Record", ci)
        self.assertIn("Import", ci)
        self.assertIn("Analyze", ci)
        self.assertLess(
            ci.index("Record the run and import findings"),
            ci.index("Enforce the repository's security gate"),
        )
        self.assertIn("repeat key", ci)
        self.assertIn("untrusted fork", ci)
        self.assertIn("no record-only mode", action)
        self.assertIn("first duplicate anchors", tools)
        self.assertIn("Unique findings with validated proofs", tools)

    def test_trigger_dataset_has_broad_unnamed_cases(self) -> None:
        cases = json.loads((ROOT / "tests" / "trigger_cases.json").read_text())
        positives = [case for case in cases if case["expected"]]
        negatives = [case for case in cases if not case["expected"]]
        unnamed = [case for case in positives if "bevor" not in case["prompt"].lower()]
        self.assertGreaterEqual(len(positives), 20)
        self.assertGreaterEqual(len(negatives), 10)
        self.assertGreaterEqual(len(unnamed), len(positives) // 2)
        self.assertGreaterEqual(len({case["class"] for case in positives}), 8)

    def test_workflow_dataset_covers_required_decisions(self) -> None:
        cases = json.loads((ROOT / "tests" / "workflow_cases.json").read_text())
        names = {case["name"] for case in cases}
        self.assertTrue(
            {
                "exact context before scan",
                "graph impact",
                "SARIF submission",
                "existing CI job",
                "CI retry",
                "Slither first",
                "Python integration",
                "non-Python integration",
                "acknowledgement",
                "savings",
            }.issubset(names)
        )
        for case in cases:
            self.assertTrue(case["must"])
            self.assertTrue(case["must_not"])


if __name__ == "__main__":
    unittest.main()
