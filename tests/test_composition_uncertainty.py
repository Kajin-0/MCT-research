from __future__ import annotations

import numpy as np
import pytest

from mct_research.analytical_benchmark import (
    OscillatorBasisSpec,
    fit_linear_gap_model,
    oscillator_design_matrix,
)
from mct_research.composition_uncertainty import (
    CompositionAwareGapData,
    CompositionUncertaintySpec,
    fit_composition_aware_gap_model,
    leave_one_source_out,
    named_composition_holdout_cross_validation,
    oscillator_composition_derivative_matrix,
)


def test_zero_composition_uncertainty_reproduces_exact_x_fit() -> None:
    x = np.repeat([0.2, 0.4, 0.6, 0.8], 4)
    temperature = np.tile([0.0, 50.0, 150.0, 300.0], 4)
    groups = np.repeat(["s1", "s2", "s3", "s4"], 4)
    specification = OscillatorBasisSpec(
        static_degree=2,
        amplitude_degree=1,
        oscillator_temperatures_k=(140.0,),
    )
    matrix, _ = oscillator_design_matrix(specification, x, temperature)
    gap = matrix @ np.array([-0.30, 1.80, -0.20, 0.04, -0.08])
    data = CompositionAwareGapData.from_arrays(
        x,
        temperature,
        gap,
        sigma_ev=0.001,
        sigma_x=0.0,
        group=groups,
    )

    exact = fit_linear_gap_model(data.benchmark, specification)
    aware = fit_composition_aware_gap_model(data, specification)

    np.testing.assert_allclose(aware.coefficients, exact.coefficients, atol=0.0)
    np.testing.assert_allclose(aware.fitted_gap_ev, exact.fitted_gap_ev, atol=0.0)
    np.testing.assert_allclose(aware.effective_sigma_ev, data.sigma_ev, atol=0.0)
    assert aware.composition_mode == "exact_x"
    assert aware.composition_iterations == 0
    assert aware.composition_converged is True


def test_nonzero_sigma_x_requires_explicit_interpretation() -> None:
    data = CompositionAwareGapData.from_arrays(
        [0.2, 0.4, 0.6],
        [0.0, 0.0, 0.0],
        [0.04, 0.38, 0.72],
        sigma_ev=0.001,
        sigma_x=0.003,
        group=["a", "b", "c"],
    )

    with pytest.raises(ValueError, match="explicit CompositionUncertaintySpec"):
        fit_composition_aware_gap_model(
            data,
            OscillatorBasisSpec(static_degree=1),
        )


def test_analytic_composition_derivative_matches_finite_difference() -> None:
    specification = OscillatorBasisSpec(
        static_degree=3,
        amplitude_degree=2,
        oscillator_temperatures_k=(120.0,),
        quasiharmonic_degree=2,
    )
    coefficients = np.array(
        [-0.30, 1.8, -0.2, 0.1, 0.02, -0.03, 0.04, 4.0e-4, -2.0e-4, 1.0e-4]
    )
    x = np.array([0.2, 0.5, 0.8])
    temperature = np.array([20.0, 100.0, 300.0])
    derivative_matrix, _ = oscillator_composition_derivative_matrix(
        specification, x, temperature
    )
    analytic = derivative_matrix @ coefficients

    step = 1.0e-7
    plus, _ = oscillator_design_matrix(specification, x + step, temperature)
    minus, _ = oscillator_design_matrix(specification, x - step, temperature)
    finite_difference = ((plus - minus) @ coefficients) / (2.0 * step)

    np.testing.assert_allclose(analytic, finite_difference, rtol=2.0e-8, atol=1.0e-10)


def test_independent_linearized_variance_exposes_five_mev_composition_scale() -> None:
    x = np.array([0.2, 0.4, 0.6, 0.8])
    gap = -0.30 + 1.70 * x
    data = CompositionAwareGapData.from_arrays(
        x,
        np.zeros_like(x),
        gap,
        sigma_ev=0.001,
        sigma_x=0.003,
        group=["a", "b", "c", "d"],
    )

    fit = fit_composition_aware_gap_model(
        data,
        OscillatorBasisSpec(static_degree=1),
        composition_uncertainty=CompositionUncertaintySpec(mode="independent"),
    )

    expected_composition_sigma_ev = 1.70 * 0.003
    expected_total_sigma_ev = np.sqrt(0.001**2 + expected_composition_sigma_ev**2)
    np.testing.assert_allclose(
        fit.composition_derivative_ev_per_x,
        1.70,
        rtol=0.0,
        atol=1.0e-12,
    )
    np.testing.assert_allclose(
        fit.effective_sigma_ev,
        expected_total_sigma_ev,
        rtol=1.0e-12,
    )
    assert expected_composition_sigma_ev * 1000.0 == pytest.approx(5.1)
    assert fit.composition_converged is True


