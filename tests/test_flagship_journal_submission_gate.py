from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "data" / "validation" / "flagship_journal_submission_gate.json"
REFS_PATH = (
    ROOT / "manuscript" / "distributional_band_edge" / "references_verified.json"
)
PACKAGE_PATH = (
    ROOT
    / "manuscript"
    / "distributional_band_edge"
    / "journal_submission"
    / "semiconductor_science_and_technology.md"
)
README_PATH = ROOT / "manuscript" / "distributional_band_edge" / "README.md"
SUBMISSION_GAP_PATH = (
    ROOT / "manuscript" / "distributional_band_edge" / "submission_gap.md"
)
ACTIVE_STATE_PATH = ROOT / "research" / "active_program_state.md"
DECISION_PATH = (
    ROOT
    / "research"
    / "decision_records"
    / "2026-07-21-flagship-journal-and-evidence-threshold.md"
)

REQUIRED_REFERENCE_DOIS = {
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
    "10.1038/ncomms12576",
    "10.1016/j.physb.2009.08.210",
    "10.1016/0020-0891(91)90110-2",
}


def load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_primary_venue_and_article_type_are_locked() -> None:
    gate = load_json(GATE_PATH)
    assert gate["schema_version"] == "1.0"
    assert gate["program_issue"] == 191
    primary = gate["primary_venue"]
    assert primary["journal"] == "Semiconductor Science and Technology"
    assert primary["article_type"] == "Paper"
    assert primary["status"] == "selected_primary"
    assert "theoretical" in " ".join(primary["scope_snapshot"])
    assert "new analytical techniques" in primary["scope_snapshot"]
    assert "simulation" in primary["scope_snapshot"]


def test_digitized_spectrum_is_not_initial_sst_blocker() -> None:
    gate = load_json(GATE_PATH)
    threshold = gate["primary_venue"]["initial_submission_evidence_threshold"]
    assert threshold["current_scientific_package_sufficient"] is True
    assert threshold["digitized_real_spectrum_required_before_submission"] is False
    assert gate["locked_decisions"]["digitization_before_initial_submission"] == "not required"
    assert gate["evidence_state"]["initial_submission_authorized_after_packaging"] is True
    assert gate["evidence_state"]["complete_native_spectrum_validation"] is False


def test_measurement_science_threshold_remains_stricter() -> None:
    gate = load_json(GATE_PATH)
    stretch = gate["stretch_venue"]
    assert stretch["journal"] == "Measurement Science and Technology"
    assert stretch["status"] == "not_ready_current_state"
    assert stretch["digitized_real_spectrum_required_before_submission"] is True
    required = set(stretch["minimum_additional_evidence"])
    assert "calibrated digitized or source-native spectrum" in required
    assert "digitization and measurement uncertainty" in required
    assert "comparison against a baseline extraction method" in required


def test_fallback_is_fixed_without_reopening_ranking() -> None:
    gate = load_json(GATE_PATH)
    fallback = gate["fallback_venue"]
    assert fallback["journal"] == "Journal of Applied Physics"
    assert fallback["status"] == "selected_fallback"
    assert fallback["digitized_real_spectrum_required_before_submission"] is False
    locked = set(gate["locked_decisions"]["do_not_reopen_without_new_evidence"])
    assert "exhaustive journal ranking" in locked
    assert "broad physical-model expansion" in locked


def test_verified_reference_manifest_is_complete_and_unique() -> None:
    manifest = load_json(REFS_PATH)
    assert manifest["schema_version"] == "1.0"
    references = manifest["references"]
    assert len(references) == len(REQUIRED_REFERENCE_DOIS)
    assert manifest["verification_complete"] is True

    dois = [entry["doi"] for entry in references]
    keys = [entry["key"] for entry in references]
    assert set(dois) == REQUIRED_REFERENCE_DOIS
    assert len(dois) == len(set(dois))
    assert len(keys) == len(set(keys))

    for entry in references:
        assert entry["authors"]
        assert entry["title"]
        assert entry["journal"]
        assert entry["year"]
        assert entry["doi"]
        assert entry["role"]
        assert entry["metadata_status"] == "verified"
        assert entry.get("pages") or entry.get("article_number") or entry["key"] == "iupac_beer_lambert_2025"


def test_journal_package_contains_required_submission_text() -> None:
    package = PACKAGE_PATH.read_text(encoding="utf-8")
    required = (
        "Semiconductor Science and Technology",
        "Paper",
        "journal-positioning paragraph",
        "Cover-letter draft",
        "Data availability statement",
        "Code availability statement",
        "Restricted-source statement",
        "Conceptualization",
        "Writing – original draft",
        "A digitized spectrum remains optional strengthening",
    )
    for phrase in required:
        assert phrase in package

    assert "new general identifiability mathematics" not in package
    assert "complete native-spectrum validation" not in package


def test_program_documents_agree_on_venue_and_threshold() -> None:
    texts = [
        README_PATH.read_text(encoding="utf-8"),
        SUBMISSION_GAP_PATH.read_text(encoding="utf-8"),
        ACTIVE_STATE_PATH.read_text(encoding="utf-8"),
        DECISION_PATH.read_text(encoding="utf-8"),
    ]
    for text in texts:
        assert "Semiconductor Science and Technology" in text
        assert "Journal of Applied Physics" in text
        assert "Measurement Science and Technology" in text
        assert "not required before initial submission" in text or "not required before initial SST submission" in text or "not required before initial submission" in text.lower()
        assert "11.297 meV" in text

    active = texts[2]
    assert "**Active milestone:** #191" in active
    assert "PR #190" in active
    assert "speculative spectrum digitization" in active


def test_submission_gate_does_not_overstate_validation() -> None:
    documents = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (PACKAGE_PATH, README_PATH, SUBMISSION_GAP_PATH, ACTIVE_STATE_PATH, DECISION_PATH)
    )
    assert "qualified real-specimen" in documents
    assert "not complete native-spectrum validation" in documents or "not complete spectrum validation" in documents
    assert "Chang 2007" in documents
    assert "calculated" in documents
    prohibited = (
        "complete external validation has been achieved",
        "Chang experimentally validates the thickness curve",
        "The universal HgCdTe momentum matrix is 8.5107",
        "digitization is mandatory before SST submission",
    )
    for phrase in prohibited:
        assert phrase not in documents
