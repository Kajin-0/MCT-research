"""Phase 1C carrier-statistics prototypes for R06.

This module is intentionally limited to source-audit support and reduction
benchmarks. It does not implement the final HgCdTe Kane density of states,
charge-neutrality model, or drift-diffusion solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import exp, gamma, isfinite, sqrt
from typing import overload

import numpy as np
from numpy.typing import ArrayLike, NDArray

BOLTZMANN_EV_PER_K = 8.617333262145e-5
_SUPPORTED_ORDERS = (-0.5, 0.5)


@dataclass(frozen=True)
class ParabolicFermiStatistics:
    """Normalized parabolic-band statistics at one reduced chemical potential."""

    eta: float
    fermi_half: float
    fermi_minus_half: float
    generalized_einstein_factor: float
    boltzmann_density: float
    boltzmann_error_relative_to_fermi: float
    fermi_correction_relative_to_boltzmann: float


def _finite_float(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _positive_integer(value: int, *, name: str) -> int:
    number = int(value)
    if number != value or number < 16:
        raise ValueError(f"{name} must be an integer >= 16")
    return number


@lru_cache(maxsize=16)
def _legendre_nodes_weights(
    order: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    return nodes.astype(float), weights.astype(float)


@overload
def normalized_fermi_dirac(
    order: float,
    eta: float,
    *,
    quadrature_order: int = 256,
    tail_margin: float = 40.0,
) -> float: ...


@overload
def normalized_fermi_dirac(
    order: float,
    eta: ArrayLike,
    *,
    quadrature_order: int = 256,
    tail_margin: float = 40.0,
) -> NDArray[np.float64]: ...


def normalized_fermi_dirac(
    order: float,
    eta: ArrayLike,
    *,
    quadrature_order: int = 256,
    tail_margin: float = 40.0,
) -> float | NDArray[np.float64]:
    r"""Evaluate the normalized complete Fermi-Dirac integral.

    The convention is

    .. math::

        \mathcal F_j(\eta)
        = \frac{1}{\Gamma(j+1)}
          \int_0^\infty \frac{t^j}{1+\exp(t-\eta)}\,dt.

    Only ``j = -1/2`` and ``j = 1/2`` are implemented because they are the
    quantities needed for the Phase 1C parabolic density and compressibility
    benchmarks. The substitution ``t = y**2`` removes the integrable endpoint
    singularity for ``j = -1/2``. Fixed Gauss-Legendre quadrature is then
    applied over a tail-truncated interval whose omitted occupation is
    exponentially small relative to ``tail_margin``.
    """

    order_value = _finite_float(order, name="order")
    if order_value not in _SUPPORTED_ORDERS:
        raise ValueError("order must be -0.5 or 0.5")

    quadrature = _positive_integer(quadrature_order, name="quadrature_order")
    margin = _finite_float(tail_margin, name="tail_margin")
    if margin < 24.0:
        raise ValueError("tail_margin must be >= 24")

    eta_array = np.asarray(eta, dtype=float)
    scalar = eta_array.ndim == 0
    flat_eta = np.atleast_1d(eta_array).reshape(-1)
    if not np.all(np.isfinite(flat_eta)):
        raise ValueError("eta must contain only finite values")

    upper_energy = max(margin, float(np.max(flat_eta)) + margin)
    y_max = sqrt(upper_energy)
    nodes, weights = _legendre_nodes_weights(quadrature)
    y = 0.5 * (nodes + 1.0) * y_max
    mapped_weights = 0.5 * y_max * weights

    energy = y[:, None] ** 2
    occupation = np.exp(-np.logaddexp(0.0, energy - flat_eta[None, :]))
    exponent = 2.0 * order_value + 1.0
    integrand = 2.0 * y[:, None] ** exponent * occupation
    values = (
        np.sum(mapped_weights[:, None] * integrand, axis=0)
        / gamma(order_value + 1.0)
    )
    reshaped = values.reshape(np.atleast_1d(eta_array).shape)

    if scalar:
        return float(reshaped[0])
    return reshaped


def parabolic_fermi_statistics(eta: float) -> ParabolicFermiStatistics:
    """Return density and generalized-Einstein reduction diagnostics."""

    eta_value = _finite_float(eta, name="eta")
    fermi_half = float(normalized_fermi_dirac(0.5, eta_value))
    fermi_minus_half = float(normalized_fermi_dirac(-0.5, eta_value))
    boltzmann = exp(eta_value)
    theta = fermi_half / fermi_minus_half
    return ParabolicFermiStatistics(
        eta=eta_value,
        fermi_half=fermi_half,
        fermi_minus_half=fermi_minus_half,
        generalized_einstein_factor=theta,
        boltzmann_density=boltzmann,
        boltzmann_error_relative_to_fermi=(
            abs(boltzmann - fermi_half) / fermi_half
        ),
        fermi_correction_relative_to_boltzmann=(
            abs(fermi_half - boltzmann) / boltzmann
        ),
    )


def hansen_schmit_intrinsic_density_cm3(
    *,
    composition: float,
    temperature_k: float,
    gap_ev: float,
    enforce_source_domain: bool = True,
) -> float:
    r"""Evaluate the Hansen-Schmit 1983 fitted intrinsic-density expression.

    The abstract-reported fit is

    .. math::

        n_i = 10^{14}
        [5.585 - 3.820x + 1.753\times10^{-3}T
        - 1.364\times10^{-3}xT]
        E_g^{3/4}T^{3/2}\exp[-E_g/(2k_BT)]

    in ``cm^-3`` with ``E_g`` in eV and ``T`` in kelvin.

    This function reproduces the published fit only. It is not the selected
    R06 reference statistics model and must not be extrapolated silently.
    """

    x = _finite_float(composition, name="composition")
    temperature = _finite_float(temperature_k, name="temperature_k")
    gap = _finite_float(gap_ev, name="gap_ev")
    if temperature <= 0.0:
        raise ValueError("temperature_k must be positive")
    if gap <= 0.0:
        raise ValueError("gap_ev must be positive")
    if x < 0.0:
        raise ValueError("composition must be non-negative")
    if enforce_source_domain and not (50.0 < temperature < 300.0 and x < 0.7):
        raise ValueError("outside abstract-reported Hansen-Schmit fit domain")

    prefactor = (
        5.585
        - 3.820 * x
        + 1.753e-3 * temperature
        - 1.364e-3 * x * temperature
    )
    if prefactor <= 0.0:
        raise ValueError("Hansen-Schmit prefactor is non-positive")
    return float(
        1.0e14
        * prefactor
        * gap**0.75
        * temperature**1.5
        * exp(-gap / (2.0 * BOLTZMANN_EV_PER_K * temperature))
    )
