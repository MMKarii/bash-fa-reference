import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError

from scripts.check_external_links import (
    _ascii_url,
    check_url,
    classify_http_status,
    collect_external_links,
    is_warning_only_url,
)


class _Response:
    def __init__(self, status=200):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class ExternalLinkTests(unittest.TestCase):
    def test_status_classification(self):
        for status, state in [(200, "ok"), (301, "ok"), (403, "warning"), (429, "warning"), (404, "error"), (410, "error"), (500, "warning")]:
            self.assertEqual(classify_http_status(status), state)

    def test_project_pages_urls_are_not_allowlisted(self):
        self.assertFalse(is_warning_only_url("https://mmkarii.github.io/bash-fa-reference/"))
        self.assertTrue(is_warning_only_url("https://github.com/MMKarii/bash-fa-reference"))

    def test_collects_plain_urls_from_config_and_metadata(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github").mkdir()
            (root / "mkdocs.fa.yml").write_text("repo_url: https://github.com/MMKarii/bash-fa-reference\n", encoding="utf-8")
            (root / ".github" / "repository-metadata.md").write_text(
                "Website: https://github.com/MMKarii/bash-fa-reference/blob/main/docs/fa/index.md\n", encoding="utf-8"
            )
            links = collect_external_links(root)
            self.assertIn("https://github.com/MMKarii/bash-fa-reference", links)

    def test_inline_code_url_does_not_include_backtick(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "Run `curl https://example.com` for a documentation example.\n",
                encoding="utf-8",
            )
            links = collect_external_links(root)
            self.assertIn("https://example.com", links)
            self.assertNotIn("https://example.com`", links)

    def test_unicode_url_is_ascii_encoded(self):
        _ascii_url("https://example.test/راهنما?q=بش").encode("ascii")

    def test_success(self):
        self.assertEqual(check_url("https://example.test/", opener=lambda *_a, **_k: _Response(200))[0], "ok")

    def test_404_fails(self):
        def opener(request, timeout=0):
            raise HTTPError(request.full_url, 404, "Not Found", {}, io.BytesIO())
        self.assertEqual(check_url("https://example.test/missing", opener=opener, retries=0)[0], "error")

    def test_transient_warns(self):
        def opener(_request, timeout=0):
            raise URLError("temporary DNS failure")
        self.assertEqual(check_url("https://example.test/transient", opener=opener, retries=0)[0], "warning")


if __name__ == "__main__":
    unittest.main()
