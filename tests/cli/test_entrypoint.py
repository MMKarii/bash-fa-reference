from bashref import __version__
from bashref.cli import main


def test_version_constant_is_v2_development_line():
    assert __version__ == "2.0.0"


def test_main_version_prints_version(capsys):
    assert main(["--version"]) == 0
    assert capsys.readouterr().out.strip() == "bashref 2.0.0"
