from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.finite_volume_prototype import (
    UniformNodeMesh1D,
    UnipolarBoundaryValues,
    UnipolarFVParameters,
    assemble_unipolar_jacobian,
    assemble_unipolar_residual,
    bernoulli_derivative,
    bernoulli_function,
    current_conservation_metrics,
    electron_face_current,
    pack_unipolar_state,
    reconstruct_unipolar_state,
)


@pytest.mark.parametrize("value", [-80.0, -5.0, -1e-7, 0.0, 1e-7, 5.0, 80.0])
def test_bernoulli_identity(value: float) -> None:
    assert bernoulli_function(-value) == pytest.approx(
        bernoulli_function(value) + value,
        rel=2e-13,
        abs=2e-13,
    )


@pytest.mark.parametrize("value", [-10.0, -2.0, -0.1, 0.0, 0.1, 2.0, 10.0])
def test_bernoulli_derivative_matches_centered_difference(value: float) -> None:
    step = 1e-6
    numerical = (
        bernoulli_function(value + step) - bernoulli_function(value - step)
    ) / (2.0 * step)
    assert bernoulli_derivative(value) == pytest.approx(
        numerical,
        rel=2e-8,
        abs=2e-9,
    )


def test_log_density_reconstruction_is_positive() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=4)
    boundaries = UnipolarBoundaryValues(0.0, -1.0, 1.0, 2.0)
    state = pack_unipolar_state(
        potential_interior=[-0.25, -0.5, -0.75],
        log_density_interior=np.log([0.5, 1.0, 3.0]),
    )
    reconstructed = reconstruct_unipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    np.testing.assert_allclose(
        reconstructed.density,
        [1.0, 0.5, 1.0, 3.0, 2.0],
    )
    assert np.all(reconstructed.density > 0.0)


def test_equilibrium_uniform_state_has_zero_residual() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=8)
    boundaries = UnipolarBoundaryValues(0.0, 0.0, 1.0, 1.0)
    parameters = UnipolarFVParameters(screening_strength=25.0)
    state = pack_unipolar_state(
        potential_interior=np.zeros(mesh.interior_count),
        log_density_interior=np.zeros(mesh.interior_count),
    )
    residual = assemble_unipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    np.testing.assert_allclose(residual, 0.0, atol=2e-14)


def test_uniform_resistor_is_exact_and_current_conserving() -> None:
    mesh = UniformNodeMesh1D(length=2.0, intervals=10)
    voltage = 1.7
    boundaries = UnipolarBoundaryValues(0.0, -voltage, 1.0, 1.0)
    parameters = UnipolarFVParameters(
        screening_strength=12.0,
        diffusion_ratio=0.8,
    )
    potential = np.linspace(0.0, -voltage, mesh.node_count)
    state = pack_unipolar_state(
        potential_interior=potential[1:-1],
        log_density_interior=np.zeros(mesh.interior_count),
    )
    residual = assemble_unipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    np.testing.assert_allclose(residual, 0.0, atol=5e-13)
    metrics = current_conservation_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    expected = parameters.diffusion_ratio * voltage / mesh.length
    np.testing.assert_allclose(
        metrics.face_current,
        expected,
        rtol=1e-14,
        atol=1e-14,
    )
    assert metrics.relative_variation < 2e-14


def test_zero_field_face_current_reduces_to_centered_diffusion() -> None:
    potential = np.zeros(4)
    density = np.array([1.0, 1.5, 2.5, 4.0])
    current = electron_face_current(
        potential,
        density,
        spacing=0.25,
        diffusion_ratio=1.3,
    )
    expected = 1.3 * np.diff(density) / 0.25
    np.testing.assert_allclose(current, expected, rtol=2e-15, atol=0.0)


def test_analytical_jacobian_matches_finite_difference() -> None:
    mesh = UniformNodeMesh1D(length=1.3, intervals=6)
    boundaries = UnipolarBoundaryValues(
        potential_left=0.15,
        potential_right=-0.8,
        density_left=1.2,
        density_right=0.7,
    )
    parameters = UnipolarFVParameters(
        screening_strength=9.0,
        diffusion_ratio=0.65,
        background_density=0.9,
    )
    state = pack_unipolar_state(
        potential_interior=[0.02, -0.11, -0.30, -0.47, -0.63],
        log_density_interior=np.log([1.1, 0.95, 0.82, 0.76, 0.72]),
    )
    analytical = assemble_unipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    numerical = np.empty_like(analytical)
    step = 2e-7
    for column in range(state.size):
        perturbation = np.zeros_like(state)
        perturbation[column] = step
        plus = assemble_unipolar_residual(
            state + perturbation,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
        minus = assemble_unipolar_residual(
            state - perturbation,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        )
        numerical[:, column] = (plus - minus) / (2.0 * step)
    np.testing.assert_allclose(
        analytical,
        numerical,
        rtol=3e-8,
        atol=2e-8,
    )


def test_continuity_residual_telescopes_to_terminal_current_difference() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=5)
    boundaries = UnipolarBoundaryValues(0.0, -0.6, 1.0, 1.4)
    parameters = UnipolarFVParameters(screening_strength=3.0)
    state = pack_unipolar_state(
        potential_interior=[-0.05, -0.17, -0.34, -0.51],
        log_density_interior=np.log([1.08, 1.16, 1.24, 1.32]),
    )
    residual = assemble_unipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    reconstructed = reconstruct_unipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    current = electron_face_current(
        reconstructed.potential,
        reconstructed.density,
        spacing=mesh.spacing,
    )
    continuity = residual[mesh.interior_count :]
    assert np.sum(continuity) * mesh.spacing == pytest.approx(
        current[-1] - current[0],
        rel=2e-14,
        abs=2e-14,
    )


@pytest.mark.parametrize(
    "constructor,args",
    [
        (UniformNodeMesh1D, {"length": 0.0, "intervals": 4}),
        (UniformNodeMesh1D, {"length": 1.0, "intervals": 1}),
        (
            UnipolarBoundaryValues,
            {
                "potential_left": 0.0,
                "potential_right": 0.0,
                "density_left": 0.0,
                "density_right": 1.0,
            },
        ),
        (UnipolarFVParameters, {"screening_strength": -1.0}),
    ],
)
def test_invalid_configuration_is_rejected(constructor, args) -> None:
    with pytest.raises(ValueError):
        constructor(**args)
