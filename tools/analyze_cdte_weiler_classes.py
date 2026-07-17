#!/usr/bin/env python3
"""Fit deterministic Weiler quadratic classes to the existing static CdTe matrices."""
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
    _fit_subspace,
    build_quadratic_projector,
)
from cdte_weiler_class_templates import (
    CLASS_NAMES,
    build_weiler_class_basis,
    conventional_relation_diagnostics,
    conventional_tied_and_departure_coordinates,
)


def analyze(
    mmn_path: str | Path,
    nnkp_path: str | Path,
    eigenvalues_path: str | Path,
    basis_result_path: str | Path,
    finite_k_contract_path: str | Path,
    residual_result_path: str | Path,
    prior_art_mapping_path: str | Path,
    class_contract_path: str | Path,
) -> dict[str, Any]:
    eigenvalues = json.loads(Path(eigenvalues_path).read_text(encoding="utf-8"))
    basis_result = json.loads(Path(basis_result_path).read_text(encoding="utf-8"))
    finite_contract = json.loads(Path(finite_k_contract_path).read_text(encoding="utf-8"))
    residual_result = json.loads(Path(residual_result_path).read_text(encoding="utf-8"))
    prior_art_mapping = json.loads(
        Path(prior_art_mapping_path).read_text(encoding="utf-8")
    )
    contract = json.loads(Path(class_contract_path).read_text(encoding="utf-8"))
    if contract.get("stage") != "cdte_weiler_class_template_gate":
        raise ValueError("unexpected Weiler class-template contract stage")
    if prior_art_mapping.get("stage") != "cdte_quadratic_weiler_prior_art_mapping":
        raise ValueError("unexpected Weiler prior-art mapping stage")
    if basis_result.get("upstream", {}).get("basis_convention") != "Novik_2005_Eq_4":
        raise ValueError("canonical basis is not in the exact Novik convention")
    declared_names = tuple(item["name"] for item in contract["class_order"])
    if declared_names != CLASS_NAMES:
        raise ValueError("class contract order differs from executable class order")

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
    class_basis, class_diagnostics = build_weiler_class_basis(
        projector, hermitian_sectors
    )
    conventional_relations = conventional_relation_diagnostics(
        tensors, hermitian, class_basis
    )
    training = list(finite_contract["training_directions"])
    holdouts = list(finite_contract["holdout_directions"])
    fit = _fit_subspace(
        class_basis,
        observations,
        directions,
        training,
        tensors,
        hermitian,
    )
    named_coordinates = dict(
        zip(
            CLASS_NAMES,
            fit["orthonormal_basis_coefficients_ev_angstrom2"],
            strict=True,
        )
    )
    tied_departures = conventional_tied_and_departure_coordinates(named_coordinates)

    thresholds = contract["thresholds"]
    maximum_holdout = max(
        fit["direction_relative_residuals"][name] for name in holdouts
    )
    class_gate_passed = (
        class_diagnostics["gram_residual"]
        <= float(thresholds["maximum_class_gram_residual"])
        and class_diagnostics["projector_residual"]
        <= float(thresholds["maximum_class_projector_residual"])
        and conventional_relations["normalized_relation_residual"]
        <= float(thresholds["maximum_conventional_relation_residual"])
        and fit["training_relative_residual"]
        <= float(thresholds["maximum_training_relative_residual"])
        and maximum_holdout
        <= float(thresholds["maximum_holdout_relative_residual"])
        and fit["condition_number"]
        <= float(thresholds["maximum_design_condition_number"])
    )
    if not class_gate_passed:
        raise RuntimeError("deterministic Weiler class-template gate failed")

    return {
        "schema_version": "1.0",
        "status": "deterministic_weiler_quadratic_classes_fit_in_repository_normalization",
        "input_sha256": {
            "mmn": _sha256(mmn_path),
            "nnkp": _sha256(nnkp_path),
            "exact_qe_eigenvalues": _sha256(eigenvalues_path),
            "canonical_basis_result": _sha256(basis_result_path),
            "finite_k_contract": _sha256(finite_k_contract_path),
            "residual_result": _sha256(residual_result_path),
            "prior_art_mapping": _sha256(prior_art_mapping_path),
            "class_contract": _sha256(class_contract_path),
        },
        "minimum_overlap_singular_value": min(
            item["minimum_overlap_singular_value"] for item in reconstruction
        ),
        "projector_diagnostics": projector_diagnostics,
        "class_basis_diagnostics": class_diagnostics,
        "conventional_relation_diagnostics": conventional_relations,
        "normalization": contract["normalization"],
        "fit": {
            "design_rank": fit["design_rank"],
            "condition_number": fit["condition_number"],
            "training_relative_residual": fit["training_relative_residual"],
            "direction_relative_residuals": fit["direction_relative_residuals"],
            "repository_orthonormal_class_coordinates_ev_angstrom2": {
                name: float(value) for name, value in named_coordinates.items()
            },
            "conventional_ties_and_departures": tied_departures,
        },
        "decision": {
            "passed": class_gate_passed,
            "standard_weiler_parameter_values_validated": false,
            "interpretation": (
                "The independently generated ten-dimensional projector separates "
                "deterministically into the established Weiler F, N2, G, G', gamma, "
                "and primed-gamma symmetry classes. The executable conventional "
                "four-parameter model is exactly the expected tied subspace. The "
                "static CdTe matrices require nonzero coordinates in all three omitted "
                "conduction-valence classes and in all three directions orthogonal to "
                "the conventional primed/unprimed gamma ties. Numerical coordinates "
                "are reported only in repository orthonormal class normalization."
            ),
            "next_authorized_task": (
                "Derive and verify the exact conventional Weiler scale and sign "
                "normalization from primary matrix formulas, then test nested named "
                "physical reductions. Do not launch new electronic-structure work."
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
    parser.add_argument("--prior-art-mapping", required=True)
    parser.add_argument("--class-contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.mmn,
        args.nnkp,
        args.eigenvalues,
        args.basis_result,
        args.finite_k_contract,
        args.residual_result,
        args.prior_art_mapping,
        args.class_contract,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
