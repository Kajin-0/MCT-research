"""Thickness-pair design and uncertainty propagation for Chang tail validation."""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, sqrt


@dataclass(frozen=True)
class TailWidthPairEstimate:
    """Tail-width estimate and first-order uncertainty from two cutoffs."""

    width_ev: float
    standard_uncertainty_ev: float
    relative_standard_uncertainty: float
    cutoff_difference_ev: float
    log_thickness_ratio: float
    cutoff_difference_variance_ev2: float
    log_thickness_ratio_variance: float
    energy_ratio_covariance_ev: float


def _finite(value: float, *, name: str) -> float:
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _positive(value: float, *, name: str) -> float:
    number = _finite(value, name=name)
    if number <= 0.0:
        raise ValueError(f"{name} must be positive")
    return number


def _nonnegative(value: float, *, name: str) -> float:
    number = _finite(value, name=name)
    if number < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return number


def _correlation(value: float, *, name: str) -> float:
    number = _finite(value, name=name)
    if not -1.0 <= number <= 1.0:
        raise ValueError(f"{name} must lie between -1 and 1")
    return number


def cutoff_difference_variance_ev2(
    cutoff_sigma_1_ev: float,
    cutoff_sigma_2_ev: float,
    *,
    correlation: float = 0.0,
) -> float:
    """Return ``Var(E2-E1)`` including correlated cutoff errors."""

    sigma_1 = _nonnegative(cutoff_sigma_1_ev, name="cutoff_sigma_1_ev")
    sigma_2 = _nonnegative(cutoff_sigma_2_ev, name="cutoff_sigma_2_ev")
    rho = _correlation(correlation, name="correlation")
    variance = sigma_1**2 + sigma_2**2 - 2.0 * rho * sigma_1 * sigma_2
    return float(max(0.0, variance))


def log_thickness_ratio_variance(
    thickness_1: float,
    thickness_2: float,
    thickness_sigma_1: float = 0.0,
    thickness_sigma_2: float = 0.0,
    *,
    correlation: float = 0.0,
) -> float:
    """First-order variance of ``ln(d2/d1)``.

    Thicknesses and their uncertainties may use any common unit. They must refer
    to effective optical thickness when the result is used with the Chang
    response operator.
    """

    d1 = _positive(thickness_1, name="thickness_1")
    d2 = _positive(thickness_2, name="thickness_2")
    sigma_1 = _nonnegative(thickness_sigma_1, name="thickness_sigma_1")
    sigma_2 = _nonnegative(thickness_sigma_2, name="thickness_sigma_2")
    rho = _correlation(correlation, name="correlation")
    relative_1 = sigma_1 / d1
    relative_2 = sigma_2 / d2
    variance = (
        relative_1**2
        + relative_2**2
        - 2.0 * rho * relative_1 * relative_2
    )
    return float(max(0.0, variance))


def estimate_tail_width_from_cutoff_pair(
    cutoff_energy_1_ev: float,
    cutoff_energy_2_ev: float,
    effective_thickness_1: float,
    effective_thickness_2: float,
    *,
    cutoff_sigma_1_ev: float = 0.0,
    cutoff_sigma_2_ev: float = 0.0,
    cutoff_correlation: float = 0.0,
    thickness_sigma_1: float = 0.0,
    thickness_sigma_2: float = 0.0,
    thickness_correlation: float = 0.0,
    cutoff_difference_log_ratio_covariance_ev: float = 0.0,
) -> TailWidthPairEstimate:
    """Estimate ``W=-DeltaE/ln(d2/d1)`` and first-order uncertainty.

    The covariance argument is ``Cov(DeltaE, ln(d2/d1))`` in electron-volts.
    It is retained explicitly because energy calibration and effective-thickness
    inference may share nuisance parameters in a real optical model.
    """

    energy_1 = _finite(cutoff_energy_1_ev, name="cutoff_energy_1_ev")
    energy_2 = _finite(cutoff_energy_2_ev, name="cutoff_energy_2_ev")
    d1 = _positive(effective_thickness_1, name="effective_thickness_1")
    d2 = _positive(effective_thickness_2, name="effective_thickness_2")
    log_ratio = log(d2 / d1)
    if abs(log_ratio) < 1.0e-15:
        raise ValueError("effective thicknesses must have a non-unit ratio")

    delta_energy = energy_2 - energy_1
    width = -delta_energy / log_ratio
    if width <= 0.0:
        raise ValueError(
            "cutoff ordering is inconsistent with a positive exponential-tail width"
        )

    variance_energy = cutoff_difference_variance_ev2(
        cutoff_sigma_1_ev,
        cutoff_sigma_2_ev,
        correlation=cutoff_correlation,
    )
    variance_log_ratio = log_thickness_ratio_variance(
        d1,
        d2,
        thickness_sigma_1,
        thickness_sigma_2,
        correlation=thickness_correlation,
    )
    covariance = _finite(
        cutoff_difference_log_ratio_covariance_ev,
        name="cutoff_difference_log_ratio_covariance_ev",
    )

    derivative_energy = -1.0 / log_ratio
    derivative_ratio = delta_energy / log_ratio**2
    variance_width = (
        derivative_energy**2 * variance_energy
        + derivative_ratio**2 * variance_log_ratio
        + 2.0 * derivative_energy * derivative_ratio * covariance
    )
    scale = max(
        derivative_energy**2 * variance_energy,
        derivative_ratio**2 * variance_log_ratio,
        abs(2.0 * derivative_energy * derivative_ratio * covariance),
        1.0e-30,
    )
    if variance_width < -1.0e-12 * scale:
        raise ValueError("declared covariance produces a negative propagated variance")
    variance_width = max(0.0, variance_width)
    sigma_width = sqrt(variance_width)

    return TailWidthPairEstimate(
        width_ev=float(width),
        standard_uncertainty_ev=float(sigma_width),
        relative_standard_uncertainty=float(sigma_width / width),
        cutoff_difference_ev=float(delta_energy),
        log_thickness_ratio=float(log_ratio),
        cutoff_difference_variance_ev2=float(variance_energy),
        log_thickness_ratio_variance=float(variance_log_ratio),
        energy_ratio_covariance_ev=float(covariance),
    )


