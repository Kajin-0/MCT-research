from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tools.validate_r02_hybrid_contracts import (
    ContractError,
    encode_complex_matrix,
    validate_covariant_pair,
    validate_frohlich_input,
    validate_hybrid_combination,
    validate_short_range_record,
)

ROOT = Path(__file__).resolve().parents[1]
SHORT_CONTRACT_PATH = ROOT / "first_principles/b0/r02_hybrid_matrix_contract.json"
FROHLICH_CONTRACT_PATH = ROOT / "first_principles/b0/r02_generalized_frohlich_contract.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash(character: str) -> str:
    return character * 64


def _metadata() -> dict:
    return {
        "backend": "synthetic",
        "release": "B0",
        "commit_sha": "1" * 40,
        "source_archive_sha256": _hash("2"),
        "executable_sha256": _hash("3"),
        "ground_state_sha256": _hash("4"),
        "wfpt_state_sha256": _hash("5"),
        "reference_volume_angstrom3": 271.0,
        "temperature_k": 0.0,
        "k_point_crystal": [0.0, 0.0, 0.0],
        "source_gauge_id": "synthetic-source",
        "canonical_transform_id": "identity",
        "denominator_convention": "static synthetic test",
    }


def _component_matrices() -> dict[str, np.ndarray]:
    lower = np.diag(
        [0.010, 0.010, -0.004, -0.004, -0.004, -0.004, -0.006, -0.006]
    ).astype(complex)
    lower[0, 1] = 0.001 + 0.002j
    lower[1, 0] = lower[0, 1].conjugate()

    upper = np.diag(
        [0.002, 0.002, 0.001, 0.001, 0.001, 0.001, -0.001, -0.001]
    ).astype(complex)
    upper[2, 3] = -0.0005j
    upper[3, 2] = upper[2, 3].conjugate()

    dw = np.diag(
        [-0.003, -0.003, 0.002, 0.002, 0.002, 0.002, 0.001, 0.001]
    ).astype(complex)
    return {"lower_fan": lower, "upper_fan": upper, "debye_waller": dw}


def _short_record(matrices: dict[str, np.ndarray] | None = None) -> dict:
    components = _component_matrices() if matrices is None else matrices
    total = sum(components.values(), np.zeros((8, 8), dtype=complex))
    return {
        "schema_version": "1.0",
        "stage": "B0_hybrid_short_range_matrix_contract",
        "metadata": _metadata(),
        "long_range_included": False,
        "thermal_expansion_included": False,
        "components": {
            name: encode_complex_matrix(value) for name, value in components.items()
        },
        "total": encode_complex_matrix(total),
        "standard_diagonal_ev": np.real(np.diag(total)).tolist(),
    }


def _block_unitary() -> np.ndarray:
    angle = 0.37
    phase = np.exp(0.41j)
    unitary = np.eye(8, dtype=complex)
    unitary[:2, :2] = np.array(
        [
            [np.cos(angle), -phase.conjugate() * np.sin(angle)],
            [phase * np.sin(angle), np.cos(angle)],
        ],
        dtype=complex,
    )
    return unitary


def _rotated_record(record: dict, unitary: np.ndarray) -> dict:
    components = {
        name: unitary.conj().T
        @ (
            np.asarray(value["real"], dtype=float)
            + 1j * np.asarray(value["imag"], dtype=float)
        )
        @ unitary
        for name, value in record["components"].items()
    }
    rotated = _short_record(components)
    rotated["metadata"]["source_gauge_id"] = "synthetic-rotated"
    rotated["metadata"]["canonical_transform_id"] = "block-unitary"
    return rotated


def _provenance(source_id: str) -> dict:
    return {
        "source_id": source_id,
        "sha256_or_doi": f"doi:{source_id}",
        "uncertainty_semantics": "synthetic standard uncertainty",
    }


