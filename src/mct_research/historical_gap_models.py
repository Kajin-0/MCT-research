"""Historical HgCdTe band-gap formulas retained as explicit comparators.

These models are not promoted reference equations. They are separated from the
main gap-model module because their original data, composition metrology, and
uncertainty records are incomplete in the repository.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

GapValue = float | NDArray[np.float64]

SEILER_1990_A_K3 = -1822.0
SEILER_1990_B_K2 = 255.2
SEILER_1990_SOURCE_DOI = "10.1116/1.576952"


def _validated_inputs(
    x: ArrayLike, temperature_k: ArrayLike
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    composition = np.asarray(x, dtype=float)
    temperature = np.asarray(temperature_k, dtype=float)
    composition, temperature = np.broadcast_arrays(composition, temperature)
    if not np.all(np.isfinite(composition)) or not np.all(np.isfinite(temperature)):
        raise ValueError("composition and temperature must be finite")
    if np.any((composition < 0.0) | (composition > 1.0)):
        raise ValueError("Cd mole fraction x must lie in [0, 1]")
    if np.any(temperature < 0.0):
        raise ValueError("temperature must be non-negative")
    return composition, temperature


def _scalar_or_array(value: NDArray[np.float64]) -> GapValue:
    return float(value) if value.ndim == 0 else value


def _hansen_static_gap_ev(composition: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.asarray(
        -0.302
        + 1.930 * composition
        - 0.810 * composition**2
        + 0.832 * composition**3,
        dtype=float,
    )


def seiler_1990_gap_ev(x: ArrayLike, temperature_k: ArrayLike) -> GapValue:
    """Return the published Seiler 1990 rational-temperature gap in eV.

    The reconstructed published expression is

    ``Eg = Eg_Hansen(x,0) + 5.35e-4*(1-2*x)*(A+T^3)/(B+T^2)``

    with ``A=-1822 K^3`` and ``B=255.2 K^2``. The primary source is
    DOI ``10.1116/1.576952``. This function is retained as a historical
    comparator, not a production-selected equation. Its thermal term is nonzero
    at ``T=0``.
    """

    composition, temperature = _validated_inputs(x, temperature_k)
    thermal = (
        5.35e-4
        * (1.0 - 2.0 * composition)
        * (SEILER_1990_A_K3 + temperature**3)
        / (SEILER_1990_B_K2 + temperature**2)
    )
    return _scalar_or_array(_hansen_static_gap_ev(composition) + thermal)


def chu_1983_gap_ev(x: ArrayLike, temperature_k: ArrayLike) -> GapValue:
    """Return the Chu et al. 1983 empirical signed gap in eV.

    The published expression is

    ``Eg = -0.295 + 1.87x - 0.28x^2 + 0.35x^4
           + (6 - 14x + 3x^2) 1e-4 T``.

    Chu et al. reported the relation for ``0 <= x <= 0.37`` together with the
    CdTe endpoint and ``4.2 <= T <= 300 K``. The repository retains it only as
    a provenance-bound historical comparator. The point-level primary fitting
    table and composition uncertainties have not been recovered.

    Primary formula source: Appl. Phys. Lett. 43, 1064 (1983),
    DOI ``10.1063/1.94237``.
    """

    composition, temperature = _validated_inputs(x, temperature_k)
    gap = (
        -0.295
        + 1.87 * composition
        - 0.28 * composition**2
        + 0.35 * composition**4
        + (6.0 - 14.0 * composition + 3.0 * composition**2)
        * 1.0e-4
        * temperature
    )
    return _scalar_or_array(np.asarray(gap, dtype=float))
