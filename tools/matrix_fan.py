#!/usr/bin/env python3
"""Synthetic, backend-independent matrix lower-Fan contraction for R02."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


class MatrixFanError(ValueError):
    """Raised when a matrix-Fan record or algebraic operation is invalid."""


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise MatrixFanError(f"expected a JSON object in {path}")
    return value


def _require_keys(mapping: Mapping[str, Any], keys: Sequence[str], context: str) -> None:
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise MatrixFanError(f"{context} missing keys: {', '.join(missing)}")


def _finite_vector(value: Any, context: str) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if array.ndim != 1 or array.size == 0:
        raise MatrixFanError(f"{context} must be a nonempty vector")
    if not np.all(np.isfinite(array)):
        raise MatrixFanError(f"{context} contains non-finite values")
    return array


def _finite_complex_matrix(value: Any, context: str) -> np.ndarray:
    array = np.asarray(value, dtype=complex)
    if array.ndim != 2:
        raise MatrixFanError(f"{context} must be a rank-2 matrix")
    if not np.all(np.isfinite(array.real)) or not np.all(np.isfinite(array.imag)):
        raise MatrixFanError(f"{context} contains non-finite values")
    return array


def decode_complex_matrix(value: Mapping[str, Any], context: str) -> np.ndarray:
    _require_keys(value, ("real", "imag"), context)
    real = np.asarray(value["real"], dtype=float)
    imag = np.asarray(value["imag"], dtype=float)
    if real.ndim != 2 or imag.shape != real.shape:
        raise MatrixFanError(f"{context} real/imag arrays must be matching matrices")
    if not np.all(np.isfinite(real)) or not np.all(np.isfinite(imag)):
        raise MatrixFanError(f"{context} contains non-finite values")
    return real + 1j * imag


def encode_complex_matrix(matrix: Any) -> dict[str, list[list[float]]]:
    value = _finite_complex_matrix(matrix, "matrix")
    return {"real": value.real.tolist(), "imag": value.imag.tolist()}


def _max_abs(value: np.ndarray) -> float:
    return float(np.max(np.abs(value))) if value.size else 0.0


def denominator_factors(
    energy_ev: float,
    eta_ev: float,
    intermediate_energies_ev: Sequence[float],
    occupations: Sequence[float],
    phonon_energy_ev: float,
    bose_occupation: float,
) -> np.ndarray:
    """Return diagonal retarded Fan denominator factors at one common energy."""
    energies = _finite_vector(intermediate_energies_ev, "intermediate energies")
    occupations_array = _finite_vector(occupations, "intermediate occupations")
    if occupations_array.shape != energies.shape:
        raise MatrixFanError("intermediate energies and occupations must have matching shapes")
    if np.any(occupations_array < 0.0) or np.any(occupations_array > 1.0):
        raise MatrixFanError("occupations must lie in [0, 1]")
    if not np.isfinite(energy_ev):
        raise MatrixFanError("evaluation energy must be finite")
    if not np.isfinite(eta_ev) or eta_ev <= 0.0:
        raise MatrixFanError("eta must be finite and strictly positive for a retarded self-energy")
    if not np.isfinite(phonon_energy_ev) or phonon_energy_ev <= 0.0:
        raise MatrixFanError("phonon energy must be finite and strictly positive")
    if not np.isfinite(bose_occupation) or bose_occupation < 0.0:
        raise MatrixFanError("Bose occupation must be finite and nonnegative")

    z = complex(float(energy_ev), float(eta_ev))
    emission = (bose_occupation + 1.0 - occupations_array) / (
        z - energies - phonon_energy_ev
    )
    absorption = (bose_occupation + occupations_array) / (
        z - energies + phonon_energy_ev
    )
    return emission + absorption


def denominator_derivative(
    energy_ev: float,
    eta_ev: float,
    intermediate_energies_ev: Sequence[float],
    occupations: Sequence[float],
    phonon_energy_ev: float,
    bose_occupation: float,
) -> np.ndarray:
    """Return the analytic derivative of the retarded denominator with respect to E."""
    energies = _finite_vector(intermediate_energies_ev, "intermediate energies")
    occupations_array = _finite_vector(occupations, "intermediate occupations")
    denominator_factors(
        energy_ev,
        eta_ev,
        energies,
        occupations_array,
        phonon_energy_ev,
        bose_occupation,
    )
    z = complex(float(energy_ev), float(eta_ev))
    return -(
        (bose_occupation + 1.0 - occupations_array)
        / (z - energies - phonon_energy_ev) ** 2
        + (bose_occupation + occupations_array)
        / (z - energies + phonon_energy_ev) ** 2
    )


def fan_contribution_matrix(
    vertex_ev: Any,
    *,
    energy_ev: float,
    eta_ev: float,
    intermediate_energies_ev: Sequence[float],
    occupations: Sequence[float],
    phonon_energy_ev: float,
    bose_occupation: float,
    q_weight: float = 1.0,
) -> np.ndarray:
    """Contract one normalized complex vertex matrix as G^dagger D G."""
    vertex = _finite_complex_matrix(vertex_ev, "vertex")
    if not np.isfinite(q_weight) or q_weight < 0.0:
        raise MatrixFanError("q weight must be finite and nonnegative")
    factors = denominator_factors(
        energy_ev,
        eta_ev,
        intermediate_energies_ev,
        occupations,
        phonon_energy_ev,
        bose_occupation,
    )
    if vertex.shape[0] != factors.size:
        raise MatrixFanError("vertex intermediate dimension does not match denominator data")
    return float(q_weight) * (vertex.conj().T @ (factors[:, None] * vertex))


def fan_contribution_derivative(
    vertex_ev: Any,
    *,
    energy_ev: float,
    eta_ev: float,
    intermediate_energies_ev: Sequence[float],
    occupations: Sequence[float],
    phonon_energy_ev: float,
    bose_occupation: float,
    q_weight: float = 1.0,
) -> np.ndarray:
    """Contract one analytic energy derivative as G^dagger D' G."""
    vertex = _finite_complex_matrix(vertex_ev, "vertex")
    if not np.isfinite(q_weight) or q_weight < 0.0:
        raise MatrixFanError("q weight must be finite and nonnegative")
    factors = denominator_derivative(
        energy_ev,
        eta_ev,
        intermediate_energies_ev,
        occupations,
        phonon_energy_ev,
        bose_occupation,
    )
    if vertex.shape[0] != factors.size:
        raise MatrixFanError("vertex intermediate dimension does not match denominator data")
    return float(q_weight) * (vertex.conj().T @ (factors[:, None] * vertex))


