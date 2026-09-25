# Installing Bashref

Bashref is an offline bilingual Bash reference CLI plus its documentation corpus.

## Requirements

- Python 3.10 or newer for the Python package
- Bash is optional; Bashref can search and display reference data without Bash installed
- network access is not required after installation for core lookup/search

## Recommended installation

Install the released wheel with pipx:

```bash
pipx install https://github.com/MMKarii/bash-fa-reference/releases/download/v2.1.0/bashref-2.1.0-py3-none-any.whl
bashref --version
bashref doctor
```

## Python package

```bash
python -m pip install bashref-2.1.0-py3-none-any.whl
```

## Debian / Ubuntu

```bash
sudo dpkg -i bashref_2.1.0_all.deb
bashref --version
```

## RPM-based Linux

```bash
sudo rpm -i bashref-2.1.0-1.noarch.rpm
bashref --version
```

## Development installation

```bash
git clone https://github.com/MMKarii/bash-fa-reference.git
cd bash-fa-reference
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e .
bashref doctor
```

## Integrity verification

Release assets include `SHA256SUMS`:

```bash
sha256sum -c SHA256SUMS
```

## Uninstall

For pipx:

```bash
pipx uninstall bashref
```

For Debian packages:

```bash
sudo dpkg -r bashref
```

For RPM packages:

```bash
sudo rpm -e bashref
```

User configuration under the user's config directory is intentionally not deleted by system package removal.
