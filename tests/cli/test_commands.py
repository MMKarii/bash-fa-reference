import json

from bashref.cli import main


def test_search_printf_text(capsys):
    assert main(["--lang", "en", "search", "printf"]) == 0
    out = capsys.readouterr().out
    assert "printf" in out
    assert "Format and print data" in out


def test_builtin_printf_direct_lookup(capsys):
    assert main(["--lang", "en", "builtin", "printf"]) == 0
    assert "printf" in capsys.readouterr().out


def test_json_lookup_is_machine_readable(capsys):
    assert main(["--lang", "en", "--format", "json", "builtin", "printf"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["id"] == "builtin.printf"


def test_empty_search_result_is_successful_json(capsys):
    assert main(["--lang", "en", "--format", "json", "search", "zzzz-no-match"]) == 0
    assert json.loads(capsys.readouterr().out) == []


def test_list_builtin_returns_records(capsys):
    assert main(["--lang", "en", "--format", "json", "list", "builtin"]) == 0
    payload = json.loads(capsys.readouterr().out)
    ids = [item["id"] for item in payload]
    assert "builtin.printf" in ids
    assert ids == sorted(ids)


def test_lang_command_persists(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    assert main(["lang", "fa"]) == 0
    assert "fa" in capsys.readouterr().out
    assert json.loads((tmp_path / "bashref" / "config.json").read_text())["language"] == "fa"
