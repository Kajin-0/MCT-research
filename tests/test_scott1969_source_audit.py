from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "experimental"
METADATA = DATA / "scott1969_source_metadata.csv"
SPECIMENS = DATA / "scott1969_figure1_specimens.csv"
README = DATA / "scott1969_README.md"
FIGURE2 = DATA / "scott1969_figure2_digitized.csv"
FIGURE5 = DATA / "scott1969_figure5_digitized.csv"
PDF_SHA = "7b2e5790745897ecd75bd22134e5d9293397820c3b7851eb5a9e648a5c441324"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_source_metadata_contract_is_exact() -> None:
    rows = _rows(METADATA)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "SCOTT1969"
    assert row["doi"] == "10.1063/1.1657147"
    assert row["pages"] == "4077-4081"
    assert row["source_file_library_name"] == "scott1969.pdf"
    assert row["source_binary_status"] == (
        "materialized_from_user_uploaded_pdf_in_extraction_runtime"
    )
    assert row["source_pdf_sha256"] == PDF_SHA
    assert row["source_pdf_sha256_status"] == "computed_and_verified"
    assert row["digitization_status"] == (
        "figure2_70_direct_markers_calibrated_figure5_crosscheck_only"
    )


def test_metrology_and_operational_edge_are_preserved() -> None:
    row = _rows(METADATA)[0]
    assert row["growth_method"] == "modified_Bridgman"
    assert row["nominal_composition_method"] == "density"
    assert float(row["nominal_composition_precision_x"]) == pytest.approx(0.005)
    assert row["composition_profile_method"] == (
        "electron_beam_microprobe_on_sample_or_adjacent_ingot_slice"
    )
    assert float(row["maximum_reported_beam_area_variation_x"]) == pytest.approx(
        0.02
    )
    assert float(row["specimen_thickness_um"]) == pytest.approx(50.0)
    assert row["spectrometer"] == "Perkin-Elmer_model_112_IR_spectrometer"
    assert row["prisms"] == "CaF2;NaCl;KBr"
    assert float(row["minimum_measurable_transmittance"]) == pytest.approx(1e-4)
    assert float(row["spectral_resolution_ev_upper_bound"]) == pytest.approx(0.01)
    assert float(row["cryostat_temperature_min_k"]) == pytest.approx(4.2)
    assert float(row["cryostat_temperature_max_k"]) == pytest.approx(300.0)
    assert row["operational_edge_criterion"] == (
        "photon_energy_at_fixed_absorption_coefficient"
    )
    assert float(row["edge_alpha_cm_inverse"]) == pytest.approx(500.0)
    assert float(row["maximum_measurable_alpha_cm_inverse"]) == pytest.approx(
        1000.0
    )
    assert row["tauc_extrapolation_status"] == (
        "unavailable_alpha_range_too_narrow"
    )


def test_article_level_uncertainty_is_not_pointwise_gaussian_covariance() -> None:
    row = _rows(METADATA)[0]
    assert float(row["source_level_gap_uncertainty_ev"]) == pytest.approx(0.01)
    assert row["source_level_composition_uncertainty_mole_percent"] == "1-2"
    assert row["source_uncertainty_semantics"] == (
        "article_level_approximate_bounds_not_pointwise_gaussian_sigma"
    )
    assert row["pointwise_energy_covariance"] == "not_reported"


def test_figure1_specimen_labels_are_exact_and_unique() -> None:
    rows = _rows(SPECIMENS)
    assert len(rows) == 10
    assert [row["figure1_label_mole_percent_cdte"] for row in rows] == [
        "21",
        "23",
        "25",
        "31",
        "35",
        "38.5",
        "40.5",
        "46",
        "53",
        "61",
    ]
    assert [float(row["composition_x_nominal"]) for row in rows] == pytest.approx(
        [0.21, 0.23, 0.25, 0.31, 0.35, 0.385, 0.405, 0.46, 0.53, 0.61]
    )
    assert len({row["specimen_id"] for row in rows}) == 10
    assert {row["figure1_room_temperature_absorption_present"] for row in rows} == {
        "true"
    }
    assert {row["source_pdf_sha256_status"] for row in rows} == {
        "computed_and_verified"
    }


def test_source_specific_quality_flags_are_exact() -> None:
    rows = {row["figure1_label_mole_percent_cdte"]: row for row in _rows(SPECIMENS)}
    assert rows["25"]["quality_flag"] == (
        "high_residual_absorption_inhomogeneity_concern"
    )
    for label in ("38.5", "53"):
        assert rows[label]["quality_flag"] == (
            "kinked_edge_composition_nonuniformity_concern"
        )
    unflagged = {"21", "23", "31", "35", "40.5", "46", "61"}
    assert {
        label
        for label, row in rows.items()
        if row["quality_flag"] == "no_specific_quality_exception_reported"
    } == unflagged


def test_figure2_extension_replaces_the_old_fail_closed_state() -> None:
    specimens = {
        row["figure1_label_mole_percent_cdte"]: row for row in _rows(SPECIMENS)
    }
    assert specimens["21"]["figure2_temperature_marker_ledger_status"] == (
        "not_present_in_figure2"
    )
    reconstructed = {"23", "25", "31", "35", "38.5", "40.5", "46", "53", "61"}
    assert {
        label
        for label, row in specimens.items()
        if row["figure2_temperature_marker_ledger_status"]
        == "reconstructed_direct_marker_ledger"
    } == reconstructed
    assert {
        specimens[label]["figure5_measured_vs_fit_label_status"]
        for label in reconstructed
    } == {"provenance_cross_check_only_not_independent_data"}
    assert {row["pointwise_gap_ev"] for row in specimens.values()} == {""}
    assert {row["pointwise_gap_uncertainty_ev"] for row in specimens.values()} == {
        ""
    }

    assert FIGURE2.exists()
    markers = _rows(FIGURE2)
    assert len(markers) == 70
    assert Counter(row["specimen_label"] for row in markers) == {
        "61": 8,
        "53": 6,
        "46": 9,
        "40.5": 8,
        "38.5": 8,
        "35": 8,
        "31": 8,
        "25": 7,
        "23": 8,
    }
    assert not FIGURE5.exists()


def test_lineage_measurement_class_and_equation_boundaries_are_explicit() -> None:
    metadata = _rows(METADATA)[0]
    specimens = _rows(SPECIMENS)
    assert metadata["measurement_class"] == (
        "fixed_absorption_optical_edge_alpha_500_cm_inverse"
    )
    assert metadata["relationship_to_hansen"] == (
        "fitted_source_in_Hansen_1982_not_independent_validation"
    )
    assert metadata["source_equation"] == (
        "Eg_eV=-0.303+1.73*x+5.6e-4*(1-2*x)*T+0.25*x^4"
    )
    assert metadata["source_equation_declared_validity"] == (
        "strictly_x_le_0.6_and_100K_le_T_le_300K"
    )
    assert {row["measurement_class"] for row in specimens} == {
        "fixed_absorption_optical_edge_alpha_500_cm_inverse"
    }
    assert {row["relationship_to_hansen"] for row in specimens} == {
        "in_sample_fitted_source"
    }


def test_readme_records_numerical_extension_without_overclaiming() -> None:
    text = README.read_text(encoding="utf-8")
    required = (
        PDF_SHA,
        "70 visually identifiable direct `x` marker centers",
        "Only direct Figure 2 marker centers are admitted.",
        "Figure 5 remains a provenance cross-check only.",
        "cannot be used as an independent held-out validation of Hansen",
        "sample Equation (3) or Figure 5 curves as data",
    )
    assert all(token in text for token in required)
