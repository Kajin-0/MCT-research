from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "experimental" / "schmit1969_source_metadata.csv"
SPECIMENS = ROOT / "data" / "experimental" / "schmit1969_specimens.csv"
OBSERVATIONS = (
    ROOT / "data" / "experimental" / "schmit1969_table3_cutoff_observations.csv"
)
README = ROOT / "data" / "experimental" / "schmit1969_README.md"
HANSEN_GRAPH = ROOT / "data" / "hansen" / "hansen_1982_source_graph.csv"


EXPECTED_SPECIMENS = {
    "SS69_S01": (0.600, 0.030, 0.599, 4),
    "SS69_S02": (0.580, 0.050, 0.572, 6),
    "SS69_S03": (0.325, 0.010, 0.329, 8),
    "SS69_S04": (0.266, 0.003, 0.262, 6),
    "SS69_S05": (0.217, 0.006, 0.223, 8),
    "SS69_S06": (0.195, 0.006, 0.201, 6),
    "SS69_S07": (0.180, 0.006, 0.183, 10),
    "SS69_S08": (0.170, 0.006, 0.174, 8),
}

EXPECTED_OBSERVATIONS = {
    "SS69_S01": [
        (300, 1.688, 0.735),
        (244, 1.678, 0.739),
        (194, 1.666, 0.744),
        (146, 1.647, 0.753),
    ],
    "SS69_S02": [
        (300, 1.811, 0.685),
        (244, 1.791, 0.692),
        (194, 1.770, 0.701),
        (146, 1.756, 0.706),
        (90, 1.734, 0.715),
        (77, 1.730, 0.717),
    ],
    "SS69_S03": [
        (287, 3.73, 0.332),
        (271, 3.77, 0.329),
        (246, 3.80, 0.326),
        (207, 3.90, 0.318),
        (156, 3.99, 0.311),
        (101, 4.11, 0.302),
        (85, 4.19, 0.296),
        (22, 4.40, 0.282),
    ],
    "SS69_S04": [
        (300, 5.10, 0.243),
        (244, 5.37, 0.231),
        (194, 5.67, 0.219),
        (146, 6.01, 0.206),
        (90, 6.38, 0.194),
        (77, 6.49, 0.191),
    ],
    "SS69_S05": [
        (287, 6.55, 0.189),
        (255, 6.87, 0.181),
        (211, 7.37, 0.168),
        (156, 8.13, 0.153),
        (131, 8.59, 0.144),
        (85, 9.52, 0.130),
        (43, 10.79, 0.115),
        (26, 11.37, 0.109),
    ],
    "SS69_S06": [
        (300, 7.60, 0.163),
        (244, 8.40, 0.148),
        (194, 9.38, 0.132),
        (146, 10.75, 0.115),
        (90, 12.12, 0.102),
        (77, 12.6, 0.098),
    ],
    "SS69_S07": [
        (198, 11.5, 0.108),
        (166, 12.0, 0.103),
        (151, 12.5, 0.099),
        (122, 14.7, 0.084),
        (102, 16.45, 0.075),
        (89, 17.48, 0.071),
        (79, 18.2, 0.068),
        (59, 20.5, 0.061),
        (38, 23.0, 0.054),
        (22, 25.0, 0.050),
    ],
    "SS69_S08": [
        (153, 15.5, 0.080),
        (98, 19.7, 0.063),
        (83, 22.5, 0.055),
        (78, 23.2, 0.053),
        (59, 26.7, 0.046),
        (44, 30.4, 0.041),
        (27, 32.9, 0.038),
        (24, 33.7, 0.037),
    ],
}


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_source_identity_and_unavailable_binary_hash_are_explicit() -> None:
    rows = _rows(METADATA)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "SCHMIT1969"
    assert row["authors"] == "J. L. Schmit; E. L. Stelzer"
    assert row["title"] == (
        "Temperature and Alloy Compositional Dependences of the Energy Gap of Hg1-xCdxTe"
    )
    assert row["venue"] == "Journal of Applied Physics"
    assert row["volume"] == "40"
    assert row["issue"] == "12"
    assert row["pages"] == "4865-4869"
    assert row["doi"] == "10.1063/1.1657304"
    assert row["source_file_library_name"] == "schmit1969.pdf"
    assert row["source_pdf_sha256"] == ""
    assert row["source_pdf_sha256_status"] == "unavailable_not_computed"


