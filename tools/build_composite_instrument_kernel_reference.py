"""Build the controlled R04 composite-instrument-kernel validation record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from mct_research.spatial_disorder_instrument import (
    CompositeInstrumentKernel,
    composite_instrument_effective_variance,
    composite_instrument_log_sensitivity,
    gaussian_psf_rectangular_pixel_axis_ratio,
    gaussian_psf_rectangular_pixel_axis_ratio_quadrature,
    moment_matched_gaussian_axis_ratio,
    propagate_composite_instrument_calibration,
)


def _case(
    *,
    correlation_lengths: list[float],
    kernel: CompositeInstrumentKernel,
    point_variance: float = 0.01,
    depth_quadrature_order: int = 160,
) -> dict[str, object]:
    result = composite_instrument_effective_variance(
        point_variance,
        correlation_lengths,
        kernel,
        depth_quadrature_order=depth_quadrature_order,
    )
    return {
        "point_variance": point_variance,
        "correlation_lengths": correlation_lengths,
        "kernel": {
            "psf_sigma_x": kernel.psf_sigma_x,
            "psf_sigma_y": kernel.psf_sigma_y,
            "pixel_width_x": kernel.pixel_width_x,
            "pixel_width_y": kernel.pixel_width_y,
            "attenuation_coefficient": kernel.attenuation_coefficient,
            "thickness": kernel.thickness,
            "side": kernel.side,
        },
        "lateral_ratio_x": result.lateral_ratio_x,
        "lateral_ratio_y": result.lateral_ratio_y,
        "depth_ratio": result.depth_ratio,
        "exact_variance_ratio": result.exact_variance_ratio,
        "effective_variance": result.effective_variance,
        "moment_matched_sigma_x": result.moment_matched_sigma_x,
        "moment_matched_sigma_y": result.moment_matched_sigma_y,
        "equivalent_gaussian_variance_ratio": (
            result.equivalent_gaussian_variance_ratio
        ),
        "equivalent_gaussian_effective_variance": (
            result.equivalent_gaussian_effective_variance
        ),
        "equivalent_gaussian_relative_error": (
            result.equivalent_gaussian_relative_error
        ),
    }


def build_reference() -> dict[str, object]:
    reference_kernel = CompositeInstrumentKernel(2.0, 2.0, 5.0, 5.0, 0.5, 10.0)
    reference_case = _case(
        correlation_lengths=[2.0, 2.0, 2.0],
        kernel=reference_kernel,
    )

    pixel_dominated_kernel = CompositeInstrumentKernel(
        3.8,
        3.8,
        44.2,
        44.2,
        0.5,
        10.0,
    )
    pixel_dominated_case = _case(
        correlation_lengths=[5.0, 5.0, 2.0],
        kernel=pixel_dominated_kernel,
        point_variance=1.0,
        depth_quadrature_order=128,
    )

    anisotropic_kernel = CompositeInstrumentKernel(
        1.0,
        3.0,
        4.0,
        12.0,
        1.0,
        8.0,
    )
    anisotropic_case = _case(
        correlation_lengths=[2.0, 4.0, 1.0],
        kernel=anisotropic_kernel,
        point_variance=1.0,
        depth_quadrature_order=128,
    )

    log_standard_deviations = np.array(
        [0.05, 0.05, 0.01, 0.01, 0.10, 0.05],
        dtype=float,
    )
    calibration = propagate_composite_instrument_calibration(
        [2.0, 2.0, 2.0],
        reference_kernel,
        np.diag(log_standard_deviations**2),
        log_step=1.0e-5,
        depth_quadrature_order=128,
    )

    psf_ratios = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0]
    pixel_ratios = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    grid: list[dict[str, float]] = []
    for psf_ratio in psf_ratios:
        for pixel_ratio in pixel_ratios:
            exact_axis = gaussian_psf_rectangular_pixel_axis_ratio(
                1.0,
                psf_ratio,
                pixel_ratio,
            )
            approximate_axis = moment_matched_gaussian_axis_ratio(
                1.0,
                psf_ratio,
                pixel_ratio,
            )
            exact_2d = exact_axis**2
            approximate_2d = approximate_axis**2
            grid.append(
                {
                    "psf_sigma_over_xi": psf_ratio,
                    "pixel_width_over_xi": pixel_ratio,
                    "exact_lateral_ratio_2d": exact_2d,
                    "equivalent_gaussian_ratio_2d": approximate_2d,
                    "relative_error": approximate_2d / exact_2d - 1.0,
                }
            )
    maximum_grid_case = max(grid, key=lambda item: item["relative_error"])
    above_one_percent = sum(item["relative_error"] > 0.01 for item in grid)

    axis_verification_cases = []
    for correlation_length, psf_sigma, pixel_width in (
        (0.2, 0.0, 1.0),
        (1.0, 0.3, 2.0),
        (2.0, 2.0, 5.0),
        (10.0, 0.1, 30.0),
    ):
        analytical = gaussian_psf_rectangular_pixel_axis_ratio(
            correlation_length,
            psf_sigma,
            pixel_width,
        )
        quadrature = gaussian_psf_rectangular_pixel_axis_ratio_quadrature(
            correlation_length,
            psf_sigma,
            pixel_width,
            quadrature_order=160,
        )
        axis_verification_cases.append(
            {
                "correlation_length": correlation_length,
                "psf_sigma": psf_sigma,
                "pixel_width": pixel_width,
                "analytical_ratio": analytical,
                "quadrature_ratio": quadrature,
                "relative_difference": quadrature / analytical - 1.0,
            }
        )

    return {
        "schema_version": "1.0",
        "program_issue": 196,
        "implementation_issue": 228,
        "portfolio_contribution": "R04",
        "status": "controlled_instrument_kernel_not_specimen_calibration",
        "model": {
            "material_covariance": "axis-aligned separable Gaussian in 3D",
            "lateral_kernel": (
                "axis-aligned elliptical Gaussian PSF convolved with a "
                "rectangular pixel or scan bin"
            ),
            "depth_kernel": (
                "normalized exponential sensitivity in a homogeneous finite slab"
            ),
            "lateral_evaluation": "analytical",
            "depth_evaluation": "deterministic Gauss-Legendre covariance quadratic form",
            "equivalent_gaussian": "axiswise second-moment matching",
        },
        "reference_case": reference_case,
        "pixel_dominated_case": pixel_dominated_case,
        "anisotropic_case": anisotropic_case,
        "calibration_case": {
            "parameter_names": list(calibration.parameter_names),
            "independent_log_standard_deviations": log_standard_deviations.tolist(),
            "log_sensitivity": calibration.log_sensitivity.tolist(),
            "log_variance_standard_deviation": (
                calibration.log_variance_standard_deviation
            ),
            "first_order_relative_standard_deviation": (
                calibration.first_order_relative_standard_deviation
            ),
            "lognormal_relative_standard_deviation": (
                calibration.lognormal_relative_standard_deviation
            ),
        },
        "equivalent_gaussian_stress_grid": {
            "psf_sigma_over_xi": psf_ratios,
            "pixel_width_over_xi": pixel_ratios,
            "case_count": len(grid),
            "cases_above_one_percent_error": above_one_percent,
            "maximum_error_case": maximum_grid_case,
        },
        "independent_axis_verification": axis_verification_cases,
        "headline": {
            "reference_exact_variance_ratio": reference_case["exact_variance_ratio"],
            "reference_equivalent_gaussian_relative_error": reference_case[
                "equivalent_gaussian_relative_error"
            ],
            "reference_calibration_relative_standard_deviation": (
                calibration.first_order_relative_standard_deviation
            ),
            "pixel_dominated_equivalent_gaussian_relative_error": (
                pixel_dominated_case["equivalent_gaussian_relative_error"]
            ),
            "stress_grid_maximum_relative_error": maximum_grid_case[
                "relative_error"
            ],
            "stress_grid_cases_above_one_percent": above_one_percent,
        },
        "claim_boundaries": [
            "The model is a declared representative separable kernel, not a universal instrument PSF.",
            "The analytical result applies to axis-aligned separable Gaussian covariance and lateral kernels.",
            "The finite-depth Gaussian factor is evaluated by deterministic quadrature rather than a new closed finite-slab formula.",
            "Moment matching preserves the lateral kernel covariance but not its full shape.",
            "The stress grid is dimensionless controlled analysis, not a survey of commercial instruments.",
            "The calibration case is synthetic and does not estimate a specimen correlation length.",
            "No covariance family, specimen parameter, manuscript, or novelty claim is authorized."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "data/validation/spatial_disorder_composite_instrument_kernel.json"
        ),
    )
    arguments = parser.parse_args()
    record = build_reference()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
