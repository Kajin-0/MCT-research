#!/usr/bin/env python3
"""Generate the frozen restricted R04 result for the Bowman CdSeTe map."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import urllib.request
import zipfile
from typing import Any

import numpy as np

from mct_research.spatial_disorder_real_data import (
    FamilyFit,
    SourceMap,
    analyze_real_map,
    read_bowman_map_csv,
)

DATASET_URL = "https://zenodo.org/records/13869384/files/Datasets.zip?download=1"
ARCHIVE_MD5 = "1401ee9b5372edb78f888d152940fc79"
ARCHIVE_SHA256 = "cc3e1ce1a02266da2d0e0f301464a9d8a519855f33a597adeb7f16048684c9a6"
SOURCE_MEMBER = "Datasets/Figure 3e.csv"
SOURCE_MEMBER_SHA256 = "49422bda851686db62574fb30354d698138f221db4b66d8782e0717698bc5679"


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def acquire_archive(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        request = urllib.request.Request(
            DATASET_URL,
            headers={"User-Agent": "MCT-research-R04-CdSeTe-demonstration/1.0"},
        )
        partial = destination.with_suffix(destination.suffix + ".partial")
        partial.unlink(missing_ok=True)
        with urllib.request.urlopen(request, timeout=120) as response, partial.open("wb") as out:
            shutil.copyfileobj(response, out, length=1024 * 1024)
        partial.replace(destination)
    observed_md5 = digest(destination, "md5")
    observed_sha256 = digest(destination, "sha256")
    if observed_md5 != ARCHIVE_MD5 or observed_sha256 != ARCHIVE_SHA256:
        raise RuntimeError(
            "public archive failed immutable identity: "
            f"md5={observed_md5}, sha256={observed_sha256}"
        )


def extract_source_member(archive: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as source:
        names = source.namelist()
        if SOURCE_MEMBER not in names:
            raise RuntimeError(f"archive does not contain {SOURCE_MEMBER!r}")
        with source.open(SOURCE_MEMBER) as incoming, destination.open("wb") as outgoing:
            shutil.copyfileobj(incoming, outgoing)
    observed = digest(destination, "sha256")
    if observed != SOURCE_MEMBER_SHA256:
        raise RuntimeError(
            f"source member failed immutable SHA-256: expected {SOURCE_MEMBER_SHA256}, got {observed}"
        )


def normalize_rounded_coordinates(source: SourceMap) -> tuple[SourceMap, dict[str, float]]:
    x = np.asarray(source.x)
    y = np.asarray(source.y)
    ideal_x = np.linspace(float(x[0]), float(x[-1]), x.size)
    ideal_y = np.linspace(float(y[0]), float(y[-1]), y.size)
    max_x = float(np.max(np.abs(x - ideal_x)))
    max_y = float(np.max(np.abs(y - ideal_y)))
    tolerance = 1.0e-3
    if max_x > tolerance or max_y > tolerance:
        raise ValueError(
            "coordinate rounding exceeds the declared endpoint-linear normalization tolerance"
        )
    normalized = SourceMap(
        x=ideal_x,
        y=ideal_y,
        values=source.values,
        note=source.note,
    )
    return normalized, {
        "maximum_x_rounding_residual_micrometre": max_x,
        "maximum_y_rounding_residual_micrometre": max_y,
        "normalization_tolerance_micrometre": tolerance,
        "normalized_spacing_micrometre": float(
            (ideal_x[1] - ideal_x[0] + ideal_y[1] - ideal_y[0]) / 2.0
        ),
    }


def serialize(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not np.isfinite(value):
            raise ValueError("result contains a nonfinite float")
        return value
    if isinstance(value, np.generic):
        return serialize(value.item())
    if isinstance(value, np.ndarray):
        return serialize(value.tolist())
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    raise TypeError(f"cannot serialize {type(value)!r}")


def family_record(fit: FamilyFit) -> dict[str, Any]:
    return {
        "family": fit.family,
        "descriptive_point_variance_nm2": fit.point_variance,
        "descriptive_correlation_scale_pixels": fit.correlation_scale_pixels,
        "predicted_variances_nm2": fit.predicted_variances,
        "training_log_rms": fit.training_log_rms,
        "held_out_signed_relative_error": fit.held_out_signed_relative_error,
        "held_out_absolute_relative_error": fit.held_out_absolute_relative_error,
    }


def build_result(protocol: dict[str, Any], source_path: Path) -> dict[str, Any]:
    declared_scales = protocol["primary_numerical_kernel_sweep"]["added_sigma_pixels"]
    declared_training = protocol["training_and_holdout"]["training_sigma_pixels"]
    declared_holdout = protocol["training_and_holdout"]["held_out_sigma_pixels"]
    scales = np.asarray(declared_scales, dtype=float)
    training_indices = [
        int(np.flatnonzero(np.isclose(scales, float(scale), rtol=0.0, atol=1.0e-14))[0])
        for scale in declared_training
    ]
    held_out_index = int(
        np.flatnonzero(np.isclose(scales, float(declared_holdout), rtol=0.0, atol=1.0e-14))[0]
    )

    parsed = read_bowman_map_csv(source_path)
    source, coordinate_record = normalize_rounded_coordinates(parsed)
    result = analyze_real_map(
        source,
        scales_pixels=scales,
        training_indices=training_indices,
        held_out_index=held_out_index,
        crop_rows=slice(4, 20),
        crop_columns=slice(4, 20),
        surrogate_seed=int(protocol["synthetic_control"]["seed"]),
        truncate=float(protocol["primary_numerical_kernel_sweep"]["truncate_standard_deviations"]),
    )

    family_records = [family_record(fit) for fit in result.family_fits]
    best_training = min(family_records, key=lambda item: item["training_log_rms"])["family"]
    best_holdout = min(
        family_records, key=lambda item: item["held_out_absolute_relative_error"]
    )["family"]
    primary = np.asarray(result.primary_variances)

    return serialize(
        {
            "schema_version": "1.0",
            "portfolio_contribution": "R04",
            "issue": 317,
            "result_date": "2026-07-23",
            "decision": "RESTRICTED_REAL_DATA_DEMONSTRATION_COMPLETE",
            "source": {
                "article_doi": protocol["source"]["article_doi"],
                "dataset_doi": protocol["source"]["dataset_doi"],
                "archive_sha256": ARCHIVE_SHA256,
                "archive_member": SOURCE_MEMBER,
                "archive_member_sha256": SOURCE_MEMBER_SHA256,
                "license": "CC-BY-4.0",
            },
            "protocol": {
                "path": "data/validation/r04_cdsete_phase2_protocol.json",
                "status": protocol["protocol_status"],
                "primary_edge_mode": protocol["primary_numerical_kernel_sweep"]["primary_edge_mode"],
                "variance_ddof": protocol["variance_estimator"]["ddof"],
                "training_sigma_pixels": declared_training,
                "held_out_sigma_pixels": declared_holdout,
                "formal_scale_grid_changed_after_result": False,
            },
            "coordinate_normalization": coordinate_record,
            "field": {
                "shape": list(source.values.shape),
                "observable": protocol["primary_field"]["observable"],
                "units": protocol["primary_field"]["units"],
                "mean_nm": result.source_mean,
                "sample_variance_nm2": result.source_sample_variance,
                "sample_standard_deviation_nm": float(np.sqrt(result.source_sample_variance)),
                "minimum_nm": float(np.min(source.values)),
                "maximum_nm": float(np.max(source.values)),
                "missing_or_nonfinite_count": int(
                    np.size(source.values) - np.count_nonzero(np.isfinite(source.values))
                ),
            },
            "primary_added_kernel_sweep": {
                "sigma_pixels": result.scales_pixels,
                "sigma_coordinate_conversion_micrometre": result.scales_micrometre,
                "sample_variance_nm2": result.primary_variances,
                "variance_fraction_of_unsmoothed": primary / primary[0],
                "interpretation": "unknown native instrument kernel convolved with declared added numerical kernels",
            },
            "family_diagnostics": {
                "fit_loss": protocol["covariance_family_diagnostics"]["fit_loss"],
                "records": family_records,
                "lowest_training_log_rms_family": best_training,
                "lowest_held_out_absolute_error_family": best_holdout,
                "selection_status": "descriptive only; no universal-family or independent-prediction claim",
                "gaussian_reciprocal_fit": {
                    "point_variance_nm2": result.reciprocal_fit_point_variance,
                    "correlation_scale_pixels": result.reciprocal_fit_correlation_scale_pixels,
                    "maximum_absolute_relative_variance_residual": result.reciprocal_fit_maximum_relative_residual,
                },
            },
            "same_raster_gaussian_model_conditioned": {
                "finite_map_bias_factors": result.gaussian_bias_factors,
                "delta_log_variance_covariance": result.gaussian_log_variance_covariance,
                "cross_scale_correlation": result.gaussian_cross_scale_correlation,
                "moment_matched_effective_degrees_of_freedom": result.gaussian_effective_degrees_of_freedom,
                "parameter_standard_deviation_inflation_vs_false_independence": result.gaussian_parameter_sd_inflation,
                "parameter_covariance_determinant_inflation_vs_false_independence": result.gaussian_parameter_covariance_determinant_inflation,
                "status": "exact quadratic-form result conditional on fitted descriptive Gaussian covariance; not empirical repeat covariance",
            },
            "sensitivity": {
                "full_reflect_variances_nm2": result.primary_variances,
                "full_wrap_variances_nm2": result.wrap_variances,
                "full_nearest_variances_nm2": result.nearest_variances,
                "central_16x16_reflect_variances_nm2": result.crop_variances,
                "planar_detrended_full_reflect_variances_nm2": result.planar_detrended_variances,
                "maximum_relative_difference_wrap_vs_reflect": float(
                    np.max(np.abs((np.asarray(result.wrap_variances) - primary) / primary))
                ),
                "maximum_relative_difference_nearest_vs_reflect": float(
                    np.max(np.abs((np.asarray(result.nearest_variances) - primary) / primary))
                ),
                "maximum_relative_difference_crop_vs_full_reflect": float(
                    np.max(np.abs((np.asarray(result.crop_variances) - primary) / primary))
                ),
                "maximum_relative_difference_planar_detrended_vs_primary": float(
                    np.max(
                        np.abs(
                            (np.asarray(result.planar_detrended_variances) - primary)
                            / primary
                        )
                    )
                ),
            },
            "phase_randomized_control": {
                "seed": protocol["synthetic_control"]["seed"],
                "mean_residual_nm": result.surrogate_mean_residual,
                "sample_variance_relative_residual": result.surrogate_variance_relative_residual,
                "wrap_variance_maximum_relative_residual": result.surrogate_wrap_variance_maximum_relative_residual,
                "reflect_variances_nm2": result.surrogate_reflect_variances,
                "status": "power-spectrum-preserving control; not a semiconductor mechanism model",
            },
            "claim_boundary": {
                "real_semiconductor_method_demonstration": True,
                "hgcdte_external_validation": False,
                "native_kernel_deconvolution": False,
                "latent_physical_correlation_length": False,
                "composition_assignment": False,
                "independent_scale_claim": False,
                "universal_covariance_family": False,
                "r05": False,
                "manuscript": False,
            },
        }
    )


def render_markdown(result: dict[str, Any]) -> str:
    sweep = result["primary_added_kernel_sweep"]
    families = result["family_diagnostics"]
    dependence = result["same_raster_gaussian_model_conditioned"]
    sensitivity = result["sensitivity"]
    lines = [
        "# CdSeTe real-map R04 demonstration result",
        "",
        "## Decision",
        "",
        "```text",
        result["decision"],
        "```",
        "",
        "This is a restricted demonstration on a source-data-derived CdSeTe PL",
        "peak-wavelength map. It is not HgCdTe validation and does not identify a",
        "native physical correlation length because the sample-plane instrument",
        "kernel is unmeasured.",
        "",
        "## Primary added-kernel sweep",
        "",
        "```text",
        f"sigma pixels       {sweep['sigma_pixels']}",
        f"variance nm^2      {sweep['sample_variance_nm2']}",
        f"fraction raw       {sweep['variance_fraction_of_unsmoothed']}",
        "```",
        "",
        "## Descriptive family fits",
        "",
    ]
    for record in families["records"]:
        lines.append(
            "- {family}: train log-RMS `{rms:.6g}`, held-out relative error "
            "`{error:+.6%}`, descriptive scale `{scale:.6g} px`.".format(
                family=record["family"],
                rms=record["training_log_rms"],
                error=record["held_out_signed_relative_error"],
                scale=record["descriptive_correlation_scale_pixels"],
            )
        )
    lines.extend(
        [
            "",
            "These are closure diagnostics on deterministic transforms of one",
            "raster, not independent model validation or a universal-family result.",
            "",
            "## Same-raster dependence",
            "",
            "```text",
            f"bias factors                 {dependence['finite_map_bias_factors']}",
            f"effective variance dof        {dependence['moment_matched_effective_degrees_of_freedom']}",
            f"parameter SD inflation        {dependence['parameter_standard_deviation_inflation_vs_false_independence']}",
            f"covariance determinant ratio  {dependence['parameter_covariance_determinant_inflation_vs_false_independence']:.6g}",
            "```",
            "",
            "The covariance is exact only conditional on the fitted descriptive",
            "Gaussian field model. It is not empirical repeat covariance.",
            "",
            "## Sensitivity",
            "",
            "```text",
            f"max wrap/reflect difference       {sensitivity['maximum_relative_difference_wrap_vs_reflect']:.6%}",
            f"max nearest/reflect difference    {sensitivity['maximum_relative_difference_nearest_vs_reflect']:.6%}",
            f"max crop/full difference          {sensitivity['maximum_relative_difference_crop_vs_full_reflect']:.6%}",
            f"max detrended/primary difference  {sensitivity['maximum_relative_difference_planar_detrended_vs_primary']:.6%}",
            "```",
            "",
            "## Claim boundary",
            "",
            "No HgCdTe validation, composition assignment, native-kernel",
            "deconvolution, independent-scale claim, R05 activation, or manuscript",
            "authorization follows from this result.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-markdown", type=Path, required=True)
    args = parser.parse_args()

    protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    archive = args.workdir / "Datasets.zip"
    member = args.workdir / SOURCE_MEMBER
    acquire_archive(archive)
    extract_source_member(archive, member)
    result = build_result(protocol, member)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.output_markdown.write_text(render_markdown(result), encoding="utf-8")
    print(args.output_markdown.read_text(encoding="utf-8"))
    print(f"result JSON: {args.output_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
