import json

from bashref.cli import main
from bashref.errors import CorruptReferenceError


def test_no_args_prints_concise_usage_summary(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "COMMON COMMANDS" in out
    assert "bashref search quoting" in out
    assert "SEE ALSO" in out


def test_usage_subcommand_prints_same_summary(capsys):
    assert main(["usage"]) == 0
    usage = capsys.readouterr().out
    assert "COMMON COMMANDS" in usage
    assert "EXAMPLES" in usage


def test_doctor_json_reports_healthy_reference(capsys):
    assert main(["--lang", "en", "--format", "json", "doctor"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ok"
    assert payload["bashref_version"] == "2.1.0"
    assert payload["language"] == "en"
    assert payload["reference_records"] >= 97
    assert payload["reference_languages"] == ["en", "fa"]


def test_doctor_returns_corrupt_data_exit_code(monkeypatch, capsys):
    def broken_load(*args, **kwargs):
        raise CorruptReferenceError("broken reference store")

    monkeypatch.setattr("bashref.cli.ReferenceStore.load", broken_load)
    assert main(["--format", "json", "doctor"]) == 4
    payload = json.loads(capsys.readouterr().err)
    assert payload["code"] == 4
    assert "broken reference store" in payload["message"]
