# 6. Processes, Jobs, and Signals

## Inspect processes

```bash
ps aux
top
```

`htop` provides a richer interactive view when installed.

## Job control

```bash
long_task &
jobs
fg %1
bg %1
```

Job control is mainly an interactive-shell feature.

## Signals

```bash
kill -TERM "$pid"
```

Start with a manageable signal such as `TERM`. `KILL` prevents cleanup and should be a last resort.

## Cleanup with trap

```bash
tmp="$(mktemp)"
cleanup() {
  rm -f -- "$tmp"
}
trap cleanup EXIT INT TERM
```

`trap` is useful for temporary files, locks, and predictable shutdown behavior.

Avoid using fragile text matching such as `ps | grep` for safety-critical process decisions. Prefer a service manager or a PID/handle you actually own.
