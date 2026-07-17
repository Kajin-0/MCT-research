from __future__ import annotations

import math

import numpy as np

from mct_research.kane8 import (
    ExtendedKaneParameters,
    hamiltonian_two_p,
    time_reversal_unitary,
)
from tools.analyze_kane_symmetry_intertwiner import (
    analyze,
    coupled_p_basis,
    rotation,
    target_blocks,
    time_reversal_blocks,
)


def _full_blocks(blocks: tuple[np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
    gamma6, gamma8, gamma7 = blocks
    matrix = np.zeros((8, 8), dtype=complex)
    matrix[0:2, 0:2] = gamma6
    matrix[2:6, 2:6] = gamma8
    matrix[6:8, 6:8] = gamma7
    return matrix


def test_double_group_intertwiner_recovers_canonical_blocks() -> None:
    result = analyze()
    assert result["basis_convention"] == "Novik_2005_Eq_4"
    assert result["maximum_recovery_error"] < 1.0e-12
    assert result["maximum_symmetry_residual"] < 1.0e-12
    assert result["maximum_time_reversal_residual"] < 1.0e-12
    for block in result["irreps"].values():
        assert block["nullity_C3_only"] > 1
        assert block["nullity_C3_and_S4"] == 1
        assert block["next_singular_value_above_nullspace"] > 0.9
        assert block["character_error_after_random_gauge"] < 1.0e-12


def test_coupled_p_basis_matches_novik_equation_4() -> None:
    x = np.array([1.0, 0.0, 0.0])
    y = np.array([0.0, 1.0, 0.0])
    z = np.array([0.0, 0.0, 1.0])
    up = np.array([1.0, 0.0])
    down = np.array([0.0, 1.0])
    product = lambda orbital, spin: np.kron(orbital, spin)

    expected_gamma8 = np.column_stack(
        [
            product(x + 1j * y, up) / math.sqrt(2.0),
            (product(x + 1j * y, down) - 2.0 * product(z, up))
            / math.sqrt(6.0),
            -(product(x - 1j * y, up) + 2.0 * product(z, down))
            / math.sqrt(6.0),
            -product(x - 1j * y, down) / math.sqrt(2.0),
        ]
    )
    expected_gamma7 = np.column_stack(
        [
            (product(x + 1j * y, down) + product(z, up)) / math.sqrt(3.0),
            (product(x - 1j * y, up) - product(z, down)) / math.sqrt(3.0),
        ]
    )
    gamma8, gamma7 = coupled_p_basis()
    assert np.linalg.norm(gamma8 - expected_gamma8) < 1.0e-14
    assert np.linalg.norm(gamma7 - expected_gamma7) < 1.0e-14


def test_symmetry_targets_covary_with_executable_novik_hamiltonian() -> None:
    parameters = ExtendedKaneParameters(
        ev=0.13,
        eg=1.47,
        delta=0.91,
        p8=7.4,
        p7=6.8,
        f=-0.09,
        gamma1=1.47,
        gamma2=-0.28,
        gamma3=0.03,
    )
    k = np.array([0.011, -0.007, 0.013])
    operations = (
        rotation((1.0, 1.0, 1.0), 2.0 * math.pi / 3.0),
        np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, -1.0]]),
    )
    for orthogonal in operations:
        representation = _full_blocks(target_blocks(orthogonal))
        transformed = representation @ hamiltonian_two_p(k, parameters) @ representation.conj().T
        expected = hamiltonian_two_p(orthogonal @ k, parameters)
        assert np.linalg.norm(transformed - expected) < 1.0e-12


def test_time_reversal_targets_match_executable_novik_convention() -> None:
    target = _full_blocks(time_reversal_blocks())
    assert np.linalg.norm(target - time_reversal_unitary()) < 1.0e-14
