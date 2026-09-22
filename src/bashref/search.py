from __future__ import annotations

import difflib
import json
from importlib import resources
from pathlib import Path
from typing import Any

from .errors import CorruptReferenceError
from .reference import ReferenceStore


def _norm(value: str) -> str:
    return value.casefold().strip()


def score_entry(query: str, entry: dict) -> int:
    q = _norm(query)
    if not q:
        return 0
    record_id = _norm(str(entry.get("id", "")))
    name = _norm(str(entry.get("name", "")))
    aliases = [_norm(str(item)) for item in entry.get("aliases", [])]
    tags = [_norm(str(item)) for item in entry.get("tags", [])]
    summary = _norm(str(entry.get("summary", "")))
    description = _norm(str(entry.get("description", "")))

    if q == record_id or q == name:
        return 100
    if q in aliases:
        return 90
    if name.startswith(q) or any(alias.startswith(q) for alias in aliases):
        return 70
    if any(tag == q or tag.startswith(q) for tag in tags):
        return 50
    if q in summary.split() or q in summary:
        return 30
    if q in description.split() or q in description:
        return 10
    return 0


def _read_index(root: Any | None = None) -> dict:
    path = root if root is not None else resources.files("bashref").joinpath("data", "search-index.json")
    if isinstance(path, (str, Path)):
        path = Path(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        raise CorruptReferenceError(f"invalid search index: {exc}") from exc
    if payload.get("format_version") != 1 or not isinstance(payload.get("languages"), dict):
        raise CorruptReferenceError("unsupported search index format")
    return payload


class SearchEngine:
    def __init__(self, store: ReferenceStore, index: dict):
        self.store = store
        self.index = index

    @classmethod
    def load(cls, store: ReferenceStore, root: Any | None = None) -> "SearchEngine":
        return cls(store, _read_index(root))

    def search(self, query: str, language: str, limit: int = 20) -> list[dict]:
        if not query.strip():
            return []
        entries = self.index.get("languages", {}).get(language)
        if not isinstance(entries, list):
            raise CorruptReferenceError(f"search index missing language: {language}")
        scored = []
        for entry in entries:
            score = score_entry(query, entry)
            if score > 0:
                scored.append((score, str(entry.get("id", "")), entry))
        scored.sort(key=lambda item: (-item[0], item[1]))
        result = []
        seen: set[str] = set()
        for _, record_id, _ in scored:
            if record_id in seen:
                continue
            seen.add(record_id)
            result.append(self.store.get(record_id, language))
            if len(result) >= max(0, limit):
                break
        return result

    def suggest(self, query: str, language: str, limit: int = 3) -> list[str]:
        entries = self.index.get("languages", {}).get(language)
        if not isinstance(entries, list):
            raise CorruptReferenceError(f"search index missing language: {language}")
        candidates: list[str] = []
        for entry in entries:
            name = entry.get("name")
            if isinstance(name, str):
                candidates.append(name)
            for alias in entry.get("aliases", []):
                if isinstance(alias, str):
                    candidates.append(alias)
        return difflib.get_close_matches(query, sorted(set(candidates)), n=max(0, limit), cutoff=0.5)