def _frohlich_record() -> dict:
    return {
        "schema_version": "1.0",
        "stage": "B0_generalized_frohlich_input_contract",
        "material": "synthetic zincblende",
        "phase": "zincblende",
        "reference_volume_angstrom3": 271.0,
        "reference_temperature_k": 0.0,
        "epsilon_infinity": [
            [7.0, 0.0, 0.0],
            [0.0, 7.0, 0.0],
            [0.0, 0.0, 7.0],
        ],
        "epsilon_static": [
            [10.0, 0.0, 0.0],
            [0.0, 10.0, 0.0],
            [0.0, 0.0, 10.0],
        ],
        "lo_modes": [
            {
                "branch_id": "LO1",
                "frequency_mev": 21.0,
                "frequency_uncertainty_mev": 0.2,
                "source_id": "synthetic-lo",
            }
        ],
        "effective_mass_tensors": {
            "Gamma6": {
                "tensor": [
                    [0.10, 0.0, 0.0],
                    [0.0, 0.10, 0.0],
                    [0.0, 0.0, 0.10],
                ],
                "relative_uncertainty": 0.05,
                "source_id": "synthetic-mass",
            },
            "Gamma8": {
                "tensor": [
                    [0.40, 0.0, 0.0],
                    [0.0, 0.40, 0.0],
                    [0.0, 0.0, 0.40],
                ],
                "relative_uncertainty": 0.08,
                "source_id": "synthetic-mass",
            },
            "Gamma7": {
                "tensor": [
                    [0.20, 0.0, 0.0],
                    [0.0, 0.20, 0.0],
                    [0.0, 0.0, 0.20],
                ],
                "relative_uncertainty": 0.07,
                "source_id": "synthetic-mass",
            },
        },
        "edge_covariance_ev2": [
            [1.0e-6, 0.2e-6, 0.0],
            [0.2e-6, 2.0e-6, 0.1e-6],
            [0.0, 0.1e-6, 1.5e-6],
        ],
        "nonadiabatic_denominator_convention": (
            "retarded finite-phonon-frequency synthetic convention"
        ),
        "input_origin_flags": {
            "uses_failed_cdte_born_tensors": False,
            "uses_charge_asr_repaired_inputs": False,
        },
        "provenance": {
            "epsilon_infinity": _provenance("epsilon-infinity"),
            "epsilon_static": _provenance("epsilon-static"),
            "lo_modes": _provenance("lo-modes"),
            "effective_mass_tensors": _provenance("effective-masses"),
            "reference_volume": _provenance("reference-volume"),
        },
    }


def test_contracts_remain_fail_closed() -> None:
    short = _load(SHORT_CONTRACT_PATH)
    frohlich = _load(FROHLICH_CONTRACT_PATH)
    assert short["issue"] == 287
    assert short["invariants"]["long_range_included"] is False
    assert short["authorization"]["cdte_material_calculation"] is False
    assert short["authorization"]["hgte_material_calculation"] is False
    assert short["authorization"]["alter_scientific_algorithm"] is False
    assert frohlich["issue"] == 287
    assert frohlich["requirements"]["failed_cdte_born_tensors_prohibited"] is True
    assert frohlich["requirements"]["charge_asr_repaired_inputs_prohibited"] is True
    assert frohlich["authorization"]["material_prediction"] is False


def test_short_range_record_passes_and_recovers_standard_diagonal() -> None:
    result = validate_short_range_record(_short_record(), _load(SHORT_CONTRACT_PATH))
    assert result["passed"] is True
    assert result["component_sum_max_abs_ev"] == pytest.approx(0.0)
    assert result["diagonal_recovery_max_abs_ev"] == pytest.approx(0.0)


def test_short_range_record_rejects_long_range_contamination() -> None:
    record = _short_record()
    record["long_range_included"] = True
    with pytest.raises(ContractError, match="exclude long-range"):
        validate_short_range_record(record, _load(SHORT_CONTRACT_PATH))


def test_short_range_record_rejects_nonhermitian_component() -> None:
    record = _short_record()
    record["components"]["lower_fan"]["imag"][0][1] += 0.01
    with pytest.raises(ContractError, match="not Hermitian"):
        validate_short_range_record(record, _load(SHORT_CONTRACT_PATH))


