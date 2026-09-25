# مرجع حرفه‌ای Bash

<img class="hero-banner" src="assets/brand-banner.webp" alt="بنر مرجع حرفه‌ای Bash">

**Bashref 2.0.0** یک CLI آفلاین، Reference Guide ساختاریافته دوزبانه، man pageهای سیستمی، بسته‌های قابل دانلود و Professional Guide چهارده‌فصلی را در یک پروژه یکپارچه می‌کند.

این پروژه **فرمان‌های روزمره، Pipeline و Redirection، پردازش متن، اسکریپت‌نویسی، خودکارسازی، مدیریت سیستم، DevOps، امنیت دفاعی و Debugging** را پوشش می‌دهد. رفتارهای ویژه Bash با [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html) تطبیق داده می‌شوند.

## استفاده از Bashref

- **[Reference Guide](reference/):** مراجعه دقیق به builtinها، syntax، expansionها، optionها، variableها و conceptهای اصلی.
- **[Professional Guide](book/):** راهنمای آموزشی و عملی ۱۴ فصلی.
- **[نصب](install/):** نصب CLI از artifactهای رسمی انتشار.
- **[دانلود](download/):** wheel، source archive، DEB/RPM، man page، completion و checksum.
- **[انتشارها](releases/):** تاریخچه نسخه‌ها.
- **[درباره](about/):** معماری، محدوده و مجوزها.

نمونه‌های CLI:

```bash
bashref --version
bashref search quoting
bashref --lang fa builtin printf
bashref --format json option pipefail
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
