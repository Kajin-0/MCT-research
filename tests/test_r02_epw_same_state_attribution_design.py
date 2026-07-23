from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from tools.design_epw_same_state_attribution import (
    SameStateDesignError,
    assert_identical_manifests,
    build_dry_run_manifest,
    build_tree_manifest,
    compare_pre_post_manifests,
    evaluate_attribution,
    load_contract,
    manifest_payload,
    require_paths,
    validate_contract,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_same_state_attribution_contract.json"
REPLAY_INPUT = ROOT / "first_principles/b0/r02_epw_same_state_replay.in"
TOOL = ROOT / "tools/design_epw_same_state_attribution.py"


def _contract() -> dict:
    return load_contract(CONTRACT)


def _state_tree(root: Path) -> Path:
    root.mkdir(parents=True)
    required = _contract()["prepared_state"]["source_audited_required_paths"]
    for index, relative in enumerate(required):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"state-{index}-{relative}\n".encode())
    (root / "unknown-but-preserved.dat").write_bytes(b"conservative clone\n")
    return root


def _metrics(value: float) -> dict[str, list[float]]:
    return {
        "energy_ev": [value, value + 0.1],
        "self_energy_ev": [value * 2.0, value * 3.0],
        "dimensionless": [value * 0.5, value * 0.25],
    }


def _floors() -> dict[str, float]:
    return _contract()["attribution_rule"]["numerical_floors"]


def _ceilings() -> dict[str, float]:
    return _contract()["attribution_rule"]["baseline_reproducibility_ceilings"]


def test_contract_is_design_only_and_historical_result_is_unchanged() -> None:
    contract = _contract()
    validate_contract(contract)
    assert contract["issue"] == 318
    assert contract["predecessor_issue"] == 313
    assert contract["predecessor_result_commit"] == (
        "49476afe6f9b4c3b2be534bc9d81ada67c4ecab9"
    )
    assert contract["phase"] == "design_only"
    assert contract["attribution_rule"]["historical_issue_313_result_unchanged"] is True
    assert contract["attribution_rule"]["retrospective_floor_or_threshold_change_allowed"] is False
    authorization = contract["authorization"]
    for field in (
        "configure_or_build",
        "preparation_execution",
        "epw_replay_execution",
        "automatic_retry",
        "threshold_fitting",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "automatic_phase_transition",
    ):
        assert authorization[field] is False


def test_replay_input_changes_only_restart_controls() -> None:
    contract = _contract()
    replay = contract["replay_input"]
    assert replay["sha256"] == (
        "6e36c722d58c90cb6d58ffdee06568d1803fdea41c1d1196f57c583e8add7b73"
    )
    assert replay["derived_from_epw1"] == {
        "epwwrite": [True, False],
        "epwread": [False, True],
        "wannierize": [True, False],
    }
    assert replay["electron_self_energy_enabled"] is True
    assert replay["nest_function_enabled"] is False
    assert replay["physical_parameter_change"] is False
    text = REPLAY_INPUT.read_text(encoding="utf-8")
    assert "epwwrite    = .false." in text
    assert "epwread     = .true." in text
    assert "wannierize  = .false." in text
    assert "elecselfen  = .true." in text
    assert "nest_fn     = .false." in text


