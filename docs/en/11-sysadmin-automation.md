# 11. System Administration Automation

## Disk use

```bash
df -h
du -sh /var/log
```

## Services and logs

```bash
systemctl status nginx
journalctl -u nginx --since "1 hour ago"
```

Review dependencies and production impact before restarting a service.

## Backup example

```bash
#!/usr/bin/env bash
set -u
set -o pipefail

source_dir="/srv/example"
backup_dir="/srv/backups"
stamp="$(date +%Y%m%d_%H%M%S)"
archive="${backup_dir}/example_${stamp}.tar.gz"

mkdir -p -- "$backup_dir"
tar -czf "$archive" -- "$source_dir"
printf 'backup: %s\n' "$archive"
```

A backup is not proven until restore is tested.

## Monitoring boundary

Bash is appropriate for small checks and automation glue. Durable production monitoring should use a monitoring/alerting system and a service manager rather than an endlessly growing shell script.
