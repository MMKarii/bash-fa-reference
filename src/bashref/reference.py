from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any, Iterable

from .errors import CorruptReferenceError, EntryNotFoundError


def _children(node: Any) -> Iterable[Any]:
    try:
        return tuple(node.iterdir())
    except (AttributeError, OSError) as exc:
        raise CorruptReferenceError(f"cannot read reference directory: {exc}") from exc


def _iter_json(node: Any) -> Iterable[Any]:
    for child in sorted(_children(node), key=lambda item: item.name):
        if child.is_dir():
            yield from _iter_json(child)
        elif child.name.endswith(".json"):
            yield child


def _read_json(path: Any) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        raise CorruptReferenceError(f"invalid reference JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CorruptReferenceError(f"reference JSON must be an object: {path}")
    return data


class ReferenceStore:
    def __init__(self, records: dict[str, dict[str, dict]], indexes: dict[str, dict[str, str]]):
        self._records = records
        self._indexes = indexes

    @classmethod
    def load(cls, root: Path | Any | None = None) -> "ReferenceStore":
        data_root = root if root is not None else resources.files("bashref").joinpath("data")
        manifest_path = data_root.joinpath("manifest.json")
        manifest = _read_json(manifest_path)
        if manifest.get("format_version") != 1:
            raise CorruptReferenceError("unsupported reference manifest format")
        languages = manifest.get("languages")
        if languages != ["en", "fa"]:
            raise CorruptReferenceError("reference manifest languages must be ['en', 'fa']")
        declared_ids = manifest.get("records")
        if not isinstance(declared_ids, list) or not all(isinstance(x, str) for x in declared_ids):
            raise CorruptReferenceError("reference manifest records must be a string list")

        records: dict[str, dict[str, dict]] = {"en": {}, "fa": {}}
        indexes: dict[str, dict[str, str]] = {"en": {}, "fa": {}}

        for language in languages:
            language_root = data_root.joinpath(language)
            for path in _iter_json(language_root):
                record = _read_json(path)
                record_id = record.get("id")
                name = record.get("name")
                record_language = record.get("language")
                aliases = record.get("aliases", [])
                if not isinstance(record_id, str) or not isinstance(name, str) or record_language != language:
                    raise CorruptReferenceError(f"invalid record identity in {path}")
                if not isinstance(aliases, list) or not all(isinstance(x, str) for x in aliases):
                    raise CorruptReferenceError(f"invalid aliases in {path}")
                if record_id in records[language]:
                    raise CorruptReferenceError(f"duplicate record id: {record_id}")
                records[language][record_id] = record
                keys = {record_id.casefold(), name.casefold(), *(alias.casefold() for alias in aliases)}
                for key in keys:
                    existing = indexes[language].get(key)
                    if existing is not None and existing != record_id:
                        raise CorruptReferenceError(f"ambiguous lookup key {key!r}: {existing}, {record_id}")
                    indexes[language][key] = record_id

        actual_ids = sorted(records["en"])
        if actual_ids != sorted(records["fa"]):
            raise CorruptReferenceError("packaged English/Persian record IDs do not match")
        if actual_ids != sorted(declared_ids):
            raise CorruptReferenceError("manifest record IDs do not match packaged records")
        if manifest.get("record_count") != len(actual_ids):
            raise CorruptReferenceError("manifest record count does not match packaged records")
        return cls(records, indexes)

    def get(self, query: str, language: str) -> dict:
        if language not in self._indexes:
            raise CorruptReferenceError(f"unsupported language: {language}")
        record_id = self._indexes[language].get(query.casefold())
        if record_id is None:
            raise EntryNotFoundError(query, language)
        return self._records[language][record_id]

    def list(self, kind: str | None, language: str) -> list[dict]:
        if language not in self._records:
            raise CorruptReferenceError(f"unsupported language: {language}")
        result = self._records[language].values()
        if kind is not None:
            result = (record for record in result if record.get("kind") == kind)
        return sorted(result, key=lambda record: record["id"])
