# ۱۰. شبکه و ابزارهای راه‌دور

بخش مهمی از منابع اولیه ابزارهای مکمل Bash را پوشش می‌دهد. این ابزارها خود Bash نیستند، اما در Workflowهای Shell بسیار رایج‌اند.

## SSH

```bash
ssh user@example.test
```

برای Automation از کلیدها و Host verification استاندارد استفاده کنید. غیرفعال‌کردن بررسی Host key برای راحتی، کنترل مهم امنیتی را حذف می‌کند.

## SCP و rsync

```bash
scp report.txt user@example.test:/tmp/
rsync -av --dry-run src/ user@example.test:/srv/app/
```

قبل از گزینه‌های همگام‌سازی حذف‌کننده، `--dry-run` را بررسی کنید.

## curl

```bash
curl -fsS https://example.com/
curl -I https://example.com/
```

در اسکریپت‌ها Flagهای مناسب failure و timeout را انتخاب کنید.

## JSON با jq

```bash
printf '%s\n' '{"ok":true}' | jq -r '.ok'
```

## ابزارهای شبکه محلی

برای مشاهده Socketهای محلی در Linux مدرن معمولاً `ss` انتخاب مناسبی است:

```bash
ss -lnt
```

این مرجع اسکریپت‌های اسکن انبوه یا هدف‌گیری سامانه‌های ثالث را منتشر نمی‌کند.
