from __future__ import annotations

import re

SITE_ROOT = "https://mmkarii.github.io/bash-fa-reference"
_KIND_DIR = {
    "builtin": "builtins",
    "syntax": "syntax",
    "expansion": "expansions",
    "option": "options",
    "shopt": "shopt",
    "variable": "variables",
    "concept": "concepts",
    "example": "examples",
}
_ID_RE = re.compile(r"^([a-z][a-z0-9-]*)\.([a-z0-9][a-z0-9_-]*)$")
_SUBCOMMANDS = "search show builtin syntax expansion option shopt variable example list lang man docs completion usage doctor"


def docs_url(record: dict | None, language: str) -> str:
    if language not in {"en", "fa"}:
        raise ValueError(f"unsupported language: {language}")
    if record is None:
        return f"{SITE_ROOT}/{language}/"
    record_id = record.get("id")
    kind = record.get("kind")
    if not isinstance(record_id, str) or not isinstance(kind, str):
        raise ValueError("record lacks trusted id/kind")
    match = _ID_RE.fullmatch(record_id)
    if not match or match.group(1) != kind or kind not in _KIND_DIR:
        raise ValueError(f"unsafe record id: {record_id}")
    slug = match.group(2)
    return f"{SITE_ROOT}/{language}/reference/generated/{_KIND_DIR[kind]}/{slug}/"


def completion_script(shell: str) -> str:
    if shell == "bash":
        return f'''_bashref() {{
    local cur="${{COMP_WORDS[COMP_CWORD]}}"
    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "{_SUBCOMMANDS}" -- "$cur") )
    fi
}}
complete -F _bashref bashref
'''
    if shell == "zsh":
        return f'''#compdef bashref
_arguments '1:command:({_SUBCOMMANDS})' '*::arg:->args'
'''
    if shell == "fish":
        lines = ["complete -c bashref -f"]
        for command in _SUBCOMMANDS.split():
            lines.append(f"complete -c bashref -n '__fish_use_subcommand' -a '{command}'")
        return "\n".join(lines) + "\n"
    raise ValueError(f"unsupported shell: {shell}")
