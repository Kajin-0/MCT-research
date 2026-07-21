from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "data" / "validation" / "flagship_novelty_claim_matrix.json"
AUDIT_PATH = (
    ROOT
    / "literature"
    / "prior_art"
    / "2026-07-21-flagship-rank-theorem-audit.md"
)
DECISION_PATH = (
    ROOT
    / "research"
    / "decision_records"
    / "2026-07-21-flagship-publication-framing.md"
)
MANUSCRIPT_PATH = (
    ROOT / "manuscript" / "distributional_band_edge" / "manuscript_draft.md"
)
CLAIM_MATRIX_PATH = (
    ROOT / "manuscript" / "distributional_band_edge" / "claim_matrix.md"
)
README_PATH = ROOT / "manuscript" / "distributional_band_edge" / "README.md"
ACTIVE_STATE_PATH = ROOT / "research" / "active_program_state.md"

REQUIRED_DOIS = {
    "10.1016/0025-5564(70)90132-X",
    "10.1016/j.automatica.2009.07.009",
    "10.1016/j.mbs.2014.08.008",
    "10.1351/goldbook.B00626",
    "10.1364/AO.36.008238",
    "10.1364/AO.40.002675",
    "10.1364/AO.40.002682",
    "10.1364/OL.418277",
    "10.1016/0022-0248(92)90851-9",
    "10.1063/1.2245220",
    "10.1007/s11664-007-0162-0",
    "10.1016/0038-1098(85)90315-1",
}

EXPECTED_CLASSES = {
    "red": {"N01", "N02", "N03", "N08"},
    "yellow": {"N04", "N05", "N07", "N09", "N13"},
    "green": {"N06", "N10", "N11", "N12"},
}


def load_matrix() -> dict[str, object]:
    with MATRIX_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_novelty_matrix_schema_and_unique_claims() -> None:
    matrix = load_matrix()
    assert matrix["schema_version"] == "1.0"
    assert matrix["program_issue"] == 189

    claims = matrix["claims"]
    assert isinstance(claims, list)
    assert len(claims) == 13
    identifiers = [claim["id"] for claim in claims]
    assert identifiers == [f"N{index:02d}" for index in range(1, 14)]
    assert len(set(identifiers)) == len(identifiers)

    allowed = set(matrix["classifications"])
    assert allowed == {"red", "yellow", "green"}
    assert all(claim["classification"] in allowed for claim in claims)
    assert all(claim["authorized"] for claim in claims)
    assert all(claim["prohibited"] for claim in claims)


def test_fixed_novelty_classifications() -> None:
    matrix = load_matrix()
    by_class: dict[str, set[str]] = {name: set() for name in EXPECTED_CLASSES}
    for claim in matrix["claims"]:
        by_class[claim["classification"]].add(claim["id"])
    assert by_class == EXPECTED_CLASSES


def test_prior_art_doi_coverage() -> None:
    matrix = load_matrix()
    prior_art = matrix["prior_art"]
    dois = {entry["doi"] for entry in prior_art}
    assert dois == REQUIRED_DOIS
    assert len({entry["key"] for entry in prior_art}) == len(prior_art)
    assert all(entry["boundary"] for entry in prior_art)


def test_publication_framing_is_fixed() -> None:
    matrix = load_matrix()
    framing = matrix["publication_framing"]
    assert (
        framing["selected"]
        == "HgCdTe-specific semiconductor optical metrology and inverse-problem methods paper"
    )
    not_claimed = set(framing["not_claimed"])
    assert "new general structural-identifiability theory" in not_claimed
    assert "new universal HgCdTe bandgap equation" in not_claimed
    assert "complete external specimen-spectrum validation" in not_claimed


def test_audit_and_decision_files_preserve_general_prior_art_boundary() -> None:
    audit = AUDIT_PATH.read_text(encoding="utf-8")
    decision = DECISION_PATH.read_text(encoding="utf-8")
    for text in (audit, decision):
        assert "structural identifiability" in text.lower()
        assert "Beer-Lambert" in text
        assert "application-specific" in text
        assert "HgCdTe-specific semiconductor optical-metrology" in text
    for doi in REQUIRED_DOIS:
        assert doi in audit


def test_manuscript_uses_audited_language() -> None:
    draft = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    required = (
        "apply established structural-identifiability methods",
        "application-specific structural-identifiability bound",
        "inherits the standard optical-depth product dependence",
        "not a new general theory of structural identifiability",
        "not a fit to the Dingrong specimen",
        "not the Dingrong free-carrier absorption law",
        "11.297 meV",
        "0.785 meV",
        "data/validation/dingrong1985_table1_reproduction.json",
        "data/validation/flagship_novelty_claim_matrix.json",
    )
    for phrase in required:
        assert phrase in draft

    prohibited = (
        "The unified rank theorem is the new synthesis",
        "We introduce a new structural-identifiability theory",
        "We discover that detector cutoff depends on thickness",
        "The universal HgCdTe momentum matrix is 8.51",
        "The Dingrong sensitivity calculation is zero-temperature and does not reproduce",
    )
    for phrase in prohibited:
        assert phrase not in draft


def test_claim_matrix_separates_exactness_from_novelty() -> None:
    text = CLAIM_MATRIX_PATH.read_text(encoding="utf-8")
    assert "does **not** assert unprecedented general mathematics" in text
    assert "Established ingredients — do not claim novelty" in text
    assert "Application-specific analytical contributions" in text
    assert "Strong project-specific quantitative findings" in text
    for claim_id in range(1, 24):
        assert f"C{claim_id:02d}" in text


def test_readme_and_active_state_match_merged_source_state() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    active = ACTIVE_STATE_PATH.read_text(encoding="utf-8")

    for text in (readme, active):
        assert "Dingrong Table 1" in text
        assert "11.297 meV" in text
        assert "HgCdTe-specific semiconductor optical-metrology" in text
        assert "new general structural-identifiability theory" in text
        assert "Chang 2007 Figure 1" in text or "Chang 2007 thickness curve" in text

    assert "**Active milestone:** #189" in active
    assert "This is the sole controlling research ledger" in active
    assert "PR #188" in active
    assert "complete CI and merge Issue #189" in active


def test_no_novelty_status_is_treated_as_global_proof() -> None:
    matrix = load_matrix()
    limitations = " ".join(matrix["limitations"]).lower()
    assert "targeted" in limitations
    assert "revised" in limitations
    assert "not unprecedented mathematics" in limitations
