from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tools.analyze_epw_raw_vertex_fixture import (
    RawVertexError,
    analyze,
    compare_standard_outputs,
    parse_raw_rows,
)

ROOT = Path(__file__).resolve().parents[1]
BASE_CONTRACT = ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
PATCH = ROOT / "patches/qe76-epw61-r02-raw-vertex-export.patch"
RYD2EV = 13.605693122994


def _write_contract(tmp_path: Path, *, phase: str = "fixture_execution") -> Path:
    contract = json.loads(BASE_CONTRACT.read_text(encoding="utf-8"))
    contract["phase"] = phase
    if phase == "source_qualification_only":
        contract["authorization"]["qe_epw_build"] = False
        contract["authorization"]["upstream_fixture_execution"] = False
        contract["authorization"]["observational_export_patch_application"] = False
    path = tmp_path / f"contract-{phase}.json"
    path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    return path


def _vertex(q_index: int, mode: int, jbnd: int, ibnd: int) -> complex:
    scale = 1.0e-2 * (1 + q_index + mode + jbnd + ibnd)
    return complex(scale, 0.25 * scale * (jbnd - ibnd))


def _write_raw(tmp_path: Path, *, corrupt_g2: bool = False) -> Path:
    lines = ["# R02_RAW_VERTEX_V1", "# 8 integer fields followed by 19 real fields"]
    q_data = [(1, 1, 0.4), (2, 2, 0.6)]
    external = [-0.10, 0.00, 0.20, 0.30]
    intermediate_by_q = {
        1: [-0.20, 0.10, 0.40, 0.80],
        2: [-0.15, 0.12, 0.45, 0.85],
    }
    for iqq, iq, q_weight in q_data:
        intermediate = intermediate_by_q[iqq]
        for imode, (wq, inv_wq, mask, bose) in enumerate(
            [(1.0e-6, 0.0, 0.0, 0.0), (0.05, 10.0, 1.0, 0.2)],
            1,
        ):
            eta = 0.01
            for ibnd, ekk in enumerate(external, 1):
                for jbnd, ekq in enumerate(intermediate, 1):
                    epf = _vertex(iqq, imode, jbnd, ibnd)
                    f_occ = 1.0 if jbnd == 1 else 0.0
                    fact1 = f_occ + bose
                    fact2 = 1.0 - f_occ + bose
                    etmp1 = ekk - ekq + wq
                    etmp2 = ekk - ekq - wq
                    g2 = abs(epf) ** 2 * inv_wq * mask
                    if corrupt_g2 and iqq == 1 and imode == 2 and ibnd == 1 and jbnd == 1:
                        g2 += 1.0e-6
                    real_weight = q_weight * np.real(
                        fact1 / complex(etmp1, -eta)
                        + fact2 / complex(etmp2, -eta)
                    )
                    real_increment = g2 * real_weight
                    imag_increment = 0.0 if mask == 0.0 else abs(g2) * q_weight * 0.125
                    integers = [iqq, iq, 1, 1, imode, ibnd, jbnd, 1]
                    reals = [
                        epf.real,
                        epf.imag,
                        ekk,
                        ekq,
                        wq,
                        inv_wq,
                        mask,
                        q_weight,
                        f_occ,
                        bose,
                        eta,
                        fact1,
                        fact2,
                        etmp1,
                        etmp2,
                        g2,
                        real_increment,
                        imag_increment,
                        RYD2EV,
                    ]
                    lines.append(
                        " ".join([*(str(value) for value in integers), *(f"{value:.17e}" for value in reals)])
                    )
    path = tmp_path / "raw.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _write_stdout(tmp_path: Path, name: str, *, shift_mev: float = 0.0) -> Path:
    lines = ["EPW synthetic stdout", "Temperature: 300.000K"]
    for band, energy in enumerate([-1.0, 0.0, 1.0, 2.0], 1):
        lines.append(
            f"{1:9d}{band:9d}{energy:22.14E}{(0.1 * band + shift_mev):22.14E}"
            f"{(0.2 * band):22.14E}{0.9:22.14E}{0.1:22.14E}"
        )
    path = tmp_path / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_synthetic_raw_fixture_passes_all_normalization_gates(tmp_path: Path) -> None:
    result = analyze(
        _write_raw(tmp_path),
        _write_stdout(tmp_path, "disabled.out"),
        _write_stdout(tmp_path, "enabled.out"),
        _write_contract(tmp_path),
    )
    assert result["status"] == "passed"
    assert result["decision"]["classification"] == "RESTRICTED_GO"
    assert result["row_count"] == 64
    assert result["diagonal_and_covariance"]["external_dimension"] == 4
    assert result["diagonal_and_covariance"]["contribution_count"] == 4
    assert result["row_diagnostics"]["normalization_identity_max_abs_ry2"] < 1.0e-15
    assert result["row_diagnostics"]["per_row_real_diagonal_max_abs_ev"] < 1.0e-12
    assert result["diagonal_and_covariance"]["summed_real_diagonal_max_abs_ev"] < 1.0e-12
    assert result["q_coverage"]["q_weight_sum_max_abs_from_one"] < 1.0e-15
    assert result["row_diagnostics"]["zero_mask_row_count"] == 32
    assert all(result["checks"].values())
    assert result["decision"]["soc_spinor_compatibility_validated"] is False
    assert result["decision"]["material_self_energy_validated"] is False


