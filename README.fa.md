# مرجع حرفه‌ای Bash — فارسی + English

![Bash Professional Reference](docs/fa/assets/brand-banner.webp)

Bashref یک محصول مرجع دوزبانه Bash است: CLI آفلاین، Reference Guide ساختاریافته، man pageهای تولیدشده، executable مستقل چندپلتفرمی، بسته‌های Linux و Professional Guide چهارده‌فصلی.

**سایت مستندات:** https://mmkarii.github.io/bash-fa-reference/  
**فارسی:** https://mmkarii.github.io/bash-fa-reference/fa/  
**English:** https://mmkarii.github.io/bash-fa-reference/en/

## CLI Bashref

نسخه 2.1.0 جست‌وجو و lookup عادی را آفلاین نگه می‌دارد:

```bash
bashref
bashref search quoting
bashref --lang fa builtin printf
bashref --format json option pipefail
bashref doctor
```

اجرای `bashref` بدون آرگومان خلاصه فرمان‌ها را نشان می‌دهد. `bashref doctor` وضعیت runtime، سیستم، زبان، تعداد رکوردها و برابری فارسی/انگلیسی را گزارش می‌کند.

## نصب

خروجی‌های انتشار شامل این موارد هستند:

- standalone برای Linux x86_64
- standalone برای macOS arm64 و x86_64
- standalone برای Windows x86_64
- wheel / pipx برای Python 3.10+
- بسته Debian
- بسته RPM
- Homebrew formula

نسخه standalone به نصب جداگانه Python نیاز ندارد. راهنمای کامل نصب و حذف در سایت مستندات قرار دارد.

## معماری محصول

- CLI آفلاین با خروجی text و JSON
- Reference Guide دوزبانه و ساختاریافته
- Professional Guide چهارده‌فصلی
- man pageهای تولیدشده از منبع مرجع
- wheel/sdist، DEB/RPM، completion، Homebrew و checksum
- standaloneهای Linux/macOS/Windows که در CI smoke-test می‌شوند
- سایت RTL/LTR با snapshot نسخه‌ها

## کیفیت

CI داده مرجع، تست‌ها، خروجی تولیدشده، نصب wheel، man page، link/anchor، metadata، accessibility، DEB/RPM و executableهای مستقل را بررسی می‌کند.

Bashref هیچ مثال ذخیره‌شده در پایگاه مرجع را اجرا نمی‌کند و برای رفتارهای ویژه Bash از GNU Bash Reference Manual استفاده می‌کند.

## پشتیبانی و مشارکت

برای گزارش مشکل ابتدا اجرا کنید:

```bash
bashref --format json doctor
```

سپس [SUPPORT.md](SUPPORT.md) و برای مسائل امنیتی [SECURITY.md](SECURITY.md) را ببینید. راهنمای مشارکت در [CONTRIBUTING.md](CONTRIBUTING.md) است.

## مجوز

کد نرم‌افزار MIT و متن مستندات/مرجع CC BY 4.0 است.
