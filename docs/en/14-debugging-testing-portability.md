# 14. Debugging, Testing, Portability, and Shell Comparison

## Syntax check

```bash
bash -n script.sh
```

## Execution trace

```bash
bash -x script.sh
```

Tracing can expose sensitive values, so use it carefully in production.

## ShellCheck

[ShellCheck](https://github.com/koalaman/shellcheck) provides static analysis for shell scripts:

```bash
shellcheck script.sh
```

## Testing

Keep pure logic in functions with clear input/output. Use temporary directories for filesystem tests. Isolate or mock external operations where practical.

## Portability

A script starting with `#!/bin/sh` should not silently rely on Bash-only arrays or `[[ ... ]]`. If Bash is required, declare it.

## Bash vs. Zsh vs. Fish

- Bash: widely available and well suited to scripting.
- Zsh: strong interactive customization.
- Fish: rich interactive UX, but its scripting syntax is not Bash/POSIX shell syntax.

Choose a scripting shell for the deployment environment and portability needs; choose an interactive shell for user experience.
