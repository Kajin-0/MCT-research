import numpy as np
import pytest

from mct_research.transport_noise.contact_control_prototype import (
    FiniteContactBoundaryValues,
    FiniteContactFVParameters,
    FiniteExchangeContact,
    assemble_finite_contact_jacobian,
    assemble_finite_contact_residual,
    contact_balance_metrics,
    contact_regime_metrics,
    exact_zero_field_current,
    exact_zero_field_state,
    loaded_current_fraction,
    reconstruct_finite_contact_state,
    solve_finite_contact_damped_newton,
)
from mct_research.transport_noise.finite_volume_prototype import UniformNodeMesh1D


def make_case(
    *,
    left_biot=2.0,
    right_biot=3.0,
    left_density=1.0,
    right_density=1.4,
    screening=0.0,
    potential_left=0.0,
    potential_right=0.0,
):
    mesh = UniformNodeMesh1D(1.0, 12)
    boundaries = FiniteContactBoundaryValues(
        potential_left,
        potential_right,
        FiniteExchangeContact(left_density, left_biot),
        FiniteExchangeContact(right_density, right_biot),
    )
    parameters = FiniteContactFVParameters(
        screening_strength=screening,
        diffusion_ratio=1.3,
        background_density=1.0,
    )
    return mesh, boundaries, parameters


