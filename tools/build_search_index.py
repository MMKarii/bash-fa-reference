from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from tools.validate_reference import validate_tree
except ModuleNotFoundError:  # direct script execution
    from validate_reference import validate_tree


def _entry(record: dict) -> dict:
    description = record.get("description", [])
    if isinstance(description, list):
        description_text = " ".join(str(item) for item in description)
    else:
        description_text = str(description)
    return {
        "id": record["id"],
        "name": record["name"],
        "aliases": list(record.get("aliases", [])),
        "tags": list(record.get("tags", [])),
        "summary": str(record.get("summary", "")),
        "description": description_text,
    }


def build_search_index(source_root: Path, output_path: Path) -> dict:
    issues = validate_tree(source_root)
    if issues:
        raise ValueError("invalid reference tree:\n" + "\n".join(issues))
    languages: dict[str, list[dict]] = {}
    for language in ("en", "fa"):
        entries = []
        for path in sorted((source_root / language).rglob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            entries.append(_entry(record))
        entries.sort(key=lambda item: item["id"])
        languages[language] = entries
    payload = {"format_version": 1, "languages": languages}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("reference"))
    parser.add_argument("--output", type=Path, default=Path("src/bashref/data/search-index.json"))
    args = parser.parse_args()
    payload = build_search_index(args.source, args.output)
    count = len(payload["languages"]["en"])
    print(f"Built search index for {count} bilingual record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
