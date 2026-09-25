from tools.verify_public_release import verify_release


def complete_release():
    version = "2.0.0"
    names = [
        f"bashref-{version}-py3-none-any.whl",
        f"bashref-{version}.tar.gz",
        f"bashref_{version}_all.deb",
        f"bashref-{version}-1.noarch.rpm",
        f"bashref-{version}-portable.tar.gz",
        f"bashref-{version}-manpages.tar.gz",
        f"bashref-{version}-completions.tar.gz",
        f"bashref-{version}-docs.tar.gz",
        "bashref.rb",
        "SHA256SUMS",
    ]
    return {
        "tag_name": "v2.0.0",
        "draft": True,
        "assets": [{"name": name} for name in names],
    }, names


def checksum_text(names):
    return "\n".join(
        f"{'0' * 64}  {name}" for name in names if name != "SHA256SUMS"
    ) + "\n"


def good_fetcher(url: str) -> str:
    return "<html><body>Bashref 2.0.0</body></html>"


def test_complete_release_passes():
    release, names = complete_release()
    assert verify_release(release, checksum_text(names), good_fetcher) == []


def test_missing_wheel_is_reported():
    release, names = complete_release()
    release["assets"] = [
        asset for asset in release["assets"]
        if not asset["name"].endswith("-py3-none-any.whl")
    ]
    issues = verify_release(release, checksum_text(names), good_fetcher)
    assert any("wheel" in issue or "py3-none-any.whl" in issue for issue in issues)


def test_checksum_omission_is_reported():
    release, names = complete_release()
    checksums = checksum_text([name for name in names if "portable" not in name])
    issues = verify_release(release, checksums, good_fetcher)
    assert any("portable" in issue and "SHA256SUMS" in issue for issue in issues)


def test_stale_pages_marker_is_reported():
    release, names = complete_release()
    issues = verify_release(release, checksum_text(names), lambda url: "Bashref 1.0.0")
    assert any("release marker" in issue for issue in issues)
