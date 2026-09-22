from __future__ import annotations

import json
import os
from pathlib import Path

VALID_LANGUAGES = {"en", "fa"}


def config_path(environ: dict[str, str] | None = None) -> Path:
    env = os.environ if environ is None else environ
    appdata = env.get("APPDATA")
    if os.name == "nt" and appdata:
        return Path(appdata) / "bashref" / "config.json"
    xdg = env.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "bashref" / "config.json"
    return Path.home() / ".config" / "bashref" / "config.json"


def load_config(path: Path | None = None) -> dict[str, str]:
    target = config_path() if path is None else path
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    language = data.get("language")
    if language not in VALID_LANGUAGES:
        return {}
    return {"language": language}


def save_language(language: str, path: Path | None = None) -> None:
    if language not in VALID_LANGUAGES:
        raise ValueError(f"unsupported language: {language}")
    target = config_path() if path is None else path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"language": language}, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