def fan_matrix(
    contributions: Sequence[Mapping[str, Any]], energy_ev: float, eta_ev: float
) -> np.ndarray:
    """Sum normalized q/mode contributions at one common external energy."""
    if not contributions:
        raise MatrixFanError("at least one contribution is required")
    result: np.ndarray | None = None
    for index, item in enumerate(contributions):
        current = fan_contribution_matrix(
            item["vertex_ev"],
            energy_ev=energy_ev,
            eta_ev=eta_ev,
            intermediate_energies_ev=item["intermediate_energies_ev"],
            occupations=item["occupations"],
            phonon_energy_ev=float(item["phonon_energy_ev"]),
            bose_occupation=float(item["bose_occupation"]),
            q_weight=float(item["q_weight"]),
        )
        if result is None:
            result = np.zeros_like(current)
        elif result.shape != current.shape:
            raise MatrixFanError(f"contribution {index} external dimension mismatch")
        result += current
    assert result is not None
    return result


def fan_matrix_derivative(
    contributions: Sequence[Mapping[str, Any]], energy_ev: float, eta_ev: float
) -> np.ndarray:
    """Sum analytic energy derivatives at one common external energy."""
    if not contributions:
        raise MatrixFanError("at least one contribution is required")
    result: np.ndarray | None = None
    for index, item in enumerate(contributions):
        current = fan_contribution_derivative(
            item["vertex_ev"],
            energy_ev=energy_ev,
            eta_ev=eta_ev,
            intermediate_energies_ev=item["intermediate_energies_ev"],
            occupations=item["occupations"],
            phonon_energy_ev=float(item["phonon_energy_ev"]),
            bose_occupation=float(item["bose_occupation"]),
            q_weight=float(item["q_weight"]),
        )
        if result is None:
            result = np.zeros_like(current)
        elif result.shape != current.shape:
            raise MatrixFanError(f"contribution {index} external dimension mismatch")
        result += current
    assert result is not None
    return result


