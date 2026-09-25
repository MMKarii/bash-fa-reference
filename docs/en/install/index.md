# Install Bashref

Bashref 2.0.0 is an offline bilingual Bash reference CLI.

## Python package

The primary portable installation path is:

```bash
pipx install bashref
```

You can also install with pip:

```bash
python -m pip install bashref
```

For a checkout of this repository:

```bash
python -m pip install -e .
```

Verify the installation:

```bash
bashref --version
bashref search quoting
bashref builtin printf
```

## Linux packages

Release assets include Debian and RPM packages. They install the CLI, packaged reference data, man pages, and Bash/Zsh/Fish completions.

## Offline behavior

Core lookup and search do not require network access. Bashref never executes examples from the reference database.
