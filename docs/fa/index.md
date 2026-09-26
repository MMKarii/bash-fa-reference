# Bashref: مرجع Bash از ترمینال تا راهنمای کامل

**Bashref 2.1.0** یک پروژه آزاد و متن‌باز برای Bash است که CLI آفلاین، **Reference Guide دوزبانه با ۲۱۴ رکورد**، man pageهای سیستمی، بسته‌های قابل نصب و Professional Guide چهارده‌فصلی را در یک مجموعه ارائه می‌کند.

[دریافت Bashref 2.1.0](download/index.md){ .md-button }

## اخبار

- **Bashref 2.1.0:** مرجع ساختاریافته فارسی/انگلیسی به ۲۱۴ رکورد رسیده و پوشش `set -o`، `shopt`، variableهای Bash و compound commandها گسترده‌تر شده است.
- **Diagnostics آفلاین:** `bashref stats` پوشش مجموعه مرجع و `bashref doctor` وضعیت runtime محلی را بدون نیاز به شبکه گزارش می‌کند.
- **مستندات نسخه‌بندی‌شده:** snapshotهای ثابت v2.1، v2.0 و v1.0 حفظ می‌شوند.

## Bashref چه چیزهایی ارائه می‌کند؟

- **[Reference Guide](reference/):** مراجعه دقیق به builtinها، syntax، expansionها، shell optionها، `shopt`، variableها، conceptها و مثال‌ها.
- **[Professional Guide](book/):** راهنمای چهارده‌فصلی برای یادگیری، automation، SysAdmin، DevOps، امنیت و debugging.
- **[نصب](install/):** نصب CLI از artifactهای بررسی‌شده انتشار.
- **[دانلود](download/):** wheel، source archive، DEB/RPM، portable archive، man page، completion، Homebrew formula و checksum.
- **[انتشارها](releases/):** تاریخچه نسخه‌ها و snapshotهای پایدار.
- **[درباره](about/):** معماری، محدوده، مجوزها و مرزهای پروژه.

## شروع سریع

```bash
bashref search quoting
bashref --lang fa builtin printf
bashref option pipefail
bashref shopt extglob
bashref variable BASH_VERSION
bashref doctor
```

## Bashref یعنی...

- **جامع:** ۲۱۴ رکورد جفت‌شده فارسی/انگلیسی در کنار Professional Guide بلندمدت.
- **آفلاین:** lookup، search، diagnostics، JSON output و completionهای اصلی به شبکه نیاز ندارند.
- **قابل‌حمل:** wheel، source distribution، بسته‌های Debian/RPM، آرشیو portable، man page و shell completion.
- **مستند:** Reference Guide، Professional Guide، راهنمای نصب، مستندات contributor و man pageهای سیستمی.
- **قابل‌راستی‌آزمایی:** CI محافظت‌شده، checksum انتشار، خروجی‌های deterministic و snapshotهای پایدار.

رفتارهای خاص Bash عمدتاً با [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) تطبیق داده می‌شوند.

!!! warning "اجرای فرمان‌ها"
    حذف فایل، تغییر permission/ownership، عملیات سرویس‌ها و automation سطح سیستم را ابتدا در محیط کنترل‌شده آزمایش کنید.
