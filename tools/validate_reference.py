from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED_FIELDS = {
    "id": str,
    "kind": str,
    "name": str,
    "language": str,
    "summary": str,
    "synopsis": str,
    "description": list,
    "examples": list,
    "related": list,
    "sources": list,
}
OPTIONAL_LIST_FIELDS = {"aliases", "parameters", "exit_status", "pitfalls", "portability", "security", "tags"}
ALLOWED_LANGUAGES = {"en", "fa"}
ALLOWED_KINDS = {"builtin", "syntax", "expansion", "option", "shopt", "variable", "concept", "example"}
ID_RE = re.compile(r"^[a-z][a-z0-9-]*\\.[A-Za-z0-9][A-Za-z0-9._-]*$")


def validate_record(data: dict, expected_language: str | None = None) -> list[str]:
    issues: list[str] = []
    if not isinstance(data, dict):
        return ["record must be a JSON object"]

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            issues.append(f"missing required field: {field}")
            continue
        if not isinstance(data[field], expected_type):
            issues.append(f"field {field} must be {expected_type.__name__}")

    record_id = data.get("id")
    if isinstance(record_id, str) and not ID_RE.fullmatch(record_id):
        issues.append(f"invalid id: {record_id}")

    kind = data.get("kind")
    if isinstance(kind, str) and kind not in ALLOWED_KINDS:
        issues.append(f"unsupported kind: {kind}")
    if isinstance(record_id, str) and isinstance(kind, str) and not record_id.startswith(kind + "."):
        issues.append(f"id {record_id} must start with {kind}.")

    language = data.get("language")
    if isinstance(language, str) and language not in ALLOWED_LANGUAGES:
        issues.append(f"unsupported language: {language}")
    if expected_language and language != expected_language:
        issues.append(f"language {language!r} does not match tree {expected_language!r}")

    for field in OPTIONAL_LIST_FIELDS:
        if field in data and not isinstance(data[field], list):
            issues.append(f"field {field} must be list")

    description = data.get("description")
    if isinstance(description, list) and not all(isinstance(item, str) for item in description):
        issues.append("description entries must be strings")
    related = data.get("related")
    if isinstance(related, list) and not all(isinstance(item, str) for item in related):
        issues.append("related entries must be strings")
    sources = data.get("sources")
    if isinstance(sources, list):
        for source in sources:
            if not isinstance(source, str):
                issues.append("source entries must be strings")
                continue
            parsed = urlsplit(source)
            if parsed.scheme != "https" or not parsed.netloc:
                issues.append(f"source must be an https URL: {source}")
    return issues


def validate_tree(root: Path) -> list[str]:
    issues: list[str] = []
    ids_by_language: dict[str, set[str]] = {lang: set() for lang in ALLOWED_LANGUAGES}
    all_records: dict[str, dict[str, dict]] = {lang: {} for lang in ALLOWED_LANGUAGES}

    for language in sorted(ALLOWED_LANGUAGES):
        language_root = root / language
        if not language_root.exists():
            issues.append(f"missing language tree: {language}")
            continue
        for path in sorted(language_root.rglob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                issues.append(f"{path}: invalid JSON: {exc}")
                continue
            for issue in validate_record(data, expected_language=language):
                issues.append(f"{path}: {issue}")
            record_id = data.get("id")
            if isinstance(record_id, str):
                if record_id in ids_by_language[language]:
                    issues.append(f"{path}: duplicate id: {record_id}")
                ids_by_language[language].add(record_id)
                all_records[language][record_id] = data

    en_ids = ids_by_language["en"]
    fa_ids = ids_by_language["fa"]
    if en_ids != fa_ids:
        missing_fa = sorted(en_ids - fa_ids)
        missing_en = sorted(fa_ids - en_ids)
        issues.append(f"bilingual parity mismatch: missing fa={missing_fa}, missing en={missing_en}")

    known_ids = en_ids | fa_ids
    for language, records in all_records.items():
        for record_id, data in records.items():
            for related in data.get("related", []):
                if related not in known_ids:
                    issues.append(f"{language}:{record_id}: related id not found: {related}")
    return issues


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "reference"
    issues = validate_tree(root)
    if issues:
        print("Reference validation issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    count = sum(1 for _ in (root / "en").rglob("*.json"))
    print(f"Reference validation passed for {count} bilingual record(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
