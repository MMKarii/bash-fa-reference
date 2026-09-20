# ۷. مبانی اسکریپت‌نویسی Bash

## Shebang

```bash
#!/usr/bin/env bash
```

اگر اسکریپت دقیقاً به مسیر `/bin/bash` وابسته است، همان مسیر را صریح بنویسید. انتخاب به سیاست محیط Deployment وابسته است.

## شرط

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

## حلقه

```bash
for file in *.log; do
  [[ -e "$file" ]] || continue
  printf '%s\n' "$file"
done
```

## آرایه

```bash
servers=(db1 db2 db3)
for server in "${servers[@]}"; do
  printf '%s\n' "$server"
done
```

## Function

```bash
sum() {
  local a="$1" b="$2"
  printf '%d\n' "$((a + b))"
}
```

## `main`

برای اسکریپت‌های متوسط، قراردادن منطق در Functionها و پایان دادن فایل با `main "$@"` خوانایی و تست را بهتر می‌کند.
