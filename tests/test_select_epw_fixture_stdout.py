from __future__ import annotations

from pathlib import Path

import pytest

from tools.select_epw_fixture_stdout import (
    EpwStdoutSelectionError,
    preserve_epw_stdout,
    select_epw_stdout,
)


def _epw_output(root: Path, run_id: str, text: str = "EPW output\n") -> Path:
    path = root / f"test.out.{run_id}.inp=epw1.in.args=3"
    path.write_text(text, encoding="utf-8")
    return path


def test_selects_exact_upstream_epw1_output(tmp_path: Path) -> None:
    expected = _epw_output(tmp_path, "220726")
    (tmp_path / "test.out.220726.inp=scf.in.args=1").write_text(
        "PW output\n", encoding="utf-8"
    )
    assert select_epw_stdout(tmp_path) == expected


def test_preserves_output_before_fixture_cleanup(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture"
    evidence = tmp_path / "evidence" / "epw1.stdout.txt"
    fixture.mkdir()
    source = _epw_output(fixture, "220726", "immutable EPW stdout\n")

    selected = preserve_epw_stdout(fixture, evidence)
    source.unlink()

    assert selected.name == "test.out.220726.inp=epw1.in.args=3"
    assert evidence.read_text(encoding="utf-8") == "immutable EPW stdout\n"
    assert evidence.with_suffix(".txt.source-path.txt").read_text(
        encoding="utf-8"
    ).strip().endswith(selected.name)


def test_missing_output_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(EpwStdoutSelectionError, match="found 0"):
        select_epw_stdout(tmp_path)


def test_empty_output_fails_closed(tmp_path: Path) -> None:
    _epw_output(tmp_path, "220726", "")
    with pytest.raises(EpwStdoutSelectionError, match="found 0"):
        select_epw_stdout(tmp_path)


def test_ambiguous_outputs_fail_closed(tmp_path: Path) -> None:
    _epw_output(tmp_path, "220726")
    _epw_output(tmp_path, "220727")
    with pytest.raises(EpwStdoutSelectionError, match="found 2"):
        select_epw_stdout(tmp_path)
