# Install Bashref

Bashref 2.1.0 is an offline bilingual Bash reference CLI. Use a standalone executable when you do not want to manage Python, or use the Python/Linux packages for deeper system integration.

## Standalone: no separate Python required

### Linux x86_64

```bash
curl -LO https://github.com/MMKarii/bash-fa-reference/releases/download/v2.1.0/bashref-2.1.0-linux-x86_64.tar.gz
tar -xzf bashref-2.1.0-linux-x86_64.tar.gz
install -m 755 bashref ~/.local/bin/bashref
bashref doctor
```

### macOS Apple Silicon

Use `bashref-2.1.0-macos-arm64.tar.gz`. Intel Macs use `bashref-2.1.0-macos-x86_64.tar.gz`.

### Windows x86_64

Download `bashref-2.1.0-windows-x86_64.zip`, extract `bashref.exe`, and place it in a directory on `PATH`.

## pipx / wheel

```bash
pipx install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.1.0/bashref-2.1.0-py3-none-any.whl
```

Or:

```bash
python -m pip install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.1.0/bashref-2.1.0-py3-none-any.whl
```

## Linux system packages

The release includes `bashref_2.1.0_all.deb` and an RPM. These install the CLI, reference data, man pages, and Bash/Zsh/Fish completions.

## Verify

```bash
bashref --version
bashref doctor
bashref search quoting
bashref builtin printf
```

## Uninstall

- Standalone: remove the copied `bashref` or `bashref.exe`.
- pipx: `pipx uninstall bashref`
- pip: `python -m pip uninstall bashref`
- Debian: `sudo dpkg -r bashref`
- RPM: `sudo rpm -e bashref`

User preferences under the Bashref config directory are not removed by DEB/RPM uninstall.
