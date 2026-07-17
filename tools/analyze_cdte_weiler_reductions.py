#!/usr/bin/env python3
"""Enumerate compact reductions of the complete static CdTe Weiler space."""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from cdte_quadratic_invariant_space import (
    _conventional_span,
    _evaluate,
    _fit_subspace,
    build_quadratic_projector,
)
from cdte_weiler_class_templates import (
    CLASS_NAMES,
    build_weiler_class_basis,
)

DEPARTURE_NAMES = (
    "N2",
    "G",
    "G_prime",
    "delta_gamma1",
    "delta_gamma2",
    "delta_gamma3",
)


def build_departure_basis(class_basis: np.ndarray) -> np.ndarray:
    index = {name: position for position, name in enumerate(CLASS_NAMES)}
    vectors = [
        class_basis[:, index["N2"]],
        class_basis[:, index["G"]],
        class_basis[:, index["G_prime"]],
    ]
    delta_gamma1 = np.zeros(10)
    delta_gamma1[index["gamma1"]] = 1.0 / math.sqrt(3.0)
    delta_gamma1[index["gamma1_prime"]] = -math.sqrt(2.0 / 3.0)
    delta_gamma2 = np.zeros(10)
    delta_gamma2[index["gamma2"]] = math.sqrt(2.0 / 3.0)
    delta_gamma2[index["gamma2_prime"]] = -1.0 / math.sqrt(3.0)
    delta_gamma3 = np.zeros(10)
    delta_gamma3[index["gamma3"]] = math.sqrt(2.0 / 3.0)
    delta_gamma3[index["gamma3_prime"]] = 1.0 / math.sqrt(3.0)
    vectors.extend(
        (
            class_basis @ delta_gamma1,
            class_basis @ delta_gamma2,
            class_basis @ delta_gamma3,
        )
    )
    return np.column_stack(vectors)


def enumerate_reductions(
    conventional_basis: np.ndarray,
    departure_basis: np.ndarray,
    observations: dict[str, np.ndarray],
    directions: dict[str, np.ndarray],
    training: list[str],
    tensors: list[np.ndarray],
    hermitian_basis: list[np.ndarray],
) -> list[dict[str, Any]]:
    records = []
    for count in range(len(DEPARTURE_NAMES) + 1):
        for subset_indices in itertools.combinations(range(len(DEPARTURE_NAMES)), count):
            columns = [conventional_basis]
            columns.extend(
                departure_basis[:, index : index + 1] for index in subset_indices
            )
            basis = np.column_stack(columns)
            fit = _fit_subspace(
                basis,
                observations,
                directions,
                training,
                tensors,
                hermitian_basis,
            )
            holdout_names = [name for name in observations if name not in training]
            maximum_holdout = max(
                fit["direction_relative_residuals"][name] for name in holdout_names
            )
            records.append(
                {
                    "departure_count": count,
                    "departures": [DEPARTURE_NAMES[index] for index in subset_indices],
                    "dimension": int(basis.shape[1]),
                    "design_rank": fit["design_rank"],
                    "condition_number": fit["condition_number"],
                    "training_relative_residual": fit["training_relative_residual"],
                    "maximum_holdout_relative_residual": maximum_holdout,
                    "maximum_training_or_holdout_relative_residual": max(
                        fit["training_relative_residual"], maximum_holdout
                    ),
                    "direction_relative_residuals": fit[
                        "direction_relative_residuals"
                    ],
                }
            )
    return records


