from pathlib import Path


def test_v2_release_notes_cover_user_contract():
    text = Path(".github/release-notes/v2.0.0.md").read_text(encoding="utf-8")
    for heading in [
        "## Installation",
        "## Artifacts",
        "## Checksums",
        "## Documentation",
        "## Upgrade from v1",
    ]:
        assert heading in text
    assert "bashref-2.0.0-py3-none-any.whl" in text
    assert "sha256sum -c SHA256SUMS" in text
