# نصب Bashref

Bashref 2.1.0 یک CLI آفلاین دوزبانه است. اگر نمی‌خواهید Python جداگانه مدیریت کنید از standalone استفاده کنید.

## Standalone بدون نیاز به Python جداگانه

### Linux x86_64

```bash
curl -LO https://github.com/MMKarii/bash-fa-reference/releases/download/v2.1.0/bashref-2.1.0-linux-x86_64.tar.gz
tar -xzf bashref-2.1.0-linux-x86_64.tar.gz
install -m 755 bashref ~/.local/bin/bashref
bashref doctor
```

### macOS

Apple Silicon از `bashref-2.1.0-macos-arm64.tar.gz` و Intel از `bashref-2.1.0-macos-x86_64.tar.gz` استفاده می‌کند.

### Windows x86_64

`bashref-2.1.0-windows-x86_64.zip` را دانلود کنید، `bashref.exe` را استخراج و در مسیری داخل `PATH` قرار دهید.

## pipx / wheel

```bash
pipx install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.1.0/bashref-2.1.0-py3-none-any.whl
```

## بسته‌های Linux

انتشار شامل DEB و RPM است که CLI، داده مرجع، man page و completionها را نصب می‌کنند.

## بررسی نصب

```bash
bashref --version
bashref doctor
bashref --lang fa search quoting
```

## حذف

- Standalone: فایل `bashref` یا `bashref.exe` را حذف کنید.
- pipx: `pipx uninstall bashref`
- pip: `python -m pip uninstall bashref`
- Debian: `sudo dpkg -r bashref`
- RPM: `sudo rpm -e bashref`

حذف DEB/RPM preference کاربر را پاک نمی‌کند.
