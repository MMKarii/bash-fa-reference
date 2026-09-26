from bashref import __version__
from bashref.cli import main


def test_version_constant_matches_v21_release_line():
    assert __version__ == "2.1.0"


def test_main_version_prints_version(capsys):
    assert main(["--version"]) == 0
    assert capsys.readouterr().out.strip() == f"bashref {__version__}"
