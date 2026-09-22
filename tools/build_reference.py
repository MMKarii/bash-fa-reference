from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from tools.validate_reference import validate_tree


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def build_reference(source_root: Path, output_root: Path, version: str) -> dict:
    issues = validate_tree(source_root)
    if issues:
        raise ValueError("invalid reference tree:\n" + "\n".join(issues))

    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    ids: set[str] = set()
    for language in ("en", "fa"):
        language_root = source_root / language
        for source in sorted(language_root.rglob("*.json")):
            record = json.loads(source.read_text(encoding="utf-8"))
            ids.add(record["id"])
            relative = source.relative_to(language_root)
            _write_json(output_root / language / relative, record)

    manifest = {
        "format_version": 1,
        "product_version": version,
        "languages": ["en", "fa"],
        "record_count": len(ids),
        "records": sorted(ids),
    }
    _write_json(output_root / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("reference"))
    parser.add_argument("--output", type=Path, default=Path("src/bashref/data"))
    parser.add_argument("--version", default="2.0.0")
    args = parser.parse_args()
    manifest = build_reference(args.source, args.output, args.version)
    print(f"Built {manifest['record_count']} bilingual reference record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
