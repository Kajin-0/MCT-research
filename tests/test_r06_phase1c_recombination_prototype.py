from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarFVParameters,
    assemble_bipolar_jacobian,
    assemble_bipolar_residual,
    linear_bipolar_reservoir_state,
    reconstruct_bipolar_state,
)
from mct_research.transport_noise.finite_volume_prototype import UniformNodeMesh1D
from mct_research.transport_noise.recombination_prototype import (
    MassActionPairParameters,
    assemble_recombining_bipolar_jacobian,
    assemble_recombining_bipolar_residual,
    mass_action_pair_rate,
    pair_balance_metrics,
    solve_recombining_bipolar_damped_newton,
)


def _equilibrium_case(
    intervals: int = 12,
    electron_density: float = 2.0,
    hole_density: float = 0.5,
):
    mesh = UniformNodeMesh1D(length=1.0, intervals=intervals)
    boundaries = BipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.0,
        electron_density_left=electron_density,
        electron_density_right=electron_density,
        hole_density_left=hole_density,
        hole_density_right=hole_density,
    )
    parameters = BipolarFVParameters(
        screening_strength=4.0,
        electron_diffusion_ratio=1.0,
        hole_diffusion_ratio=0.7,
        fixed_charge_density=electron_density - hole_density,
    )
    pair_parameters = MassActionPairParameters(
        rate_coefficient=3.0,
        equilibrium_product=electron_density * hole_density,
    )
    state = linear_bipolar_reservoir_state(
        mesh=mesh,
        boundaries=boundaries,
    )
    return mesh, boundaries, parameters, pair_parameters, state


def test_rate_sign_and_detailed_balance():
    pair_parameters = MassActionPairParameters(
        rate_coefficient=2.0,
        equilibrium_product=1.0,
    )
    assert (
        mass_action_pair_rate(2.0, 1.0, pair_parameters=pair_parameters)
        == 2.0
    )
    assert (
        mass_action_pair_rate(0.5, 1.0, pair_parameters=pair_parameters)
        == -1.0
    )
    assert (
        mass_action_pair_rate(2.0, 0.5, pair_parameters=pair_parameters)
        == 0.0
    )


def test_exact_equilibrium_has_zero_residual_and_balance():
    mesh, boundaries, parameters, pair_parameters, state = _equilibrium_case()
    residual = assemble_recombining_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    assert np.allclose(residual, 0.0, atol=1.0e-13)
    metrics = pair_balance_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    assert np.allclose(metrics.pair_rate, 0.0)
    assert metrics.total_current_relative_variation == 0.0


def test_zero_rate_reduces_exactly_to_bipolar_base():
    mesh, boundaries, parameters, _, state = _equilibrium_case()
    state = state + 0.1 * np.random.default_rng(12).normal(size=state.size)
    pair_parameters = MassActionPairParameters(
        rate_coefficient=0.0,
        equilibrium_product=7.0,
    )
    assert np.array_equal(
        assemble_recombining_bipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            pair_parameters=pair_parameters,
        ),
        assemble_bipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        ),
    )
    assert np.array_equal(
        assemble_recombining_bipolar_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            pair_parameters=pair_parameters,
        ),
        assemble_bipolar_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        ),
    )


def test_pair_source_cancels_from_sum_of_continuity_blocks():
    mesh, boundaries, parameters, pair_parameters, state = _equilibrium_case()
    state = state + 0.1 * np.random.default_rng(3).normal(size=state.size)
    base = assemble_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    source = assemble_recombining_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    count = mesh.interior_count
    assert np.allclose(
        source[count : 2 * count] + source[2 * count :],
        base[count : 2 * count] + base[2 * count :],
    )


def test_analytical_jacobian_matches_centered_difference():
    mesh, boundaries, parameters, pair_parameters, state = _equilibrium_case(
        intervals=8
    )
    state = state + 0.08 * np.random.default_rng(8).normal(size=state.size)
    analytical = assemble_recombining_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    numerical = np.empty_like(analytical)
    for column in range(state.size):
        step = 1.0e-7 * max(1.0, abs(state[column]))
        plus = state.copy()
        minus = state.copy()
        plus[column] += step
        minus[column] -= step
        numerical[:, column] = (
            assemble_recombining_bipolar_residual(
                plus,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                pair_parameters=pair_parameters,
            )
            - assemble_recombining_bipolar_residual(
                minus,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                pair_parameters=pair_parameters,
            )
        ) / (2.0 * step)
    assert np.allclose(analytical, numerical, rtol=2.0e-6, atol=2.0e-7)


