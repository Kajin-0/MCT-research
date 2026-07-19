from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT_MATTER = ROOT / (
    "manuscript/observation_model_uncertainty/irpt_submission_front_matter.md"
)
TEXT = FRONT_MATTER.read_text(encoding="utf-8")


def _section(name: str, next_name: str) -> str:
    start = TEXT.index(f"## {name}") + len(f"## {name}")
    end = TEXT.index(f"## {next_name}", start)
    return TEXT[start:end].strip()


def test_irpt_abstract_is_within_250_words() -> None:
    section = _section("Abstract", "Keywords")
    abstract, declared = section.split("**Word count:**", 1)
    words = re.findall(r"\b[\w−–-]+(?:\.[\w]+)?\b", abstract)
    declared_count = int(declared.strip())
    assert declared_count == len(words)
    assert len(words) <= 250
    assert "6.414" in abstract
    assert "6.830" in abstract
    assert "0.891" in abstract
    assert "0.177–0.255" in abstract


def test_irpt_keywords_meet_count_gate() -> None:
    keywords = [
        item.strip()
        for item in _section("Keywords", "Highlights").split(";")
        if item.strip()
    ]
    assert 1 <= len(keywords) <= 7
    assert keywords == [
        "HgCdTe",
        "infrared absorption",
        "band gap",
        "optical spectroscopy",
        "uncertainty",
        "identifiability",
        "photodetectors",
    ]


def test_irpt_highlights_are_three_to_five_and_at_most_85_characters() -> None:
    block = _section("Highlights", "Data availability statement")
    highlights = [
        line.removeprefix("- ")
        for line in block.splitlines()
        if line.startswith("- ")
    ]
    assert 3 <= len(highlights) <= 5
    assert all(len(item) <= 85 for item in highlights)
    assert any("6.4–6.8 meV" in item for item in highlights)
    assert any("0.9 meV" in item for item in highlights)


def test_irpt_required_declarations_are_present_and_fail_closed() -> None:
    for heading in (
        "## Data availability statement",
        "## Declaration of generative AI and AI-assisted technologies",
        "## CRediT author statement",
        "## Funding",
        "## Declaration of competing interests",
        "## Acknowledgments",
        "## Suggested reviewers",
    ):
        assert heading in TEXT
    assert "OpenAI ChatGPT" in TEXT
    assert "[AUTHOR NAMES REQUIRED]" in TEXT
    assert "[FUNDING STATEMENT REQUIRED" in TEXT
    assert "[COMPETING-INTEREST STATEMENT REQUIRED" in TEXT
    assert "[INSERT PUBLIC ARCHIVE DOI OR FINAL REPOSITORY URL" in TEXT
