from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.analyze_cdte_a0_zeu_zue import analyze

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/a0/cdte_a0_zeu_zue_contract.json"
DRIVER = ROOT / "tools/run_cdte_a0_zeu_zue_ci.sh"
WORKFLOW = ROOT / ".github/workflows/cdte-a0-zeu-zue-diagnostic.yml"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _ph_output(
    force_value: float,
    polarization_value: float | None,
    *,
    include_force: bool = True,
    include_polarization: bool = True,
) -> str:
    parts = [
        "Convergence has been achieved\nConvergence has been achieved\n",
        "Dielectric constant in cartesian axis\n"
        " ( 7.0 0.0 0.0 )\n ( 0.0 7.0 0.0 )\n ( 0.0 0.0 7.0 )\n",
    ]
    if include_force:
        parts.append(
            "Effective charges (d Force / dE) in cartesian axis without acoustic sum rule applied (asr)\n"
            " atom 1 Cd Mean Z*: 2.0\n"
            f" Ex ( {force_value:.6f} 0.0 0.0 )\n"
            f" Ey ( 0.0 {force_value:.6f} 0.0 )\n"
            f" Ez ( 0.0 0.0 {force_value:.6f} )\n"
            " atom 2 Te Mean Z*: -2.0\n"
            f" Ex ( {-force_value:.6f} 0.0 0.0 )\n"
            f" Ey ( 0.0 {-force_value:.6f} 0.0 )\n"
            f" Ez ( 0.0 0.0 {-force_value:.6f} )\n"
            "Effective charges Sum: Mean: 0.0\n"
        )
    if include_polarization:
        value = force_value if polarization_value is None else polarization_value
        parts.append(
            "Effective charges (d P / du) in cartesian axis\n"
            " atom 1 Cd\n"
            f" Px ( {value:.6f} 0.0 0.0 )\n"
            f" Py ( 0.0 {value:.6f} 0.0 )\n"
            f" Pz ( 0.0 0.0 {value:.6f} )\n"
            " atom 2 Te\n"
            f" Px ( {-value:.6f} 0.0 0.0 )\n"
            f" Py ( 0.0 {-value:.6f} 0.0 )\n"
            f" Pz ( 0.0 0.0 {-value:.6f} )\n"
        )
    parts.append("Diagonalizing the dynamical matrix\nJOB DONE\n")
    return "".join(parts)