def test_short_range_record_rejects_diagonal_collapse_mismatch() -> None:
    record = _short_record()
    record["standard_diagonal_ev"][0] += 1.0e-4
    with pytest.raises(ContractError, match="standard diagonal"):
        validate_short_range_record(record, _load(SHORT_CONTRACT_PATH))


def test_matrix_export_is_covariant_under_degenerate_block_rotation() -> None:
    contract = _load(SHORT_CONTRACT_PATH)
    reference = _short_record()
    unitary = _block_unitary()
    rotated = _rotated_record(reference, unitary)
    result = validate_covariant_pair(
        reference,
        rotated,
        encode_complex_matrix(unitary),
        contract,
    )
    assert result["passed"] is True
    assert result["covariance_max_abs_ev"] < 1.0e-12


def test_covariance_check_rejects_component_invariant_only_by_diagonal() -> None:
    contract = _load(SHORT_CONTRACT_PATH)
    reference = _short_record()
    unitary = _block_unitary()
    rotated = _rotated_record(reference, unitary)
    rotated["components"]["lower_fan"]["real"][0][1] += 1.0e-4
    rotated["components"]["lower_fan"]["real"][1][0] += 1.0e-4
    matrices = {
        name: np.asarray(value["real"]) + 1j * np.asarray(value["imag"])
        for name, value in rotated["components"].items()
    }
    total = sum(matrices.values(), np.zeros((8, 8), dtype=complex))
    rotated["total"] = encode_complex_matrix(total)
    rotated["standard_diagonal_ev"] = np.real(np.diag(total)).tolist()
    with pytest.raises(ContractError, match="not unitary-covariant"):
        validate_covariant_pair(reference, rotated, encode_complex_matrix(unitary), contract)


def test_frohlich_input_passes_positive_tensor_and_provenance_gates() -> None:
    result = validate_frohlich_input(
        _frohlich_record(),
        _load(FROHLICH_CONTRACT_PATH),
    )
    assert result["passed"] is True
    assert result["lo_mode_count"] == 1
    assert result["minimum_dielectric_increment_eigenvalue"] == pytest.approx(3.0)


def test_frohlich_input_rejects_failed_born_tensor_origin() -> None:
    record = _frohlich_record()
    record["input_origin_flags"]["uses_failed_cdte_born_tensors"] = True
    with pytest.raises(ContractError, match="failed CdTe Born tensors"):
        validate_frohlich_input(record, _load(FROHLICH_CONTRACT_PATH))


def test_frohlich_input_rejects_unphysical_dielectric_ordering() -> None:
    record = _frohlich_record()
    record["epsilon_static"][0][0] = 6.0
    with pytest.raises(ContractError, match="epsilon_static_minus_infinity"):
        validate_frohlich_input(record, _load(FROHLICH_CONTRACT_PATH))


def test_hybrid_combination_adds_long_range_exactly_once() -> None:
    contract = _load(SHORT_CONTRACT_PATH)
    short_record = _short_record()
    short_total = np.asarray(short_record["total"]["real"]) + 1j * np.asarray(
        short_record["total"]["imag"]
    )
    edges = {"Gamma6": 0.004, "Gamma8": -0.002, "Gamma7": -0.001}
    long_diagonal = np.diag([0.004, 0.004] + [-0.002] * 4 + [-0.001] * 2)
    declared = encode_complex_matrix(short_total + long_diagonal)
    result = validate_hybrid_combination(short_record, edges, declared, contract)
    assert result["passed"] is True
    assert result["combination_max_abs_ev"] == pytest.approx(0.0)


def test_hybrid_combination_detects_double_counting() -> None:
    contract = _load(SHORT_CONTRACT_PATH)
    short_record = _short_record()
    short_total = np.asarray(short_record["total"]["real"]) + 1j * np.asarray(
        short_record["total"]["imag"]
    )
    edges = {"Gamma6": 0.004, "Gamma8": -0.002, "Gamma7": -0.001}
    long_diagonal = np.diag([0.004, 0.004] + [-0.002] * 4 + [-0.001] * 2)
    declared = encode_complex_matrix(short_total + 2.0 * long_diagonal)
    with pytest.raises(ContractError, match="double-counted"):
        validate_hybrid_combination(short_record, edges, declared, contract)
