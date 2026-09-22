from bashref.reference import ReferenceStore
from bashref.search import SearchEngine, score_entry


def entry(record_id, name, aliases=None, tags=None, summary="", description=""):
    return {
        "id": record_id,
        "name": name,
        "aliases": aliases or [],
        "tags": tags or [],
        "summary": summary,
        "description": description,
    }


def test_exact_name_scores_above_alias_and_prefix():
    exact = score_entry("printf", entry("builtin.printf", "printf"))
    alias = score_entry("printf", entry("builtin.echo", "echo", aliases=["printf"]))
    prefix = score_entry("pri", entry("builtin.printf", "printf"))
    assert exact > alias > prefix


def test_tag_scores_above_description():
    tag = score_entry("format", entry("builtin.printf", "printf", tags=["format"]))
    body = score_entry("format", entry("builtin.echo", "echo", description="format output"))
    assert tag > body


def test_packaged_search_returns_printf_once():
    engine = SearchEngine.load(ReferenceStore.load())
    results = engine.search("printf", "en")
    assert [item["id"] for item in results] == ["builtin.printf"]


def test_zero_results_is_empty_list():
    engine = SearchEngine.load(ReferenceStore.load())
    assert engine.search("definitely-not-present", "en") == []


def test_typo_suggests_printf():
    engine = SearchEngine.load(ReferenceStore.load())
    assert "printf" in engine.suggest("pritnf", "en")
