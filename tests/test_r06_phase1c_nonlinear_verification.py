from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.finite_volume_prototype import (
    UniformNodeMesh1D,
    UnipolarBoundaryValues,
    UnipolarFVParameters,
    assemble_unipolar_jacobian,
    assemble_unipolar_residual,
    electron_face_current,
    reconstruct_unipolar_state,
)
from mct_research.transport_noise.nonlinear_verification import (
    ManufacturedSolutionSpec,
    NewtonOptions,
    UnipolarForcing,
    assemble_forced_unipolar_residual,
    continue_right_contact_potential,
    jacobian_as_coo,
    linear_reservoir_state,
    manufactured_refinement_study,
    manufactured_unipolar_case,
    solve_unipolar_damped_newton,
)


def test_exact_equilibrium_converges_without_iteration() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=24)
    boundaries = UnipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.0,
        density_left=1.0,
        density_right=1.0,
    )
    parameters = UnipolarFVParameters(
        screening_strength=6.0,
        diffusion_ratio=1.0,
        background_density=1.0,
    )
    initial = linear_reservoir_state(mesh=mesh, boundaries=boundaries)
    result = solve_unipolar_damped_newton(
        initial,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    assert result.converged
    assert result.termination_reason == "initial_residual_converged"
    assert result.iterations == 0
    assert result.final_residual_inf_norm < 1.0e-13


def test_perturbed_equilibrium_is_recovered() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=32)
    boundaries = UnipolarBoundaryValues(0.0, 0.0, 1.0, 1.0)
    parameters = UnipolarFVParameters(5.0, 1.0, 1.0)
    x = mesh.nodes[1:-1]
    initial = np.concatenate(
        [
            0.10 * np.sin(np.pi * x),
            np.log(1.0 + 0.05 * np.sin(2.0 * np.pi * x)),
        ]
    )
    result = solve_unipolar_damped_newton(
        initial,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    assert result.converged
    assert result.iterations <= 6
    assert result.final_residual_inf_norm <= result.target_residual_inf_norm
    np.testing.assert_allclose(result.state, 0.0, atol=3.0e-13)


def test_difficult_initial_guess_uses_backtracking_and_converges() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=32)
    boundaries = UnipolarBoundaryValues(0.0, 2.0, 1.0, 1.0)
    parameters = UnipolarFVParameters(20.0, 1.0, 1.0)
    x = mesh.nodes[1:-1]
    initial = np.concatenate(
        [
            2.0 * x + np.sin(3.0 * np.pi * x),
            np.sin(2.0 * np.pi * x),
        ]
    )
    result = solve_unipolar_damped_newton(
        initial,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    assert result.converged
    assert min(record.accepted_damping for record in result.history) < 1.0
    assert result.current_conservation.relative_variation < 1.0e-11


def test_line_search_failure_is_reported_without_nonfinite_state() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=32)
    boundaries = UnipolarBoundaryValues(0.0, 2.0, 1.0, 1.0)
    parameters = UnipolarFVParameters(20.0, 1.0, 1.0)
    x = mesh.nodes[1:-1]
    initial = np.concatenate(
        [
            2.0 * x + np.sin(3.0 * np.pi * x),
            np.sin(2.0 * np.pi * x),
        ]
    )
    result = solve_unipolar_damped_newton(
        initial,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        options=NewtonOptions(maximum_backtracks=0),
    )
    assert not result.converged
    assert result.termination_reason == "line_search_failed"
    assert np.all(np.isfinite(result.state))


