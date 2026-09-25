# مرجع حرفه‌ای Bash

<img class="hero-banner" src="assets/brand-banner.webp" alt="بنر مرجع حرفه‌ای Bash">

**Bashref 2.1.0** یک CLI آفلاین، Reference Guide ساختاریافته دوزبانه، man pageهای تولیدشده، executableهای مستقل Linux/macOS/Windows، بسته‌های Linux و Professional Guide چهارده‌فصلی را در یک پروژه یکپارچه می‌کند.

این پروژه **فرمان‌های روزمره، Pipeline و Redirection، پردازش متن، اسکریپت‌نویسی، خودکارسازی، مدیریت سیستم، DevOps، امنیت دفاعی و Debugging** را پوشش می‌دهد. رفتارهای ویژه Bash با [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) تطبیق داده می‌شوند.

## استفاده از Bashref

- **[Reference Guide](reference/):** مراجعه دقیق به builtinها، syntax، expansionها، optionها، variableها و conceptهای اصلی.
- **[خلاصه فرمان‌ها](reference/usage-summary.md):** مرور فشرده commandها و optionهای CLI.
- **[Professional Guide](book/):** راهنمای آموزشی و عملی ۱۴ فصلی.
- **[نصب](install/):** standalone، wheel/pipx، DEB/RPM، بررسی نصب و حذف.
- **[دانلود](download/):** binaryهای Linux/macOS/Windows، بسته‌ها، man page، completion و checksum.
- **[سازگاری](compatibility.md):** سیستم‌های پشتیبانی‌شده و قرارداد خروجی machine-readable.
- **[رفع اشکال](troubleshooting.md):** diagnostics و مشکلات متداول نصب/اجرا.
- **[FAQ](faq.md):** پرسش‌های متداول.
- **[انتشارها](releases/):** تاریخچه نسخه‌ها.
- **[درباره](about/):** معماری، محدوده و مجوزها.

نمونه‌های CLI:

```bash
bashref
bashref search quoting
bashref --lang fa builtin printf
bashref --format json option pipefail
bashref doctor
```

## از کجا شروع کنم؟

- تازه‌کار: [مسیر یادگیری](learning-path.md) و فصل‌های ۱ تا ۴
- اسکریپت‌نویسی: فصل‌های ۷ و ۸
- SysAdmin/DevOps: فصل‌های ۱۰ تا ۱۲
- امنیت و کیفیت: فصل‌های ۸، ۱۳ و ۱۴
- مراجعه سریع: [Cheat Sheet](cheatsheet.md)
- اصطلاحات: [واژه‌نامه](glossary.md)

!!! warning "اجرای فرمان‌ها"
    مثال‌ها را ابتدا روی سیستم شخصی، VM یا محیط آزمایشگاهی بررسی کنید. فرمان‌های حذف، تغییر مجوز، تغییر مالکیت، سرویس‌ها و فایل‌های سیستمی می‌توانند اثر دائمی داشته باشند.
