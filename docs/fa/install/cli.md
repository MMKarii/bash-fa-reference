# نصب ابزار خط فرمان Bashref

نسخه v2 ابزار `bashref` را برای جست‌وجو و مراجعه آفلاین به مرجع دوزبانه Bash اضافه می‌کند.

## نصب نسخه توسعه

تا پیش از انتشار رسمی بسته v2، از نسخه checkoutشده مخزن نصب کنید:

```bash
python -m pip install -e .
bashref --version
```

نمونه‌های اصلی:

```bash
bashref search printf
bashref builtin printf
bashref --lang fa builtin printf
bashref --format json builtin printf
bashref completion bash
```

جست‌وجو و مراجعه اصلی به شبکه نیاز ندارند و مثال‌های ذخیره‌شده در داده مرجع را اجرا نمی‌کنند.
