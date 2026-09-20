# ۳. متغیرها، Expansion و Quoting

بخش مهمی از خطاهای Bash از Expansion و Quote نکردن متغیرها ناشی می‌شود.

```bash
name="Ali"
printf 'Hello %s\n' "$name"
path="${HOME}/projects"
```

## پارامترها

- `$1`, `$2` آرگومان‌های positional
- `$#` تعداد آرگومان‌ها
- `"$@"` همه آرگومان‌ها با حفظ مرز هر آرگومان
- `$?` وضعیت خروجی فرمان قبلی
- `$$` PID شل جاری

## مقدار پیش‌فرض

```bash
mode="${1:-status}"
required="${API_URL:?API_URL is required}"
```

## Command substitution

```bash
today="$(date +%F)"
```

## Quoting

- Single quotes تقریباً همه چیز را literal نگه می‌دارند.
- Double quotes Expansion متغیر و command substitution را نگه می‌دارند، اما word splitting و globbing ناخواسته را مهار می‌کنند.
- متغیرهایی که ممکن است فاصله یا wildcard داشته باشند را معمولاً Quote کنید: `"$file"`.

## Arithmetic

```bash
count=4
((count += 1))
printf '%d\n' "$count"
```

برای داده‌های پیچیده یا عدد اعشاری، ابزار یا زبان مناسب‌تری انتخاب کنید.
