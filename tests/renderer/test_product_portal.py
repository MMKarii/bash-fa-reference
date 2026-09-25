from pathlib import Path


def test_root_portal_exposes_product_sections():
    text = Path("site-root/index.html").read_text(encoding="utf-8")
    for marker in [
        "Bashref 2.1.0",
        'href="en/reference/"',
        'href="en/book/"',
        'href="en/install/"',
        'href="en/download/"',
        'href="en/releases/"',
        'href="fa/"',
        'href="en/"',
    ]:
        assert marker in text


def test_root_portal_links_stable_snapshots():
    text = Path("site-root/index.html").read_text(encoding="utf-8")
    assert 'href="v2.1/en/"' in text
    assert 'href="v2.1/fa/"' in text
    assert 'href="v2.0/en/"' in text
    assert 'href="v2.0/fa/"' in text
    assert 'href="v1.0/en/"' in text
    assert 'href="v1.0/fa/"' in text