def test_shared_group_mode_builds_correlated_specimen_blocks() -> None:
    x = np.repeat([0.2, 0.6], 3)
    temperature = np.tile([0.0, 100.0, 200.0], 2)
    groups = np.repeat(["specimen_a", "specimen_b"], 3)
    specification = OscillatorBasisSpec(
        static_degree=1,
        quasiharmonic_degree=0,
    )
    matrix, _ = oscillator_design_matrix(specification, x, temperature)
    gap = matrix @ np.array([-0.30, 1.70, 5.0e-4])
    data = CompositionAwareGapData.from_arrays(
        x,
        temperature,
        gap,
        sigma_ev=0.001,
        sigma_x=0.003,
        group=groups,
    )

    fit = fit_composition_aware_gap_model(
        data,
        specification,
        composition_uncertainty=CompositionUncertaintySpec(mode="shared_group"),
    )

    expected_covariance = 1.70**2 * 0.003**2
    assert fit.effective_covariance_ev2[0, 1] == pytest.approx(expected_covariance)
    assert fit.effective_covariance_ev2[0, 2] == pytest.approx(expected_covariance)
    assert fit.effective_covariance_ev2[0, 3] == pytest.approx(0.0)
    assert fit.effective_covariance_ev2[3, 5] == pytest.approx(expected_covariance)


def test_shared_group_mode_rejects_inconsistent_specimen_composition() -> None:
    data = CompositionAwareGapData.from_arrays(
        [0.20, 0.21, 0.60, 0.60],
        [0.0, 100.0, 0.0, 100.0],
        [0.04, 0.06, 0.72, 0.74],
        sigma_ev=0.001,
        sigma_x=[0.003, 0.003, 0.003, 0.003],
        group=["a", "a", "b", "b"],
    )

    with pytest.raises(ValueError, match="composition values disagree"):
        fit_composition_aware_gap_model(
            data,
            OscillatorBasisSpec(static_degree=1),
            composition_uncertainty=CompositionUncertaintySpec(
                mode="shared_group"
            ),
        )


def test_mixed_measurement_classes_are_not_pooled_implicitly() -> None:
    data = CompositionAwareGapData.from_arrays(
        [0.2, 0.4, 0.6, 0.8],
        [0.0, 0.0, 0.0, 0.0],
        [0.04, 0.38, 0.72, 1.06],
        sigma_ev=0.001,
        sigma_x=0.0,
        group=["a", "b", "c", "d"],
        measurement_class=["optical", "optical", "electrical", "electrical"],
    )

    with pytest.raises(ValueError, match="mixed measurement classes"):
        fit_composition_aware_gap_model(
            data,
            OscillatorBasisSpec(static_degree=1),
        )

    fit = fit_composition_aware_gap_model(
        data,
        OscillatorBasisSpec(static_degree=1),
        allow_mixed_measurement_classes=True,
    )
    assert fit.metrics.rmse_mev < 1.0e-8


def test_shared_composition_cross_validation_cannot_split_a_specimen() -> None:
    x = np.repeat([0.2, 0.4, 0.6], 2)
    temperature = np.tile([0.0, 100.0], 3)
    groups = np.repeat(["a", "b", "c"], 2)
    gap = -0.30 + 1.70 * x + 5.0e-4 * temperature
    data = CompositionAwareGapData.from_arrays(
        x,
        temperature,
        gap,
        sigma_ev=0.001,
        sigma_x=0.003,
        group=groups,
    )

    with pytest.raises(ValueError, match="splits a shared-composition group"):
        named_composition_holdout_cross_validation(
            data,
            OscillatorBasisSpec(static_degree=1, quasiharmonic_degree=0),
            {"zero_temperature": temperature == 0.0, "warm": temperature > 0.0},
            composition_uncertainty=CompositionUncertaintySpec(
                mode="shared_group"
            ),
        )


def test_leave_one_source_out_uses_source_labels_without_offset_fitting() -> None:
    x = np.array([0.2, 0.4, 0.6, 0.8])
    gap = -0.30 + 1.70 * x
    data = CompositionAwareGapData.from_arrays(
        x,
        np.zeros_like(x),
        gap,
        sigma_ev=0.001,
        sigma_x=0.0,
        group=["a", "b", "c", "d"],
        source=["source_1", "source_1", "source_2", "source_2"],
        measurement_class=["optical"] * 4,
    )

    result = leave_one_source_out(
        data,
        OscillatorBasisSpec(static_degree=1),
    )

    np.testing.assert_allclose(result.predictions_ev, gap, atol=1.0e-12)
    assert {fold.name for fold in result.folds} == {"source_1", "source_2"}
    assert result.metrics.rmse_mev < 1.0e-8
