#!/usr/bin/env python3
"""Refresh or check this skill's release contract without making remote requests."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
from pathlib import Path

from cli_contract import check_documents, export_contract, serialized

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "skills" / "bevor"
SNAPSHOT = ROOT / "tests" / "fixtures" / "cli_contract.json"
COMMANDS = ROOT / "tests" / "fixtures" / "cli_commands.txt"
RELEASE = ROOT / "tests" / "fixtures" / "cli-release.txt"
DEPENDENCIES = ROOT / "tests" / "fixtures" / "cli-dependencies.txt"
REFERENCE = SKILL / "references" / "cli-command-tree.md"


def render(contract: dict) -> tuple[str, str]:
    rows = [
        "# CLI command tree", "",
        f"Generated from installed bevor-cli {contract['cli_version']} (released package).",
        "Regenerate with `python skills/bevor/scripts/check_cli_contract.py --update`.",
        "No authentication or command callback runs during generation.", "",
        "This is syntax metadata, not a guarantee of remote behavior. See the workflow references for write boundaries and verified recipes.",
        "The release help can still say staged even though the finding writes apply immediately.", "",
        "| Command | Available options |", "| --- | --- |",
    ]
    names = []
    for command in contract["commands"]:
        name = " ".join(command["path"])
        if name == "bevor":
            continue
        names.append(name)
        flags = [flag for param in command["parameters"] if param["kind"] == "option"
                 for flag in param["options"] + param["secondary_options"] if flag != "--help"]
        rows.append("| `" + name + "` | " + ", ".join("`" + f + "`" for f in flags) + " |")
    return "\n".join(rows) + "\n", "# Generated from the installed CLI; do not edit.\n" + "\n".join(names) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="Regenerate release snapshot and command reference")
    parser.add_argument("--docs-only", action="store_true", help="Validate examples against a newer installed release")
    args = parser.parse_args()
    contract = export_contract()
    reference, names = render(contract)
    if args.update:
        SNAPSHOT.write_text(serialized(contract))
        REFERENCE.write_text(reference)
        COMMANDS.write_text(names)
        RELEASE.write_text(contract["cli_version"] + "\n")
        DEPENDENCIES.write_text(
            "# Metadata renderer versions used for this contract.\n"
            + "".join(f"{name}=={importlib.metadata.version(name)}\n" for name in ("typer", "click"))
        )
    elif not args.docs_only:
        if RELEASE.read_text().strip() != contract["cli_version"]:
            print("Installed CLI differs from the reviewed release pin.")
            return 1
        if SNAPSHOT.read_text() != serialized(contract):
            print("CLI contract drift: install the pinned release, or review and regenerate with --update.")
            return 1
        if REFERENCE.read_text() != reference or COMMANDS.read_text() != names:
            print("Generated command reference differs from installed source. Regenerate with --update.")
            return 1
    errors, count = check_documents([SKILL / "SKILL.md", SKILL / "references"], contract)
    for error in errors:
        print(error)
    print(f"Validated {count} snippets against CLI {contract['cli_version']}; {len(errors)} errors")
    return int(bool(errors) or not count)


if __name__ == "__main__":
    raise SystemExit(main())
