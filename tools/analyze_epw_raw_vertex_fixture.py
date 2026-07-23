#!/usr/bin/env python3
"""Analyze a bounded EPW raw complex-vertex normalization fixture."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping

import numpy as np

from tools.matrix_fan import (
    fan_matrix,
    rotate_external_contributions,
    scalar_diagonal_reference,
)


class RawVertexError(ValueError):
    """Raised when raw EPW evidence violates the fixture contract."""


@dataclass(frozen=True)
class RawRow:
    iqq: int
    iq: int
    ik: int
    ik_global: int
    imode: int
    ibnd: int
    jbnd: int
    itemp: int
    epf: complex
    ekk_ry: float
    ekq_ry: float
    wq_ry: float
    inv_wq_ry_inverse: float
    mask: float
    q_weight: float
    f_occ: float
    bose: float
    eta_ry: float
    fact1: float
    fact2: float
    etmp1_ry: float
    etmp2_ry: float
    g2_ry2: float
    real_increment_ry: float
    imag_increment_ry: float
    ryd2ev: float


_FLOAT_PATTERN = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][-+]?\d+)?"
_COMPACT_SELF_ENERGY = re.compile(
    rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT_PATTERN})\s+({_FLOAT_PATTERN})\s+"
    rf"({_FLOAT_PATTERN})\s+({_FLOAT_PATTERN})\s+({_FLOAT_PATTERN})\s*$"
)


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RawVertexError(f"expected JSON object in {path}")
    return value


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _as_float(value: str) -> float:
    return float(value.replace("D", "E").replace("d", "e"))


def parse_raw_rows(path: str | Path) -> list[RawRow]:
    rows: list[RawRow] = []
    for line_number, line in enumerate(
        Path(path).read_text(encoding="utf-8", errors="strict").splitlines(), 1
    ):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        fields = stripped.split()
        if len(fields) != 27:
            raise RawVertexError(
                f"raw row {line_number} has {len(fields)} fields, expected 27"
            )
        integers = [int(value) for value in fields[:8]]
        values = [_as_float(value) for value in fields[8:]]
        if not np.all(np.isfinite(values)):
            raise RawVertexError(f"raw row {line_number} contains non-finite values")
        rows.append(
            RawRow(
                *integers,
                epf=complex(values[0], values[1]),
                ekk_ry=values[2],
                ekq_ry=values[3],
                wq_ry=values[4],
                inv_wq_ry_inverse=values[5],
                mask=values[6],
                q_weight=values[7],
                f_occ=values[8],
                bose=values[9],
                eta_ry=values[10],
                fact1=values[11],
                fact2=values[12],
                etmp1_ry=values[13],
                etmp2_ry=values[14],
                g2_ry2=values[15],
                real_increment_ry=values[16],
                imag_increment_ry=values[17],
                ryd2ev=values[18],
            )
        )
    if not rows:
        raise RawVertexError("raw-vertex file contains no data rows")
    return rows


def parse_compact_self_energy_table(path: str | Path) -> list[dict[str, float | int]]:
    records: list[dict[str, float | int]] = []
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        match = _COMPACT_SELF_ENERGY.match(line)
        if match is None:
            continue
        records.append(
            {
                "ik": int(match.group(1)),
                "ibnd": int(match.group(2)),
                "energy_ev": _as_float(match.group(3)),
                "real_sigma_mev": _as_float(match.group(4)),
                "imag_sigma_mev": _as_float(match.group(5)),
                "z": _as_float(match.group(6)),
                "lambda": _as_float(match.group(7)),
            }
        )
    if not records:
        raise RawVertexError(f"no compact EPW self-energy table found in {path}")
    return records


def compare_standard_outputs(
    disabled_path: str | Path, enabled_path: str | Path
) -> dict[str, Any]:
    disabled = parse_compact_self_energy_table(disabled_path)
    enabled = parse_compact_self_energy_table(enabled_path)
    if len(disabled) != len(enabled):
        raise RawVertexError("enabled/disabled compact self-energy table lengths differ")
    maximum_energy_ev = 0.0
    maximum_self_energy_ev = 0.0
    maximum_dimensionless = 0.0
    for index, (left, right) in enumerate(zip(disabled, enabled, strict=True)):
        if (left["ik"], left["ibnd"]) != (right["ik"], right["ibnd"]):
            raise RawVertexError(f"enabled/disabled table index mismatch at row {index}")
        maximum_energy_ev = max(
            maximum_energy_ev,
            abs(float(left["energy_ev"]) - float(right["energy_ev"])),
        )
        maximum_self_energy_ev = max(
            maximum_self_energy_ev,
            abs(float(left["real_sigma_mev"]) - float(right["real_sigma_mev"]))
            * 1.0e-3,
            abs(float(left["imag_sigma_mev"]) - float(right["imag_sigma_mev"]))
            * 1.0e-3,
        )
        maximum_dimensionless = max(
            maximum_dimensionless,
            abs(float(left["z"]) - float(right["z"])),
            abs(float(left["lambda"]) - float(right["lambda"])),
        )
    return {
        "row_count": len(disabled),
        "maximum_energy_difference_ev": maximum_energy_ev,
        "maximum_self_energy_difference_ev": maximum_self_energy_ev,
        "maximum_dimensionless_difference": maximum_dimensionless,
    }


def _maximum(values: Iterable[float]) -> float:
    collected = list(values)
    return max(collected) if collected else 0.0


def _validate_row_identities(rows: list[RawRow]) -> dict[str, Any]:
    ryd2ev_values = {row.ryd2ev for row in rows}
    if len(ryd2ev_values) != 1:
        raise RawVertexError("ryd2ev differs across exported rows")
    ryd2ev = next(iter(ryd2ev_values))
    if ryd2ev <= 0.0:
        raise RawVertexError("ryd2ev must be positive")

    normalization_residuals: list[float] = []
    numerator_residuals: list[float] = []
    denominator_residuals: list[float] = []
    row_real_residuals_ev: list[float] = []
    sign_failures = 0
    for row in rows:
        expected_g2 = abs(row.epf) ** 2 * row.inv_wq_ry_inverse * row.mask
        normalization_residuals.append(abs(row.g2_ry2 - expected_g2))
        numerator_residuals.extend(
            [
                abs(row.fact1 - (row.f_occ + row.bose)),
                abs(row.fact2 - (1.0 - row.f_occ + row.bose)),
            ]
        )
        denominator_residuals.extend(
            [
                abs(row.etmp1_ry - (row.ekk_ry - row.ekq_ry + row.wq_ry)),
                abs(row.etmp2_ry - (row.ekk_ry - row.ekq_ry - row.wq_ry)),
            ]
        )
        normalized_vertex_ev = (
            row.epf
            * np.sqrt(max(0.0, row.inv_wq_ry_inverse * row.mask))
            * ryd2ev
        )
        contribution = {
            "vertex_ev": np.asarray([[normalized_vertex_ev]], dtype=complex),
            "intermediate_energies_ev": [row.ekq_ry * ryd2ev],
            "occupations": [row.f_occ],
            "phonon_energy_ev": row.wq_ry * ryd2ev,
            "bose_occupation": row.bose,
            "q_weight": row.q_weight,
        }
        reconstructed = scalar_diagonal_reference(
            [contribution], 0, row.ekk_ry * ryd2ev, row.eta_ry * ryd2ev
        )
        backend_ev = row.real_increment_ry * ryd2ev
        row_real_residuals_ev.append(abs(reconstructed.real - backend_ev))
        if reconstructed.imag > 1.0e-14 or row.imag_increment_ry < -1.0e-16:
            sign_failures += 1

    mask_values = {row.mask for row in rows}
    zero_mask_rows = [row for row in rows if row.mask == 0.0]
    active_rows = [row for row in rows if row.mask > 0.0]
    if not zero_mask_rows or not active_rows:
        raise RawVertexError("export must contain both masked and active phonon rows")
    zero_mask_residual = _maximum(
        max(abs(row.g2_ry2), abs(row.real_increment_ry), abs(row.imag_increment_ry))
        for row in zero_mask_rows
    )
    return {
        "ryd2ev": ryd2ev,
        "normalization_identity_max_abs_ry2": _maximum(normalization_residuals),
        "occupation_numerator_max_abs": _maximum(numerator_residuals),
        "denominator_identity_max_abs_ry": _maximum(denominator_residuals),
        "per_row_real_diagonal_max_abs_ev": _maximum(row_real_residuals_ev),
        "imaginary_sign_failure_count": sign_failures,
        "mask_values": sorted(mask_values),
        "zero_mask_row_count": len(zero_mask_rows),
        "active_row_count": len(active_rows),
        "zero_mask_max_abs_ry2_or_ry": zero_mask_residual,
    }


def _build_matrix_contributions(rows: list[RawRow]) -> tuple[list[dict[str, Any]], list[float]]:
    external_bands = sorted({row.ibnd for row in rows})
    intermediate_bands = sorted({row.jbnd for row in rows})
    if external_bands != list(range(1, len(external_bands) + 1)):
        raise RawVertexError("external band indices are not contiguous from one")
    if intermediate_bands != list(range(1, len(intermediate_bands) + 1)):
        raise RawVertexError("intermediate band indices are not contiguous from one")
    external_dimension = len(external_bands)
    intermediate_dimension = len(intermediate_bands)

    groups: dict[tuple[int, int, int, int], list[RawRow]] = {}
    for row in rows:
        groups.setdefault((row.iqq, row.iq, row.imode, row.itemp), []).append(row)

    contributions: list[dict[str, Any]] = []
    external_energies_ev: np.ndarray | None = None
    for key in sorted(groups):
        group = groups[key]
        expected_count = external_dimension * intermediate_dimension
        if len(group) != expected_count:
            raise RawVertexError(
                f"incomplete complex vertex block {key}: {len(group)} != {expected_count}"
            )
        ryd2ev = group[0].ryd2ev
        vertex = np.empty((intermediate_dimension, external_dimension), dtype=complex)
        intermediate_energies = np.empty(intermediate_dimension, dtype=float)
        occupations = np.empty(intermediate_dimension, dtype=float)
        group_external = np.empty(external_dimension, dtype=float)
        q_weight = group[0].q_weight
        wq = group[0].wq_ry
        bose = group[0].bose
        mask = group[0].mask
        for row in group:
            if (
                row.ryd2ev != ryd2ev
                or row.q_weight != q_weight
                or row.wq_ry != wq
                or row.bose != bose
                or row.mask != mask
            ):
                raise RawVertexError(f"inconsistent scalar metadata inside block {key}")
            vertex[row.jbnd - 1, row.ibnd - 1] = (
                row.epf
                * np.sqrt(max(0.0, row.inv_wq_ry_inverse * row.mask))
                * ryd2ev
            )
            intermediate_energies[row.jbnd - 1] = row.ekq_ry * ryd2ev
            occupations[row.jbnd - 1] = row.f_occ
            group_external[row.ibnd - 1] = row.ekk_ry * ryd2ev
        if external_energies_ev is None:
            external_energies_ev = group_external
        elif not np.allclose(external_energies_ev, group_external, rtol=0.0, atol=1.0e-13):
            raise RawVertexError("external energies differ across q/mode blocks")
        contributions.append(
            {
                "vertex_ev": vertex,
                "intermediate_energies_ev": intermediate_energies,
                "occupations": occupations,
                "phonon_energy_ev": wq * ryd2ev,
                "bose_occupation": bose,
                "q_weight": q_weight,
            }
        )
    assert external_energies_ev is not None
    return contributions, external_energies_ev.tolist()


def _summed_diagonal_and_covariance(rows: list[RawRow]) -> dict[str, Any]:
    contributions, external_energies_ev = _build_matrix_contributions(rows)
    external_dimension = len(external_energies_ev)
    backend_sums = np.zeros(external_dimension, dtype=float)
    for row in rows:
        backend_sums[row.ibnd - 1] += row.real_increment_ry * row.ryd2ev
    reconstructed = np.asarray(
        [
            scalar_diagonal_reference(
                contributions,
                external_index,
                external_energies_ev[external_index],
                rows[0].eta_ry * rows[0].ryd2ev,
            ).real
            for external_index in range(external_dimension)
        ]
    )
    summed_residual = float(np.max(np.abs(reconstructed - backend_sums)))

    rng = np.random.default_rng(300)
    trial = rng.normal(size=(external_dimension, external_dimension)) + 1j * rng.normal(
        size=(external_dimension, external_dimension)
    )
    unitary, _ = np.linalg.qr(trial)
    common_energy = float(np.mean(external_energies_ev))
    eta_ev = rows[0].eta_ry * rows[0].ryd2ev
    reference = fan_matrix(contributions, common_energy, eta_ev)
    rotated = fan_matrix(
        rotate_external_contributions(contributions, unitary), common_energy, eta_ev
    )
    covariance_residual = float(
        np.max(np.abs(rotated - unitary.conj().T @ reference @ unitary))
    )
    return {
        "external_dimension": external_dimension,
        "contribution_count": len(contributions),
        "external_energies_ev": external_energies_ev,
        "backend_selected_window_real_diagonal_ev": backend_sums.tolist(),
        "reconstructed_selected_window_real_diagonal_ev": reconstructed.tolist(),
        "summed_real_diagonal_max_abs_ev": summed_residual,
        "synthetic_external_covariance_max_abs_ev": covariance_residual,
    }


def _q_coverage(rows: list[RawRow]) -> dict[str, Any]:
    q_weights: dict[tuple[int, int, int], float] = {}
    for row in rows:
        key = (row.iqq, row.iq, row.itemp)
        if key in q_weights and q_weights[key] != row.q_weight:
            raise RawVertexError(f"q weight differs inside q-point group {key}")
        q_weights[key] = row.q_weight
    itemps = sorted({key[2] for key in q_weights})
    sums = {
        str(itemp): sum(weight for key, weight in q_weights.items() if key[2] == itemp)
        for itemp in itemps
    }
    return {
        "unique_q_temperature_count": len(q_weights),
        "temperature_indices": itemps,
        "q_weight_sums": sums,
        "q_weight_sum_max_abs_from_one": _maximum(abs(value - 1.0) for value in sums.values()),
        "iqq_indices": sorted({row.iqq for row in rows}),
        "iq_indices": sorted({row.iq for row in rows}),
    }


def analyze(
    raw_path: str | Path,
    disabled_stdout_path: str | Path,
    enabled_stdout_path: str | Path,
    contract_path: str | Path,
) -> dict[str, Any]:
    contract = _load_json(contract_path)
    if contract.get("stage") != "B0_epw_raw_vertex_fixture":
        raise RawVertexError("unexpected raw-vertex contract stage")
    if contract.get("phase") != "fixture_execution":
        raise RawVertexError("fixture analyzer requires the committed fixture_execution phase")
    rows = parse_raw_rows(raw_path)
    selected_ik = int(contract["fixture"]["selected_export_window"]["ik_global"])
    if {row.ik_global for row in rows} != {selected_ik}:
        raise RawVertexError("raw export contains an unauthorized global k-point")

    row_checks = _validate_row_identities(rows)
    diagonal = _summed_diagonal_and_covariance(rows)
    q_coverage = _q_coverage(rows)
    standard = compare_standard_outputs(disabled_stdout_path, enabled_stdout_path)
    thresholds = contract["thresholds"]
    checks = {
        "standard_output_unchanged": standard["maximum_self_energy_difference_ev"]
        <= float(thresholds["exporter_enabled_disabled_standard_output_max_abs_ev"]),
        "normalization_identity": row_checks["normalization_identity_max_abs_ry2"]
        <= float(thresholds["normalization_identity_max_abs_ry2"]),
        "per_row_real_diagonal": row_checks["per_row_real_diagonal_max_abs_ev"]
        <= float(thresholds["per_state_real_diagonal_max_abs_ev"]),
        "summed_real_diagonal": diagonal["summed_real_diagonal_max_abs_ev"]
        <= float(thresholds["summed_real_diagonal_max_abs_ev"]),
        "synthetic_external_covariance": diagonal[
            "synthetic_external_covariance_max_abs_ev"
        ]
        <= float(thresholds["synthetic_external_covariance_max_abs_ev"]),
        "q_weight_sum": q_coverage["q_weight_sum_max_abs_from_one"]
        <= float(thresholds["q_weight_sum_max_abs"]),
        "imaginary_sign": row_checks["imaginary_sign_failure_count"] == 0,
        "acoustic_mask": row_checks["zero_mask_max_abs_ry2_or_ry"] <= 1.0e-15,
        "complete_four_band_blocks": diagonal["external_dimension"] == 4,
    }
    passed = all(checks.values())
    return {
        "schema_version": "1.0",
        "stage": "B0_epw_raw_vertex_fixture_result",
        "status": "passed" if passed else "failed",
        "input_sha256": {
            "raw_vertex": _sha256(raw_path),
            "disabled_stdout": _sha256(disabled_stdout_path),
            "enabled_stdout": _sha256(enabled_stdout_path),
            "contract": _sha256(contract_path),
        },
        "row_count": len(rows),
        "row_diagnostics": row_checks,
        "diagonal_and_covariance": diagonal,
        "q_coverage": q_coverage,
        "standard_output_comparison": standard,
        "checks": checks,
        "decision": {
            "classification": "RESTRICTED_GO" if passed else "STOP",
            "raw_complex_vertex_export_validated": passed,
            "normalization_validated_for_upstream_scalar_fixture": passed,
            "soc_spinor_compatibility_validated": False,
            "material_self_energy_validated": False,
            "automatic_followup_authorized": False,
            "failed_checks": [name for name, value in checks.items() if not value],
        },
        "authorization": contract["authorization"],
        "claim_boundary": contract["claim_boundary"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True)
    parser.add_argument("--disabled-stdout", required=True)
    parser.add_argument("--enabled-stdout", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()
    result = analyze(
        args.raw,
        args.disabled_stdout,
        args.enabled_stdout,
        args.contract,
    )
    Path(args.output_json).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if result["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
