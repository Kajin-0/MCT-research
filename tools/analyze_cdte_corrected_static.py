#!/usr/bin/env python3
"""Generate the controlling corrected static CdTe Kane analysis record."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from analyze_cdte_finite_k_kane import select_signs
from cdte_finite_k_projection import (
    SELECTED_BAND_POLAR,
    _apply_signs,
    _read_nnkp,
    _sha256,
    _validate_kpoint_contract,
    extract_coefficients,
    reconstruct_canonical_matrices,
)
from cdte_quadratic_invariant_space import (
    _conventional_span,
    _fit_subspace,
    build_quadratic_projector,
)
from cdte_weiler_class_templates import (
    CLASS_NAMES,
    build_weiler_class_basis,
    conventional_tied_and_departure_coordinates,
)
from analyze_cdte_weiler_reductions import (
    DEPARTURE_NAMES,
    build_departure_basis,
    enumerate_reductions,
    summarize_frontier,
)


def _maximum_holdout(fit: dict[str, Any], holdouts: list[str]) -> float:
    return max(float(fit["direction_relative_residuals"][name]) for name in holdouts)


def analyze(
    mmn_path: str | Path,
    nnkp_path: str | Path,
    eigenvalues_path: str | Path,
    basis_result_path: str | Path,
    finite_contract_path: str | Path,
    finite_result_path: str | Path,
    spectral_result_path: str | Path,
) -> dict[str, Any]:
    eigenvalues = json.loads(Path(eigenvalues_path).read_text(encoding="utf-8"))
    basis_result = json.loads(Path(basis_result_path).read_text(encoding="utf-8"))
    contract = json.loads(Path(finite_contract_path).read_text(encoding="utf-8"))
    finite_result = json.loads(Path(finite_result_path).read_text(encoding="utf-8"))
    spectral_result = json.loads(Path(spectral_result_path).read_text(encoding="utf-8"))
    if finite_result.get("reconstruction_mode") != SELECTED_BAND_POLAR:
        raise ValueError("corrected static analysis requires selected-band polar input")
    if spectral_result.get("reconstruction_mode") != SELECTED_BAND_POLAR:
        raise ValueError("spectral result does not use selected-band polar input")

    _, cartesian = _read_nnkp(nnkp_path)
    _validate_kpoint_contract(cartesian, contract)
    matrices, reconstruction = reconstruct_canonical_matrices(
        mmn_path,
        eigenvalues,
        basis_result,
        mode=SELECTED_BAND_POLAR,
    )
    selected_signs = finite_result["sign_convention"]["selected"]
    gamma8 = int(selected_signs["gamma8_sign"])
    gamma7 = int(selected_signs["gamma7_sign"])
    signed = _apply_signs(matrices, gamma8, gamma7)
    coefficients = extract_coefficients(signed, contract["pairs"])
    observations = {name: record["quadratic"] for name, record in coefficients.items()}
    directions = {
        name: np.asarray(spec["unit_direction"], dtype=float)
        for name, spec in contract["pairs"].items()
    }
    training = list(contract["training_directions"])
    holdouts = list(contract["holdout_directions"])

    projector, tensors, hermitian, sectors, projector_diagnostics = (
        build_quadratic_projector()
    )
    class_basis, class_diagnostics = build_weiler_class_basis(projector, sectors)
    _, conventional_basis = _conventional_span(tensors, hermitian)
    departure_basis = build_departure_basis(class_basis)

    complete_fit = _fit_subspace(
        class_basis,
        observations,
        directions,
        training,
        tensors,
        hermitian,
    )
    conventional_fit = _fit_subspace(
        conventional_basis,
        observations,
        directions,
        training,
        tensors,
        hermitian,
    )
    named_coordinates = dict(
        zip(
            CLASS_NAMES,
            complete_fit["orthonormal_basis_coefficients_ev_angstrom2"],
            strict=True,
        )
    )
    ties = conventional_tied_and_departure_coordinates(named_coordinates)

    reductions = enumerate_reductions(
        conventional_basis,
        departure_basis,
        observations,
        directions,
        training,
        tensors,
        hermitian,
    )
    reduction_thresholds = [0.10, 0.05, 0.01, 0.005, 0.001]
    frontier, minimum_by_threshold = summarize_frontier(
        reductions, reduction_thresholds
    )
    one_percent = minimum_by_threshold["0.01"]
    one_per_mille = minimum_by_threshold["0.001"]
    if one_percent is None or one_per_mille is None:
        raise RuntimeError("corrected reduction frontier did not reach declared gates")

    complete_holdout = _maximum_holdout(complete_fit, holdouts)
    conventional_holdout = _maximum_holdout(conventional_fit, holdouts)
    spectral = spectral_result["spectral_closure"]
    maximum_isospectral_error = max(
        float(item["maximum_selected_eigenvalue_absolute_error_ev"])
        for item in reconstruction
    )
    full_projector_residual = float(
        np.linalg.norm(class_basis @ class_basis.T - projector)
    )
    corrected_gate_passed = (
        maximum_isospectral_error <= 1.0e-10
        and complete_fit["training_relative_residual"] <= 1.0e-3
        and complete_holdout <= 1.0e-3
        and conventional_fit["training_relative_residual"] >= 0.10
        and conventional_holdout >= 0.10
        and one_percent["departure_count"] == 5
        and "N2" not in one_percent["departures"]
        and one_per_mille["departure_count"] == 6
        and not bool(spectral["passed_declared_spectral_gate"])
        and full_projector_residual <= 1.0e-10
    )
    if not corrected_gate_passed:
        raise RuntimeError("corrected static CdTe decision gate failed")

    return {
        "schema_version": "1.0",
        "status": "corrected_static_cdte_kane_analysis_validated",
        "input_sha256": {
            "mmn": _sha256(mmn_path),
            "nnkp": _sha256(nnkp_path),
            "exact_qe_eigenvalues": _sha256(eigenvalues_path),
            "canonical_basis_result": _sha256(basis_result_path),
            "finite_k_contract": _sha256(finite_contract_path),
            "finite_k_result": _sha256(finite_result_path),
            "spectral_result": _sha256(spectral_result_path),
        },
        "reconstruction": {
            "scientific_mode": SELECTED_BAND_POLAR,
            "maximum_selected_eigenvalue_absolute_error_ev": maximum_isospectral_error,
            "minimum_selected_overlap_singular_value": min(
                float(item["minimum_overlap_singular_value"])
                for item in reconstruction
            ),
            "interpretation": (
                "The finite-k Hamiltonian is the selected-eight polar transport in "
                "the fixed Novik Gamma reference basis and is exactly isospectral to "
                "the selected DFT manifold."
            ),
        },
        "linear": {
            "p8_ev_angstrom": float(finite_result["two_p"]["parameters"]["p8"]),
            "p7_ev_angstrom": float(finite_result["two_p"]["parameters"]["p7"]),
            "eta_p": float(finite_result["two_p"]["eta_p"]),
            "two_p_training_relative_residual": float(
                finite_result["two_p"]["diagnostics"]["linear"]["relative_residual"]
            ),
            "maximum_two_p_holdout_relative_residual": max(
                float(record["linear_relative_error"])
                for record in finite_result["two_p"]["heldout"].values()
            ),
            "claim_status": (
                "robust static method-smoke reproduction in the stated fixed basis; "
                "the complete four-linear-invariant structure is established prior art"
            ),
        },
        "quadratic_matrix_closure_in_polar_gauge": {
            "complete_dimension": 10,
            "conventional_dimension": 4,
            "projector_diagnostics": {
                **projector_diagnostics,
                "class_basis_projector_residual": full_projector_residual,
                "class_gram_residual": class_diagnostics["gram_residual"],
            },
            "complete_training_relative_residual": float(
                complete_fit["training_relative_residual"]
            ),
            "complete_direction_relative_residuals": complete_fit[
                "direction_relative_residuals"
            ],
            "complete_maximum_holdout_relative_residual": complete_holdout,
            "conventional_training_relative_residual": float(
                conventional_fit["training_relative_residual"]
            ),
            "conventional_direction_relative_residuals": conventional_fit[
                "direction_relative_residuals"
            ],
            "conventional_maximum_holdout_relative_residual": conventional_holdout,
            "repository_orthonormal_class_coordinates_ev_angstrom2": {
                name: float(value) for name, value in named_coordinates.items()
            },
            "conventional_ties_and_departures": ties,
            "gauge_boundary": (
                "Matrix coordinates and Frobenius matrix residuals are properties of "
                "the declared fixed-Gamma polar gauge. They are not invariant under "
                "arbitrary additional smooth k-dependent unitary transformations."
            ),
        },
        "gauge_invariant_conventional_spectral_closure": spectral,
        "exhaustive_reduction_frontier": {
            "subset_count": len(reductions),
            "frontier_by_departure_count": frontier,
            "minimum_model_by_residual_threshold": minimum_by_threshold,
            "one_percent_model": one_percent,
            "one_per_mille_model": one_per_mille,
            "decision": (
                "Five established departure directions—G, G_prime and the three "
                "primed/unprimed gamma departures—are sufficient below one percent; "
                "N2 is not required at that gate. All six are required below one per "
                "mille at this static smoke point."
            ),
        },
        "decision": {
            "passed": corrected_gate_passed,
            "conventional_quadratic_matrix_model_fails": true,
            "conventional_quadratic_spectral_model_fails_declared_gate": true,
            "five_departures_sufficient_below_one_percent": true,
            "n2_required_below_one_percent": false,
            "all_six_required_below_one_per_mille": true,
            "supersedes": [
                "approximately 49 percent conventional quadratic residual",
                "large N2 coordinate",
                "all six departures required below ten percent",
                "120-band convergence run for the all-state reconstruction",
            ],
            "next_authorized_task": (
                "Record this corrected result and return effort to finite-temperature "
                "matrix self-energy design or independent empirical validation. Do not "
                "spend additional compute on static band-count convergence."
            ),
        },
        "claim_boundary": (
            "This is an unconverged static PBE planning-geometry method smoke. The "
            "matrix result is stated in the fixed-Gamma polar gauge; the spectral "
            "failure is basis invariant. No coefficient is a reference CdTe material "
            "parameter and no HgTe, alloy, phonon, AHC or higher-band work is authorized."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mmn", required=True)
    parser.add_argument("--nnkp", required=True)
    parser.add_argument("--eigenvalues", required=True)
    parser.add_argument("--basis-result", required=True)
    parser.add_argument("--finite-k-contract", required=True)
    parser.add_argument("--finite-result", required=True)
    parser.add_argument("--spectral-result", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.mmn,
        args.nnkp,
        args.eigenvalues,
        args.basis_result,
        args.finite_k_contract,
        args.finite_result,
        args.spectral_result,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(args.output_json).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
