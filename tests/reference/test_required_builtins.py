import json
from pathlib import Path

REQUIRED = {
    "alias","bg","bind","break","builtin","caller","cd","command","compgen",
    "complete","compopt","continue","declare","dirs","disown","echo","enable",
    "eval","exec","exit","export","false","fc","fg","getopts","hash","help",
    "history","jobs","kill","let","local","logout","mapfile","popd","printf",
    "pushd","pwd","read","readarray","readonly","return","set","shift","shopt",
    "source","suspend","test","times","trap","true","type","typeset","ulimit",
    "umask","unalias","unset","wait",
}


def records(lang: str) -> dict[str, dict]:
    root = Path("reference") / lang / "builtins"
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in root.glob("*.json")
    }


def test_required_builtin_files_exist_in_both_languages():
    assert REQUIRED - set(records("en")) == set()
    assert REQUIRED - set(records("fa")) == set()


def test_required_builtin_ids_and_languages_match_files():
    for lang in ("en", "fa"):
        for name, record in records(lang).items():
            assert record["id"] == f"builtin.{name}"
            assert record["kind"] == "builtin"
            assert record["language"] == lang
