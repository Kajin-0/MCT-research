from __future__ import annotations

import json
from pathlib import Path

from tools.compare_cdte_a0_response_diagnostic import compare
from tools.render_cdte_a0_runtime_inputs import derive_settings
from tools.render_cdte_a0_stricter_response import _effective_settings

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/a0/cdte_a0_stricter_response_contract.json"
RUN_SPEC = ROOT / "first_principles/a0/cdte_a0_run_spec.json"
DRIVER = ROOT / "tools/run_cdte_a0_stricter_response_ci.sh"
WORKFLOW = ROOT / ".github/workflows/cdte-a0-stricter-response.yml"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_contract_changes_only_the_authorized_response_controls() -> None:
    contract = _load(CONTRACT)
    settings = contract["required_settings"]
    assert contract["stage"] == "A0_same_geometry_stricter_response_diagnostic"
    assert settings["ecutwfc_ry"] == 114.0
    assert settings["ecutrho_ry"] == 570.0
    assert settings["ph_tr2"] == 1e-14
    assert settings["reference_lattice_angstrom"] == 6.476035479332049
    assert settings["k_grid"] == [4, 4, 4]
    assert settings["nbnd"] == 40
    assert contract["authorization"]["automatic_ladder_continuation"] is False
    assert contract["authorization"]["a1_electron_phonon"] is False


def test_renderer_applies_only_declared_overrides() -> None:
    contract = _load(CONTRACT)
    derived = derive_settings(_load(RUN_SPEC))
    effective = _effective_settings(_load(RUN_SPEC), contract)
    assert derived["ecutrho_ry"] == 456.0
    assert derived["ph_tr2"] == 1e-10
    assert effective["ecutrho_ry"] == 570.0
    assert effective["ph_tr2"] == 1e-14
    for name in (
        "reference_lattice_angstrom",
        "ecutwfc_ry",
        "nbnd",
        "scf_conv_thr_ry",
        "kgrid",
    ):
        assert effective[name] == derived[name]


def test_comparison_requires_all_three_metrics_to_collapse() -> None:
    contract = _load(CONTRACT)
    baseline = {
        "observables": {
            "maximum_raw_acoustic_absolute_frequency_cm1": 100.0,
            "born_charge_sum_mean_e": -0.5,
            "asr_optical_relative_shift": 0.2,
            "total_energy_ry": -1.0,
            "direct_gamma_gap_ev": 0.5,
            "pressure_kbar": 30.0,
            "dielectric_eigenvalues": [10.0, 10.0, 10.0],
            "raw_optical_mean_cm1": 200.0,
            "simple_asr_optical_mean_cm1": 240.0,
        }
    }
    improved = {
        "observables": {
            "maximum_raw_acoustic_absolute_frequency_cm1": 40.0,
            "born_charge_sum_mean_e": -0.2,
            "asr_optical_relative_shift": 0.08,
            "total_energy_ry": -1.1,
            "direct_gamma_gap_ev": 0.49,
            "pressure_kbar": 29.5,
            "dielectric_eigenvalues": [11.0, 11.0, 11.0],
            "raw_optical_mean_cm1": 205.0,
            "simple_asr_optical_mean_cm1": 221.4,
        }
    }
    result = compare(baseline, improved, contract)
    assert result["decision"]["all_three_failed_response_metrics_materially_collapsed"]
    improved["observables"]["born_charge_sum_mean_e"] = -0.4
    result = compare(baseline, improved, contract)
    assert not result["decision"]["all_three_failed_response_metrics_materially_collapsed"]
    assert not result["decision"]["a1_electron_phonon_authorized"]


def test_driver_and_workflow_are_single_point_and_fail_closed() -> None:
    driver = DRIVER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert driver.count('stage="scf"') == 1
    assert driver.count('stage="gamma_phonon"') == 1
    assert "for ecut" not in driver
    assert "for kgrid" not in driver
    assert "automatic_next_point_authorized\": False" in driver
    assert "stricter-response-comparison.json" in driver
    assert "cdte-a0-stricter-response-evidence" in workflow
    assert "timeout-minutes: 180" in workflow
