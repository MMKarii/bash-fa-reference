# 8. Robust Bash Scripting

The supplied sources recommend `set -euo pipefail` and `trap`. The intent is useful, but each option has specific semantics.

```bash
set -u
set -o pipefail
```

- `-u`: reports expansion of unset variables as an error in many contexts.
- `pipefail`: exposes failures from earlier elements of a pipeline.
- `-e`: has syntax-dependent exceptions and is not a universal "safe mode."

## Explicit error handling

```bash
if ! cp -- "$src" "$dst"; then
  printf 'copy failed: %s -> %s\n' "$src" "$dst" >&2
  exit 1
fi
```

## Temporary files

```bash
tmp="$(mktemp)"
trap 'rm -f -- "$tmp"' EXIT
```

## User input

Keep input as data rather than assembling it into command strings. Avoid `eval` with untrusted values. Quote arguments and use an allowlist when only a small set of values is valid.

## Logging

```bash
log() {
  printf '%s %s\n' "$(date -Is)" "$*" >&2
}
```

Do not log passwords, tokens, cookies, or private keys.
