from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .core import PromptError, PromptLibrary

VERSION = "1.0.0"


def _pairs(items: list[str]) -> dict[str, str]:
    result = {}
    for item in items:
        if "=" not in item:
            raise PromptError(f"Expected KEY=VALUE, got: {item}")
        key, value = item.split("=", 1)
        if not key:
            raise PromptError("Variable name cannot be empty")
        result[key] = value
    return result


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="prompt-library", description="Search and render a local prompt library")
    p.add_argument("--version", action="version", version=f"prompt-library {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    p.add_argument("--dir", default="prompts", help="Prompt directory (default: prompts)")
    sub = p.add_subparsers(dest="command", required=True)
    ls = sub.add_parser("list", help="List prompts")
    ls.add_argument("--tag", action="append", default=[])
    find = sub.add_parser("search", help="Search prompt metadata")
    find.add_argument("query", nargs="?", default="")
    find.add_argument("--tag", action="append", default=[])
    show = sub.add_parser("show", help="Show prompt metadata and template")
    show.add_argument("name")
    render = sub.add_parser("render", help="Render a prompt")
    render.add_argument("name")
    render.add_argument("--var", action="append", default=[], metavar="KEY=VALUE")
    render.add_argument("--allow-missing", action="store_true")
    sub.add_parser("validate", help="Validate every prompt file")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    lib = PromptLibrary(Path(args.dir))
    try:
        if args.command in {"list", "search"}:
            query = getattr(args, "query", "")
            items = lib.search(query, args.tag)
            for item in items:
                print(f"{item.name}\tv{item.version}\t{item.title}\t[{', '.join(item.tags)}]")
            return 0
        if args.command == "show":
            item = lib.load(args.name)
            print(json.dumps({"name": item.name, "title": item.title, "description": item.description, "tags": item.tags, "version": item.version, "variables": item.variables, "template": item.template}, ensure_ascii=False, indent=2))
            return 0
        if args.command == "render":
            print(lib.load(args.name).render(_pairs(args.var), strict=not args.allow_missing))
            return 0
        errors = lib.validate()
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print(f"OK: {len(lib.all())} prompt(s) valid")
        return 0
    except PromptError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
