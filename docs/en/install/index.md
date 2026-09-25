# Install Bashref

Bashref 2.0.0 is an offline bilingual Bash reference CLI.

## Recommended installation

Install the official wheel directly from the GitHub Release:

```bash
pipx install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.0.0/bashref-2.0.0-py3-none-any.whl
```

Or with pip:

```bash
python -m pip install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.0.0/bashref-2.0.0-py3-none-any.whl
```

For a checked-out source tree:

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

The v2 release also includes Debian and RPM packages. They install the CLI runtime, packaged reference data, man pages, and Bash/Zsh/Fish completions.

## Offline behavior

Core lookup and search do not require network access. Bashref never executes examples from the reference database.

> The project currently publishes installation artifacts through GitHub Releases. A PyPI publication is not assumed by this documentation.
