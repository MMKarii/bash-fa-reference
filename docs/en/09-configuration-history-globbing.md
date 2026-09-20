# 9. Bash Configuration, History, Aliases, and Globbing

## Startup files

Startup behavior depends on whether Bash is interactive and/or a login shell. Common files include `.bash_profile`, `.profile`, and `.bashrc`. Verify the startup path on the target platform instead of assuming all distributions behave identically.

## Aliases

```bash
alias ll='ls -lah'
```

Aliases are interactive conveniences, not reliable script-safety controls. Scripts should implement their own safe behavior.

## History

```bash
history
HISTCONTROL=ignoreboth
```

History can capture secrets. Avoid putting credentials directly on the command line.

## Globbing

```bash
printf '%s\n' *.log
```

The shell expands filename patterns before executing the command. Handle the no-match case deliberately.

```bash
shopt -s nullglob
files=(*.log)
```

Keep `shopt` choices explicit inside scripts that depend on them.
