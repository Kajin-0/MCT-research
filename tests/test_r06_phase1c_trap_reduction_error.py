from __future__ import annotations

import numpy as np
import pytest

from mct_research.transport_noise.trap_kinetics_prototype import ReversibleTrapParameters
from mct_research.transport_noise.trap_reduction_error import (
    conservative_reduction_boundary,
    constant_kappa_pair_rate,
    constant_kappa_reference,
    corner_coefficient_errors,
    reduction_error_metrics,
    symmetric_log_domain_radius,
)


def _trap(
    *,
    density: float = 0.12,
    electron_capture: float = 0.45,
    hole_capture: float = 0.45,
    electron_equilibrium: float = 1.0,
    hole_equilibrium: float = 1.0,
    occupancy: float = 0.5,
) -> ReversibleTrapParameters:
    return ReversibleTrapParameters(
        trap_density=density,
        electron_capture_coefficient=electron_capture,
        hole_capture_coefficient=hole_capture,
        equilibrium_electron_density=electron_equilibrium,
        equilibrium_hole_density=hole_equilibrium,
        equilibrium_occupancy=occupancy,
    )


def _ensemble() -> list[tuple[str, ReversibleTrapParameters]]:
    return [
        ("balanced", _trap()),
        (
            "electron_fast",
            _trap(electron_capture=0.9, hole_capture=0.25, occupancy=0.35),
        ),
        (
            "hole_fast",
            _trap(electron_capture=0.25, hole_capture=0.9, occupancy=0.65),
        ),
        (
            "shifted_equilibrium",
            _trap(
                electron_capture=0.65,
                hole_capture=0.35,
                electron_equilibrium=1.3,
                hole_equilibrium=0.75,
                occupancy=0.42,
            ),
        ),
    ]


def test_reference_defaults_to_declared_equilibrium() -> None:
    trap = _trap()
    reference = constant_kappa_reference(trap_parameters=trap)
    assert reference.electron_density == trap.equilibrium_electron_density
    assert reference.hole_density == trap.equilibrium_hole_density
    assert reference.coefficient > 0.0


def test_constant_reduction_and_exact_rate_agree_at_reference() -> None:
    trap = _trap()
    reference = constant_kappa_reference(trap_parameters=trap)
    electron = np.array([0.7, 1.0, 1.8])
    hole = np.array([1.4, 1.0, 0.9])
    metrics = reduction_error_metrics(
        electron,
        hole,
        trap_parameters=trap,
        reference=reference,
    )
    reduced = constant_kappa_pair_rate(
        electron,
        hole,
        trap_parameters=trap,
        reference=reference,
    )
    assert metrics.reduced_pair_rate == pytest.approx(reduced)
    assert metrics.coefficient_relative_error[1] == pytest.approx(0.0)
    assert metrics.exact_pair_rate[1] == pytest.approx(0.0)
    assert metrics.reduced_pair_rate[1] == pytest.approx(0.0)


def test_pair_rate_relative_error_equals_coefficient_error_off_balance() -> None:
    trap = _trap()
    reference = constant_kappa_reference(trap_parameters=trap)
    electron = np.array([0.6, 1.4, 2.0])
    hole = np.array([0.8, 1.2, 1.5])
    metrics = reduction_error_metrics(
        electron,
        hole,
        trap_parameters=trap,
        reference=reference,
    )
    relative_rate = np.abs(
        metrics.reduced_pair_rate / metrics.exact_pair_rate - 1.0
    )
    assert relative_rate == pytest.approx(metrics.coefficient_relative_error)


def test_exact_radius_saturates_tolerance_at_a_corner() -> None:
    trap = _trap()
    tolerance = 0.1
    radius = symmetric_log_domain_radius(
        trap_parameters=trap,
        tolerance=tolerance,
    )
    errors = corner_coefficient_errors(
        trap_parameters=trap,
        radius=radius,
    )
    assert np.max(errors) == pytest.approx(tolerance, rel=2e-13, abs=2e-15)
    assert np.all(errors <= tolerance * (1.0 + 3e-13))


