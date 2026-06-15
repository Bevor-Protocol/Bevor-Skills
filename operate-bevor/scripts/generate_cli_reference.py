#!/usr/bin/env python3
"""Generate a Markdown reference from the registered Bevor Typer command tree."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import click


def _summary(value: str | None) -> str:
    lines: list[str] = []
    for line in (value or "").strip().splitlines():
        if not line.strip():
            break
        lines.append(line.strip())
    return " ".join(lines)


def _usage(param: click.Parameter) -> str:
    if isinstance(param, click.Option):
        names = ", ".join(param.opts + param.secondary_opts)
        suffix = ""
        if not param.is_flag:
            suffix = f" {param.make_metavar()}"
        required = " (required)" if param.required else ""
        return f"`{names}{suffix}`{required}"

    metavar = param.make_metavar()
    required = " (required)" if param.required else ""
    return f"`{metavar}`{required}"


def _walk(group: click.Group, prefix: tuple[str, ...]) -> list[tuple[tuple[str, ...], click.Command]]:
    rows: list[tuple[tuple[str, ...], click.Command]] = []
    for name in sorted(group.commands):
        command = group.commands[name]
        path = (*prefix, name)
        rows.append((path, command))
        if isinstance(command, click.Group):
            rows.extend(_walk(command, path))
    return rows


def render(cli_root: Path) -> str:
    sys.path.insert(0, str(cli_root))

    from typer.main import get_command
    from bevor_cli.main import app
    from bevor_cli.commands.analyses.findings.common import FINDING_LEVELS, FINDING_TYPES

    root = get_command(app)
    if not isinstance(root, click.Group):
        raise RuntimeError("bevor_cli.main:app did not resolve to a Click group")

    lines = [
        "# Bevor CLI Surface",
        "",
        "> Generated from `bevor_cli.main:app`; do not edit manually.",
        "",
        "Regenerate with `operate-bevor/scripts/generate_cli_reference.py` after CLI registration or",
        "option changes.",
        "",
    ]

    root_params = [p for p in root.params if p.name != "help"]
    if root_params:
        lines.extend(["## Global Options", ""])
        for param in root_params:
            detail = _summary(getattr(param, "help", None))
            line = f"- {_usage(param)}"
            if detail:
                line += f": {detail}"
            lines.append(line)
        lines.append("")

    lines.extend(
        [
            "## Finding Import Values",
            "",
            f"- Types: {', '.join(f'`{value}`' for value in FINDING_TYPES)}",
            f"- Levels: {', '.join(f'`{value}`' for value in FINDING_LEVELS)}",
            "",
        ]
    )

    for path, command in _walk(root, ("bevor",)):
        lines.extend([f"## `{' '.join(path)}`", ""])
        help_text = _summary(command.help or command.short_help)
        if help_text:
            lines.extend([help_text, ""])

        params = [p for p in command.params if p.name != "help"]
        if params:
            lines.extend(["Parameters:", ""])
            for param in params:
                detail = _summary(getattr(param, "help", None))
                line = f"- {_usage(param)}"
                if detail:
                    line += f": {detail}"
                lines.append(line)
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli-root", type=Path, required=True, help="Directory containing bevor_cli/")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when the output file differs from the registered CLI surface.",
    )
    args = parser.parse_args()

    output = args.output.resolve()
    generated = render(args.cli_root.resolve())
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != generated:
            print(f"CLI reference is stale: {output}", file=sys.stderr)
            raise SystemExit(1)
        print(f"CLI reference is current: {output}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generated, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
