# Bash Professional Reference

<img class="hero-banner" src="assets/brand-banner.webp" alt="Bash Professional Reference banner">

**Bashref 2.1.0** combines an offline CLI, a structured bilingual Reference Guide, generated system man pages, standalone Linux/macOS/Windows executables, Linux packages, and the 14-chapter Professional Guide.

This project covers **command-line fundamentals, pipelines and redirection, text processing, scripting, automation, system administration, DevOps, defensive security, and debugging**. Bash-specific behavior is cross-checked against the [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html).

## Use Bashref

- **[Reference Guide](reference/):** precise lookup for builtins, syntax, expansions, options, variables, and core concepts.
- **[Command Summary](reference/usage-summary.md):** compact CLI command/options overview.
- **[Professional Guide](book/):** the 14-chapter learning and operations handbook.
- **[Installation](install/):** standalone executables, wheel/pipx, DEB/RPM, verification, and uninstall.
- **[Download](download/):** Linux/macOS/Windows binaries, packages, man pages, completions, and checksums.
- **[Compatibility](compatibility.md):** runtime/platform support and machine-readable compatibility.
- **[Troubleshooting](troubleshooting.md):** diagnostics and common installation/runtime problems.
- **[FAQ](faq.md):** common questions about offline operation, Bash requirements, and downloads.
- **[Releases](releases/):** release history and version information.
- **[About](about/):** architecture, scope, and licensing.

Quick CLI examples:

```bash
bashref
bashref search quoting
bashref builtin printf
bashref --format json option pipefail
bashref doctor
```

## Start here

- New to Bash: [Learning Path](learning-path.md) and chapters 1–4
- Scripting: chapters 7–8
- SysAdmin/DevOps: chapters 10–12
- Security and quality: chapters 8, 13, and 14
- Fast lookup: [Cheat Sheet](cheatsheet.md)
- Terminology: [Glossary](glossary.md)

!!! warning "Run commands deliberately"
    Test file deletion, permission/ownership changes, service operations, and system-level automation in a controlled environment before production use.
