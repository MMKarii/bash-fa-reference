# Bash Cheat Sheet

| Goal | Example |
|---|---|
| Current directory | `pwd` |
| Detailed listing | `ls -lah` |
| Create nested path | `mkdir -p path/to/dir` |
| Tail a log | `tail -n 50 app.log` |
| Follow a log | `tail -f app.log` |
| Search text | `grep -n "ERROR" app.log` |
| Find files | `find . -type f -name '*.log'` |
| Disk use | `df -h` / `du -sh .` |
| Processes | `ps aux` |
| Service status | `systemctl status nginx` |
| Service log | `journalctl -u nginx` |
| Archive | `tar -czf backup.tar.gz dir/` |
| HTTP headers | `curl -I https://example.com` |
| Secure copy | `scp file user@example.test:/tmp/` |
| Sync | `rsync -av src/ dst/` |
| Syntax check | `bash -n script.sh` |
| Execution trace | `bash -x script.sh` |
| Static analysis | `shellcheck script.sh` |

## Script skeleton

```bash
#!/usr/bin/env bash
set -u
set -o pipefail

main() {
  printf '%s\n' "hello"
}

main "$@"
```

Add `set -e` only when you understand its exact semantics; it is not a substitute for explicit error handling at critical boundaries.
