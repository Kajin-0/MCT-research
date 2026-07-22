"""Build the deterministic R04 correlated-map sampling reference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from mct_research.spatial_disorder import GaussianCovariance, GaussianKernel
from mct_research.spatial_disorder_map_sampling import (
    gaussian_regular_grid_sampling_diagnostics,
)


def _diagnostic_record(shape: tuple[int, int], spacing: float) -> dict[str, Any]:
    covariance = GaussianCovariance.isotropic(0.005**2, 2.0, 2)
    kernel = GaussianKernel.isotropic(1.0, 2)
    _, result = gaussian_regular_grid_sampling_diagnostics(
        covariance,
        kernel,
        shape,
        spacing,
    )
    return {
        "shape": list(shape),
        "spacing_um": spacing,
        "nominal_sample_count": result.nominal_sample_count,
        "average_marginal_variance": result.average_marginal_variance,
        "map_mean_variance": result.map_mean_variance,
        "map_mean_effective_sample_count": result.map_mean_effective_sample_count,
        "naive_sample_variance_expectation": result.naive_sample_variance_expectation,
        "naive_sample_variance_ratio": (
            result.naive_sample_variance_expectation
            / result.average_marginal_variance
        ),
        "naive_sample_variance_relative_bias": (
            result.naive_sample_variance_relative_bias
        ),
        "naive_sample_variance_variance": result.naive_sample_variance_variance,
        "naive_sample_variance_relative_standard_deviation": (
            result.naive_sample_variance_relative_standard_deviation
        ),
        "variance_effective_degrees_of_freedom": (
            result.variance_effective_degrees_of_freedom
        ),
        "covariance_condition_number": result.covariance_condition_number,
    }


def build_reference() -> dict[str, Any]:
    spacing_cases = [
        _diagnostic_record((10, 10), spacing)
        for spacing in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0)
    ]
    coarse = _diagnostic_record((10, 10), 0.5)
    fine = _diagnostic_record((20, 20), 0.25)
    information_gain = (
        fine["map_mean_effective_sample_count"]
        / coarse["map_mean_effective_sample_count"]
        - 1.0
    )
    dense = spacing_cases[1]
    nearly_independent = spacing_cases[-1]
    return {
        "schema_version": "1.0",
        "program_issue": 196,
        "implementation_issue": 234,
        "portfolio_contribution": "R04",
        "status": "controlled_gaussian_map_sampling_not_specimen_inference",
        "model": {
            "dimension": 2,
            "point_composition_standard_deviation": 0.005,
            "point_composition_variance": 0.005**2,
            "correlation_length_um": 2.0,
            "gaussian_probe_sigma_um": 1.0,
            "filtered_marginal_variance": 1.6666666666666667e-5,
            "grid_shape": [10, 10],
        },
        "exact_theorems": {
            "cross_covariance": (
                "A sqrt(det(Lambda)/det(Lambda+Sigma_i+Sigma_j)) "
                "exp[-0.5 delta^T (Lambda+Sigma_i+Sigma_j)^-1 delta]"
            ),
            "map_mean_variance": "1^T C 1 / n^2",
            "naive_sample_variance_expectation": "tr(P C)/(n-1)",
            "naive_sample_variance_variance": (
                "2 tr[(P C)^2]/(n-1)^2"
            ),
            "map_mean_effective_sample_count": (
                "average marginal variance / Var(map mean)"
            ),
            "variance_effective_degrees_of_freedom": (
                "[tr(P C)]^2/tr[(P C)^2]"
            ),
        },
        "spacing_sweep": spacing_cases,
        "fixed_field_of_view_oversampling": {
            "coarse": coarse,
            "fine": fine,
            "nominal_pixel_ratio": (
                fine["nominal_sample_count"] / coarse["nominal_sample_count"]
            ),
            "map_mean_effective_information_gain_fraction": information_gain,
            "naive_variance_ratio_change": (
                fine["naive_sample_variance_ratio"]
                - coarse["naive_sample_variance_ratio"]
            ),
        },
        "headline": {
            "dense_nominal_sample_count": dense["nominal_sample_count"],
            "dense_map_mean_effective_sample_count": (
                dense["map_mean_effective_sample_count"]
            ),
            "dense_naive_sample_variance_ratio": (
                dense["naive_sample_variance_ratio"]
            ),
            "dense_variance_effective_degrees_of_freedom": (
                dense["variance_effective_degrees_of_freedom"]
            ),
            "fourfold_pixel_increase_information_gain_fraction": information_gain,
            "nearly_independent_map_mean_effective_sample_count": (
                nearly_independent["map_mean_effective_sample_count"]
            ),
            "nearly_independent_naive_sample_variance_ratio": (
                nearly_independent["naive_sample_variance_ratio"]
            ),
        },
        "allocation_connection": [
            "Repeat counts in the allocation theorem represent independent realizations or covariance-weighted information, not nominal raster pixels.",
            "Increasing raster density at fixed field of view does not create new material realizations.",
            "Use the full covariance matrix when accurate inference is required; effective counts are summaries.",
        ],
        "claim_boundaries": [
            "Gaussian-process filtering and Gaussian quadratic-form moments are established mathematics.",
            "The spacing sweep is a controlled model calculation, not a specimen scan-pitch prescription.",
            "The effective variance degrees of freedom are moment matched, not an exact chi-square law for arbitrary covariance spectra.",
            "No specimen covariance, correlation length, or disorder amplitude is inferred.",
            "This result does not authorize a manuscript.",
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
