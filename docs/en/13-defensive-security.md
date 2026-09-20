# 13. Defensive Security with Bash

The supplied security-oriented documents emphasize **input validation, least privilege, permissions, cautious sudo use, and log analysis**.

## Avoid command injection

Keep data as arguments rather than constructing command strings:

```bash
grep -F -- "$needle" "$logfile"
```

Validate input; use allowlists when the valid domain is small.

## Permissions and umask

```bash
umask 027
install -m 640 /dev/null report.log
```

## PATH control

Privileged scripts should not trust an uncontrolled `PATH`. Make the execution environment predictable.

## Authentication log review

```bash
journalctl -u ssh --since "today" | grep -i "failed"
```

This is for defensive review on systems you administer.

## Sensitive data

Do not put passwords, tokens, private keys, or cookies in shell history, process arguments, or logs.

## High-impact changes

Narrow scope, inspect the selected objects first, keep backup/rollback options, and minimize privileged execution.
