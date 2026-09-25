# نصب Bashref

Bashref 2.0.0 یک ابزار خط فرمان آفلاین برای مرجع دوزبانه Bash است.

## بسته Python

روش اصلی نصب قابل‌حمل:

```bash
pipx install bashref
```

همچنین می‌توانید از pip استفاده کنید:

```bash
python -m pip install bashref
```

برای نسخه checkoutشده همین مخزن:

```bash
python -m pip install -e .
```

بررسی نصب:

```bash
bashref --version
bashref search quoting
bashref --lang fa builtin printf
```

## بسته‌های Linux

Release شامل بسته‌های Debian و RPM است. این بسته‌ها CLI، داده مرجع، man page و completionهای Bash/Zsh/Fish را نصب می‌کنند.

## اجرای آفلاین

جست‌وجو و lookup اصلی به اینترنت نیاز ندارند و Bashref هیچ مثال ذخیره‌شده در مرجع را اجرا نمی‌کند.
