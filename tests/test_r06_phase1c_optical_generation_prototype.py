from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarFVParameters,
)
from mct_research.transport_noise.finite_volume_prototype import UniformNodeMesh1D
from mct_research.transport_noise.nonlinear_verification import NewtonOptions
from mct_research.transport_noise.optical_generation_prototype import (
    UniformOpticalGeneration,
    assemble_illuminated_trap_jacobian,
    assemble_illuminated_trap_residual,
    optical_balance_metrics,
    solve_illuminated_trap_damped_newton,
)
from mct_research.transport_noise.trap_kinetics_prototype import (
    ReversibleTrapParameters,
    assemble_trap_bipolar_jacobian,
    assemble_trap_bipolar_residual,
    logit_from_occupancy,
    pack_trap_state,
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


def _trap() -> ReversibleTrapParameters:
    return ReversibleTrapParameters(
        trap_density=0.12,
        electron_capture_coefficient=0.45,
        hole_capture_coefficient=0.45,
        equilibrium_electron_density=1.0,
        equilibrium_hole_density=1.0,
        equilibrium_occupancy=0.5,
    )


def _uniform_state(mesh: UniformNodeMesh1D, density: float = 1.0) -> np.ndarray:
    count = mesh.interior_count
    return pack_trap_state(
        np.zeros(count),
        np.full(count, np.log(density)),
        np.full(count, np.log(density)),
        np.full(count, logit_from_occupancy(0.5)),
    )


def _arbitrary_state(mesh: UniformNodeMesh1D) -> np.ndarray:
    x = mesh.nodes[1:-1]
    return pack_trap_state(
        0.08 * np.sin(np.pi * x),
        np.log(1.05 + 0.13 * np.cos(np.pi * x)),
        np.log(0.95 + 0.11 * np.sin(2.0 * np.pi * x)),
        logit_from_occupancy(0.3 + 0.25 * x),
    )


def test_generation_parameter_rejects_invalid_rate() -> None:
    with pytest.raises(ValueError):
        UniformOpticalGeneration(-1.0)
    with pytest.raises(ValueError):
        UniformOpticalGeneration(float("inf"))


def test_dark_residual_reduces_bitwise_to_trap_model() -> None:
    mesh = _mesh()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(
        screening_strength=0.7,
        fixed_charge_density=0.1,
    )
    trap = _trap()
    state = _arbitrary_state(mesh)
    assert np.array_equal(
        assemble_illuminated_trap_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap,
            optical_generation=UniformOpticalGeneration(0.0),
        ),
        assemble_trap_bipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap,
        ),
    )


def test_dark_jacobian_reduces_bitwise_to_trap_model() -> None:
    mesh = _mesh()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(
        screening_strength=0.7,
        fixed_charge_density=0.1,
    )
    trap = _trap()
    state = _arbitrary_state(mesh)
    assert np.array_equal(
        assemble_illuminated_trap_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap,
            optical_generation=UniformOpticalGeneration(0.0),
        ),
        assemble_trap_bipolar_jacobian(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            trap_parameters=trap,
        ),
    )


def test_generation_source_signs_and_local_charge_cancellation() -> None:
    mesh = _mesh()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(screening_strength=0.7)
    trap = _trap()
    state = _arbitrary_state(mesh)
    generation = UniformOpticalGeneration(0.037)
    illuminated = assemble_illuminated_trap_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        optical_generation=generation,
    )
    dark = assemble_trap_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
    )
    count = mesh.interior_count
    increment = illuminated - dark
    assert increment[:count] == pytest.approx(0.0)
    assert increment[count : 2 * count] == pytest.approx(
        generation.pair_generation_rate
    )
    assert increment[2 * count : 3 * count] == pytest.approx(
        -generation.pair_generation_rate
    )
    assert increment[3 * count :] == pytest.approx(0.0)
    assert (
        increment[count : 2 * count]
        + increment[2 * count : 3 * count]
        + increment[3 * count :]
    ) == pytest.approx(0.0, abs=2e-15)


