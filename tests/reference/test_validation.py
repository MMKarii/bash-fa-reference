import json
from pathlib import Path

from tools.validate_reference import validate_record, validate_tree


def sample_record(language: str = "en") -> dict:
    return {
        "id": "builtin.printf",
        "kind": "builtin",
        "name": "printf",
        "aliases": [],
        "language": language,
        "summary": "Format and print data.",
        "synopsis": "printf [-v var] format [arguments]",
        "description": ["Format arguments according to a format string."],
        "examples": [],
        "related": [],
        "sources": ["https://www.gnu.org/software/bash/manual/bash.html#Bash-Builtins"],
    }


def write_record(root: Path, language: str, name: str, record: dict) -> None:
    path = root / language / "builtins" / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")


def test_valid_record_passes():
    assert validate_record(sample_record()) == []


def test_missing_required_field_fails():
    record = sample_record()
    del record["synopsis"]
    assert any("synopsis" in issue for issue in validate_record(record))


def test_bilingual_id_parity_is_required(tmp_path: Path):
    en = sample_record("en")
    fa = sample_record("fa")
    fa["id"] = "builtin.echo"
    fa["name"] = "echo"
    write_record(tmp_path, "en", "printf", en)
    write_record(tmp_path, "fa", "echo", fa)
    issues = validate_tree(tmp_path)
    assert any("bilingual parity" in issue for issue in issues)


def test_language_must_match_tree(tmp_path: Path):
    write_record(tmp_path, "en", "printf", sample_record("fa"))
    write_record(tmp_path, "fa", "printf", sample_record("fa"))
    issues = validate_tree(tmp_path)
    assert any("language" in issue for issue in issues)