def test_exact_eight_specimens_preserve_nominal_and_adjusted_composition() -> None:
    rows = _rows(SPECIMENS)
    assert len(rows) == 8
    assert [row["specimen_id"] for row in rows] == list(EXPECTED_SPECIMENS)

    for row in rows:
        nominal, uncertainty, adjusted, count = EXPECTED_SPECIMENS[row["specimen_id"]]
        assert float(row["nominal_x"]) == pytest.approx(nominal)
        assert float(row["nominal_x_uncertainty"]) == pytest.approx(uncertainty)
        assert float(row["adjusted_x"]) == pytest.approx(adjusted)
        assert int(row["table3_row_count"]) == count
        assert row["nominal_x_status"] == "source_reported_composition_and_limit"
        assert row["adjusted_x_status"] == "source_fit_adjusted_composition"
        assert row["adjusted_x_is_independently_measured"] == "false"
        assert row["adjusted_x_is_eligible_for_held_out_composition_validation"] == "false"

    assert any(
        float(row["nominal_x"]) != float(row["adjusted_x"]) for row in rows
    )


def test_exact_56_table3_rows_and_specimen_row_counts() -> None:
    rows = _rows(OBSERVATIONS)
    assert len(rows) == 56
    counts = Counter(row["specimen_id"] for row in rows)
    assert counts == Counter(
        {specimen: values[3] for specimen, values in EXPECTED_SPECIMENS.items()}
    )
    assert [row["specimen_id"] for row in rows[:4]] == ["SS69_S01"] * 4
    assert [row["specimen_id"] for row in rows[-8:]] == ["SS69_S08"] * 8


def test_all_printed_temperature_wavelength_and_energy_values_are_exact() -> None:
    grouped: dict[str, list[tuple[int, float, float]]] = {
        specimen: [] for specimen in EXPECTED_OBSERVATIONS
    }
    for row in _rows(OBSERVATIONS):
        grouped[row["specimen_id"]].append(
            (
                int(row["temperature_k"]),
                float(row["cutoff_wavelength_um"]),
                float(row["cutoff_energy_ev"]),
            )
        )

    assert grouped.keys() == EXPECTED_OBSERVATIONS.keys()
    for specimen, expected in EXPECTED_OBSERVATIONS.items():
        assert grouped[specimen] == pytest.approx(expected)


def test_printed_energy_is_retained_and_consistent_with_wavelength_rounding() -> None:
    for row in _rows(OBSERVATIONS):
        wavelength = float(row["cutoff_wavelength_um"])
        printed_energy = float(row["cutoff_energy_ev"])
        calculated_energy = 1.23984 / wavelength
        assert abs(calculated_energy - printed_energy) < 0.0006
        assert row["energy_origin"] == (
            "source_converted_from_half_peak_cutoff_wavelength"
        )


def test_observation_class_is_detector_cutoff_not_signed_or_intrinsic_gap() -> None:
    rows = _rows(OBSERVATIONS)
    assert {row["measurement_class"] for row in rows} == {
        "detector_half_peak_spectral_response_cutoff"
    }
    assert {row["signed_gap_eligible"] for row in rows} == {"false"}
    assert {
        row["intrinsic_gap_eligible_without_observation_operator"] for row in rows
    } == {"false"}
    assert {row["pointwise_covariance_status"] for row in rows} == {"not_reported"}


def test_detector_type_knowledge_boundary_and_weighting_are_exact() -> None:
    rows = {row["specimen_id"]: row for row in _rows(SPECIMENS)}
    assert rows["SS69_S02"]["detector_type"] == "photovoltaic"
    assert rows["SS69_S02"]["detector_type_status"] == "explicit_in_source"
    assert rows["SS69_S03"]["detector_type"] == "photoconductive"
    assert rows["SS69_S03"]["detector_type_status"] == "explicit_in_source"

    unresolved = {
        specimen
        for specimen, row in rows.items()
        if row["detector_type"] == "not_explicitly_resolved"
    }
    assert unresolved == {
        "SS69_S01",
        "SS69_S04",
        "SS69_S05",
        "SS69_S06",
        "SS69_S07",
        "SS69_S08",
    }
    assert rows["SS69_S04"]["source_fit_weighting"] == "heavier_weight"
    assert all(
        rows[specimen]["source_fit_weighting"] == "standard"
        for specimen in rows
        if specimen != "SS69_S04"
    )


