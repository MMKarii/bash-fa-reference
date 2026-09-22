from pathlib import Path

from bashref.config import load_config, save_language
from bashref.languages import resolve_language


def test_explicit_language_wins_over_config_and_persian_locale():
    assert resolve_language("en", "fa", {"LANG": "fa_IR.UTF-8"}) == "en"


def test_configured_language_wins_over_locale():
    assert resolve_language(None, "en", {"LANG": "fa_IR.UTF-8"}) == "en"


def test_persian_locale_selects_fa():
    assert resolve_language(None, None, {"LANG": "fa_IR.UTF-8"}) == "fa"


def test_non_persian_locale_falls_back_to_en():
    assert resolve_language(None, None, {"LANG": "de_DE.UTF-8"}) == "en"


def test_malformed_config_is_ignored(tmp_path: Path):
    path = tmp_path / "config.json"
    path.write_text("{bad json", encoding="utf-8")
    assert load_config(path) == {}


def test_save_language_round_trips(tmp_path: Path):
    path = tmp_path / "nested" / "config.json"
    save_language("fa", path)
    assert load_config(path) == {"language": "fa"}
