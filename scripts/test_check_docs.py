import tempfile
import unittest
from pathlib import Path

from scripts.check_docs import (
    compare_language_structure,
    evaluate_translation_drift,
    find_broken_local_anchors,
    find_broken_local_links,
    find_public_safety_issues,
    slugify_heading,
)


class DocsChecksTests(unittest.TestCase):
    def test_detects_missing_relative_markdown_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text("[Missing](missing.md)\n", encoding="utf-8")
            self.assertEqual(len(find_broken_local_links(root)), 1)

    def test_ignores_external_link_for_file_existence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text("[Web](https://example.org/)\n", encoding="utf-8")
            self.assertEqual(find_broken_local_links(root), [])

    def test_language_structure_must_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fa = root / "fa"
            en = root / "en"
            fa.mkdir()
            en.mkdir()
            (fa / "index.md").write_text("# fa\n")
            (en / "index.md").write_text("# en\n")
            (fa / "01.md").write_text("# fa\n")
            self.assertEqual(compare_language_structure(fa, en), ([], ["01.md"]))

    def test_slugify_heading_handles_latin_and_persian(self):
        self.assertEqual(slugify_heading("Bash Fundamentals"), "bash-fundamentals")
        self.assertEqual(slugify_heading("مبانی Bash"), "مبانی-bash")

    def test_local_anchor_must_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.md").write_text("# موجود\n\n[Missing](#ناموجود)\n", encoding="utf-8")
            self.assertEqual(find_broken_local_anchors(root), ["index.md: #ناموجود"])

    def test_translation_drift_thresholds(self):
        self.assertEqual(evaluate_translation_drift(30), "ok")
        self.assertEqual(evaluate_translation_drift(31), "warning")
        self.assertEqual(evaluate_translation_drift(91), "error")

    def test_high_risk_pattern_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "en").mkdir(parents=True)
            (root / "docs" / "en" / "index.md").write_text("rm -rf / # never do this\n", encoding="utf-8")
            self.assertTrue(find_public_safety_issues(root))


if __name__ == "__main__":
    unittest.main()
