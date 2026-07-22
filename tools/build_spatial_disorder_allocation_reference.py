#!/usr/bin/env python3
"""Build the deterministic R04 multiscale probe-allocation reference."""

from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path
from typing import Any

import numpy as np

from mct_research.spatial_disorder_allocation import (
    endpoint_d_optimal_allocation,
    gaussian_allocation_diagnostics,
    gaussian_log_correlation_sensitivity,
    optimize_three_scale_allocation,
)


def _float_list(values: Any) -> list[float]:
    return [float(value) for value in np.asarray(values).ravel()]


def _matrix(values: Any) -> list[list[float]]:
    array = np.asarray(values, dtype=float)
    return [[float(value) for value in row] for row in array]


def _design_record(total_repeats: int) -> dict[str, Any]:
    result = optimize_three_scale_allocation(
        0.01,
        1.0,
        [0.1, 1.0, 2.0],
        total_repeats,
        single_repeat_relative_standard_deviation=0.03,
        minimum_middle_repeats=1,
        minimum_d_efficiency=0.8,
        common_log_scale_standard_deviation=0.02,
    )
    design = result.recommended
    allocation = design.allocation
    return {
        "total_repeats": total_repeats,
        "recommended_repeats": [int(value) for value in allocation.repeats],
        "d_efficiency": allocation.d_efficiency,
        "worst_case_absolute_standardized_residual": (
            design.worst_case_absolute_standardized_residual
        ),
        "mean_absolute_standardized_residual": (
            design.mean_absolute_standardized_residual
        ),
        "matern_smoothness": _float_list(design.matern_smoothness),
        "standardized_family_residuals": _float_list(
            design.standardized_family_residuals
        ),
        "relative_parameter_covariance": _matrix(
            allocation.parameter_covariance_relative_scale
        ),
        "absolute_parameter_covariance": _matrix(
            allocation.parameter_covariance_absolute_scale
        ),
        "relative_log_xi_standard_deviation": (
            allocation.log_correlation_length_relative_standard_deviation
        ),
        "absolute_log_xi_standard_deviation": (
            allocation.log_correlation_length_absolute_standard_deviation
        ),
        "pareto_front_size": len(result.pareto_front),
    }


def build_reference() -> dict[str, Any]:
    sensitivities = gaussian_log_correlation_sensitivity([0.1, 2.0], 1.0)
    lower_sensitivity, upper_sensitivity = map(float, sensitivities)
    a_optimal_lower_fraction = sqrt(1.0 + upper_sensitivity**2) / (
        sqrt(1.0 + lower_sensitivity**2)
        + sqrt(1.0 + upper_sensitivity**2)
    )

    endpoint_30 = gaussian_allocation_diagnostics(
        0.01,
        1.0,
        [0.1, 2.0],
        endpoint_d_optimal_allocation(30),
        single_repeat_relative_standard_deviation=0.03,
        common_log_scale_standard_deviation=0.02,
    )

    tradeoff = []
    for floor in (0.95, 0.90, 0.80, 0.70, 0.60):
        result = optimize_three_scale_allocation(
            0.01,
            1.0,
            [0.1, 1.0, 2.0],
            30,
            single_repeat_relative_standard_deviation=0.03,
            minimum_middle_repeats=1,
            minimum_d_efficiency=floor,
        )
        design = result.recommended
        tradeoff.append(
            {
                "minimum_d_efficiency": floor,
                "recommended_repeats": [
                    int(value) for value in design.allocation.repeats
                ],
                "achieved_d_efficiency": design.allocation.d_efficiency,
                "worst_case_absolute_standardized_residual": (
                    design.worst_case_absolute_standardized_residual
                ),
            }
        )

    return {
        "schema_version": "1.0",
        "program_issue": 196,
        "implementation_issue": 230,
        "portfolio_contribution": "R04",
        "status": "local_optimal_design_not_specimen_prescription",
        "model": {
            "variance": "A/(1+2s^2/xi^2)",
            "parameters": ["log A", "log xi"],
            "single_repeat_relative_standard_deviation": 0.03,
            "candidate_scale_ratios": [0.1, 1.0, 2.0],
            "common_log_scale_standard_deviation": 0.02,
        },
        "exact_theorems": {
            "log_xi_sensitivity": "4(s/xi)^2/[1+2(s/xi)^2]",
            "fisher_determinant": (
                "N sum_i n_i(g_i-g_bar)^2 / sigma_y^4"
            ),
            "continuous_d_optimal_support": "equal weight at feasible endpoints",
            "integer_d_optimal_counts": "floor(N/2), ceil(N/2)",
            "correlation_length_variance": (
                "sigma_y^2 N/[n_low n_high (g_high-g_low)^2]"
            ),
            "a_optimal_lower_endpoint_fraction": a_optimal_lower_fraction,
            "common_scale_floor": (
                "Var(log xi_absolute)=Var(log xi_relative)+tau_scale^2"
            ),
        },
        "endpoint_reference_30": {
            "repeats": [int(value) for value in endpoint_30.repeats],
            "sensitivity_endpoints": [lower_sensitivity, upper_sensitivity],
            "fisher_determinant": endpoint_30.fisher_determinant,
            "d_efficiency": endpoint_30.d_efficiency,
            "relative_parameter_covariance": _matrix(
                endpoint_30.parameter_covariance_relative_scale
            ),
            "absolute_parameter_covariance": _matrix(
                endpoint_30.parameter_covariance_absolute_scale
            ),
            "relative_log_xi_standard_deviation": (
                endpoint_30.log_correlation_length_relative_standard_deviation
            ),
            "absolute_log_xi_standard_deviation": (
                endpoint_30.log_correlation_length_absolute_standard_deviation
            ),
        },
        "three_scale_recommendations": [
            _design_record(total) for total in (12, 30, 60)
        ],
        "thirty_repeat_precision_falsification_tradeoff": tradeoff,
        "claim_boundaries": [
            "Optimal-design, Fisher, Popoviciu, and Neyman-allocation mathematics are established.",
            "The physical scales are local design ratios relative to a declared correlation length, not universal spot sizes.",
            "The common absolute-scale calibration floor cannot be removed by repeat allocation.",
            "The Matérn residuals are controlled synthetic family-separation diagnostics, not specimen covariance evidence.",
            "This result does not authorize a manuscript or prescribe a laboratory instrument configuration.",
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
    print(output)


if __name__ == "__main__":
    main()
