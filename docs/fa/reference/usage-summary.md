# خلاصه فرمان‌ها

اجرای `bashref` بدون آرگومان یا `bashref usage` خلاصه فرمان‌ها را نمایش می‌دهد.

| فرمان | کاربرد |
| --- | --- |
| `bashref search QUERY` | جست‌وجوی همه رکوردها |
| `bashref show TOPIC` | یافتن رکورد با نام، alias یا ID |
| `bashref builtin NAME` | نمایش builtin |
| `bashref syntax NAME` | نمایش syntax |
| `bashref expansion NAME` | نمایش expansion |
| `bashref option NAME` | نمایش shell option |
| `bashref shopt NAME` | نمایش shopt option |
| `bashref variable NAME` | نمایش variable |
| `bashref list CATEGORY` | فهرست یک دسته |
| `bashref doctor` | بررسی runtime و داده مرجع |
| `bashref docs [TOPIC]` | نمایش URL مستندات |
| `bashref man [TOPIC]` | باز کردن man page در صورت نصب |
| `bashref completion SHELL` | تولید completion برای Bash/Zsh/Fish |

گزینه‌های سراسری:

```text
--lang {fa,en}
--format {text,json}
--no-color
--width N
--version
```
