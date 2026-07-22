from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data/experimental/finkman1979_source_metadata.csv"
PARAMETER_PATH = ROOT / "data/experimental/finkman1979_parameter_ledger.csv"
README_PATH = ROOT / "data/experimental/finkman1979_README.md"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _parameter_rows() -> dict[str, dict[str, str]]:
    return {row["record_id"]: row for row in _read_csv(PARAMETER_PATH)}


def test_source_identity_and_unavailable_hash_boundary() -> None:
    rows = _read_csv(METADATA_PATH)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "FINKMAN1979"
    assert row["doi"] == "10.1063/1.326421"
    assert row["source_file_library_name"] == "finkman1979.pdf"
    assert row["source_binary_status"] == "available_in_user_file_library_not_materialized"
    assert row["source_pdf_sha256"] == ""
    assert row["source_pdf_sha256_status"] == "unavailable_not_computed"


def test_primary_specimen_and_metrology_contract() -> None:
    row = _read_csv(METADATA_PATH)[0]
    assert float(row["measured_x_min"]) == 0.205
    assert float(row["measured_x_max"]) == 0.220
    assert row["primary_source_composition_method"] == "electron_beam_microprobe"
    assert float(row["primary_source_composition_precision_x"]) == 0.003
    assert float(row["temperature_min_k"]) == 80.0
    assert float(row["temperature_max_k"]) == 300.0
    assert float(row["initial_specimen_thickness_um"]) == 80.0
    assert float(row["thinnest_specimen_thickness_um"]) == 15.0
    assert float(row["thickness_uniformity_um"]) == 2.0
    assert row["spectrometer"] == "Beckman_IR_spectrophotometer_model_4250"
    assert row["cryostat"] == "Air_Products_Helitran_model_110"
    assert row["cryostat_windows"] == "ZnSe"
    assert float(row["temperature_uniformity_k"]) == 1.0
    assert row["pointwise_covariance"] == "not_reported"


def test_source_heating_is_preserved_as_an_artifact_control() -> None:
    row = _read_csv(METADATA_PATH)[0]
    assert row["source_heating_artifact"] == (
        "IR_source_heating_detected_from_abnormal_band_edge_shift"
    )
    assert row["heating_mitigation"] == (
        "reduce_source_power_or_insert_attenuators_until_absorption_no_longer_shifted"
    )


def test_primary_and_hansen_composition_provenance_are_not_conflated() -> None:
    row = _read_csv(METADATA_PATH)[0]
    assert row["primary_source_composition_method"] == "electron_beam_microprobe"
    assert "vendor_Cominco" in row["hansen_composition_description"]
    assert row["composition_provenance_reconciliation_status"] == (
        "primary_paper_and_Hansen_lineage_descriptions_retained_without_silent_reconciliation"
    )
    assert row["hansen_graph_id"] == "HSC_R03"
    assert row["role_in_hansen"] == "fitted_data"
    assert row["independent_validation_of_hansen"] == "false"


def test_optical_inversion_observation_class_and_error_semantics() -> None:
    row = _read_csv(METADATA_PATH)[0]
    assert row["measurement_class"] == (
        "transmission_inverted_optical_absorption_coefficient"
    )
    assert float(row["measured_alpha_tail_min_cm_inverse"]) == 20.0
    assert float(row["measured_alpha_tail_max_cm_inverse"]) == 1000.0
    assert float(row["presented_alpha_upper_limit_cm_inverse"]) == 2000.0
    assert float(row["reflection_approximation_error_percent_upper_bound"]) == 0.5
    assert float(row["refractive_index_extrapolation_absorption_error_percent"]) == 2.0
    assert float(row["index_of_refraction_absolute_uncertainty_percent"]) == 3.0
    assert float(row["index_relative_change_accuracy_percent"]) == 0.5