def test_voltage_continuation_recovers_exact_uniform_resistor() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=32)
    initial_boundaries = UnipolarBoundaryValues(0.0, 0.0, 1.0, 1.0)
    parameters = UnipolarFVParameters(8.0, 1.0, 1.0)
    initial = linear_reservoir_state(
        mesh=mesh,
        boundaries=initial_boundaries,
    )
    continuation = continue_right_contact_potential(
        initial,
        mesh=mesh,
        initial_boundaries=initial_boundaries,
        target_potential_right=4.0,
        steps=8,
        parameters=parameters,
    )
    assert continuation.completed
    assert len(continuation.steps) == 8
    final_boundaries = UnipolarBoundaryValues(0.0, 4.0, 1.0, 1.0)
    reconstructed = reconstruct_unipolar_state(
        continuation.final_state,
        mesh=mesh,
        boundaries=final_boundaries,
    )
    np.testing.assert_allclose(
        reconstructed.potential,
        4.0 * mesh.nodes,
        atol=2.0e-14,
    )
    np.testing.assert_allclose(reconstructed.density, 1.0, atol=2.0e-14)
    current = electron_face_current(
        reconstructed.potential,
        reconstructed.density,
        spacing=mesh.spacing,
        diffusion_ratio=parameters.diffusion_ratio,
    )
    np.testing.assert_allclose(current, -4.0, atol=3.0e-13)


def test_manufactured_forcing_has_expected_shape_and_is_finite() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=20)
    parameters = UnipolarFVParameters(4.0, 1.0, 1.0)
    case = manufactured_unipolar_case(
        mesh=mesh,
        parameters=parameters,
    )
    vector = case.forcing.vector(mesh.interior_count)
    assert vector.shape == (2 * mesh.interior_count,)
    assert np.all(np.isfinite(vector))
    residual = assemble_forced_unipolar_residual(
        case.exact_state,
        mesh=mesh,
        boundaries=case.boundaries,
        parameters=parameters,
        forcing=case.forcing,
    )
    assert np.linalg.norm(residual, ord=np.inf) < 0.05


def test_manufactured_refinement_is_second_order() -> None:
    study = manufactured_refinement_study(
        (16, 32, 64),
        parameters=UnipolarFVParameters(4.0, 1.0, 1.0),
        specification=ManufacturedSolutionSpec(),
    )
    assert all(record.iterations <= 6 for record in study.records)
    assert min(study.potential_linf_orders) > 1.95
    assert min(study.density_linf_orders) > 1.95
    assert study.records[-1].potential_linf_error < 1.1e-5
    assert study.records[-1].density_linf_error < 3.7e-5


def test_coo_round_trip_matches_dense_jacobian_exactly() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=12)
    boundaries = UnipolarBoundaryValues(0.0, 0.7, 1.0, 1.2)
    parameters = UnipolarFVParameters(3.0, 0.8, 1.0)
    initial = linear_reservoir_state(mesh=mesh, boundaries=boundaries)
    dense = assemble_unipolar_jacobian(
        initial,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    coordinate = jacobian_as_coo(
        initial,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    np.testing.assert_array_equal(coordinate.to_dense(), dense)
    assert coordinate.data.size < dense.size


@pytest.mark.parametrize(
    "options",
    [
        {"maximum_iterations": 0},
        {"maximum_backtracks": -1},
        {"absolute_tolerance": 0.0},
        {"relative_tolerance": -1.0},
        {"backtrack_factor": 1.0},
        {"minimum_damping": 2.0},
    ],
)
def test_invalid_newton_options_are_rejected(
    options: dict[str, float],
) -> None:
    with pytest.raises(ValueError):
        NewtonOptions(**options)


def test_forcing_shape_mismatch_is_rejected() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=8)
    boundaries = UnipolarBoundaryValues(0.0, 0.0, 1.0, 1.0)
    parameters = UnipolarFVParameters(1.0, 1.0, 1.0)
    state = linear_reservoir_state(mesh=mesh, boundaries=boundaries)
    forcing = UnipolarForcing(
        poisson=np.zeros(mesh.interior_count - 1),
        continuity=np.zeros(mesh.interior_count),
    )
    with pytest.raises(ValueError):
        assemble_forced_unipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
            forcing=forcing,
        )


def test_unforced_wrapper_matches_base_residual() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=10)
    boundaries = UnipolarBoundaryValues(0.0, 0.5, 1.0, 1.0)
    parameters = UnipolarFVParameters(2.0, 1.0, 1.0)
    state = linear_reservoir_state(mesh=mesh, boundaries=boundaries)
    np.testing.assert_array_equal(
        assemble_forced_unipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        ),
        assemble_unipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        ),
    )
