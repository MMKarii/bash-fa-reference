from __future__ import annotations

from . import __version__


def usage_summary() -> str:
    return f"""Bashref {__version__}
Usage: bashref [GLOBAL OPTIONS] COMMAND [ARGS]

COMMON COMMANDS:
  search QUERY         Search all reference records
  show TOPIC           Show a record by name, alias, or canonical ID
  builtin NAME         Show a Bash builtin
  syntax NAME          Show a shell-syntax record
  expansion NAME       Show an expansion record
  option NAME          Show a shell option
  shopt NAME           Show a shopt option
  variable NAME        Show a Bash variable
  example NAME         Show a worked example
  list CATEGORY        List records by category
  doctor               Diagnose the installed Bashref runtime and data
  docs [TOPIC]         Print the matching documentation URL
  man [TOPIC]          Open the installed manual page when available
  completion SHELL     Generate Bash, Zsh, or Fish completion
  lang {fa,en}         Save the preferred language
  usage                Print this summary

GLOBAL OPTIONS:
  --lang {fa,en}       Select output language
  --format {text,json} Select human or machine-readable output
  --no-color           Disable terminal color
  --width N            Set text output width
  --version            Print Bashref version

EXAMPLES:
  bashref search quoting
  bashref builtin printf
  bashref option pipefail
  bashref --lang fa builtin read
  bashref --format json search array
  bashref doctor

SEE ALSO:
  bashref man
  bashref docs
  https://mmkarii.github.io/bash-fa-reference/
"""
