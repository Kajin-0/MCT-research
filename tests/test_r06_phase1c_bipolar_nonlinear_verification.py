from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.bipolar_nonlinear_verification import (
    BipolarForcing,
    ManufacturedBipolarSolutionSpec,
    assemble_forced_bipolar_residual,
    bipolar_continuity_balance,
    bipolar_jacobian_as_coo,
    continue_bipolar_right_contact_potential,
    manufactured_bipolar_case,
    manufactured_bipolar_refinement_study,
    solve_bipolar_damped_newton,
)
from mct_research.transport_noise.bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarFVParameters,
    assemble_bipolar_jacobian,
    linear_bipolar_reservoir_state,
    reconstruct_bipolar_state,
)
from mct_research.transport_noise.finite_volume_prototype import UniformNodeMesh1D
from mct_research.transport_noise.nonlinear_verification import NewtonOptions


def _basic_case(intervals: int = 20):
    mesh = UniformNodeMesh1D(length=1.0, intervals=intervals)
    boundaries = BipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.0,
        electron_density_left=1.0,
        electron_density_right=1.0,
        hole_density_left=1.0,
        hole_density_right=1.0,
    )
    parameters = BipolarFVParameters(
        screening_strength=5.0,
        electron_diffusion_ratio=1.0,
        hole_diffusion_ratio=0.8,
        fixed_charge_density=0.0,
    )
    state = linear_bipolar_reservoir_state(
        mesh=mesh,
        boundaries=boundaries,
    )
    return mesh, boundaries, parameters, state


def test_forcing_vector_and_validation():
    forcing = BipolarForcing(
        poisson=np.ones(3),
        electron_continuity=2.0 * np.ones(3),
        hole_continuity=3.0 * np.ones(3),
    )
    assert np.array_equal(
        forcing.vector(3),
        np.array([1, 1, 1, 2, 2, 2, 3, 3, 3]),
    )
    with pytest.raises(ValueError):
        forcing.vector(2)
    invalid = BipolarForcing(
        poisson=np.array([np.nan]),
        electron_continuity=np.zeros(1),
        hole_continuity=np.zeros(1),
    )
    with pytest.raises(ValueError):
        invalid.vector(1)


