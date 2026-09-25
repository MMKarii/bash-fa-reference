# نصب Bashref

Bashref 2.0.0 یک ابزار خط فرمان آفلاین برای مرجع دوزبانه Bash است.

## روش پیشنهادی نصب

wheel رسمی را مستقیماً از GitHub Release نصب کنید:

```bash
pipx install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.0.0/bashref-2.0.0-py3-none-any.whl
```

یا با pip:

```bash
python -m pip install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.0.0/bashref-2.0.0-py3-none-any.whl
```

برای source checkoutشده:

```bash
python -m pip install -e .
```

بررسی نصب:

```bash
bashref --version
bashref search quoting
bashref --lang fa builtin printf
```

## بسته‌های Linux

انتشار v2 شامل بسته‌های Debian و RPM نیز هست. این بسته‌ها runtime ابزار، داده مرجع، man page و completionهای Bash/Zsh/Fish را نصب می‌کنند.

## اجرای آفلاین

جست‌وجو و lookup اصلی به اینترنت نیاز ندارند و Bashref هیچ مثال ذخیره‌شده در مرجع را اجرا نمی‌کند.

> در حال حاضر artifactهای نصب از طریق GitHub Releases منتشر می‌شوند و این مستندات انتشار روی PyPI را فرض نمی‌کنند.