def test_arbitrary_state_balance_mismatch_matches_residual_integral():
    mesh, boundaries, parameters, pair_parameters, state = _equilibrium_case()
    state = state + 0.12 * np.random.default_rng(4).normal(size=state.size)
    residual = assemble_recombining_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    metrics = pair_balance_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    count = mesh.interior_count
    assert np.isclose(
        metrics.electron_terminal_difference - metrics.integrated_pair_rate,
        mesh.spacing * np.sum(residual[count : 2 * count]),
    )
    assert np.isclose(
        metrics.hole_terminal_difference + metrics.integrated_pair_rate,
        mesh.spacing * np.sum(residual[2 * count :]),
    )
    assert np.isclose(
        metrics.total_current_terminal_difference,
        mesh.spacing
        * np.sum(residual[count : 2 * count] + residual[2 * count :]),
    )


def test_contact_supplied_symmetric_recombination_state_converges():
    mesh = UniformNodeMesh1D(length=1.0, intervals=24)
    boundaries = BipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.0,
        electron_density_left=1.5,
        electron_density_right=1.5,
        hole_density_left=1.5,
        hole_density_right=1.5,
    )
    parameters = BipolarFVParameters(
        screening_strength=5.0,
        electron_diffusion_ratio=1.0,
        hole_diffusion_ratio=1.0,
        fixed_charge_density=0.0,
    )
    pair_parameters = MassActionPairParameters(
        rate_coefficient=2.0,
        equilibrium_product=1.0,
    )
    initial = linear_bipolar_reservoir_state(
        mesh=mesh,
        boundaries=boundaries,
    )
    result = solve_recombining_bipolar_damped_newton(
        initial,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    assert result.converged, result.termination_reason
    assert result.final_residual_inf_norm <= result.target_residual_inf_norm
    reconstructed = reconstruct_bipolar_state(
        result.state,
        mesh=mesh,
        boundaries=boundaries,
    )
    assert np.allclose(reconstructed.potential, 0.0, atol=1.0e-11)
    assert np.allclose(
        reconstructed.electron_density,
        reconstructed.hole_density,
        atol=1.0e-11,
    )
    assert reconstructed.electron_density[mesh.intervals // 2] < 1.5
    assert result.pair_balance.integrated_pair_rate > 0.0
    assert result.pair_balance.electron_relative_mismatch < 1.0e-10
    assert result.pair_balance.hole_relative_mismatch < 1.0e-10
    assert result.pair_balance.total_current_relative_variation < 1.0e-10


def test_equilibrium_solver_terminates_without_iteration():
    mesh, boundaries, parameters, pair_parameters, state = _equilibrium_case()
    result = solve_recombining_bipolar_damped_newton(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    assert result.converged
    assert result.termination_reason == "initial_residual_converged"
    assert result.iterations == 0


def test_invalid_parameters_and_densities_are_rejected():
    with pytest.raises(ValueError):
        MassActionPairParameters(rate_coefficient=-1.0)
    with pytest.raises(ValueError):
        MassActionPairParameters(rate_coefficient=1.0, equilibrium_product=0.0)
    pair_parameters = MassActionPairParameters(rate_coefficient=1.0)
    with pytest.raises(ValueError):
        mass_action_pair_rate(
            np.array([1.0]),
            np.array([1.0, 2.0]),
            pair_parameters=pair_parameters,
        )
    with pytest.raises(ValueError):
        mass_action_pair_rate(
            np.array([0.0]),
            np.array([1.0]),
            pair_parameters=pair_parameters,
        )


def test_source_jacobian_cross_blocks_have_expected_signs():
    mesh, boundaries, parameters, pair_parameters, state = _equilibrium_case(
        intervals=6
    )
    base = assemble_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    full = assemble_recombining_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        pair_parameters=pair_parameters,
    )
    delta = full - base
    count = mesh.interior_count
    electron_hole_diagonal = np.diag(delta[count : 2 * count, 2 * count :])
    assert np.all(electron_hole_diagonal < 0.0)
    assert np.allclose(
        np.diag(delta[2 * count :, count : 2 * count]),
        -electron_hole_diagonal,
    )
    assert np.array_equal(
        delta[count:, :count],
        np.zeros((2 * count, count)),
    )
