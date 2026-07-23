"""Safe entry point for the Moazzami reconstruction and fit-domain audit.

Some reconstruction-specific fit populations begin below a predeclared edge-search
upper bound. Such scenarios are inadmissible for the declared grid and are exported
as exclusions rather than silently changing the search bounds.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from tools import audit_moazzami2005_model_robustness as core

SCREEN_RMS_THRESHOLDS = (0.75, 1.0, 1.25, 1.5)
SCREEN_TWO_HALFWIDTH_COVERAGE = (0.90, 0.95, 0.975)


def _screen_sensitivity(
    candidates: list[dict[str, Any]], adequacy: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    edge_map = core._edge_map(candidates)
    records: list[dict[str, Any]] = []
    for rms_threshold in SCREEN_RMS_THRESHOLDS:
        for coverage_threshold in SCREEN_TWO_HALFWIDTH_COVERAGE:
            retained = [
                item["candidate_id"]
                for item in adequacy
                if not item["boundary_limited"]
                and item["normalized_rms_using_vertical_line_halfwidth"]
                <= rms_threshold
                and item["fraction_within_two_vertical_halfwidths"]
                >= coverage_threshold
            ]
            edges = np.asarray([edge_map[item] for item in retained], dtype=float)
            records.append(
                {
                    "normalized_rms_maximum": rms_threshold,
                    "minimum_fraction_within_two_vertical_halfwidths": coverage_threshold,
                    "retained_candidate_ids": retained,
                    "retained_candidate_count": len(retained),
                    "retained_span_mev": (
                        None if edges.size < 2 else float(1000.0 * np.ptp(edges))
                    ),
                }
            )
    return records


def _residual_records(
    candidates: list[dict[str, Any]],
    energy: np.ndarray,
    absorption: np.ndarray,
    log10_sigma: np.ndarray,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for candidate in candidates:
        prediction = core._predict(candidate, energy)
        residual = np.log10(absorption) - np.log10(prediction)
        records.append(
            {
                "candidate_id": candidate["candidate_id"],
                "boundary_limited": candidate["boundary_limited"],
                "predicted_absorption_cm1": prediction.tolist(),
                "residual_log10_absorption": residual.tolist(),
                "normalized_residual_by_vertical_line_halfwidth": (
                    residual / log10_sigma
                ).tolist(),
            }
        )
    return records


def _analyze_specimen(root: Path, definition: dict[str, str]) -> dict[str, Any]:
    columns = core._read_csv(root / definition["csv"])
    calibration = core._read_json(root / definition["calibration"])
    energy = columns["energy_ev"]
    committed = columns["absorption_cm1"]
    nominal_low, nominal_high = (
        float(value)
        for value in calibration["contract_analysis_assumptions"][
            "fit_absorption_window_cm1"
        ]
    )
    bounds_upper = float(
        calibration["contract_analysis_assumptions"]["edge_search_bounds_ev"][1]
    )
    nominal_mask = (committed >= nominal_low) & (committed <= nominal_high)
    variants = core._reconstruction_variants(columns, calibration)

    reconstruction_records: list[dict[str, Any]] = []
    reconstruction_exclusions: list[dict[str, Any]] = []
    for name, absorption in variants.items():
        for membership in ("fixed_committed_membership", "variant_specific_membership"):
            mask = nominal_mask if membership == "fixed_committed_membership" else (
                (absorption >= nominal_low) & (absorption <= nominal_high)
            )
            point_count = int(np.count_nonzero(mask))
            if point_count < 20:
                reconstruction_exclusions.append(
                    {
                        "reconstruction": name,
                        "fit_membership": membership,
                        "fit_point_count": point_count,
                        "reason": "fewer than 20 fitted coordinates",
                    }
                )
                continue
            fit_energy = energy[mask]
            if bounds_upper >= float(np.min(fit_energy)):
                reconstruction_exclusions.append(
                    {
                        "reconstruction": name,
                        "fit_membership": membership,
                        "fit_point_count": point_count,
                        "minimum_fitted_energy_ev": float(np.min(fit_energy)),
                        "declared_edge_search_upper_ev": bounds_upper,
                        "reason": (
                            "declared edge-search upper bound is not below the fitted "
                            "energy population; scenario excluded without changing bounds"
                        ),
                    }
                )
                continue
            fit_absorption = absorption[mask]
            candidates = core._fit_models(
                fit_energy,
                fit_absorption,
                np.ones_like(fit_energy),
                calibration,
            )
            reconstruction_records.append(
                {
                    "reconstruction": name,
                    "fit_membership": membership,
                    "fit_point_count": point_count,
                    "model_edges_ev": core._edge_map(candidates),
                    "full_model_span_mev": core._span(
                        candidates, exclude_boundary=False
                    ),
                    "nonboundary_model_span_mev": core._span(
                        candidates, exclude_boundary=True
                    ),
                    "boundary_limited_candidate_ids": [
                        item["candidate_id"]
                        for item in candidates
                        if item["boundary_limited"]
                    ],
                }
            )

    fit_grid_records: list[dict[str, Any]] = []
    fit_grid_exclusions: list[dict[str, Any]] = []
    for low in core.FIT_MINIMA_CM1:
        for high in core.FIT_MAXIMA_CM1:
            if low >= high:
                continue
            mask = (committed >= low) & (committed <= high)
            point_count = int(np.count_nonzero(mask))
            if point_count < 20:
                fit_grid_exclusions.append(
                    {
                        "fit_absorption_window_cm1": [low, high],
                        "reason": "fewer than 20 fitted coordinates",
                    }
                )
                continue
            fit_energy = energy[mask]
            if bounds_upper >= float(np.min(fit_energy)):
                fit_grid_exclusions.append(
                    {
                        "fit_absorption_window_cm1": [low, high],
                        "minimum_fitted_energy_ev": float(np.min(fit_energy)),
                        "declared_edge_search_upper_ev": bounds_upper,
                        "reason": (
                            "declared edge-search upper bound is not below the fitted "
                            "energy population; scenario excluded without changing bounds"
                        ),
                    }
                )
                continue
            fit_absorption = committed[mask]
            for rule in core.WEIGHTING_RULES:
                candidates = core._fit_models(
                    fit_energy,
                    fit_absorption,
                    core._weights(rule, fit_energy, fit_absorption),
                    calibration,
                )
                fit_grid_records.append(
                    {
                        "fit_absorption_window_cm1": [low, high],
                        "weighting_rule": rule,
                        "fit_point_count": point_count,
                        "model_edges_ev": core._edge_map(candidates),
                        "full_model_span_mev": core._span(
                            candidates, exclude_boundary=False
                        ),
                        "nonboundary_model_span_mev": core._span(
                            candidates, exclude_boundary=True
                        ),
                        "boundary_limited_candidate_ids": [
                            item["candidate_id"]
                            for item in candidates
                            if item["boundary_limited"]
                        ],
                    }
                )

    nominal_energy = energy[nominal_mask]
    nominal_absorption = committed[nominal_mask]
    nominal_sigma = columns["log10_absorption_sigma"][nominal_mask]
    nominal_candidates = core._fit_models(
        nominal_energy,
        nominal_absorption,
        np.ones_like(nominal_energy),
        calibration,
    )
    adequacy = core._adequacy(
        nominal_candidates,
        nominal_energy,
        nominal_absorption,
        nominal_sigma,
    )
    nominal_edges = core._edge_map(nominal_candidates)

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
        "nominal_fit_data": {
            "energy_ev": nominal_energy.tolist(),
            "absorption_cm1": nominal_absorption.tolist(),
            "log10_vertical_line_halfwidth": nominal_sigma.tolist(),
        },
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
        "nominal_residual_records": _residual_records(
            nominal_candidates,
            nominal_energy,
            nominal_absorption,
            nominal_sigma,
        ),
        "line_envelope_screen_sensitivity": _screen_sensitivity(
            nominal_candidates, adequacy
        ),
        "reconstruction_sensitivity": reconstruction_records,
        "excluded_reconstruction_scenarios": reconstruction_exclusions,
        "fit_domain_and_weighting_sensitivity": fit_grid_records,
        "excluded_fit_domain_scenarios": fit_grid_exclusions,
        "maximum_reconstruction_shift_mev_by_candidate": reconstruction_max_shifts,
        "maximum_fit_domain_or_weighting_shift_mev_by_candidate": grid_max_shifts,
        "decision": {
            "raw_and_alternative_reconstructions_evaluated": True,
            "fit_membership_effect_reported_separately": True,
            "inadmissible_membership_scenarios_excluded_without_changing_bounds": True,
            "fit_endpoint_grid_evaluated": True,
            "point_density_weighting_evaluated": True,
            "adequacy_metrics_are_descriptive_not_probabilistic": True,
            "screen_threshold_sensitivity_reported": True,
            "residual_versus_energy_records_exported": True,
            "fixed_absorption_thresholds_excluded_from_model_span": True,
        },
    }


def build(root: Path) -> dict[str, Any]:
    specimens = [_analyze_specimen(root, definition) for definition in core.SPECIMENS]
    return {
        "schema_version": "1.1",
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
                "lower": list(core.FIT_MINIMA_CM1),
                "upper": list(core.FIT_MAXIMA_CM1),
            },
            "weighting_rules": list(core.WEIGHTING_RULES),
            "line_envelope_screen_grid": {
                "normalized_rms_maximum": list(SCREEN_RMS_THRESHOLDS),
                "minimum_fraction_within_two_vertical_halfwidths": list(
                    SCREEN_TWO_HALFWIDTH_COVERAGE
                ),
            },
            "model_class": (
                "fitted intercept models only; fixed-alpha operational coordinates "
                "are excluded"
            ),
            "grid_points": core.GRID_POINTS,
            "infeasible_scenario_policy": (
                "exclude without changing predeclared edge-search bounds"
            ),
        },
        "specimens": specimens,
        "claim_boundary": (
            "These are deterministic reconstruction, endpoint, weighting, residual, "
            "and screen-threshold diagnostics for two bitmap-derived spectra. They "
            "are not experimental uncertainty intervals and do not identify a unique "
            "latent material gap."
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
