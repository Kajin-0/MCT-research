"""R07 conditional spectral and root bounds, without material parameters.

These helpers do not infer alloy kernels from binary data. A discrete measure
is a Hermitian Feshbach model; its tests establish mathematical behavior only.
Real-axis bounds require an actual support separation and simple-root bounds.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DiscreteFeshbachMeasure:
    """Positive spectral weights (energy squared) at real energies."""

    energies: np.ndarray
    weights: np.ndarray

    def __post_init__(self):
        energies = np.array(self.energies, dtype=float, copy=True)
        weights = np.array(self.weights, dtype=float, copy=True)
        if (energies.ndim != 1 or weights.shape != energies.shape
                or not np.all(np.isfinite(energies))
                or not np.all(np.isfinite(weights)) or np.any(weights < 0)):
            raise ValueError("A finite one-dimensional positive measure is required")
        support = weights > 0
        energies, weights = energies[support], weights[support]
        energies.flags.writeable = weights.flags.writeable = False
        object.__setattr__(self, "energies", energies)
        object.__setattr__(self, "weights", weights)

    def kernel(self, z: complex) -> complex:
        denominators = complex(z) - self.energies
        if np.any(denominators == 0):
            raise ValueError("Evaluation on the support is not an off-spectrum bound")
        return complex(np.sum(self.weights / denominators))

    def derivative(self, z: complex) -> complex:
        denominators = complex(z) - self.energies
        if np.any(denominators == 0):
            raise ValueError("Evaluation on the support is not an off-spectrum bound")
        return complex(-np.sum(self.weights / denominators**2))

    def moments(self, reference: float) -> tuple[float, float, float]:
        if not np.isfinite(reference):
            raise ValueError("A finite real reference is required")
        distance = float(np.min(np.abs(reference - self.energies), initial=np.inf))
        if distance == 0:
            raise ValueError("Reference must be outside the positive measure support")
        return self.kernel(reference).real, -self.derivative(reference).real, distance

    def linearization_bound(self, reference: float, half_width: float) -> float:
        """Uniform value error on a real interval; fails if it touches support."""
        if not np.isfinite(half_width) or half_width < 0:
            raise ValueError("A finite nonnegative half-width is required")
        _, susceptibility, distance = self.moments(reference)
        if half_width >= distance:
            raise ValueError("The requested interval is not separated from support")
        return float(susceptibility * half_width**2 / (distance - half_width))


def mass_root_error_bound(eps_scalar: float, eps_mass: float,
                          scalar_slope_min: float, mass_energy_lipschitz: float,
                          mass_composition_slope_min: float) -> float:
    """Conditional |delta x| bound; callers must establish bracket/existence.

    eps values are uniform errors in energy; scalar slope and energy Lipschitz
    factor are dimensionless; mass composition slope is energy per unit x.
    This does not certify those bounds from endpoint derivatives.
    """
    values = (eps_scalar, eps_mass, scalar_slope_min,
              mass_energy_lipschitz, mass_composition_slope_min)
    if not all(np.isfinite(v) for v in values):
        raise ValueError("Bounds must be finite")
    if (eps_scalar < 0 or eps_mass < 0 or mass_energy_lipschitz < 0
            or scalar_slope_min <= 0 or mass_composition_slope_min <= 0):
        raise ValueError("Errors must be nonnegative and slope bounds positive")
    return ((eps_mass + mass_energy_lipschitz * eps_scalar / scalar_slope_min)
            / mass_composition_slope_min)


def covariance_resolvent_error_bound(contrast_norm: float,
                                    coherent_spectral_distance: float) -> float:
    """Conditional resolvent error including the Born Dyson resummation tail."""
    if (not np.isfinite(contrast_norm) or not np.isfinite(coherent_spectral_distance)
            or contrast_norm < 0 or coherent_spectral_distance <= 0):
        raise ValueError("Finite nonnegative contrast and positive distance required")
    ratio = contrast_norm / coherent_spectral_distance
    if ratio >= 1:
        raise ValueError("No Neumann certificate when contrast/distance >= 1")
    return (ratio**3 / (1-ratio) + ratio**4 / (1-ratio**2)) / coherent_spectral_distance
