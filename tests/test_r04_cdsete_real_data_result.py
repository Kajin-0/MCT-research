from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "data" / "validation" / "r04_cdsete_real_data_result.json"
NOTE_PATH = ROOT / "literature" / "notes" / "cdsete2024_real_data_result.md"


def load_result() -> dict:
    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def test_result_source_and_protocol_are_immutable() -> None:
    result = load_result()

    assert result["decision"] == "RESTRICTED_REAL_DATA_DEMONSTRATION_COMPLETE"
    assert result["source"]["archive_sha256"] == (
        "cc3e1ce1a02266da2d0e0f301464a9d8a519855f33a597adeb7f16048684c9a6"
    )
    assert result["source"]["archive_member"] == "Datasets/Figure 3e.csv"
    assert result["source"]["archive_member_sha256"] == (
        "49422bda851686db62574fb30354d698138f221db4b66d8782e0717698bc5679"
    )
    assert result["protocol"]["status"] == "frozen_before_formal_result_generation"
    assert result["protocol"]["training_sigma_pixels"] == [0.0, 0.5, 2.0, 4.0]
    assert result["protocol"]["held_out_sigma_pixels"] == 1.0
    assert result["protocol"]["formal_scale_grid_changed_after_result"] is False


def test_primary_field_and_added_kernel_curve() -> None:
    result = load_result()
    field = result["field"]
    sweep = result["primary_added_kernel_sweep"]

    assert field["shape"] == [24, 24]
    assert field["observable"] == "Gaussian-fitted photoluminescence peak wavelength"
    assert field["missing_or_nonfinite_count"] == 0
    assert field["minimum_nm"] == 837.0
    assert field["maximum_nm"] == 862.5
    np.testing.assert_allclose(field["mean_nm"], 844.8215104166667, rtol=0.0, atol=1.0e-12)
    np.testing.assert_allclose(field["sample_variance_nm2"], 13.73732519293478, rtol=0.0, atol=1.0e-12)

    assert sweep["sigma_pixels"] == [0.0, 0.5, 1.0, 2.0, 4.0]
    np.testing.assert_allclose(
        sweep["sample_variance_nm2"],
        [
            13.73732519293478,
            11.374408090901321,
            7.829969631751158,
            4.3497792689765,
            1.5443547243068794,
        ],
        rtol=0.0,
        atol=1.0e-12,
    )
    fractions = np.asarray(sweep["variance_fraction_of_unsmoothed"], dtype=float)
    assert np.all(np.diff(fractions) < 0.0)
    assert fractions[-1] < 0.12


def test_family_result_is_descriptive_and_not_decisive() -> None:
    diagnostics = load_result()["family_diagnostics"]
    records = {record["family"]: record for record in diagnostics["records"]}

    assert diagnostics["lowest_training_log_rms_family"] == "Matern_nu_3_over_2"
    assert diagnostics["lowest_held_out_absolute_error_family"] == "Matern_nu_3_over_2"
    assert "descriptive only" in diagnostics["selection_status"]
    assert records["Matern_nu_3_over_2"]["held_out_absolute_relative_error"] < 0.05
    assert records["Gaussian"]["held_out_absolute_relative_error"] > 0.13
    assert diagnostics["gaussian_reciprocal_fit"][
        "maximum_absolute_relative_variance_residual"
    ] > 0.11


def test_same_raster_dependence_is_large_and_model_conditioned() -> None:
    dependence = load_result()["same_raster_gaussian_model_conditioned"]
    correlation = np.asarray(dependence["cross_scale_correlation"], dtype=float)
    effective_dof = np.asarray(
        dependence["moment_matched_effective_degrees_of_freedom"], dtype=float
    )

    np.testing.assert_allclose(correlation, correlation.T, rtol=0.0, atol=1.0e-14)
    np.testing.assert_allclose(np.diag(correlation), 1.0, rtol=0.0, atol=3.0e-16)
    assert correlation[0, 1] > 0.998
    assert correlation[1, 2] > 0.989
    assert effective_dof[-1] < 8.0
    assert dependence[
        "parameter_covariance_determinant_inflation_vs_false_independence"
    ] > 16.9
    assert "not empirical repeat covariance" in dependence["status"]


def test_field_of_view_and_boundary_sensitivity_prevent_strong_family_claim() -> None:
    sensitivity = load_result()["sensitivity"]

    assert sensitivity["maximum_relative_difference_wrap_vs_reflect"] > 0.72
    assert sensitivity["maximum_relative_difference_crop_vs_full_reflect"] > 0.72
    assert sensitivity["maximum_relative_difference_nearest_vs_reflect"] > 0.37
    assert sensitivity["maximum_relative_difference_planar_detrended_vs_primary"] > 0.19


def test_phase_randomized_control_and_claim_boundary() -> None:
    result = load_result()
    control = result["phase_randomized_control"]
    boundary = result["claim_boundary"]

    assert abs(control["mean_residual_nm"]) < 2.0e-13
    assert abs(control["sample_variance_relative_residual"]) < 1.0e-14
    assert control["wrap_variance_maximum_relative_residual"] < 3.0e-14
    assert boundary["real_semiconductor_method_demonstration"] is True
    assert boundary["hgcdte_external_validation"] is False
    assert boundary["native_kernel_deconvolution"] is False
    assert boundary["latent_physical_correlation_length"] is False
    assert boundary["composition_assignment"] is False
    assert boundary["independent_scale_claim"] is False
    assert boundary["universal_covariance_family"] is False
    assert boundary["r05"] is False
    assert boundary["manuscript"] is False


def test_result_note_preserves_restrictions() -> None:
    note = " ".join(NOTE_PATH.read_text(encoding="utf-8").split())
    assert "RESTRICTED_REAL_DATA_DEMONSTRATION_COMPLETE" in note
    assert "not HgCdTe validation" in note
    assert "not independent model validation" in note
    assert "No HgCdTe validation" in note