def test_exact_equilibrium_terminates_without_iterations():
    mesh, boundaries, parameters, state = _basic_case()
    result = solve_bipolar_damped_newton(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    assert result.converged
    assert result.termination_reason == "initial_residual_converged"
    assert result.iterations == 0
    assert result.final_residual_inf_norm == 0.0


def test_perturbed_equilibrium_converges():
    mesh, boundaries, parameters, state = _basic_case()
    perturbed = state + 0.15 * np.random.default_rng(9).standard_normal(state.shape)
    result = solve_bipolar_damped_newton(
        perturbed,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    assert result.converged
    assert result.final_residual_inf_norm <= result.target_residual_inf_norm
    assert result.continuity_balance.electron_relative_mismatch < 1.0e-10
    assert result.continuity_balance.hole_relative_mismatch < 1.0e-10


def test_difficult_state_uses_damping_and_converges():
    mesh, boundaries, parameters, state = _basic_case()
    difficult = state + 0.5 * np.random.default_rng(3).standard_normal(state.shape)
    result = solve_bipolar_damped_newton(
        difficult,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        options=NewtonOptions(
            absolute_tolerance=1.0e-10,
            relative_tolerance=1.0e-12,
        ),
    )
    assert result.converged
    assert any(record.accepted_damping < 1.0 for record in result.history)
    assert all(
        record.residual_inf_norm_after < record.residual_inf_norm_before
        for record in result.history
    )


def test_disabled_backtracking_reports_controlled_failure():
    mesh, boundaries, parameters, state = _basic_case()
    difficult = state + 0.5 * np.random.default_rng(0).standard_normal(state.shape)
    result = solve_bipolar_damped_newton(
        difficult,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
        options=NewtonOptions(
            maximum_backtracks=0,
            minimum_damping=1.0,
            armijo_fraction=0.9,
        ),
    )
    assert not result.converged
    assert result.termination_reason == "line_search_failed"
    assert np.all(np.isfinite(result.state))


def test_voltage_continuation_recovers_neutral_bipolar_resistor():
    mesh, boundaries, parameters, state = _basic_case()
    continuation = continue_bipolar_right_contact_potential(
        state,
        mesh=mesh,
        initial_boundaries=boundaries,
        target_potential_right=0.8,
        steps=4,
        parameters=parameters,
    )
    assert continuation.completed
    assert len(continuation.steps) == 4
    final = continuation.steps[-1].result
    final_boundaries = BipolarBoundaryValues(
        potential_left=0.0,
        potential_right=0.8,
        electron_density_left=1.0,
        electron_density_right=1.0,
        hole_density_left=1.0,
        hole_density_right=1.0,
    )
    reconstructed = reconstruct_bipolar_state(
        final.state,
        mesh=mesh,
        boundaries=final_boundaries,
    )
    assert np.allclose(
        reconstructed.potential,
        np.linspace(0.0, 0.8, mesh.node_count),
        atol=1.0e-12,
    )
    assert np.allclose(reconstructed.electron_density, 1.0, atol=1.0e-12)
    assert np.allclose(reconstructed.hole_density, 1.0, atol=1.0e-12)
    assert final.current_conservation.electron.relative_variation < 1.0e-12
    assert final.current_conservation.hole.relative_variation < 1.0e-12


def test_source_free_balance_telescopes_exactly():
    mesh, boundaries, parameters, state = _basic_case()
    state = state + 0.1 * np.random.default_rng(5).standard_normal(state.shape)
    balance = bipolar_continuity_balance(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    residual = assemble_forced_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    count = mesh.interior_count
    assert np.isclose(
        balance.electron_terminal_difference,
        mesh.spacing * np.sum(residual[count : 2 * count]),
    )
    assert np.isclose(
        balance.hole_terminal_difference,
        mesh.spacing * np.sum(residual[2 * count :]),
    )


def test_continuous_manufactured_residual_decreases_by_four():
    parameters = BipolarFVParameters(
        screening_strength=2.0,
        electron_diffusion_ratio=1.0,
        hole_diffusion_ratio=0.7,
        fixed_charge_density=0.1,
    )
    errors = []
    for intervals in (16, 32, 64):
        mesh = UniformNodeMesh1D(length=1.0, intervals=intervals)
        case = manufactured_bipolar_case(mesh=mesh, parameters=parameters)
        residual = assemble_forced_bipolar_residual(
            case.exact_state,
            mesh=mesh,
            boundaries=case.boundaries,
            parameters=parameters,
            forcing=case.forcing,
        )
        errors.append(float(np.linalg.norm(residual, ord=np.inf)))
    assert errors[0] / errors[1] > 3.9
    assert errors[1] / errors[2] > 3.9


def test_manufactured_refinement_is_second_order_for_all_fields():
    parameters = BipolarFVParameters(
        screening_strength=2.0,
        electron_diffusion_ratio=1.0,
        hole_diffusion_ratio=0.7,
        fixed_charge_density=0.1,
    )
    study = manufactured_bipolar_refinement_study(
        (16, 32, 64),
        length=1.0,
        parameters=parameters,
    )
    assert min(study.potential_linf_orders) > 1.95
    assert min(study.electron_linf_orders) > 1.95
    assert min(study.hole_linf_orders) > 1.95
    assert max(
        record.electron_balance_relative_mismatch for record in study.records
    ) < 1.0e-11
    assert max(
        record.hole_balance_relative_mismatch for record in study.records
    ) < 1.0e-11


def test_forced_solve_satisfies_terminal_volume_balance():
    mesh = UniformNodeMesh1D(length=1.0, intervals=32)
    parameters = BipolarFVParameters(
        screening_strength=2.0,
        electron_diffusion_ratio=1.0,
        hole_diffusion_ratio=0.7,
        fixed_charge_density=0.1,
    )
    case = manufactured_bipolar_case(mesh=mesh, parameters=parameters)
    initial = linear_bipolar_reservoir_state(
        mesh=mesh,
        boundaries=case.boundaries,
    )
    result = solve_bipolar_damped_newton(
        initial,
        mesh=mesh,
        boundaries=case.boundaries,
        parameters=parameters,
        forcing=case.forcing,
    )
    assert result.converged
    assert result.continuity_balance.electron_relative_mismatch < 1.0e-11
    assert result.continuity_balance.hole_relative_mismatch < 1.0e-11


def test_bipolar_coo_round_trip_equals_dense_jacobian():
    mesh = UniformNodeMesh1D(length=1.0, intervals=12)
    parameters = BipolarFVParameters(
        screening_strength=2.0,
        electron_diffusion_ratio=1.0,
        hole_diffusion_ratio=0.7,
        fixed_charge_density=0.1,
    )
    case = manufactured_bipolar_case(mesh=mesh, parameters=parameters)
    dense = assemble_bipolar_jacobian(
        case.exact_state,
        mesh=mesh,
        boundaries=case.boundaries,
        parameters=parameters,
    )
    coo = bipolar_jacobian_as_coo(
        case.exact_state,
        mesh=mesh,
        boundaries=case.boundaries,
        parameters=parameters,
    )
    assert np.array_equal(coo.to_dense(), dense)


def test_invalid_solver_and_continuation_inputs_are_rejected():
    mesh, boundaries, parameters, state = _basic_case()
    with pytest.raises(ValueError):
        solve_bipolar_damped_newton(
            state[:-1],
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
    with pytest.raises(ValueError):
        continue_bipolar_right_contact_potential(
            state,
            mesh=mesh,
            initial_boundaries=boundaries,
            target_potential_right=1.0,
            steps=0,
            parameters=parameters,
        )


def test_invalid_manufactured_specification_is_rejected():
    with pytest.raises(ValueError):
        ManufacturedBipolarSolutionSpec(electron_boundary_density=0.0)
    with pytest.raises(ValueError):
        ManufacturedBipolarSolutionSpec(hole_boundary_density=float("nan"))


def test_refinement_requires_increasing_three_level_sequence():
    parameters = BipolarFVParameters(screening_strength=2.0)
    with pytest.raises(ValueError):
        manufactured_bipolar_refinement_study(
            (16, 32),
            length=1.0,
            parameters=parameters,
        )
    with pytest.raises(ValueError):
        manufactured_bipolar_refinement_study(
            (16, 16, 32),
            length=1.0,
            parameters=parameters,
        )
