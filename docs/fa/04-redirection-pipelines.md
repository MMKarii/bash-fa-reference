# ۴. Redirection، Pipeline و Exit Status

قدرت مدل یونیکس از اتصال ابزارهای کوچک به یکدیگر می‌آید.

## جریان‌های استاندارد

- stdin: ورودی استاندارد
- stdout: خروجی استاندارد
- stderr: خروجی خطا

```bash
printf '%s\n' "ok" > result.txt
printf '%s\n' "next" >> result.txt
command 2> errors.log
command > output.log 2>&1
```

## Pipeline

```bash
journalctl -u ssh | grep -i "failed"
```

در Pipeline، خروجی stdout یک مرحله وارد stdin مرحله بعد می‌شود.

```bash
set -o pipefail
producer | filter | consumer
status=$?
```

با `pipefail`، شکست یک جزء Pipeline می‌تواند در وضعیت نهایی منعکس شود.

## Exit status

قرارداد عمومی: صفر یعنی موفقیت و مقدار غیرصفر یعنی خطا یا نتیجه خاص.

```bash
if grep -q "READY" app.log; then
  printf '%s\n' "ready"
fi
```

## نکته مهم درباره `set -e`

`set -e` رفتار ساده‌ای مثل «توقف روی هر خطا» ندارد و استثناهای نحوی متعددی دارد. در مسیرهای بحرانی، نتیجه فرمان را صریحاً بررسی کنید و `set -e` را یک لایه کمکی بدانید، نه کل استراتژی خطا.