def test_slightly_larger_radius_violates_tolerance() -> None:
    trap = _trap()
    tolerance = 0.1
    radius = symmetric_log_domain_radius(
        trap_parameters=trap,
        tolerance=tolerance,
    )
    errors = corner_coefficient_errors(
        trap_parameters=trap,
        radius=radius + 1e-4,
    )
    assert np.max(errors) > tolerance


def test_dense_grid_inside_exact_radius_respects_tolerance() -> None:
    trap = _trap()
    tolerance = 0.08
    reference = constant_kappa_reference(trap_parameters=trap)
    radius = symmetric_log_domain_radius(
        trap_parameters=trap,
        tolerance=tolerance,
        reference=reference,
    )
    coordinates = np.linspace(-radius, radius, 31)
    electron, hole = np.meshgrid(
        reference.electron_density * np.exp(coordinates),
        reference.hole_density * np.exp(coordinates),
        indexing="ij",
    )
    metrics = reduction_error_metrics(
        electron,
        hole,
        trap_parameters=trap,
        reference=reference,
    )
    assert np.max(metrics.coefficient_relative_error) <= tolerance * (1 + 5e-13)


def test_radius_increases_monotonically_with_tolerance() -> None:
    trap = _trap()
    radii = [
        symmetric_log_domain_radius(trap_parameters=trap, tolerance=value)
        for value in (0.02, 0.05, 0.1, 0.2)
    ]
    assert radii == sorted(radii)
    assert len(set(radii)) == len(radii)


def test_trap_density_changes_scale_but_not_relative_domain() -> None:
    low = _trap(density=0.03)
    high = _trap(density=0.6)
    tolerance = 0.1
    assert symmetric_log_domain_radius(
        trap_parameters=low,
        tolerance=tolerance,
    ) == pytest.approx(
        symmetric_log_domain_radius(
            trap_parameters=high,
            tolerance=tolerance,
        )
    )
    assert constant_kappa_reference(
        trap_parameters=high
    ).coefficient == pytest.approx(
        20.0 * constant_kappa_reference(trap_parameters=low).coefficient
    )


def test_conservative_boundary_is_minimum_of_declared_scenarios() -> None:
    boundary = conservative_reduction_boundary(_ensemble(), tolerance=0.1)
    radii = {record.name: record.radius for record in boundary.scenarios}
    assert boundary.conservative_radius == min(radii.values())
    assert radii[boundary.controlling_scenario] == boundary.conservative_radius
    assert boundary.minimum_density_factor == pytest.approx(
        np.exp(-boundary.conservative_radius)
    )
    assert boundary.maximum_density_factor == pytest.approx(
        np.exp(boundary.conservative_radius)
    )


def test_conservative_radius_verifies_each_scenario_corner() -> None:
    boundary = conservative_reduction_boundary(_ensemble(), tolerance=0.1)
    for name, trap in _ensemble():
        errors = corner_coefficient_errors(
            trap_parameters=trap,
            radius=boundary.conservative_radius,
        )
        assert np.max(errors) <= boundary.tolerance * (1 + 5e-13), name


def test_invalid_inputs_are_rejected() -> None:
    trap = _trap()
    with pytest.raises(ValueError):
        symmetric_log_domain_radius(trap_parameters=trap, tolerance=0.0)
    with pytest.raises(ValueError):
        symmetric_log_domain_radius(trap_parameters=trap, tolerance=1.0)
    with pytest.raises(ValueError):
        constant_kappa_reference(trap_parameters=trap, electron_density=-1.0)
    with pytest.raises(ValueError):
        corner_coefficient_errors(trap_parameters=trap, radius=-0.1)
    with pytest.raises(ValueError):
        conservative_reduction_boundary([], tolerance=0.1)
    with pytest.raises(ValueError):
        conservative_reduction_boundary(
            [("same", trap), ("same", trap)],
            tolerance=0.1,
        )