def maximum_source_valid_thickness_ratio(
    baseline_cutoff_energy_ev: float,
    tail_width_ev: float,
    minimum_allowed_energy_ev: float,
    *,
    energy_margin_ev: float = 0.0,
) -> float:
    """Return the largest ``d2/d1 >= 1`` that stays above the energy bound."""

    energy_1 = _finite(
        baseline_cutoff_energy_ev,
        name="baseline_cutoff_energy_ev",
    )
    width = _positive(tail_width_ev, name="tail_width_ev")
    minimum = _finite(minimum_allowed_energy_ev, name="minimum_allowed_energy_ev")
    margin = _nonnegative(energy_margin_ev, name="energy_margin_ev")
    allowed_minimum = minimum + margin
    if energy_1 <= allowed_minimum:
        raise ValueError(
            "baseline cutoff must lie above the minimum energy plus margin"
        )
    return float(exp((energy_1 - allowed_minimum) / width))


def required_equal_cutoff_sigma_ev(
    tail_width_ev: float,
    thickness_ratio: float,
    target_relative_width_uncertainty: float,
    *,
    cutoff_correlation: float = 0.0,
    relative_thickness_sigma_1: float = 0.0,
    relative_thickness_sigma_2: float = 0.0,
    thickness_correlation: float = 0.0,
) -> float:
    """Required equal per-cutoff uncertainty for a target relative ``W`` error.

    The result uses first-order propagation with zero covariance between the
    cutoff difference and the logarithmic thickness ratio. A negative residual
    variance budget means thickness uncertainty alone exceeds the target.
    """

    width = _positive(tail_width_ev, name="tail_width_ev")
    ratio = _positive(thickness_ratio, name="thickness_ratio")
    if abs(ratio - 1.0) < 1.0e-15:
        raise ValueError("thickness_ratio must not equal one")
    target = _positive(
        target_relative_width_uncertainty,
        name="target_relative_width_uncertainty",
    )
    rho_energy = _correlation(cutoff_correlation, name="cutoff_correlation")
    rho_thickness = _correlation(
        thickness_correlation,
        name="thickness_correlation",
    )
    if rho_energy >= 1.0:
        raise ValueError(
            "equal cutoff errors with correlation one provide no finite independent-error requirement"
        )
    rel_1 = _nonnegative(
        relative_thickness_sigma_1,
        name="relative_thickness_sigma_1",
    )
    rel_2 = _nonnegative(
        relative_thickness_sigma_2,
        name="relative_thickness_sigma_2",
    )
    variance_log_ratio = (
        rel_1**2 + rel_2**2 - 2.0 * rho_thickness * rel_1 * rel_2
    )
    logarithm = abs(log(ratio))
    residual = target**2 * logarithm**2 - variance_log_ratio
    if residual < -1.0e-15:
        raise ValueError(
            "thickness uncertainty alone exceeds the target width uncertainty"
        )
    residual = max(0.0, residual)
    return float(
        width * sqrt(residual / (2.0 * (1.0 - rho_energy)))
    )
