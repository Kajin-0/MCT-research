from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarFVParameters,
    assemble_bipolar_residual,
)
from mct_research.transport_noise.finite_volume_prototype import UniformNodeMesh1D
from mct_research.transport_noise.nonlinear_verification import NewtonOptions
from mct_research.transport_noise.trap_kinetics_prototype import (
    ReversibleTrapParameters,
    assemble_trap_bipolar_jacobian,
    assemble_trap_bipolar_residual,
    effective_mass_action_coefficient,
    equilibrium_trap_state,
    logit_from_occupancy,
    occupancy_from_logit,
    pack_trap_state,
    reconstruct_trap_state,
    reversible_trap_channel_rates,
    solve_trap_bipolar_damped_newton,
    steady_trap_occupancy,
    trap_balance_metrics,
    trap_eliminated_pair_rate,
)


def _mesh(intervals: int = 8) -> UniformNodeMesh1D:
    return UniformNodeMesh1D(length=1.0, intervals=intervals)


def _boundaries(n: float = 1.0, p: float = 1.0) -> BipolarBoundaryValues:
    return BipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.0,
        electron_density_left=n,
        electron_density_right=n,
        hole_density_left=p,
        hole_density_right=p,
    )


def _trap(density: float = 0.3) -> ReversibleTrapParameters:
    return ReversibleTrapParameters(
        trap_density=density,
        electron_capture_coefficient=0.7,
        hole_capture_coefficient=0.4,
        equilibrium_electron_density=1.2,
        equilibrium_hole_density=0.8,
        equilibrium_occupancy=0.35,
    )


def _arbitrary_state(mesh: UniformNodeMesh1D) -> np.ndarray:
    x = mesh.nodes[1:-1]
    return pack_trap_state(
        0.12 * np.sin(np.pi * x),
        np.log(1.1 + 0.15 * np.cos(np.pi * x)),
        np.log(0.9 + 0.12 * np.sin(2.0 * np.pi * x)),
        logit_from_occupancy(0.25 + 0.3 * x),
    )


def test_emission_coefficients_enforce_both_equilibrium_channel_balances() -> None:
    trap = _trap()
    rates = reversible_trap_channel_rates(
        np.array([trap.equilibrium_electron_density]),
        np.array([trap.equilibrium_hole_density]),
        np.array([trap.equilibrium_occupancy]),
        trap_parameters=trap,
    )
    assert rates.electron_capture == pytest.approx(rates.electron_emission)
    assert rates.hole_capture == pytest.approx(rates.hole_emission)
    assert rates.trap_kinetic_rate == pytest.approx(0.0, abs=1e-15)


def test_channel_directions_follow_capture_and_emission_definitions() -> None:
    trap = _trap()
    occupancy = np.array([0.2, 0.8])
    rates = reversible_trap_channel_rates(
        np.array([2.0, 0.2]),
        np.array([0.2, 2.0]),
        occupancy,
        trap_parameters=trap,
    )
    assert rates.net_electron_capture[0] > 0.0
    assert rates.net_electron_capture[1] < 0.0
    assert rates.net_hole_capture[0] < 0.0
    assert rates.net_hole_capture[1] > 0.0


def test_logit_transform_is_stable_and_strictly_bounded() -> None:
    logits = np.array([-100.0, -3.0, 0.0, 2.0, 100.0])
    occupancy = occupancy_from_logit(logits)
    assert np.all(occupancy > 0.0)
    assert np.all(occupancy < 1.0)
    middle = occupancy[1:-1]
    assert logit_from_occupancy(middle) == pytest.approx(logits[1:-1])


def test_constant_detailed_balance_state_has_zero_full_residual() -> None:
    mesh = _mesh()
    trap = _trap()
    boundaries = BipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.0,
        electron_density_left=trap.equilibrium_electron_density,
        electron_density_right=trap.equilibrium_electron_density,
        hole_density_left=trap.equilibrium_hole_density,
        hole_density_right=trap.equilibrium_hole_density,
    )
    fixed_charge = (
        trap.equilibrium_electron_density
        + trap.trap_density * trap.equilibrium_occupancy
        - trap.equilibrium_hole_density
    )
    parameters = BipolarFVParameters(
        screening_strength=1.7,
        fixed_charge_density=fixed_charge,
    )
    state = equilibrium_trap_state(
        mesh=mesh,
        boundaries=boundaries,
        trap_parameters=trap,
    )
    residual = assemble_trap_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    assert np.linalg.norm(residual, ord=np.inf) < 2e-13


