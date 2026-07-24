"""Audit reconstruction, fit-domain, weighting, and model adequacy for Moazzami spectra.

This module is deliberately deterministic.  Its outputs are sensitivity and leverage
records, not probability distributions or experimental uncertainty intervals.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from mct_research.absorption_edge_uncertainty import chu_1994_beta_ev_inverse

GRID_POINTS = 4001
FIT_MINIMA_CM1 = (400.0, 600.0, 800.0, 1000.0)
FIT_MAXIMA_CM1 = (3000.0, 4000.0, 5000.0)
WEIGHTING_RULES = ("uniform_points", "energy_interval", "log_absorption_interval")

SPECIMENS = (
    {
        "specimen_id": "moazzami2005_x0.226",
        "csv": "data/manuscript/moazzami2005_figure6a_irse_digitized.csv",
        "calibration": "data/manuscript/moazzami2005_figure6a_irse_calibration.json",
    },
    {
        "specimen_id": "moazzami2005_x0.310",
        "csv": "data/manuscript/moazzami2005_figure6b_irse_digitized.csv",
        "calibration": "data/manuscript/moazzami2005_figure6b_irse_calibration.json",
    },
)


def _read_csv(path: Path) -> dict[str, np.ndarray]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"empty spectrum file: {path}")
    columns = {
        name: np.asarray([float(row[name]) for row in rows], dtype=float)
        for name in rows[0]
    }
    if np.any(np.diff(columns["energy_ev"]) <= 0.0):
        raise ValueError("energy must be strictly increasing")
    return columns


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _pixel_y_to_log10_alpha(pixel_y: np.ndarray, calibration: dict[str, Any]) -> np.ndarray:
    axis = calibration["axis_calibration"]
    anchor = axis["absorption_anchor_1"]
    slope = float(axis["log10_absorption_per_pixel"])
    return math.log10(float(anchor["absorption_cm1"])) + slope * (
        np.asarray(pixel_y, dtype=float) - float(anchor["pixel_y"])
    )


def _pava(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Return weighted nondecreasing isotonic regression by pooled adjacent violators."""

    y = np.asarray(values, dtype=float)
    w = np.asarray(weights, dtype=float)
    if y.ndim != 1 or w.shape != y.shape or np.any(w <= 0.0):
        raise ValueError("PAVA inputs must be aligned one-dimensional positive-weight arrays")
    means: list[float] = []
    masses: list[float] = []
    starts: list[int] = []
    ends: list[int] = []
    for index, (value, mass) in enumerate(zip(y, w, strict=True)):
        means.append(float(value))
        masses.append(float(mass))
        starts.append(index)
        ends.append(index + 1)
        while len(means) >= 2 and means[-2] > means[-1]:
            combined_mass = masses[-2] + masses[-1]
            combined_mean = (
                masses[-2] * means[-2] + masses[-1] * means[-1]
            ) / combined_mass
            means[-2:] = [combined_mean]
            masses[-2:] = [combined_mass]
            ends[-2:] = [ends[-1]]
            starts.pop()
    fitted = np.empty_like(y)
    for mean, start, end in zip(means, starts, ends, strict=True):
        fitted[start:end] = mean
    return fitted


def _quadrature_weights(coordinate: np.ndarray) -> np.ndarray:
    x = np.asarray(coordinate, dtype=float)
    if x.ndim != 1 or x.size < 3:
        raise ValueError("coordinate must contain at least three points")
    delta = np.abs(np.diff(x))
    positive = delta[delta > 0.0]
    floor = float(np.min(positive)) * 0.25 if positive.size else 1.0
    delta = np.maximum(delta, floor)
    weights = np.empty_like(x)
    weights[0] = 0.5 * delta[0]
    weights[-1] = 0.5 * delta[-1]
    weights[1:-1] = 0.5 * (delta[:-1] + delta[1:])
    weights *= x.size / np.sum(weights)
    return weights


def _weights(rule: str, energy: np.ndarray, absorption: np.ndarray) -> np.ndarray:
    if rule == "uniform_points":
        return np.ones_like(energy)
    if rule == "energy_interval":
        return _quadrature_weights(energy)
    if rule == "log_absorption_interval":
        return _quadrature_weights(np.log(absorption))
    raise ValueError(f"unknown weighting rule: {rule}")


