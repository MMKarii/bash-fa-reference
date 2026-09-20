# ۲. فایل‌سیستم و دستورات پایه

## موقعیت و جابه‌جایی

```bash
pwd
cd /etc
cd ~
cd -
```

برای اسکریپت‌های عملیاتی، مسیرهای مشخص و قابل پیش‌بینی بهتر از اتکا به دایرکتوری فعلی هستند.

## مشاهده و ساخت

```bash
ls -lah
mkdir -p workspace/logs
touch workspace/logs/app.log
```

`ls -l` مجوز، مالکیت و اندازه را نشان می‌دهد. گزینه `-a` فایل‌های مخفی و `-h` اندازه‌های خوانا را نمایش می‌دهد.

## کپی و انتقال

```bash
cp file.txt backup.txt
cp -r src/ dst/
mv old_name new_name
```

قبل از عملیات دسته‌ای، ابتدا انتخاب فایل‌ها را با `printf`, `find -print` یا حالت dry-run ابزار مقصد بررسی کنید.

## مجوزها و مالکیت

```bash
chmod u+x deploy.sh
chmod 750 private-dir
chown app:app file.txt
```

اعداد مجوز ترکیبی از read=4، write=2 و execute=1 هستند. تغییر مالکیت یا مجوز باید با اصل حداقل دسترسی انجام شود.

## راهنمای داخلی

```bash
type cd
help cd
man ls
command -v bash
```

`type` مشخص می‌کند یک نام Builtin، Alias، Function یا برنامه خارجی است.
