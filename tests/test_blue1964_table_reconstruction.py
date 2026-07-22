from __future__ import annotations

import csv
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "experimental" / "blue1964_source_metadata.csv"
OBSERVATIONS = ROOT / "data" / "experimental" / "blue1964_table2_optical_gaps.csv"
README = ROOT / "data" / "experimental" / "blue1964_README.md"
HANSEN_GRAPH = ROOT / "data" / "hansen" / "hansen_1982_source_graph.csv"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_source_contract_and_table_identity_are_explicit() -> None:
    rows = _rows(METADATA)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "BLUE1964"
    assert row["title"] == "Optical Absorption in HgTe and HgCdTe"
    assert row["venue"] == "Physical Review"
    assert row["volume"] == "134"
    assert row["issue"] == "1A"
    assert row["pages"] == "A226-A234"
    assert row["source_file_library_name"] == "blue1964.pdf"
    assert row["source_pdf_sha256"] == ""
    assert row["source_pdf_sha256_status"] == "unavailable_not_computed"
    assert row["article_table_identifier"] == "Table_II"
    assert row["ocr_table_identifier_status"] == (
        "article_narrative_says_Table_II_OCR_roman_numeral_inconsistent"
    )


def test_exact_seven_printed_rows_are_transcribed() -> None:
    rows = _rows(OBSERVATIONS)
    assert len(rows) == 7
    assert [float(row["cdte_atomic_percent"]) for row in rows] == pytest.approx(
        [0.0, 0.5, 14.0, 22.0, 25.0, 28.0, 32.0]
    )
    assert [float(row["composition_x_reported"]) for row in rows] == pytest.approx(
        [0.0, 0.005, 0.14, 0.22, 0.25, 0.28, 0.32]
    )
    assert [float(row["optical_gap_parameter_ev"]) for row in rows] == pytest.approx(
        [0.03, 0.04, 0.12, 0.22, 0.25, 0.28, 0.365]
    )
    assert [
        float(row["optical_gap_uncertainty_ev"]) for row in rows
    ] == pytest.approx([0.02, 0.02, 0.04, 0.02, 0.02, 0.02, 0.01])
    assert len({row["observation_id"] for row in rows}) == 7
    assert len({row["specimen_id"] for row in rows}) == 7


def test_room_temperature_context_is_retained_without_invented_kelvin_value() -> None:
    rows = _rows(OBSERVATIONS)
    assert {row["temperature_context"] for row in rows} == {"room_temperature"}
    assert {row["temperature_k"] for row in rows} == {""}
    metadata = _rows(METADATA)[0]
    assert metadata["tabulated_observation_temperature_context"] == "room_temperature"
    assert metadata["tabulated_temperature_k"] == ""
    assert float(metadata["measurement_temperature_min_k"]) == pytest.approx(90.0)
    assert float(metadata["measurement_temperature_max_k"]) == pytest.approx(373.0)


def test_observable_is_positive_theory_conditioned_and_not_signed_gap_eligible() -> None:
    rows = _rows(OBSERVATIONS)
    assert {row["measurement_class"] for row in rows} == {
        "theory_conditioned_positive_optical_gap_parameter"
    }
    assert {row["gap_extraction_method"] for row in rows} == {
        "comparison_of_measured_high_absorption_curve_to_direct_transition_theory"
    }
    assert {row["fit_region_alpha_cm_inverse"] for row in rows} == {
        "approximately_above_1e3"
    }
    assert {row["observable_sign_semantics"] for row in rows} == {
        "positive_parameter_not_signed_Gamma6_minus_Gamma8"
    }
    assert {row["signed_gap_eligible"] for row in rows} == {"false"}
    hg_rich = rows[:2]
    assert [float(row["optical_gap_parameter_ev"]) for row in hg_rich] == pytest.approx(
        [0.03, 0.04]
    )


def test_uncertainty_and_composition_accuracy_semantics_are_not_overstated() -> None:
    rows = _rows(OBSERVATIONS)
    assert {row["optical_gap_uncertainty_semantics"] for row in rows} == {
        "source_reported_curve_fit_bound_not_asserted_gaussian_sigma"
    }
    assert {row["pointwise_energy_covariance"] for row in rows} == {"not_reported"}
    assert {row["composition_accuracy_as_reported"] for row in rows} == {
        "better_than_one_percent_or_one_percent_assumed"
    }
    assert {row["composition_accuracy_semantics"] for row in rows} == {
        "one_percent_as_reported_scale_ambiguous_not_sigma_x"
    }
    assert all("sigma_x" not in row for row in rows)


def test_abstract_and_numerical_table_range_inconsistency_is_preserved() -> None:
    metadata = _rows(METADATA)[0]
    assert float(metadata["abstract_max_cdte_atomic_percent"]) == pytest.approx(28.0)
    assert float(metadata["numerical_table_max_cdte_atomic_percent"]) == pytest.approx(
        32.0
    )
    assert metadata["composition_range_inconsistency_status"] == (
        "preserve_unresolved_abstract_vs_figure_and_table_inconsistency"
    )
    rows = _rows(OBSERVATIONS)
    assert rows[-1]["cdte_atomic_percent"] == "32"
    assert "despite abstract statement" in rows[-1]["notes"]


def test_source_metrology_is_preserved() -> None:
    row = _rows(METADATA)[0]
    assert row["growth_method"] == "vertical_Bridgman"
    assert float(row["bridgman_drop_rate_mm_per_h"]) == pytest.approx(2.0)
    assert row["composition_method"] == "chemical_analysis_of_Hg_Te_Cd"
    assert row["composition_sampling"] == (
        "multiple_positions_along_ingot_due_to_segregation"
    )
    assert float(row["specimen_thickness_typical_um"]) == pytest.approx(20.0)
    assert float(row["specimen_thickness_min_achievable_um"]) == pytest.approx(6.0)
    assert row["spectrometer"] == "Perkin-Elmer_model_112_IR_spectrometer"
    assert row["optics"] == "NaCl;KBr"
    assert row["wavelength_range_um"] == "1-25"


def test_lineage_and_no_pseudodata_boundary_are_enforced() -> None:
    metadata = _rows(METADATA)[0]
    assert metadata["relationship_to_hansen"] == (
        "not_in_reconstructed_Hansen_22_source_graph_historical_predecessor"
    )
    assert metadata["source_equation_sampling_status"] == "prohibited"
    graph_text = HANSEN_GRAPH.read_text(encoding="utf-8").lower()
    assert "m. d. blue" not in graph_text
    assert not (
        ROOT / "data" / "experimental" / "blue1964_figure6_digitized.csv"
    ).exists()
    readme = README.read_text(encoding="utf-8")
    required = (
        "does not place the rows in a signed-gap benchmark by default",
        "does not invent one exact kelvin value",
        "Both statements are retained",
        "contains no digitized Figure 6 coordinates",
    )
    assert all(token in readme for token in required)
