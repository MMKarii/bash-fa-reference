from __future__ import annotations

import argparse

TEMPLATE = '''class Bashref < Formula
  include Language::Python::Virtualenv

  desc "Offline bilingual Bash reference CLI"
  homepage "https://mmkarii.github.io/bash-fa-reference/"
  url "{url}"
  sha256 "{sha256}"
  version "{version}"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_create(libexec, "python3.13")
    system libexec/"bin/pip", "install", "."
    bin.install_symlink libexec/"bin/bashref"
    man1.install "man/bashref.1"
    man5.install "man/bashref-reference.5"
    bash_completion.install "packaging/completions/bash/bashref"
    zsh_completion.install "packaging/completions/zsh/_bashref"
    fish_completion.install "packaging/completions/fish/bashref.fish"
  end

  test do
    assert_match "bashref {version}", shell_output("#{bin}/bashref --version")
  end
end
'''


def render_formula(version: str, url: str, sha256: str) -> str:
    if len(sha256) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in sha256):
        raise ValueError("sha256 must be a 64-character hexadecimal digest")
    if not url.startswith("https://"):
        raise ValueError("Homebrew source URL must use https")
    return TEMPLATE.format(version=version, url=url, sha256=sha256.lower())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args(argv)
    print(render_formula(args.version, args.url, args.sha256), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
