from __future__ import annotations

import json
from pathlib import Path

from tools.audit_cdte_a0_first_point import analyze


def _write_inputs(tmp_path: Path, *, failing: bool) -> dict[str, Path]:
    pressure = 31.20 if failing else 2.0
    born_sum = -0.51611 if failing else 0.001
    raw_acoustic = -183.63 if failing else -1.0
    raw_optical = 223.27
    simple_optical = 283.52 if failing else 224.0
    scf = tmp_path / "scf.out"
    ph = tmp_path / "ph.out"
    no_asr = tmp_path / "no-asr.out"
    simple = tmp_path / "simple.out"
    state = tmp_path / "state.json"
    contract = Path(__file__).resolve().parents[1] / (
        "first_principles/a0/cdte_a0_first_point_audit_contract.json"
    )
    scf.write_text(
        f"""
!    total energy              =    -560.29427515 Ry
     estimated scf accuracy    <          4.5E-09 Ry
     highest occupied, lowest unoccupied level (ev):     7.9857    8.4830
          total   stress  (Ry/bohr**3)                   (kbar)     P=       {pressure:.2f}
   JOB DONE.
""",
        encoding="utf-8",
    )
    ph.write_text(
        f"""
     convergence threshold     =      1.0E-10
     Convergence has been achieved
     Convergence has been achieved
          Dielectric constant in cartesian axis
          (      62.326671426      0.000000000       0.000000000 )
          (       0.000000000     62.326671426       0.000000000 )
          (       0.000000000      0.000000000      62.326671426 )
          Effective charges Sum: Mean:       {born_sum:.5f}
   JOB DONE.
""",
        encoding="utf-8",
    )

    def dynmat(acoustic: float, optical: float) -> str:
        rows = []
        for index in range(1, 4):
            rows.append(f" {index} {acoustic:9.2f} -5.0000 0.0100")
        for index in range(4, 7):
            rows.append(f" {index} {optical:9.2f}  7.0000 5.0000")
        return "\n".join(rows) + "\n JOB DONE.\n"

    no_asr.write_text(dynmat(raw_acoustic, raw_optical), encoding="utf-8")
    simple.write_text(dynmat(0.0, simple_optical), encoding="utf-8")
    state.write_text(
        json.dumps(
            {
                "scf_converged": True,
                "gamma_phonon_executed": True,
                "dynmat_no_asr_completed": True,
                "dynmat_simple_asr_completed": True,
                "gamma_eigenvalues_preserved": True,
                "dielectric_and_born_requested": True,
            }
        ),
        encoding="utf-8",
    )
    return {
        "scf": scf,
        "ph": ph,
        "no_asr": no_asr,
        "simple": simple,
        "state": state,
        "contract": contract,
    }


def _analyze(paths: dict[str, Path]) -> dict[str, object]:
    return analyze(
        paths["scf"],
        paths["ph"],
        paths["no_asr"],
        paths["simple"],
        paths["state"],
        paths["contract"],
    )


def test_a0_audit_passes_a_physically_sane_fixture(tmp_path: Path) -> None:
    result = _analyze(_write_inputs(tmp_path, failing=False))
    decision = result["decision"]
    assert decision["execution_pass"]
    assert decision["electronic_sanity_pass"]
    assert decision["response_numerical_sanity_pass"]
    assert decision["fixed_volume_interpretation_pass"]
    assert decision["a1_electron_phonon_authorized"]
    assert decision["next_authorized_diagnostic"] is None


def test_a0_audit_blocks_a1_and_authorizes_only_one_diagnostic(tmp_path: Path) -> None:
    result = _analyze(_write_inputs(tmp_path, failing=True))
    decision = result["decision"]
    assert decision["execution_pass"]
    assert decision["electronic_sanity_pass"]
    assert not decision["response_numerical_sanity_pass"]
    assert not decision["fixed_volume_interpretation_pass"]
    assert not decision["a1_electron_phonon_authorized"]
    assert set(decision["failed_response_checks"]) == {
        "raw_acoustic_translation",
        "born_charge_neutrality",
        "asr_optical_stability",
    }
    diagnostic = decision["next_authorized_diagnostic"]
    assert diagnostic["ecutrho_ry"] == 570
    assert diagnostic["ph_tr2_ph"] == 1e-14
