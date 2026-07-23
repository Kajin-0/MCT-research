from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.bipolar_prototype import (
    BipolarBoundaryValues,
    BipolarFVParameters,
    assemble_bipolar_jacobian,
    assemble_bipolar_residual,
    bipolar_current_conservation_metrics,
    hole_face_current,
    linear_bipolar_reservoir_state,
    pack_bipolar_state,
    reconstruct_bipolar_state,
)
from mct_research.transport_noise.finite_volume_prototype import (
    UniformNodeMesh1D,
    UnipolarBoundaryValues,
    UnipolarFVParameters,
    assemble_unipolar_residual,
    electron_face_current,
)


def _constant_bipolar_state(
    mesh: UniformNodeMesh1D,
    *,
    potential_left: float = 0.0,
    potential_right: float = 0.0,
    electron_density: float = 1.4,
    hole_density: float = 0.4,
) -> np.ndarray:
    fraction = mesh.nodes / mesh.length
    potential = potential_left + fraction * (potential_right - potential_left)
    return pack_bipolar_state(
        potential[1:-1],
        np.full(mesh.interior_count, np.log(electron_density)),
        np.full(mesh.interior_count, np.log(hole_density)),
    )


def test_uniform_neutral_equilibrium_has_zero_residual_and_current() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=16)
    boundaries = BipolarBoundaryValues(0.0, 0.0, 1.4, 1.4, 0.4, 0.4)
    parameters = BipolarFVParameters(
        screening_strength=3.0,
        electron_diffusion_ratio=1.2,
        hole_diffusion_ratio=0.7,
        fixed_charge_density=1.0,
    )
    state = _constant_bipolar_state(mesh)

    np.testing.assert_allclose(
        assemble_bipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        ),
        0.0,
        atol=2.0e-13,
    )
    metrics = bipolar_current_conservation_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    np.testing.assert_allclose(metrics.electron.face_current, 0.0, atol=1.0e-14)
    np.testing.assert_allclose(metrics.hole.face_current, 0.0, atol=1.0e-14)


def test_biased_neutral_resistor_is_exact_for_both_carriers() -> None:
    mesh = UniformNodeMesh1D(length=2.0, intervals=20)
    boundaries = BipolarBoundaryValues(-0.2, 0.6, 1.4, 1.4, 0.4, 0.4)
    parameters = BipolarFVParameters(
        screening_strength=5.0,
        electron_diffusion_ratio=1.3,
        hole_diffusion_ratio=0.6,
        fixed_charge_density=1.0,
    )
    state = _constant_bipolar_state(
        mesh,
        potential_left=-0.2,
        potential_right=0.6,
    )

    np.testing.assert_allclose(
        assemble_bipolar_residual(
            state,
            mesh=mesh,
            boundaries=boundaries,
            parameters=parameters,
        ),
        0.0,
        atol=2.0e-12,
    )
    metrics = bipolar_current_conservation_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    delta_potential = 0.8
    assert np.mean(metrics.electron.face_current) == pytest.approx(
        -1.3 * 1.4 * delta_potential / mesh.length,
        rel=2.0e-14,
    )
    assert np.mean(metrics.hole.face_current) == pytest.approx(
        -0.6 * 0.4 * delta_potential / mesh.length,
        rel=2.0e-14,
    )
    assert metrics.electron.relative_variation < 1.0e-13
    assert metrics.hole.relative_variation < 1.0e-13


def test_zero_field_diffusion_signs_are_opposite() -> None:
    potential = np.zeros(11)
    density = np.linspace(1.0, 2.0, 11)
    electron = electron_face_current(
        potential,
        density,
        spacing=0.1,
        diffusion_ratio=1.7,
    )
    hole = hole_face_current(
        potential,
        density,
        spacing=0.1,
        diffusion_ratio=0.8,
    )
    np.testing.assert_allclose(electron, 1.7)
    np.testing.assert_allclose(hole, -0.8)


