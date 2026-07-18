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
    json.dumps(result, sort_keys=True)

    assert result["reconstruction_mode"] == projection.SELECTED_BAND_POLAR
    assert result["maximum_selected_eigenvalue_absolute_error_ev"] < 1.0e-12
    assert result["minimum_overlap_singular_value"] > 1.0 - 1.0e-12
    assert result["maximum_time_reversal_pair_residual_ev"] < 1.0e-11
    assert result["sign_convention"]["selected"]["gamma8_sign"] == 1
    assert result["sign_convention"]["selected"]["gamma7_sign"] == 1
    assert result["closure_decision"]["passed_declared_static_smoke_thresholds"]
    assert result["closure_decision"]["linear_two_p"]["passed"]
    assert result["closure_decision"]["quadratic_conventional_kane"]["passed"]
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


def test_selected_band_polar_isospectral_while_all_state_returns_bare_projection(
    tmp_path: Path,
) -> None:
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
    selected, selected_diagnostics = projection.reconstruct_canonical_matrices(
        mmn_path,
        payload,
        basis,
        mode=projection.SELECTED_BAND_POLAR,
    )
    bare, bare_diagnostics = projection.reconstruct_canonical_matrices(
        mmn_path,
        payload,
        basis,
        mode=projection.ALL_STATE_BARE_PROJECTION,
    )
    expected_bare = (
        math.cos(theta) ** 2 * energies[30]
        + math.sin(theta) ** 2 * energies[39]
    )

    # Probe row 30 is the first Gamma7 state, reordered to canonical index 6.
    assert selected[0][6, 6].real == pytest.approx(energies[30], abs=1.0e-12)
    assert bare[0][6, 6].real == pytest.approx(expected_bare, abs=1.0e-12)
    assert selected_diagnostics[0]["finite_state_count_used"] == 8
    assert bare_diagnostics[0]["finite_state_count_used"] == 40
    assert selected_diagnostics[0]["maximum_selected_eigenvalue_absolute_error_ev"] < 1.0e-12
    assert bare_diagnostics[0]["maximum_selected_eigenvalue_absolute_error_ev"] > 0.1


def test_coupled_two_level_model_falsifies_all_state_effective_interpretation() -> None:
    delta = 2.0
    velocity = 1.3
    k = 0.08
    exact = np.asarray([[0.0, velocity * k], [velocity * k, delta]])
    energies, eigenvectors = np.linalg.eigh(exact)
    full_overlap = eigenvectors[0:1, :]
    selected_overlap = full_overlap[:, :1]

    selected, _ = projection.reconstruct_fixed_basis(
        selected_overlap, np.diag(energies[:1])
    )
    bare, _ = projection.reconstruct_fixed_basis(
        full_overlap, np.diag(energies)
    )

    assert selected[0, 0].real == pytest.approx(energies[0], abs=1.0e-14)
    assert bare[0, 0].real == pytest.approx(exact[0, 0], abs=1.0e-14)
    assert energies[0] == pytest.approx(
        -(velocity * velocity / delta) * k * k,
        rel=0.02,
    )
    assert abs(selected[0, 0] - bare[0, 0]) > 1.0e-3


def test_selected_polar_is_invariant_to_admissible_source_gauge() -> None:
    rng = np.random.default_rng(20260718)
    raw = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8))
    overlap = np.linalg.qr(raw)[0]
    energies = np.asarray([-2.0, -2.0, -0.7, -0.7, 0.2, 0.9, 1.4, 2.3])
    reference, _ = projection.reconstruct_fixed_basis(overlap, np.diag(energies))

    rotation = np.eye(8, dtype=complex)
    angle = 0.43
    rotation[:2, :2] = np.asarray(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    phases = np.diag(np.exp(1j * np.linspace(0.1, 1.7, 8)))
    gauge = rotation @ phases
    transformed, _ = projection.reconstruct_fixed_basis(
        overlap @ gauge,
        gauge.conj().T @ np.diag(energies) @ gauge,
    )
    np.testing.assert_allclose(transformed, reference, atol=1.0e-12)


def test_kpoint_contract_fails_on_wrong_direction() -> None:
    contract = _contract()
    points = _k_points(contract)
    points[9] += np.asarray([1.0e-3, 0.0, 0.0])
    with pytest.raises(ValueError, match="k point does not match"):
        projection._validate_kpoint_contract(points, contract)
