# سازگاری و ماتریس پشتیبانی

Bashref دو نوع سازگاری دارد: **زبان Bash که مستند می‌شود** و **سیستمی که CLI Bashref را اجرا می‌کند**.

## اجرای CLI

| توزیع | سیستم | نیاز به Python |
| --- | --- | --- |
| Standalone archive | Linux x86_64 | خیر |
| Standalone archive | macOS arm64 | خیر |
| Standalone archive | macOS x86_64 | خیر |
| Standalone ZIP | Windows x86_64 | خیر |
| Wheel / pipx | Linux، macOS، Windows و سایر سیستم‌های دارای Python | Python 3.10+ |
| DEB | خانواده Debian | Python سیستمی 3.10+ |
| RPM | خانواده RPM | Python سیستمی 3.10+ |

نسخه‌های standalone به‌صورت مستقل در GitHub Actions build و smoke-test می‌شوند و runtime لازم را همراه خود دارند.

## محدوده زبان Bash

Bashref رفتار GNU Bash را مستند می‌کند. برای جست‌وجوی پایگاه مرجع لازم نیست Bash نصب باشد. تفاوت با POSIX shell، Zsh، Fish یا پوسته‌های دیگر باید در مستندات مشخص شود.

برای رفتارهای حساس به نسخه، GNU Bash Reference Manual منبع اصلی است.

## سازگاری machine-readable

خروجی JSON رابط پایدار automation در major version 2 است:

```bash
bashref --format json builtin printf
bashref --format json doctor
```
