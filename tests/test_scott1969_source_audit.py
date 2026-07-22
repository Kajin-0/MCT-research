from __future__ import annotations

import csv
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "experimental" / "scott1969_source_metadata.csv"
SPECIMENS = ROOT / "data" / "experimental" / "scott1969_figure1_specimens.csv"
README = ROOT / "data" / "experimental" / "scott1969_README.md"


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
        "available_in_user_file_library_not_materialized"
    )
    assert row["source_pdf_sha256"] == ""
    assert row["source_pdf_sha256_status"] == "unavailable_not_computed"


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


def test_digitization_gate_is_fail_closed() -> None:
    rows = _rows(SPECIMENS)
    assert {row["figure2_temperature_marker_ledger_status"] for row in rows} == {
        "not_reconstructed_current_interface"
    }
    assert {row["figure5_measured_vs_fit_label_status"] for row in rows} == {
        "not_reconstructed_current_interface"
    }
    assert {row["pointwise_gap_ev"] for row in rows} == {""}
    assert {row["pointwise_gap_uncertainty_ev"] for row in rows} == {""}
    assert not (
        ROOT / "data" / "experimental" / "scott1969_figure2_digitized.csv"
    ).exists()
    assert not (
        ROOT / "data" / "experimental" / "scott1969_figure5_digitized.csv"
    ).exists()


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


def test_readme_prohibits_equation_sampling_and_overclaiming() -> None:
    text = README.read_text(encoding="utf-8")
    required = (
        "Sampling it does not reconstruct the experimental marker dataset.",
        "no Figure 2 or Figure 5 energy coordinate is committed",
        "cannot be used as an independent held-out validation of Hansen",
        "does not:\n\n- digitize Figures 2 or 5",
    )
    assert all(token in text for token in required)
