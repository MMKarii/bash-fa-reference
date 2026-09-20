# 10. Networking and Remote Tools

Several supplied articles cover tools commonly orchestrated from Bash. They are not Bash builtins, but they are core shell-workflow components.

## SSH

```bash
ssh user@example.test
```

Use normal host verification and managed keys. Disabling host-key checks trades away an important security control.

## SCP and rsync

```bash
scp report.txt user@example.test:/tmp/
rsync -av --dry-run src/ user@example.test:/srv/app/
```

Use `--dry-run` before deletion-capable synchronization.

## curl

```bash
curl -fsS https://example.com/
curl -I https://example.com/
```

Select timeout and failure flags appropriate for automation.

## JSON with jq

```bash
printf '%s\n' '{"ok":true}' | jq -r '.ok'
```

## Local sockets on Linux

```bash
ss -lnt
```

Modern Linux environments commonly use `ss` for socket inspection. This reference does not publish bulk scanning or third-party targeting scripts.
