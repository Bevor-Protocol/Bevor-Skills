"""Export the installed CLI contract and check documented commands without running them.

This file runs standalone so documentation consumers can vendor the checker
independently of CLI releases. The imported command tree is always the installed
``bevor-cli`` package, never a hand-maintained command list.
"""

from __future__ import annotations

import argparse
import difflib
import importlib.metadata
import json
import re
import shlex
from pathlib import Path
from typing import Any

import click
import typer


def command_tree() -> click.Command:
    from bevor_cli.main import app

    return typer.main.get_command(app)


def is_group(command: click.Command) -> bool:
    # Recent Typer versions vendor Click, so isinstance(click.Group) is not portable.
    return callable(getattr(command, "list_commands", None)) and callable(
        getattr(command, "get_command", None)
    )


def _default(value: Any) -> Any:
    if callable(value):
        return "<dynamic>"
    if isinstance(value, (str, int, float, bool, list, tuple, dict)) or value is None:
        return value
    return str(value)


def export_contract(root: click.Command | None = None) -> dict[str, Any]:
    """Walk Click metadata only. No callback, authentication, or network call runs."""
    commands: list[dict[str, Any]] = []

    def walk(command: click.Command, path: list[str], parent: click.Context | None) -> None:
        ctx = click.Context(command, info_name=path[-1], parent=parent)
        parameters = []
        for param in command.get_params(ctx):
            if getattr(param, "hidden", False):
                continue
            choices = getattr(param.type, "choices", None)
            parameters.append(
                {
                    "name": param.name,
                    "kind": param.param_type_name,
                    "options": list(param.opts),
                    "secondary_options": list(getattr(param, "secondary_opts", [])),
                    "required": param.required,
                    "type": param.type.name,
                    "choices": [str(choice) for choice in choices] if choices else None,
                    "nargs": param.nargs,
                    "multiple": param.multiple,
                    "is_flag": bool(getattr(param, "is_flag", False)),
                    "default": _default(param.default),
                    "help": getattr(param, "help", None) or "",
                }
            )
        commands.append(
            {
                "path": path,
                "kind": "group" if is_group(command) else "command",
                "help": command.help or "",
                "parameters": parameters,
            }
        )
        if is_group(command):
            for name in sorted(command.list_commands(ctx)):
                child = command.get_command(ctx, name)
                if child is not None and not child.hidden:
                    walk(child, [*path, name], ctx)

    walk(root or command_tree(), ["bevor"], None)
    return {
        "schema_version": 1,
        "cli_version": importlib.metadata.version("bevor-cli"),
        "commands": commands,
    }


