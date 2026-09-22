from __future__ import annotations

from .reference import ReferenceStore
from .search import SearchEngine

LOOKUP_COMMAND_KINDS = {
    "builtin": "builtin",
    "syntax": "syntax",
    "expansion": "expansion",
    "option": "option",
    "shopt": "shopt",
    "variable": "variable",
    "example": "example",
}


def lookup_record(store: ReferenceStore, command: str, name: str, language: str) -> dict:
    if command == "show":
        return store.get(name, language)
    kind = LOOKUP_COMMAND_KINDS[command]
    query = name if "." in name else f"{kind}.{name}"
    return store.get(query, language)


def search_records(engine: SearchEngine, query: str, language: str) -> list[dict]:
    return engine.search(query, language)


def list_records(store: ReferenceStore, category: str, language: str) -> list[dict]:
    kind = None if category == "all" else category
    return store.list(kind, language)
