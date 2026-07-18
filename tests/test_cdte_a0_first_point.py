from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.render_cdte_a0_first_point import _check_settings, _required_settings
from tools.render_cdte_a0_runtime_inputs import derive_settings

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "first_principles/a0/cdte_a0_first_point_contract.json"
RUN_SPEC_PATH = ROOT / "first_principles/a0/cdte_a0_run_spec.json"
SCF_TEMPLATE = ROOT / "first_principles/a0/templates/cdte_qe_scf_first_point.in.template"
PH_TEMPLATE = ROOT / "first_principles/a0/templates/cdte_qe_ph_gamma_first_point.in.template"
DRIVER = ROOT / "tools/run_cdte_a0_first_point_ci.sh"
WORKFLOW = ROOT / ".github/workflows/cdte-a0-first-point.yml"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_contract_authorizes_exactly_one_breadth_point() -> None:
    contract = _load(CONTRACT_PATH)
    auth = contract["authorization"]

    assert contract["stage"] == "A0_first_point_breadth_smoke"
    assert auth["one_qe_scf_point"] is True
    assert auth["gamma_eigenvalue_extraction"] is True
    assert auth["one_gamma_phonon_dielectric_born_point"] is True
    assert auth["convergence_claim"] is False
    assert auth["automatic_ladder_continuation"] is False
    assert auth["a1_electron_phonon"] is False
    assert auth["production_ahc"] is False
    assert auth["hgte"] is False
    assert auth["alloy"] is False
    assert contract["required_settings"] == {
        "reference_lattice_angstrom": 6.476035479332049,
        "ecutwfc_ry": 114.0,
        "ecutrho_ry": 456.0,
        "k_grid": [4, 4, 4],
        "k_grid_shift": [0, 0, 0],
        "nbnd": 40,
        "scf_conv_thr_ry": 1e-8,
        "ph_tr2": 1e-10,
        "q_point": [0.0, 0.0, 0.0],
    }


def test_run_spec_derives_exact_contract_settings() -> None:
    settings = derive_settings(_load(RUN_SPEC_PATH))
    required = _required_settings(_load(CONTRACT_PATH))

    _check_settings(settings, required)
    assert settings["volume_grid"]["execution_authorized"] is True
    assert settings["volume_grid"]["reference_lattice_constant_angstrom"] == (
        required["reference_lattice_angstrom"]
    )


def test_setting_drift_fails_closed() -> None:
    settings = derive_settings(_load(RUN_SPEC_PATH))
    required = dict(_required_settings(_load(CONTRACT_PATH)))
    required["nbnd"] = 48

    with pytest.raises(ValueError, match="differs from contract"):
        _check_settings(settings, required)


def test_scf_template_is_real_execution_not_dry_run() -> None:
    text = SCF_TEMPLATE.read_text(encoding="utf-8")

    assert "calculation = 'scf'" in text
    assert "nstep = 0" not in text
    assert "tprnfor = .true." in text
    assert "tstress = .true." in text
    assert "noncolin = .true." in text
    assert "lspinorb = .true." in text
    assert "@ECUTWFC_RY@" in text
    assert "@ECUTRHO_RY@" in text
    assert "@KGRID@ @KGRID@ @KGRID@ 0 0 0" in text


def test_ph_template_is_one_gamma_response_point() -> None:
    text = PH_TEMPLATE.read_text(encoding="utf-8")

    assert "ldisp = .false." in text
    assert "trans = .true." in text
    assert "epsil = .true." in text
    assert "niter_ph" not in text
    assert text.rstrip().endswith("0.0 0.0 0.0")


def test_driver_stops_before_phonons_on_scf_failure() -> None:
    text = DRIVER.read_text(encoding="utf-8")

    scf = text.index('stage="scf"')
    convergence_gate = text.index("convergence has been achieved", scf)
    job_gate = text.index("JOB DONE", convergence_gate)
    eigenvalues = text.index('stage="eigenvalue_extraction"', job_gate)
    phonon = text.index('stage="gamma_phonon"', eigenvalues)

    assert scf < convergence_gate < job_gate < eigenvalues < phonon
    assert 'automatic_next_point_authorized": False' in text
    assert "for ecut" not in text
    assert "for kgrid" not in text


def test_workflow_isolated_to_first_point_files() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "cdte-a0-first-point" in text
    assert "run_cdte_a0_first_point_ci.sh" in text
    assert "timeout-minutes: 180" in text
    assert "cdte-a0-first-point-evidence" in text
    assert "run_cdte_a0_runtime_readiness_ci.sh" not in text
