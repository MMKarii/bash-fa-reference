import unittest
from types import SimpleNamespace

from hooks.language_links import _published_url, on_page_context


class LanguageLinksTests(unittest.TestCase):
    def test_published_url_maps_matching_page(self):
        self.assertEqual(
            _published_url("en", "03-variables-expansion-quoting/"),
            "https://mmkarii.github.io/bash-fa-reference/en/03-variables-expansion-quoting/",
        )

    def test_home_page_maps_to_language_root(self):
        self.assertEqual(
            _published_url("fa", ""),
            "https://mmkarii.github.io/bash-fa-reference/fa/",
        )

    def test_generated_reference_maps_to_same_record_peer(self):
        context = {}
        page = SimpleNamespace(
            url="reference/generated/builtins/printf/",
            meta={"record_id": "builtin.printf", "reference_kind": "builtin"},
        )
        config = SimpleNamespace(extra={})
        on_page_context(context, page=page, config=config, nav=None)
        self.assertEqual(
            config.extra["alternate"][0]["link"],
            "https://mmkarii.github.io/bash-fa-reference/fa/reference/generated/builtins/printf/",
        )
        self.assertEqual(
            config.extra["alternate"][1]["link"],
            "https://mmkarii.github.io/bash-fa-reference/en/reference/generated/builtins/printf/",
        )

    def test_page_context_sets_bilingual_matching_links(self):
        context = {}
        page = SimpleNamespace(url="cheatsheet/")
        config = SimpleNamespace(extra={})
        result = on_page_context(context, page=page, config=config, nav=None)
        self.assertIs(result, context)
        self.assertEqual(
            config.extra["alternate"],
            [
                {
                    "name": "فارسی",
                    "link": "https://mmkarii.github.io/bash-fa-reference/fa/cheatsheet/",
                    "lang": "fa",
                },
                {
                    "name": "English",
                    "link": "https://mmkarii.github.io/bash-fa-reference/en/cheatsheet/",
                    "lang": "en",
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
