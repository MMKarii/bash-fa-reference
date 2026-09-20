# ۱۴. Debugging، تست، Portability و مقایسه Shellها

## Syntax check

```bash
bash -n script.sh
```

## Trace

```bash
bash -x script.sh
```

Trace ممکن است داده حساس را نشان دهد؛ در محیط Production با احتیاط استفاده کنید.

## ShellCheck

[ShellCheck](https://github.com/koalaman/shellcheck) تحلیل ایستا برای `sh`/`bash` ارائه می‌کند:

```bash
shellcheck script.sh
```

## تست

برای Functionهای pure، ورودی/خروجی مشخص تعریف کنید. برای عملیات filesystem از temporary directory استفاده کنید. عملیات خارجی را تا حد ممکن mock یا isolate کنید.

## Portability

اگر Shebang `#!/bin/sh` است، از syntax مخصوص Bash مثل Arrayها و `[[ ... ]]` استفاده نکنید. اگر ویژگی Bash لازم دارید، آن را صریح اعلام کنید.

## Bash، Zsh و Fish

- Bash: رایج، مناسب اسکریپت‌نویسی و سازگاری گسترده.
- Zsh: امکانات تعاملی و customization قوی.
- Fish: تجربه تعاملی ساده و غنی، اما syntax اسکریپت آن با Bash/POSIX shell یکسان نیست.

برای اسکریپت سازمانی، Shell را بر اساس محیط مقصد و portability انتخاب کنید؛ برای Shell تعاملی، تجربه کاربر معیار مهم‌تری است.
