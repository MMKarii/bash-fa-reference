# 1. Bash Fundamentals and the Shell Model

Bash means **Bourne Again Shell**. It is both an interactive command shell and a scripting language for Unix-like systems. Bash parses command text, performs expansions, establishes redirections and pipelines, then runs a builtin or external program.

The supplied source articles consistently emphasize three roles: **daily Linux interaction, automation, and system administration**. Those themes drive this reference.

## Shell, terminal, and kernel

- A terminal displays text input and output.
- A shell interprets commands.
- The kernel manages processes, files, devices, and other system resources.
- Many commands used from Bash—such as `grep`, `find`, `tar`, `ssh`, and `rsync`—are separate programs, not Bash builtins.

## Short history

Bash was developed as part of GNU and became a common shell on Linux systems. It remains installable on macOS, while newer macOS releases use Zsh as the default interactive shell.

## Check the actual version

```bash
bash --version
printf '%s\n' "$BASH_VERSION"
```

This reference cross-checks Bash-specific semantics against GNU Bash 5.3 documentation, but production scripts should always account for the version actually deployed.
