from __future__ import annotations

import numpy as np

from mct_research.random_mass_covariance import generate_random_mass_field
from mct_research.random_mass_dirac import (
    dirac_eigenvalues,
    dirac_hamiltonian,
    hermiticity_residual,
    homogeneous_reference_eigenvalues,
    paired_spectrum_residual,
    periodic_domain_wall_pair,
)


def test_homogeneous_spectrum_matches_exact_reference_for_both_boundaries() -> None:
    mass = np.full(32, 0.7)
    for boundary in ("periodic", "antiperiodic"):
        hamiltonian = dirac_hamiltonian(mass, 12.0, boundary=boundary)
        values = np.linalg.eigvalsh(hamiltonian)
        reference = homogeneous_reference_eigenvalues(
            32, 12.0, 0.7, boundary=boundary
        )
        assert hermiticity_residual(hamiltonian) < 1.0e-14
        assert paired_spectrum_residual(values) < 1.0e-14
        assert np.max(np.abs(values - reference)) < 1.0e-12


def test_random_mass_realization_preserves_particle_hole_pairing() -> None:
    field = generate_random_mass_field(48, 16.0, 0.2, 0.6, 1.0, seed=418)
    values = dirac_eigenvalues(field.mass, 16.0, boundary="antiperiodic")
    assert paired_spectrum_residual(values) < 1.0e-13


def test_domain_wall_pair_near_zero_splitting_decreases_with_separation() -> None:
    minima = []
    for length, points in ((20.0, 80), (40.0, 160)):
        profile = periodic_domain_wall_pair(points, length, 1.0, 1.0)
        values = dirac_eigenvalues(profile, length, boundary="antiperiodic")
        minima.append(float(np.min(np.abs(values))))
    assert minima[1] < 0.2 * minima[0]