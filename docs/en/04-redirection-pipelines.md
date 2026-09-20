# 4. Redirection, Pipelines, and Exit Status

Unix-style workflows become powerful when small tools are composed.

## Standard streams

- stdin: standard input
- stdout: standard output
- stderr: standard error

```bash
printf '%s\n' "ok" > result.txt
printf '%s\n' "next" >> result.txt
command 2> errors.log
command > output.log 2>&1
```

## Pipelines

```bash
journalctl -u ssh | grep -i "failed"
```

A pipeline connects one command's stdout to the next command's stdin.

```bash
set -o pipefail
producer | filter | consumer
status=$?
```

With `pipefail`, failures in earlier pipeline elements can influence the final status.

## Exit status

A general convention is zero for success and non-zero for failure or a command-specific result.

```bash
if grep -q "READY" app.log; then
  printf '%s\n' "ready"
fi
```

## `set -e` is nuanced

`set -e` does not simply mean "exit after every failing command"; its behavior depends on shell syntax and context. Treat it as an optional aid, not your complete error strategy. Explicitly handle failures at important boundaries.
