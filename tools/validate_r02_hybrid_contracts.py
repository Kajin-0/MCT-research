#!/usr/bin/env python3
"""Validate R02 hybrid short-range matrix and generalized-Frohlich contracts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


class ContractError(ValueError):
    """Raised when a record violates an R02 hybrid contract."""


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"expected a JSON object in {path}")
    return value


def _require_keys(mapping: Mapping[str, Any], keys: Sequence[str], context: str) -> None:
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise ContractError(f"{context} missing keys: {', '.join(missing)}")


def _finite_array(value: Any, *, shape: tuple[int, ...], context: str) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if array.shape != shape:
        raise ContractError(f"{context} has shape {array.shape}, expected {shape}")
    if not np.all(np.isfinite(array)):
        raise ContractError(f"{context} contains non-finite values")
    return array


def decode_complex_matrix(value: Mapping[str, Any], dimension: int, context: str) -> np.ndarray:
    _require_keys(value, ("real", "imag"), context)
    real = _finite_array(value["real"], shape=(dimension, dimension), context=f"{context}.real")
    imag = _finite_array(value["imag"], shape=(dimension, dimension), context=f"{context}.imag")
    return real + 1j * imag


def encode_complex_matrix(matrix: np.ndarray) -> dict[str, list[list[float]]]:
    array = np.asarray(matrix, dtype=complex)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        raise ContractError("matrix must be square")
    return {"real": array.real.tolist(), "imag": array.imag.tolist()}


def _max_abs(value: np.ndarray) -> float:
    return float(np.max(np.abs(value))) if value.size else 0.0


def _hermiticity_residual(matrix: np.ndarray) -> float:
    return _max_abs(matrix - matrix.conj().T)


def validate_short_range_record(
    record: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    if contract.get("stage") != "B0_hybrid_short_range_matrix_contract":
        raise ContractError("unexpected short-range contract stage")
    dimension = int(contract["matrix_dimension"])
    required_components = list(contract["required_components"])
    tolerances = contract["tolerances"]

    _require_keys(
        record,
        (
            "schema_version",
            "stage",
            "metadata",
            "long_range_included",
            "thermal_expansion_included",
            "components",
            "total",
            "standard_diagonal_ev",
        ),
        "short-range record",
    )
    if record["stage"] != contract["stage"]:
        raise ContractError("short-range record stage does not match contract")
    if record["schema_version"] != contract["schema_version"]:
        raise ContractError("short-range record schema version does not match contract")
    if record["long_range_included"] is not False:
        raise ContractError("short-range record must explicitly exclude long-range physics")
    if record["thermal_expansion_included"] is not False:
        raise ContractError("short-range record must explicitly exclude thermal expansion")

    metadata = record["metadata"]
    if not isinstance(metadata, Mapping):
        raise ContractError("short-range metadata must be an object")
    _require_keys(metadata, contract["required_metadata"], "short-range metadata")
    if not isinstance(metadata["commit_sha"], str) or len(metadata["commit_sha"]) != 40:
        raise ContractError("metadata.commit_sha must be a full 40-character SHA")
    for name in (
        "source_archive_sha256",
        "executable_sha256",
        "ground_state_sha256",
        "wfpt_state_sha256",
    ):
        value = metadata[name]
        if not isinstance(value, str) or len(value) != 64:
            raise ContractError(f"metadata.{name} must be a 64-character SHA-256")
    _finite_array(metadata["k_point_crystal"], shape=(3,), context="metadata.k_point_crystal")
    if float(metadata["reference_volume_angstrom3"]) <= 0:
        raise ContractError("reference volume must be positive")
    if float(metadata["temperature_k"]) < 0:
        raise ContractError("temperature cannot be negative")

    components_value = record["components"]
    if not isinstance(components_value, Mapping):
        raise ContractError("components must be an object")
    if set(components_value) != set(required_components):
        raise ContractError(
            f"components must be exactly {required_components}, got {sorted(components_value)}"
        )

    component_matrices: dict[str, np.ndarray] = {}
    hermiticity: dict[str, float] = {}
    hermiticity_limit = float(tolerances["hermiticity_max_abs_ev"])
    for name in required_components:
        matrix = decode_complex_matrix(components_value[name], dimension, f"components.{name}")
        residual = _hermiticity_residual(matrix)
        if residual > hermiticity_limit:
            raise ContractError(
                f"components.{name} is not Hermitian: residual {residual:.6e} eV"
            )
        component_matrices[name] = matrix
        hermiticity[name] = residual

    total = decode_complex_matrix(record["total"], dimension, "total")
    total_hermiticity = _hermiticity_residual(total)
    if total_hermiticity > hermiticity_limit:
        raise ContractError(f"total is not Hermitian: residual {total_hermiticity:.6e} eV")

    component_sum = sum(component_matrices.values(), np.zeros_like(total))
    component_sum_residual = _max_abs(total - component_sum)
    if component_sum_residual > float(tolerances["component_sum_max_abs_ev"]):
        raise ContractError(
            f"total does not equal component sum: residual {component_sum_residual:.6e} eV"
        )

    standard_diagonal = _finite_array(
        record["standard_diagonal_ev"],
        shape=(dimension,),
        context="standard_diagonal_ev",
    )
    diagonal_imag_residual = _max_abs(np.imag(np.diag(total)))
    diagonal_recovery_residual = _max_abs(standard_diagonal - np.real(np.diag(total)))
    diagonal_limit = float(tolerances["diagonal_recovery_max_abs_ev"])
    if diagonal_imag_residual > diagonal_limit:
        raise ContractError(
            f"total diagonal has non-negligible imaginary part: {diagonal_imag_residual:.6e} eV"
        )
    if diagonal_recovery_residual > diagonal_limit:
        raise ContractError(
            "standard diagonal does not match exported total diagonal: "
            f"{diagonal_recovery_residual:.6e} eV"
        )

    return {
        "passed": True,
        "dimension": dimension,
        "hermiticity_max_abs_ev": {**hermiticity, "total": total_hermiticity},
        "component_sum_max_abs_ev": component_sum_residual,
        "diagonal_recovery_max_abs_ev": diagonal_recovery_residual,
        "matrices": component_matrices,
        "total_matrix": total,
    }


def validate_covariant_pair(
    reference_record: Mapping[str, Any],
    rotated_record: Mapping[str, Any],
    unitary_value: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    reference = validate_short_range_record(reference_record, contract)
    rotated = validate_short_range_record(rotated_record, contract)
    dimension = reference["dimension"]
    unitary = decode_complex_matrix(unitary_value, dimension, "unitary")
    tolerances = contract["tolerances"]

    unitary_residual = _max_abs(unitary.conj().T @ unitary - np.eye(dimension))
    if unitary_residual > float(tolerances["unitarity_max_abs"]):
        raise ContractError(f"declared transform is not unitary: {unitary_residual:.6e}")

    residuals: dict[str, float] = {}
    for name in contract["required_components"]:
        expected = unitary.conj().T @ reference["matrices"][name] @ unitary
        residuals[name] = _max_abs(rotated["matrices"][name] - expected)
    expected_total = unitary.conj().T @ reference["total_matrix"] @ unitary
    residuals["total"] = _max_abs(rotated["total_matrix"] - expected_total)
    covariance_residual = max(residuals.values())
    if covariance_residual > float(tolerances["covariance_max_abs_ev"]):
        raise ContractError(
            f"matrix export is not unitary-covariant: residual {covariance_residual:.6e} eV"
        )

    return {
        "passed": True,
        "unitarity_max_abs": unitary_residual,
        "covariance_max_abs_ev": covariance_residual,
        "component_residuals_ev": residuals,
    }


def _validate_symmetric_tensor(
    value: Any,
    *,
    context: str,
    symmetry_limit: float,
    eigenvalue_min: float,
    semidefinite: bool = False,
) -> np.ndarray:
    tensor = _finite_array(value, shape=(3, 3), context=context)
    symmetry_residual = _max_abs(tensor - tensor.T)
    if symmetry_residual > symmetry_limit:
        raise ContractError(f"{context} is not symmetric: residual {symmetry_residual:.6e}")
    eigenvalues = np.linalg.eigvalsh((tensor + tensor.T) / 2.0)
    limit = eigenvalue_min
    if float(np.min(eigenvalues)) < limit:
        qualifier = "positive semidefinite" if semidefinite else "positive definite"
        raise ContractError(
            f"{context} is not {qualifier}: minimum eigenvalue {np.min(eigenvalues):.6e}"
        )
    return tensor


def validate_frohlich_input(
    record: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    if contract.get("stage") != "B0_generalized_frohlich_input_contract":
        raise ContractError("unexpected generalized-Frohlich contract stage")
    _require_keys(
        record,
        (
            "schema_version",
            "stage",
            "material",
            "phase",
            "reference_volume_angstrom3",
            "reference_temperature_k",
            "epsilon_infinity",
            "epsilon_static",
            "lo_modes",
            "effective_mass_branches",
            "edge_covariance_ev2",
            "nonadiabatic_denominator_convention",
            "input_origin_flags",
            "provenance",
        ),
        "generalized-Frohlich record",
    )
    if record["schema_version"] != contract["schema_version"]:
        raise ContractError("generalized-Frohlich schema version mismatch")
    if record["stage"] != contract["stage"]:
        raise ContractError("generalized-Frohlich stage mismatch")
    if float(record["reference_volume_angstrom3"]) <= 0:
        raise ContractError("reference volume must be positive")
    if float(record["reference_temperature_k"]) < 0:
        raise ContractError("reference temperature cannot be negative")
    if not str(record["nonadiabatic_denominator_convention"]).strip():
        raise ContractError("nonadiabatic denominator convention is required")

    flags = record["input_origin_flags"]
    if not isinstance(flags, Mapping):
        raise ContractError("input_origin_flags must be an object")
    if flags.get("uses_failed_cdte_born_tensors") is not False:
        raise ContractError("failed CdTe Born tensors are prohibited")
    if flags.get("uses_charge_asr_repaired_inputs") is not False:
        raise ContractError("charge-ASR-repaired inputs are prohibited")

    tolerances = contract["tolerances"]
    symmetry_limit = float(tolerances["symmetry_max_abs"])
    positive_min = float(tolerances["positive_eigenvalue_min"])
    psd_min = float(tolerances["positive_semidefinite_min"])
    epsilon_inf = _validate_symmetric_tensor(
        record["epsilon_infinity"],
        context="epsilon_infinity",
        symmetry_limit=symmetry_limit,
        eigenvalue_min=positive_min,
    )
    epsilon_static = _validate_symmetric_tensor(
        record["epsilon_static"],
        context="epsilon_static",
        symmetry_limit=symmetry_limit,
        eigenvalue_min=positive_min,
    )
    dielectric_increment = _validate_symmetric_tensor(
        epsilon_static - epsilon_inf,
        context="epsilon_static_minus_infinity",
        symmetry_limit=symmetry_limit,
        eigenvalue_min=psd_min,
        semidefinite=True,
    )

    modes = record["lo_modes"]
    if not isinstance(modes, list) or not modes:
        raise ContractError("at least one LO mode is required")
    branch_ids: set[str] = set()
    for index, mode in enumerate(modes):
        if not isinstance(mode, Mapping):
            raise ContractError(f"lo_modes[{index}] must be an object")
        _require_keys(
            mode,
            ("branch_id", "frequency_mev", "frequency_uncertainty_mev", "source_id"),
            f"lo_modes[{index}]",
        )
        branch_id = str(mode["branch_id"])
        if not branch_id or branch_id in branch_ids:
            raise ContractError("LO branch identifiers must be non-empty and unique")
        branch_ids.add(branch_id)
        if float(mode["frequency_mev"]) <= 0:
            raise ContractError(f"lo_modes[{index}] frequency must be positive")
        if float(mode["frequency_uncertainty_mev"]) < 0:
            raise ContractError(f"lo_modes[{index}] uncertainty cannot be negative")
        if not str(mode["source_id"]).strip():
            raise ContractError(f"lo_modes[{index}] source_id is required")

    mass_values = record["effective_mass_branches"]
    if not isinstance(mass_values, Mapping):
        raise ContractError("effective_mass_branches must be an object")
    expected_reps = set(contract["required_representations"])
    if set(mass_values) != expected_reps:
        raise ContractError(
            f"effective_mass_branches must contain exactly {sorted(expected_reps)}"
        )
    mass_tensors: dict[str, list[np.ndarray]] = {}
    multiplicities: dict[str, int] = {}
    for representation in contract["required_representations"]:
        branches = mass_values[representation]
        if not isinstance(branches, list) or not branches:
            raise ContractError(
                f"effective_mass_branches.{representation} must be a non-empty list"
            )
        mass_branch_ids: set[str] = set()
        mass_tensors[representation] = []
        multiplicities[representation] = 0
        for index, entry in enumerate(branches):
            context = f"effective_mass_branches.{representation}[{index}]"
            if not isinstance(entry, Mapping):
                raise ContractError(f"{context} must be an object")
            _require_keys(
                entry,
                (
                    "branch_id",
                    "multiplicity",
                    "carrier_type",
                    "mass_sign_convention",
                    "tensor",
                    "relative_uncertainty",
                    "fit_window_inv_angstrom",
                    "source_id",
                ),
                context,
            )
            branch_id = str(entry["branch_id"])
            if not branch_id or branch_id in mass_branch_ids:
                raise ContractError(f"{context}.branch_id must be non-empty and unique")
            mass_branch_ids.add(branch_id)
            multiplicity = int(entry["multiplicity"])
            if multiplicity <= 0:
                raise ContractError(f"{context}.multiplicity must be positive")
            multiplicities[representation] += multiplicity
            if entry["carrier_type"] not in {"electron", "hole"}:
                raise ContractError(f"{context}.carrier_type must be electron or hole")
            if entry["mass_sign_convention"] != "positive_carrier_mass_magnitude":
                raise ContractError(
                    f"{context}.mass_sign_convention must be positive_carrier_mass_magnitude"
                )
            tensor = _validate_symmetric_tensor(
                entry["tensor"],
                context=f"{context}.tensor",
                symmetry_limit=symmetry_limit,
                eigenvalue_min=positive_min,
            )
            mass_tensors[representation].append(tensor)
            if float(entry["relative_uncertainty"]) < 0:
                raise ContractError(f"{context}.relative_uncertainty cannot be negative")
            if float(entry["fit_window_inv_angstrom"]) <= 0:
                raise ContractError(f"{context}.fit_window_inv_angstrom must be positive")
            if not str(entry["source_id"]).strip():
                raise ContractError(f"{context}.source_id is required")
        expected_multiplicity = int(contract["required_degeneracies"][representation])
        if multiplicities[representation] != expected_multiplicity:
            raise ContractError(
                f"{representation} branch multiplicity {multiplicities[representation]} "
                f"does not close required degeneracy {expected_multiplicity}"
            )

    covariance = _validate_symmetric_tensor(
        record["edge_covariance_ev2"],
        context="edge_covariance_ev2",
        symmetry_limit=symmetry_limit,
        eigenvalue_min=float(tolerances["covariance_positive_semidefinite_min"]),
        semidefinite=True,
    )

    provenance = record["provenance"]
    if not isinstance(provenance, Mapping):
        raise ContractError("provenance must be an object")
    _require_keys(
        provenance,
        (
            "epsilon_infinity",
            "epsilon_static",
            "lo_modes",
            "effective_mass_branches",
            "reference_volume",
        ),
        "provenance",
    )
    for key, value in provenance.items():
        if not isinstance(value, Mapping):
            raise ContractError(f"provenance.{key} must be an object")
        _require_keys(
            value,
            ("source_id", "sha256_or_doi", "uncertainty_semantics"),
            f"provenance.{key}",
        )
        if not all(
            str(value[field]).strip()
            for field in ("source_id", "sha256_or_doi", "uncertainty_semantics")
        ):
            raise ContractError(f"provenance.{key} fields must be non-empty")

    return {
        "passed": True,
        "minimum_epsilon_infinity_eigenvalue": float(np.min(np.linalg.eigvalsh(epsilon_inf))),
        "minimum_epsilon_static_eigenvalue": float(np.min(np.linalg.eigvalsh(epsilon_static))),
        "minimum_dielectric_increment_eigenvalue": float(
            np.min(np.linalg.eigvalsh(dielectric_increment))
        ),
        "minimum_mass_eigenvalue_by_representation": {
            key: min(float(np.min(np.linalg.eigvalsh(tensor))) for tensor in tensors)
            for key, tensors in mass_tensors.items()
        },
        "branch_multiplicity_by_representation": multiplicities,
        "minimum_covariance_eigenvalue_ev2": float(np.min(np.linalg.eigvalsh(covariance))),
        "lo_mode_count": len(modes),
    }


def _long_range_matrix(edge_corrections_ev: Mapping[str, Any]) -> np.ndarray:
    _require_keys(edge_corrections_ev, ("Gamma6", "Gamma8", "Gamma7"), "edge corrections")
    values = {key: float(edge_corrections_ev[key]) for key in ("Gamma6", "Gamma8", "Gamma7")}
    if not all(np.isfinite(value) for value in values.values()):
        raise ContractError("edge corrections contain non-finite values")
    diagonal = [values["Gamma6"]] * 2 + [values["Gamma8"]] * 4 + [values["Gamma7"]] * 2
    return np.diag(diagonal).astype(complex)


def validate_hybrid_combination(
    short_record: Mapping[str, Any],
    edge_corrections_ev: Mapping[str, Any],
    declared_combined: Mapping[str, Any],
    short_contract: Mapping[str, Any],
) -> dict[str, Any]:
    short = validate_short_range_record(short_record, short_contract)
    dimension = short["dimension"]
    if dimension != 8:
        raise ContractError("generalized-Frohlich Gamma-block expansion requires dimension 8")
    long_range = _long_range_matrix(edge_corrections_ev)
    declared = decode_complex_matrix(declared_combined, dimension, "declared_combined")
    expected = short["total_matrix"] + long_range
    residual = _max_abs(declared - expected)
    limit = float(short_contract["tolerances"]["no_double_counting_max_abs_ev"])
    if residual > limit:
        double_added = _max_abs(declared - (short["total_matrix"] + 2.0 * long_range))
        reason = "long-range term appears double-counted" if double_added <= limit else "combination mismatch"
        raise ContractError(f"{reason}: residual {residual:.6e} eV")
    return {
        "passed": True,
        "combination_max_abs_ev": residual,
        "combined_matrix": expected,
        "long_range_matrix": long_range,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--short-contract")
    parser.add_argument("--short-record")
    parser.add_argument("--frohlich-contract")
    parser.add_argument("--frohlich-record")
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    result: dict[str, Any] = {"schema_version": "1.0", "checks": {}}
    if bool(args.short_contract) != bool(args.short_record):
        parser.error("--short-contract and --short-record must be supplied together")
    if bool(args.frohlich_contract) != bool(args.frohlich_record):
        parser.error("--frohlich-contract and --frohlich-record must be supplied together")
    if not args.short_contract and not args.frohlich_contract:
        parser.error("at least one contract/record pair is required")

    try:
        if args.short_contract:
            result["checks"]["short_range"] = {
                key: value
                for key, value in validate_short_range_record(
                    _load_json(args.short_record), _load_json(args.short_contract)
                ).items()
                if key not in {"matrices", "total_matrix"}
            }
        if args.frohlich_contract:
            result["checks"]["generalized_frohlich"] = validate_frohlich_input(
                _load_json(args.frohlich_record), _load_json(args.frohlich_contract)
            )
        result["passed"] = True
    except ContractError as exc:
        result["passed"] = False
        result["error"] = str(exc)

    Path(args.output_json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
