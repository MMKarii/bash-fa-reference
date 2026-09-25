from __future__ import annotations

import argparse
import os
import shutil
import sys
import subprocess
import webbrowser
import json

from . import __version__
from .commands import LOOKUP_COMMAND_KINDS, list_records, lookup_record, search_records
from .completion import completion_script, docs_url
from .config import load_config, save_language
from .diagnostics import doctor_report, reference_stats
from .errors import CorruptReferenceError, EntryNotFoundError
from .languages import resolve_language
from .reference import ReferenceStore
from .renderer import render_error, render_record, render_records
from .search import SearchEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bashref", description="Offline bilingual Bash reference")
    parser.add_argument("--version", action="version", version=f"bashref {__version__}")
    parser.add_argument("--lang", choices=("fa", "en"), default=None)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--width", type=int, default=None)

    sub = parser.add_subparsers(dest="command")

    search = sub.add_parser("search", help="Search the reference")
    search.add_argument("query")

    show = sub.add_parser("show", help="Show a reference entry")
    show.add_argument("name")

    for command in LOOKUP_COMMAND_KINDS:
        lookup = sub.add_parser(command, help=f"Show a {command} reference entry")
        lookup.add_argument("name")

    listing = sub.add_parser("list", help="List reference entries")
    listing.add_argument(
        "category",
        choices=("all", "builtin", "syntax", "expansion", "option", "shopt", "variable", "concept", "example"),
    )

    lang = sub.add_parser("lang", help="Save the preferred language")
    lang.add_argument("language", choices=("fa", "en"))

    completion = sub.add_parser("completion", help="Generate shell completion")
    completion.add_argument("shell", choices=("bash", "zsh", "fish"))

    man = sub.add_parser("man", help="Open the Bashref manual")
    man.add_argument("topic", nargs="?")

    docs = sub.add_parser("docs", help="Print or open documentation URL")
    docs.add_argument("topic", nargs="?")
    docs.add_argument("--open", action="store_true", dest="open_url")

    sub.add_parser("stats", help="Show reference coverage statistics")
    sub.add_parser("doctor", help="Show local Bashref runtime diagnostics")
    return parser


def _write_error(code: int, message: str, suggestions: list[str], output_format: str) -> int:
    sys.stderr.write(render_error(code, message, suggestions, format=output_format))
    return code


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "lang":
        save_language(args.language)
        print(f"language: {args.language}")
        return 0

    if args.command == "completion":
        sys.stdout.write(completion_script(args.shell))
        return 0

    if args.command == "man":
        page = "bashref-reference" if args.topic else "bashref"
        if shutil.which("man") is None:
            print(page)
            return 0
        return subprocess.run(["man", page], check=False).returncode

    config = load_config()
    language = resolve_language(args.lang, config.get("language"), os.environ)
    width = args.width if args.width is not None else shutil.get_terminal_size((80, 24)).columns
    width = max(10, width)
    color = not args.no_color and sys.stdout.isatty()

    try:
        store = ReferenceStore.load()
        engine = SearchEngine.load(store)
        if args.command == "stats":
            payload = reference_stats(store)
            if args.format == "json":
                print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
            else:
                print(f"bashref {payload['product_version']}")
                print(f"records: {payload['record_count']}")
                for kind, count in payload["kinds"].items():
                    print(f"{kind}: {count}")
            return 0
        if args.command == "doctor":
            payload = doctor_report(store)
            if args.format == "json":
                print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
            else:
                print(f"bashref: {payload['bashref_version']}")
                print(f"python: {payload['python_version']}")
                print(f"platform: {payload['platform']}")
                print(f"language: {payload['default_language']}")
                print(f"reference records: {payload['reference_records']}")
                bash = payload["bash"]
                print(f"bash: {bash['version'] if bash else 'not found'}")
                print("network required: no")
            return 0
        if args.command == "docs":
            record = store.get(args.topic, language) if args.topic else None
            url = docs_url(record, language)
            print(url)
            if args.open_url:
                webbrowser.open(url)
            return 0
        if args.command == "search":
            records = search_records(engine, args.query, language)
            sys.stdout.write(render_records(records, format=args.format, color=color, width=width))
            return 0
        if args.command == "list":
            records = list_records(store, args.category, language)
            sys.stdout.write(render_records(records, format=args.format, color=color, width=width))
            return 0
        record = lookup_record(store, args.command, args.name, language)
        sys.stdout.write(render_record(record, format=args.format, color=color, width=width))
        return 0
    except EntryNotFoundError as exc:
        suggestions = []
        try:
            suggestions = engine.suggest(exc.query, language)
        except Exception:
            suggestions = []
        return _write_error(3, str(exc), suggestions, args.format)
    except CorruptReferenceError as exc:
        return _write_error(4, str(exc), [], args.format)
    except Exception as exc:
        return _write_error(1, f"internal error: {type(exc).__name__}: {exc}", [], args.format)