def serialized(contract: dict[str, Any]) -> str:
    return json.dumps(contract, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def check_command(words: list[str], contract: dict[str, Any]) -> str | None:
    """Validate paths and explicit options, accepting incomplete usage snippets.

    This deliberately does not evaluate shell substitutions, enforce required
    operands, or claim that a syntactically valid operation succeeds remotely.
    """
    commands = {tuple(command["path"]): command for command in contract["commands"]}
    path = ("bevor",)
    index = 1
    while index < len(words):
        token = words[index]
        if token in (";", "|", "||", "&&", ">", ">>", "2>", "2>&1") or token.startswith("#"):
            break
        if token in ("[OPTIONS]", "COMMAND", "[ARGS]...", "..."):
            index += 1
            continue
        command = commands[path]
        if token.startswith("-"):
            option, equals, value = token.partition("=")
            parameters = {
                name: p
                for p in command["parameters"]
                for name in p["options"] + p["secondary_options"]
            }
            parameter = parameters.get(option)
            if parameter is None:
                return f"{' '.join(path)}: unknown option {option}"
            if not parameter["is_flag"]:
                if not equals:
                    index += 1
                    if index >= len(words):
                        return f"{' '.join(path)}: {option} needs a value"
                    value = words[index]
                choices = parameter["choices"]
                placeholder = bool(re.search(r"[$<>\[\]{}]|^[A-Z][A-Z0-9_]*$", value))
                if choices and not placeholder and value not in choices:
                    return f"{' '.join(path)}: {option} value {value!r} is not one of {choices}"
            index += 1
            continue
        if command["kind"] == "group":
            child = (*path, token)
            if child not in commands:
                return f"{' '.join(path)}: unknown command {token}"
            path = child
        index += 1
    return None


def snippets(text: str) -> list[tuple[int, str]]:
    """Read inline code and shell fences, not prose or commands inside Python."""
    found: list[tuple[int, str]] = []
    fence: str | None = None
    shell = False
    pending = ""
    start = 0
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"\s*(`{3,}|~{3,})(.*)$", line)
        if marker:
            if fence is None:
                fence = marker.group(1)[0]
                shell = marker.group(2).strip().split(" ")[0] in (
                    "bash",
                    "sh",
                    "shell",
                    "zsh",
                    "console",
                )
            elif marker.group(1)[0] == fence:
                if pending:
                    found.append((start, pending))
                fence, pending, shell = None, "", False
            continue
        if fence is not None:
            if not shell:
                continue
            if not pending:
                start = number
            pending += line.rstrip().removesuffix("\\") + " "
            if not line.rstrip().endswith("\\"):
                found.append((start, pending))
                pending = ""
        else:
            for match in re.finditer(r"`([^`\n]+)`", line):
                found.append((number, match.group(1)))
    return found


def check_documents(paths: list[Path], contract: dict[str, Any]) -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    files: set[Path] = set()
    for path in paths:
        if path.is_dir():
            files.update(p for p in path.rglob("*") if p.suffix in (".md", ".mdx"))
        elif path.is_file():
            files.add(path)
        else:
            errors.append(f"{path}: path does not exist")
    for path in sorted(files):
        for line, snippet in snippets(path.read_text()):
            if not re.search(r"\bbevor(?:\s|$)", snippet):
                continue
            try:
                lexer = shlex.shlex(snippet, posix=True, punctuation_chars=";&|")
                lexer.whitespace_split = True
                words = list(lexer)
            except ValueError as exc:
                errors.append(f"{path}:{line}: cannot parse command: {exc}")
                continue
            for index, token in enumerate(words):
                if token != "bevor":
                    continue
                # Avoid quoted prose and package names that merely mention Bevor.
                if (
                    index
                    and words[index - 1] not in (";", "&&", "||", "|", "$", "do", "then")
                    and "=" not in words[index - 1]
                ):
                    continue
                count += 1
                error = check_command(words[index:], contract)
                if error:
                    errors.append(f"{path}:{line}: {error}")
    return errors, count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    export = sub.add_parser("export", help="Write deterministic installed CLI metadata")
    export.add_argument("--output", type=Path, required=True)
    check = sub.add_parser("check", help="Detect installed CLI drift from a saved contract")
    check.add_argument("--snapshot", type=Path, required=True)
    docs = sub.add_parser(
        "check-docs", help="Check documented command paths and options, without running them"
    )
    docs.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args()
    contract = export_contract()
    if args.operation == "export":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized(contract))
        print(
            f"Exported {len(contract['commands'])} commands from bevor-cli {contract['cli_version']}"
        )
    elif args.operation == "check":
        expected = args.snapshot.read_text()
        actual = serialized(contract)
        if expected != actual:
            print(
                "".join(
                    difflib.unified_diff(
                        expected.splitlines(True),
                        actual.splitlines(True),
                        fromfile=str(args.snapshot),
                        tofile="installed CLI",
                    )
                )
            )
            raise SystemExit(1)
        print("CLI contract matches")
    else:
        errors, count = check_documents(args.paths, contract)
        for error in errors:
            print(error)
        print(
            f"Checked {count} command snippets against bevor-cli {contract['cli_version']}; {len(errors)} errors"
        )
        if errors or not count:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