def _weighted_fractional_fit(
    energy: np.ndarray,
    absorption: np.ndarray,
    weights: np.ndarray,
    bounds: tuple[float, float],
    exponent: float | None,
) -> dict[str, float]:
    edges = np.linspace(float(bounds[0]), float(bounds[1]), GRID_POINTS)
    predictor = np.log(energy[None, :] - edges[:, None])
    target = np.log(absorption * energy)
    w = weights[None, :]
    sw = float(np.sum(weights))
    sx = np.sum(w * predictor, axis=1)
    sy = float(np.sum(weights * target))
    if exponent is None:
        sxx = np.sum(w * predictor * predictor, axis=1)
        sxy = np.sum(w * predictor * target[None, :], axis=1)
        denominator = sxx - sx * sx / sw
        fitted_p = (sxy - sx * sy / sw) / denominator
        intercept = (sy - fitted_p * sx) / sw
        valid = np.isfinite(fitted_p) & (fitted_p >= 0.2) & (fitted_p <= 1.5)
    else:
        fitted_p = np.full(edges.shape, float(exponent))
        intercept = (sy - fitted_p * sx) / sw
        valid = np.ones(edges.shape, dtype=bool)
    predicted = intercept[:, None] + fitted_p[:, None] * predictor
    mse = np.sum(w * (target[None, :] - predicted) ** 2, axis=1) / sw
    mse[~valid] = np.inf
    index = int(np.argmin(mse))
    if not np.isfinite(mse[index]):
        raise RuntimeError("no valid fractional-power fit")
    step = (float(bounds[1]) - float(bounds[0])) / (GRID_POINTS - 1)
    return {
        "edge_ev": float(edges[index]),
        "amplitude": float(np.exp(intercept[index])),
        "exponent": float(fitted_p[index]),
        "log_mean_square_error": float(mse[index]),
        "boundary_limited": bool(
            abs(edges[index] - float(bounds[0])) <= 0.5 * step
            or abs(edges[index] - float(bounds[1])) <= 0.5 * step
        ),
    }


def _weighted_chu_fit(
    energy: np.ndarray,
    absorption: np.ndarray,
    weights: np.ndarray,
    bounds: tuple[float, float],
    composition_x: float,
    temperature_k: float,
) -> dict[str, float]:
    beta = chu_1994_beta_ev_inverse(composition_x, temperature_k)
    edges = np.linspace(float(bounds[0]), float(bounds[1]), GRID_POINTS)
    predictor = np.sqrt(beta * (energy[None, :] - edges[:, None]))
    target = np.log(absorption)
    sw = float(np.sum(weights))
    intercept = np.sum(weights[None, :] * (target[None, :] - predictor), axis=1) / sw
    predicted = intercept[:, None] + predictor
    mse = np.sum(weights[None, :] * (target[None, :] - predicted) ** 2, axis=1) / sw
    index = int(np.argmin(mse))
    step = (float(bounds[1]) - float(bounds[0])) / (GRID_POINTS - 1)
    return {
        "edge_ev": float(edges[index]),
        "alpha_g_cm1": float(np.exp(intercept[index])),
        "beta_ev_inverse": float(beta),
        "log_mean_square_error": float(mse[index]),
        "boundary_limited": bool(
            abs(edges[index] - float(bounds[0])) <= 0.5 * step
            or abs(edges[index] - float(bounds[1])) <= 0.5 * step
        ),
    }


def _fit_models(
    energy: np.ndarray,
    absorption: np.ndarray,
    weights: np.ndarray,
    calibration: dict[str, Any],
) -> list[dict[str, Any]]:
    assumptions = calibration["contract_analysis_assumptions"]
    bounds = tuple(float(value) for value in assumptions["edge_search_bounds_ev"])
    exponents: Iterable[str | float] = assumptions["fractional_power_exponents"]
    output: list[dict[str, Any]] = []
    for exponent_value in exponents:
        exponent = None if exponent_value == "free" else float(exponent_value)
        identifier = "fractional_power_free" if exponent is None else f"fractional_power_p_{exponent:g}"
        output.append(
            {
                "candidate_id": identifier,
                "method": "fractional_power_fit",
                **_weighted_fractional_fit(energy, absorption, weights, bounds, exponent),
            }
        )
    specimen = calibration["specimen"]
    output.append(
        {
            "candidate_id": "chu_1994_kane_region",
            "method": "chu_1994_kane_region_fit",
            **_weighted_chu_fit(
                energy,
                absorption,
                weights,
                bounds,
                float(specimen["composition_x"]),
                float(specimen["temperature_k"]),
            ),
        }
    )
    return output


def _predict(candidate: dict[str, Any], energy: np.ndarray) -> np.ndarray:
    edge = float(candidate["edge_ev"])
    delta = np.maximum(energy - edge, 0.0)
    if candidate["candidate_id"] == "chu_1994_kane_region":
        return float(candidate["alpha_g_cm1"]) * np.exp(
            np.sqrt(float(candidate["beta_ev_inverse"]) * delta)
        )
    return float(candidate["amplitude"]) * delta ** float(candidate["exponent"]) / energy


