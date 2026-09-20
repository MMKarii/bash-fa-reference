# ۱۲. Bash در DevOps و CI/CD

منابع اولیه Bash را برای Build، Test، Deployment، Git، Docker و انتقال فایل معرفی می‌کنند. در CI، هدف باید **قابل‌تکرار بودن** و **Fail شدن واضح** باشد.

## الگوی ساده CI script

```bash
#!/usr/bin/env bash
set -u
set -o pipefail

run_tests() {
  printf '%s\n' "running tests"
  ./scripts/test.sh
}

main() {
  run_tests
}

main "$@"
```

## Git

```bash
git status --short
git diff --check
```

Automation نباید بدون سیاست مشخص به‌صورت خودکار هر تغییر workspace را Commit/Push کند.

## Container tooling

Bash معمولاً orchestration لایه نازک را انجام می‌دهد؛ منطق پیچیده Business یا parsing حجیم را به زبان/ابزار مناسب واگذار کنید.

## Secretها

- Secret را در Repository یا Log چاپ نکنید.
- ورودی CI را Trusted فرض نکنید.
- Credentialها را از Secret store پلتفرم بگیرید.
- Commandهایی که داده خارجی واردشان می‌شود را با Quote و allowlist طراحی کنید.

## Idempotency

Jobهای CI/CD بهتر است بتوانند بدون ایجاد state ناسازگار دوباره اجرا شوند.