def scalar_diagonal_reference(
    contributions: Sequence[Mapping[str, Any]],
    external_index: int,
    energy_ev: float,
    eta_ev: float,
) -> complex:
    """Evaluate the conventional scalar diagonal expression directly."""
    value = 0.0j
    for item in contributions:
        vertex = _finite_complex_matrix(item["vertex_ev"], "vertex")
        if external_index < 0 or external_index >= vertex.shape[1]:
            raise MatrixFanError("external index out of range")
        factors = denominator_factors(
            energy_ev,
            eta_ev,
            item["intermediate_energies_ev"],
            item["occupations"],
            float(item["phonon_energy_ev"]),
            float(item["bose_occupation"]),
        )
        if factors.size != vertex.shape[0]:
            raise MatrixFanError("vertex intermediate dimension mismatch")
        value += float(item["q_weight"]) * np.sum(
            np.abs(vertex[:, external_index]) ** 2 * factors
        )
    return complex(value)


def hermitian_part(matrix: Any) -> np.ndarray:
    """Return (M + M^dagger)/2 without misclassifying the raw retarded matrix."""
    value = _finite_complex_matrix(matrix, "matrix")
    if value.shape[0] != value.shape[1]:
        raise MatrixFanError("matrix must be square")
    return 0.5 * (value + value.conj().T)


def linewidth_matrix(retarded_matrix: Any) -> np.ndarray:
    """Return Gamma = i(Sigma^R - Sigma^{R,dagger}), positive for retarded input."""
    value = _finite_complex_matrix(retarded_matrix, "retarded matrix")
    if value.shape[0] != value.shape[1]:
        raise MatrixFanError("retarded matrix must be square")
    return 1j * (value - value.conj().T)


def symmetrized_on_shell_hermitian(
    contributions: Sequence[Mapping[str, Any]],
    external_energies_ev: Sequence[float],
    eta_ev: float,
) -> np.ndarray:
    """Return 1/2[S_ab(e_a) + S_ba(e_b)^*] in the H0 eigenbasis."""
    energies = _finite_vector(external_energies_ev, "external energies")
    samples = [fan_matrix(contributions, float(energy), eta_ev) for energy in energies]
    if any(sample.shape != (energies.size, energies.size) for sample in samples):
        raise MatrixFanError("external energies do not match matrix dimension")
    result = np.empty((energies.size, energies.size), dtype=complex)
    for a in range(energies.size):
        for b in range(energies.size):
            result[a, b] = 0.5 * (
                samples[a][a, b] + np.conj(samples[b][b, a])
            )
    return result


def unitary_residual(unitary: Any) -> float:
    value = _finite_complex_matrix(unitary, "unitary")
    if value.shape[0] != value.shape[1]:
        raise MatrixFanError("unitary must be square")
    return _max_abs(value.conj().T @ value - np.eye(value.shape[0]))


def commutator_residual(operator: Any, unitary: Any) -> float:
    operator_array = _finite_complex_matrix(operator, "operator")
    unitary_array = _finite_complex_matrix(unitary, "unitary")
    if operator_array.shape != unitary_array.shape or operator_array.shape[0] != operator_array.shape[1]:
        raise MatrixFanError("operator and unitary must be square with matching shapes")
    return _max_abs(operator_array @ unitary_array - unitary_array @ operator_array)


def rotate_external_contributions(
    contributions: Sequence[Mapping[str, Any]],
    unitary: Any,
    tolerance: float = 1e-12,
) -> list[dict[str, Any]]:
    """Apply G -> G U in the external subspace."""
    unitary_array = _finite_complex_matrix(unitary, "external unitary")
    if unitary_residual(unitary_array) > tolerance:
        raise MatrixFanError("external transform is not unitary")
    rotated: list[dict[str, Any]] = []
    for item in contributions:
        vertex = _finite_complex_matrix(item["vertex_ev"], "vertex")
        if vertex.shape[1] != unitary_array.shape[0]:
            raise MatrixFanError("external unitary dimension mismatch")
        clone = dict(item)
        clone["vertex_ev"] = vertex @ unitary_array
        rotated.append(clone)
    return rotated


