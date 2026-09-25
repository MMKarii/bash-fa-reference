# Troubleshooting

## Start with diagnostics

```bash
bashref doctor
bashref --format json doctor
```

A healthy installation reports the Bashref version, runtime type, host platform, selected language, record count, and bilingual parity.

## Command not found

Check whether the install directory is on `PATH`:

```bash
command -v bashref
```

For a standalone install under `~/.local/bin`, ensure that directory is included in `PATH`.

## Reference entry not found

Search before direct lookup:

```bash
bashref search process
bashref search quoting
```

Direct lookup returns exit code 3 when no record exists. Machine-readable errors are available with `--format json`.

## Language looks wrong

Override one command:

```bash
bashref --lang en search array
bashref --lang fa search array
```

Persist a preference:

```bash
bashref lang en
```

Explicit `--lang` wins over saved preference and locale.

## Man page unavailable

Standalone archives focus on the single executable. If a system man page is not installed, use:

```bash
bashref docs
bashref docs printf
```

DEB/RPM packages install Bashref man pages.

## Corrupt-data error

Exit code 4 means packaged reference data failed validation/loading. Reinstall the same release from a verified artifact and compare it with `SHA256SUMS`. If the problem persists, report it with the JSON doctor output.
