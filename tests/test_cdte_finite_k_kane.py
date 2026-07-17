from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from mct_research.kane8 import ExtendedKaneParameters, hamiltonian_two_p
from tools import analyze_cdte_finite_k_kane as finite
from tools import cdte_finite_k_projection as projection


def _serialized(matrix: np.ndarray) -> list[list[list[float]]]:
    return [
        [[float(value.real), float(value.imag)] for value in row]
        for row in np.asarray(matrix, dtype=complex)
    ]


def _basis_result() -> dict[str, object]:
    return {
        "selected_global_bands_one_based": list(range(31, 39)),
        "upstream": {"basis_convention": "Novik_2005_Eq_4"},
        "irreps": {
            "Gamma7": {
                "probe_block_index": 0,
                "bands_one_based": [31, 32],
                "intertwiner": _serialized(np.eye(2)),
            },
            "Gamma8": {
                "probe_block_index": 1,
                "bands_one_based": [33, 34, 35, 36],
                "intertwiner": _serialized(np.eye(4)),
            },
            "Gamma6": {
                "probe_block_index": 2,
                "bands_one_based": [37, 38],
                "intertwiner": _serialized(np.eye(2)),
            },
        },
    }


def _contract() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    return json.loads(
        (root / "first_principles/a0/cdte_finite_k_kane_smoke.json").read_text(
            encoding="utf-8"
        )
    )


def _k_points(contract: dict[str, object]) -> np.ndarray:
    points = [np.zeros(3)]
    for name in ("001", "111", "110"):
        spec = contract["pairs"][name]
        direction = np.asarray(spec["unit_direction"], dtype=float)
        h = float(spec["radius_inverse_angstrom"])
        points.extend(
            (
                h * direction,
                -h * direction,
                0.5 * h * direction,
                -0.5 * h * direction,
            )
        )
    return np.asarray(points)


def _write_nnkp(path: Path, points: np.ndarray) -> None:
    lines = [
        "begin recip_lattice",
        "1 0 0",
        "0 1 0",
        "0 0 1",
        "end recip_lattice",
        "begin kpoints",
        str(len(points)),
    ]
    lines.extend(
        " ".join(f"{value:.17g}" for value in point) for point in points
    )
    lines.append("end kpoints")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_mmn(path: Path, matrices: list[np.ndarray]) -> None:
    lines = ["synthetic Gamma star", f"40 {len(matrices)} 1"]
    for source, matrix in enumerate(matrices, start=1):
        lines.append(f"{source} 1 0 0 0")
        for n in range(40):
            for m in range(40):
                value = matrix[m, n]
                lines.append(f"{value.real:.17e} {value.imag:.17e}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _synthetic_files(
    tmp_path: Path,
) -> tuple[dict[str, Path], ExtendedKaneParameters]:
    contract = _contract()
    basis = _basis_result()
    points = _k_points(contract)
    canonical = projection._canonical_columns(basis)
    parameters = ExtendedKaneParameters(
        ev=0.17,
        eg=0.82,
        delta=0.91,
        p8=7.2,
        p7=6.4,
        f=-0.08,
        gamma1=1.48,
        gamma2=-0.27,
        gamma3=0.11,
    )
    lower = np.linspace(-30.0, -2.0, 30)
    upper = np.asarray([8.0, 10.0])
    mmn = []
    blocks = []
    for index, point in enumerate(points, start=1):
        target = hamiltonian_two_p(point, parameters)
        fixed = canonical @ target @ canonical.conj().T
        selected, eigenvectors = np.linalg.eigh(fixed)
        energies = np.concatenate((lower, selected, upper))
        transform = np.eye(40, dtype=complex)
        transform[30:38, 30:38] = eigenvectors
        mmn.append(transform.conj().T)
        blocks.append(
            {
                "index": index,
                "eigenvalues_ev": energies.tolist(),
                "eigenvalues_hartree": (
                    energies / 27.211386245988
                ).tolist(),
                "occupations": [0.0] * 40,
                "k_point_crystal": point.tolist(),
                "weight": 1.0,
            }
        )

    paths = {
        "mmn": tmp_path / "synthetic.mmn",
        "nnkp": tmp_path / "synthetic.nnkp",
        "eigenvalues": tmp_path / "eigenvalues.json",
        "basis": tmp_path / "basis.json",
        "contract": tmp_path / "contract.json",
    }
    _write_mmn(paths["mmn"], mmn)
    _write_nnkp(paths["nnkp"], points)
    paths["eigenvalues"].write_text(
        json.dumps({"num_kpoints": 13, "num_bands": 40, "blocks": blocks}),
        encoding="utf-8",
    )
    paths["basis"].write_text(json.dumps(basis), encoding="utf-8")
    paths["contract"].write_text(json.dumps(contract), encoding="utf-8")
    return paths, parameters


