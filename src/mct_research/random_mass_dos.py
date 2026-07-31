"""DOS estimation, ensemble averaging, convolution, and effect sizes for R05."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi, sqrt

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .random_mass_covariance import CovarianceFamily, generate_random_mass_field
from .random_mass_dirac import (
    BoundaryCondition,
    dirac_eigenvalues,
    homogeneous_reference_eigenvalues,
)

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class EnsembleDOS:
    energies: FloatArray
    mean_dos: FloatArray
    standard_error: FloatArray
    realization_dos: FloatArray
    realized_mass_means: FloatArray
    realized_mass_sigmas: FloatArray
    mean_mass: float
    sigma_mass: float
    correlation_length: float
    length: float
    grid_points: int
    broadening: float
    realizations: int
    seed: int
    covariance_family: str
    boundary: str
    remove_sample_mean: bool
    normalize_sample_variance: bool


@dataclass(frozen=True)
class ScalarFiniteBoxDOS:
    energies: FloatArray
    mean_dos: FloatArray
    standard_error: FloatArray
    realization_dos: FloatArray
    sampled_masses: FloatArray
    mean_mass: float
    sigma_mass: float
    length: float
    grid_points: int
    broadening: float
    realizations: int
    seed: int
    boundary: str


@dataclass(frozen=True)
class EffectSize:
    delta_1: float
    delta_infinity: float
    integrated_reference: float
    maximum_reference: float
    energy_minimum: float
    energy_maximum: float


def _read_only(values: ArrayLike) -> FloatArray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _uniform_energies(values: ArrayLike) -> tuple[FloatArray, float]:
    energy = np.asarray(values, dtype=float)
    if energy.ndim != 1 or energy.size < 3:
        raise ValueError("energies must be a one-dimensional array with at least 3 points")
    if not np.all(np.isfinite(energy)) or np.any(np.diff(energy) <= 0.0):
        raise ValueError("energies must be finite and strictly increasing")
    spacings = np.diff(energy)
    spacing = float(np.mean(spacings))
    if np.max(np.abs(spacings - spacing)) > 1.0e-10 * max(abs(spacing), 1.0):
        raise ValueError("energies must be uniformly spaced")
    return _read_only(energy), spacing


def _trapezoid(values: NDArray[np.float64], coordinates: NDArray[np.float64]) -> float:
    implementation = getattr(np, "trapezoid", None)
    if implementation is None:
        implementation = np.trapz
    return float(implementation(values, coordinates))


def _positive(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def gaussian_broadened_dos(
    energies: ArrayLike,
    eigenvalues: ArrayLike,
    length: float,
    broadening: float,
) -> FloatArray:
    """Return a normalized Gaussian-kernel DOS per unit length."""

    energy = np.asarray(energies, dtype=float)
    levels = np.asarray(eigenvalues, dtype=float)
    if energy.ndim != 1 or energy.size == 0 or not np.all(np.isfinite(energy)):
        raise ValueError("energies must be a finite non-empty one-dimensional array")
    if levels.ndim != 1 or levels.size == 0 or not np.all(np.isfinite(levels)):
        raise ValueError("eigenvalues must be a finite non-empty one-dimensional array")
    box_length = _positive("length", length)
    eta = _positive("broadening", broadening)
    differences = (energy[:, np.newaxis] - levels[np.newaxis, :]) / eta
    kernels = np.exp(-0.5 * differences**2) / (sqrt(2.0 * pi) * eta)
    return np.asarray(np.sum(kernels, axis=1) / box_length, dtype=float)


def average_random_mass_dos(
    energies: ArrayLike,
    mean_mass: float,
    sigma_mass: float,
    correlation_length: float,
    length: float,
    grid_points: int,
    broadening: float,
    realizations: int,
    *,
    seed: int,
    covariance_family: CovarianceFamily = "gaussian",
    boundary: BoundaryCondition = "periodic",
    hbar_velocity: float = 1.0,
    remove_sample_mean: bool = True,
    normalize_sample_variance: bool = False,
) -> EnsembleDOS:
    """Average the exact finite-box DOS over deterministic seed-spawned fields."""

    energy = np.asarray(energies, dtype=float)
    if energy.ndim != 1 or energy.size == 0 or not np.all(np.isfinite(energy)):
        raise ValueError("energies must be a finite non-empty one-dimensional array")
    if isinstance(realizations, bool) or int(realizations) != realizations:
        raise ValueError("realizations must be an integer")
    count = int(realizations)
    if count < 2:
        raise ValueError("at least two realizations are required")
    if isinstance(seed, bool) or int(seed) != seed or int(seed) < 0:
        raise ValueError("seed must be a non-negative integer")

    seed_sequences = np.random.SeedSequence(int(seed)).spawn(count)
    realization_values = np.empty((count, energy.size), dtype=float)
    realized_means = np.empty(count, dtype=float)
    realized_sigmas = np.empty(count, dtype=float)
    for index, child_seed in enumerate(seed_sequences):
        field = generate_random_mass_field(
            grid_points,
            length,
            mean_mass,
            sigma_mass,
            correlation_length,
            seed=child_seed,
            family=covariance_family,
            remove_sample_mean=remove_sample_mean,
            normalize_sample_variance=normalize_sample_variance,
        )
        levels = dirac_eigenvalues(
            field.mass,
            length,
            hbar_velocity=hbar_velocity,
            boundary=boundary,
        )
        realization_values[index] = gaussian_broadened_dos(
            energy,
            levels,
            length,
            broadening,
        )
        realized_means[index] = float(np.mean(field.mass))
        realized_sigmas[index] = field.realized_fluctuation_sigma

    mean_dos = np.mean(realization_values, axis=0)
    standard_error = np.std(realization_values, axis=0, ddof=1) / sqrt(count)
    return EnsembleDOS(
        energies=_read_only(energy),
        mean_dos=_read_only(mean_dos),
        standard_error=_read_only(standard_error),
        realization_dos=_read_only(realization_values),
        realized_mass_means=_read_only(realized_means),
        realized_mass_sigmas=_read_only(realized_sigmas),
        mean_mass=float(mean_mass),
        sigma_mass=float(sigma_mass),
        correlation_length=float(correlation_length),
        length=float(length),
        grid_points=int(grid_points),
        broadening=float(broadening),
        realizations=count,
        seed=int(seed),
        covariance_family=covariance_family,
        boundary=boundary,
        remove_sample_mean=bool(remove_sample_mean),
        normalize_sample_variance=bool(normalize_sample_variance),
    )


def finite_box_gaussian_quadrature_dos(
    energies: ArrayLike,
    mean_mass: float,
    sigma_mass: float,
    length: float,
    grid_points: int,
    broadening: float,
    *,
    boundary: BoundaryCondition = "periodic",
    hbar_velocity: float = 1.0,
    quadrature_order: int = 96,
) -> FloatArray:
    """Return a deterministic finite-box Gaussian scalar null.

    Gauss-Hermite nodes integrate the one-point Gaussian mass distribution,
    while every node uses the exact finite-box homogeneous Dirac spectrum and
    the same numerical DOS kernel as the correlated oracle.
    """

    energy = np.asarray(energies, dtype=float)
    if energy.ndim != 1 or energy.size == 0 or not np.all(np.isfinite(energy)):
        raise ValueError("energies must be a finite non-empty one-dimensional array")
    mean = float(mean_mass)
    sigma = float(sigma_mass)
    if not isfinite(mean):
        raise ValueError("mean_mass must be finite")
    if not isfinite(sigma) or sigma <= 0.0:
        raise ValueError("sigma_mass must be finite and positive")
    if isinstance(quadrature_order, bool) or int(quadrature_order) != quadrature_order:
        raise ValueError("quadrature_order must be an integer")
    order = int(quadrature_order)
    if order < 16 or order > 192:
        raise ValueError("quadrature_order must lie from 16 through 192")
    nodes, weights = np.polynomial.hermite.hermgauss(order)
    masses = mean + sqrt(2.0) * sigma * nodes
    result = np.zeros_like(energy)
    for mass, weight in zip(masses, weights, strict=True):
        levels = homogeneous_reference_eigenvalues(
            grid_points,
            length,
            float(mass),
            hbar_velocity=hbar_velocity,
            boundary=boundary,
        )
        result += float(weight) * gaussian_broadened_dos(
            energy, levels, length, broadening
        )
    return np.asarray(result / sqrt(pi), dtype=float)


def average_homogeneous_gaussian_mixture_dos(
    energies: ArrayLike,
    mean_mass: float,
    sigma_mass: float,
    length: float,
    grid_points: int,
    broadening: float,
    realizations: int,
    *,
    seed: int,
    boundary: BoundaryCondition = "periodic",
    hbar_velocity: float = 1.0,
) -> ScalarFiniteBoxDOS:
    """Monte Carlo finite-box implementation of the matched scalar mixture.

    Each realization draws one spatially homogeneous mass from the declared
    one-point Gaussian distribution.  This is an independent numerical null,
    not a correlated field with a large but finite correlation length.
    """

    energy = np.asarray(energies, dtype=float)
    if energy.ndim != 1 or energy.size == 0 or not np.all(np.isfinite(energy)):
        raise ValueError("energies must be a finite non-empty one-dimensional array")
    mean = float(mean_mass)
    sigma = float(sigma_mass)
    if not isfinite(mean):
        raise ValueError("mean_mass must be finite")
    if not isfinite(sigma) or sigma <= 0.0:
        raise ValueError("sigma_mass must be finite and positive")
    if isinstance(realizations, bool) or int(realizations) != realizations:
        raise ValueError("realizations must be an integer")
    count = int(realizations)
    if count < 2:
        raise ValueError("at least two realizations are required")
    if isinstance(seed, bool) or int(seed) != seed or int(seed) < 0:
        raise ValueError("seed must be a non-negative integer")

    rng = np.random.default_rng(int(seed))
    sampled_masses = rng.normal(mean, sigma, size=count)
    realization_values = np.empty((count, energy.size), dtype=float)
    for index, sampled_mass in enumerate(sampled_masses):
        levels = homogeneous_reference_eigenvalues(
            grid_points,
            length,
            float(sampled_mass),
            hbar_velocity=hbar_velocity,
            boundary=boundary,
        )
        realization_values[index] = gaussian_broadened_dos(
            energy, levels, length, broadening
        )
    return ScalarFiniteBoxDOS(
        energies=_read_only(energy),
        mean_dos=_read_only(np.mean(realization_values, axis=0)),
        standard_error=_read_only(
            np.std(realization_values, axis=0, ddof=1) / sqrt(count)
        ),
        realization_dos=_read_only(realization_values),
        sampled_masses=_read_only(sampled_masses),
        mean_mass=mean,
        sigma_mass=sigma,
        length=float(length),
        grid_points=int(grid_points),
        broadening=float(broadening),
        realizations=count,
        seed=int(seed),
        boundary=boundary,
    )


def average_ensemble_results(results: list[EnsembleDOS]) -> EnsembleDOS:
    """Combine compatible ensembles, for example periodic and antiperiodic batches."""

    if not results:
        raise ValueError("at least one ensemble result is required")
    reference = results[0]
    for result in results[1:]:
        if not np.array_equal(result.energies, reference.energies):
            raise ValueError("ensemble energy grids do not match")
        fields = (
            "mean_mass",
            "sigma_mass",
            "correlation_length",
            "length",
            "grid_points",
            "broadening",
            "covariance_family",
            "remove_sample_mean",
            "normalize_sample_variance",
        )
        for field in fields:
            if getattr(result, field) != getattr(reference, field):
                raise ValueError(f"ensemble field {field} does not match")
    realization_values = np.concatenate([r.realization_dos for r in results], axis=0)
    means = np.concatenate([r.realized_mass_means for r in results])
    sigmas = np.concatenate([r.realized_mass_sigmas for r in results])
    total = realization_values.shape[0]
    return EnsembleDOS(
        energies=reference.energies,
        mean_dos=_read_only(np.mean(realization_values, axis=0)),
        standard_error=_read_only(
            np.std(realization_values, axis=0, ddof=1) / sqrt(total)
        ),
        realization_dos=_read_only(realization_values),
        realized_mass_means=_read_only(means),
        realized_mass_sigmas=_read_only(sigmas),
        mean_mass=reference.mean_mass,
        sigma_mass=reference.sigma_mass,
        correlation_length=reference.correlation_length,
        length=reference.length,
        grid_points=reference.grid_points,
        broadening=reference.broadening,
        realizations=total,
        seed=reference.seed,
        covariance_family=reference.covariance_family,
        boundary="combined",
        remove_sample_mean=reference.remove_sample_mean,
        normalize_sample_variance=reference.normalize_sample_variance,
    )


def gaussian_convolve_uniform_grid(
    energies: ArrayLike,
    values: ArrayLike,
    width: float,
) -> FloatArray:
    """Convolve a uniformly sampled spectrum with a Gaussian using zero padding."""

    energy, spacing = _uniform_energies(energies)
    spectrum = np.asarray(values, dtype=float)
    if spectrum.shape != energy.shape or not np.all(np.isfinite(spectrum)):
        raise ValueError("values must be finite and match energies")
    sigma = _positive("width", width)
    offsets = (np.arange(energy.size) - energy.size // 2) * spacing
    kernel = np.exp(-0.5 * (offsets / sigma) ** 2) / (sqrt(2.0 * pi) * sigma)
    kernel /= float(np.sum(kernel) * spacing)
    full = np.convolve(spectrum, kernel, mode="full") * spacing
    start = (kernel.size - 1) // 2
    return np.asarray(full[start : start + spectrum.size], dtype=float)


def effect_size(
    energies: ArrayLike,
    correlated_dos: ArrayLike,
    scalar_dos: ArrayLike,
    *,
    energy_window: tuple[float, float] = (-1.0, 1.0),
    integrated_regularization: float = 1.0e-12,
    point_regularization_fraction: float = 0.05,
) -> EffectSize:
    """Return the predeclared integrated and maximum relative DOS differences."""

    energy = np.asarray(energies, dtype=float)
    correlated = np.asarray(correlated_dos, dtype=float)
    scalar = np.asarray(scalar_dos, dtype=float)
    if energy.ndim != 1 or correlated.shape != energy.shape or scalar.shape != energy.shape:
        raise ValueError("energy and DOS arrays must be matching one-dimensional arrays")
    if (
        not np.all(np.isfinite(energy))
        or not np.all(np.isfinite(correlated))
        or not np.all(np.isfinite(scalar))
    ):
        raise ValueError("energy and DOS arrays must be finite")
    if np.any(correlated < 0.0) or np.any(scalar < 0.0):
        raise ValueError("DOS arrays must be non-negative")
    lower, upper = map(float, energy_window)
    if not isfinite(lower) or not isfinite(upper) or lower >= upper:
        raise ValueError("energy_window must be finite and ordered")
    mask = (energy >= lower) & (energy <= upper)
    if np.count_nonzero(mask) < 3:
        raise ValueError("energy_window contains too few grid points")
    selected_energy = energy[mask]
    selected_correlated = correlated[mask]
    selected_scalar = scalar[mask]
    difference = np.abs(selected_correlated - selected_scalar)
    reference_integral = _trapezoid(selected_scalar, selected_energy)
    difference_integral = _trapezoid(difference, selected_energy)
    epsilon_1 = float(integrated_regularization) * max(
        reference_integral, np.finfo(float).tiny
    )
    maximum_reference = float(np.max(selected_scalar))
    epsilon_infinity = float(point_regularization_fraction) * max(
        maximum_reference, np.finfo(float).tiny
    )
    delta_1 = difference_integral / (reference_integral + epsilon_1)
    delta_infinity = float(np.max(difference / (selected_scalar + epsilon_infinity)))
    return EffectSize(
        delta_1=float(delta_1),
        delta_infinity=delta_infinity,
        integrated_reference=reference_integral,
        maximum_reference=maximum_reference,
        energy_minimum=lower,
        energy_maximum=upper,
    )