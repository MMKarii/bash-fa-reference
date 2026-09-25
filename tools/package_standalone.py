from __future__ import annotations

import argparse
import gzip
import io
import tarfile
import zipfile
from pathlib import Path

_PLATFORMS = {"linux", "macos", "windows"}
_ARCHES = {"x86_64", "arm64"}


def archive_name(version: str, platform_name: str, arch: str) -> str:
    if platform_name not in _PLATFORMS:
        raise ValueError(f"unsupported platform: {platform_name}")
    if arch not in _ARCHES:
        raise ValueError(f"unsupported architecture: {arch}")
    suffix = ".zip" if platform_name == "windows" else ".tar.gz"
    return f"bashref-{version}-{platform_name}-{arch}{suffix}"


def build_standalone_archive(
    binary: Path,
    version: str,
    platform_name: str,
    arch: str,
    out_dir: Path,
) -> Path:
    if not binary.is_file():
        raise FileNotFoundError(binary)
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / archive_name(version, platform_name, arch)
    member_name = "bashref.exe" if platform_name == "windows" else "bashref"
    data = binary.read_bytes()

    if platform_name == "windows":
        info = zipfile.ZipInfo(member_name, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o755 << 16
        with zipfile.ZipFile(output, "w") as archive:
            archive.writestr(info, data)
        return output

    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as archive:
        info = tarfile.TarInfo(member_name)
        info.size = len(data)
        info.mode = 0o755
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        info.mtime = 0
        archive.addfile(info, io.BytesIO(data))
    tar_buffer.seek(0)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            compressed.write(tar_buffer.getvalue())
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--platform", dest="platform_name", choices=sorted(_PLATFORMS), required=True)
    parser.add_argument("--arch", choices=sorted(_ARCHES), required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("standalone-dist"))
    args = parser.parse_args(argv)
    output = build_standalone_archive(
        args.binary,
        args.version,
        args.platform_name,
        args.arch,
        args.out_dir,
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