def test_exact_two_p_smoke_recovers_parameters_and_holdout(
    tmp_path: Path,
) -> None:
    paths, expected = _synthetic_files(tmp_path)
    result = finite.analyze(
        paths["mmn"],
        paths["nnkp"],
        paths["eigenvalues"],
        paths["basis"],
        paths["contract"],
    )

    assert result["minimum_overlap_singular_value"] > 1.0 - 1.0e-12
    assert result["maximum_time_reversal_pair_residual_ev"] < 1.0e-11
    assert result["sign_convention"]["selected"]["gamma8_sign"] == 1
    assert result["sign_convention"]["selected"]["gamma7_sign"] == 1
    assert result["closure_decision"]["passed_declared_static_smoke_thresholds"]
    assert result["two_p"]["diagnostics"]["linear"]["relative_residual"] < 1.0e-10
    assert result["two_p"]["diagnostics"]["quadratic"]["relative_residual"] < 1.0e-8
    assert result["one_p"]["diagnostics"]["linear"]["relative_residual"] > 1.0e-3

    recovered = result["two_p"]["parameters"]
    for name in (
        "ev",
        "eg",
        "delta",
        "p8",
        "p7",
        "f",
        "gamma1",
        "gamma2",
        "gamma3",
    ):
        assert recovered[name] == pytest.approx(getattr(expected, name), abs=2.0e-7)


def test_projection_retains_remote_band_contribution(tmp_path: Path) -> None:
    basis = _basis_result()
    theta = 0.2
    transform = np.eye(40, dtype=complex)
    transform[30, 30] = math.cos(theta)
    transform[30, 39] = math.sin(theta)
    transform[39, 30] = -math.sin(theta)
    transform[39, 39] = math.cos(theta)
    mmn_path = tmp_path / "remote.mmn"
    _write_mmn(mmn_path, [transform.conj().T for _ in range(13)])

    energies = np.linspace(-10.0, 10.0, 40)
    payload = {
        "num_kpoints": 13,
        "num_bands": 40,
        "blocks": [
            {"index": index, "eigenvalues_ev": energies.tolist()}
            for index in range(1, 14)
        ],
    }
    matrices, diagnostics = projection.reconstruct_canonical_matrices(
        mmn_path, payload, basis
    )
    expected = (
        math.cos(theta) ** 2 * energies[30]
        + math.sin(theta) ** 2 * energies[39]
    )

    # Probe row 30 is the first Gamma7 state, reordered to canonical index 6.
    assert matrices[0][6, 6].real == pytest.approx(expected, abs=1.0e-12)
    assert diagnostics[0]["finite_state_count_used"] == 40
    assert abs(expected - energies[30]) > 0.1


def test_kpoint_contract_fails_on_wrong_direction() -> None:
    contract = _contract()
    points = _k_points(contract)
    points[9] += np.asarray([1.0e-3, 0.0, 0.0])
    with pytest.raises(ValueError, match="k point does not match"):
        projection._validate_kpoint_contract(points, contract)
