import numpy as np
import pytest

from mct_research.transport_noise.bipolar_contact_control_prototype import (
    BipolarFiniteContactBoundaryValues,
    BipolarFiniteContactFVParameters,
    assemble_bipolar_finite_contact_jacobian,
    assemble_bipolar_finite_contact_residual,
    bipolar_contact_balance_metrics,
    exact_zero_field_bipolar_contact_currents,
    exact_zero_field_bipolar_contact_state,
    pack_bipolar_finite_contact_state,
    reconstruct_bipolar_finite_contact_state,
    solve_bipolar_finite_contact_damped_newton,
)
from mct_research.transport_noise.contact_control_prototype import FiniteExchangeContact
from mct_research.transport_noise.finite_volume_prototype import UniformNodeMesh1D


def make_case(
    *,
    electron_left_biot=0.8,
    electron_right_biot=5.0,
    hole_left_biot=2.0,
    hole_right_biot=0.6,
    electron_left_density=1.0,
    electron_right_density=1.4,
    hole_left_density=1.5,
    hole_right_density=0.8,
    screening=0.0,
    fixed_charge=0.0,
    potential_left=0.0,
    potential_right=0.0,
    electron_diffusion=1.3,
    hole_diffusion=0.7,
):
    mesh = UniformNodeMesh1D(1.0, 12)
    boundaries = BipolarFiniteContactBoundaryValues(
        potential_left,
        potential_right,
        FiniteExchangeContact(electron_left_density, electron_left_biot),
        FiniteExchangeContact(electron_right_density, electron_right_biot),
        FiniteExchangeContact(hole_left_density, hole_left_biot),
        FiniteExchangeContact(hole_right_density, hole_right_biot),
    )
    parameters = BipolarFiniteContactFVParameters(
        screening,
        electron_diffusion,
        hole_diffusion,
        fixed_charge,
    )
    return mesh, boundaries, parameters


