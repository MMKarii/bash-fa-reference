from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

try:
    from tools.validate_reference import validate_tree
except ModuleNotFoundError:
    from validate_reference import validate_tree

KIND_DIR = {
    "builtin": "builtins",
    "syntax": "syntax",
    "expansion": "expansions",
    "option": "options",
    "shopt": "shopt",
    "variable": "variables",
    "concept": "concepts",
    "example": "examples",
}


def record_doc_path(record: dict) -> Path:
    slug = str(record["id"]).split(".", 1)[1]
    return Path(KIND_DIR[str(record["kind"])]) / f"{slug}.md"


def _lines(items: list) -> str:
    rendered = []
    for item in items:
        if isinstance(item, dict):
            title = str(item.get("title", "Example"))
            code = str(item.get("code", ""))
            rendered.append(f"### {title}\n\n```bash\n{code}\n```")
        else:
            rendered.append(f"- {item}")
    return "\n\n".join(rendered)


def render_markdown_record(record: dict) -> str:
    summary = str(record.get("summary", ""))
    front = (
        "---\n"
        "generated: true\n"
        f"record_id: {record['id']}\n"
        f"reference_kind: {record['kind']}\n"
        f"description: {json.dumps(summary, ensure_ascii=False)}\n"
        "---\n\n"
    )
    sections = [
        f"# {record['name']}\n\n{summary}",
        f"## Synopsis\n\n```bash\n{record.get('synopsis', '')}\n```",
        "## Description\n\n" + "\n\n".join(str(x) for x in record.get("description", [])),
    ]
    field_titles = [
        ("parameters", "Parameters"),
        ("exit_status", "Exit status"),
        ("examples", "Examples"),
        ("pitfalls", "Pitfalls"),
        ("portability", "Portability"),
        ("security", "Security"),
    ]
    for field, title in field_titles:
        values = record.get(field, [])
        if values:
            sections.append(f"## {title}\n\n{_lines(values)}")
    related = record.get("related", [])
    if related:
        sections.append("## Related\n\n" + "\n".join(f"- `{item}`" for item in related))
    sources = record.get("sources", [])
    if sources:
        sections.append("## Sources\n\n" + "\n".join(f"- [{url}]({url})" for url in sources))
    return front + "\n\n".join(sections) + "\n"


def _load_records(root: Path, language: str) -> list[dict]:
    records = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((root / language).rglob("*.json"))
    ]
    records.sort(key=lambda item: item["id"])
    return records


def _index(language: str, records: list[dict]) -> str:
    fa = language == "fa"
    title = "فهرست کامل Reference Guide" if fa else "Complete Reference Guide Index"
    intro = (
        "این فهرست به‌صورت خودکار از داده مرجع canonical تولید می‌شود."
        if fa else
        "This index is generated automatically from the canonical reference data."
    )
    groups: dict[str, list[dict]] = {}
    for record in records:
        groups.setdefault(record["kind"], []).append(record)
    parts = [f"# {title}\n\n{intro}"]
    for kind in sorted(groups):
        parts.append(f"## {kind}")
        links = []
        for record in groups[kind]:
            path = record_doc_path(record).with_suffix("").as_posix()
            links.append(f"- [{record['name']}]({path}/) — {record['summary']}")
        parts.append("\n".join(links))
    return "\n\n".join(parts) + "\n"


def build_docs_reference(source_root: Path, docs_root: Path) -> None:
    issues = validate_tree(source_root)
    if issues:
        raise ValueError("invalid reference tree:\n" + "\n".join(issues))
    for language in ("en", "fa"):
        records = _load_records(source_root, language)
        generated = docs_root / language / "reference" / "generated"
        if generated.exists():
            shutil.rmtree(generated)
        generated.mkdir(parents=True, exist_ok=True)
        (generated / "index.md").write_text(_index(language, records), encoding="utf-8")
        for record in records:
            target = generated / record_doc_path(record)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_markdown_record(record), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("reference"))
    parser.add_argument("--docs-root", type=Path, default=Path("docs"))
    args = parser.parse_args()
    build_docs_reference(args.source, args.docs_root)
    print("Generated bilingual web Reference Guide.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
