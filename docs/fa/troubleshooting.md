# رفع اشکال

## ابتدا diagnostics را اجرا کنید

```bash
bashref doctor
bashref --format json doctor
```

نصب سالم نسخه Bashref، نوع runtime، سیستم، زبان انتخاب‌شده، تعداد رکوردها و برابری فارسی/انگلیسی را گزارش می‌کند.

## فرمان bashref پیدا نمی‌شود

مسیر نصب را بررسی کنید:

```bash
command -v bashref
```

اگر standalone را در `~/.local/bin` گذاشته‌اید، این مسیر باید در `PATH` باشد.

## رکورد پیدا نمی‌شود

ابتدا search کنید:

```bash
bashref search process
bashref search quoting
```

lookup مستقیم در صورت نبود رکورد exit code 3 می‌دهد. برای خطای machine-readable از `--format json` استفاده کنید.

## زبان اشتباه است

```bash
bashref --lang en search array
bashref --lang fa search array
bashref lang fa
```

گزینه صریح `--lang` همیشه بر preference ذخیره‌شده و locale اولویت دارد.

## man page در دسترس نیست

در نصب standalone می‌توانید از سایت استفاده کنید:

```bash
bashref docs
bashref docs printf
```

بسته‌های DEB/RPM man pageهای Bashref را نصب می‌کنند.

## خطای corrupt data

exit code 4 یعنی داده مرجع بسته‌بندی‌شده قابل اعتماد نبوده است. artifact همان release را دوباره نصب و checksum آن را با `SHA256SUMS` مقایسه کنید.
