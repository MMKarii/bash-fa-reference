# 5. Text Processing and Search

The source material gives significant attention to `grep`, `awk`, `sed`, `cut`, `sort`, `uniq`, `find`, and `xargs`.

## grep

```bash
grep -in "error" app.log
grep -R "listen" ./config/
```

## awk

```bash
awk -F: '{print $1}' /etc/passwd
awk '{sum += $2} END {print sum}' data.txt
```

## sed

```bash
sed 's/error/ERROR/g' app.log
sed '/DEBUG/d' app.log
```

Take a backup or review a diff before using in-place edits on important files.

## sort and uniq

```bash
cut -d: -f1 /etc/passwd | sort
sort events.txt | uniq -c | sort -nr
```

## find

```bash
find /var/log -type f -name '*.log'
find . -type f -size +100M -print
```

## Safer filename handling with xargs

```bash
find . -type f -name '*.tmp' -print0 | xargs -0 -r printf '%s\n'
```

Inspect results with a harmless operation first. Apply destructive changes only after verifying the selection.
