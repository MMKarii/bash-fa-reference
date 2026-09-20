# ۶. پردازه‌ها، Jobها و Signalها

## مشاهده پردازه

```bash
ps aux
top
```

در محیط‌های دارای `htop`، نمایش تعاملی خواناتری در دسترس است.

## Job control

```bash
long_task &
jobs
fg %1
bg %1
```

Job control بیشتر برای Shell تعاملی مناسب است.

## Signal

```bash
kill -TERM "$pid"
```

به‌صورت پیش‌فرض از Signal قابل مدیریت مثل `TERM` شروع کنید. `KILL` فرصت cleanup را از پردازه می‌گیرد و باید گزینه نهایی باشد.

## Cleanup با trap

```bash
tmp="$(mktemp)"
cleanup() {
  rm -f -- "$tmp"
}
trap cleanup EXIT INT TERM
```

`trap` برای حذف فایل موقت، آزادکردن Lock و ثبت پایان اجرای اسکریپت مفید است.

## PID قابل اعتماد

از patternهایی مثل `ps | grep` برای تصمیم‌های حساس دوری کنید. در سرویس‌های systemd، از ابزار مدیریت همان سرویس استفاده کنید؛ در برنامه‌های خودتان PID یا handle معتبر را نگه دارید.
