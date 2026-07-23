"""Restricted real-semiconductor map demonstration for R04.

The functions in this module operate on one source-data-derived spatial field and
on added numerical Gaussian kernels.  They do not deconvolve the unknown native
instrument kernel, identify a physical material correlation length, or turn
numerically smoothed maps into independent measurements.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, exp, isfinite, log, sqrt
from pathlib import Path
import csv
from typing import Callable, Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .spatial_disorder import GaussianCovariance
from .spatial_disorder_covariance_families import (
    gaussian_reciprocal_linearity_fit,
    matern_gaussian_probe_attenuation_2d,
)
from .spatial_disorder_multiscale_map import (
    gaussian_multiscale_map_covariance_blocks,
    gaussian_multiscale_map_fisher_comparison,
    gaussian_multiscale_map_variance_statistics,
)

FloatArray = NDArray[np.float64]
FloatMatrix = NDArray[np.float64]


@dataclass(frozen=True)
class SourceMap:
    """Parsed rectangular source-data map and physical coordinate axes."""

    x: FloatArray
    y: FloatArray
    values: FloatMatrix
    note: str


@dataclass(frozen=True)
class FamilyFit:
    """Descriptive covariance-family fit to a numerical smoothing curve."""

    family: str
    point_variance: float
    correlation_scale_pixels: float
    predicted_variances: FloatArray
    training_log_rms: float
    held_out_signed_relative_error: float
    held_out_absolute_relative_error: float


@dataclass(frozen=True)
class RealMapAnalysis:
    """Complete restricted result for one source-data-derived field."""

    scales_pixels: FloatArray
    scales_micrometre: FloatArray
    source_mean: float
    source_sample_variance: float
    primary_variances: FloatArray
    wrap_variances: FloatArray
    nearest_variances: FloatArray
    crop_variances: FloatArray
    planar_detrended_variances: FloatArray
    family_fits: tuple[FamilyFit, ...]
    reciprocal_fit_point_variance: float
    reciprocal_fit_correlation_scale_pixels: float
    reciprocal_fit_maximum_relative_residual: float
    gaussian_bias_factors: FloatArray
    gaussian_log_variance_covariance: FloatMatrix
    gaussian_cross_scale_correlation: FloatMatrix
    gaussian_effective_degrees_of_freedom: FloatArray
    gaussian_parameter_sd_inflation: FloatArray
    gaussian_parameter_covariance_determinant_inflation: float
    surrogate_mean_residual: float
    surrogate_variance_relative_residual: float
    surrogate_wrap_variance_maximum_relative_residual: float
    surrogate_reflect_variances: FloatArray


def _read_only(value: ArrayLike) -> FloatArray:
    result = np.array(value, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _validated_field(field: ArrayLike) -> FloatMatrix:
    result = np.asarray(field, dtype=float)
    if result.ndim != 2 or min(result.shape) < 2:
        raise ValueError("field must be a two-dimensional array with at least 2 x 2 cells")
    if not np.all(np.isfinite(result)):
        raise ValueError("field must contain only finite values")
    return np.asarray(_read_only(result))


def _validated_scales(scales: ArrayLike) -> FloatArray:
    result = np.asarray(scales, dtype=float)
    if result.ndim != 1 or result.size < 3:
        raise ValueError("scales must contain at least three values")
    if not np.all(np.isfinite(result)) or np.any(result < 0.0):
        raise ValueError("scales must be finite and non-negative")
    if np.unique(result).size != result.size:
        raise ValueError("scales must be distinct")
    if np.any(np.diff(result) <= 0.0):
        raise ValueError("scales must be strictly increasing")
    return _read_only(result)


def read_bowman_map_csv(path: str | Path) -> SourceMap:
    """Parse a Bowman et al. source-data map with coordinate row and column.

    The declared archive format contains a note row, a blank row, an x-coordinate
    row, and then one y coordinate followed by map values on every remaining row.
    The parser fails closed on any nonrectangular, nonfinite, or nonmonotone map.
    """

    source = Path(path)
    rows = list(csv.reader(source.open("r", encoding="utf-8-sig", newline="")))
    if len(rows) < 5 or len(rows[0]) < 3:
        raise ValueError("source CSV is too small for the declared map format")
    note = rows[0][0].strip()
    if "position" not in note.lower():
        raise ValueError("source CSV note does not declare coordinate positions")

    try:
        x = np.array([float(value) for value in rows[2][1:] if value.strip()], dtype=float)
        y_values: list[float] = []
        map_rows: list[list[float]] = []
        for row in rows[3:]:
            if not row or not row[0].strip():
                continue
            y_values.append(float(row[0]))
            values = [float(value) for value in row[1 : 1 + x.size]]
            if len(values) != x.size:
                raise ValueError("source CSV map row has the wrong width")
            map_rows.append(values)
    except (TypeError, ValueError) as exc:
        raise ValueError("source CSV contains an invalid numerical map") from exc

    y = np.asarray(y_values, dtype=float)
    values = np.asarray(map_rows, dtype=float)
    if values.shape != (y.size, x.size):
        raise ValueError("source CSV coordinate and map dimensions disagree")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("source coordinates must be finite")
    if not np.all(np.isfinite(values)):
        raise ValueError("source map must contain only finite values")
    if np.any(np.diff(x) <= 0.0) or np.any(np.diff(y) <= 0.0):
        raise ValueError("source coordinates must be strictly increasing")

    return SourceMap(x=_read_only(x), y=_read_only(y), values=_read_only(values), note=note)


def gaussian_kernel_1d(sigma_pixels: float, *, truncate: float = 4.0) -> FloatArray:
    """Return the normalized sampled Gaussian kernel used by SciPy ndimage."""

    sigma = float(sigma_pixels)
    cutoff = float(truncate)
    if not isfinite(sigma) or sigma <= 0.0:
        raise ValueError("sigma_pixels must be finite and positive")
    if not isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError("truncate must be finite and positive")
    radius = int(cutoff * sigma + 0.5)
    offsets = np.arange(-radius, radius + 1, dtype=float)
    kernel = np.exp(-0.5 * (offsets / sigma) ** 2)
    kernel /= np.sum(kernel)
    return _read_only(kernel)


def _convolve_axis(values: FloatMatrix, kernel: FloatArray, axis: int, mode: str) -> FloatMatrix:
    radius = kernel.size // 2
    if mode == "reflect":
        pad_mode = "symmetric"
    elif mode == "nearest":
        pad_mode = "edge"
    elif mode == "wrap":
        pad_mode = "wrap"
    else:
        raise ValueError("mode must be 'reflect', 'nearest', or 'wrap'")
    padding = [(0, 0), (0, 0)]
    padding[axis] = (radius, radius)
    padded = np.pad(values, padding, mode=pad_mode)
    convolved = np.apply_along_axis(
        lambda row: np.convolve(row, np.asarray(kernel), mode="valid"),
        axis,
        padded,
    )
    return np.asarray(convolved, dtype=float)


def gaussian_smooth(
    field: ArrayLike,
    sigma_pixels: float,
    *,
    mode: str = "reflect",
    truncate: float = 4.0,
) -> FloatMatrix:
    """Apply an isotropic separable discrete Gaussian to one finite map.

    The sampled kernel, radius convention, and boundary extensions reproduce
    ``scipy.ndimage.gaussian_filter`` for the supported modes without adding
    SciPy as a package dependency.
    """

    values = _validated_field(field)
    sigma = float(sigma_pixels)
    if not isfinite(sigma) or sigma < 0.0:
        raise ValueError("sigma_pixels must be finite and non-negative")
    if sigma == 0.0:
        return _read_only(values)
    kernel = gaussian_kernel_1d(sigma, truncate=truncate)
    result = _convolve_axis(values, kernel, 0, mode)
    result = _convolve_axis(result, kernel, 1, mode)
    return _read_only(result)


def variance_curve(
    field: ArrayLike,
    scales_pixels: ArrayLike,
    *,
    mode: str = "reflect",
    truncate: float = 4.0,
) -> FloatArray:
    """Return ordinary sample variance after every declared added kernel."""

    values = _validated_field(field)
    scales = _validated_scales(scales_pixels)
    variances = [
        float(np.var(gaussian_smooth(values, float(scale), mode=mode, truncate=truncate), ddof=1))
        for scale in scales
    ]
    if not np.all(np.isfinite(variances)) or np.any(np.asarray(variances) <= 0.0):
        raise ArithmeticError("variance curve left its finite positive domain")
    return _read_only(variances)


def planar_detrend(field: ArrayLike) -> FloatMatrix:
    """Remove a least-squares plane from one map while preserving its mean."""

    values = _validated_field(field)
    rows, columns = values.shape
    yy, xx = np.indices(values.shape, dtype=float)
    design = np.column_stack((np.ones(values.size), xx.ravel(), yy.ravel()))
    coefficients, _, rank, _ = np.linalg.lstsq(design, values.ravel(), rcond=None)
    if rank != 3:
        raise ArithmeticError("planar detrending design is rank deficient")
    trend = (design @ coefficients).reshape(values.shape)
    result = values - trend + float(np.mean(values))
    return _read_only(result)


def phase_randomized_surrogate(field: ArrayLike, *, seed: int) -> FloatMatrix:
    """Return a real surrogate with the source discrete Fourier amplitudes."""

    values = _validated_field(field)
    centered = values - float(np.mean(values))
    source_fft = np.fft.rfft2(centered)
    rng = np.random.default_rng(int(seed))
    noise_fft = np.fft.rfft2(rng.normal(size=values.shape))
    amplitudes = np.abs(noise_fft)
    phases = np.ones_like(noise_fft, dtype=complex)
    nonzero = amplitudes > 0.0
    phases[nonzero] = noise_fft[nonzero] / amplitudes[nonzero]
    surrogate_fft = np.abs(source_fft) * phases
    surrogate_fft[0, 0] = 0.0
    surrogate = np.fft.irfft2(surrogate_fft, s=values.shape)
    surrogate += float(np.mean(values))
    return _read_only(surrogate)


def _golden_section_minimize(
    function: Callable[[float], float],
    lower: float,
    upper: float,
    *,
    iterations: int = 160,
) -> float:
    ratio = (sqrt(5.0) - 1.0) / 2.0
    left = float(lower)
    right = float(upper)
    x1 = right - ratio * (right - left)
    x2 = left + ratio * (right - left)
    f1 = function(x1)
    f2 = function(x2)
    for _ in range(iterations):
        if f1 <= f2:
            right, x2, f2 = x2, x1, f1
            x1 = right - ratio * (right - left)
            f1 = function(x1)
        else:
            left, x1, f1 = x1, x2, f2
            x2 = left + ratio * (right - left)
            f2 = function(x2)
    return float((left + right) / 2.0)


def _attenuation(scales: FloatArray, correlation_scale: float, family: str) -> FloatArray:
    ell = float(correlation_scale)
    if not isfinite(ell) or ell <= 0.0:
        raise ValueError("correlation_scale must be finite and positive")
    if family == "Gaussian":
        values = 1.0 / (1.0 + 2.0 * np.asarray(scales) ** 2 / ell**2)
    else:
        smoothness = {
            "Matern_nu_1_over_2": 0.5,
            "Matern_nu_3_over_2": 1.5,
            "Matern_nu_5_over_2": 2.5,
        }.get(family)
        if smoothness is None:
            raise ValueError("unsupported covariance family")
        values = np.array(
            [
                matern_gaussian_probe_attenuation_2d(float(scale), ell, smoothness)
                for scale in scales
            ],
            dtype=float,
        )
    return _read_only(values)


def fit_family_log_variance(
    scales_pixels: ArrayLike,
    observed_variances: ArrayLike,
    *,
    training_indices: Iterable[int],
    held_out_index: int,
    family: str,
    minimum_scale_pixels: float = 0.02,
    maximum_scale_pixels: float = 200.0,
) -> FamilyFit:
    """Fit one family by deterministic unweighted log-variance loss."""

    scales = _validated_scales(scales_pixels)
    observed = np.asarray(observed_variances, dtype=float)
    if observed.shape != scales.shape or not np.all(np.isfinite(observed)) or np.any(observed <= 0.0):
        raise ValueError("observed_variances must match scales and be finite and positive")
    indices = np.array(tuple(int(index) for index in training_indices), dtype=int)
    if indices.ndim != 1 or indices.size < 2 or np.unique(indices).size != indices.size:
        raise ValueError("training_indices must contain at least two distinct indices")
    if np.any(indices < 0) or np.any(indices >= scales.size):
        raise ValueError("training index lies outside the scale array")
    holdout = int(held_out_index)
    if holdout < 0 or holdout >= scales.size or holdout in set(indices.tolist()):
        raise ValueError("held_out_index must identify one nontraining scale")

    train_scales = np.asarray(scales)[indices]
    train_log_values = np.log(observed[indices])

    def loss(log_ell: float) -> float:
        attenuation = np.asarray(_attenuation(train_scales, exp(log_ell), family))
        log_a = float(np.mean(train_log_values - np.log(attenuation)))
        residual = log_a + np.log(attenuation) - train_log_values
        return float(residual @ residual)

    lower = log(float(minimum_scale_pixels))
    upper = log(float(maximum_scale_pixels))
    log_ell = _golden_section_minimize(loss, lower, upper)
    ell = exp(log_ell)
    train_attenuation = np.asarray(_attenuation(train_scales, ell, family))
    log_a = float(np.mean(train_log_values - np.log(train_attenuation)))
    point_variance = exp(log_a)
    prediction = point_variance * np.asarray(_attenuation(scales, ell, family))
    training_residual = np.log(prediction[indices]) - train_log_values
    signed_error = float((prediction[holdout] - observed[holdout]) / observed[holdout])

    return FamilyFit(
        family=family,
        point_variance=point_variance,
        correlation_scale_pixels=ell,
        predicted_variances=_read_only(prediction),
        training_log_rms=float(sqrt(float(training_residual @ training_residual) / indices.size)),
        held_out_signed_relative_error=signed_error,
        held_out_absolute_relative_error=abs(signed_error),
    )


def analyze_real_map(
    source: SourceMap,
    *,
    scales_pixels: ArrayLike,
    training_indices: Iterable[int],
    held_out_index: int,
    crop_rows: slice,
    crop_columns: slice,
    surrogate_seed: int,
    truncate: float = 4.0,
) -> RealMapAnalysis:
    """Execute the frozen restricted CdSeTe real-map protocol."""

    scales = _validated_scales(scales_pixels)
    values = _validated_field(source.values)
    dx = np.diff(np.asarray(source.x))
    dy = np.diff(np.asarray(source.y))
    spacing = float((np.mean(dx) + np.mean(dy)) / 2.0)
    if not np.allclose(dx, spacing, rtol=2.0e-4, atol=2.0e-5) or not np.allclose(
        dy, spacing, rtol=2.0e-4, atol=2.0e-5
    ):
        raise ValueError("source coordinate grid is not uniform within rounding tolerance")

    primary = variance_curve(values, scales, mode="reflect", truncate=truncate)
    wrap = variance_curve(values, scales, mode="wrap", truncate=truncate)
    nearest = variance_curve(values, scales, mode="nearest", truncate=truncate)
    cropped = values[crop_rows, crop_columns]
    if cropped.shape != (16, 16):
        raise ValueError("frozen crop must have shape 16 x 16")
    crop_curve = variance_curve(cropped, scales, mode="reflect", truncate=truncate)
    detrended_curve = variance_curve(
        planar_detrend(values), scales, mode="reflect", truncate=truncate
    )

    families = (
        "Gaussian",
        "Matern_nu_1_over_2",
        "Matern_nu_3_over_2",
        "Matern_nu_5_over_2",
    )
    fits = tuple(
        fit_family_log_variance(
            scales,
            primary,
            training_indices=training_indices,
            held_out_index=held_out_index,
            family=family,
        )
        for family in families
    )
    gaussian_fit = fits[0]
    reciprocal = gaussian_reciprocal_linearity_fit(scales, primary)

    yy, xx = np.indices(values.shape, dtype=float)
    positions = np.column_stack((xx.ravel(), yy.ravel()))
    covariance = GaussianCovariance.isotropic(
        gaussian_fit.point_variance,
        gaussian_fit.correlation_scale_pixels,
        dimension=2,
    )
    blocks = gaussian_multiscale_map_covariance_blocks(covariance, positions, scales)
    statistics = gaussian_multiscale_map_variance_statistics(blocks, scales)
    comparison = gaussian_multiscale_map_fisher_comparison(
        gaussian_fit.point_variance,
        gaussian_fit.correlation_scale_pixels,
        scales,
        statistics.delta_log_variance_covariance,
        nominal_pixel_count=values.size,
    )

    surrogate = phase_randomized_surrogate(values, seed=surrogate_seed)
    source_mean = float(np.mean(values))
    source_variance = float(np.var(values, ddof=1))
    surrogate_mean_residual = float(np.mean(surrogate) - source_mean)
    surrogate_variance_relative_residual = float(
        (np.var(surrogate, ddof=1) - source_variance) / source_variance
    )
    surrogate_wrap = variance_curve(surrogate, scales, mode="wrap", truncate=truncate)
    surrogate_reflect = variance_curve(surrogate, scales, mode="reflect", truncate=truncate)
    wrap_relative = np.abs((np.asarray(surrogate_wrap) - np.asarray(wrap)) / np.asarray(wrap))

    return RealMapAnalysis(
        scales_pixels=scales,
        scales_micrometre=_read_only(np.asarray(scales) * spacing),
        source_mean=source_mean,
        source_sample_variance=source_variance,
        primary_variances=primary,
        wrap_variances=wrap,
        nearest_variances=nearest,
        crop_variances=crop_curve,
        planar_detrended_variances=detrended_curve,
        family_fits=fits,
        reciprocal_fit_point_variance=reciprocal.fitted_point_variance,
        reciprocal_fit_correlation_scale_pixels=reciprocal.fitted_correlation_length,
        reciprocal_fit_maximum_relative_residual=reciprocal.maximum_absolute_relative_variance_residual,
        gaussian_bias_factors=statistics.deterministic_bias_factors,
        gaussian_log_variance_covariance=statistics.delta_log_variance_covariance,
        gaussian_cross_scale_correlation=statistics.delta_log_variance_correlation,
        gaussian_effective_degrees_of_freedom=statistics.moment_matched_effective_degrees_of_freedom,
        gaussian_parameter_sd_inflation=comparison.parameter_standard_deviation_inflation,
        gaussian_parameter_covariance_determinant_inflation=(
            comparison.parameter_covariance_determinant_inflation
        ),
        surrogate_mean_residual=surrogate_mean_residual,
        surrogate_variance_relative_residual=surrogate_variance_relative_residual,
        surrogate_wrap_variance_maximum_relative_residual=float(np.max(wrap_relative)),
        surrogate_reflect_variances=surrogate_reflect,
    )