def test_source_read_set_and_complete_tree_policy_are_explicit() -> None:
    contract = _contract()
    assert contract["source"]["files"]["EPW/src/io/io.f90"] == (
        "73fb24ecbf4b690c460006ec354d0b9a7772a044"
    )
    assert contract["upstream_control_flow"]["epmatwp_open_mode_mpi"] == (
        "MPI_MODE_RDONLY"
    )
    state = contract["prepared_state"]
    assert state["source_audited_required_paths"] == [
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
    assert state["preexisting_file_mutation_allowed"] is False
    assert state["preexisting_file_deletion_allowed"] is False


def test_tree_manifest_hashes_all_regular_files_and_required_paths(tmp_path: Path) -> None:
    tree = _state_tree(tmp_path / "state")
    entries = build_tree_manifest(tree)
    require_paths(entries, _contract()["prepared_state"]["source_audited_required_paths"])
    payload = manifest_payload(entries)
    assert payload["file_count"] == 8
    assert len(payload["manifest_sha256"]) == 64
    assert any(
        item["relative_path"] == "unknown-but-preserved.dat"
        for item in payload["files"]
    )


def test_missing_required_path_fails_closed(tmp_path: Path) -> None:
    tree = _state_tree(tmp_path / "state")
    (tree / "diam.ukk").unlink()
    with pytest.raises(SameStateDesignError, match="missing required"):
        require_paths(
            build_tree_manifest(tree),
            _contract()["prepared_state"]["source_audited_required_paths"],
        )


def test_symlink_is_rejected(tmp_path: Path) -> None:
    tree = _state_tree(tmp_path / "state")
    (tree / "link").symlink_to(tree / "epwdata.fmt")
    with pytest.raises(SameStateDesignError, match="symlink"):
        build_tree_manifest(tree)


def test_three_clone_manifests_must_be_identical(tmp_path: Path) -> None:
    manifests = {}
    for clone_id in ("disabled_a", "disabled_b", "enabled"):
        tree = _state_tree(tmp_path / clone_id)
        manifests[clone_id] = build_tree_manifest(tree)
    assert_identical_manifests(manifests, ["disabled_a", "disabled_b", "enabled"])
    (tmp_path / "enabled" / "epwdata.fmt").write_text("drift\n", encoding="utf-8")
    manifests["enabled"] = build_tree_manifest(tmp_path / "enabled")
    with pytest.raises(SameStateDesignError, match="clone differs"):
        assert_identical_manifests(
            manifests, ["disabled_a", "disabled_b", "enabled"]
        )


def test_preexisting_mutation_and_deletion_fail_closed(tmp_path: Path) -> None:
    tree = _state_tree(tmp_path / "state")
    pre = build_tree_manifest(tree)
    (tree / "epwdata.fmt").write_text("mutated\n", encoding="utf-8")
    (tree / "diam.ukk").unlink()
    post = build_tree_manifest(tree)
    result = compare_pre_post_manifests(
        pre,
        post,
        _contract()["prepared_state"]["allowed_new_file_patterns"],
    )
    assert result["passed"] is False
    assert result["mutated"] == ["epwdata.fmt"]
    assert result["deleted"] == ["diam.ukk"]


def test_only_declared_new_outputs_are_allowed(tmp_path: Path) -> None:
    tree = _state_tree(tmp_path / "state")
    pre = build_tree_manifest(tree)
    (tree / "EPW.bib").write_text("new output\n", encoding="utf-8")
    (tree / "linewidth.elself.300.000K").write_text("new output\n", encoding="utf-8")
    allowed = compare_pre_post_manifests(
        pre,
        build_tree_manifest(tree),
        _contract()["prepared_state"]["allowed_new_file_patterns"],
    )
    assert allowed["passed"] is True
    (tree / "unexpected.bin").write_bytes(b"not declared")
    rejected = compare_pre_post_manifests(
        pre,
        build_tree_manifest(tree),
        _contract()["prepared_state"]["allowed_new_file_patterns"],
    )
    assert rejected["passed"] is False
    assert rejected["unauthorized_new"] == ["unexpected.bin"]


def test_attribution_passes_inside_disabled_interval(tmp_path: Path) -> None:
    del tmp_path
    disabled_a = _metrics(1.0)
    disabled_b = {
        name: [value + 5e-13 for value in values]
        for name, values in disabled_a.items()
    }
    enabled = {
        name: [(left + right) / 2.0 for left, right in zip(disabled_a[name], disabled_b[name], strict=True)]
        for name in disabled_a
    }
    result = evaluate_attribution(
        disabled_a,
        disabled_b,
        enabled,
        floors=_floors(),
        baseline_ceilings=_ceilings(),
    )
    assert result["passed"] is True
    assert result["classification"] == "ATTRIBUTION_NONINTERFERENCE_PASS"
    assert result["statistical_population_claim_allowed"] is False
    assert result["historical_issue_313_result_changed"] is False


def test_unstable_disabled_baseline_stops_before_enabled_claim() -> None:
    disabled_a = _metrics(1.0)
    disabled_b = {
        name: [value + 2e-12 for value in values]
        for name, values in disabled_a.items()
    }
    result = evaluate_attribution(
        disabled_a,
        disabled_b,
        disabled_a,
        floors=_floors(),
        baseline_ceilings=_ceilings(),
    )
    assert result["passed"] is False
    assert result["classification"] == "ATTRIBUTION_STOP"
    assert any(
        metric["baseline_passed"] is False for metric in result["metrics"].values()
    )


def test_enabled_outside_expanded_interval_stops() -> None:
    disabled_a = _metrics(1.0)
    disabled_b = {
        name: [value + 5e-13 for value in values]
        for name, values in disabled_a.items()
    }
    enabled = deepcopy(disabled_a)
    enabled["self_energy_ev"][0] += 2e-12
    result = evaluate_attribution(
        disabled_a,
        disabled_b,
        enabled,
        floors=_floors(),
        baseline_ceilings=_ceilings(),
    )
    assert result["passed"] is False
    assert result["metrics"]["self_energy_ev"]["baseline_passed"] is True
    assert result["metrics"]["self_energy_ev"]["enabled_envelope_passed"] is False


def test_metric_shape_nonfinite_and_threshold_drift_fail_closed() -> None:
    a = _metrics(1.0)
    b = _metrics(1.0)
    e = _metrics(1.0)
    e["energy_ev"] = [1.0]
    with pytest.raises(SameStateDesignError, match="lengths differ"):
        evaluate_attribution(a, b, e, floors=_floors(), baseline_ceilings=_ceilings())
    e = _metrics(1.0)
    e["energy_ev"][0] = float("nan")
    with pytest.raises(SameStateDesignError, match="nonfinite"):
        evaluate_attribution(a, b, e, floors=_floors(), baseline_ceilings=_ceilings())
    bad_floors = _floors()
    bad_floors["energy_ev"] = -1.0
    with pytest.raises(SameStateDesignError, match="negative threshold"):
        evaluate_attribution(a, b, _metrics(1.0), floors=bad_floors, baseline_ceilings=_ceilings())


def test_dry_run_manifest_is_inert_and_deterministic(tmp_path: Path) -> None:
    prepared = _state_tree(tmp_path / "prepared")
    replay_root = tmp_path / "replays"
    manifest = build_dry_run_manifest(
        _contract(),
        prepared_state_dir=prepared,
        replay_root=replay_root,
        replay_input=REPLAY_INPUT,
        executable_label="/opt/qe build/bin/epw.x",
    )
    assert manifest["execution_authorized"] is False
    assert [item["id"] for item in manifest["replays"]] == [
        "disabled_a",
        "disabled_b",
        "enabled",
    ]
    assert [item["export_enabled"] for item in manifest["replays"]] == [
        False,
        False,
        True,
    ]
    assert all("/evidence/" in item["stdout"] for item in manifest["replays"])
    assert len(manifest["manifest_payload_sha256"]) == 64
    output = tmp_path / "dry-run.json"
    write_json(manifest, output)
    first = output.read_bytes()
    write_json(manifest, output)
    assert output.read_bytes() == first
    tool_text = TOOL.read_text(encoding="utf-8")
    assert "subprocess" not in tool_text
    assert "os.system" not in tool_text


def test_replay_input_hash_drift_fails_closed(tmp_path: Path) -> None:
    prepared = _state_tree(tmp_path / "prepared")
    bad_input = tmp_path / "replay.in"
    bad_input.write_text(REPLAY_INPUT.read_text(encoding="utf-8") + "! drift\n", encoding="utf-8")
    with pytest.raises(SameStateDesignError, match="SHA-256 mismatch"):
        build_dry_run_manifest(
            _contract(),
            prepared_state_dir=prepared,
            replay_root=tmp_path / "replays",
            replay_input=bad_input,
            executable_label="epw.x",
        )


def test_contract_rejects_execution_authorization() -> None:
    contract = deepcopy(_contract())
    contract["authorization"]["epw_replay_execution"] = True
    with pytest.raises(SameStateDesignError, match="must be false"):
        validate_contract(contract)
