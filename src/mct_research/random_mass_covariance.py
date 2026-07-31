"""Periodic correlated random-mass fields for the R05 minimal Dirac oracle.

The functions in this module use dimensionless or explicitly documented physical
inputs.  They generate stationary Gaussian fields on a periodic one-dimensional
grid from a non-negative discrete power spectrum.  A generated field is a
synthetic model realization, not an inferred HgCdTe alloy profile.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi, sqrt
from typing import Literal

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
CovarianceFamily = Literal["gaussian", "matern_0.5", "matern_1.5", "matern_2.5"]
SUPPORTED_COVARIANCE_FAMILIES: tuple[CovarianceFamily, ...] = (
    "gaussian",
    "matern_0.5",
    "matern_1.5",
    "matern_2.5",
)


@dataclass(frozen=True)
class RandomMassField:
    """One deterministic realization and its declared/realized statistics."""

    coordinates: FloatArray
    mass: FloatArray
    fluctuation: FloatArray
    mean_mass: float
    target_sigma_mass: float
    correlation_length: float
    covariance_family: str
    remove_sample_mean: bool
    normalize_sample_variance: bool
    realized_fluctuation_mean: float
    realized_fluctuation_sigma: float


def _read_only(values: NDArray[np.float64] | list[float]) -> FloatArray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _finite(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _grid_size(grid_points: int) -> int:
    if isinstance(grid_points, bool) or int(grid_points) != grid_points:
        raise ValueError("grid_points must be an integer")
    count = int(grid_points)
    if count < 8:
        raise ValueError("grid_points must be at least 8")
    return count


def periodic_wave_numbers(grid_points: int, length: float) -> FloatArray:
    """Return FFT-ordered periodic wave numbers in inverse length units."""

    count = _grid_size(grid_points)
    box_length = _positive("length", length)
    spacing = box_length / count
    return _read_only(2.0 * pi * np.fft.fftfreq(count, d=spacing))


def covariance_power_spectrum(
    grid_points: int,
    length: float,
    correlation_length: float,
    family: CovarianceFamily = "gaussian",
    *,
    remove_zero_mode: bool = True,
) -> FloatArray:
    """Return a normalized non-negative discrete covariance power spectrum.

    The spectrum is normalized so that ``mean(power) == 1`` over retained modes.
    Consequently, filtering unit-variance real white noise by ``sqrt(power)``
    gives unit ensemble point variance under NumPy's FFT normalization.

    Gaussian convention::

        C(r) = exp[-r**2/(2 xi**2)]  (in the large-box limit)

    Matérn convention matches the standard one-dimensional spectral shape for
    ``z = sqrt(2 nu) r / xi``.  The finite grid represents the corresponding
    periodized covariance.
    """

    count = _grid_size(grid_points)
    box_length = _positive("length", length)
    xi = _positive("correlation_length", correlation_length)
    if family not in SUPPORTED_COVARIANCE_FAMILIES:
        raise ValueError(
            f"family must be one of {SUPPORTED_COVARIANCE_FAMILIES}, got {family!r}"
        )

    wave_numbers = np.asarray(periodic_wave_numbers(count, box_length))
    if family == "gaussian":
        raw = np.exp(-0.5 * (wave_numbers * xi) ** 2)
    else:
        smoothness = float(family.split("_")[1])
        inverse_scale = sqrt(2.0 * smoothness) / xi
        raw = (inverse_scale**2 + wave_numbers**2) ** (-(smoothness + 0.5))

    raw = np.asarray(raw, dtype=float)
    if remove_zero_mode:
        raw[0] = 0.0
    if not np.all(np.isfinite(raw)) or np.any(raw < 0.0):
        raise ArithmeticError("covariance spectrum must be finite and non-negative")
    mean_power = float(np.mean(raw))
    if mean_power <= 0.0:
        raise ArithmeticError("covariance spectrum has no retained variance")
    return _read_only(raw / mean_power)


def periodic_target_correlation(
    grid_points: int,
    length: float,
    correlation_length: float,
    family: CovarianceFamily = "gaussian",
    *,
    remove_zero_mode: bool = True,
) -> FloatArray:
    """Return the exact discrete periodic correlation implied by the spectrum."""

    power = np.asarray(
        covariance_power_spectrum(
            grid_points,
            length,
            correlation_length,
            family,
            remove_zero_mode=remove_zero_mode,
        )
    )
    correlation = np.fft.ifft(power).real
    if correlation[0] <= 0.0:
        raise ArithmeticError("zero-lag covariance must be positive")
    correlation /= correlation[0]
    return _read_only(correlation)


def generate_random_mass_field(
    grid_points: int,
    length: float,
    mean_mass: float,
    sigma_mass: float,
    correlation_length: float,
    *,
    seed: int | np.random.SeedSequence,
    family: CovarianceFamily = "gaussian",
    remove_sample_mean: bool = True,
    normalize_sample_variance: bool = False,
) -> RandomMassField:
    """Generate one real periodic Gaussian random-mass realization.

    ``remove_sample_mean=True`` removes the zero Fourier mode before filtering,
    so the declared mean mass is exact for every realization.  This conditions
    the finite box and must be recorded.  ``normalize_sample_variance=True`` is a
    stronger per-realization conditioning operation and is disabled by default.
    """

    count = _grid_size(grid_points)
    box_length = _positive("length", length)
    mean_value = _finite("mean_mass", mean_mass)
    sigma = _finite("sigma_mass", sigma_mass)
    xi = _positive("correlation_length", correlation_length)
    if sigma < 0.0:
        raise ValueError("sigma_mass must be non-negative")

    coordinates = np.arange(count, dtype=float) * (box_length / count)
    if sigma == 0.0:
        fluctuation = np.zeros(count, dtype=float)
    else:
        rng = np.random.default_rng(seed)
        white = rng.normal(size=count)
        power = np.asarray(
            covariance_power_spectrum(
                count,
                box_length,
                xi,
                family,
                remove_zero_mode=remove_sample_mean,
            )
        )
        fluctuation = np.fft.ifft(np.fft.fft(white) * np.sqrt(power)).real
        if remove_sample_mean:
            fluctuation -= float(np.mean(fluctuation))
        if normalize_sample_variance:
            realized = float(np.std(fluctuation))
            if realized <= 0.0:
                raise ArithmeticError("cannot normalize a zero-variance realization")
            fluctuation /= realized
        fluctuation *= sigma

    realized_mean = float(np.mean(fluctuation))
    realized_sigma = float(np.std(fluctuation))
    mass = mean_value + fluctuation
    return RandomMassField(
        coordinates=_read_only(coordinates),
        mass=_read_only(mass),
        fluctuation=_read_only(fluctuation),
        mean_mass=mean_value,
        target_sigma_mass=sigma,
        correlation_length=xi,
        covariance_family=family,
        remove_sample_mean=bool(remove_sample_mean),
        normalize_sample_variance=bool(normalize_sample_variance),
        realized_fluctuation_mean=realized_mean,
        realized_fluctuation_sigma=realized_sigma,
    )