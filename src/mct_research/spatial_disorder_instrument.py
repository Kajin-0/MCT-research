"""Composite instrument-kernel diagnostics for spatially correlated disorder.

The declared instrument model is separable:

* an axis-aligned elliptical Gaussian optical point-spread function;
* rectangular pixel or scan-bin integration in the specimen plane;
* normalized exponential depth weighting in a finite slab.

For separable Gaussian material covariance, the lateral factors are analytical.
The finite-depth factor reuses the deterministic depth quadrature established in
:mod:`mct_research.spatial_disorder_depth`.

This module does not assert that any particular HgCdTe instrument has this PSF,
that one equivalent Gaussian width is universally valid, or that a specimen
correlation length has been measured.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, hypot, isfinite, log, sqrt
from typing import ClassVar

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder import GaussianCovariance
from .spatial_disorder_depth import (
    ExponentialDepthKernel,
    finite_slab_depth_effective_variance,
)
from .spatial_disorder_theorems import top_hat_gaussian_effective_variance_1d

FloatArray = NDArray[np.float64]


def _finite_positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _finite_nonnegative_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


def _validated_quadrature_order(order: int) -> int:
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)):
        raise ValueError("quadrature_order must be an integer")
    result = int(order)
    if result < 2 or result > 2048:
        raise ValueError("quadrature_order must lie between 2 and 2048")
    return result


def _read_only_float(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _validated_log_covariance(value: ArrayLike, dimension: int) -> FloatArray:
    matrix = np.array(value, dtype=float, copy=True)
    if matrix.shape != (dimension, dimension):
        raise ValueError(
            f"parameter_log_covariance must have shape ({dimension}, {dimension})"
        )
    if not np.all(np.isfinite(matrix)):
        raise ValueError("parameter_log_covariance must contain only finite values")
    scale = max(1.0, float(np.linalg.norm(matrix, ord=np.inf)))
    if not np.allclose(matrix, matrix.T, rtol=1.0e-12, atol=1.0e-14 * scale):
        raise ValueError("parameter_log_covariance must be symmetric")
    eigenvalues = np.linalg.eigvalsh(matrix)
    tolerance = 128.0 * np.finfo(float).eps * max(
        1.0,
        scale,
        float(np.max(np.abs(eigenvalues))),
    )
    if float(np.min(eigenvalues)) < -tolerance:
        raise ValueError("parameter_log_covariance must be positive semidefinite")
    matrix.setflags(write=False)
    return matrix


@dataclass(frozen=True)
class CompositeInstrumentKernel:
    """Separable PSF, pixel, and finite-depth measurement kernel.

    All lateral lengths and slab thickness must use one consistent length unit.
    ``attenuation_coefficient`` must use the reciprocal unit.
    """

    psf_sigma_x: float
    psf_sigma_y: float
    pixel_width_x: float
    pixel_width_y: float
    attenuation_coefficient: float
    thickness: float
    side: str = "front"

    log_parameter_names: ClassVar[tuple[str, ...]] = (
        "psf_sigma_x",
        "psf_sigma_y",
        "pixel_width_x",
        "pixel_width_y",
        "attenuation_coefficient",
        "thickness",
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "psf_sigma_x",
            _finite_nonnegative_scalar("psf_sigma_x", self.psf_sigma_x),
        )
        object.__setattr__(
            self,
            "psf_sigma_y",
            _finite_nonnegative_scalar("psf_sigma_y", self.psf_sigma_y),
        )
        object.__setattr__(
            self,
            "pixel_width_x",
            _finite_nonnegative_scalar("pixel_width_x", self.pixel_width_x),
        )
        object.__setattr__(
            self,
            "pixel_width_y",
            _finite_nonnegative_scalar("pixel_width_y", self.pixel_width_y),
        )
        object.__setattr__(
            self,
            "attenuation_coefficient",
            _finite_positive_scalar(
                "attenuation_coefficient", self.attenuation_coefficient
            ),
        )
        object.__setattr__(
            self,
            "thickness",
            _finite_positive_scalar("thickness", self.thickness),
        )
        if self.side not in ("front", "back"):
            raise ValueError("side must be 'front' or 'back'")

    @property
    def moment_matched_sigma_x(self) -> float:
        return float(hypot(self.psf_sigma_x, self.pixel_width_x / sqrt(12.0)))

    @property
    def moment_matched_sigma_y(self) -> float:
        return float(hypot(self.psf_sigma_y, self.pixel_width_y / sqrt(12.0)))

    def with_log_perturbation(self, index: int, delta: float) -> CompositeInstrumentKernel:
        if isinstance(index, bool) or not isinstance(index, (int, np.integer)):
            raise ValueError("index must identify one instrument log parameter")
        parameter_index = int(index)
        if parameter_index < 0 or parameter_index >= len(self.log_parameter_names):
            raise ValueError("index must identify one instrument log parameter")
        shift = float(delta)
        if not isfinite(shift):
            raise ValueError("delta must be finite")
        values = [
            self.psf_sigma_x,
            self.psf_sigma_y,
            self.pixel_width_x,
            self.pixel_width_y,
            self.attenuation_coefficient,
            self.thickness,
        ]
        if values[parameter_index] == 0.0:
            raise ValueError(
                f"{self.log_parameter_names[parameter_index]} must be positive "
                "for log-parameter perturbation"
            )
        values[parameter_index] *= exp(shift)
        return CompositeInstrumentKernel(*values, side=self.side)


def gaussian_psf_rectangular_pixel_axis_ratio(
    correlation_length: float,
    psf_sigma: float,
    pixel_width: float,
) -> float:
    r"""Return the exact one-axis Gaussian-PSF plus rectangular-pixel ratio.

    Let the material covariance be ``exp(-h**2/(2 xi**2))``. Two independent
    Gaussian PSF samples differ by a zero-mean Gaussian with variance
    ``2 sigma**2``. Conditional on the triangular rectangular-pixel difference,
    Gaussian integration produces an enlarged correlation scale

    ``L = sqrt(xi**2 + 2 sigma**2)``

    and prefactor ``xi/L``. The remaining triangular integral is exactly the
    established one-dimensional top-hat/Gaussian-covariance ratio at scale ``L``.
    """

    xi = _finite_positive_scalar("correlation_length", correlation_length)
    sigma = _finite_nonnegative_scalar("psf_sigma", psf_sigma)
    width = _finite_nonnegative_scalar("pixel_width", pixel_width)
    enlarged = hypot(xi, sqrt(2.0) * sigma)
    gaussian_ratio = xi / enlarged
    if width == 0.0:
        return float(gaussian_ratio)
    pixel_ratio = top_hat_gaussian_effective_variance_1d(
        1.0,
        enlarged,
        width,
    )
    ratio = gaussian_ratio * pixel_ratio
    tolerance = 256.0 * np.finfo(float).eps
    if not 0.0 < ratio <= 1.0 + tolerance:
        raise RuntimeError("lateral attenuation left its physical interval")
    return float(min(ratio, 1.0))


def gaussian_psf_rectangular_pixel_axis_ratio_quadrature(
    correlation_length: float,
    psf_sigma: float,
    pixel_width: float,
    *,
    quadrature_order: int = 96,
) -> float:
    """Independently evaluate the one-axis ratio by triangular quadrature."""

    xi = _finite_positive_scalar("correlation_length", correlation_length)
    sigma = _finite_nonnegative_scalar("psf_sigma", psf_sigma)
    width = _finite_nonnegative_scalar("pixel_width", pixel_width)
    order = _validated_quadrature_order(quadrature_order)
    enlarged = hypot(xi, sqrt(2.0) * sigma)
    gaussian_ratio = xi / enlarged
    if width == 0.0:
        return float(gaussian_ratio)

    nodes, weights = np.polynomial.legendre.leggauss(order)
    displacement = 0.5 * width * (nodes + 1.0)
    integration_weights = 0.5 * width * weights
    triangular_density_twice = 2.0 * (width - displacement) / width**2
    conditional = np.exp(-0.5 * (displacement / enlarged) ** 2)
    result = gaussian_ratio * float(
        np.dot(integration_weights, triangular_density_twice * conditional)
    )
    if not 0.0 < result <= 1.0 + 1024.0 * np.finfo(float).eps:
        raise RuntimeError("quadrature attenuation left its physical interval")
    return float(min(result, 1.0))


def moment_matched_gaussian_axis_ratio(
    correlation_length: float,
    psf_sigma: float,
    pixel_width: float,
) -> float:
    """Return the Gaussian approximation using the kernel's second moment."""

    xi = _finite_positive_scalar("correlation_length", correlation_length)
    sigma = _finite_nonnegative_scalar("psf_sigma", psf_sigma)
    width = _finite_nonnegative_scalar("pixel_width", pixel_width)
    equivalent_variance = sigma**2 + width**2 / 12.0
    return float(xi / sqrt(xi**2 + 2.0 * equivalent_variance))


