from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import tools.analyze_epw_same_state_attribution as analyzer
from tools.analyze_epw_same_state_attribution import (
    SameStateAnalysisError,
    _classify,
    _load_three_tables,
    _table_metrics,
    analyze,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_same_state_execution_contract.json"
REPLAY_INPUT = ROOT / "first_principles/b0/r02_epw_same_state_replay.in"
PATCH = ROOT / "patches/qe76-epw61-r02-raw-vertex-export.patch"
ANALYZER = ROOT / "tools/analyze_epw_same_state_attribution.py"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def _write_table(path: Path, shift: float = 0.0) -> None:
    lines = []
    for ibnd in range(1, 5):
        energy = -1.0 + 0.1 * ibnd + shift
        real_mev = 10.0 + ibnd + shift * 1.0e3
        imag_mev = -2.0 - ibnd - shift * 1.0e3
        z = 0.9 + 0.01 * ibnd + shift
        lam = 0.1 + 0.01 * ibnd + shift
        lines.append(
            f"1 {ibnd} {energy:.16e} {real_mev:.16e} {imag_mev:.16e} "
            f"{z:.16e} {lam:.16e}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _state_integrity() -> dict:
    comparison = {
        "passed": True,
        "deleted": [],
        "mutated": [],
        "new_paths": [],
        "unauthorized_new": [],
    }
    return {
        "schema_version": "1.0",
        "stage": "B0_epw_same_state_integrity",
        "pre_manifests_identical": True,
        "required_paths_present": True,
        "replay_comparisons": {
            "disabled_a": deepcopy(comparison),
            "disabled_b": deepcopy(comparison),
            "enabled": deepcopy(comparison),
        },
    }


def _raw_pass() -> dict:
    return {"passed": True, "failed_checks": []}


def _attribution_pass() -> dict:
    return {
        "metrics": {
            "energy_ev": {
                "baseline_passed": True,
                "enabled_envelope_passed": True,
            },
            "self_energy_ev": {
                "baseline_passed": True,
                "enabled_envelope_passed": True,
            },
            "dimensionless": {
                "baseline_passed": True,
                "enabled_envelope_passed": True,
            },
        }
    }


def test_contract_is_one_build_one_preparation_three_replays() -> None:
    contract = _contract()
    assert contract["stage"] == "B0_epw_same_state_attribution_execution"
    assert contract["issue"] == 332
    assert contract["design_merge_commit"] == (
        "cb4b13c36bca8d1b47080be23a2c7190b35c6f1a"
    )
    assert contract["phase"] == "one_pinned_execution"
    assert contract["preparation"]["command_count"] == 6
    assert contract["replay"]["clone_ids"] == [
        "disabled_a",
        "disabled_b",
        "enabled",
    ]
    assert contract["replay"]["replay_count"] == 3
    authorization = contract["authorization"]
    for field in (
        "source_clone_and_verify",
        "observational_patch_application",
        "exactly_one_pinned_build",
        "exactly_one_preparation_sequence",
        "exactly_three_final_replays",
        "repository_analysis",
    ):
        assert authorization[field] is True
    for field in (
        "automatic_retry",
        "fourth_replay",
        "alternate_build",
        "parameter_sweep",
        "output_removal_or_manifest_relaxation",
        "threshold_fitting",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "automatic_phase_transition",
    ):
        assert authorization[field] is False


def test_source_verification_separates_sha256_and_git_objects() -> None:
    source = _contract()["source"]
    assert source["required_sha256"] == {
        "EPW/src/selfen.f90": "92814fb0ba79b355cda842598fe6e22ee24a77027864524c91fd6ea4bf63ff97",
        "test-suite/epw_base/scf.in": "74d06ffa7c45aef4fe11094e430d0cef00ccac74bcf689189ea1d6e84506563b",
        "test-suite/epw_base/ph.in": "1dac9d47d8c234f7b88ef5f8ce7db6c9aaeb1c4a83f7b2cd13bd78e288b4983f",
        "test-suite/epw_base/pp.in": "f052c801085cf37855fbab544b5cbe46c864e54c37a163a2bc6eab51c2a34e47",
        "test-suite/epw_base/scf_epw.in": "eccb8bd933e7748e65310d04e853992db0e2f353e8af062af26df00c4dc509f5",
        "test-suite/epw_base/nscf_epw.in": "bc1dae9fecb2d589f33d8e0924a1d7aae0e29603e8d63c0380e5bf3173eb6f41",
        "test-suite/epw_base/epw1.in": "18e83caf042d88d59d23653cb83319aa0cad9a400d8422f13f11788373045999",
        "pseudo/C_3.98148.UPF": "cc147806e663aa2c487cff67fc287a27d846edd438c7f4fc15d8851409244f2a",
    }
    assert source["required_git_blob_ids"]["EPW/src/epw.f90"] == (
        "fca6e313d45ef636a81ca45b3585d2abe3124da5"
    )
    assert source["required_git_blob_ids"]["EPW/src/close.f90"] == (
        "f9693bb6e7f8afbe1643cd6f039e90805aa0e100"
    )
    assert source["required_git_blob_ids"]["test-suite/epw_base/epw2.in"] == (
        "a30b69515a204f74d1565f43806efa72f064e67a"
    )


def test_preparation_outputs_cannot_be_removed_or_relaxed() -> None:
    state = _contract()["prepared_state"]
    assert state["required_paths"] == [
        "epwdata.fmt",
        "crystal.fmt",
        "vmedata.fmt",
        "dmedata.fmt",
        "wigner.fmt",
        "diam.epmatwp",
        "diam.ukk",
    ]
    assert state["complete_tree_manifest_required"] is True
    assert state["unknown_regular_files_included"] is True
    assert state["preexisting_mutation_allowed"] is False
    assert state["preexisting_deletion_allowed"] is False
    assert state["preparation_outputs_may_not_be_removed_before_manifest"] is True


def test_replay_input_and_patch_are_fixed() -> None:
    contract = _contract()
    assert contract["replay"]["input_sha256"] == (
        "6e36c722d58c90cb6d58ffdee06568d1803fdea41c1d1196f57c583e8add7b73"
    )
    replay = REPLAY_INPUT.read_text(encoding="utf-8")
    assert "epwwrite    = .false." in replay
    assert "epwread     = .true." in replay
    assert "wannierize  = .false." in replay
    assert "elecselfen  = .true." in replay
    patch = PATCH.read_text(encoding="utf-8")
    assert "r02_export_raw_vertex = .FALSE." in patch
    assert "R02_EXPORT_RAW_VERTEX" in patch
    assert "R02_RAW_VERTEX_PATH" in patch
    assert "MATMUL" not in patch


def test_table_metrics_preserve_units_and_indices() -> None:
    records = [
        {
            "ik": 1,
            "ibnd": 2,
            "energy_ev": 3.0,
            "real_sigma_mev": 4.0,
            "imag_sigma_mev": -5.0,
            "z": 0.9,
            "lambda": 0.2,
        }
    ]
    indices, metrics = _table_metrics(records)
    assert indices == [(1, 2)]
    assert metrics == {
        "energy_ev": [3.0],
        "self_energy_ev": [0.004, -0.005],
        "dimensionless": [0.9, 0.2],
    }


def test_three_tables_require_identical_ordered_indices(tmp_path: Path) -> None:
    a = tmp_path / "a.out"
    b = tmp_path / "b.out"
    e = tmp_path / "e.out"
    _write_table(a)
    _write_table(b)
    _write_table(e)
    _, _, _, rows = _load_three_tables(a, b, e)
    assert rows == 4
    e.write_text(e.read_text(encoding="utf-8").replace("1 4", "2 4"), encoding="utf-8")
    with pytest.raises(SameStateAnalysisError, match="index mismatch"):
        _load_three_tables(a, b, e)


def test_classification_priority_is_fail_closed() -> None:
    state = _state_integrity()
    attribution = _attribution_pass()
    raw = _raw_pass()
    assert _classify(state, attribution, raw)[0] == (
        "RESTRICTED_GO_SAME_STATE_NONINTERFERENCE"
    )

    broken = deepcopy(state)
    broken["pre_manifests_identical"] = False
    assert _classify(broken, attribution, raw)[0] == "STOP_HARNESS"

    broken = deepcopy(state)
    broken["replay_comparisons"]["enabled"]["mutated"] = ["linewidth.elself.300.000K"]
    assert _classify(broken, attribution, raw)[0] == "STOP_STATE_MUTATION"

    broken = deepcopy(state)
    broken["replay_comparisons"]["enabled"]["unauthorized_new"] = ["unknown.out"]
    assert _classify(broken, attribution, raw)[0] == "STOP_UNDECLARED_OUTPUT"

    broken_attr = deepcopy(attribution)
    broken_attr["metrics"]["energy_ev"]["baseline_passed"] = False
    assert _classify(state, broken_attr, raw)[0] == "STOP_BASELINE_REPRODUCIBILITY"

    broken_attr = deepcopy(attribution)
    broken_attr["metrics"]["self_energy_ev"]["enabled_envelope_passed"] = False
    assert _classify(state, broken_attr, raw)[0] == "STOP_EXPORTER_ATTRIBUTION"

    assert _classify(state, attribution, {"passed": False, "failed_checks": ["q_weight"]})[0] == (
        "STOP_RAW_DIAGNOSTIC"
    )


def test_analyze_passes_only_when_all_four_gates_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = tmp_path / "a.out"
    b = tmp_path / "b.out"
    e = tmp_path / "e.out"
    raw = tmp_path / "raw.txt"
    state = tmp_path / "state.json"
    contract = tmp_path / "contract.json"
    _write_table(a)
    _write_table(b, 5.0e-13)
    _write_table(e, 2.5e-13)
    raw.write_text("synthetic\n", encoding="utf-8")
    state.write_text(json.dumps(_state_integrity()), encoding="utf-8")
    contract.write_text(json.dumps(_contract()), encoding="utf-8")

    monkeypatch.setattr(
        analyzer,
        "parse_raw_rows",
        lambda _: [SimpleNamespace(ik_global=1)],
    )
    monkeypatch.setattr(
        analyzer,
        "_validate_row_identities",
        lambda _: {
            "normalization_identity_max_abs_ry2": 0.0,
            "per_row_real_diagonal_max_abs_ev": 0.0,
            "imaginary_sign_failure_count": 0,
            "zero_mask_max_abs_ry2_or_ry": 0.0,
        },
    )
    monkeypatch.setattr(
        analyzer,
        "_summed_diagonal_and_covariance",
        lambda _: {
            "summed_real_diagonal_max_abs_ev": 0.0,
            "synthetic_external_covariance_max_abs_ev": 0.0,
            "external_dimension": 4,
        },
    )
    monkeypatch.setattr(
        analyzer,
        "_q_coverage",
        lambda _: {"q_weight_sum_max_abs_from_one": 0.0},
    )
    result = analyze(
        raw_path=raw,
        disabled_a_stdout=a,
        disabled_b_stdout=b,
        enabled_stdout=e,
        state_integrity_path=state,
        contract_path=contract,
    )
    assert result["status"] == "restricted_go"
    assert result["classification"] == "RESTRICTED_GO_SAME_STATE_NONINTERFERENCE"
    assert result["decision"]["historical_issue_313_result_changed"] is False
    assert result["decision"]["soc_spinor_compatibility_validated"] is False
    assert result["decision"]["material_self_energy_validated"] is False
    assert result["decision"]["automatic_followup_authorized"] is False


def test_analyzer_contains_no_threshold_fitting_or_process_launch() -> None:
    text = ANALYZER.read_text(encoding="utf-8")
    assert "subprocess" not in text
    assert "os.system" not in text
    assert "optimize" not in text.lower()
    assert "curve_fit" not in text
    assert "automatic_followup_authorized\": False" in text