def test_analyzer_rejects_prequalification_contract_phase(tmp_path: Path) -> None:
    with pytest.raises(RawVertexError, match="fixture_execution"):
        analyze(
            _write_raw(tmp_path),
            _write_stdout(tmp_path, "disabled.out"),
            _write_stdout(tmp_path, "enabled.out"),
            _write_contract(tmp_path, phase="source_qualification_only"),
        )


def test_analyzer_detects_normalization_corruption(tmp_path: Path) -> None:
    result = analyze(
        _write_raw(tmp_path, corrupt_g2=True),
        _write_stdout(tmp_path, "disabled.out"),
        _write_stdout(tmp_path, "enabled.out"),
        _write_contract(tmp_path),
    )
    assert result["status"] == "failed"
    assert result["checks"]["normalization_identity"] is False
    assert result["decision"]["classification"] == "STOP"


def test_enabled_disabled_standard_output_difference_is_detected(tmp_path: Path) -> None:
    comparison = compare_standard_outputs(
        _write_stdout(tmp_path, "disabled.out"),
        _write_stdout(tmp_path, "enabled.out", shift_mev=1.0e-6),
    )
    assert comparison["maximum_self_energy_difference_ev"] == pytest.approx(1.0e-9)


def test_raw_parser_requires_exact_field_count(tmp_path: Path) -> None:
    path = tmp_path / "bad.txt"
    path.write_text("1 2 3\n", encoding="utf-8")
    with pytest.raises(RawVertexError, match="expected 27"):
        parse_raw_rows(path)


def test_observational_patch_is_disabled_and_does_not_add_matrix_contraction() -> None:
    text = PATCH.read_text(encoding="utf-8")
    assert "R02_EXPORT_RAW_VERTEX" in text
    assert "R02_RAW_VERTEX_PATH" in text
    assert "R02_EXPORT_IK_GLOBAL" in text
    assert "r02_export_raw_vertex = .FALSE." in text
    assert "epf17(jbnd, ibnd, imode, ik)" in text
    assert "r02_real_increment = g2 * weight" in text
    assert "r02_imag_increment = g2 * weight" in text
    assert "ryd2ev" in text
    assert "ibnd2" not in text
    assert "MATMUL" not in text
    assert "G^dagger" not in text
    assert "19(ES26.17E3" in text


def test_patch_uses_compile_safe_short_header_lines() -> None:
    additions = [line[1:] for line in PATCH.read_text(encoding="utf-8").splitlines() if line.startswith("+")]
    for line in additions:
        assert len(line) <= 132
