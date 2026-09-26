import json

from bashref.cli import main


def test_stats_reports_reference_counts(capsys):
    assert main(["--format", "json", "stats"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["product_version"] == "2.1.0"
    assert payload["languages"] == ["en", "fa"]
    assert payload["record_count"] >= 180
    assert payload["kinds"]["builtin"] >= 58
    assert payload["kinds"]["option"] >= 20
    assert payload["kinds"]["shopt"] >= 30
    assert payload["kinds"]["variable"] >= 20
    assert payload["kinds"]["syntax"] >= 8


def test_doctor_reports_runtime_without_network(capsys):
    assert main(["--format", "json", "doctor"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["bashref_version"] == "2.1.0"
    assert payload["python_version"]
    assert payload["platform"]
    assert payload["default_language"] in {"en", "fa"}
    assert payload["reference_records"] >= 180
    assert "bash" in payload
    assert "network_required" in payload
    assert payload["network_required"] is False