def test_zero_trap_density_reduces_exactly_to_source_free_bipolar_blocks() -> None:
    mesh = _mesh()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(screening_strength=0.8)
    trap = ReversibleTrapParameters(
        trap_density=0.0,
        electron_capture_coefficient=0.7,
        hole_capture_coefficient=0.4,
    )
    state = _arbitrary_state(mesh)
    count = mesh.interior_count
    full = assemble_trap_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    base = assemble_bipolar_residual(
        state[: 3 * count],
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    assert np.array_equal(full[: 3 * count], base)
    assert np.array_equal(full[3 * count :], np.zeros(count))


def test_local_source_contributions_cancel_from_charge_balance_identity() -> None:
    mesh = _mesh()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(screening_strength=0.9)
    trap = _trap()
    state = _arbitrary_state(mesh)
    count = mesh.interior_count
    full = assemble_trap_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    base = assemble_bipolar_residual(
        state[: 3 * count],
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    electron_source = full[count : 2 * count] - base[count : 2 * count]
    hole_source = full[2 * count : 3 * count] - base[2 * count :]
    trap_source = full[3 * count :]
    assert electron_source + hole_source + trap_source == pytest.approx(
        0.0,
        abs=2e-15,
    )


def test_steady_occupancy_equalizes_net_capture_channels() -> None:
    trap = _trap()
    electron = np.array([0.5, 1.2, 2.4])
    hole = np.array([2.0, 0.8, 0.4])
    occupancy = steady_trap_occupancy(
        electron,
        hole,
        trap_parameters=trap,
    )
    rates = reversible_trap_channel_rates(
        electron,
        hole,
        occupancy,
        trap_parameters=trap,
    )
    assert rates.net_electron_capture == pytest.approx(rates.net_hole_capture)
    assert rates.trap_kinetic_rate == pytest.approx(0.0, abs=2e-16)


def test_eliminated_rate_has_exact_mass_action_numerator_and_positive_coefficient() -> None:
    trap = _trap()
    electron = np.array([0.6, 1.2, 2.0])
    hole = np.array([0.7, 0.8, 1.5])
    rate = trap_eliminated_pair_rate(
        electron,
        hole,
        trap_parameters=trap,
    )
    coefficient = effective_mass_action_coefficient(
        electron,
        hole,
        trap_parameters=trap,
    )
    assert np.all(coefficient > 0.0)
    assert rate == pytest.approx(
        coefficient * (electron * hole - trap.equilibrium_product)
    )
    assert rate[0] < 0.0
    assert rate[1] == pytest.approx(0.0, abs=1e-15)
    assert rate[2] > 0.0


def test_analytical_jacobian_matches_centered_finite_difference() -> None:
    mesh = _mesh(intervals=6)
    boundaries = _boundaries()
    parameters = BipolarFVParameters(
        screening_strength=1.1,
        electron_diffusion_ratio=0.8,
        hole_diffusion_ratio=1.3,
        fixed_charge_density=0.2,
    )
    trap = _trap()
    state = _arbitrary_state(mesh)
    analytical = assemble_trap_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    numerical = np.empty_like(analytical)
    epsilon = 2e-7
    for column in range(state.size):
        plus = state.copy()
        minus = state.copy()
        plus[column] += epsilon
        minus[column] -= epsilon
        numerical[:, column] = (
            assemble_trap_bipolar_residual(
                plus,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap,
            )
            - assemble_trap_bipolar_residual(
                minus,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap,
            )
        ) / (2.0 * epsilon)
    assert analytical == pytest.approx(numerical, rel=3e-7, abs=2e-7)


def test_arbitrary_state_global_balance_mismatches_match_integrated_residuals() -> None:
    mesh = _mesh()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(screening_strength=0.6)
    trap = _trap()
    state = _arbitrary_state(mesh)
    count = mesh.interior_count
    residual = assemble_trap_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    metrics = trap_balance_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    assert metrics.electron_absolute_mismatch == pytest.approx(
        abs(mesh.spacing * np.sum(residual[count : 2 * count]))
    )
    assert metrics.hole_absolute_mismatch == pytest.approx(
        abs(mesh.spacing * np.sum(residual[2 * count : 3 * count]))
    )
    assert metrics.trap_absolute_mismatch == pytest.approx(
        abs(mesh.spacing * np.sum(residual[3 * count :]))
    )
    summed = (
        residual[count : 2 * count]
        + residual[2 * count : 3 * count]
        + residual[3 * count :]
    )
    assert metrics.total_current_terminal_difference == pytest.approx(
        mesh.spacing * np.sum(summed)
    )


def test_equilibrium_solver_terminates_without_iteration() -> None:
    mesh = _mesh()
    trap = _trap()
    boundaries = BipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.0,
        electron_density_left=trap.equilibrium_electron_density,
        electron_density_right=trap.equilibrium_electron_density,
        hole_density_left=trap.equilibrium_hole_density,
        hole_density_right=trap.equilibrium_hole_density,
    )
    parameters = BipolarFVParameters(
        screening_strength=1.0,
        fixed_charge_density=(
            trap.equilibrium_electron_density
            + trap.trap_density * trap.equilibrium_occupancy
            - trap.equilibrium_hole_density
        ),
    )
    state = equilibrium_trap_state(
        mesh=mesh,
        boundaries=boundaries,
        trap_parameters=trap,
    )
    result = solve_trap_bipolar_damped_newton(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    assert result.converged
    assert result.termination_reason == "initial_residual_converged"
    assert result.iterations == 0


def test_contact_supplied_trap_recombination_converges_and_total_current_is_constant() -> None:
    mesh = _mesh(intervals=16)
    trap = ReversibleTrapParameters(
        trap_density=0.12,
        electron_capture_coefficient=0.45,
        hole_capture_coefficient=0.45,
        equilibrium_electron_density=1.0,
        equilibrium_hole_density=1.0,
        equilibrium_occupancy=0.5,
    )
    boundaries = _boundaries(n=2.0, p=2.0)
    parameters = BipolarFVParameters(
        screening_strength=0.7,
        fixed_charge_density=trap.trap_density * 0.5,
    )
    count = mesh.interior_count
    state = pack_trap_state(
        np.zeros(count),
        np.full(count, np.log(2.0)),
        np.full(count, np.log(2.0)),
        np.full(count, logit_from_occupancy(0.5)),
    )
    result = solve_trap_bipolar_damped_newton(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        options=NewtonOptions(
            maximum_iterations=40,
            absolute_tolerance=2e-10,
            relative_tolerance=1e-10,
        ),
    )
    assert result.converged, result.termination_reason
    reconstructed = reconstruct_trap_state(
        result.state,
        mesh=mesh,
        boundaries=boundaries,
    )
    rates = reversible_trap_channel_rates(
        reconstructed.electron_density[1:-1],
        reconstructed.hole_density[1:-1],
        reconstructed.trap_occupancy,
        trap_parameters=trap,
    )
    assert mesh.spacing * np.sum(rates.net_electron_capture) > 0.0
    assert result.balance.electron_relative_mismatch < 2e-9
    assert result.balance.hole_relative_mismatch < 2e-9
    assert result.balance.trap_relative_mismatch < 2e-9
    assert result.balance.total_current_relative_variation < 2e-9


def test_invalid_trap_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        ReversibleTrapParameters(
            trap_density=-1.0,
            electron_capture_coefficient=1.0,
            hole_capture_coefficient=1.0,
        )
    with pytest.raises(ValueError):
        ReversibleTrapParameters(
            trap_density=1.0,
            electron_capture_coefficient=1.0,
            hole_capture_coefficient=1.0,
            equilibrium_occupancy=1.0,
        )
    with pytest.raises(ValueError):
        logit_from_occupancy(np.array([0.0, 0.5]))
    with pytest.raises(ValueError):
        reversible_trap_channel_rates(
            np.array([1.0]),
            np.array([1.0]),
            np.array([1.0]),
            trap_parameters=_trap(),
        )