def rotate_intermediate_contribution(
    contribution: Mapping[str, Any],
    unitary: Any,
    *,
    energy_ev: float,
    eta_ev: float,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Apply G -> V^dagger G only when V commutes with the denominator operator."""
    vertex = _finite_complex_matrix(contribution["vertex_ev"], "vertex")
    unitary_array = _finite_complex_matrix(unitary, "intermediate unitary")
    if unitary_array.shape != (vertex.shape[0], vertex.shape[0]):
        raise MatrixFanError("intermediate unitary dimension mismatch")
    if unitary_residual(unitary_array) > tolerance:
        raise MatrixFanError("intermediate transform is not unitary")
    factors = denominator_factors(
        energy_ev,
        eta_ev,
        contribution["intermediate_energies_ev"],
        contribution["occupations"],
        float(contribution["phonon_energy_ev"]),
        float(contribution["bose_occupation"]),
    )
    if commutator_residual(np.diag(factors), unitary_array) > tolerance:
        raise MatrixFanError("intermediate rotation mixes unequal denominator factors")
    clone = dict(contribution)
    clone["vertex_ev"] = unitary_array.conj().T @ vertex
    return clone


def require_rotation_commutes_with_external_hamiltonian(
    external_energies_ev: Sequence[float],
    unitary: Any,
    tolerance: float = 1e-12,
) -> None:
    """Restrict on-shell covariance claims to rotations commuting with H0."""
    energies = _finite_vector(external_energies_ev, "external energies")
    unitary_array = _finite_complex_matrix(unitary, "external unitary")
    if unitary_array.shape != (energies.size, energies.size):
        raise MatrixFanError("external unitary dimension mismatch")
    if unitary_residual(unitary_array) > tolerance:
        raise MatrixFanError("external transform is not unitary")
    if commutator_residual(np.diag(energies), unitary_array) > tolerance:
        raise MatrixFanError("external rotation mixes unequal unperturbed energies")


def validate_matrix_fan_record(
    record: Mapping[str, Any], contract: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate a JSON-compatible synthetic record and return numerical contributions."""
    if contract.get("stage") != "B0_external_matrix_fan_contract":
        raise MatrixFanError("unexpected matrix-Fan contract stage")
    _require_keys(record, contract["required_record_fields"], "matrix-Fan record")
    if record["schema_version"] != contract["schema_version"]:
        raise MatrixFanError("matrix-Fan schema version mismatch")
    if record["stage"] != contract["stage"]:
        raise MatrixFanError("matrix-Fan record stage mismatch")

    metadata = record["metadata"]
    if not isinstance(metadata, Mapping):
        raise MatrixFanError("metadata must be an object")
    for name, required_value in contract["required_metadata"].items():
        if metadata.get(name) != required_value:
            raise MatrixFanError(f"metadata.{name} must equal {required_value!r}")
    if not str(metadata.get("source_id", "")).strip():
        raise MatrixFanError("metadata.source_id is required")
    if not str(metadata.get("external_gauge_id", "")).strip():
        raise MatrixFanError("metadata.external_gauge_id is required")
    if not str(metadata.get("intermediate_gauge_id", "")).strip():
        raise MatrixFanError("metadata.intermediate_gauge_id is required")

    external_dimension = int(record["external_dimension"])
    if external_dimension <= 0:
        raise MatrixFanError("external dimension must be positive")
    external_energies = _finite_vector(record["external_energies_ev"], "external energies")
    if external_energies.size != external_dimension:
        raise MatrixFanError("external energy count does not match external dimension")
    external_groups = list(record["external_degeneracy_groups"])
    if len(external_groups) != external_dimension:
        raise MatrixFanError("external degeneracy-group count mismatch")

    evaluation_energy = float(record["evaluation_energy_ev"])
    eta_ev = float(record["eta_ev"])
    if not np.isfinite(evaluation_energy):
        raise MatrixFanError("evaluation energy must be finite")
    if not np.isfinite(eta_ev) or eta_ev <= 0.0:
        raise MatrixFanError("eta must be finite and strictly positive")

    raw_contributions = record["contributions"]
    if not isinstance(raw_contributions, list) or not raw_contributions:
        raise MatrixFanError("contributions must be a nonempty list")
    contributions: list[dict[str, Any]] = []
    for index, item in enumerate(raw_contributions):
        if not isinstance(item, Mapping):
            raise MatrixFanError(f"contributions[{index}] must be an object")
        _require_keys(
            item,
            contract["required_contribution_fields"],
            f"contributions[{index}]",
        )
        intermediate_dimension = int(item["intermediate_dimension"])
        if intermediate_dimension <= 0:
            raise MatrixFanError("intermediate dimension must be positive")
        energies = _finite_vector(
            item["intermediate_energies_ev"],
            f"contributions[{index}].intermediate_energies_ev",
        )
        occupations = _finite_vector(
            item["intermediate_occupations"],
            f"contributions[{index}].intermediate_occupations",
        )
        groups = list(item["intermediate_degeneracy_groups"])
        if energies.size != intermediate_dimension or occupations.size != intermediate_dimension:
            raise MatrixFanError("intermediate vector count does not match declared dimension")
        if len(groups) != intermediate_dimension:
            raise MatrixFanError("intermediate degeneracy-group count mismatch")
        vertex = decode_complex_matrix(item["vertex"], f"contributions[{index}].vertex")
        if vertex.shape != (intermediate_dimension, external_dimension):
            raise MatrixFanError("vertex shape does not match declared dimensions")
        normalized = {
            "vertex_ev": vertex,
            "intermediate_energies_ev": energies,
            "occupations": occupations,
            "phonon_energy_ev": float(item["phonon_energy_ev"]),
            "bose_occupation": float(item["bose_occupation"]),
            "q_weight": float(item["q_weight"]),
            "q_id": str(item["q_id"]),
            "mode_id": str(item["mode_id"]),
            "source_id": str(item["source_id"]),
            "intermediate_degeneracy_groups": groups,
        }
        fan_contribution_matrix(
            vertex,
            energy_ev=evaluation_energy,
            eta_ev=eta_ev,
            intermediate_energies_ev=energies,
            occupations=occupations,
            phonon_energy_ev=normalized["phonon_energy_ev"],
            bose_occupation=normalized["bose_occupation"],
            q_weight=normalized["q_weight"],
        )
        contributions.append(normalized)

    return {
        "passed": True,
        "external_dimension": external_dimension,
        "external_energies_ev": external_energies,
        "external_degeneracy_groups": external_groups,
        "evaluation_energy_ev": evaluation_energy,
        "eta_ev": eta_ev,
        "contributions": contributions,
    }


def evaluate_record(
    record: Mapping[str, Any], contract: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate and evaluate the retarded, Hermitian and linewidth matrices."""
    validated = validate_matrix_fan_record(record, contract)
    sigma = fan_matrix(
        validated["contributions"],
        validated["evaluation_energy_ev"],
        validated["eta_ev"],
    )
    gamma = linewidth_matrix(sigma)
    hermitian = hermitian_part(sigma)
    return {
        "schema_version": contract["schema_version"],
        "stage": contract["stage"],
        "status": "synthetic_matrix_fan_record_evaluated",
        "retarded_matrix": encode_complex_matrix(sigma),
        "hermitian_common_energy_matrix": encode_complex_matrix(hermitian),
        "linewidth_matrix": encode_complex_matrix(gamma),
        "diagnostics": {
            "hermitian_reduction_residual_ev": _max_abs(hermitian - hermitian.conj().T),
            "linewidth_hermiticity_residual_ev": _max_abs(gamma - gamma.conj().T),
            "linewidth_minimum_eigenvalue_ev": float(np.min(np.linalg.eigvalsh(gamma))),
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = evaluate_record(_load_json(args.record), _load_json(args.contract))
    Path(args.output_json).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
