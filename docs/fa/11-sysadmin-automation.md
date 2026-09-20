# ۱۱. مدیریت سیستم و خودکارسازی

## فضای دیسک

```bash
df -h
du -sh /var/log
```

## سرویس‌ها

```bash
systemctl status nginx
journalctl -u nginx --since "1 hour ago"
```

قبل از restart کردن سرویس Production، dependency و impact را بررسی کنید.

## Backup نمونه

```bash
#!/usr/bin/env bash
set -u
set -o pipefail

source_dir="/srv/example"
backup_dir="/srv/backups"
stamp="$(date +%Y%m%d_%H%M%S)"
archive="${backup_dir}/example_${stamp}.tar.gz"

mkdir -p -- "$backup_dir"
tar -czf "$archive" -- "$source_dir"
printf 'backup: %s\n' "$archive"
```

وجود فایل Backup به‌تنهایی به معنی قابل‌بازیابی بودن نیست؛ Restore را دوره‌ای آزمایش کنید.

## مانیتورینگ

Bash برای Checkهای کوچک مناسب است، اما برای Monitoring پایدار از سیستم مانیتورینگ، alerting و service manager استفاده کنید. اسکریپت کوتاه نباید جای observability کامل را بگیرد.
