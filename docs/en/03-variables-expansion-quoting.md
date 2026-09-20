# 3. Variables, Expansion, and Quoting

Many Bash failures originate in expansion and unquoted variables.

```bash
name="Ali"
printf 'Hello %s\n' "$name"
path="${HOME}/projects"
```

## Parameters

- `$1`, `$2`: positional arguments
- `$#`: argument count
- `"$@"`: all arguments while preserving argument boundaries
- `$?`: previous command status
- `$$`: current shell PID

## Defaults and required values

```bash
mode="${1:-status}"
required="${API_URL:?API_URL is required}"
```

## Command substitution

```bash
today="$(date +%F)"
```

## Quoting

Single quotes keep almost everything literal. Double quotes still allow parameter and command substitution while preventing unwanted word splitting and glob expansion. Variables that may contain spaces or wildcard characters normally belong inside double quotes.

## Arithmetic

```bash
count=4
((count += 1))
printf '%d\n' "$count"
```

Use a more suitable language or tool for complex numeric or structured-data work.
