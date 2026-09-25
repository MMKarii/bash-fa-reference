from pathlib import Path


def test_v20_release_notes_remain_available():
    text = Path(".github/release-notes/v2.0.0.md").read_text(encoding="utf-8")
    assert "## Installation" in text
    assert "bashref-2.0.0-py3-none-any.whl" in text


def test_v21_release_notes_cover_platform_contract():
    text = Path(".github/release-notes/v2.1.0.md").read_text(encoding="utf-8")
    for heading in [
        "## Installation",
        "## Artifacts",
        "## Checksums",
        "## Documentation",
        "## Upgrade from v2.0",
    ]:
        assert heading in text
    for artifact in [
        "bashref-2.1.0-linux-x86_64.tar.gz",
        "bashref-2.1.0-macos-arm64.tar.gz",
        "bashref-2.1.0-macos-x86_64.tar.gz",
        "bashref-2.1.0-windows-x86_64.zip",
        "bashref-2.1.0-py3-none-any.whl",
    ]:
        assert artifact in text
    assert "sha256sum -c SHA256SUMS" in text
