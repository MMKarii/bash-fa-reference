# ۵. پردازش متن و جست‌وجو

منابع اولیه روی `grep`, `awk`, `sed`, `cut`, `sort`, `uniq`, `find` و `xargs` تأکید دارند.

## grep

```bash
grep -in "error" app.log
grep -R "listen" ./config/
```

## awk

```bash
awk -F: '{print $1}' /etc/passwd
awk '{sum += $2} END {print sum}' data.txt
```

## sed

```bash
sed 's/error/ERROR/g' app.log
sed '/DEBUG/d' app.log
```

قبل از `sed -i` روی فایل مهم، نسخه پشتیبان یا Diff بگیرید.

## sort و uniq

```bash
cut -d: -f1 /etc/passwd | sort
sort events.txt | uniq -c | sort -nr
```

## find

```bash
find /var/log -type f -name '*.log'
find . -type f -size +100M -print
```

## xargs و نام فایل‌های پیچیده

به‌جای شکستن نام فایل‌ها روی whitespace، برای پردازش امن‌تر از جداکننده NUL استفاده کنید:

```bash
find . -type f -name '*.tmp' -print0 | xargs -0 -r printf '%s\n'
```

ابتدا با فرمان بی‌خطر نتیجه را مشاهده کنید، سپس عملیات تغییردهنده را جداگانه اجرا کنید.
