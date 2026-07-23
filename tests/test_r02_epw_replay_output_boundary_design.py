from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from tools.design_epw_replay_output_boundary import (
    FileRecord,
    ReplayBoundaryError,
    build_dry_run_manifest,
    build_tree_manifest,
    classify_path,
    compare_replay_tree,
    count_numeric_rows,
    evaluate_completion,
    load_contract,
    manifest_payload,
    project_immutable_seed,
    validate_contract,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_replay_output_boundary_contract.json"
REPLAY_INPUT = ROOT / "first_principles/b0/r02_epw_nonmutating_replay.in"
TOOL = ROOT / "tools/design_epw_replay_output_boundary.py"
PREDECESSOR_RESULT = (
    ROOT / "first_principles/b0/r02_epw_serial_patch_validation_terminal_result.json"
)


def _contract() -> dict:
    return load_contract(CONTRACT)


def _write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _preparation_tree(root: Path) -> Path:
    required = _contract()["path_classes"]["consumed_immutable_state"][
        "required_exact_paths"
    ]
    for index, relative in enumerate(required):
        _write(root / relative, f"immutable-{index}-{relative}\n".encode())
    _write(root / "unknown-required-by-conservative-policy.dat", b"retain me\n")
    _write(root / "EPW.bib", b"preparation output\n")
    _write(root / "linewidth.elself.300.000K", b"1 2 3\n")
    _write(root / "selecq.fmt", b"selection output\n")
    _write(root / "diam.kgmap", b"map output\n")
    _write(root / "diam_0.kmap", b"map output\n")
    _write(root / "diam.epb1", b"forbidden coarse Bloch serialization\n")
    _write(root / "out.1_1", b"transient\n")
    return root


def _copy_records(records: list[FileRecord]) -> list[FileRecord]:
    return [FileRecord(**record.as_dict()) for record in records]


def _valid_stdout(calls: int = 216) -> str:
    return (
        "Reading Hamiltonian, Dynamical matrix and EP vertex in Wann rep from file\n"
        "Electron-Phonon interpolation\n"
        f"selfen_elec_ : 1.23s CPU 1.25s WALL ({calls} calls)\n"
        "Total program execution\n"
        "EPW : 1.60s CPU 1.67s WALL\n"
    )


def _valid_outputs() -> dict[str, bytes]:
    return {
        "linewidth.elself.300.000K": (
            b"# ik ibnd energy linewidth\n"
            b"1 1 -1.234000E+00 2.500000E-03\n"
            b"2 1 -1.100000D+00 2.700000D-03\n"
        ),
        "EPW.bib": b"@Article{Giustino2007}\n",
    }


def test_contract_is_design_only_and_preserves_issue_350_stop() -> None:
    contract = _contract()
    validate_contract(contract)
    assert contract["issue"] == 355
    assert contract["predecessor_issue"] == 350
    assert contract["predecessor_result_commit"] == (
        "743f34f8f3e0e9edbdf66185ffaa62df67ac4a6d"
    )
    assert contract["classification_target"] == "REPLAY_BOUNDARY_SUPPORTED"
    assert contract["historical_issue_350_result_unchanged"] is True
    result = json.loads(PREDECESSOR_RESULT.read_text(encoding="utf-8"))
    assert result["classification"] == "SERIAL_EPWREAD_PATCH_VALIDATION_STOP"


def test_replay_input_changes_only_epb_output_control() -> None:
    contract = _contract()
    replay = contract["replay_input"]
    assert replay["sha256"] == (
        "e56d76aad9dd4fd6f8a5e2969bcc66ebff0fa468836cb2a313adffb11b5d8dda"
    )
    assert replay["delta"] == {
        "epbwrite": [True, False],
        "epbread": [False, False],
    }
    assert replay["physical_parameter_change"] is False
    assert replay["self_energy_parameter_change"] is False
    assert replay["restart_format_change"] is False
    assert replay["output_control_change_only"] is True
    text = REPLAY_INPUT.read_text(encoding="utf-8")
    assert "epbwrite    = .false." in text
    assert "epbread     = .false." in text
    assert "epwwrite    = .false." in text
    assert "epwread     = .true." in text
    assert "wannierize  = .false." in text
    assert "elecselfen  = .true." in text


def test_source_audit_resolves_epb_as_optional_serialization() -> None:
    findings = _contract()["source_findings"]
    assert findings["epbread_default"] is False
    assert findings["epbwrite_default"] is False
    assert findings["epwread_without_epbread_skips_coarse_epmatq_reconstruction"] is True
    assert findings["epwread_without_epbread_message"] == (
        "Do not need to read .epb files; read .fmt files"
    )
    assert findings["epb_serialization_condition"] == "epbread OR epbwrite"
    assert findings["epbwrite_changes_self_energy_control_flow"] is False
    assert findings["epbwrite_changes_in_memory_physics"] is False
    assert findings["diam_epb1_consumed_by_tested_replay"] is False
    assert findings["diam_epb1_rewritten_because_epbwrite_true"] is True


def test_path_classes_are_disjoint_for_required_and_known_paths() -> None:
    contract = _contract()
    required = contract["path_classes"]["consumed_immutable_state"][
        "required_exact_paths"
    ]
    assert all(classify_path(contract, path) == "consumed_immutable_state" for path in required)
    assert classify_path(contract, "diam.epb1") == "forbidden_unknown_files"
    assert classify_path(contract, "linewidth.elself.300.000K") == (
        "replay_declared_outputs"
    )
    assert classify_path(contract, "out.1_1") == "transient_runtime_files"
    assert classify_path(contract, "unrecognized-state.dat") == (
        "consumed_immutable_state"
    )


def test_projection_removes_outputs_transients_and_epb_but_retains_unknowns(
    tmp_path: Path,
) -> None:
    preparation = build_tree_manifest(_preparation_tree(tmp_path / "preparation"))
    projection = project_immutable_seed(preparation, _contract())
    seed_paths = {record.relative_path for record in projection["seed"]}
    assert "unknown-required-by-conservative-policy.dat" in seed_paths
    assert "diam.epb1" not in seed_paths
    assert "EPW.bib" not in seed_paths
    assert "linewidth.elself.300.000K" not in seed_paths
    assert "out.1_1" not in seed_paths
    assert projection["removed"]["forbidden_unknown_files"] == ["diam.epb1"]
    assert "EPW.bib" in projection["removed"]["replay_declared_outputs"]
    assert projection["removed"]["transient_runtime_files"] == ["out.1_1"]


def test_missing_source_audited_consumed_path_fails_closed(tmp_path: Path) -> None:
    tree = _preparation_tree(tmp_path / "preparation")
    (tree / "diam.epmatwp").unlink()
    with pytest.raises(ReplayBoundaryError, match="missing source-audited"):
        project_immutable_seed(build_tree_manifest(tree), _contract())


def test_symlink_is_rejected(tmp_path: Path) -> None:
    tree = _preparation_tree(tmp_path / "preparation")
    (tree / "link").symlink_to(tree / "epwdata.fmt")
    with pytest.raises(ReplayBoundaryError, match="symlink"):
        build_tree_manifest(tree)


def test_valid_post_replay_tree_preserves_seed_and_creates_declared_outputs(
    tmp_path: Path,
) -> None:
    preparation = build_tree_manifest(_preparation_tree(tmp_path / "preparation"))
    seed = project_immutable_seed(preparation, _contract())["seed"]
    post = _copy_records(seed)
    post.extend(
        [
            FileRecord("EPW.bib", "regular", 0o644, 10, "a" * 64),
            FileRecord(
                "linewidth.elself.300.000K", "regular", 0o644, 100, "b" * 64
            ),
            FileRecord("out.1_1", "regular", 0o644, 5, "c" * 64),
        ]
    )
    comparison = compare_replay_tree(seed, post, _contract())
    assert comparison["passed"] is True
    assert comparison["created_declared_outputs"] == [
        "EPW.bib",
        "linewidth.elself.300.000K",
    ]
    assert comparison["created_transient_files"] == ["out.1_1"]


def test_immutable_mutation_or_deletion_fails_closed(tmp_path: Path) -> None:
    preparation = build_tree_manifest(_preparation_tree(tmp_path / "preparation"))
    seed = project_immutable_seed(preparation, _contract())["seed"]
    post = _copy_records(seed)
    target = post[0]
    post[0] = FileRecord(
        target.relative_path,
        target.file_type,
        target.mode,
        target.size_bytes + 1,
        "d" * 64,
    )
    post.pop()
    comparison = compare_replay_tree(seed, post, _contract())
    assert comparison["passed"] is False
    assert comparison["mutated_immutable_paths"]
    assert comparison["deleted_immutable_paths"]


def test_epb_recreation_and_unknown_output_fail_closed(tmp_path: Path) -> None:
    preparation = build_tree_manifest(_preparation_tree(tmp_path / "preparation"))
    seed = project_immutable_seed(preparation, _contract())["seed"]
    post = _copy_records(seed)
    post.extend(
        [
            FileRecord("diam.epb1", "regular", 0o644, 660, "e" * 64),
            FileRecord("surprise.bin", "regular", 0o644, 12, "f" * 64),
        ]
    )
    comparison = compare_replay_tree(seed, post, _contract())
    assert comparison["passed"] is False
    assert comparison["forbidden_created_paths"] == ["diam.epb1"]
    assert comparison["unknown_created_paths"] == ["surprise.bin"]


def test_numeric_row_parser_accepts_fortran_exponents_and_rejects_headers() -> None:
    content = (
        b"# header\n"
        b"ik ibnd energy linewidth\n"
        b"1 2 -1.0E+00 2.5E-03\n"
        b"3 4 -2.0D+00 4.5D-03\n"
        b"not numeric\n"
    )
    assert count_numeric_rows(content) == 2


def test_completion_requires_all_independent_observables() -> None:
    result = evaluate_completion(
        stdout=_valid_stdout(),
        stderr="",
        exit_code=0,
        output_files=_valid_outputs(),
        contract=_contract(),
    )
    assert result["passed"] is True
    assert result["classification"] == "EPW_COMPLETION_EVIDENCE_PASS"
    assert result["selfen_timer_calls"] == [216]
    assert result["result_files_pass"] is True
    assert result["historical_issue_350_result_changed"] is False


def test_exit_zero_or_total_marker_alone_cannot_false_positive() -> None:
    result = evaluate_completion(
        stdout="Total program execution\n",
        stderr="",
        exit_code=0,
        output_files=_valid_outputs(),
        contract=_contract(),
    )
    assert result["passed"] is False
    assert result["selfen_timer_positive_call_count"] is False


def test_zero_call_timer_and_missing_total_marker_fail() -> None:
    zero_calls = evaluate_completion(
        stdout=_valid_stdout(calls=0),
        stderr="",
        exit_code=0,
        output_files=_valid_outputs(),
        contract=_contract(),
    )
    assert zero_calls["passed"] is False
    assert zero_calls["selfen_timer_positive_call_count"] is False
    missing_total = evaluate_completion(
        stdout=_valid_stdout().replace("Total program execution\n", ""),
        stderr="",
        exit_code=0,
        output_files=_valid_outputs(),
        contract=_contract(),
    )
    assert missing_total["passed"] is False
    assert missing_total["total_program_execution_present"] is False


def test_fatal_marker_or_nonzero_exit_fails() -> None:
    fatal = evaluate_completion(
        stdout=_valid_stdout(),
        stderr="Error in routine epw_read\n",
        exit_code=0,
        output_files=_valid_outputs(),
        contract=_contract(),
    )
    assert fatal["passed"] is False
    assert fatal["forbidden_markers_present"]["Error in routine"] is True
    nonzero = evaluate_completion(
        stdout=_valid_stdout(),
        stderr="",
        exit_code=1,
        output_files=_valid_outputs(),
        contract=_contract(),
    )
    assert nonzero["passed"] is False
    assert nonzero["exit_code_zero"] is False


def test_missing_empty_or_malformed_linewidth_output_fails() -> None:
    missing = evaluate_completion(
        stdout=_valid_stdout(),
        stderr="",
        exit_code=0,
        output_files={"EPW.bib": b"citation\n"},
        contract=_contract(),
    )
    assert missing["passed"] is False
    empty = evaluate_completion(
        stdout=_valid_stdout(),
        stderr="",
        exit_code=0,
        output_files={"linewidth.elself.300.000K": b""},
        contract=_contract(),
    )
    assert empty["passed"] is False
    malformed = evaluate_completion(
        stdout=_valid_stdout(),
        stderr="",
        exit_code=0,
        output_files={"linewidth.elself.300.000K": b"header only\n"},
        contract=_contract(),
    )
    assert malformed["passed"] is False


def test_rejected_historical_markers_do_not_affect_new_completion_rule() -> None:
    stdout = _valid_stdout() + "JOB DONE.\nElectron Self-Energy\n"
    result = evaluate_completion(
        stdout=stdout,
        stderr="",
        exit_code=0,
        output_files=_valid_outputs(),
        contract=_contract(),
    )
    assert result["passed"] is True
    rejected = _contract()["completion_observables"]["rejected_markers"]
    assert set(rejected) == {"JOB DONE.", "Electron Self-Energy"}


def test_dry_run_is_inert_deterministic_and_hash_pinned(tmp_path: Path) -> None:
    manifest = build_dry_run_manifest(
        _contract(),
        preparation_tree_label="prepared-tree-sha256",
        replay_seed_label="immutable-seed-sha256",
        replay_input=REPLAY_INPUT,
        executable_label="/opt/qe/bin/epw.x",
    )
    assert manifest["execution_authorized"] is False
    assert manifest["replay_input_sha256"] == (
        "e56d76aad9dd4fd6f8a5e2969bcc66ebff0fa468836cb2a313adffb11b5d8dda"
    )
    assert len(manifest["manifest_payload_sha256"]) == 64
    output = tmp_path / "dry-run.json"
    write_json(manifest, output)
    first = output.read_bytes()
    write_json(manifest, output)
    assert output.read_bytes() == first
    tool = TOOL.read_text(encoding="utf-8")
    assert "subprocess" not in tool
    assert "os.system" not in tool
    assert "Popen" not in tool


def test_input_hash_drift_fails_closed(tmp_path: Path) -> None:
    drift = tmp_path / "replay.in"
    drift.write_text(REPLAY_INPUT.read_text(encoding="utf-8") + "! drift\n", encoding="utf-8")
    with pytest.raises(ReplayBoundaryError, match="SHA-256 mismatch"):
        build_dry_run_manifest(
            _contract(),
            preparation_tree_label="prepared",
            replay_seed_label="seed",
            replay_input=drift,
            executable_label="epw.x",
        )


def test_accidental_execution_authorization_fails_contract_validation() -> None:
    contract = deepcopy(_contract())
    contract["authorization"]["epw_replay_execution"] = True
    with pytest.raises(ReplayBoundaryError, match="must be false"):
        validate_contract(contract)


def test_path_class_collision_fails_contract_validation() -> None:
    contract = deepcopy(_contract())
    contract["path_classes"]["replay_declared_outputs"]["patterns"].append(
        "epwdata.fmt"
    )
    with pytest.raises(ReplayBoundaryError, match="class collision"):
        validate_contract(contract)
