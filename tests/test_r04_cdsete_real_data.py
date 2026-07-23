from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from mct_research.spatial_disorder_real_data import (
    fit_family_log_variance,
    gaussian_smooth,
    phase_randomized_surrogate,
    read_bowman_map_csv,
    variance_curve,
)


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "validation" / "r04_cdsete_phase2_protocol.json"


def test_protocol_freezes_primary_field_scales_and_claim_boundary() -> None:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))

    assert protocol["protocol_status"] == "frozen_before_formal_result_generation"
    assert protocol["source"]["archive_member"] == "Datasets/Figure 3e.csv"
    assert protocol["primary_numerical_kernel_sweep"]["added_sigma_pixels"] == [
        0.0,
        0.5,
        1.0,
        2.0,
        4.0,
    ]
    assert protocol["training_and_holdout"]["training_sigma_pixels"] == [
        0.0,
        0.5,
        2.0,
        4.0,
    ]
    assert protocol["training_and_holdout"]["held_out_sigma_pixels"] == 1.0
    assert protocol["authorization"]["real_semiconductor_method_demonstration"] is True
    assert protocol["authorization"]["hgcdte_external_validation"] is False
    assert protocol["authorization"]["latent_physical_correlation_length"] is False
    assert protocol["authorization"]["independent_scale_claim"] is False
    assert protocol["authorization"]["manuscript"] is False


def test_bowman_map_parser_preserves_coordinates_and_values(tmp_path: Path) -> None:
    source = tmp_path / "map.csv"
    source.write_text(
        '"First column and row are position in um, other parts wavelength in nm",,,\n'
        ',,,\n'
        'NaN,0,0.5,1.0\n'
        '0,840,841,842\n'
        '0.5,843,844,845\n'
        '1.0,846,847,848\n',
        encoding="utf-8",
    )

    parsed = read_bowman_map_csv(source)
    np.testing.assert_array_equal(parsed.x, [0.0, 0.5, 1.0])
    np.testing.assert_array_equal(parsed.y, [0.0, 0.5, 1.0])
    np.testing.assert_array_equal(
        parsed.values,
        [[840.0, 841.0, 842.0], [843.0, 844.0, 845.0], [846.0, 847.0, 848.0]],
    )


def test_gaussian_smoothing_conserves_constant_fields_for_all_modes() -> None:
    field = np.full((7, 9), 3.25)
    for mode in ("reflect", "nearest", "wrap"):
        for sigma in (0.0, 0.5, 1.0, 2.0, 4.0):
            smoothed = gaussian_smooth(field, sigma, mode=mode)
            np.testing.assert_allclose(smoothed, field, rtol=0.0, atol=2.0e-14)


def test_gaussian_smoothing_reference_values_match_ndimage_convention() -> None:
    field = np.array(
        [[1.0, 2.0, 4.0, 8.0], [2.0, 3.0, 5.0, 9.0], [4.0, 5.0, 7.0, 11.0]],
        dtype=float,
    )
    smoothed = gaussian_smooth(field, 1.0, mode="reflect")
    expected = np.array(
        [
            [1.989190649565, 3.024116023490, 5.009165562617, 6.917777564328],
            [2.800224604025, 3.835149977950, 5.820199517077, 7.728811518788],
            [3.722969346851, 4.757894720776, 6.742944259903, 8.651556261614],
        ]
    )
    np.testing.assert_allclose(smoothed, expected, rtol=0.0, atol=5.0e-9)


def test_family_fit_recovers_exact_gaussian_training_curve() -> None:
    scales = np.array([0.0, 0.5, 1.0, 2.0, 4.0])
    point_variance = 12.5
    correlation_scale = 2.75
    variances = point_variance / (1.0 + 2.0 * scales**2 / correlation_scale**2)

    fit = fit_family_log_variance(
        scales,
        variances,
        training_indices=[0, 1, 3, 4],
        held_out_index=2,
        family="Gaussian",
    )

    assert abs(fit.point_variance / point_variance - 1.0) < 1.0e-10
    assert abs(fit.correlation_scale_pixels / correlation_scale - 1.0) < 1.0e-10
    assert fit.training_log_rms < 1.0e-11
    assert fit.held_out_absolute_relative_error < 1.0e-10


def test_phase_randomization_preserves_periodic_smoothing_curve() -> None:
    yy, xx = np.indices((12, 14), dtype=float)
    field = 3.0 + np.sin(2.0 * np.pi * xx / 7.0) + 0.4 * np.cos(2.0 * np.pi * yy / 6.0)
    surrogate = phase_randomized_surrogate(field, seed=3172026)
    scales = np.array([0.0, 0.5, 1.0, 2.0, 4.0])

    assert abs(float(np.mean(surrogate) - np.mean(field))) < 1.0e-12
    assert abs(float(np.var(surrogate, ddof=1) / np.var(field, ddof=1) - 1.0)) < 1.0e-12
    original_curve = variance_curve(field, scales, mode="wrap")
    surrogate_curve = variance_curve(surrogate, scales, mode="wrap")
    np.testing.assert_allclose(surrogate_curve, original_curve, rtol=5.0e-13, atol=2.0e-14)
