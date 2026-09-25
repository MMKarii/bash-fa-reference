from __future__ import annotations

import argparse
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

try:
    from tools.build_deb import stage_system_payload
except ModuleNotFoundError:
    from build_deb import stage_system_payload


SPEC_TEMPLATE = """Name: bashref
Version: {version}
Release: 1%{{?dist}}
Summary: Offline bilingual Bash reference CLI
License: MIT AND CC-BY-4.0
BuildArch: noarch
Source0: {source_name}
Requires: python3 >= 3.10

%description
Offline bilingual Bash reference CLI and generated reference data.

%prep
%setup -q -c -T
tar -xzf %{{SOURCE0}}

%build

%install
mkdir -p %{{buildroot}}
cp -a root/* %{{buildroot}}/

%files
%{{_bindir}}/bashref
/usr/lib/bashref/bashref
%{{_mandir}}/man1/bashref.1*
%{{_mandir}}/man5/bashref-reference.5*
%{{_datadir}}/bash-completion/completions/bashref
%{{_datadir}}/zsh/vendor-completions/_bashref
%{{_datadir}}/fish/vendor_completions.d/bashref.fish
%{{_datadir}}/doc/bashref/LICENSE-MIT
%{{_datadir}}/doc/bashref/LICENSE-CC-BY-4.0

%changelog
* Fri Sep 25 2026 MMKarii - {version}-1
- Bashref v2 package
"""


def render_spec(version: str, source_name: str) -> str:
    return SPEC_TEMPLATE.format(version=version, source_name=source_name)


def build_rpm(version: str, out_dir: Path = Path("dist")) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if shutil.which("rpmbuild") is None:
        raise RuntimeError("rpmbuild is not installed")

    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        stage = temp / "root"
        stage.mkdir()
        stage_system_payload(stage, version)

        build_root = temp / "rpmbuild"
        for name in ("BUILD", "BUILDROOT", "RPMS", "SOURCES", "SPECS", "SRPMS"):
            (build_root / name).mkdir(parents=True, exist_ok=True)

        source_name = f"bashref-{version}-package.tar.gz"
        source = build_root / "SOURCES" / source_name
        with tarfile.open(source, "w:gz") as tf:
            tf.add(stage, arcname="root")

        spec = build_root / "SPECS/bashref.spec"
        spec.write_text(render_spec(version, source_name), encoding="utf-8")
        subprocess.run(
            ["rpmbuild", "--define", f"_topdir {build_root.resolve()}", "-bb", str(spec)],
            check=True,
        )
        candidates = list((build_root / "RPMS").rglob("bashref-*.noarch.rpm"))
        if not candidates:
            raise RuntimeError("rpmbuild did not produce a noarch RPM")
        target = out_dir / candidates[0].name
        shutil.copy2(candidates[0], target)
        return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="2.1.0")
    parser.add_argument("--out-dir", type=Path, default=Path("dist"))
    args = parser.parse_args(argv)
    print(build_rpm(args.version, args.out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
