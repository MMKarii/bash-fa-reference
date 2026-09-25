# Compatibility and support matrix

Bashref has two compatibility dimensions: the **Bash language being documented** and the **platform running the Bashref CLI**.

## CLI runtime

| Distribution | Host | Python required |
| --- | --- | --- |
| Standalone archive | Linux x86_64 | No |
| Standalone archive | macOS arm64 | No |
| Standalone archive | macOS x86_64 | No |
| Standalone ZIP | Windows x86_64 | No |
| Wheel / pipx | Linux, macOS, Windows and other Python platforms | Python 3.10+ |
| DEB | Debian-family Linux | System Python 3.10+ |
| RPM | RPM-family Linux | System Python 3.10+ |

Standalone binaries are built and smoke-tested independently in GitHub Actions and contain the runtime Bashref needs.

## Bash language scope

Bashref documents GNU Bash semantics. Bash itself is not required merely to search the reference database. Where behavior differs from POSIX shell, Zsh, Fish, or another shell, the documentation should identify that difference.

For version-sensitive Bash behavior, use the GNU Bash Reference Manual cited by the corresponding reference record.

## Machine-readable compatibility

JSON output is the stable automation interface within the v2 major line:

```bash
bashref --format json builtin printf
bashref --format json doctor
```

Documented exit codes and JSON keys should remain backward compatible in minor releases.
