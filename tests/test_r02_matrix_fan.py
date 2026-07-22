from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tools.matrix_fan import (
    MatrixFanError,
    encode_complex_matrix,
    evaluate_record,
    fan_matrix,
    fan_matrix_derivative,
    hermitian_part,
    linewidth_matrix,
    require_rotation_commutes_with_external_hamiltonian,
    rotate_external_contributions,
    rotate_intermediate_contribution,
    scalar_diagonal_reference,
    symmetrized_on_shell_hermitian,
    validate_matrix_fan_record,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "first_principles/b0/r02_matrix_fan_contract.json"


def _contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _unitary_2() -> np.ndarray:
    angle = 0.37
    phase = np.exp(0.31j)
    return np.array(
        [
            [np.cos(angle), -phase.conjugate() * np.sin(angle)],
            [phase * np.sin(angle), np.cos(angle)],
        ],
        dtype=complex,
    )


def _contribution(
    *,
    vertex: np.ndarray | None = None,
    intermediate_energies_ev: list[float] | None = None,
    occupations: list[float] | None = None,
    q_weight: float = 0.4,
) -> dict:
    if vertex is None:
        vertex = np.array(
            [
                [0.10 + 0.02j, 0.03 - 0.01j],
                [0.02 + 0.04j, -0.08 + 0.01j],
                [0.05 - 0.03j, 0.07 + 0.02j],
            ],
            dtype=complex,
        )
    return {
        "vertex_ev": np.asarray(vertex, dtype=complex),
        "intermediate_energies_ev": (
            [-0.3, 0.2, 0.7]
            if intermediate_energies_ev is None
            else intermediate_energies_ev
        ),
        "occupations": [1.0, 0.0, 0.0] if occupations is None else occupations,
        "phonon_energy_ev": 0.04,
        "bose_occupation": 0.3,
        "q_weight": q_weight,
    }


def _record() -> dict:
    vertex = _contribution()["vertex_ev"]
    return {
        "schema_version": "1.0",
        "stage": "B0_external_matrix_fan_contract",
        "metadata": {
            "source_id": "synthetic-two-band-fixture",
            "external_gauge_id": "synthetic-external-gauge",
            "intermediate_gauge_id": "synthetic-intermediate-gauge",
            "vertex_normalization": (
                "energy_normalized_includes_phonon_zero_point_amplitude"
            ),
            "vertex_units": "eV",
            "energy_units": "eV",
            "q_weight_location": "separate_scalar_not_in_vertex",
            "spin_convention": "explicit_spinors_no_extra_spin_factor",
            "retarded_sign_convention": "positive_eta",
            "long_range_included": False,
            "thermal_expansion_included": False,
        },
        "external_dimension": 2,
        "external_energies_ev": [-0.1, -0.1],
        "external_degeneracy_groups": ["A", "A"],
        "evaluation_energy_ev": 0.12,
        "eta_ev": 0.02,
        "contributions": [
            {
                "q_id": "q0",
                "mode_id": "nu0",
                "source_id": "synthetic-mode",
                "q_weight": 1.0,
                "phonon_energy_ev": 0.04,
                "bose_occupation": 0.3,
                "intermediate_dimension": 3,
                "intermediate_energies_ev": [-0.3, 0.2, 0.7],
                "intermediate_occupations": [1.0, 0.0, 0.0],
                "intermediate_degeneracy_groups": ["m0", "m1", "m2"],
                "vertex": encode_complex_matrix(vertex),
            }
        ],
    }


def test_contract_is_fail_closed_for_material_and_backend_work() -> None:
    contract = _contract()
    assert contract["issue"] == 296
    assert contract["invariants"]["long_range_included"] is False
    assert contract["invariants"]["thermal_expansion_included"] is False
    authorization = contract["authorization"]
    assert authorization["analytical_derivation"] is True
    assert authorization["synthetic_numpy_kernel"] is True
    assert authorization["backend_build"] is False
    assert authorization["backend_source_modification"] is False
    assert authorization["raw_vertex_material_export"] is False
    assert authorization["cdte_hgte_or_alloy_calculation"] is False
    assert authorization["a1_a2_a3"] is False


def test_json_record_passes_explicit_normalization_and_provenance_gates() -> None:
    validated = validate_matrix_fan_record(_record(), _contract())
    assert validated["passed"] is True
    assert validated["external_dimension"] == 2
    assert len(validated["contributions"]) == 1
    result = evaluate_record(_record(), _contract())
    assert result["status"] == "synthetic_matrix_fan_record_evaluated"
    assert result["diagnostics"]["linewidth_minimum_eigenvalue_ev"] >= -1.0e-12


def test_json_record_rejects_long_range_or_thermal_contamination() -> None:
    record = _record()
    record["metadata"]["long_range_included"] = True
    with pytest.raises(MatrixFanError, match="long_range_included"):
        validate_matrix_fan_record(record, _contract())

    record = _record()
    record["metadata"]["thermal_expansion_included"] = True
    with pytest.raises(MatrixFanError, match="thermal_expansion_included"):
        validate_matrix_fan_record(record, _contract())


def test_one_state_scalar_diagonal_equivalence() -> None:
    contributions = [
        {
            "vertex_ev": np.array([[0.2 + 0.1j]]),
            "intermediate_energies_ev": [0.4],
            "occupations": [0.0],
            "phonon_energy_ev": 0.05,
            "bose_occupation": 0.2,
            "q_weight": 0.3,
        }
    ]
    matrix = fan_matrix(contributions, 0.1, 0.01)
    scalar = scalar_diagonal_reference(contributions, 0, 0.1, 0.01)
    assert matrix[0, 0] == pytest.approx(scalar, abs=1.0e-14)


def test_multiband_diagonal_equivalence_for_every_external_index() -> None:
    contributions = [
        _contribution(),
        _contribution(
            vertex=np.array(
                [[0.0 + 0.02j, 0.03], [0.01, 0.0 + 0.04j], [0.03, 0.02]],
                dtype=complex,
            ),
            q_weight=0.6,
        ),
    ]
    matrix = fan_matrix(contributions, 0.11, 0.012)
    for external_index in range(2):
        scalar = scalar_diagonal_reference(
            contributions, external_index, 0.11, 0.012
        )
        assert matrix[external_index, external_index] == pytest.approx(
            scalar, abs=1.0e-14
        )


def test_external_unitary_covariance_requires_one_common_frequency() -> None:
    contributions = [_contribution()]
    unitary = _unitary_2()
    matrix = fan_matrix(contributions, 0.1, 0.02)
    rotated = fan_matrix(
        rotate_external_contributions(contributions, unitary), 0.1, 0.02
    )
    expected = unitary.conj().T @ matrix @ unitary
    assert np.max(np.abs(rotated - expected)) < 1.0e-13


def test_intermediate_rotation_is_invariant_inside_equal_denominator_block() -> None:
    unitary = np.eye(3, dtype=complex)
    unitary[:2, :2] = _unitary_2()
    contribution = _contribution(
        intermediate_energies_ev=[0.2, 0.2, 0.7],
        occupations=[0.0, 0.0, 1.0],
    )
    rotated = rotate_intermediate_contribution(
        contribution, unitary, energy_ev=0.1, eta_ev=0.02
    )
    reference_matrix = fan_matrix([contribution], 0.1, 0.02)
    rotated_matrix = fan_matrix([rotated], 0.1, 0.02)
    assert np.max(np.abs(rotated_matrix - reference_matrix)) < 1.0e-13


def test_intermediate_rotation_mixing_unequal_denominators_fails_closed() -> None:
    unitary = np.eye(3, dtype=complex)
    unitary[:2, :2] = _unitary_2()
    with pytest.raises(MatrixFanError, match="unequal denominator factors"):
        rotate_intermediate_contribution(
            _contribution(), unitary, energy_ev=0.1, eta_ev=0.02
        )


def test_retarded_linewidth_is_hermitian_positive_semidefinite() -> None:
    retarded = fan_matrix([_contribution()], 0.1, 0.02)
    linewidth = linewidth_matrix(retarded)
    assert np.max(np.abs(linewidth - linewidth.conj().T)) < 1.0e-13
    assert np.min(np.linalg.eigvalsh(linewidth)) >= -1.0e-13


def test_advanced_or_zero_eta_is_rejected() -> None:
    with pytest.raises(MatrixFanError, match="strictly positive"):
        fan_matrix([_contribution()], 0.1, 0.0)
    with pytest.raises(MatrixFanError, match="strictly positive"):
        fan_matrix([_contribution()], 0.1, -0.01)


def test_analytic_derivative_matches_centered_finite_difference() -> None:
    contributions = [_contribution()]
    energy = 0.12
    eta = 0.02
    step = 1.0e-6
    analytic = fan_matrix_derivative(contributions, energy, eta)
    numerical = (
        fan_matrix(contributions, energy + step, eta)
        - fan_matrix(contributions, energy - step, eta)
    ) / (2.0 * step)
    assert np.max(np.abs(analytic - numerical)) < 1.0e-8


def test_common_energy_and_on_shell_reductions_are_hermitian() -> None:
    contributions = [_contribution()]
    common = hermitian_part(fan_matrix(contributions, 0.1, 0.02))
    assert np.max(np.abs(common - common.conj().T)) < 1.0e-13

    external_energies = [-0.1, -0.1]
    on_shell = symmetrized_on_shell_hermitian(
        contributions, external_energies, 0.02
    )
    assert np.max(np.abs(on_shell - on_shell.conj().T)) < 1.0e-13
    for index, energy in enumerate(external_energies):
        diagonal = fan_matrix(contributions, energy, 0.02)[index, index].real
        assert on_shell[index, index].real == pytest.approx(diagonal, abs=1.0e-14)


def test_on_shell_form_is_covariant_inside_exactly_degenerate_external_block() -> None:
    contributions = [_contribution()]
    external_energies = [-0.1, -0.1]
    unitary = _unitary_2()
    require_rotation_commutes_with_external_hamiltonian(external_energies, unitary)
    reference = symmetrized_on_shell_hermitian(
        contributions, external_energies, 0.02
    )
    rotated = symmetrized_on_shell_hermitian(
        rotate_external_contributions(contributions, unitary),
        external_energies,
        0.02,
    )
    expected = unitary.conj().T @ reference @ unitary
    assert np.max(np.abs(rotated - expected)) < 1.0e-13


def test_on_shell_covariance_claim_rejects_non_degenerate_rotation() -> None:
    with pytest.raises(MatrixFanError, match="unequal unperturbed energies"):
        require_rotation_commutes_with_external_hamiltonian(
            [-0.1, 0.2], _unitary_2()
        )


def test_zero_coupling_limit_is_exact() -> None:
    contribution = _contribution(vertex=np.zeros((3, 2), dtype=complex))
    matrix = fan_matrix([contribution], 0.1, 0.02)
    assert np.max(np.abs(matrix)) <= 1.0e-15
