# Debian packaging

`tools/build_deb.py` stages and builds the Bashref Debian package.

The package owns only system files under `/usr` and `/opt/bashref/<version>`.
It never creates, edits, or removes user configuration under `~/.config/bashref`.
