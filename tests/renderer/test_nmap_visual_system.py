from pathlib import Path


def test_root_portal_uses_classic_project_site_structure():
    text = Path("site-root/index.html").read_text(encoding="utf-8")
    for marker in [
        'class="networkbar"',
        'class="masthead"',
        'class="site-search"',
        'class="primary-nav"',
        'class="release-callout"',
        'class="news-list"',
        'class="feature-list"',
        'class="site-footer"',
        'Bashref 2.1.0',
        '214 bilingual records',
    ]:
        assert marker in text


def test_docs_theme_uses_classic_nmap_like_chrome():
    for path in [
        Path("docs/en/assets/stylesheets/extra.css"),
        Path("docs/fa/assets/stylesheets/extra.css"),
    ]:
        text = path.read_text(encoding="utf-8")
        for marker in [
            "--bashref-navy",
            "--bashref-link",
            ".md-header",
            ".md-tabs",
            ".md-main",
            ".md-content",
            ".md-footer",
            ".bashref-utilitybar",
        ]:
            assert marker in text


def test_override_adds_project_utility_links():
    text = Path("overrides/main.html").read_text(encoding="utf-8")
    assert 'class="bashref-utilitybar"' in text
    assert "GitHub" in text
    assert "GNU Bash" in text
    assert "ShellCheck" in text
