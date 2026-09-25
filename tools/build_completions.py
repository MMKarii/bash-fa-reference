from __future__ import annotations

from pathlib import Path

from bashref.completion import completion_script

OUTPUTS = {
    "bash": Path("packaging/completions/bash/bashref"),
    "zsh": Path("packaging/completions/zsh/_bashref"),
    "fish": Path("packaging/completions/fish/bashref.fish"),
}


def build_completions(outputs: dict[str, Path] | None = None) -> list[Path]:
    targets = OUTPUTS if outputs is None else outputs
    written: list[Path] = []
    for shell, path in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        text = completion_script(shell)
        if not text.endswith("\n"):
            text += "\n"
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def main() -> int:
    paths = build_completions()
    print(f"Generated {len(paths)} completion file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
