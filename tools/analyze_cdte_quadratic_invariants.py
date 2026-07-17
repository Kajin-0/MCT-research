#!/usr/bin/env python3
"""Test complete Td- and time-reversal-even quadratic closure for static CdTe."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from cdte_finite_k_projection import (
    _apply_signs,
    _read_nnkp,
    _sha256,
    _validate_kpoint_contract,
    extract_coefficients,
    reconstruct_canonical_matrices,
)
from cdte_quadratic_invariant_space import (
    SECTORS,
    _conventional_span,
    _fit_subspace,
    _orthonormalize,
    _projected_basis,
    build_quadratic_projector,
)

def analyze(
    mmn_path: str | Path,
    nnkp_path: str | Path,
    eigenvalues_path: str | Path,
    basis_result_path: str | Path,
    finite_k_contract_path: str | Path,
    residual_result_path: str | Path,
    invariant_contract_path: str | Path,
) -> dict[str, Any]:
    eigenvalues = json.loads(Path(eigenvalues_path).read_text(encoding="utf-8"))
    basis_result = json.loads(Path(basis_result_path).read_text(encoding="utf-8"))
    finite_contract = json.loads(Path(finite_k_contract_path).read_text(encoding="utf-8"))
    residual_result = json.loads(Path(residual_result_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(invariant_contract_path).read_text(encoding="utf-8"))
    if contract.get("stage") != "cdte_complete_quadratic_invariant_gate":
        raise ValueError("unexpected complete quadratic invariant contract stage")
    if basis_result.get("upstream", {}).get("basis_convention") != "Novik_2005_Eq_4":
        raise ValueError("canonical basis is not in the exact Novik convention")

    _, cartesian = _read_nnkp(nnkp_path)
    _validate_kpoint_contract(cartesian, finite_contract)
    matrices, reconstruction = reconstruct_canonical_matrices(
        mmn_path, eigenvalues, basis_result
    )
    signs = residual_result["sign_convention"]
    signed = _apply_signs(matrices, int(signs["Gamma8"]), int(signs["Gamma7"]))
    coefficients = extract_coefficients(signed, finite_contract["pairs"])
    observations = {name: record["quadratic"] for name, record in coefficients.items()}
    directions = {
        name: np.asarray(spec["unit_direction"], dtype=float)
        for name, spec in finite_contract["pairs"].items()
    }

    projector, tensors, hermitian, hermitian_sectors, projector_diagnostics = (
        build_quadratic_projector()
    )
    complete_raw = _projected_basis(projector)
    sector_bases = {}
    for sector in SECTORS:
        indices = [
            tensor * 64 + matrix
            for tensor in range(6)
            for matrix, matrix_sector in enumerate(hermitian_sectors)
            if matrix_sector == sector
        ]
        sector_bases[sector] = _projected_basis(projector, indices)

    conventional_raw, conventional = _conventional_span(tensors, hermitian)
    gamma_span = _orthonormalize(
        [conventional_raw[:, index] for index in range(1, 4)]
    )
    valence = np.column_stack(
        [sector_bases["88"], sector_bases["87"], sector_bases["77"]]
    )
    valence_candidates = [
        column - gamma_span @ (gamma_span.T @ column) for column in valence.T
    ]
    valence_extra = _orthonormalize(valence_candidates)
    groups = {
        "conventional": conventional,
        "Gamma6-Gamma8": sector_bases["68"],
        "Gamma6-Gamma7": sector_bases["67"],
        "valence-extra": valence_extra,
    }
    complete = np.column_stack(list(groups.values()))

    thresholds = contract["thresholds"]
    expected_sector_dimensions = contract["expected_sector_dimensions"]
    sector_dimensions = {name: int(value.shape[1]) for name, value in sector_bases.items()}
    if sector_dimensions != expected_sector_dimensions:
        raise RuntimeError(
            f"quadratic sector dimensions changed: {sector_dimensions}"
        )
    if complete.shape[1] != int(contract["expected_total_dimension"]):
        raise RuntimeError("complete quadratic invariant dimension changed")
    if conventional.shape[1] != int(contract["expected_conventional_dimension"]):
        raise RuntimeError("conventional quadratic span dimension changed")

    full_space_residual = float(np.linalg.norm(complete @ complete.T - projector))
    conventional_projection_residual = max(
        float(np.linalg.norm((np.eye(384) - projector) @ conventional_raw[:, index]))
        / np.linalg.norm(conventional_raw[:, index])
        for index in range(conventional_raw.shape[1])
    )
    if max(
        projector_diagnostics["symmetry_residual"],
        projector_diagnostics["idempotency_residual"],
        full_space_residual,
        conventional_projection_residual,
    ) > float(thresholds["maximum_projector_residual"]):
        raise RuntimeError("quadratic invariant projector failed its numerical gate")

    models = {
        "conventional": ("conventional",),
        "conventional_plus_68": ("conventional", "Gamma6-Gamma8"),
        "conventional_plus_67": ("conventional", "Gamma6-Gamma7"),
        "conventional_plus_valence": ("conventional", "valence-extra"),
        "without_valence_extra": (
            "conventional",
            "Gamma6-Gamma8",
            "Gamma6-Gamma7",
        ),
        "without_67": (
            "conventional",
            "Gamma6-Gamma8",
            "valence-extra",
        ),
        "without_68": (
            "conventional",
            "Gamma6-Gamma7",
            "valence-extra",
        ),
        "complete": (
            "conventional",
            "Gamma6-Gamma8",
            "Gamma6-Gamma7",
            "valence-extra",
        ),
    }
    training = list(finite_contract["training_directions"])
    fits = {
        name: _fit_subspace(
            np.column_stack([groups[group] for group in model_groups]),
            observations,
            directions,
            training,
            tensors,
            hermitian,
        )
        for name, model_groups in models.items()
    }
    complete_fit = fits["complete"]
    holdouts = list(finite_contract["holdout_directions"])
    maximum_complete_holdout = max(
        complete_fit["direction_relative_residuals"][name] for name in holdouts
    )
    complete_passed = (
        complete_fit["training_relative_residual"]
        <= float(thresholds["maximum_complete_training_relative_residual"])
        and maximum_complete_holdout
        <= float(thresholds["maximum_complete_holdout_relative_residual"])
        and complete_fit["condition_number"]
        <= float(thresholds["maximum_design_condition_number"])
    )
    omitted_models = ("without_valence_extra", "without_67", "without_68")
    all_groups_required = all(
        max(fits[name]["direction_relative_residuals"][holdout] for holdout in holdouts)
        > float(thresholds["maximum_reduced_holdout_relative_residual"])
        for name in omitted_models
    )

    return {
        "schema_version": "1.0",
        "status": "complete_Td_time_reversal_even_quadratic_space_tested",
        "input_sha256": {
            "mmn": _sha256(mmn_path),
            "nnkp": _sha256(nnkp_path),
            "exact_qe_eigenvalues": _sha256(eigenvalues_path),
            "canonical_basis_result": _sha256(basis_result_path),
            "finite_k_contract": _sha256(finite_k_contract_path),
            "residual_result": _sha256(residual_result_path),
            "invariant_contract": _sha256(invariant_contract_path),
        },
        "minimum_overlap_singular_value": min(
            item["minimum_overlap_singular_value"] for item in reconstruction
        ),
        "projector_diagnostics": {
            **projector_diagnostics,
            "complete_basis_projector_residual": full_space_residual,
            "maximum_conventional_template_projection_residual": conventional_projection_residual,
        },
        "dimensions": {
            "complete": int(complete.shape[1]),
            "conventional": int(conventional.shape[1]),
            "additional": int(complete.shape[1] - conventional.shape[1]),
            "sectors": sector_dimensions,
            "additional_groups": {
                "Gamma6-Gamma8": int(groups["Gamma6-Gamma8"].shape[1]),
                "Gamma6-Gamma7": int(groups["Gamma6-Gamma7"].shape[1]),
                "valence-extra": int(groups["valence-extra"].shape[1]),
            },
        },
        "fits": fits,
        "decision": {
            "complete_space_passed": complete_passed,
            "all_three_additional_channel_groups_required": all_groups_required,
            "interpretation": (
                "The complete ten-dimensional Td-covariant, time-reversal-even "
                "quadratic matrix space closes the existing static CdTe matrices, "
                "while the four-dimensional conventional Kane span does not. The "
                "six missing dimensions consist of two Gamma6-Gamma8 channels, one "
                "Gamma6-Gamma7 channel, and three additional valence/split-off "
                "combinations. This identifies model-form incompleteness at the "
                "static smoke level; it does not establish novel or converged "
                "material parameters."
            ),
            "next_authorized_task": (
                "Map the six additional invariant combinations to published complete "
                "zincblende k.p conventions and perform a prior-art/physical-naming "
                "audit before proposing a reduced analytical extension."
            ),
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mmn", required=True)
    parser.add_argument("--nnkp", required=True)
    parser.add_argument("--eigenvalues", required=True)
    parser.add_argument("--basis-result", required=True)
    parser.add_argument("--finite-k-contract", required=True)
    parser.add_argument("--residual-result", required=True)
    parser.add_argument("--invariant-contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.mmn,
        args.nnkp,
        args.eigenvalues,
        args.basis_result,
        args.finite_k_contract,
        args.residual_result,
        args.invariant_contract,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
