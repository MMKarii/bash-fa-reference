import tempfile
import unittest
from pathlib import Path

from scripts.check_built_site import check_html_file

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

    def test_local_img_requires_alt(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "index.html"
            p.write_text(GOOD.replace(' alt="Meaningful alt"', ""))
            self.assertTrue(any("img alt" in x for x in check_html_file(p)))


if __name__ == "__main__":
    unittest.main()
