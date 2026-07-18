from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from mct_research.kane8 import ExtendedKaneParameters, hamiltonian_two_p
from mct_research.thermal_kane import (
    RationalSelfEnergy,
    ThermalParameterScale,
    bose_thermal_factor,
    fit_extended_kane_parameters,
    gamma_irrep_covariance_residual,
    gamma_irrep_matrix,
    linear_self_energy_for_target,
    linearized_quasiparticle_hamiltonian,
    linearized_scalar_pole,
    solve_quasiparticle_pole,
    thermal_extended_parameters,
)
from tools.run_finite_temperature_kane_oracle import analyze


def test_bose_thermal_factor_is_zero_at_zero_and_overflow_safe() -> None:
    assert bose_thermal_factor(100.0, 0.0) == 0.0
    assert bose_thermal_factor(1000.0, 1.0) == 0.0
    assert bose_thermal_factor(100.0, 100.0) == pytest.approx(
        2.0 / np.expm1(1.0)
    )
    with pytest.raises(ValueError):
        bose_thermal_factor(-1.0, 100.0)
    with pytest.raises(ValueError):
        bose_thermal_factor(100.0, -1.0)


def test_gamma_self_energy_has_exact_td_block_structure() -> None:
    matrix = gamma_irrep_matrix(0.02, -0.01, 0.03)
    assert gamma_irrep_covariance_residual(matrix) < 1.0e-15
    perturbed = matrix.copy()
    perturbed[0, 2] = perturbed[2, 0] = 1.0e-3
    assert gamma_irrep_covariance_residual(perturbed) > 1.0e-6


def test_matrix_quasiparticle_linearization_recovers_known_target() -> None:
    base = ExtendedKaneParameters(
        ev=0.1,
        eg=0.8,
        delta=0.9,
        p8=7.2,
        p7=6.4,
        f=-0.05,
        gamma1=1.4,
        gamma2=-0.2,
        gamma3=0.1,
    )
    target = ExtendedKaneParameters(
        ev=0.11,
        eg=0.77,
        delta=0.91,
        p8=7.18,
        p7=6.42,
        f=-0.04,
        gamma1=1.42,
        gamma2=-0.19,
        gamma3=0.12,
    )
    k_point = np.asarray([0.005, 0.004, 0.003])
    bare_h = hamiltonian_two_p(k_point, base)
    target_h = hamiltonian_two_p(k_point, target)
    derivative = gamma_irrep_matrix(0.08, 0.04, 0.06)
    sigma0 = linear_self_energy_for_target(bare_h, target_h, derivative, 0.5)
    recovered, diagnostics = linearized_quasiparticle_hamiltonian(
        bare_h, sigma0, derivative, 0.5
    )
    np.testing.assert_allclose(recovered, target_h, atol=1.0e-12)
    assert diagnostics["minimum_metric_eigenvalue"] > 0.9


def test_matrix_quasiparticle_linearization_rejects_nonpositive_metric() -> None:
    zero = np.zeros((2, 2), dtype=complex)
    with pytest.raises(ValueError, match="positive definite"):
        linearized_quasiparticle_hamiltonian(
            zero,
            zero,
            np.eye(2, dtype=complex),
            0.0,
        )


def test_rational_exact_and_linearized_poles_agree_in_declared_regime() -> None:
    bare = 0.5
    self_energy = RationalSelfEnergy(
        reference_ev=bare,
        offset_ev=0.01,
        slope=0.05,
        coupling_ev=0.025,
        remote_ev=2.0,
    )
    exact = solve_quasiparticle_pole(
        bare, self_energy, (bare - 0.2, bare + 0.2)
    )
    linearized = linearized_scalar_pole(bare, self_energy, bare)
    assert abs(exact - linearized) < 1.0e-6
    residual = exact - bare - self_energy.value(exact)
    assert abs(residual) < 1.0e-12


def test_thermal_parameter_trajectory_and_matrix_recovery() -> None:
    base = ExtendedKaneParameters(
        ev=0.1,
        eg=0.8,
        delta=0.9,
        p8=7.2,
        p7=6.4,
        f=-0.05,
        gamma1=1.4,
        gamma2=-0.2,
        gamma3=0.1,
    )
    scales = [
        ThermalParameterScale(70.0, {"eg": 0.004, "p8": 0.002}),
        ThermalParameterScale(240.0, {"eg": -0.018, "p7": -0.003}),
    ]
    target = thermal_extended_parameters(base, scales, 200.0)
    points = [
        np.zeros(3),
        np.asarray([0.0, 0.0, 0.01]),
        np.asarray([0.01, 0.0, 0.0]),
        np.asarray([0.007, 0.007, 0.0]),
        np.asarray([0.0058, 0.0058, 0.0058]),
    ]
    matrices = [hamiltonian_two_p(point, target) for point in points]
    recovered, diagnostics = fit_extended_kane_parameters(points, matrices)
    for name in target.__dataclass_fields__:
        assert getattr(recovered, name) == pytest.approx(
            getattr(target, name), abs=1.0e-10
        )
    assert diagnostics["relative_residual"] < 1.0e-12


def test_complete_finite_temperature_oracle_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    result = analyze(
        root
        / "first_principles/matrix_oracle/finite_temperature_kane_oracle.json"
    )
    assert result["status"] == "finite_temperature_kane_matrix_oracle_passed"
    assert all(result["checks"].values())
    assert result["decision"]["matrix_pipeline_ready_for_real_input"]
    assert not result["decision"]["a1_electron_phonon_authorized"]
    assert (
        result["thermal_reduction"]["one_scale"]
        ["maximum_holdout_absolute_error_mev"]
        >= 2.0
    )
    assert (
        result["thermal_reduction"]["two_scale"]
        ["maximum_holdout_absolute_error_mev"]
        <= 1.0e-8
    )
    assert result["thermal_reduction"]["turnover_detected"]
