# ۸. اسکریپت‌نویسی مقاوم

نسخه‌های منبع `set -euo pipefail` و `trap` را به‌عنوان Best Practice معرفی می‌کنند. این توصیه مفید است، اما باید semantics هر گزینه را فهمید.

```bash
set -u
set -o pipefail
```

- `-u`: استفاده از متغیر تعریف‌نشده را خطا می‌کند.
- `pipefail`: خطای مراحل Pipeline را قابل مشاهده‌تر می‌کند.
- `-e`: در contextهای مختلف رفتار استثنایی دارد؛ برای همه پروژه‌ها «حالت ایمن خودکار» نیست.

## بررسی صریح عملیات بحرانی

```bash
if ! cp -- "$src" "$dst"; then
  printf 'copy failed: %s -> %s\n' "$src" "$dst" >&2
  exit 1
fi
```

## فایل موقت

```bash
tmp="$(mktemp)"
trap 'rm -f -- "$tmp"' EXIT
```

## ورودی کاربر

ورودی را به‌عنوان داده نگه دارید، نه بخشی از command string. از ساخت فرمان با `eval` یا concatenation ورودی ناشناس دوری کنید. آرگومان‌ها را Quote کنید و برای مقادیر محدود allowlist تعریف کنید.

## Logging

```bash
log() {
  printf '%s %s\n' "$(date -Is)" "$*" >&2
}
```

اطلاعات حساس مثل Token و Password را Log نکنید.