def test_both_continuity_blocks_telescope_to_terminal_current_difference() -> None:
    rng = np.random.default_rng(12)
    mesh = UniformNodeMesh1D(length=1.3, intervals=9)
    boundaries = BipolarBoundaryValues(-0.1, 0.4, 1.1, 1.6, 0.8, 0.5)
    parameters = BipolarFVParameters(2.2, 1.4, 0.9, 0.2)
    state = pack_bipolar_state(
        rng.normal(scale=0.2, size=mesh.interior_count),
        rng.normal(scale=0.15, size=mesh.interior_count),
        rng.normal(scale=0.12, size=mesh.interior_count),
    )

    residual = assemble_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    count = mesh.interior_count
    metrics = bipolar_current_conservation_metrics(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    assert mesh.spacing * np.sum(residual[count : 2 * count]) == pytest.approx(
        metrics.electron.face_current[-1] - metrics.electron.face_current[0],
        abs=2.0e-13,
    )
    assert mesh.spacing * np.sum(residual[2 * count :]) == pytest.approx(
        metrics.hole.face_current[-1] - metrics.hole.face_current[0],
        abs=2.0e-13,
    )


def test_analytical_bipolar_jacobian_matches_centered_difference() -> None:
    rng = np.random.default_rng(4)
    mesh = UniformNodeMesh1D(length=1.0, intervals=7)
    boundaries = BipolarBoundaryValues(-0.2, 0.3, 1.3, 0.9, 0.6, 1.1)
    parameters = BipolarFVParameters(1.7, 1.2, 0.8, -0.15)
    state = pack_bipolar_state(
        rng.normal(scale=0.15, size=mesh.interior_count),
        rng.normal(scale=0.1, size=mesh.interior_count),
        rng.normal(scale=0.1, size=mesh.interior_count),
    )

    analytical = assemble_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    step = 2.0e-6
    numerical = np.empty_like(analytical)
    for column in range(state.size):
        perturbation = np.zeros_like(state)
        perturbation[column] = step
        numerical[:, column] = (
            assemble_bipolar_residual(
                state + perturbation,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
            )
            - assemble_bipolar_residual(
                state - perturbation,
                mesh=mesh,
                boundaries=boundaries,
                parameters=parameters,
            )
        ) / (2.0 * step)
    np.testing.assert_allclose(analytical, numerical, rtol=2.0e-8, atol=2.0e-8)


def test_jacobian_has_no_direct_cross_carrier_continuity_coupling() -> None:
    mesh = UniformNodeMesh1D(length=1.0, intervals=6)
    boundaries = BipolarBoundaryValues(-0.1, 0.2, 1.2, 1.1, 0.7, 0.9)
    parameters = BipolarFVParameters(2.0, 1.3, 0.8, 0.25)
    state = linear_bipolar_reservoir_state(mesh=mesh, boundaries=boundaries)
    jacobian = assemble_bipolar_jacobian(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )
    count = mesh.interior_count
    np.testing.assert_allclose(jacobian[count : 2 * count, 2 * count :], 0.0)
    np.testing.assert_allclose(jacobian[2 * count :, count : 2 * count], 0.0)


def test_electron_hole_symmetry_transforms_residual_blocks() -> None:
    rng = np.random.default_rng(8)
    mesh = UniformNodeMesh1D(length=1.0, intervals=8)
    count = mesh.interior_count
    boundaries = BipolarBoundaryValues(-0.3, 0.5, 1.2, 0.7, 0.4, 1.1)
    parameters = BipolarFVParameters(2.4, 1.7, 0.6, 0.25)
    potential = rng.normal(scale=0.2, size=count)
    log_electron = rng.normal(scale=0.15, size=count)
    log_hole = rng.normal(scale=0.13, size=count)
    state = pack_bipolar_state(potential, log_electron, log_hole)
    residual = assemble_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )

    transformed_boundaries = BipolarBoundaryValues(
        0.3,
        -0.5,
        0.4,
        1.1,
        1.2,
        0.7,
    )
    transformed_parameters = BipolarFVParameters(2.4, 0.6, 1.7, -0.25)
    transformed_state = pack_bipolar_state(-potential, log_hole, log_electron)
    transformed = assemble_bipolar_residual(
        transformed_state,
        mesh=mesh,
        boundaries=transformed_boundaries,
        parameters=transformed_parameters,
    )
    np.testing.assert_allclose(
        transformed[:count], -residual[:count], rtol=2.0e-13, atol=2.0e-13
    )
    np.testing.assert_allclose(
        transformed[count : 2 * count],
        -residual[2 * count :],
        rtol=2.0e-13,
        atol=2.0e-13,
    )
    np.testing.assert_allclose(
        transformed[2 * count :],
        -residual[count : 2 * count],
        rtol=2.0e-13,
        atol=2.0e-13,
    )


