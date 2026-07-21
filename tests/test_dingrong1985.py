from __future__ import annotations

import numpy as np

from mct_research.dingrong1985 import (
    DINGRONG_ELECTRON_DENSITY_CM3,
    DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM,
    audit_momentum_matrix,
    dingrong_electron_density_cm3,
    reproduce_table,
    solve_fermi_shift_ev,
)

TEMPERATURES_K = (77.0, 100.0, 200.0, 300.0)
BANDGAPS_EV = (0.078, 0.085, 0.120, 0.154)
SOURCE_FERMI_SHIFTS_EV = (0.155, 0.153, 0.134, 0.117)
SOURCE_FERMI_ENERGIES_EV = (0.233, 0.238, 0.254, 0.271)
SOURCE_OPTICAL_GAPS_EV = (0.230, 0.238, 0.250, 0.268)


def test_printed_equation_inverts_density_and_converges() -> None:
    expected = (0.1438074839, 0.1405278143, 0.1237274249, 0.1058582674)
    for temperature, gap, target in zip(
        TEMPERATURES_K,
        BANDGAPS_EV,
        expected,
        strict=True,
    ):
        shift_128 = solve_fermi_shift_ev(
            electron_density_cm3=DINGRONG_ELECTRON_DENSITY_CM3,
            temperature_k=temperature,
            bandgap_ev=gap,
            quadrature_order=128,
        )
        shift_256 = solve_fermi_shift_ev(
            electron_density_cm3=DINGRONG_ELECTRON_DENSITY_CM3,
            temperature_k=temperature,
            bandgap_ev=gap,
            quadrature_order=256,
        )
        assert abs(shift_256 - target) < 2.0e-9
        assert abs(shift_256 - shift_128) < 2.0e-7
        eta = shift_256 / (8.617333262145e-5 * temperature)
        density = dingrong_electron_density_cm3(
            reduced_fermi_level=eta,
            temperature_k=temperature,
            bandgap_ev=gap,
            quadrature_order=256,
        )
        assert abs(density / DINGRONG_ELECTRON_DENSITY_CM3 - 1.0) < 2.0e-11


def test_printed_momentum_matrix_does_not_reproduce_source_table() -> None:
    result = reproduce_table(
        temperatures_k=TEMPERATURES_K,
        bandgaps_ev=BANDGAPS_EV,
        source_fermi_shifts_ev=SOURCE_FERMI_SHIFTS_EV,
        source_fermi_energies_ev=SOURCE_FERMI_ENERGIES_EV,
        source_optical_gaps_ev=SOURCE_OPTICAL_GAPS_EV,
        momentum_matrix_ev_cm=DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM,
    )
    assert result.shift_rms_error_ev == np.testing.assert_allclose(
        result.shift_rms_error_ev,
        0.0112970332,
        rtol=0.0,
        atol=2.0e-9,
    )
    assert result.shift_max_abs_error_ev > 0.012
    assert all(point.shift_residual_ev < -0.010 for point in result.points)
    assert result.optical_gap_rms_error_ev > 0.009


def test_source_rows_imply_consistent_unprinted_momentum_matrix() -> None:
    audit = audit_momentum_matrix(
        temperatures_k=TEMPERATURES_K,
        bandgaps_ev=BANDGAPS_EV,
        source_fermi_shifts_ev=SOURCE_FERMI_SHIFTS_EV,
    )
    np.testing.assert_allclose(
        audit.row_implied_values_ev_cm,
        (
            8.5078030268e-8,
            8.5663482946e-8,
            8.4672979056e-8,
            8.5014094230e-8,
        ),
        rtol=0.0,
        atol=2.0e-17,
    )
    np.testing.assert_allclose(audit.mean_ev_cm, 8.5107146625e-8, atol=2.0e-17)
    assert audit.sample_standard_deviation_ev_cm < 4.2e-10
    assert audit.mean_ev_cm / DINGRONG_PRINTED_MOMENTUM_MATRIX_EV_CM > 1.063


def test_row_implied_mean_reproduces_rounded_source_table() -> None:
    audit = audit_momentum_matrix(
        temperatures_k=TEMPERATURES_K,
        bandgaps_ev=BANDGAPS_EV,
        source_fermi_shifts_ev=SOURCE_FERMI_SHIFTS_EV,
    )
    result = reproduce_table(
        temperatures_k=TEMPERATURES_K,
        bandgaps_ev=BANDGAPS_EV,
        source_fermi_shifts_ev=SOURCE_FERMI_SHIFTS_EV,
        source_fermi_energies_ev=SOURCE_FERMI_ENERGIES_EV,
        source_optical_gaps_ev=SOURCE_OPTICAL_GAPS_EV,
        momentum_matrix_ev_cm=audit.mean_ev_cm,
    )
    assert result.shift_rms_error_ev < 0.0008
    assert result.shift_max_abs_error_ev < 0.0013
    assert result.optical_gap_rms_error_ev < 0.0034
    assert result.optical_gap_max_abs_error_ev < 0.0050