def test_uncertainty_and_temperature_stability_semantics_remain_separate() -> None:
    row = _rows(METADATA)[0]
    assert float(row["microprobe_limit_fraction"]) == pytest.approx(0.006)
    assert row["composition_uncertainty_semantics"] == (
        "source_reported_microprobe_limit_not_asserted_gaussian_sigma"
    )
    assert float(row["temperature_absolute_accuracy_k"]) == pytest.approx(10.0)
    assert row["temperature_absolute_accuracy_semantics"] == (
        "source_believed_absolute_temperature_accuracy_better_than_value_not_sigma"
    )
    assert float(row["temperature_stability_k"]) == pytest.approx(0.5)
    assert row["temperature_stability_semantics"] == (
        "source_control_stability_approximately_plus_minus_value_not_absolute_accuracy"
    )
    assert float(row["cutoff_relative_precision_fraction"]) == pytest.approx(0.01)
    assert row["cutoff_precision_semantics"] == (
        "source_precision_better_than_fraction_of_listed_lambda_and_energy_not_pointwise_sigma"
    )


def test_hansen_lineage_and_downstream_exclusions_are_preserved_without_deletion() -> None:
    metadata = _rows(METADATA)[0]
    assert metadata["hansen_graph_id"] == "HSC_R01"
    assert metadata["relationship_to_hansen"] == (
        "Hansen_fitted_source_not_independent_validation"
    )

    specimens = {row["specimen_id"]: row for row in _rows(SPECIMENS)}
    assert {
        specimen
        for specimen, row in specimens.items()
        if row["hansen_downstream_selection_status"] == "excluded_by_Hansen_downstream"
    } == {"SS69_S05", "SS69_S06", "SS69_S07", "SS69_S08"}
    assert all(
        specimens[specimen]["hansen_downstream_exclusion_reason"]
        == "mercury_inclusions"
        for specimen in ("SS69_S05", "SS69_S06", "SS69_S07", "SS69_S08")
    )
    assert len(_rows(OBSERVATIONS)) == 56

    graph = _rows(HANSEN_GRAPH)
    hsc_r01 = next(row for row in graph if row["graph_id"] == "HSC_R01")
    assert hsc_r01["role_in_hansen"] == "fitted_data"
    assert hsc_r01["gap_observable"] == (
        "detector half-peak cutoff; argued to approximate alpha=500 cm^-1"
    )
    assert "four lowest-x samples excluded" in hsc_r01["notes"]


def test_source_equation_is_metadata_only_and_no_figure_pseudodata_exist() -> None:
    metadata = _rows(METADATA)[0]
    assert metadata["source_equation"] == (
        "E_cutoff_eV=1.59*x-0.25+5.233e-4*T*(1-2.08*x)+0.327*x^3"
    )
    assert metadata["source_equation_status"] == (
        "historical_source_fit_metadata_not_sampled_as_observations"
    )
    assert metadata["best_fit_composition_range"] == "0.17_lt_x_lt_0.33"
    assert metadata["best_fit_temperature_rule"] == "T_gt_77_K"
    assert metadata["figure1_digitization_status"] == "not_digitized_in_this_tranche"

    observation_fields = set(_rows(OBSERVATIONS)[0])
    assert "model_prediction_ev" not in observation_fields
    assert "source_equation_prediction_ev" not in observation_fields
    assert not (
        ROOT / "data" / "experimental" / "schmit1969_figure1_digitized.csv"
    ).exists()


def test_readme_preserves_claim_boundaries() -> None:
    text = README.read_text(encoding="utf-8")
    required = (
        "fit-dependent quantities rather than new independent measurements",
        "detector_half_peak_spectral_response_cutoff",
        "The printed energy values are retained exactly",
        "short-term control stability: approximately +/- 0.5 K",
        "absolute temperature determination: believed better than 10 K",
        "Hansen source `HSC_R01`",
        "does not delete the printed Table III observations",
        "It does not support:",
        "production-equation, manuscript, or submission authorization",
    )
    assert all(token in text for token in required)
