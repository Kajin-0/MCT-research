"""Project-defined simplified Kane statistics closure for R06 Phase 1C.

This module uses the isotropic nonparabolic dispersion

    E (1 + alpha E) = hbar^2 k^2 / (2 m*)

as a mathematical benchmark.  It is not the full three-band HgCdTe closure
used by Madarasz or Lowney, does not contain material parameter relations, and
is not authorized for predictive HgCdTe calculations.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import isfinite, pi, sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .statistics_interface import CarrierStatisticsState
from .statistics_prototype import BOLTZMANN_EV_PER_K


MODEL_IDENTITY = "project_defined_isotropic_simplified_kane"


@dataclass(frozen=True)
class KaneQuadratureOptions:
    """Fixed quadrature controls for the dimensionless energy integrals."""

    quadrature_order: int = 320
    tail_margin: float = 40.0

    def __post_init__(self) -> None:
        order = int(self.quadrature_order)
        margin = float(self.tail_margin)
        if order != self.quadrature_order or order < 32:
            raise ValueError("quadrature_order must be an integer >= 32")
        if not isfinite(margin) or margin < 24.0:
            raise ValueError("tail_margin must be finite and >= 24")
        object.__setattr__(self, "quadrature_order", order)
        object.__setattr__(self, "tail_margin", margin)


@dataclass(frozen=True)
class SimplifiedKaneStatistics:
    """Carrier state plus explicit simplified-Kane diagnostics."""

    carrier: CarrierStatisticsState
    nonparabolicity_ev_inverse: float
    reduced_nonparabolicity: float
    parabolic_normalized_density: float
    parabolic_normalized_compressibility: float
    density_enhancement_over_parabolic: float
    compressibility_enhancement_over_parabolic: float
    model_identity: str = MODEL_IDENTITY

    def __post_init__(self) -> None:
        values = (
            self.nonparabolicity_ev_inverse,
            self.reduced_nonparabolicity,
            self.parabolic_normalized_density,
            self.parabolic_normalized_compressibility,
            self.density_enhancement_over_parabolic,
            self.compressibility_enhancement_over_parabolic,
        )
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("Kane diagnostic values must be finite")
        if self.nonparabolicity_ev_inverse < 0.0:
            raise ValueError("nonparabolicity_ev_inverse must be non-negative")
        if self.reduced_nonparabolicity < 0.0:
            raise ValueError("reduced_nonparabolicity must be non-negative")
        if self.parabolic_normalized_density <= 0.0:
            raise ValueError("parabolic_normalized_density must be positive")
        if self.parabolic_normalized_compressibility <= 0.0:
            raise ValueError("parabolic_normalized_compressibility must be positive")
        if self.density_enhancement_over_parabolic <= 0.0:
            raise ValueError("density enhancement must be positive")
        if self.compressibility_enhancement_over_parabolic <= 0.0:
            raise ValueError("compressibility enhancement must be positive")
        if self.model_identity != MODEL_IDENTITY:
            raise ValueError("model_identity must remain explicit and fixed")


@dataclass(frozen=True)
class ProjectDefinedKaneClosure:
    """Closure adapter satisfying the merged carrier-statistics protocol.

    ``parabolic_density_scale_cm3`` is the density scale that would multiply
    ``F_{1/2}`` in the parabolic limit.  It is supplied explicitly rather than
    inferred from an HgCdTe effective-mass model.
    """

    parabolic_density_scale_cm3: float
    nonparabolicity_ev_inverse: float
    quadrature: KaneQuadratureOptions = KaneQuadratureOptions()

    def __post_init__(self) -> None:
        scale = float(self.parabolic_density_scale_cm3)
        alpha = float(self.nonparabolicity_ev_inverse)
        if not isfinite(scale) or scale <= 0.0:
            raise ValueError("parabolic_density_scale_cm3 must be finite and positive")
        if not isfinite(alpha) or alpha < 0.0:
            raise ValueError("nonparabolicity_ev_inverse must be finite and non-negative")
        object.__setattr__(self, "parabolic_density_scale_cm3", scale)
        object.__setattr__(self, "nonparabolicity_ev_inverse", alpha)

    def evaluate(self, *, eta: float, temperature_k: float) -> CarrierStatisticsState:
        """Return the protocol carrier state."""

        return self.evaluate_detailed(eta=eta, temperature_k=temperature_k).carrier

    def evaluate_detailed(
        self,
        *,
        eta: float,
        temperature_k: float,
    ) -> SimplifiedKaneStatistics:
        """Return the carrier state and model-specific diagnostics."""

        return evaluate_simplified_kane_statistics(
            eta=eta,
            temperature_k=temperature_k,
            parabolic_density_scale_cm3=self.parabolic_density_scale_cm3,
            nonparabolicity_ev_inverse=self.nonparabolicity_ev_inverse,
            quadrature=self.quadrature,
        )


@lru_cache(maxsize=16)
def _legendre_nodes_weights(
    order: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    return nodes.astype(float), weights.astype(float)


def _finite(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def simplified_kane_dos_shape(
    reduced_energy: ArrayLike,
    reduced_nonparabolicity: float,
) -> float | NDArray[np.float64]:
    r"""Return the dimensionless DOS shape relative to ``sqrt(epsilon)``.

    For

    .. math::

        E(1+\alpha E)=\hbar^2k^2/(2m^*),

    the three-dimensional density of states is proportional to

    .. math::

        \sqrt{E(1+\alpha E)}(1+2\alpha E).

    With ``epsilon=E/(k_B T)`` and ``beta=alpha k_B T``, the factor multiplying
    ``sqrt(epsilon)`` is

    .. math::

        \sqrt{1+\beta\epsilon}(1+2\beta\epsilon).
    """

    energy = np.asarray(reduced_energy, dtype=float)
    scalar = energy.ndim == 0
    beta = _finite(reduced_nonparabolicity, name="reduced_nonparabolicity")
    if beta < 0.0:
        raise ValueError("reduced_nonparabolicity must be non-negative")
    if not np.all(np.isfinite(energy)) or np.any(energy < 0.0):
        raise ValueError("reduced_energy must be finite and non-negative")
    shape = np.sqrt(1.0 + beta * energy) * (1.0 + 2.0 * beta * energy)
    if scalar:
        return float(shape)
    return shape.astype(float)


def simplified_kane_normalized_integrals(
    *,
    eta: float,
    reduced_nonparabolicity: float,
    quadrature: KaneQuadratureOptions | None = None,
) -> tuple[float, float]:
    r"""Return normalized density and chemical-compressibility integrals.

    The normalization is chosen so the zero-nonparabolicity limit is exactly
    the R06 normalized parabolic convention:

    .. math::

        I_n(\eta,0)=\mathcal F_{1/2}(\eta),
        \qquad
        I_\chi(\eta,0)=\mathcal F_{-1/2}(\eta).
    """

    eta_value = _finite(eta, name="eta")
    beta = _finite(reduced_nonparabolicity, name="reduced_nonparabolicity")
    if beta < 0.0:
        raise ValueError("reduced_nonparabolicity must be non-negative")
    controls = KaneQuadratureOptions() if quadrature is None else quadrature

    upper_energy = max(controls.tail_margin, eta_value + controls.tail_margin)
    y_max = sqrt(upper_energy)
    nodes, weights = _legendre_nodes_weights(controls.quadrature_order)
    y = 0.5 * (nodes + 1.0) * y_max
    mapped_weights = 0.5 * y_max * weights
    energy = y**2
    occupation = np.exp(-np.logaddexp(0.0, energy - eta_value))
    shape = np.asarray(simplified_kane_dos_shape(energy, beta), dtype=float)

    # epsilon=y^2 removes the square-root endpoint.  The complete normalized
    # prefactor is (2/sqrt(pi)) and d epsilon = 2 y d y.
    base = 4.0 / sqrt(pi) * y**2 * shape
    density = float(np.sum(mapped_weights * base * occupation))
    compressibility = float(
        np.sum(mapped_weights * base * occupation * (1.0 - occupation))
    )
    if not isfinite(density) or not isfinite(compressibility):
        raise FloatingPointError("non-finite simplified-Kane integral")
    if density <= 0.0 or compressibility <= 0.0:
        raise FloatingPointError("simplified-Kane integrals must be positive")
    return density, compressibility


def evaluate_simplified_kane_statistics(
    *,
    eta: float,
    temperature_k: float,
    parabolic_density_scale_cm3: float,
    nonparabolicity_ev_inverse: float,
    quadrature: KaneQuadratureOptions | None = None,
) -> SimplifiedKaneStatistics:
    """Evaluate the project-defined simplified Kane benchmark closure."""

    eta_value = _finite(eta, name="eta")
    temperature = _finite(temperature_k, name="temperature_k")
    scale = _finite(parabolic_density_scale_cm3, name="parabolic_density_scale_cm3")
    alpha = _finite(nonparabolicity_ev_inverse, name="nonparabolicity_ev_inverse")
    if temperature <= 0.0:
        raise ValueError("temperature_k must be positive")
    if scale <= 0.0:
        raise ValueError("parabolic_density_scale_cm3 must be positive")
    if alpha < 0.0:
        raise ValueError("nonparabolicity_ev_inverse must be non-negative")

    thermal_energy = BOLTZMANN_EV_PER_K * temperature
    beta = alpha * thermal_energy
    density_integral, compressibility_integral = simplified_kane_normalized_integrals(
        eta=eta_value,
        reduced_nonparabolicity=beta,
        quadrature=quadrature,
    )
    parabolic_density, parabolic_compressibility = (
        simplified_kane_normalized_integrals(
            eta=eta_value,
            reduced_nonparabolicity=0.0,
            quadrature=quadrature,
        )
    )
    carrier = CarrierStatisticsState(
        eta=eta_value,
        temperature_k=temperature,
        density_scale_cm3=scale,
        normalized_density=density_integral,
        normalized_compressibility=compressibility_integral,
        density_cm3=scale * density_integral,
        compressibility_cm3_per_ev=(
            scale * compressibility_integral / thermal_energy
        ),
        generalized_einstein_factor=density_integral / compressibility_integral,
    )
    return SimplifiedKaneStatistics(
        carrier=carrier,
        nonparabolicity_ev_inverse=alpha,
        reduced_nonparabolicity=beta,
        parabolic_normalized_density=parabolic_density,
        parabolic_normalized_compressibility=parabolic_compressibility,
        density_enhancement_over_parabolic=density_integral / parabolic_density,
        compressibility_enhancement_over_parabolic=(
            compressibility_integral / parabolic_compressibility
        ),
    )
