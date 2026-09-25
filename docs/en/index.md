# Bash Professional Reference

<img class="hero-banner" src="assets/brand-banner.webp" alt="Bash Professional Reference banner">

**Bashref 2.0.0** combines an offline CLI, a structured bilingual Reference Guide, system man pages, downloadable packages, and the 14-chapter Professional Guide.

This project covers **command-line fundamentals, pipelines and redirection, text processing, scripting, automation, system administration, DevOps, defensive security, and debugging**. Bash-specific behavior is cross-checked against the [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html).

## Use Bashref

- **[Reference Guide](reference/):** precise lookup for builtins, syntax, expansions, options, variables, and core concepts.
- **[Professional Guide](book/):** the 14-chapter learning and operations handbook.
- **[Installation](install/):** install the CLI from the official release artifacts.
- **[Download](download/):** wheel, source archive, DEB/RPM, man pages, completions, and checksums.
- **[Releases](releases/):** release history and version information.
- **[About](about/):** architecture, scope, and licensing.

Quick CLI examples:

```bash
bashref --version
bashref search quoting
bashref builtin printf
bashref --format json option pipefail
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
