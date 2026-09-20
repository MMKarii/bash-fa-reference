# برگه تقلب Bash

| هدف | نمونه |
|---|---|
| مسیر فعلی | `pwd` |
| فهرست کامل | `ls -lah` |
| ساخت مسیر تو در تو | `mkdir -p path/to/dir` |
| مشاهده انتهای Log | `tail -n 50 app.log` |
| دنبال‌کردن Log | `tail -f app.log` |
| جست‌وجوی متن | `grep -n "ERROR" app.log` |
| یافتن فایل | `find . -type f -name '*.log'` |
| مصرف دیسک | `df -h` / `du -sh .` |
| پردازه‌ها | `ps aux` |
| وضعیت سرویس | `systemctl status nginx` |
| Log سرویس | `journalctl -u nginx` |
| آرشیو | `tar -czf backup.tar.gz dir/` |
| درخواست HTTP Header | `curl -I https://example.com` |
| انتقال امن | `scp file user@example.test:/tmp/` |
| همگام‌سازی | `rsync -av src/ dst/` |
| بررسی Syntax | `bash -n script.sh` |
| Trace اجرا | `bash -x script.sh` |
| تحلیل ایستا | `shellcheck script.sh` |

## اسکلت اسکریپت

```bash
#!/usr/bin/env bash
set -u
set -o pipefail

main() {
  printf '%s\n' "hello"
}

main "$@"
```

`set -e` را فقط با درک دقیق semantics آن اضافه کنید؛ جایگزین بررسی صریح خطا در نقاط بحرانی نیست.
