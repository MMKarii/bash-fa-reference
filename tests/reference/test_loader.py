import json
from pathlib import Path

import pytest

from bashref.errors import CorruptReferenceError, EntryNotFoundError
from bashref.reference import ReferenceStore


def write_store(root: Path, records: list[dict]) -> None:
    ids = sorted({r["id"] for r in records})
    manifest = {
        "format_version": 1,
        "product_version": "2.0.0",
        "languages": ["en", "fa"],
        "record_count": len(ids),
        "records": ids,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    for record in records:
        lang = record["language"]
        kind_dir = "builtins" if record["kind"] == "builtin" else "concepts"
        path = root / lang / kind_dir / f"{record['name']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record), encoding="utf-8")


def record(language="en", name="printf", aliases=None):
    return {
        "id": f"builtin.{name}",
        "kind": "builtin",
        "name": name,
        "aliases": aliases or [],
        "language": language,
        "summary": "summary",
        "synopsis": name,
        "description": ["description"],
        "examples": [],
        "related": [],
        "sources": ["https://example.test/manual"],
    }


def test_default_packaged_store_resolves_id_and_name():
    store = ReferenceStore.load()
    assert store.get("builtin.printf", "en")["name"] == "printf"
    assert store.get("printf", "fa")["id"] == "builtin.printf"


def test_alias_resolves_to_same_record(tmp_path: Path):
    records = [record("en", aliases=["format"]), record("fa", aliases=["format"])]
    write_store(tmp_path, records)
    store = ReferenceStore.load(tmp_path)
    assert store.get("format", "en")["id"] == "builtin.printf"


def test_missing_entry_raises_domain_error():
    store = ReferenceStore.load()
    with pytest.raises(EntryNotFoundError):
        store.get("missing", "en")


def test_invalid_manifest_json_is_corrupt(tmp_path: Path):
    tmp_path.mkdir(exist_ok=True)
    (tmp_path / "manifest.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(CorruptReferenceError):
        ReferenceStore.load(tmp_path)


def test_ambiguous_alias_is_corrupt(tmp_path: Path):
    records = [
        record("en", "printf", ["same"]), record("fa", "printf", ["same"]),
        record("en", "echo", ["same"]), record("fa", "echo", ["same"]),
    ]
    write_store(tmp_path, records)
    with pytest.raises(CorruptReferenceError):
        ReferenceStore.load(tmp_path)


def test_list_can_filter_kind():
    store = ReferenceStore.load()
    result = store.list("builtin", "en")
    ids = [item["id"] for item in result]
    assert "builtin.printf" in ids
    assert ids == sorted(ids)