def test_exact_zero_field_residual_and_current():
    mesh, boundaries, parameters = make_case()
    state = exact_zero_field_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    residual = assemble_finite_contact_residual(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(residual, np.inf) < 1.0e-11
    metrics = contact_balance_metrics(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    exact_current = exact_zero_field_current(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.allclose(metrics.face_current, exact_current)
    assert abs(metrics.left_boundary_mismatch) < 1.0e-12
    assert abs(metrics.right_boundary_mismatch) < 1.0e-12


def test_exact_current_matches_series_resistance_formula():
    mesh, boundaries, parameters = make_case(left_biot=0.4, right_biot=2.5)
    ideal = parameters.diffusion_ratio / mesh.length
    ideal *= boundaries.right.equilibrium_density - boundaries.left.equilibrium_density
    expected = 1.0 / (1.0 + 1.0 / 0.4 + 1.0 / 2.5)
    actual = exact_zero_field_current(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.isclose(actual / ideal, expected)


def test_contact_series_fractions_sum_to_one():
    metrics = contact_regime_metrics(2.0, 4.0)
    assert np.isclose(metrics.bulk_resistance_fraction, 1.0 / 1.75)
    assert np.isclose(metrics.left_contact_resistance_fraction, 0.5 / 1.75)
    assert np.isclose(
        metrics.bulk_resistance_fraction
        + metrics.left_contact_resistance_fraction
        + metrics.right_contact_resistance_fraction,
        1.0,
    )


def test_fast_limit_recovers_ideal_reservoir_current_and_density():
    mesh, boundaries, parameters = make_case(
        left_biot=1.0e9, right_biot=1.0e9
    )
    state = exact_zero_field_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    reconstructed = reconstruct_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    ideal = parameters.diffusion_ratio / mesh.length
    ideal *= boundaries.right.equilibrium_density - boundaries.left.equilibrium_density
    current = exact_zero_field_current(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.isclose(current / ideal, 1.0, rtol=3.0e-9)
    assert np.isclose(
        reconstructed.density[0], boundaries.left.equilibrium_density, rtol=1.0e-9
    )
    assert np.isclose(
        reconstructed.density[-1], boundaries.right.equilibrium_density, rtol=1.0e-9
    )


def test_blocking_limit_has_zero_current_and_population_null_mode():
    mesh, boundaries, parameters = make_case(
        left_biot=0.0,
        right_biot=0.0,
        left_density=1.0,
        right_density=2.0,
    )
    state = exact_zero_field_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    residual = assemble_finite_contact_residual(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(residual, np.inf) < 1.0e-12
    assert exact_zero_field_current(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    ) == 0.0
    metrics = contact_regime_metrics(0.0, 0.0)
    assert metrics.bulk_resistance_fraction == 0.0
    assert metrics.left_contact_resistance_fraction == 0.5
    shifted = state.copy()
    shifted[mesh.interior_count :] += np.log(1.7)
    shifted_residual = assemble_finite_contact_residual(
        shifted, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(shifted_residual, np.inf) < 1.0e-12


def test_one_blocking_contact_forces_zero_current():
    mesh, boundaries, parameters = make_case(
        left_biot=0.0,
        right_biot=2.0,
        left_density=1.0,
        right_density=2.0,
    )
    state = exact_zero_field_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    residual = assemble_finite_contact_residual(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(residual, np.inf) < 1.0e-12


def test_jacobian_matches_centered_difference():
    mesh, boundaries, parameters = make_case(
        left_biot=0.7,
        right_biot=4.0,
        left_density=1.0,
        right_density=0.9,
        screening=0.4,
        potential_left=0.1,
        potential_right=-0.2,
    )
    rng = np.random.default_rng(7)
    state = np.concatenate(
        [
            np.linspace(0.08, -0.18, mesh.interior_count)
            + 0.01 * rng.normal(size=mesh.interior_count),
            np.log(1.0 + 0.08 * rng.normal(size=mesh.node_count)),
        ]
    )
    jacobian = assemble_finite_contact_jacobian(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    epsilon = 2.0e-7
    finite_difference = np.empty_like(jacobian)
    for column in range(state.size):
        perturbation = np.zeros_like(state)
        perturbation[column] = epsilon
        plus = assemble_finite_contact_residual(
            state + perturbation,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
        minus = assemble_finite_contact_residual(
            state - perturbation,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
        finite_difference[:, column] = (plus - minus) / (2.0 * epsilon)
    assert np.allclose(jacobian, finite_difference, rtol=3.0e-6, atol=3.0e-7)


def test_damped_newton_recovers_exact_state():
    mesh, boundaries, parameters = make_case(left_biot=0.8, right_biot=5.0)
    exact = exact_zero_field_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    initial = exact.copy()
    initial[: mesh.interior_count] += 0.04 * np.sin(np.pi * mesh.nodes[1:-1])
    initial[mesh.interior_count :] += 0.1 * np.cos(np.pi * mesh.nodes)
    result = solve_finite_contact_damped_newton(
        initial, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert result.converged, result.termination_reason
    assert result.final_residual_inf_norm < 1.0e-10
    assert np.max(np.abs(result.state - exact)) < 1.0e-8


def test_loaded_current_fraction_limits():
    assert loaded_current_fraction(0.0) == 1.0
    assert loaded_current_fraction(9.0) == 0.1
    assert loaded_current_fraction(1.0e9) < 1.1e-9


def test_asymmetric_contact_drop_dominance():
    metrics = contact_regime_metrics(0.05, 50.0)
    assert metrics.left_contact_resistance_fraction > 0.94
    assert metrics.right_contact_resistance_fraction < 0.001


def test_density_positivity_reconstruction():
    mesh, boundaries, parameters = make_case()
    state = exact_zero_field_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    reconstructed = reconstruct_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    assert np.all(reconstructed.density > 0.0)


def test_blocking_jacobian_exposes_population_null_mode():
    mesh, boundaries, parameters = make_case(left_biot=0.0, right_biot=0.0)
    state = exact_zero_field_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    jacobian = assemble_finite_contact_jacobian(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.matrix_rank(jacobian) == jacobian.shape[0] - 1
    assert np.linalg.cond(jacobian) > 1.0e15


def test_invalid_inputs():
    with pytest.raises(ValueError):
        FiniteExchangeContact(0.0, 1.0)
    with pytest.raises(ValueError):
        FiniteExchangeContact(1.0, -1.0)
    with pytest.raises(ValueError):
        contact_regime_metrics(-1.0, 1.0)
    with pytest.raises(ValueError):
        loaded_current_fraction(-1.0)