@dataclass(frozen=True)
class CompositeInstrumentVariance:
    """Exact-lateral and moment-matched composite-kernel variance result."""

    point_variance: float
    correlation_lengths: FloatArray
    kernel: CompositeInstrumentKernel
    lateral_ratio_x: float
    lateral_ratio_y: float
    depth_ratio: float
    exact_variance_ratio: float
    effective_variance: float
    moment_matched_sigma_x: float
    moment_matched_sigma_y: float
    equivalent_gaussian_variance_ratio: float
    equivalent_gaussian_effective_variance: float
    equivalent_gaussian_relative_error: float


def composite_instrument_effective_variance(
    point_variance: float,
    correlation_lengths: ArrayLike,
    kernel: CompositeInstrumentKernel,
    *,
    depth_quadrature_order: int = 96,
) -> CompositeInstrumentVariance:
    """Return variance filtered by the declared separable 3D instrument kernel."""

    variance = _finite_positive_scalar("point_variance", point_variance)
    lengths = np.array(correlation_lengths, dtype=float, copy=True)
    if lengths.shape != (3,):
        raise ValueError("correlation_lengths must have shape (3,)")
    if not np.all(np.isfinite(lengths)) or np.any(lengths <= 0.0):
        raise ValueError("correlation_lengths must be finite and positive")
    if not isinstance(kernel, CompositeInstrumentKernel):
        raise TypeError("kernel must be a CompositeInstrumentKernel")
    order = _validated_quadrature_order(depth_quadrature_order)

    lateral_x = gaussian_psf_rectangular_pixel_axis_ratio(
        float(lengths[0]),
        kernel.psf_sigma_x,
        kernel.pixel_width_x,
    )
    lateral_y = gaussian_psf_rectangular_pixel_axis_ratio(
        float(lengths[1]),
        kernel.psf_sigma_y,
        kernel.pixel_width_y,
    )
    depth_covariance = GaussianCovariance.isotropic(
        1.0,
        float(lengths[2]),
        1,
    )
    depth_kernel = ExponentialDepthKernel(
        kernel.attenuation_coefficient,
        kernel.thickness,
        side=kernel.side,
    )
    depth_ratio = finite_slab_depth_effective_variance(
        depth_covariance,
        depth_kernel,
        quadrature_order=order,
    )
    exact_ratio = lateral_x * lateral_y * depth_ratio

    equivalent_x = moment_matched_gaussian_axis_ratio(
        float(lengths[0]),
        kernel.psf_sigma_x,
        kernel.pixel_width_x,
    )
    equivalent_y = moment_matched_gaussian_axis_ratio(
        float(lengths[1]),
        kernel.psf_sigma_y,
        kernel.pixel_width_y,
    )
    equivalent_ratio = equivalent_x * equivalent_y * depth_ratio
    relative_error = equivalent_ratio / exact_ratio - 1.0

    lengths.setflags(write=False)
    return CompositeInstrumentVariance(
        point_variance=variance,
        correlation_lengths=lengths,
        kernel=kernel,
        lateral_ratio_x=float(lateral_x),
        lateral_ratio_y=float(lateral_y),
        depth_ratio=float(depth_ratio),
        exact_variance_ratio=float(exact_ratio),
        effective_variance=float(variance * exact_ratio),
        moment_matched_sigma_x=kernel.moment_matched_sigma_x,
        moment_matched_sigma_y=kernel.moment_matched_sigma_y,
        equivalent_gaussian_variance_ratio=float(equivalent_ratio),
        equivalent_gaussian_effective_variance=float(variance * equivalent_ratio),
        equivalent_gaussian_relative_error=float(relative_error),
    )