def _write_case(tmp_path: Path, *, zue_value: float = 2.01, gap: float = 0.5) -> dict[str, Path]:
    paths = {
        "scf": tmp_path / "scf.out",
        "zeu": tmp_path / "ph-zeu.out",
        "zue": tmp_path / "ph-zue.out",
        "eigenvalues": tmp_path / "eigenvalues.json",
        "state": tmp_path / "state.json",
    }
    paths["scf"].write_text("convergence has been achieved\nJOB DONE\n", encoding="utf-8")
    paths["zeu"].write_text(
        _ph_output(2.0, None, include_force=True, include_polarization=False),
        encoding="utf-8",
    )
    paths["zue"].write_text(
        _ph_output(2.0, zue_value, include_force=False, include_polarization=True),
        encoding="utf-8",
    )
    paths["eigenvalues"].write_text(
        json.dumps(
            {
                "blocks": [
                    {
                        "index": 1,
                        "k_point_crystal": [0.0, 0.0, 0.0],
                        "eigenvalues_ev": [-1.0, 0.0, gap, 1.0],
                        "occupations": [1.0, 1.0, 0.0, 0.0],
                    },
                    {
                        "index": 2,
                        "k_point_crystal": [0.5, 0.0, 0.0],
                        "eigenvalues_ev": [-2.0, -0.5, 1.0, 2.0],
                        "occupations": [1.0, 1.0, 0.0, 0.0],
                    },
                ]
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    paths["state"].write_text(
        json.dumps(
            {
                "base_and_zeu_save_match": True,
                "base_and_zue_save_match": True,
                "scf_execution_count": 1,
                "response_route_count": 2,
                "route_settings_match_contract": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return paths


def test_contract_is_exactly_one_state_and_two_routes() -> None:
    contract = _load(CONTRACT)
    assert contract["stage"] == "A0_same_state_zeu_zue_response_diagnostic"
    assert contract["issue"] == 271
    settings = contract["required_settings"]
    assert settings["ecutwfc_ry"] == 114.0
    assert settings["ecutrho_ry"] == 570.0
    assert settings["k_grid"] == [4, 4, 4]
    assert settings["nbnd"] == 40
    assert settings["ph_tr2"] == 1e-14
    assert contract["baseline_run_spec"] == {"ecutrho_ry": 456.0, "ph_tr2": 1e-10}
    assert contract["source"]["stricter_response_reference_settings_required"] is True
    assert contract["routes"]["zeu"]["zeu"] is True
    assert contract["routes"]["zeu"]["zue"] is False
    assert contract["routes"]["zue"]["zeu"] is False
    assert contract["routes"]["zue"]["zue"] is True
    authorization = contract["authorization"]
    assert authorization["one_qe_scf_state"] is True
    assert authorization["exactly_two_gamma_response_routes"] is True
    assert authorization["automatic_retry"] is False
    assert authorization["automatic_ladder_continuation"] is False
    assert authorization["charge_asr_repair"] is False
    assert authorization["a1_electron_phonon"] is False


def test_driver_renders_explicit_independent_route_flags() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "tools.render_cdte_a0_stricter_response" in text
    assert 'rendered["settings"][name] == reference["settings"][name]' in text
    assert 'rendered["settings"]["q_point"] == [0.0, 0.0, 0.0]' in text
    assert 'contract["baseline_run_spec"] == {"ecutrho_ry": 456.0, "ph_tr2": 1e-10}' in text
    assert "f\"  zeu = {'.true.' if flags['zeu'] else '.false.'}" in text
    assert "f\"  zue = {'.true.' if flags['zue'] else '.false.'}" in text
    assert "base_and_zeu_save_match" in text
    assert "base_and_zue_save_match" in text


def test_analyzer_passes_only_internal_same_state_route_gate(tmp_path: Path) -> None:
    paths = _write_case(tmp_path)
    result = analyze(
        paths["scf"],
        paths["zeu"],
        paths["zue"],
        paths["eigenvalues"],
        paths["state"],
        CONTRACT,
    )
    assert result["decision"]["all_mandatory_conditions_pass"] is True
    assert result["decision"]["authorize_only_separate_k_grid_cutoff_design_review"] is True
    assert result["decision"]["a1_electron_phonon_authorized"] is False
    assert result["observables"]["maximum_zeu_zue_tensor_difference_e"] == pytest.approx(0.01)
    assert result["observables"]["sampled_band_separations"]["minimum_separation_ev"] == 0.5


def test_analyzer_terminates_path_on_route_disagreement(tmp_path: Path) -> None:
    paths = _write_case(tmp_path, zue_value=2.2)
    result = analyze(
        paths["scf"],
        paths["zeu"],
        paths["zue"],
        paths["eigenvalues"],
        paths["state"],
        CONTRACT,
    )
    assert result["decision"]["all_mandatory_conditions_pass"] is False
    assert result["decision"]["terminate_current_qe_pbe_pseudopotential_polar_path_for_a1"] is True
    assert "zeu_zue_tensor_agreement" in result["decision"]["failed_checks"]
    assert result["decision"]["automatic_followup_authorized"] is False


def test_analyzer_terminates_path_on_small_sampled_gap(tmp_path: Path) -> None:
    paths = _write_case(tmp_path, gap=0.05)
    result = analyze(
        paths["scf"],
        paths["zeu"],
        paths["zue"],
        paths["eigenvalues"],
        paths["state"],
        CONTRACT,
    )
    assert result["checks"]["sampled_insulating_separation"] is False
    assert result["decision"]["a1_electron_phonon_authorized"] is False


def test_driver_and_workflow_cannot_expand_into_a_sweep() -> None:
    driver = DRIVER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert driver.count('stage="scf"') == 1
    assert driver.count('stage="zeu_response"') == 1
    assert driver.count('stage="zue_response"') == 1
    assert "for ecut" not in driver
    assert "for kgrid" not in driver
    assert "automatic_retry_performed\": False" in driver
    assert "parameter_sweep_performed\": False" in driver
    assert "a1_or_production_executed\": False" in driver
    assert "timeout-minutes: 180" in workflow
    assert "cdte-a0-zeu-zue-evidence" in workflow
