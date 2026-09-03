#!/usr/bin/env python3
"""Compare the pinned Bevor CLI command snapshot with generated release docs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


GROUP_FILES = ("project", "team", "sessions", "finding", "agent", "chat")
PINNED_VERSION = "0.1.0"


def headings(path: Path, level: int) -> list[str]:
    pattern = re.compile(rf"^{'#' * level} `([^`]+)`$")
    return [match.group(1) for line in path.read_text().splitlines() if (match := pattern.match(line))]


def source_commands(api_root: Path) -> set[str]:
    docs = api_root / "packages" / "cli" / "docs"
    if not docs.is_dir():
        raise ValueError(f"CLI generated docs not found: {docs}")

    commands = {f"bevor {name}" for name in headings(docs / "root.mdx", 2)}

    for group in GROUP_FILES:
        commands.update(f"bevor {group} {name}" for name in headings(docs / f"{group}.mdx", 2))

    code_top = headings(docs / "code.mdx", 2)
    commands.update(f"bevor code {name}" for name in code_top if name != "node")
    commands.update(f"bevor code node {name}" for name in headings(docs / "code.mdx", 3))

    analysis_top = headings(docs / "analysis.mdx", 2)
    commands.update(f"bevor analysis {name}" for name in analysis_top if name != "delete")
    commands.update(
        f"bevor analysis delete {name}" for name in headings(docs / "analysis.mdx", 3)
    )
    return commands


def pinned_commands(repo_root: Path) -> set[str]:
    fixture = repo_root / "tests" / "fixtures" / "cli_commands.txt"
    return {
        line.strip()
        for line in fixture.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def project_version(path: Path) -> str:
    match = re.search(r'^version = "([^"]+)"$', path.read_text(), re.MULTILINE)
    if not match:
        raise ValueError(f"Version not found in {path}")
    return match.group(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("api_root", type=Path, help="Path to the bevorai-api repository")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[3]
    api_root = args.api_root.resolve()

    cli_version = project_version(api_root / "packages" / "cli" / "pyproject.toml")
    sdk_version = project_version(api_root / "packages" / "bevor-sdk" / "pyproject.toml")
    if cli_version != PINNED_VERSION or sdk_version != PINNED_VERSION:
        print(
            f"version drift: cli={cli_version}, sdk={sdk_version}, expected={PINNED_VERSION}",
            file=sys.stderr,
        )
        return 1

    expected = pinned_commands(repo_root)
    actual = source_commands(api_root)
    missing = sorted(actual - expected)
    removed = sorted(expected - actual)
    if missing or removed:
        if missing:
            print("new commands not in snapshot:", *missing, sep="\n  ", file=sys.stderr)
        if removed:
            print("snapshot commands absent from source:", *removed, sep="\n  ", file=sys.stderr)
        return 1

    reference = (repo_root / "skills" / "bevor" / "references" / "cli-command-tree.md").read_text()
    undocumented = sorted(
        command
        for command in expected
        if not re.search(rf"`{re.escape(command)}(?:`|[ ])", reference)
    )
    if undocumented:
        print("commands absent from reference:", *undocumented, sep="\n  ", file=sys.stderr)
        return 1

    print(f"CLI contract matches {len(actual)} commands at version {PINNED_VERSION}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