@dataclass(frozen=True)
class InstrumentCalibrationPropagation:
    """First-order propagation of instrument log-parameter uncertainty."""

    parameter_names: tuple[str, ...]
    log_sensitivity: FloatArray
    parameter_log_covariance: FloatArray
    log_variance_variance: float
    log_variance_standard_deviation: float
    first_order_relative_standard_deviation: float
    lognormal_relative_standard_deviation: float


def composite_instrument_log_sensitivity(
    correlation_lengths: ArrayLike,
    kernel: CompositeInstrumentKernel,
    *,
    log_step: float = 1.0e-5,
    depth_quadrature_order: int = 96,
) -> FloatArray:
    """Return central-difference derivatives of log variance ratio.

    The derivative vector follows ``CompositeInstrumentKernel.log_parameter_names``.
    The routine differentiates only instrument calibration parameters; material
    correlation lengths and covariance-family uncertainty remain separate.
    """

    step = _finite_positive_scalar("log_step", log_step)
    if step > 0.1:
        raise ValueError("log_step must not exceed 0.1")
    base_lengths = np.asarray(correlation_lengths, dtype=float)
    if base_lengths.shape != (3,):
        raise ValueError("correlation_lengths must have shape (3,)")
    if not np.all(np.isfinite(base_lengths)) or np.any(base_lengths <= 0.0):
        raise ValueError("correlation_lengths must be finite and positive")
    if not isinstance(kernel, CompositeInstrumentKernel):
        raise TypeError("kernel must be a CompositeInstrumentKernel")

    derivatives: list[float] = []
    for index in range(len(kernel.log_parameter_names)):
        plus_kernel = kernel.with_log_perturbation(index, step)
        minus_kernel = kernel.with_log_perturbation(index, -step)
        plus = composite_instrument_effective_variance(
            1.0,
            base_lengths,
            plus_kernel,
            depth_quadrature_order=depth_quadrature_order,
        ).exact_variance_ratio
        minus = composite_instrument_effective_variance(
            1.0,
            base_lengths,
            minus_kernel,
            depth_quadrature_order=depth_quadrature_order,
        ).exact_variance_ratio
        derivatives.append((log(plus) - log(minus)) / (2.0 * step))
    return _read_only_float(derivatives)