def test_exact_zero_field_state_and_independent_balances():
    mesh, boundaries, parameters = make_case()
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    residual = assemble_bipolar_finite_contact_residual(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(residual, np.inf) < 1.0e-11
    electron_current, hole_current = exact_zero_field_bipolar_contact_currents(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    metrics = bipolar_contact_balance_metrics(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.allclose(metrics.electron.face_current, electron_current)
    assert np.allclose(metrics.hole.face_current, hole_current)
    assert abs(metrics.electron.left_boundary_mismatch) < 1.0e-12
    assert abs(metrics.electron.right_boundary_mismatch) < 1.0e-12
    assert abs(metrics.hole.left_boundary_mismatch) < 1.0e-12
    assert abs(metrics.hole.right_boundary_mismatch) < 1.0e-12
    assert metrics.total_current_relative_variation < 1.0e-12


def test_hole_contact_signs_are_opposite_electron_signs():
    mesh, boundaries, parameters = make_case()
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    reconstructed = reconstruct_bipolar_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    electron_current, hole_current = exact_zero_field_bipolar_contact_currents(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert electron_current > 0.0
    assert reconstructed.electron_density[0] > boundaries.electron_left.equilibrium_density
    assert reconstructed.electron_density[-1] < boundaries.electron_right.equilibrium_density
    assert hole_current > 0.0
    assert reconstructed.hole_density[0] < boundaries.hole_left.equilibrium_density
    assert reconstructed.hole_density[-1] > boundaries.hole_right.equilibrium_density


def test_neutral_equilibrium_with_screening():
    mesh, boundaries, parameters = make_case(
        electron_left_density=1.2,
        electron_right_density=1.2,
        hole_left_density=0.9,
        hole_right_density=0.9,
        screening=1.7,
        fixed_charge=0.3,
    )
    potential = np.zeros(mesh.node_count)
    state = pack_bipolar_finite_contact_state(
        potential[1:-1],
        np.log(np.full(mesh.node_count, 1.2)),
        np.log(np.full(mesh.node_count, 0.9)),
    )
    residual = assemble_bipolar_finite_contact_residual(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(residual, np.inf) < 1.0e-12


def test_fast_reservoir_limit_recovers_contact_equilibrium_densities():
    mesh, boundaries, parameters = make_case(
        electron_left_biot=1.0e9,
        electron_right_biot=1.0e9,
        hole_left_biot=1.0e9,
        hole_right_biot=1.0e9,
    )
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    reconstructed = reconstruct_bipolar_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    assert np.isclose(
        reconstructed.electron_density[0],
        boundaries.electron_left.equilibrium_density,
        rtol=1.0e-9,
    )
    assert np.isclose(
        reconstructed.electron_density[-1],
        boundaries.electron_right.equilibrium_density,
        rtol=1.0e-9,
    )
    assert np.isclose(
        reconstructed.hole_density[0],
        boundaries.hole_left.equilibrium_density,
        rtol=1.0e-9,
    )
    assert np.isclose(
        reconstructed.hole_density[-1],
        boundaries.hole_right.equilibrium_density,
        rtol=1.0e-9,
    )


def test_selective_electron_blocking_leaves_hole_current():
    mesh, boundaries, parameters = make_case(
        electron_left_biot=0.0,
        electron_right_biot=3.0,
    )
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    electron_current, hole_current = exact_zero_field_bipolar_contact_currents(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    residual = assemble_bipolar_finite_contact_residual(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(residual, np.inf) < 1.0e-11
    assert electron_current == 0.0
    assert hole_current != 0.0


def test_selective_hole_blocking_leaves_electron_current():
    mesh, boundaries, parameters = make_case(
        hole_left_biot=4.0,
        hole_right_biot=0.0,
    )
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    electron_current, hole_current = exact_zero_field_bipolar_contact_currents(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    residual = assemble_bipolar_finite_contact_residual(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.norm(residual, np.inf) < 1.0e-11
    assert electron_current != 0.0
    assert hole_current == 0.0


def test_two_species_blocking_exposes_two_population_null_modes():
    mesh, boundaries, parameters = make_case(
        electron_left_biot=0.0,
        electron_right_biot=0.0,
        hole_left_biot=0.0,
        hole_right_biot=0.0,
    )
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    jacobian = assemble_bipolar_finite_contact_jacobian(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.linalg.matrix_rank(jacobian) == jacobian.shape[0] - 2


def test_electron_hole_symmetry_with_reflected_contacts():
    mesh, boundaries, parameters = make_case(
        electron_left_biot=2.0,
        electron_right_biot=3.0,
        hole_left_biot=3.0,
        hole_right_biot=2.0,
        electron_left_density=1.0,
        electron_right_density=1.4,
        hole_left_density=1.4,
        hole_right_density=1.0,
        electron_diffusion=1.0,
        hole_diffusion=1.0,
    )
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    reconstructed = reconstruct_bipolar_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    electron_current, hole_current = exact_zero_field_bipolar_contact_currents(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.isclose(electron_current, hole_current)
    assert np.allclose(
        reconstructed.electron_density,
        reconstructed.hole_density[::-1],
    )


def test_jacobian_matches_centered_finite_difference():
    mesh, boundaries, parameters = make_case(
        electron_left_biot=0.7,
        electron_right_biot=4.0,
        hole_left_biot=1.3,
        hole_right_biot=0.5,
        electron_right_density=0.9,
        hole_left_density=1.2,
        screening=0.4,
        fixed_charge=0.1,
        potential_left=0.1,
        potential_right=-0.2,
    )
    rng = np.random.default_rng(9)
    state = np.concatenate(
        [
            np.linspace(0.08, -0.18, mesh.interior_count)
            + 0.01 * rng.normal(size=mesh.interior_count),
            np.log(1.0 + 0.05 * rng.normal(size=mesh.node_count)),
            np.log(1.0 + 0.05 * rng.normal(size=mesh.node_count)),
        ]
    )
    analytical = assemble_bipolar_finite_contact_jacobian(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    epsilon = 2.0e-7
    finite_difference = np.empty_like(analytical)
    for column in range(state.size):
        perturbation = np.zeros_like(state)
        perturbation[column] = epsilon
        plus = assemble_bipolar_finite_contact_residual(
            state + perturbation,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
        minus = assemble_bipolar_finite_contact_residual(
            state - perturbation,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
        finite_difference[:, column] = (plus - minus) / (2.0 * epsilon)
    assert np.allclose(analytical, finite_difference, rtol=3.0e-6, atol=3.0e-7)


def test_damped_newton_recovers_exact_state():
    mesh, boundaries, parameters = make_case()
    exact = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    initial = exact.copy()
    count = mesh.interior_count
    nodes = mesh.node_count
    initial[:count] += 0.03 * np.sin(np.pi * mesh.nodes[1:-1])
    initial[count : count + nodes] += 0.08 * np.cos(np.pi * mesh.nodes)
    initial[count + nodes :] -= 0.07 * np.sin(np.pi * mesh.nodes)
    result = solve_bipolar_finite_contact_damped_newton(
        initial, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert result.converged, result.termination_reason
    assert result.final_residual_inf_norm < 1.0e-10
    assert np.max(np.abs(result.state - exact)) < 1.0e-8


def test_total_current_is_sum_of_carrier_currents():
    mesh, boundaries, parameters = make_case()
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    metrics = bipolar_contact_balance_metrics(
        state, mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    assert np.allclose(
        metrics.total_face_current,
        metrics.electron.face_current + metrics.hole.face_current,
    )


def test_positive_reconstructed_carriers():
    mesh, boundaries, parameters = make_case()
    state = exact_zero_field_bipolar_contact_state(
        mesh=mesh, boundaries=boundaries, parameters=parameters
    )
    reconstructed = reconstruct_bipolar_finite_contact_state(
        state, mesh=mesh, boundaries=boundaries
    )
    assert np.all(reconstructed.electron_density > 0.0)
    assert np.all(reconstructed.hole_density > 0.0)


def test_invalid_parameter_domain():
    with pytest.raises(ValueError):
        BipolarFiniteContactFVParameters(0.0, 0.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        BipolarFiniteContactFVParameters(0.0, 1.0, -1.0, 0.0)


def test_exact_state_rejects_screening_and_field():
    mesh, boundaries, parameters = make_case(screening=0.1)
    with pytest.raises(ValueError):
        exact_zero_field_bipolar_contact_state(
            mesh=mesh, boundaries=boundaries, parameters=parameters
        )
    mesh, boundaries, parameters = make_case(potential_right=0.2)
    with pytest.raises(ValueError):
        exact_zero_field_bipolar_contact_currents(
            mesh=mesh, boundaries=boundaries, parameters=parameters
        )
