from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "research/programs/empirical_bandgap/state.md"


def test_r01_state_is_not_a_placeholder_or_truncated() -> None:
    text = STATE_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    assert text.startswith("# Program state: empirical bandgap reconstruction\n")
    assert text.strip() != "hello"
    assert len(text.encode("utf-8")) > 20_000
    assert len(lines) > 500


def test_r01_state_retains_major_source_sections() -> None:
    text = STATE_PATH.read_text(encoding="utf-8")
    required_sections = {
        "## Hansen reconstruction state",
        "## Seiler 1990 source reconstruction",
        "## Camassel 1988 Cd-rich source reconstruction",
        "## Scott 1969 fixed-absorption optical-edge source audit",
        "## Blue 1964 theory-conditioned optical-gap reconstruction",
        "## Blue 1964 signed-gap non-commensurability certificate",
        "## Groves 1967 signed HgTe magnetoreflection endpoint audit",
        "## Schmit and Stelzer 1969 Table III detector-cutoff reconstruction",
        "## Finkman and Nemirovsky 1979 optical-absorption source audit",
    }
    missing = sorted(section for section in required_sections if section not in text)
    assert not missing, f"R01 state lost required sections: {missing}"


def test_r01_state_retains_program_boundaries() -> None:
    text = STATE_PATH.read_text(encoding="utf-8")
    assert "**Portfolio contribution:** R01" in text
    assert "## Manuscript status" in text
    assert "No active manuscript is recorded for this program." in text
    assert "not a production equation" in text
    assert "production-equation, manuscript, or submission readiness" in text