def summarize_frontier(
    records: list[dict[str, Any]], thresholds: list[float]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    frontier = []
    for count in range(len(DEPARTURE_NAMES) + 1):
        candidates = [item for item in records if item["departure_count"] == count]
        frontier.append(
            min(
                candidates,
                key=lambda item: item[
                    "maximum_training_or_holdout_relative_residual"
                ],
            )
        )
    minimum_by_threshold: dict[str, Any] = {}
    for threshold in thresholds:
        passing = [
            item
            for item in records
            if item["training_relative_residual"] <= threshold
            and item["maximum_holdout_relative_residual"] <= threshold
        ]
        if not passing:
            minimum_by_threshold[str(threshold)] = None
            continue
        minimum_count = min(item["departure_count"] for item in passing)
        best = min(
            (item for item in passing if item["departure_count"] == minimum_count),
            key=lambda item: item["maximum_training_or_holdout_relative_residual"],
        )
        minimum_by_threshold[str(threshold)] = best
    return frontier, minimum_by_threshold


def analyze(
    class_result_path: str | Path,
    finite_k_contract_path: str | Path,
    reduction_contract_path: str | Path,
) -> dict[str, Any]:
    class_result = json.loads(Path(class_result_path).read_text(encoding="utf-8"))
    finite_contract = json.loads(
        Path(finite_k_contract_path).read_text(encoding="utf-8")
    )
    contract = json.loads(Path(reduction_contract_path).read_text(encoding="utf-8"))
    if contract.get("stage") != "cdte_weiler_reduction_frontier":
        raise ValueError("unexpected Weiler reduction contract stage")
    if tuple(contract["departure_order"]) != DEPARTURE_NAMES:
        raise ValueError("departure order differs from executable order")
    if class_result.get("normalization", {}).get("name") != (
        "repository_orthonormal_class_normalization"
    ):
        raise ValueError("class result uses an unexpected normalization")

    projector, tensors, hermitian, sectors, _ = build_quadratic_projector()
    class_basis, class_diagnostics = build_weiler_class_basis(projector, sectors)
    _, conventional_basis = _conventional_span(tensors, hermitian)
    departure_basis = build_departure_basis(class_basis)
    full_basis = np.column_stack((conventional_basis, departure_basis))
    orthogonality_residual = float(
        np.linalg.norm(full_basis.T @ full_basis - np.eye(10))
    )
    full_space_residual = float(
        np.linalg.norm(full_basis @ full_basis.T - projector)
    )

    named_coordinates = class_result["fit"][
        "repository_orthonormal_class_coordinates_ev_angstrom2"
    ]
    target_coefficients = np.asarray(
        [float(named_coordinates[name]) for name in CLASS_NAMES]
    )
    target_function = class_basis @ target_coefficients
    directions = {
        name: np.asarray(spec["unit_direction"], dtype=float)
        for name, spec in finite_contract["pairs"].items()
    }
    observations = {
        name: _evaluate(target_function, direction, tensors, hermitian)
        for name, direction in directions.items()
    }
    training = list(finite_contract["training_directions"])
    records = enumerate_reductions(
        conventional_basis,
        departure_basis,
        observations,
        directions,
        training,
        tensors,
        hermitian,
    )
    frontier, minimum_by_threshold = summarize_frontier(
        records, [float(value) for value in contract["residual_thresholds"]]
    )
    leave_one_out = {
        name: next(
            item
            for item in records
            if item["departure_count"] == 5 and name not in item["departures"]
        )
        for name in DEPARTURE_NAMES
    }

    thresholds = contract["thresholds"]
    full_record = next(item for item in records if item["departure_count"] == 6)
    decision_threshold = float(contract["decision_threshold"])
    threshold_record = minimum_by_threshold[str(decision_threshold)]
    gate_passed = (
        orthogonality_residual
        <= float(thresholds["maximum_basis_orthogonality_residual"])
        and full_space_residual
        <= float(thresholds["maximum_full_space_residual"])
        and full_record["maximum_training_or_holdout_relative_residual"]
        <= float(thresholds["maximum_full_space_residual"])
        and max(item["condition_number"] for item in records)
        <= float(thresholds["maximum_design_condition_number"])
        and threshold_record is not None
        and threshold_record["departure_count"] == 6
    )
    if not gate_passed:
        raise RuntimeError("Weiler reduction frontier gate failed")

    return {
        "schema_version": "1.0",
        "status": "exhaustive_weiler_reduction_frontier_completed",
        "target": {
            "source": str(class_result_path),
            "normalization": class_result["normalization"],
            "interpretation": (
                "The target is the validated complete ten-dimensional quadratic "
                "projection, not a new fit to raw electronic-structure data."
            ),
        },
        "basis_diagnostics": {
            "class_gram_residual": class_diagnostics["gram_residual"],
            "conventional_plus_departure_orthogonality_residual": orthogonality_residual,
            "complete_projector_residual": full_space_residual,
        },
        "subset_count": len(records),
        "frontier_by_departure_count": frontier,
        "minimum_model_by_residual_threshold": minimum_by_threshold,
        "leave_one_departure_out": leave_one_out,
        "all_subsets": records,
        "decision": {
            "passed": gate_passed,
            "all_six_departures_required_below_decision_threshold": true,
            "decision_threshold": decision_threshold,
            "best_five_departure_model": frontier[5],
            "interpretation": (
                "No compact subset of the six established departures reproduces "
                "both the fitted and unused crystal directions below ten percent. "
                "The best five-departure model remains above ten percent, so the "
                "static smoke does not support a quantitatively accurate reduced "
                "extension smaller than the complete ten-dimensional space."
            ),
            "next_authorized_task": (
                "Freeze the static quadratic model at the complete Weiler space, "
                "record the failure of compact reductions, and return program effort "
                "to independent data/provenance and CdTe A0 readiness rather than "
                "adding further static model complexity."
            ),
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--class-result", required=True)
    parser.add_argument("--finite-k-contract", required=True)
    parser.add_argument("--reduction-contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.class_result,
        args.finite_k_contract,
        args.reduction_contract,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
