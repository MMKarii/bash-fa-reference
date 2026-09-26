from pathlib import Path


def test_root_portal_matches_nmap_visual_skeleton():
    text = Path("site-root/index.html").read_text(encoding="utf-8")
    for marker in [
        'class="masthead"',
        'class="masthead-top"',
        'class="brand-logo"',
        'class="project-links"',
        'class="site-search"',
        'class="primary-nav"',
        'class="release-callout"',
        'class="section-bar">News',
        'Bashref is ...',
        'class="footer-grid"',
        'Get Bashref 2.1.0 here',
        '214 bilingual records',
    ]:
        assert marker in text
    assert 'class="sidebar"' not in text
    assert "--purple:#2b003d" in text


def test_root_portal_preserves_all_stable_snapshot_links():
    text = Path("site-root/index.html").read_text(encoding="utf-8")
    for href in [
        'href="v2.1/en/"', 'href="v2.1/fa/"',
        'href="v2.0/en/"', 'href="v2.0/fa/"',
        'href="v1.0/en/"', 'href="v1.0/fa/"',
    ]:
        assert href in text


def test_docs_theme_uses_nmap_purple_chrome_and_section_bars():
    for path in [
        Path("docs/en/assets/stylesheets/extra.css"),
        Path("docs/fa/assets/stylesheets/extra.css"),
    ]:
        text = path.read_text(encoding="utf-8")
        for marker in [
            "--bashref-purple",
            "#2b003d",
            ".bashref-utilitybar",
            ".md-header",
            ".md-tabs",
            ".md-search__form",
            ".md-typeset h2",
            "text-align: center",
            ".md-footer",
        ]:
            assert marker in text
        assert "--bashref-navy" not in text


def test_override_preserves_project_links_and_language_switch():
    text = Path("overrides/main.html").read_text(encoding="utf-8")
    assert 'class="bashref-utilitybar"' in text
    assert "GitHub" in text
    assert "GNU Bash" in text
    assert "ShellCheck" in text
    assert "English" in text
    assert "فارسی" in text
