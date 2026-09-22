import tempfile
import unittest
from pathlib import Path

from scripts.check_built_site import check_built_links, check_html_file

GOOD = """<!doctype html><html lang="en"><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Useful description">
<meta property="og:title" content="Example">
<link rel="canonical" href="https://example.test/">
<title>Example</title></head><body>
<img src="asset.png" alt="Meaningful alt">
</body></html>"""


class BuiltSiteTests(unittest.TestCase):
    def test_valid_page_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "index.html"
            p.write_text(GOOD)
            self.assertEqual(check_html_file(p), [])

    def test_missing_metadata_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "index.html"
            p.write_text("<html><head></head><body></body></html>")
            issues = check_html_file(p)
            self.assertTrue(any("description" in x for x in issues))
            self.assertTrue(any("canonical" in x for x in issues))

    def test_404_page_does_not_require_canonical(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "404.html"
            p.write_text(
                GOOD.replace('<link rel="canonical" href="https://example.test/">', ""),
                encoding="utf-8",
            )
            self.assertFalse(any("canonical" in issue for issue in check_html_file(p)))

    def test_local_img_requires_alt(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "index.html"
            p.write_text(GOOD.replace(' alt="Meaningful alt"', ""))
            self.assertTrue(any("img alt" in x for x in check_html_file(p)))

    def test_built_local_link_and_anchor_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            section = root / "guide"
            section.mkdir()
            (root / "index.html").write_text(
                '<html><body><a href="guide/#topic">Guide</a></body></html>',
                encoding="utf-8",
            )
            (section / "index.html").write_text(
                '<html><body><h2 id="topic">Topic</h2></body></html>',
                encoding="utf-8",
            )
            self.assertEqual(check_built_links(root), [])

    def test_root_relative_link_uses_language_edition_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            en = root / "en"
            target = en / "guide"
            target.mkdir(parents=True)
            (en / "404.html").write_text(
                '<html><body><a href="/guide/#topic">Guide</a></body></html>',
                encoding="utf-8",
            )
            (target / "index.html").write_text(
                '<html><body><h2 id="topic">Topic</h2></body></html>',
                encoding="utf-8",
            )
            self.assertEqual(check_built_links(root), [])

    def test_project_prefixed_root_link_resolves_from_published_site_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "latest" / "en"
            target = root / "en" / "guide"
            source.mkdir(parents=True)
            target.mkdir(parents=True)
            (source / "404.html").write_text(
                '<html><body><a href="/bash-fa-reference/en/guide/#topic">Guide</a></body></html>',
                encoding="utf-8",
            )
            (target / "index.html").write_text(
                '<html><body><h2 id="topic">Topic</h2></body></html>',
                encoding="utf-8",
            )
            self.assertEqual(check_built_links(root), [])

    def test_root_relative_link_uses_versioned_language_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fa = root / "latest" / "fa"
            target = fa / "guide"
            target.mkdir(parents=True)
            (fa / "404.html").write_text(
                '<html><body><a href="/guide/">Guide</a></body></html>',
                encoding="utf-8",
            )
            (target / "index.html").write_text(
                '<html><body>Guide</body></html>',
                encoding="utf-8",
            )
            self.assertEqual(check_built_links(root), [])

    def test_built_missing_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<html><body><a href="missing/">Missing</a></body></html>',
                encoding="utf-8",
            )
            issues = check_built_links(root)
            self.assertTrue(any("broken local href target" in item for item in issues))

    def test_built_missing_anchor_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<html><body><a href="#missing">Missing anchor</a></body></html>',
                encoding="utf-8",
            )
            issues = check_built_links(root)
            self.assertTrue(any("missing local anchor" in item for item in issues))

    def test_external_links_are_not_treated_as_local(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<html><body><a href="https://example.org/path">External</a></body></html>',
                encoding="utf-8",
            )
            self.assertEqual(check_built_links(root), [])


if __name__ == "__main__":
    unittest.main()
