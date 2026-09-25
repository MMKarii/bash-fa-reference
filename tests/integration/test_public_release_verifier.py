from tools.verify_public_release import snapshot_name, verify_release


def complete_release(version: str = "2.1.0"):
    names = [
        f"bashref-{version}-py3-none-any.whl",
        f"bashref-{version}.tar.gz",
        f"bashref_{version}_all.deb",
        f"bashref-{version}-1.noarch.rpm",
        f"bashref-{version}-portable.tar.gz",
        f"bashref-{version}-manpages.tar.gz",
        f"bashref-{version}-completions.tar.gz",
        f"bashref-{version}-docs.tar.gz",
        f"bashref-{version}-linux-x86_64.tar.gz",
        f"bashref-{version}-macos-arm64.tar.gz",
        f"bashref-{version}-macos-x86_64.tar.gz",
        f"bashref-{version}-windows-x86_64.zip",
        "bashref.rb",
        "SHA256SUMS",
    ]
    return {
        "tag_name": f"v{version}",
        "draft": True,
        "assets": [{"name": name} for name in names],
    }, names


def checksum_text(names):
    return "\n".join(
        f"{'0' * 64}  {name}" for name in names if name != "SHA256SUMS"
    ) + "\n"


def good_fetcher(url: str) -> str:
    return "<html><body>Bashref 2.1.0</body></html>"


def test_snapshot_name_uses_major_minor():
    assert snapshot_name("2.1.0") == "v2.1"
    assert snapshot_name("10.4.7") == "v10.4"


def test_complete_release_passes():
    release, names = complete_release()
    assert verify_release(release, checksum_text(names), good_fetcher) == []


def test_missing_standalone_binary_is_reported():
    release, names = complete_release()
    release["assets"] = [
        asset for asset in release["assets"]
        if asset["name"] != "bashref-2.1.0-windows-x86_64.zip"
    ]
    issues = verify_release(release, checksum_text(names), good_fetcher)
    assert any("windows-x86_64" in issue for issue in issues)


def test_missing_wheel_is_reported():
    release, names = complete_release()
    release["assets"] = [
        asset for asset in release["assets"]
        if not asset["name"].endswith("-py3-none-any.whl")
    ]
    issues = verify_release(release, checksum_text(names), good_fetcher)
    assert any("py3-none-any.whl" in issue for issue in issues)


def test_checksum_omission_is_reported():
    release, names = complete_release()
    checksums = checksum_text([name for name in names if "portable" not in name])
    issues = verify_release(release, checksums, good_fetcher)
    assert any("portable" in issue and "SHA256SUMS" in issue for issue in issues)


def test_stale_pages_marker_is_reported():
    release, names = complete_release()
    issues = verify_release(release, checksum_text(names), lambda url: "Bashref 2.0.0")
    assert any("release marker" in issue for issue in issues)


def test_verifier_checks_v21_snapshot_paths():
    release, names = complete_release()
    requested = []

    def fetch(url: str) -> str:
        requested.append(url)
        return "Bashref 2.1.0"

    assert verify_release(release, checksum_text(names), fetch) == []
    assert any("/v2.1/en/" in url for url in requested)
    assert any("/v2.1/fa/" in url for url in requested)
