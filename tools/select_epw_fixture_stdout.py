from __future__ import annotations

import argparse
import shutil
from pathlib import Path

EXPECTED_PATTERN = "test.out.*.inp=epw1.in.args=3"


class EpwStdoutSelectionError(RuntimeError):
    """Raised when the upstream EPW stdout cannot be selected unambiguously."""


def select_epw_stdout(fixture_root: Path) -> Path:
    """Return the one deterministic upstream EPW stdout for ``epw1.in``.

    QE's test-suite names outputs from the exact input and argument tuple.  This
    selector deliberately uses that filename contract instead of inspecting
    file contents.  Missing, empty, or ambiguous outputs fail closed.
    """

    root = Path(fixture_root)
    candidates = sorted(
        path
        for path in root.glob(EXPECTED_PATTERN)
        if path.is_file() and path.stat().st_size > 0
    )
    if len(candidates) != 1:
        rendered = ", ".join(path.name for path in candidates) or "none"
        raise EpwStdoutSelectionError(
            f"expected exactly one nonempty {EXPECTED_PATTERN!r} output in "
            f"{root}, found {len(candidates)}: {rendered}"
        )
    return candidates[0]


def preserve_epw_stdout(fixture_root: Path, destination: Path) -> Path:
    """Copy the deterministic EPW stdout to immutable evidence storage."""

    source = select_epw_stdout(fixture_root)
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    target.with_suffix(target.suffix + ".source-path.txt").write_text(
        str(source) + "\n", encoding="utf-8"
    )
    return source


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preserve the deterministic QE test-suite epw1 stdout."
    )
    parser.add_argument("--fixture-root", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()
    source = preserve_epw_stdout(args.fixture_root, args.destination)
    print(source)


if __name__ == "__main__":
    main()
