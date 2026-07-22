"""Build the deterministic R04 cross-scale raster reference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.spatial_disorder import GaussianCovariance
from mct_research.spatial_disorder_map_sampling import regular_grid_positions
from mct_research.spatial_disorder_multiscale_map import (
    gaussian_multiscale_map_covariance_blocks,
    gaussian_multiscale_map_fisher_comparison,
    gaussian_multiscale_map_variance_statistics,
)

POINT_STANDARD_DEVIATION = 0.005
POINT_VARIANCE = POINT_STANDARD_DEVIATION**2
CORRELATION_LENGTH_UM = 2.0
PROBE_SIGMAS_UM = np.array([0.23094, 1.15470, 4.61880])


def _case(shape: tuple[int, int], spacing_um: float) -> dict[str, Any]:
    covariance = GaussianCovariance.isotropic(
        POINT_VARIANCE,
        CORRELATION_LENGTH_UM,
        2,
    )
    positions = regular_grid_positions(shape, spacing_um)
    blocks = gaussian_multiscale_map_covariance_blocks(
        covariance,
        positions,
        PROBE_SIGMAS_UM,
    )
    statistics = gaussian_multiscale_map_variance_statistics(
        blocks,
        PROBE_SIGMAS_UM,
    )
    comparison = gaussian_multiscale_map_fisher_comparison(
        POINT_VARIANCE,
        CORRELATION_LENGTH_UM,
        PROBE_SIGMAS_UM,
        statistics.delta_log_variance_covariance,
        nominal_pixel_count=statistics.nominal_pixel_count,
    )
    return {
        "shape": list(shape),
        "spacing_um": spacing_um,
        "nominal_pixel_count": statistics.nominal_pixel_count,
        "marginal_filtered_variances": (
            statistics.marginal_filtered_variances.tolist()
        ),
        "expected_naive_variances": (
            statistics.expected_naive_variances.tolist()
        ),
        "deterministic_bias_factors": (
            statistics.deterministic_bias_factors.tolist()
        ),
        "raw_variance_estimator_covariance": (
            statistics.raw_variance_estimator_covariance.tolist()
        ),
        "bias_corrected_estimator_covariance": (
            statistics.bias_corrected_estimator_covariance.tolist()
        ),
        "delta_log_variance_covariance": (
            statistics.delta_log_variance_covariance.tolist()
        ),
        "delta_log_variance_standard_deviations": (
            statistics.delta_log_variance_standard_deviations.tolist()
        ),
        "delta_log_variance_correlation": (
            statistics.delta_log_variance_correlation.tolist()
        ),
        "moment_matched_effective_degrees_of_freedom": (
            statistics.moment_matched_effective_degrees_of_freedom.tolist()
        ),
        "log_parameter_jacobian": comparison.log_parameter_jacobian.tolist(),
        "full_parameter_covariance": (
            comparison.full_parameter_covariance.tolist()
        ),
        "nominal_independent_pixel_parameter_covariance": (
            comparison.nominal_independent_pixel_parameter_covariance.tolist()
        ),
        "full_parameter_standard_deviations": np.sqrt(
            np.diag(comparison.full_parameter_covariance)
        ).tolist(),
        "nominal_parameter_standard_deviations": np.sqrt(
            np.diag(
                comparison.nominal_independent_pixel_parameter_covariance
            )
        ).tolist(),
        "parameter_standard_deviation_inflation": (
            comparison.parameter_standard_deviation_inflation.tolist()
        ),
        "parameter_covariance_determinant_inflation": (
            comparison.parameter_covariance_determinant_inflation
        ),
        "full_parameter_correlation": comparison.full_parameter_correlation,
        "nominal_parameter_correlation": comparison.nominal_parameter_correlation,
    }


def build_reference() -> dict[str, Any]:
    coarse = _case((10, 10), 0.5)
    fine = _case((20, 20), 0.25)
    coarse_full = np.asarray(coarse["full_parameter_standard_deviations"])
    fine_full = np.asarray(fine["full_parameter_standard_deviations"])
    coarse_nominal = np.asarray(coarse["nominal_parameter_standard_deviations"])
    fine_nominal = np.asarray(fine["nominal_parameter_standard_deviations"])
    return {
        "schema_version": "1.0",
        "program_issue": 196,
        "implementation_issue": 246,
        "portfolio_contribution": "R04",
        "status": "controlled_same_raster_covariance_not_specimen_inference",
        "model": {
            "dimension": 2,
            "point_composition_standard_deviation": POINT_STANDARD_DEVIATION,
            "point_composition_variance": POINT_VARIANCE,
            "correlation_length_um": CORRELATION_LENGTH_UM,
            "probe_sigmas_um": PROBE_SIGMAS_UM.tolist(),
            "common_sample_centers_across_scales": True,
        },
        "exact_theorems": {
            "mean_naive_variance": "tr(P C_ii)/(n-1)",
            "cross_scale_variance_covariance": (
                "2 tr(P C_ij P C_ji)/(n-1)^2"
            ),
            "delta_log_covariance": (
                "Cov(q_i,q_j)/(E[q_i] E[q_j])"
            ),
            "nominal_independent_pixel_log_covariance": "2 I/(n-1)",
        },
        "dense_reference": coarse,
        "fixed_field_of_view_oversampling": {
            "coarse": coarse,
            "fine": fine,
            "nominal_pixel_ratio": (
                fine["nominal_pixel_count"] / coarse["nominal_pixel_count"]
            ),
            "full_parameter_sd_ratios_fine_over_coarse": (
                fine_full / coarse_full
            ).tolist(),
            "nominal_parameter_sd_ratios_fine_over_coarse": (
                fine_nominal / coarse_nominal
            ).tolist(),
            "full_log_xi_precision_improvement_fraction": (
                1.0 - fine_full[1] / coarse_full[1]
            ),
            "nominal_log_xi_precision_improvement_fraction": (
                1.0 - fine_nominal[1] / coarse_nominal[1]
            ),
            "determinant_inflation_ratio_fine_over_coarse": (
                fine["parameter_covariance_determinant_inflation"]
                / coarse["parameter_covariance_determinant_inflation"]
            ),
        },
        "headline": {
            "dense_bias_factors": coarse["deterministic_bias_factors"],
            "dense_log_estimator_standard_deviations": (
                coarse["delta_log_variance_standard_deviations"]
            ),
            "dense_cross_scale_correlations": [
                coarse["delta_log_variance_correlation"][0][1],
                coarse["delta_log_variance_correlation"][0][2],
                coarse["delta_log_variance_correlation"][1][2],
            ],
            "dense_parameter_sd_inflation": (
                coarse["parameter_standard_deviation_inflation"]
            ),
            "dense_parameter_covariance_determinant_inflation": (
                coarse["parameter_covariance_determinant_inflation"]
            ),
            "fourfold_pixel_full_log_xi_precision_improvement_fraction": (
                1.0 - fine_full[1] / coarse_full[1]
            ),
            "fourfold_pixel_nominal_log_xi_precision_improvement_fraction": (
                1.0 - fine_nominal[1] / coarse_nominal[1]
            ),
        },
        "claim_boundaries": [
            "Gaussian quadratic-form cross moments and Fisher information are established mathematics.",
            "The log-variance covariance is a first-order delta-method result, not an exact log-normal distribution.",
            "Deterministic bias correction does not create independent spatial information.",
            "Nominal raster pixel count is not an independent-repeat count.",
            "The controlled design is not a specimen covariance estimate or a universal scan prescription.",
            "This result does not authorize a manuscript."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    record = build_reference()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
