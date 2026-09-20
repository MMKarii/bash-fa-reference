# 7. Bash Scripting Fundamentals

## Shebang

```bash
#!/usr/bin/env bash
```

If the deployment policy requires an exact interpreter path, use it explicitly.

## Conditionals

```bash
if [[ "${1:-}" == "start" ]]; then
  printf '%s\n' "starting"
elif [[ "${1:-}" == "stop" ]]; then
  printf '%s\n' "stopping"
else
  printf 'usage: %s {start|stop}\n' "$0" >&2
  exit 2
fi
```

## Loops

```bash
for file in *.log; do
  [[ -e "$file" ]] || continue
  printf '%s\n' "$file"
done
```

## Arrays

```bash
servers=(db1 db2 db3)
for server in "${servers[@]}"; do
  printf '%s\n' "$server"
done
```

## Functions

```bash
sum() {
  local a="$1" b="$2"
  printf '%d\n' "$((a + b))"
}
```

For medium scripts, structure behavior as functions and end with a single `main "$@"` entry point.