def _adequacy(
    candidates: list[dict[str, Any]],
    energy: np.ndarray,
    absorption: np.ndarray,
    log10_sigma: np.ndarray,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for candidate in candidates:
        prediction = _predict(candidate, energy)
        residual = np.log10(absorption) - np.log10(prediction)
        normalized = residual / log10_sigma
        records.append(
            {
                "candidate_id": candidate["candidate_id"],
                "boundary_limited": candidate["boundary_limited"],
                "log10_rmse": float(np.sqrt(np.mean(residual**2))),
                "log10_max_absolute_residual": float(np.max(np.abs(residual))),
                "normalized_rms_using_vertical_line_halfwidth": float(
                    np.sqrt(np.mean(normalized**2))
                ),
                "fraction_within_one_vertical_halfwidth": float(
                    np.mean(np.abs(normalized) <= 1.0)
                ),
                "fraction_within_two_vertical_halfwidths": float(
                    np.mean(np.abs(normalized) <= 2.0)
                ),
            }
        )
    return records


def _edge_map(candidates: list[dict[str, Any]]) -> dict[str, float]:
    return {item["candidate_id"]: float(item["edge_ev"]) for item in candidates}


def _span(candidates: list[dict[str, Any]], *, exclude_boundary: bool) -> float:
    selected = [
        float(item["edge_ev"])
        for item in candidates
        if not exclude_boundary or not bool(item["boundary_limited"])
    ]
    return float(1000.0 * np.ptp(np.asarray(selected, dtype=float)))


def _reconstruction_variants(
    columns: dict[str, np.ndarray], calibration: dict[str, Any]
) -> dict[str, np.ndarray]:
    raw_log = _pixel_y_to_log10_alpha(columns["source_pixel_y_center"], calibration)
    sigma = np.maximum(columns["log10_absorption_sigma"], 1e-12)
    lower_log = _pixel_y_to_log10_alpha(columns["source_pixel_y_max"], calibration)
    upper_log = _pixel_y_to_log10_alpha(columns["source_pixel_y_min"], calibration)
    return {
        "committed_isotonic": columns["absorption_cm1"].copy(),
        "raw_pixel_centerline": 10.0**raw_log,
        "recomputed_unweighted_isotonic": 10.0 ** _pava(raw_log, np.ones_like(raw_log)),
        "inverse_variance_weighted_isotonic": 10.0 ** _pava(raw_log, 1.0 / sigma**2),
        "isotonic_lower_line_envelope": 10.0 ** _pava(lower_log, np.ones_like(lower_log)),
        "isotonic_upper_line_envelope": 10.0 ** _pava(upper_log, np.ones_like(upper_log)),
    }


def _analyze_specimen(root: Path, definition: dict[str, str]) -> dict[str, Any]:
    columns = _read_csv(root / definition["csv"])
    calibration = _read_json(root / definition["calibration"])
    energy = columns["energy_ev"]
    committed = columns["absorption_cm1"]
    nominal_low, nominal_high = (
        float(value)
        for value in calibration["contract_analysis_assumptions"]["fit_absorption_window_cm1"]
    )
    nominal_mask = (committed >= nominal_low) & (committed <= nominal_high)
    variants = _reconstruction_variants(columns, calibration)

    reconstruction_records: list[dict[str, Any]] = []
    for name, absorption in variants.items():
        for membership in ("fixed_committed_membership", "variant_specific_membership"):
            mask = nominal_mask if membership == "fixed_committed_membership" else (
                (absorption >= nominal_low) & (absorption <= nominal_high)
            )
            if int(np.count_nonzero(mask)) < 20:
                continue
            fit_energy = energy[mask]
            fit_absorption = absorption[mask]
            candidates = _fit_models(
                fit_energy,
                fit_absorption,
                np.ones_like(fit_energy),
                calibration,
            )
            reconstruction_records.append(
                {
                    "reconstruction": name,
                    "fit_membership": membership,
                    "fit_point_count": int(np.count_nonzero(mask)),
                    "model_edges_ev": _edge_map(candidates),
                    "full_model_span_mev": _span(candidates, exclude_boundary=False),
                    "nonboundary_model_span_mev": _span(candidates, exclude_boundary=True),
                    "boundary_limited_candidate_ids": [
                        item["candidate_id"] for item in candidates if item["boundary_limited"]
                    ],
                }
            )

    fit_grid_records: list[dict[str, Any]] = []
    for low in FIT_MINIMA_CM1:
        for high in FIT_MAXIMA_CM1:
            if low >= high:
                continue
            mask = (committed >= low) & (committed <= high)
            if int(np.count_nonzero(mask)) < 20:
                continue
            fit_energy = energy[mask]
            fit_absorption = committed[mask]
            bounds_upper = float(
                calibration["contract_analysis_assumptions"]["edge_search_bounds_ev"][1]
            )
            if bounds_upper >= float(np.min(fit_energy)):
                continue
            for rule in WEIGHTING_RULES:
                candidates = _fit_models(
                    fit_energy,
                    fit_absorption,
                    _weights(rule, fit_energy, fit_absorption),
                    calibration,
                )
                fit_grid_records.append(
                    {
                        "fit_absorption_window_cm1": [low, high],
                        "weighting_rule": rule,
                        "fit_point_count": int(np.count_nonzero(mask)),
                        "model_edges_ev": _edge_map(candidates),
                        "full_model_span_mev": _span(candidates, exclude_boundary=False),
                        "nonboundary_model_span_mev": _span(candidates, exclude_boundary=True),
                        "boundary_limited_candidate_ids": [
                            item["candidate_id"]
                            for item in candidates
                            if item["boundary_limited"]
                        ],
                    }
                )

    nominal_energy = energy[nominal_mask]
    nominal_absorption = committed[nominal_mask]
    nominal_candidates = _fit_models(
        nominal_energy,
        nominal_absorption,
        np.ones_like(nominal_energy),
        calibration,
    )
    adequacy = _adequacy(
        nominal_candidates,
        nominal_energy,
        nominal_absorption,
        columns["log10_absorption_sigma"][nominal_mask],
    )

    nominal_edges = _edge_map(nominal_candidates)
    reconstruction_max_shifts: dict[str, float] = {}
    for candidate_id, nominal_edge in nominal_edges.items():
        values = [
            record["model_edges_ev"][candidate_id]
            for record in reconstruction_records
            if record["fit_membership"] == "fixed_committed_membership"
        ]
        reconstruction_max_shifts[candidate_id] = float(
            1000.0 * np.max(np.abs(np.asarray(values) - nominal_edge))
        )

    grid_max_shifts: dict[str, float] = {}
    for candidate_id, nominal_edge in nominal_edges.items():
        values = [record["model_edges_ev"][candidate_id] for record in fit_grid_records]
        grid_max_shifts[candidate_id] = float(
            1000.0 * np.max(np.abs(np.asarray(values) - nominal_edge))
        )

    return {
        "specimen_id": definition["specimen_id"],
        "source_files": {
            "spectrum": definition["csv"],
            "calibration": definition["calibration"],
        },
        "nominal_fit_window_cm1": [nominal_low, nominal_high],
        "nominal_fit_point_count": int(np.count_nonzero(nominal_mask)),
        "recomputed_unweighted_isotonic_max_log10_difference": float(
            np.max(
                np.abs(
                    np.log10(variants["recomputed_unweighted_isotonic"])
                    - np.log10(variants["committed_isotonic"])
                )
            )
        ),
        "nominal_candidates": nominal_candidates,
        "nominal_model_adequacy_diagnostics": adequacy,
        "reconstruction_sensitivity": reconstruction_records,
        "fit_domain_and_weighting_sensitivity": fit_grid_records,
        "maximum_reconstruction_shift_mev_by_candidate": reconstruction_max_shifts,
        "maximum_fit_domain_or_weighting_shift_mev_by_candidate": grid_max_shifts,
        "decision": {
            "raw_and_alternative_reconstructions_evaluated": True,
            "fit_membership_effect_reported_separately": True,
            "fit_endpoint_grid_evaluated": True,
            "point_density_weighting_evaluated": True,
            "adequacy_metrics_are_descriptive_not_probabilistic": True,
            "fixed_absorption_thresholds_excluded_from_model_span": True,
        },
    }


def build(root: Path) -> dict[str, Any]:
    specimens = [_analyze_specimen(root, definition) for definition in SPECIMENS]
    return {
        "schema_version": "1.0",
        "analysis": "Moazzami 2005 reconstruction and fitted-model robustness",
        "methods": {
            "reconstruction_variants": [
                "committed isotonic reconstruction",
                "raw source-pixel centerline",
                "recomputed unweighted isotonic regression",
                "inverse-variance-weighted isotonic regression",
                "isotonic lower and upper source-line envelopes",
            ],
            "fit_endpoint_grid_cm1": {
                "lower": list(FIT_MINIMA_CM1),
                "upper": list(FIT_MAXIMA_CM1),
            },
            "weighting_rules": list(WEIGHTING_RULES),
            "model_class": "fitted intercept models only; fixed-alpha coordinates are excluded",
            "grid_points": GRID_POINTS,
        },
        "specimens": specimens,
        "claim_boundary": (
            "These are deterministic reconstruction, endpoint, weighting, and model-adequacy "
            "diagnostics for two bitmap-derived spectra. They are not experimental uncertainty "
            "intervals and do not identify a unique latent material gap."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-json", type=Path, required=True)
    arguments = parser.parse_args()
    result = build(arguments.repository_root.resolve())
    arguments.output_json.parent.mkdir(parents=True, exist_ok=True)
    arguments.output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
