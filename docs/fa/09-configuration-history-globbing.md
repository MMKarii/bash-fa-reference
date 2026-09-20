# ۹. پیکربندی Bash، History، Alias و Globbing

## فایل‌های Startup

رفتار دقیق Startup به interactive/login بودن Shell وابسته است. فایل‌های رایج شامل `.bash_profile`, `.profile` و `.bashrc` هستند. قبل از انتقال تنظیمات بین توزیع‌ها، ترتیب Startup همان محیط را بررسی کنید.

## Alias

```bash
alias ll='ls -lah'
```

Alias برای راحتی تعاملی است، نه مکانیزم ایمنی قابل اتکا در اسکریپت‌ها. اسکریپت باید خودش رفتار امن را پیاده کند.

## History

```bash
history
HISTCONTROL=ignoreboth
```

History می‌تواند داده حساس را ثبت کند. Secretها را روی command line قرار ندهید و از روش‌های امن مدیریت credential استفاده کنید.

## Globbing

```bash
printf '%s\n' *.log
```

Globbing توسط Shell انجام می‌شود. در Loopها نبود Match را هم در نظر بگیرید. گزینه‌هایی مثل `nullglob` و `failglob` رفتار را تغییر می‌دهند:

```bash
shopt -s nullglob
files=(*.log)
```

تنظیمات `shopt` را در اسکریپت صریح و محلی نگه دارید.