def test_constant_hole_population_recovers_unipolar_poisson_and_electron_blocks() -> None:
    rng = np.random.default_rng(10)
    mesh = UniformNodeMesh1D(length=1.0, intervals=8)
    count = mesh.interior_count
    hole_density = 0.3
    unipolar_background = 1.2
    boundaries = BipolarBoundaryValues(
        -0.2,
        0.4,
        1.1,
        1.6,
        hole_density,
        hole_density,
    )
    parameters = BipolarFVParameters(
        1.9,
        1.3,
        0.8,
        unipolar_background - hole_density,
    )
    potential = rng.normal(scale=0.1, size=count)
    log_electron = rng.normal(scale=0.1, size=count)
    state = pack_bipolar_state(
        potential,
        log_electron,
        np.full(count, np.log(hole_density)),
    )
    bipolar = assemble_bipolar_residual(
        state,
        mesh=mesh,
        boundaries=boundaries,
        parameters=parameters,
    )

    unipolar_boundaries = UnipolarBoundaryValues(
        boundaries.potential_left,
        boundaries.potential_right,
        boundaries.electron_density_left,
        boundaries.electron_density_right,
    )
    unipolar_parameters = UnipolarFVParameters(
        parameters.screening_strength,
        parameters.electron_diffusion_ratio,
        unipolar_background,
    )
    unipolar = assemble_unipolar_residual(
        np.concatenate([potential, log_electron]),
        mesh=mesh,
        boundaries=unipolar_boundaries,
        parameters=unipolar_parameters,
    )
    np.testing.assert_allclose(
        bipolar[: 2 * count], unipolar, rtol=1.0e-13, atol=1.0e-13
    )


def test_logarithmic_state_reconstruction_preserves_positive_densities() -> None:
    mesh = UniformNodeMesh1D(length=2.0, intervals=10)
    boundaries = BipolarBoundaryValues(-0.1, 0.5, 0.2, 3.0, 4.0, 0.3)
    state = linear_bipolar_reservoir_state(mesh=mesh, boundaries=boundaries)
    reconstructed = reconstruct_bipolar_state(
        state,
        mesh=mesh,
        boundaries=boundaries,
    )
    assert np.all(reconstructed.electron_density > 0.0)
    assert np.all(reconstructed.hole_density > 0.0)
    np.testing.assert_allclose(
        reconstructed.potential,
        np.linspace(-0.1, 0.5, mesh.node_count),
    )


@pytest.mark.parametrize(
    "factory",
    [
        lambda: BipolarBoundaryValues(0.0, 0.0, 0.0, 1.0, 1.0, 1.0),
        lambda: BipolarFVParameters(-1.0),
        lambda: BipolarFVParameters(1.0, electron_diffusion_ratio=0.0),
        lambda: BipolarFVParameters(1.0, hole_diffusion_ratio=0.0),
    ],
)
def test_invalid_bipolar_configurations_are_rejected(factory) -> None:
    with pytest.raises(ValueError):
        factory()
