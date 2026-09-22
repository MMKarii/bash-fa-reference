import json

from bashref.cli import main
from bashref.errors import CorruptReferenceError


def test_missing_direct_lookup_returns_three(capsys):
    assert main(["--lang", "en", "builtin", "missing"]) == 3
    assert "not found" in capsys.readouterr().err


def test_missing_direct_lookup_json_error_contract(capsys):
    assert main(["--lang", "en", "--format", "json", "builtin", "missing"]) == 3
    payload = json.loads(capsys.readouterr().err)
    assert payload["code"] == 3
    assert payload["error"] is True


def test_unknown_command_returns_two(capsys):
    assert main(["does-not-exist"]) == 2
    assert "invalid choice" in capsys.readouterr().err


def test_corrupt_store_returns_four(monkeypatch, capsys):
    def broken_load(*args, **kwargs):
        raise CorruptReferenceError("broken manifest")

    monkeypatch.setattr("bashref.cli.ReferenceStore.load", broken_load)
    assert main(["search", "printf"]) == 4
    assert "broken manifest" in capsys.readouterr().err
