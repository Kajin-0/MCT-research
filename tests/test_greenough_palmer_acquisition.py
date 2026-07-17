from __future__ import annotations

import json
from pathlib import Path

import pytest

from acquire_greenough_palmer import (
    normalize_text,
    parse_pdfinfo_pages,
    validate_markers,
)


def test_normalize_text_handles_scan_punctuation_and_spacing() -> None:
    source = "Peak at 79·0 K\n\nR D Greenough   and S B Palmer"
    normalized = normalize_text(source)
    assert "79.0 k" in normalized
    assert "r d greenough and s b palmer" in normalized


def test_parse_pdfinfo_pages() -> None:
    assert parse_pdfinfo_pages("Title: Example\nPages:          6\n") == 6
    with pytest.raises(ValueError):
        parse_pdfinfo_pages("Title: Example\n")


def test_validate_markers_is_normalized() -> None:
    result = validate_markers(
        "A strain-gauge technique was used. Peak: 79·0 K.",
        ["strain-gauge technique", "79.0 K"],
    )
    assert result == {"strain-gauge technique": True, "79.0 K": True}


def test_contract_forbids_preserving_copyrighted_source() -> None:
    contract = json.loads(
        Path("literature/greenough_palmer_1973_acquisition_contract.json").read_text(
            encoding="utf-8"
        )
    )
    assert contract["citation"]["doi"] == "10.1088/0022-3727/6/5/315"
    assert contract["acquisition"]["expected_page_count"] == 6
    assert contract["rights_and_storage"] == {
        "commit_pdf_to_repository": False,
        "upload_pdf_as_artifact": False,
        "upload_full_text_as_artifact": False,
        "preserve_only_digest_metadata_and_validation": True,
    }
    assert not contract["scientific_gate"][
        "execution_lattice_authorized_by_acquisition_alone"
    ]


def test_audited_source_identity_and_fail_closed_gate() -> None:
    source = json.loads(
        Path("first_principles/a0/cdte_greenough_palmer_source.json").read_text(
            encoding="utf-8"
        )
    )
    assert source["source"]["sha256"] == (
        "3f6a2a39b2047d3d00c375a7441068ba88712429719b5826318876230bf46781"
    )
    assert source["source"]["size_bytes"] == 2232984
    assert source["source"]["page_count"] == 6
    assert source["source"]["copyrighted_source_committed_or_uploaded"] is False
    assert source["sample_and_measurement"]["material"] == "single-crystal CdTe"
    assert source["sample_and_measurement"][
        "reported_relative_alpha_uncertainty_fraction"
    ] == pytest.approx(0.03)
    assert source["gate_decision"]["primary_source_acquired_and_hashed"] is True
    assert source["gate_decision"]["single_crystal_morphology_gate_passed"] is True
    assert source["gate_decision"]["curve_digitization_complete"] is False
    assert source["gate_decision"]["execution_lattice_authorized"] is False
