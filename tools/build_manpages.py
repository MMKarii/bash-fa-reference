from __future__ import annotations

import argparse
import json
import shutil
import re
from pathlib import Path

try:
    from tools.validate_reference import validate_tree
except ModuleNotFoundError:
    from validate_reference import validate_tree


def project_version() -> str:
    init_path = Path(__file__).resolve().parents[1] / "src" / "bashref" / "__init__.py"
    text = init_path.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    if not match:
        raise ValueError("cannot determine Bashref version")
    return match.group(1)


def escape_roff(text: str) -> str:
    text = text.replace("\\", r"\e")
    lines: list[str] = []
    for line in text.splitlines() or [""]:
        if line.startswith((".", "'")):
            line = r"\&" + line
        lines.append(line.replace("-", r"\-"))
    return "\n".join(lines)


def _section(title: str, body: str) -> str:
    return f".SH {title}\n{escape_roff(body)}\n"


def render_reference_manpage(record: dict) -> str:
    name = str(record["name"])
    summary = str(record["summary"])
    synopsis = str(record.get("synopsis", ""))
    description = "\n\n".join(str(x) for x in record.get("description", []))
    sources = "\n".join(str(x) for x in record.get("sources", []))
    parts = [
        f'.TH "BASHREF-REFERENCE" "5" "September 26, 2026" "Bashref {project_version()}" "File Formats and Conventions"\n',
        _section("NAME", f"{name} - {summary}"),
        _section("SYNOPSIS", synopsis),
        _section("DESCRIPTION", description),
    ]
    examples = record.get("examples", [])
    if examples:
        rendered = []
        for example in examples:
            if isinstance(example, dict):
                title = str(example.get("title", "Example"))
                code = str(example.get("code", ""))
                rendered.append(f"{title}\n{code}".strip())
            else:
                rendered.append(str(example))
        parts.append(_section("EXAMPLES", "\n\n".join(rendered)))
    portability = record.get("portability", [])
    if portability:
        parts.append(_section("PORTABILITY", "\n\n".join(str(x) for x in portability)))
    security = record.get("security", [])
    if security:
        parts.append(_section("SECURITY", "\n\n".join(str(x) for x in security)))
    parts.append(_section("SEE ALSO", sources))
    return "".join(parts)


def render_cli_manpage() -> str:
    return f"""\
.TH "BASHREF" "1" "September 26, 2026" "Bashref {project_version()}" "User Commands"
.SH NAME
bashref \\- offline bilingual Bash reference
.SH SYNOPSIS
bashref [--lang fa|en] [--format text|json] COMMAND [ARGUMENTS]
.SH DESCRIPTION
Bashref provides offline lookup and search for a structured Persian and English Bash reference.
It never executes examples stored in the reference database.
.SH COMMANDS
search, show, builtin, syntax, expansion, option, shopt, variable, example, list, lang, man, docs, completion, stats, doctor.
.SH EXIT STATUS
0 means success, 1 an internal error, 2 a command-line usage error, 3 a missing reference entry, and 4 corrupt reference data.
.SH SEE ALSO
bashref-reference(5), bash(1)
"""


def render_overview_manpage(records: list[dict]) -> str:
    by_kind: dict[str, list[str]] = {}
    for record in records:
        by_kind.setdefault(str(record["kind"]), []).append(str(record["name"]))
    body = []
    for kind in sorted(by_kind):
        body.append(kind.upper())
        body.append(", ".join(sorted(by_kind[kind], key=str.casefold)))
        body.append("")
    return (
        f'.TH "BASHREF-REFERENCE" "5" "September 26, 2026" "Bashref {project_version()}" "File Formats and Conventions"\n'
        + _section("NAME", "bashref-reference - Bash language and builtin reference index")
        + _section("DESCRIPTION", "Canonical Bashref reference topics generated from bilingual JSON records.")
        + _section("REFERENCE INDEX", "\n".join(body).rstrip())
        + _section("SEE ALSO", "bashref(1), bash(1), https://www.gnu.org/software/bash/manual/bash.html")
    )


def load_records(source_root: Path, language: str = "en") -> list[dict]:
    records = []
    for path in sorted((source_root / language).rglob("*.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    records.sort(key=lambda item: item["id"])
    return records


def build_manpages(source_root: Path, output_root: Path) -> None:
    issues = validate_tree(source_root)
    if issues:
        raise ValueError("invalid reference tree:\n" + "\n".join(issues))
    generated = output_root / "generated"
    if generated.exists():
        shutil.rmtree(generated)
    generated.mkdir(parents=True, exist_ok=True)
    records = load_records(source_root, "en")
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "bashref.1").write_text(render_cli_manpage(), encoding="utf-8")
    (output_root / "bashref-reference.5").write_text(render_overview_manpage(records), encoding="utf-8")
    for record in records:
        slug = record["id"].replace(".", "-")
        (generated / f"bashref-{slug}.5").write_text(
            render_reference_manpage(record),
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("reference"))
    parser.add_argument("--output", type=Path, default=Path("man"))
    args = parser.parse_args()
    build_manpages(args.source, args.output)
    print("Generated Bashref man pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
