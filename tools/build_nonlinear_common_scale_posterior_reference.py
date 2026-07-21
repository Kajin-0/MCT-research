#!/usr/bin/env python3
"""Build the immutable nonlinear common-scale posterior reference."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from mct_research.spatial_disorder_inference import (
    gaussian_multiscale_fisher_information,
    gaussian_multiscale_variance,
)
from mct_research.spatial_disorder_posterior import (
    combine_common_scale_calibration,
    direct_bounded_common_scale_posterior,
    discrete_distribution,
    gaussian_grid_distribution,
    relative_scale_posterior_grid,
)


def _array(value: np.ndarray) -> list[float] | list[list[float]]:
    return np.asarray(value, dtype=float).tolist()


def build_reference() -> dict[str, object]:
    point_variance = 0.03
    correlation_length = 1.4
    scales = np.array([0.2, 0.7, 2.0, 6.0], dtype=float)
    observed = gaussian_multiscale_variance(
        point_variance,
        correlation_length,
        scales,
    )
    true_u = math.log(point_variance)
    true_lambda = math.log(correlation_length)

    noise_cases = []
    for uncertainty, half_width, points in (
        (0.01, 0.12, 241),
        (0.05, 0.70, 181),
        (0.15, 1.20, 201),
        (0.30, 2.00, 241),
    ):
        posterior = relative_scale_posterior_grid(
            observed,
            scales,
            np.linspace(true_u - half_width, true_u + half_width, points),
            np.linspace(
                true_lambda - half_width,
                true_lambda + half_width,
                points,
            ),
            relative_standard_deviation=uncertainty,
        )
        fisher = gaussian_multiscale_fisher_information(
            point_variance,
            correlation_length,
            scales,
            relative_standard_deviation=uncertainty,
        )
        fisher_covariance = np.asarray(fisher.parameter_covariance)
        relative_frobenius_error = float(
            np.linalg.norm(np.asarray(posterior.covariance) - fisher_covariance)
            / np.linalg.norm(fisher_covariance)
        )
        noise_cases.append(
            {
                "relative_observation_standard_deviation": uncertainty,
                "posterior_mean": _array(posterior.mean),
                "posterior_covariance": _array(posterior.covariance),
                "fisher_covariance": _array(fisher_covariance),
                "relative_frobenius_covariance_error": relative_frobenius_error,
                "posterior_boundary_mass": posterior.boundary_mass,
            }
        )

    common_calibration_cases = []
    relative_uncertainty = 0.15
    step = 0.01
    relative = relative_scale_posterior_grid(
        observed,
        scales,
        true_u + step * np.arange(-120, 121),
        true_lambda + step * np.arange(-160, 161),
        relative_standard_deviation=relative_uncertainty,
    )
    for calibration_sigma in (0.02, 0.10):
        calibration_extent = max(8, int(math.ceil(5.0 * calibration_sigma / step)))
        calibration = gaussian_grid_distribution(
            step * np.arange(-calibration_extent, calibration_extent + 1),
            0.0,
            calibration_sigma,
        )
        combined = combine_common_scale_calibration(relative, calibration)
        common_calibration_cases.append(
            {
                "calibration_log_standard_deviation": calibration_sigma,
                "discrete_calibration_variance": calibration.variance,
                "relative_posterior_covariance": _array(relative.covariance),
                "absolute_posterior_covariance": _array(combined.covariance),
                "covariance_increment": _array(combined.covariance_increment),
                "variance_addition_residual": combined.variance_addition_residual,
                "cross_covariance_residual": combined.cross_covariance_residual,
            }
        )

    asymmetric_grid = step * np.arange(-30, 31)
    asymmetric_mass = np.exp(-0.5 * ((asymmetric_grid + 0.04) / 0.09) ** 2)
    asymmetric_mass *= 1.0 + 0.8 * (asymmetric_grid > 0.0)
    asymmetric = discrete_distribution(asymmetric_grid, asymmetric_mass)
    asymmetric_combined = combine_common_scale_calibration(relative, asymmetric)

    direct_step = 0.025
    direct_u_grid = true_u + direct_step * np.arange(-32, 33)
    direct_delta = gaussian_grid_distribution(
        direct_step * np.arange(-16, 17),
        0.0,
        0.10,
    )
    broad = direct_bounded_common_scale_posterior(
        observed,
        scales,
        direct_u_grid,
        true_lambda + direct_step * np.arange(-72, 73),
        direct_delta,
        relative_standard_deviation=0.08,
    )
    narrow = direct_bounded_common_scale_posterior(
        observed,
        scales,
        direct_u_grid,
        true_lambda + direct_step * np.arange(-7, 8),
        direct_delta,
        relative_standard_deviation=0.08,
        boundary_cells=2,
    )

    return {
        "schema_version": "1.0",
        "program": "measurement-kernel-aware spatial disorder",
        "portfolio_contribution": "R04",
        "issue": 220,
        "status": "exact_model_conditioned_posterior_not_specimen_inference",
        "model": {
            "variance": "A/[1+2(s exp(delta))^2/xi^2]",
            "transformed_parameters": [
                "u=log A",
                "v=log xi",
                "lambda=v-delta",
            ],
            "factorization": "p(u,lambda,delta|y)=p(u,lambda|y)p_delta(delta)",
            "cumulant_identity": "kappa_n(v)=kappa_n(lambda)+kappa_n(delta)",
        },
        "synthetic_design": {
            "point_variance": point_variance,
            "correlation_length": correlation_length,
            "probe_sigmas": _array(scales),
            "observed_variances": _array(observed),
            "likelihood": "log_gaussian",
        },
        "fisher_comparison": noise_cases,
        "common_calibration_cases": common_calibration_cases,
        "asymmetric_calibration_case": {
            "calibration_mean": asymmetric.mean,
            "calibration_variance": asymmetric.variance,
            "calibration_third_cumulant": asymmetric.third_cumulant,
            "calibration_fourth_cumulant": asymmetric.fourth_cumulant,
            "absolute_log_correlation_cumulants": _array(
                asymmetric_combined.log_correlation_cumulants
            ),
            "variance_addition_residual": (
                asymmetric_combined.variance_addition_residual
            ),
            "cross_covariance_residual": (
                asymmetric_combined.cross_covariance_residual
            ),
        },
        "bounded_prior_cases": {
            "broad": {
                "absolute_log_length_boundary_mass": (
                    broad.log_absolute_correlation_boundary_mass
                ),
                "posterior_calibration_total_variation": (
                    broad.posterior_calibration_total_variation
                ),
                "relative_calibration_covariance": (
                    broad.relative_calibration_covariance
                ),
                "variance_addition_residual": broad.variance_addition_residual,
                "cross_covariance_residual": broad.cross_covariance_residual,
            },
            "narrow": {
                "absolute_log_length_boundary_mass": (
                    narrow.log_absolute_correlation_boundary_mass
                ),
                "posterior_calibration_total_variation": (
                    narrow.posterior_calibration_total_variation
                ),
                "relative_calibration_covariance": (
                    narrow.relative_calibration_covariance
                ),
                "variance_addition_residual": narrow.variance_addition_residual,
                "cross_covariance_residual": narrow.cross_covariance_residual,
            },
        },
        "claim_boundaries": [
            "The exact factorization requires scale dependence through s exp(delta)/xi and an independent calibration prior.",
            "A bounded or informative absolute log-length prior can break factorization near its support boundary.",
            "The grid calculations are deterministic synthetic checks, not specimen inference.",
            "The Fisher comparison is specific to the declared design and log-Gaussian likelihood.",
            "No covariance family or HgCdTe correlation length is validated by this result.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_reference(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