def propagate_composite_instrument_calibration(
    correlation_lengths: ArrayLike,
    kernel: CompositeInstrumentKernel,
    parameter_log_covariance: ArrayLike,
    *,
    log_step: float = 1.0e-5,
    depth_quadrature_order: int = 96,
) -> InstrumentCalibrationPropagation:
    """Propagate a declared instrument log-parameter covariance to log variance."""

    covariance = _validated_log_covariance(
        parameter_log_covariance,
        len(CompositeInstrumentKernel.log_parameter_names),
    )
    sensitivity = composite_instrument_log_sensitivity(
        correlation_lengths,
        kernel,
        log_step=log_step,
        depth_quadrature_order=depth_quadrature_order,
    )
    propagated = float(sensitivity @ np.asarray(covariance) @ sensitivity)
    tolerance = 1024.0 * np.finfo(float).eps * max(1.0, abs(propagated))
    if propagated < -tolerance:
        raise RuntimeError("propagated log-variance variance became negative")
    propagated = max(0.0, propagated)
    standard_deviation = sqrt(propagated)
    lognormal_relative = sqrt(expm1(propagated)) if propagated > 0.0 else 0.0
    return InstrumentCalibrationPropagation(
        parameter_names=CompositeInstrumentKernel.log_parameter_names,
        log_sensitivity=sensitivity,
        parameter_log_covariance=covariance,
        log_variance_variance=float(propagated),
        log_variance_standard_deviation=float(standard_deviation),
        first_order_relative_standard_deviation=float(standard_deviation),
        lognormal_relative_standard_deviation=float(lognormal_relative),
    )
