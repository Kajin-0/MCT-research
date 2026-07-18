"""Fixed-reference reconstruction and Taylor-coefficient helpers for the CdTe Kane smoke."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
from typing import Any, Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from analyze_fixed_basis_kane_projection import reconstruct_fixed_basis  # noqa: E402
from check_wannier90_gamma_star_mmn import read_mmn  # noqa: E402
from mct_research.kane8 import (  # noqa: E402
    ExtendedKaneParameters,
    KaneParameters,
    hamiltonian,
    hamiltonian_two_p,
)

LABEL_ORDER = ("Gamma6", "Gamma8", "Gamma7")
SELECTED_BAND_POLAR = "selected_band_polar"
ALL_STATE_BARE_PROJECTION = "all_state_bare_projection"
RECONSTRUCTION_MODES = (SELECTED_BAND_POLAR, ALL_STATE_BARE_PROJECTION)
SELECTED_BAND_SLICE = slice(30, 38)
SELECTED_BANDS_ONE_BASED = list(range(31, 39))
PARAMETER_GROUPS = {
    "zone_center": ("ev", "eg", "delta"),
    "linear_one_p": ("p",),
    "linear_two_p": ("p8", "p7"),
    "quadratic": ("f", "gamma1", "gamma2", "gamma3"),
}


def _complex(payload: Any) -> np.ndarray:
    array = np.asarray(payload, dtype=float)
    return array[..., 0] + 1j * array[..., 1]


def _real_vector(matrix: np.ndarray) -> np.ndarray:
    flat = np.asarray(matrix, dtype=complex).reshape(-1)
    return np.concatenate((flat.real, flat.imag))


def _read_nnkp(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    def section(start: str, end: str) -> list[str]:
        first = lines.index(start) + 1
        last = lines.index(end)
        return lines[first:last]

    reciprocal = np.asarray(
        [
            [float(value) for value in line.split()]
            for line in section("begin recip_lattice", "end recip_lattice")
        ],
        dtype=float,
    )
    k_lines = section("begin kpoints", "end kpoints")
    count = int(k_lines[0])
    reduced = np.asarray(
        [[float(value) for value in line.split()] for line in k_lines[1:]],
        dtype=float,
    )
    if reciprocal.shape != (3, 3) or reduced.shape != (count, 3):
        raise ValueError("invalid Wannier90 reciprocal lattice or k-point section")
    return reduced, reduced @ reciprocal


def _validate_kpoint_contract(
    cartesian: np.ndarray, contract: dict[str, Any]
) -> dict[str, float]:
    if cartesian.shape != (13, 3):
        raise ValueError("expected 13 Cartesian k points")
    if np.linalg.norm(cartesian[0]) > 1.0e-10:
        raise ValueError("first k point must be Gamma")
    maximum = 0.0
    for name, spec in contract["pairs"].items():
        direction = np.asarray(spec["unit_direction"], dtype=float)
        direction /= np.linalg.norm(direction)
        h = float(spec["radius_inverse_angstrom"])
        expected = {
            "plus_h": h * direction,
            "minus_h": -h * direction,
            "plus_h_over_2": 0.5 * h * direction,
            "minus_h_over_2": -0.5 * h * direction,
        }
        for key, target in expected.items():
            index = int(spec[key]) - 1
            residual = float(np.linalg.norm(cartesian[index] - target))
            maximum = max(maximum, residual)
            if residual > 1.0e-7:
                raise ValueError(f"{name} {key} k point does not match the contract")
    return {"maximum_cartesian_kpoint_residual_inverse_angstrom": maximum}


def _canonical_columns(result: dict[str, Any]) -> np.ndarray:
    selected = result["selected_global_bands_one_based"]
    if selected != SELECTED_BANDS_ONE_BASED:
        raise ValueError("expected contiguous selected bands 31--38")
    by_probe = sorted(
        result["irreps"].items(), key=lambda item: item[1]["probe_block_index"]
    )
    sizes = [len(item[1]["bands_one_based"]) for item in by_probe]
    if sizes != [2, 4, 2]:
        raise ValueError("expected Gamma7/Gamma8/Gamma6 probe dimensions 2/4/2")
    block = np.zeros((8, 8), dtype=complex)
    offset = 0
    target_offsets: dict[str, tuple[int, int]] = {}
    for label, record in by_probe:
        unitary = _complex(record["intertwiner"])
        dimension = unitary.shape[0]
        block[offset : offset + dimension, offset : offset + dimension] = unitary
        target_offsets[label] = (offset, offset + dimension)
        offset += dimension
    columns = []
    for label in LABEL_ORDER:
        start, stop = target_offsets[label]
        columns.extend(range(start, stop))
    canonical = block[:, columns]
    if np.linalg.norm(canonical.conj().T @ canonical - np.eye(8)) > 1.0e-10:
        raise ValueError("committed canonical intertwiners are not unitary")
    return canonical


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _all_eigenvalues(
    payload: dict[str, Any], expected_bands: int = 40
) -> list[np.ndarray]:
    if int(payload.get("num_kpoints", -1)) != 13:
        raise ValueError("expected 13 exact QE eigenvalue blocks")
    if int(payload.get("num_bands", -1)) != expected_bands:
        raise ValueError(f"expected {expected_bands} exact QE bands per k point")
    blocks = payload["blocks"]
    if len(blocks) != 13:
        raise ValueError("QE eigenvalue block count is inconsistent")
    values_by_k = []
    for expected_index, block in enumerate(blocks, start=1):
        if int(block.get("index", -1)) != expected_index:
            raise ValueError("QE eigenvalue blocks are not in exact k-point order")
        values = np.asarray(block["eigenvalues_ev"], dtype=float)
        if values.shape != (expected_bands,) or not np.all(np.isfinite(values)):
            raise ValueError("invalid exact QE eigenvalue block")
        values_by_k.append(values)
    return values_by_k


def _reconstruction_payload(
    full_overlap: np.ndarray,
    all_energies: np.ndarray,
    mode: str,
) -> tuple[np.ndarray, np.ndarray, int, str]:
    if mode == SELECTED_BAND_POLAR:
        overlap = full_overlap[:, SELECTED_BAND_SLICE]
        energies = all_energies[SELECTED_BAND_SLICE]
        interpretation = (
            "isospectral selected-band polar transport in the fixed Gamma basis; "
            "remote-band physics is retained through the selected eigenpairs"
        )
        return overlap, energies, 8, interpretation
    if mode == ALL_STATE_BARE_PROJECTION:
        interpretation = (
            "diagnostic-only finite-state approximation to P_Gamma H(k) P_Gamma; "
            "this is not an isospectral low-energy effective Hamiltonian"
        )
        return full_overlap, all_energies, int(all_energies.size), interpretation
    raise ValueError(
        f"unknown reconstruction mode {mode!r}; expected one of {RECONSTRUCTION_MODES}"
    )


def reconstruct_canonical_matrices(
    mmn_path: str | Path,
    eigenvalue_payload: dict[str, Any],
    basis_result: dict[str, Any],
    *,
    mode: str = SELECTED_BAND_POLAR,
) -> tuple[list[np.ndarray], list[dict[str, Any]]]:
    """Reconstruct finite-k matrices in the exact canonical Gamma basis.

    ``selected_band_polar`` is the scientific mode. It polar-aligns only bands
    31--38 and is exactly isospectral to those selected DFT eigenvalues.

    ``all_state_bare_projection`` is retained solely as a diagnostic. In the
    complete-state limit it approaches ``P_Gamma H(k) P_Gamma`` and therefore
    must not be interpreted as a downfolded eight-band Hamiltonian.
    """
    nbnd, nk, nntot, blocks = read_mmn(mmn_path)
    if (nbnd, nk, nntot) != (40, 13, 1):
        raise ValueError("expected the committed 40-band, 13-point Gamma star")
    if len(blocks) != 13:
        raise ValueError("expected 13 Gamma-star overlap blocks")
    by_source: dict[int, np.ndarray] = {}
    for source, target, image, matrix in blocks:
        if source in by_source:
            raise ValueError("duplicate Gamma-star overlap source index")
        if target != 1 or image != (0, 0, 0):
            raise ValueError("every finite-k source must link directly to Gamma")
        by_source[source] = matrix
    if set(by_source) != set(range(1, 14)):
        raise ValueError("Gamma-star overlap sources must be exactly 1 through 13")

    energies = _all_eigenvalues(eigenvalue_payload, expected_bands=nbnd)
    canonical = _canonical_columns(basis_result)
    matrices = []
    diagnostics: list[dict[str, Any]] = []
    for source in range(1, 14):
        # Wannier90 stores M(source,Gamma). The fixed-reference overlap is
        # S=M^dagger restricted to the eight Gamma reference rows.
        full_overlap = by_source[source].conj().T[SELECTED_BAND_SLICE, :]
        overlap, target_energies, state_count, interpretation = _reconstruction_payload(
            full_overlap, energies[source - 1], mode
        )
        fixed, singular_values = reconstruct_fixed_basis(
            overlap, np.diag(target_energies)
        )
        matrix = canonical.conj().T @ fixed @ canonical
        matrix = 0.5 * (matrix + matrix.conj().T)
        matrices.append(matrix)
        selected = np.sort(energies[source - 1][SELECTED_BAND_SLICE])
        reconstructed = np.linalg.eigvalsh(matrix)
        difference = reconstructed - selected
        diagnostics.append(
            {
                "reconstruction_mode": mode,
                "reconstruction_interpretation": interpretation,
                "minimum_overlap_singular_value": float(np.min(singular_values)),
                "maximum_overlap_singular_value": float(np.max(singular_values)),
                "hermiticity_residual": float(
                    np.linalg.norm(matrix - matrix.conj().T)
                ),
                "projected_vs_selected_eigenvalue_residual_ev": float(
                    np.linalg.norm(difference)
                ),
                "maximum_selected_eigenvalue_absolute_error_ev": float(
                    np.max(np.abs(difference))
                ),
                "finite_state_count_used": state_count,
                "available_state_count": int(nbnd),
                "selected_bands_one_based": SELECTED_BANDS_ONE_BASED,
            }
        )
    return matrices, diagnostics


def _apply_signs(
    matrices: list[np.ndarray], gamma8: int, gamma7: int
) -> list[np.ndarray]:
    signs = np.asarray([1, 1] + [gamma8] * 4 + [gamma7] * 2, dtype=float)
    transform = np.diag(signs)
    return [transform @ matrix @ transform for matrix in matrices]


def _richardson(coarse: np.ndarray, fine: np.ndarray) -> np.ndarray:
    return (4.0 * fine - coarse) / 3.0


def extract_coefficients(
    matrices: list[np.ndarray], pairs: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    gamma = matrices[0]
    result: dict[str, dict[str, Any]] = {}
    for name, spec in pairs.items():
        plus_h, minus_h, plus_fine, minus_fine = [
            int(spec[key]) - 1
            for key in (
                "plus_h",
                "minus_h",
                "plus_h_over_2",
                "minus_h_over_2",
            )
        ]
        h = float(spec["radius_inverse_angstrom"])
        linear_h = (matrices[plus_h] - matrices[minus_h]) / (2.0 * h)
        linear_fine = (matrices[plus_fine] - matrices[minus_fine]) / h
        quadratic_h = (
            matrices[plus_h] + matrices[minus_h] - 2.0 * gamma
        ) / (2.0 * h**2)
        quadratic_fine = (
            matrices[plus_fine] + matrices[minus_fine] - 2.0 * gamma
        ) / (2.0 * (h / 2.0) ** 2)
        linear = _richardson(linear_h, linear_fine)
        quadratic = _richardson(quadratic_h, quadratic_fine)
        result[name] = {
            "direction": np.asarray(spec["unit_direction"], dtype=float),
            "linear": 0.5 * (linear + linear.conj().T),
            "quadratic": 0.5 * (quadratic + quadratic.conj().T),
            "linear_coarse_fine_change": float(
                np.linalg.norm(linear_h - linear_fine)
            ),
            "quadratic_coarse_fine_change": float(
                np.linalg.norm(quadratic_h - quadratic_fine)
            ),
            "linear_richardson_correction": float(
                np.linalg.norm(linear - linear_fine)
            ),
            "quadratic_richardson_correction": float(
                np.linalg.norm(quadratic - quadratic_fine)
            ),
        }
    return result


def _coefficient_templates(
    direction: np.ndarray,
    parameter_type: type[KaneParameters] | type[ExtendedKaneParameters],
    model: Callable,
    names: tuple[str, ...],
) -> tuple[
    dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]],
    tuple[np.ndarray, np.ndarray, np.ndarray],
]:
    direction = np.asarray(direction, dtype=float)
    zero = parameter_type()
    base_plus = model(direction, zero)
    base_minus = model(-direction, zero)
    base_gamma = model(np.zeros(3), zero)
    base = (
        base_gamma,
        0.5 * (base_plus - base_minus),
        0.5 * (base_plus + base_minus - 2.0 * base_gamma),
    )
    templates = {}
    all_names = tuple(zero.__dataclass_fields__)
    for name in names:
        values = {item: 0.0 for item in all_names}
        values[name] = 1.0
        params = parameter_type(**values)
        plus = model(direction, params)
        minus = model(-direction, params)
        gamma = model(np.zeros(3), params)
        templates[name] = (
            gamma - base_gamma,
            0.5 * (plus - minus) - base[1],
            0.5 * (plus + minus - 2.0 * gamma) - base[2],
        )
    return templates, base


def _fit_group(
    observations: list[np.ndarray],
    templates: list[dict[str, np.ndarray]],
    base: list[np.ndarray],
    names: tuple[str, ...],
) -> tuple[dict[str, float], dict[str, Any]]:
    rows = []
    target = []
    for observed, item, offset in zip(observations, templates, base, strict=True):
        rows.append(np.column_stack([_real_vector(item[name]) for name in names]))
        target.append(_real_vector(observed - offset))
    design = np.vstack(rows)
    vector = np.concatenate(target)
    solution, _, rank, singular_values = np.linalg.lstsq(design, vector, rcond=None)
    predicted = design @ solution
    residual = vector - predicted
    if rank != len(names):
        raise RuntimeError(f"rank-deficient coefficient fit for {names}: {rank}")
    return dict(zip(names, solution.tolist(), strict=True)), {
        "rank": int(rank),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "absolute_residual": float(np.linalg.norm(residual)),
        "relative_residual": float(
            np.linalg.norm(residual)
            / max(np.linalg.norm(vector), np.finfo(float).eps)
        ),
        "singular_values": singular_values.tolist(),
    }
