#!/usr/bin/env python3
"""Complete the Moazzami manuscript comparison with published Seiler 1990."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from mct_research.gap_models import (
    hansen_gap_ev,
    laurenti_gap_ev,
    provisional_hansen_pade_gap_ev,
)
from mct_research.historical_gap_models import (
    SEILER_1990_SOURCE_DOI,
    seiler_1990_gap_ev,
)
from tools.analyze_moazzami2005_real_spectra import analyze as analyze_real_spectra

MODEL_ORDER = (
    "hansen",
    "published_seiler",
    "laurenti",
    "provisional_hansen_pade",
)


def _models() -> dict[str, Callable[[float, float], float]]:
    return {
        "hansen": hansen_gap_ev,
        "published_seiler": seiler_1990_gap_ev,
        "laurenti": laurenti_gap_ev,
        "provisional_hansen_pade": provisional_hansen_pade_gap_ev,
    }


def _rank_candidate(
    candidate: dict[str, Any],
    predictions_mev: dict[str, float],
    *,
    boundary_limited: bool,
) -> dict[str, Any]:
    edge_mev = float(candidate["edge_mev"])
    residuals = {
        name: abs(edge_mev - predictions_mev[name]) for name in MODEL_ORDER
    }
    ordered = sorted(residuals, key=lambda name: (residuals[name], MODEL_ORDER.index(name)))
    winner, runner_up = ordered[:2]
    return {
        "candidate_id": candidate["candidate_id"],
        "observation_class": (
            "fixed_absorption_threshold"
            if candidate["candidate_id"].startswith("threshold_")
            else "fitted_absorption_model"
        ),
        "edge_mev": edge_mev,
        "boundary_limited": boundary_limited,
        "nominal_winner": winner,
        "nominal_runner_up": runner_up,
        "nominal_winner_margin_mev": residuals[runner_up] - residuals[winner],
        "absolute_residuals_mev": residuals,
    }


def analyze(root: str | Path) -> dict[str, Any]:
    base = analyze_real_spectra(root)
    models = _models()
    specimens: list[dict[str, Any]] = []
    all_model_winners: set[str] = set()
    all_threshold_winners: set[str] = set()

    for specimen in base["specimens"]:
        composition = float(specimen["composition_x"])
        temperature = float(specimen["temperature_k"])
        predictions = {
            name: 1000.0 * float(model(composition, temperature))
            for name, model in models.items()
        }
        boundary_ids = set(specimen["boundary_limited_model_candidates"])
        ranked = [
            _rank_candidate(
                candidate,
                predictions,
                boundary_limited=candidate["candidate_id"] in boundary_ids,
            )
            for candidate in specimen["ranking_by_candidate"]
        ]
        model_rows = [
            row for row in ranked if row["observation_class"] == "fitted_absorption_model"
        ]
        threshold_rows = [
            row for row in ranked if row["observation_class"] == "fixed_absorption_threshold"
        ]
        model_winners = sorted({row["nominal_winner"] for row in model_rows})
        threshold_winners = sorted({row["nominal_winner"] for row in threshold_rows})
        all_model_winners.update(model_winners)
        all_threshold_winners.update(threshold_winners)
        composition_sigma = specimen["contract_result"]["metadata"]["composition_sigma_x"]
        hansen_seiler_separation = abs(
            predictions["hansen"] - predictions["published_seiler"]
        )
        specimens.append(
            {
                "specimen_id": specimen["specimen_id"],
                "measurement_id": specimen["measurement_id"],
                "composition_x": composition,
                "composition_sigma_x": composition_sigma,
                "temperature_k": temperature,
                "model_predictions_mev": predictions,
                "hansen_seiler_prediction_separation_mev": hansen_seiler_separation,
                "model_candidate_nominal_winners": model_winners,
                "threshold_candidate_nominal_winners": threshold_winners,
                "minimum_model_candidate_nominal_winner_margin_mev": min(
                    row["nominal_winner_margin_mev"] for row in model_rows
                ),
                "strict_material_model_ranking_authorized": False,
                "ranking_limit": (
                    "specimen-level composition uncertainty is unreported; nominal "
                    "closest-model labels are descriptive only"
                ),
                "candidates": ranked,
            }
        )

    separations = [
        specimen["hansen_seiler_prediction_separation_mev"]
        for specimen in specimens
    ]
    model_margins = [
        specimen["minimum_model_candidate_nominal_winner_margin_mev"]
        for specimen in specimens
    ]
    return {
        "schema_version": "1.0",
        "analysis": "complete material-model comparator screen for Moazzami 2005 spectra",
        "material_models": {
            "hansen": {"role": "reference baseline"},
            "published_seiler": {
                "role": "historical rational-temperature comparator",
                "source_doi": SEILER_1990_SOURCE_DOI,
            },
            "laurenti": {
                "role": "reconstructed historical comparator",
                "primary_fit_record_status": "not recovered",
            },
            "provisional_hansen_pade": {
                "role": "leading provisional constrained Seiler-family candidate",
                "production_authorized": False,
            },
        },
        "specimens": specimens,
        "decision": {
            "published_seiler_comparator_included": True,
            "all_fitted_model_candidates_nominally_prefer_published_seiler": (
                all_model_winners == {"published_seiler"}
            ),
            "nominal_winner_changes_across_observation_definitions": (
                len(all_model_winners | all_threshold_winners) > 1
            ),
            "hansen_seiler_prediction_separation_mev_range": [
                min(separations),
                max(separations),
            ],
            "minimum_fitted_candidate_nominal_winner_margin_mev": min(model_margins),
            "strict_material_model_ranking_authorized": False,
            "reason_strict_ranking_is_not_authorized": (
                "both specimens lack specimen-level composition uncertainty and come "
                "from one source study; nominal comparator margins are sub-meV"
            ),
            "universal_gap_law_promotion_authorized": False,
            "single_corrected_edge_authorized": False,
        },
        "claim_boundary": (
            "Published Seiler is the nominal closest comparator for every fitted "
            "absorption-model edge, but its advantage over Hansen is only 0.18-0.25 meV. "
            "Without specimen-level composition uncertainty this does not identify a "
            "preferred material law. Fixed-threshold definitions still change the "
            "nominal winner, and no threshold is promoted as the latent gap."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(args.repository_root)
    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["decision"], sort_keys=True))


if __name__ == "__main__":
    main()
