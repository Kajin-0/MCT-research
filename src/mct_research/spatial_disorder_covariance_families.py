"""Covariance-family checks for multiscale spatial-disorder measurements.

The Gaussian covariance/Gaussian probe benchmark in two lateral dimensions is

``V(s) = A / (1 + 2 s**2 / xi**2)``.

Its reciprocal is exactly affine in ``s**2``.  Two admissible scales therefore
identify two Gaussian parameters but cannot test the covariance family; a third
scale supplies the first exact lack-of-fit check.

This module also evaluates Gaussian-probe filtering for the standard
half-integer Matérn families ``nu = 1/2, 3/2, 5/2`` without adding SciPy.  The
results are model-conditioned experiment-design diagnostics, not specimen
covariance estimates.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import erfc, exp, gamma, isfinite, pi, sqrt

import numpy as np
from numpy.polynomial.laguerre import laggauss
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder_inference import gaussian_multiscale_variance
from .spatial_disorder_theorems import recover_isotropic_gaussian_two_scales

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]
SUPPORTED_MATERN_SMOOTHNESS = (0.5, 1.5, 2.5)


@dataclass(frozen=True)
class GaussianThreeScaleFalsification:
    """Exact endpoint-interpolation check for three ordered probe scales."""

    probe_sigmas: FloatArray
    observed_variances: FloatArray
    reciprocal_variances: FloatArray
    reciprocal_second_divided_difference: float
    reciprocal_middle_residual: float
    endpoint_predicted_middle_variance: float
    middle_relative_prediction_error: float
    residual_standard_deviation: float | None
    standardized_reciprocal_residual: float | None
    endpoint_fitted_point_variance: float
    endpoint_fitted_correlation_length: float


@dataclass(frozen=True)
class GaussianReciprocalLinearityFit:
    """Weighted affine fit of reciprocal variance against squared scale."""

    probe_sigmas: FloatArray
    observed_variances: FloatArray
    variance_standard_deviations: FloatArray | None
    reciprocal_variances: FloatArray
    reciprocal_standard_deviations: FloatArray | None
    intercept: float
    slope: float
    fitted_point_variance: float
    fitted_correlation_length: float
    fitted_variances: FloatArray
    reciprocal_residuals: FloatArray
    relative_variance_residuals: FloatArray
    maximum_absolute_relative_variance_residual: float
    weighted_rms_reciprocal_residual: float
    chi_square: float | None
    degrees_of_freedom: int
    reduced_chi_square: float | None
    coefficient_covariance: FloatMatrix | None


def _read_only(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _positive_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _nonnegative_scalar(name: str, value: float) -> float:
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return result


def _validated_smoothness(smoothness: float) -> float:
    value = float(smoothness)
    if value not in SUPPORTED_MATERN_SMOOTHNESS:
        raise ValueError(
            "smoothness must be one of "
            f"{SUPPORTED_MATERN_SMOOTHNESS}"
        )
    return value


def _validated_scales_and_variances(
    probe_sigmas: ArrayLike,
    variances: ArrayLike,
    *,
    minimum_count: int,
) -> tuple[FloatArray, FloatArray]:
    scales = np.asarray(probe_sigmas, dtype=float)
    values = np.asarray(variances, dtype=float)
    if scales.ndim != 1 or values.ndim != 1 or scales.shape != values.shape:
        raise ValueError("probe_sigmas and variances must be matching one-dimensional arrays")
    if scales.size < minimum_count:
        raise ValueError(f"at least {minimum_count} scales are required")
    if not np.all(np.isfinite(scales)) or np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be finite and non-negative")
    if not np.all(np.isfinite(values)) or np.any(values <= 0.0):
        raise ValueError("variances must be finite and positive")
    if np.unique(scales).size != scales.size:
        raise ValueError("probe_sigmas must be distinct")
    order = np.argsort(scales)
    return _read_only(scales[order]), _read_only(values[order])


def matern_half_integer_correlation(
    distance: ArrayLike,
    correlation_length: float,
    smoothness: float,
) -> FloatArray:
    r"""Return the normalized half-integer Matérn correlation.

    The parameterization is

    .. math::

       \rho_\nu(r)=\frac{2^{1-\nu}}{\Gamma(\nu)}
       z^\nu K_\nu(z),\qquad
       z=\sqrt{2\nu}\,r/\ell.

    For the supported half-integer values this reduces to an exponential times
    a finite polynomial.
    """

    xi = _positive_scalar("correlation_length", correlation_length)
    nu = _validated_smoothness(smoothness)
    distances = np.asarray(distance, dtype=float)
    if not np.all(np.isfinite(distances)) or np.any(distances < 0.0):
        raise ValueError("distance must contain only finite non-negative values")
    z = sqrt(2.0 * nu) * distances / xi
    if nu == 0.5:
        polynomial = np.ones_like(z)
    elif nu == 1.5:
        polynomial = 1.0 + z
    else:
        polynomial = 1.0 + z + z * z / 3.0
    return _read_only(polynomial * np.exp(-z))


@lru_cache(maxsize=8)
def _laguerre_rule(order: int) -> tuple[FloatArray, FloatArray]:
    if isinstance(order, bool) or int(order) != order or not 16 <= int(order) <= 128:
        raise ValueError("quadrature_order must be an integer from 16 through 128")
    nodes, weights = laggauss(int(order))
    return _read_only(nodes), _read_only(weights)


def _small_rho_closed_form(rho: float, smoothness: float) -> float:
    """Evaluate the exact half-integer attenuation before cancellation dominates."""

    scaled_complement = sqrt(pi) * exp(rho * rho) * erfc(rho)
    if smoothness == 0.5:
        return 1.0 - rho * scaled_complement
    if smoothness == 1.5:
        return 1.0 - 2.0 * rho**2 + 2.0 * rho**3 * scaled_complement
    return (
        1.0
        - (2.0 / 3.0) * rho**2
        + (4.0 / 3.0) * rho**4
        - (4.0 / 3.0) * rho**5 * scaled_complement
    )


def matern_gaussian_probe_attenuation_2d(
    probe_sigma: float,
    correlation_length: float,
    smoothness: float,
    *,
    quadrature_order: int = 96,
) -> float:
    r"""Return ``Var(X_s)/A`` for a 2D Gaussian probe and Matérn covariance.

    If ``R`` is the distance between two independent coordinates drawn from a
    two-dimensional Gaussian probe of coordinate standard deviation ``s``, then

    .. math::

       \operatorname{Var}(X_s)/A=\mathbb E[\rho_\nu(R)].

    For half-integer Matérn covariance, define
    ``rho = sqrt(2*nu) * s / ell``.  Small ``rho`` uses exact closed forms.  At
    larger ``rho`` an equivalent Gauss--Laguerre representation avoids severe
    cancellation while retaining binary64 accuracy over the design range.
    """

    scale = _nonnegative_scalar("probe_sigma", probe_sigma)
    xi = _positive_scalar("correlation_length", correlation_length)
    nu = _validated_smoothness(smoothness)
    if scale == 0.0:
        return 1.0
    ratio = scale / xi
    if not isfinite(ratio):
        raise ValueError("probe_sigma/correlation_length must be finite")
    rho = sqrt(2.0 * nu) * ratio

    if rho < 0.5:
        result = _small_rho_closed_form(rho, nu)
    else:
        nodes, weights = _laguerre_rule(quadrature_order)
        if nu == 0.5:
            polynomial = np.ones_like(nodes)
        elif nu == 1.5:
            polynomial = 1.0 + nodes
        else:
            polynomial = 1.0 + nodes + nodes * nodes / 3.0
        attenuation = (
            np.asarray(weights)
            * np.asarray(nodes)
            * polynomial
            * np.exp(-np.asarray(nodes) ** 2 / (4.0 * rho * rho))
        )
        result = float(np.sum(attenuation) / (2.0 * rho * rho))

    if not isfinite(result) or result <= 0.0 or result > 1.0 + 2.0e-12:
        raise ArithmeticError("Matérn probe attenuation left its physical interval")
    return min(result, 1.0)


def matern_gaussian_probe_variance_2d(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
    smoothness: float,
    *,
    quadrature_order: int = 96,
) -> FloatArray:
    """Return filtered variance for one supported Matérn covariance family."""

    variance = _positive_scalar("point_variance", point_variance)
    xi = _positive_scalar("correlation_length", correlation_length)
    nu = _validated_smoothness(smoothness)
    scales = np.asarray(probe_sigmas, dtype=float)
    if scales.ndim != 1 or scales.size == 0:
        raise ValueError("probe_sigmas must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(scales)) or np.any(scales < 0.0):
        raise ValueError("probe_sigmas must be finite and non-negative")
    values = [
        variance
        * matern_gaussian_probe_attenuation_2d(
            float(scale),
            xi,
            nu,
            quadrature_order=quadrature_order,
        )
        for scale in scales
    ]
    return _read_only(values)


def gaussian_three_scale_falsification(
    probe_sigmas: ArrayLike,
    variances: ArrayLike,
    *,
    variance_standard_deviations: ArrayLike | None = None,
) -> GaussianThreeScaleFalsification:
    r"""Test the exact Gaussian reciprocal-linearity identity at three scales.

    The scales are sorted internally.  The endpoint scales determine a unique
    admissible Gaussian model.  The middle scale is then a model check rather
    than another parameter-estimation datum.
    """

    scales, values = _validated_scales_and_variances(
        probe_sigmas,
        variances,
        minimum_count=3,
    )
    if scales.size != 3:
        raise ValueError("exactly three scales are required")
    x = np.asarray(scales) ** 2
    y = 1.0 / np.asarray(values)
    first_slope = (y[1] - y[0]) / (x[1] - x[0])
    second_slope = (y[2] - y[1]) / (x[2] - x[1])
    curvature = float(second_slope - first_slope)
    interpolation_fraction = float((x[1] - x[0]) / (x[2] - x[0]))
    predicted_reciprocal = float(
        (1.0 - interpolation_fraction) * y[0]
        + interpolation_fraction * y[2]
    )
    if predicted_reciprocal <= 0.0:
        raise ValueError("endpoint interpolation predicts a non-positive variance")
    predicted_middle = 1.0 / predicted_reciprocal
    reciprocal_residual = float(y[1] - predicted_reciprocal)
    relative_error = float((predicted_middle - values[1]) / values[1])

    recovery = recover_isotropic_gaussian_two_scales(
        float(values[0]),
        float(values[2]),
        float(scales[0]),
        float(scales[2]),
        dimension=2,
    )

    if variance_standard_deviations is None:
        residual_standard_deviation = None
        standardized_residual = None
    else:
        standard_deviations = np.asarray(variance_standard_deviations, dtype=float)
        if standard_deviations.shape != (3,):
            raise ValueError("variance_standard_deviations must have shape (3,)")
        if not np.all(np.isfinite(standard_deviations)) or np.any(
            standard_deviations <= 0.0
        ):
            raise ValueError(
                "variance_standard_deviations must be finite and positive"
            )
        order = np.argsort(np.asarray(probe_sigmas, dtype=float))
        standard_deviations = standard_deviations[order]
        reciprocal_standard_deviations = standard_deviations / np.asarray(values) ** 2
        residual_standard_deviation = float(
            sqrt(
                reciprocal_standard_deviations[1] ** 2
                + (1.0 - interpolation_fraction) ** 2
                * reciprocal_standard_deviations[0] ** 2
                + interpolation_fraction**2
                * reciprocal_standard_deviations[2] ** 2
            )
        )
        standardized_residual = reciprocal_residual / residual_standard_deviation

    return GaussianThreeScaleFalsification(
        probe_sigmas=scales,
        observed_variances=values,
        reciprocal_variances=_read_only(y),
        reciprocal_second_divided_difference=curvature,
        reciprocal_middle_residual=reciprocal_residual,
        endpoint_predicted_middle_variance=predicted_middle,
        middle_relative_prediction_error=relative_error,
        residual_standard_deviation=residual_standard_deviation,
        standardized_reciprocal_residual=standardized_residual,
        endpoint_fitted_point_variance=recovery.point_variance,
        endpoint_fitted_correlation_length=recovery.correlation_length,
    )


def gaussian_reciprocal_linearity_fit(
    probe_sigmas: ArrayLike,
    variances: ArrayLike,
    *,
    variance_standard_deviations: ArrayLike | None = None,
) -> GaussianReciprocalLinearityFit:
    r"""Fit the Gaussian family through reciprocal linearity.

    The fitted model is

    .. math::

       1/V=\alpha+\beta s^2,
       \quad A=1/\alpha,
       \quad \xi=\sqrt{2\alpha/\beta}.

    With supplied variance standard deviations, first-order propagation gives
    ``sigma_(1/V) = sigma_V/V**2`` and the routine reports chi-square lack of
    fit with ``N-2`` degrees of freedom.
    """

    scales, values = _validated_scales_and_variances(
        probe_sigmas,
        variances,
        minimum_count=2,
    )
    original_scales = np.asarray(probe_sigmas, dtype=float)
    order = np.argsort(original_scales)
    x = np.asarray(scales) ** 2
    y = 1.0 / np.asarray(values)
    design = np.column_stack((np.ones(scales.size), x))

    if variance_standard_deviations is None:
        reciprocal_standard_deviations = None
        whitened_design = design
        whitened_values = y
    else:
        standard_deviations = np.asarray(variance_standard_deviations, dtype=float)
        if standard_deviations.shape != values.shape:
            raise ValueError(
                "variance_standard_deviations must match the variance array"
            )
        if not np.all(np.isfinite(standard_deviations)) or np.any(
            standard_deviations <= 0.0
        ):
            raise ValueError(
                "variance_standard_deviations must be finite and positive"
            )
        standard_deviations = standard_deviations[order]
        reciprocal_standard_deviations = standard_deviations / np.asarray(values) ** 2
        whitened_design = design / reciprocal_standard_deviations[:, None]
        whitened_values = y / reciprocal_standard_deviations

    coefficients, _, rank, _ = np.linalg.lstsq(
        whitened_design,
        whitened_values,
        rcond=None,
    )
    if rank != 2:
        raise ValueError("probe-scale design is rank deficient")
    intercept, slope = map(float, coefficients)
    if intercept <= 0.0 or slope <= 0.0:
        raise ValueError(
            "best reciprocal line does not correspond to positive Gaussian parameters"
        )
    point_variance = 1.0 / intercept
    correlation_length = sqrt(2.0 * intercept / slope)
    fitted_reciprocal = design @ coefficients
    if np.any(fitted_reciprocal <= 0.0):
        raise ValueError("fitted reciprocal variance is non-positive")
    fitted_variances = 1.0 / fitted_reciprocal
    reciprocal_residuals = y - fitted_reciprocal
    relative_residuals = (fitted_variances - np.asarray(values)) / np.asarray(values)
    degrees_of_freedom = int(scales.size - 2)

    if reciprocal_standard_deviations is None:
        weighted_rms = float(sqrt(np.mean(reciprocal_residuals**2)))
        chi_square = None
        reduced_chi_square = None
        coefficient_covariance = None
        variance_standard_deviations_result = None
        reciprocal_standard_deviations_result = None
    else:
        normalized = reciprocal_residuals / reciprocal_standard_deviations
        chi_square = float(normalized @ normalized)
        reduced_chi_square = (
            chi_square / degrees_of_freedom if degrees_of_freedom > 0 else None
        )
        weighted_rms = float(sqrt(np.mean(normalized**2)))
        information = whitened_design.T @ whitened_design
        coefficient_covariance = _read_only(np.linalg.inv(information))
        variance_standard_deviations_result = _read_only(standard_deviations)
        reciprocal_standard_deviations_result = _read_only(
            reciprocal_standard_deviations
        )

    return GaussianReciprocalLinearityFit(
        probe_sigmas=scales,
        observed_variances=values,
        variance_standard_deviations=variance_standard_deviations_result,
        reciprocal_variances=_read_only(y),
        reciprocal_standard_deviations=reciprocal_standard_deviations_result,
        intercept=intercept,
        slope=slope,
        fitted_point_variance=point_variance,
        fitted_correlation_length=correlation_length,
        fitted_variances=_read_only(fitted_variances),
        reciprocal_residuals=_read_only(reciprocal_residuals),
        relative_variance_residuals=_read_only(relative_residuals),
        maximum_absolute_relative_variance_residual=float(
            np.max(np.abs(relative_residuals))
        ),
        weighted_rms_reciprocal_residual=weighted_rms,
        chi_square=chi_square,
        degrees_of_freedom=degrees_of_freedom,
        reduced_chi_square=reduced_chi_square,
        coefficient_covariance=coefficient_covariance,
    )


def gaussian_reference_variance(
    point_variance: float,
    correlation_length: float,
    probe_sigmas: ArrayLike,
) -> FloatArray:
    """Expose the exact Gaussian benchmark beside the alternative families."""

    return gaussian_multiscale_variance(
        point_variance,
        correlation_length,
        probe_sigmas,
    )