def test_uniform_illuminated_generation_recombination_balance_is_exact() -> None:
    mesh = _mesh()
    trap = _trap()
    density = 1.8
    rate = (
        trap.trap_density
        * trap.electron_capture_coefficient
        * 0.5
        * (density - 1.0)
    )
    boundaries = _boundaries(n=density, p=density)
    parameters = BipolarFVParameters(
        screening_strength=0.9,
        fixed_charge_density=trap.trap_density * 0.5,
    )
    residual = assemble_illuminated_trap_residual(
        _uniform_state(mesh, density=density),
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        optical_generation=UniformOpticalGeneration(rate),
    )
    assert np.linalg.norm(residual, ord=np.inf) < 2e-13


def test_exact_uniform_illuminated_state_terminates_without_iteration() -> None:
    mesh = _mesh()
    trap = _trap()
    density = 1.8
    rate = (
        trap.trap_density
        * trap.electron_capture_coefficient
        * 0.5
        * (density - 1.0)
    )
    boundaries = _boundaries(n=density, p=density)
    parameters = BipolarFVParameters(
        screening_strength=0.9,
        fixed_charge_density=trap.trap_density * 0.5,
    )
    result = solve_illuminated_trap_damped_newton(
        _uniform_state(mesh, density=density),
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        optical_generation=UniformOpticalGeneration(rate),
    )
    assert result.converged
    assert result.termination_reason == "initial_residual_converged"
    assert result.iterations == 0


def test_analytical_jacobian_matches_centered_finite_difference() -> None:
    mesh = _mesh(intervals=6)
    boundaries = _boundaries()
    parameters = BipolarFVParameters(
        screening_strength=1.1,
        electron_diffusion_ratio=0.8,
        hole_diffusion_ratio=1.3,
        fixed_charge_density=0.12,
    )
    trap = _trap()
    generation = UniformOpticalGeneration(0.025)
    state = _arbitrary_state(mesh)
    analytical = assemble_illuminated_trap_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        optical_generation=generation,
    )
    numerical = np.empty_like(analytical)
    epsilon = 2e-7
    for column in range(state.size):
        plus = state.copy()
        minus = state.copy()
        plus[column] += epsilon
        minus[column] -= epsilon
        numerical[:, column] = (
            assemble_illuminated_trap_residual(
                plus,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap,
                optical_generation=generation,
            )
            - assemble_illuminated_trap_residual(
                minus,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
                trap_parameters=trap,
                optical_generation=generation,
            )
        ) / (2.0 * epsilon)
    assert analytical == pytest.approx(numerical, rel=3e-7, abs=2e-7)


def test_arbitrary_state_mismatches_match_integrated_residuals() -> None:
    mesh = _mesh()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(screening_strength=0.6)
    trap = _trap()
    generation = UniformOpticalGeneration(0.021)
    state = _arbitrary_state(mesh)
    residual = assemble_illuminated_trap_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        optical_generation=generation,
    )
    metrics = optical_balance_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        optical_generation=generation,
    )
    count = mesh.interior_count
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


def test_contact_extracted_generation_converges_with_constant_total_current() -> None:
    mesh = _mesh(intervals=16)
    trap = _trap()
    boundaries = _boundaries()
    parameters = BipolarFVParameters(
        screening_strength=0.7,
        fixed_charge_density=trap.trap_density * 0.5,
    )
    generation = UniformOpticalGeneration(0.02)
    result = solve_illuminated_trap_damped_newton(
        _uniform_state(mesh),
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        trap_parameters=trap,
        optical_generation=generation,
        options=NewtonOptions(
            maximum_iterations=50,
            absolute_tolerance=2e-10,
            relative_tolerance=1e-10,
        ),
    )
    assert result.converged, result.termination_reason
    assert result.balance.integrated_generation > 0.0
    assert result.balance.electron_relative_mismatch < 2e-9
    assert result.balance.hole_relative_mismatch < 2e-9
    assert result.balance.trap_relative_mismatch < 2e-9
    assert result.balance.total_current_relative_variation < 2e-9


def test_invalid_initial_state_is_rejected() -> None:
    mesh = _mesh()
    with pytest.raises(ValueError):
        solve_illuminated_trap_damped_newton(
            np.zeros(3),
            mesh=mesh,
            boundaries=_boundaries(),
            parameters=BipolarFVParameters(screening_strength=0.5),
            trap_parameters=_trap(),
            optical_generation=UniformOpticalGeneration(0.01),
        )