def test_parameter_ledger_has_exact_declared_records() -> None:
    rows = _parameter_rows()
    assert set(rows) == {
        "FN79_MODEL",
        "FN79_SIGMA_FIT",
        "FN79_T0_FIT",
        "FN79_SIGMA_SUMMARY",
        "FN79_T0_SUMMARY",
        "FN79_E0_RELATION",
        "FN79_ALPHA0_RELATION",
        "FN79_FIXED_ALPHA_ENERGY",
        "FN79_FIXED_ALPHA_DT",
        "FN79_ALPHA1000_PROXY",
        "FN79_ALPHA500_COMPARISON",
    }
    assert rows["FN79_MODEL"]["expression"] == (
        "alpha=alpha0*exp[sigma*(E_cm_inverse-E0_cm_inverse)/(T_k+T0_k)]"
    )
    assert float(rows["FN79_SIGMA_FIT"]["value"]) == 5.65
    assert float(rows["FN79_SIGMA_FIT"]["uncertainty"]) == 0.07
    assert float(rows["FN79_T0_FIT"]["value"]) == 80.5
    assert float(rows["FN79_T0_FIT"]["uncertainty"]) == 2.0
    assert float(rows["FN79_SIGMA_SUMMARY"]["value"]) == 5.646
    assert float(rows["FN79_T0_SUMMARY"]["value"]) == 80.51


def test_composition_relations_are_exactly_retained() -> None:
    rows = _parameter_rows()
    assert rows["FN79_E0_RELATION"]["expression"] == (
        "E0_cm_inverse=-3109+16450*x"
    )
    assert rows["FN79_ALPHA0_RELATION"]["expression"] == (
        "ln(alpha0_cm_inverse)=-20.44+51.70*x"
    )
    assert "measured_range_fit_with_source_endpoint_extrapolation" == rows[
        "FN79_E0_RELATION"
    ]["source_scope"]
    assert "measured_range_fit_with_source_endpoint_extrapolation" == rows[
        "FN79_ALPHA0_RELATION"
    ]["source_scope"]


def test_equation_10_uses_dimensionally_consistent_2p20e_minus5() -> None:
    rows = _parameter_rows()
    expression = rows["FN79_FIXED_ALPHA_ENERGY"]["expression"]
    assert "2.20e-5*T_k" in expression
    assert "2.20e-7" not in expression
    conversion = 1.23984e-4 / 5.646
    assert math.isclose(conversion, 2.196e-5, rel_tol=3e-4)


def test_equation_11_closes_against_equation_10_coefficients() -> None:
    rows = _parameter_rows()
    assert rows["FN79_FIXED_ALPHA_DT"]["expression"] == (
        "dE_dT=2.20e-5*ln(alpha_cm_inverse)+4.49e-4-1.13e-3*x"
    )
    assert math.isclose(2.20e-5 * 20.44, 4.49e-4, rel_tol=2e-3)
    assert math.isclose(2.20e-5 * 51.70, 1.13e-3, rel_tol=8e-3)


def test_alpha1000_is_a_non_signed_observation_operator_proxy() -> None:
    row = _parameter_rows()["FN79_ALPHA1000_PROXY"]
    assert row["observation_class"] == (
        "fixed_absorption_optical_edge_alpha_1000_cm_inverse_proxy"
    )
    assert row["signed_gap_eligible"] == "false"
    assert row["intrinsic_gap_eligible_without_observation_operator"] == "false"
    assert "true_slope_change_region_not_reached" in row["source_scope"]


def test_readme_preserves_extrapolation_and_r03_boundaries() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    assert "whole-range use is an extrapolation claim" in text
    assert "composition dependence of `T0` remains to be studied" in text
    assert "no Figure 3-6 marker ledger" in text
    assert "no Gaussian-disorder parameter" in text
    assert "does not establish intrinsic signed gaps" in text
    assert "2.20e-5" in text
    assert "2.20e-7" in text  # explicitly documented as the rejected OCR value


def test_no_figure_pseudodata_or_r03_dataset_is_created() -> None:
    forbidden = [
        ROOT / "data/experimental/finkman1979_figure3_digitized.csv",
        ROOT / "data/experimental/finkman1979_figure4_digitized.csv",
        ROOT / "data/experimental/finkman1979_figure5_digitized.csv",
        ROOT / "data/experimental/finkman1979_figure6_digitized.csv",
        ROOT / "data/validation/finkman1979_log_curvature.csv",
    ]
    assert all(not path.exists() for path in forbidden)
