import json

import pytest

from tools.select_release import select_release_by_tag


def test_select_release_by_tag_finds_draft_release():
    releases = [
        {"id": 1, "tag_name": "v1.0.0", "draft": False},
        {"id": 2, "tag_name": "v2.0.0", "draft": True},
    ]
    assert select_release_by_tag(releases, "v2.0.0") == {
        "id": 2,
        "tag_name": "v2.0.0",
        "draft": True,
    }


def test_select_release_by_tag_rejects_missing_tag():
    with pytest.raises(LookupError):
        select_release_by_tag([], "v2.0.0")
