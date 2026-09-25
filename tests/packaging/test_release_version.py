import pytest

from tools.release_version import assert_release_version, normalize_tag


def test_exact_v2_release_matches():
    assert_release_version("v2.0.0", "2.0.0")


def test_normalize_tag_returns_package_version():
    assert normalize_tag("v2.0.0") == "2.0.0"


def test_version_mismatch_is_rejected():
    with pytest.raises(ValueError):
        assert_release_version("v2.0.1", "2.0.0")


def test_malformed_tag_is_rejected():
    with pytest.raises(ValueError):
        normalize_tag("release-2")
