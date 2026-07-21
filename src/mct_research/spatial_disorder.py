"""Scale-dependent spatial-disorder operators for HgCdTe observables.

The functions in this module separate microscopic composition variance from the
variance seen by a finite measurement kernel.  Length arguments must use a
single consistent unit; the formulas depend only on length ratios.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable


@dataclass(frozen=True)
class GaussianTwoScaleRecovery:
    """Exact recovery from two Gaussian probe-scale variance measurements."""

    microscopic_variance: float
    microscopic_standard_deviation: float
    correlation_length: float
    probe_scale_first: float
    probe_scale_second: float
    observed_variance_first: float
    observed_variance_second: float
    dimension: int
    powered_variance_ratio: float
    log_parameter_condition_number: float
    relative_reconstruction_residual: float


@dataclass(frozen=True)
class ProbeAveragedGapMoments:
    """Second-order Gaussian propagation through a declared signed-gap law."""

    latent_gap_at_mean_ev: float
    mean_gap_ev: float
    gap_variance_ev2: float
    gap_standard_deviation_ev: float
    effective_composition_variance: float
    effective_composition_standard_deviation: float
    first_composition_derivative_ev: float
    second_composition_derivative_ev: float


def _require_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _require_positive(name: str, value: float) -> float:
    value = _require_finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def _require_nonnegative(name: str, value: float) -> float:
    value = _require_finite(name, value)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _require_dimension(dimension: int) -> int:
    if isinstance(dimension, bool) or int(dimension) != dimension:
        raise ValueError("dimension must be a positive integer")
    dimension = int(dimension)
    if dimension <= 0:
        raise ValueError("dimension must be a positive integer")
    return dimension


def gaussian_probe_variance(
    microscopic_variance: float,
    correlation_length: float,
    probe_scale: float,
    dimension: int,
) -> float:
    r"""Return the exact variance seen by a Gaussian probe.

    The covariance and normalized probe are

    .. math::

       C(h)=\sigma_x^2\exp[-|h|^2/(2\ell^2)],
       \qquad
       w_a(r)=(2\pi a^2)^{-D/2}\exp[-|r|^2/(2a^2)].

    Their double convolution gives

    .. math::

       \operatorname{Var}(X_a)=\sigma_x^2
       \left(1+2a^2/\ell^2\right)^{-D/2}.
    """

    microscopic_variance = _require_nonnegative(
        "microscopic_variance", microscopic_variance
    )
    correlation_length = _require_positive("correlation_length", correlation_length)
    probe_scale = _require_nonnegative("probe_scale", probe_scale)
    dimension = _require_dimension(dimension)
    ratio_squared = (probe_scale / correlation_length) ** 2
    return microscopic_variance * (1.0 + 2.0 * ratio_squared) ** (
        -0.5 * dimension
    )


def gaussian_probe_standard_deviation(
    microscopic_standard_deviation: float,
    correlation_length: float,
    probe_scale: float,
    dimension: int,
) -> float:
    """Return the probe-averaged standard deviation for the Gaussian model."""

    microscopic_standard_deviation = _require_nonnegative(
        "microscopic_standard_deviation", microscopic_standard_deviation
    )
    return math.sqrt(
        gaussian_probe_variance(
            microscopic_standard_deviation**2,
            correlation_length,
            probe_scale,
            dimension,
        )
    )


def single_scale_microscopic_variance(
    observed_variance: float,
    correlation_length: float,
    probe_scale: float,
    dimension: int,
) -> float:
    """Return one member of the one-scale non-identifiability family.

    For every positive declared correlation length, this function produces a
    microscopic variance with exactly the same observed variance.  A single
    probe scale therefore cannot identify both quantities.
    """

    observed_variance = _require_nonnegative("observed_variance", observed_variance)
    correlation_length = _require_positive("correlation_length", correlation_length)
    probe_scale = _require_nonnegative("probe_scale", probe_scale)
    dimension = _require_dimension(dimension)
    return observed_variance * (
        1.0 + 2.0 * (probe_scale / correlation_length) ** 2
    ) ** (0.5 * dimension)


def two_scale_log_jacobian_condition_number(
    correlation_length: float,
    probe_scale_first: float,
    probe_scale_second: float,
    dimension: int,
) -> float:
    r"""Return the 2-norm condition number in logarithmic parameters.

    For :math:`y_i=\log V_i` and
    :math:`\theta=(\log\sigma_x^2,\log\ell)`, the Jacobian rows are

    .. math::

       (1,g_i),\qquad
       g_i=D\frac{2a_i^2/\ell^2}{1+2a_i^2/\ell^2}.

    The condition number diverges when the probe scales coincide and becomes
    large when both probes occupy the same asymptotic regime.
    """

    correlation_length = _require_positive("correlation_length", correlation_length)
    probe_scale_first = _require_nonnegative(
        "probe_scale_first", probe_scale_first
    )
    probe_scale_second = _require_nonnegative(
        "probe_scale_second", probe_scale_second
    )
    dimension = _require_dimension(dimension)

    def sensitivity(probe_scale: float) -> float:
        u = 2.0 * (probe_scale / correlation_length) ** 2
        return dimension * u / (1.0 + u)

    g_first = sensitivity(probe_scale_first)
    g_second = sensitivity(probe_scale_second)
    # Eigenvalues of J^T J for J=[[1,g1],[1,g2]].
    trace = 2.0 + g_first * g_first + g_second * g_second
    determinant = (g_first - g_second) ** 2
    discriminant = max(trace * trace - 4.0 * determinant, 0.0)
    root = math.sqrt(discriminant)
    lambda_max = 0.5 * (trace + root)
    lambda_min = 0.5 * (trace - root)
    if lambda_min <= 0.0:
        return math.inf
    return math.sqrt(lambda_max / lambda_min)


def recover_gaussian_disorder_two_scales(
    observed_variance_first: float,
    observed_variance_second: float,
    probe_scale_first: float,
    probe_scale_second: float,
    dimension: int,
) -> GaussianTwoScaleRecovery:
    r"""Recover microscopic variance and correlation length exactly.

    Let

    .. math::

       q=\left(V_1/V_2\right)^{2/D}.

    For distinct probe scales, the exact inverse is

    .. math::

       \ell^2=2\frac{a_2^2-q a_1^2}{q-1},\qquad
       \sigma_x^2=V_1\left(1+2a_1^2/\ell^2\right)^{D/2}.

    Inputs inconsistent with a positive Gaussian covariance model are rejected.
    """

    observed_variance_first = _require_positive(
        "observed_variance_first", observed_variance_first
    )
    observed_variance_second = _require_positive(
        "observed_variance_second", observed_variance_second
    )
    probe_scale_first = _require_nonnegative(
        "probe_scale_first", probe_scale_first
    )
    probe_scale_second = _require_nonnegative(
        "probe_scale_second", probe_scale_second
    )
    dimension = _require_dimension(dimension)
    if probe_scale_first == probe_scale_second:
        raise ValueError("two-scale recovery requires distinct probe scales")

    powered_ratio = (observed_variance_first / observed_variance_second) ** (
        2.0 / dimension
    )
    denominator = powered_ratio - 1.0
    if denominator == 0.0:
        raise ValueError("equal observed variances imply an infinite or unresolved scale")
    correlation_length_squared = 2.0 * (
        probe_scale_second**2 - powered_ratio * probe_scale_first**2
    ) / denominator
    if not math.isfinite(correlation_length_squared) or correlation_length_squared <= 0.0:
        raise ValueError("variance pair is inconsistent with a positive correlation length")

    correlation_length = math.sqrt(correlation_length_squared)
    microscopic_variance = single_scale_microscopic_variance(
        observed_variance_first,
        correlation_length,
        probe_scale_first,
        dimension,
    )
    reconstructed_first = gaussian_probe_variance(
        microscopic_variance,
        correlation_length,
        probe_scale_first,
        dimension,
    )
    reconstructed_second = gaussian_probe_variance(
        microscopic_variance,
        correlation_length,
        probe_scale_second,
        dimension,
    )
    residual = max(
        abs(reconstructed_first - observed_variance_first)
        / observed_variance_first,
        abs(reconstructed_second - observed_variance_second)
        / observed_variance_second,
    )
    return GaussianTwoScaleRecovery(
        microscopic_variance=microscopic_variance,
        microscopic_standard_deviation=math.sqrt(microscopic_variance),
        correlation_length=correlation_length,
        probe_scale_first=probe_scale_first,
        probe_scale_second=probe_scale_second,
        observed_variance_first=observed_variance_first,
        observed_variance_second=observed_variance_second,
        dimension=dimension,
        powered_variance_ratio=powered_ratio,
        log_parameter_condition_number=two_scale_log_jacobian_condition_number(
            correlation_length,
            probe_scale_first,
            probe_scale_second,
            dimension,
        ),
        relative_reconstruction_residual=residual,
    )


def top_hat_variance_gaussian_1d(
    microscopic_variance: float,
    correlation_length: float,
    window_length: float,
) -> float:
    r"""Exact variance of a 1D top-hat average with Gaussian covariance."""

    microscopic_variance = _require_nonnegative(
        "microscopic_variance", microscopic_variance
    )
    correlation_length = _require_positive("correlation_length", correlation_length)
    window_length = _require_positive("window_length", window_length)
    ratio = window_length / correlation_length
    if ratio < 1.0e-3:
        factor = (
            1.0
            - ratio**2 / 12.0
            + ratio**4 / 120.0
            - ratio**6 / 1344.0
        )
    else:
        term = (
            ratio
            * math.sqrt(math.pi / 2.0)
            * math.erf(ratio / math.sqrt(2.0))
            - (-math.expm1(-0.5 * ratio * ratio))
        )
        factor = 2.0 * term / (ratio * ratio)
    return microscopic_variance * factor


def top_hat_variance_exponential_1d(
    microscopic_variance: float,
    correlation_length: float,
    window_length: float,
) -> float:
    r"""Exact variance of a 1D top-hat average with exponential covariance."""

    microscopic_variance = _require_nonnegative(
        "microscopic_variance", microscopic_variance
    )
    correlation_length = _require_positive("correlation_length", correlation_length)
    window_length = _require_positive("window_length", window_length)
    ratio = window_length / correlation_length
    if ratio < 1.0e-4:
        factor = (
            1.0
            - ratio / 3.0
            + ratio**2 / 12.0
            - ratio**3 / 60.0
            + ratio**4 / 360.0
        )
    else:
        factor = 2.0 * (ratio - 1.0 + math.exp(-ratio)) / (ratio * ratio)
    return microscopic_variance * factor


def probe_averaged_gap_moments(
    gap_model: Callable[[float, float], float],
    mean_composition: float,
    temperature_k: float,
    microscopic_composition_variance: float,
    correlation_length: float,
    probe_scale: float,
    dimension: int,
    *,
    derivative_step: float = 1.0e-5,
) -> ProbeAveragedGapMoments:
    r"""Propagate probe-averaged Gaussian composition through a gap law.

    A quadratic expansion around the mean gives

    .. math::

       \mathbb E[E_g]\simeq E_g(\bar x,T)+\tfrac12 E_{g,xx}V_a,

    .. math::

       \operatorname{Var}(E_g)\simeq E_{g,x}^2V_a
       +\tfrac12 E_{g,xx}^2V_a^2.

    The second expression is exact for a quadratic gap law and Gaussian
    composition distribution.
    """

    mean_composition = _require_finite("mean_composition", mean_composition)
    temperature_k = _require_finite("temperature_k", temperature_k)
    derivative_step = _require_positive("derivative_step", derivative_step)
    effective_variance = gaussian_probe_variance(
        microscopic_composition_variance,
        correlation_length,
        probe_scale,
        dimension,
    )
    center = float(gap_model(mean_composition, temperature_k))
    plus = float(gap_model(mean_composition + derivative_step, temperature_k))
    minus = float(gap_model(mean_composition - derivative_step, temperature_k))
    if not all(math.isfinite(value) for value in (center, plus, minus)):
        raise ValueError("gap_model returned a non-finite value")
    first = (plus - minus) / (2.0 * derivative_step)
    second = (plus - 2.0 * center + minus) / (derivative_step**2)
    mean_gap = center + 0.5 * second * effective_variance
    gap_variance = first * first * effective_variance + 0.5 * (
        second * second * effective_variance * effective_variance
    )
    return ProbeAveragedGapMoments(
        latent_gap_at_mean_ev=center,
        mean_gap_ev=mean_gap,
        gap_variance_ev2=gap_variance,
        gap_standard_deviation_ev=math.sqrt(max(gap_variance, 0.0)),
        effective_composition_variance=effective_variance,
        effective_composition_standard_deviation=math.sqrt(effective_variance),
        first_composition_derivative_ev=first,
        second_composition_derivative_ev=second,
    )
