import pytest

from bashref.cli import main
from bashref.completion import completion_script, docs_url


def record(record_id="builtin.printf", kind="builtin", name="printf"):
    return {"id": record_id, "kind": kind, "name": name}


def test_bash_completion_has_function_and_registration():
    text = completion_script("bash")
    assert "_bashref" in text
    assert "complete -F _bashref bashref" in text


def test_zsh_completion_has_compdef():
    assert "#compdef bashref" in completion_script("zsh")


def test_fish_completion_targets_bashref():
    assert "complete -c bashref" in completion_script("fish")


def test_unknown_completion_shell_rejected():
    with pytest.raises(ValueError):
        completion_script("powershell")


def test_docs_url_maps_record_to_fixed_project_path():
    assert docs_url(record(), "en") == "https://mmkarii.github.io/bash-fa-reference/en/reference/generated/builtins/printf/"


def test_docs_url_root_without_record():
    assert docs_url(None, "fa") == "https://mmkarii.github.io/bash-fa-reference/fa/"


def test_docs_url_rejects_untrusted_record_id():
    with pytest.raises(ValueError):
        docs_url(record("builtin.../../../evil", "builtin", "evil"), "en")


def test_cli_completion_prints_script(capsys):
    assert main(["completion", "bash"]) == 0
    assert "complete -F _bashref bashref" in capsys.readouterr().out


def test_cli_docs_prints_validated_url(capsys):
    assert main(["--lang", "en", "docs", "printf"]) == 0
    assert capsys.readouterr().out.strip().endswith("/en/reference/generated/builtins/printf/")


def test_cli_man_without_system_man_prints_page_name(monkeypatch, capsys):
    monkeypatch.setattr("bashref.cli.shutil.which", lambda name: None)
    assert main(["man", "printf"]) == 0
    assert capsys.readouterr().out.strip() == "bashref-reference"
