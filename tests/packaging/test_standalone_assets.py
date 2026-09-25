import tarfile
import zipfile
from pathlib import Path

from tools.package_standalone import archive_name, build_standalone_archive


def test_archive_names_are_stable():
    assert archive_name("2.1.0", "linux", "x86_64") == "bashref-2.1.0-linux-x86_64.tar.gz"
    assert archive_name("2.1.0", "macos", "arm64") == "bashref-2.1.0-macos-arm64.tar.gz"
    assert archive_name("2.1.0", "windows", "x86_64") == "bashref-2.1.0-windows-x86_64.zip"


def test_linux_archive_contains_executable(tmp_path: Path):
    binary = tmp_path / "bashref"
    binary.write_bytes(b"standalone")
    binary.chmod(0o755)
    output = build_standalone_archive(binary, "2.1.0", "linux", "x86_64", tmp_path / "out")
    with tarfile.open(output, "r:gz") as archive:
        member = archive.getmember("bashref")
        assert member.mode & 0o111
        assert archive.extractfile(member).read() == b"standalone"


def test_windows_archive_contains_exe(tmp_path: Path):
    binary = tmp_path / "bashref.exe"
    binary.write_bytes(b"standalone")
    output = build_standalone_archive(binary, "2.1.0", "windows", "x86_64", tmp_path / "out")
    with zipfile.ZipFile(output) as archive:
        assert archive.namelist() == ["bashref.exe"]
        assert archive.read("bashref.exe") == b"standalone"
