from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

from tools.analyze_epw_nonmutating_replay_validation import analyze
from tools.design_epw_replay_output_boundary import (
    build_tree_manifest,
    manifest_payload,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_nonmutating_replay_validation_contract.json"
BOUNDARY = ROOT / "first_principles/b0/r02_epw_replay_output_boundary_contract.json"
PATCH = ROOT / "patches/qe76-epw61-serial-epwread-epmatwp-allocation.patch"
REPLAY_INPUT = ROOT / "first_principles/b0/r02_epw_nonmutating_replay.in"
DRIVER = ROOT / "tools/run_epw_nonmutating_replay_validation_ci.sh"
ANALYZER = ROOT / "tools/analyze_epw_nonmutating_replay_validation.py"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def _boundary() -> dict:
    return json.loads(BOUNDARY.read_text(encoding="utf-8"))


def _seed_tree(root: Path) -> Path:
    root.mkdir(parents=True)
    for index, relative in enumerate(
        _boundary()["path_classes"]["consumed_immutable_state"][
            "required_exact_paths"
        ]
    ):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"seed-{index}-{relative}\n".encode())
    (root / "unknown-retained.dat").write_bytes(b"immutable unknown\n")
    return root


def _write_manifest(tree: Path, destination: Path) -> None:
    write_json(manifest_payload(build_tree_manifest(tree)), destination)


def _evidence_case(tmp_path: Path) -> dict[str, Path]:
    seed_dir = _seed_tree(tmp_path / "seed")
    replay_dir = tmp_path / "replay"
    shutil.copytree(seed_dir, replay_dir)
    seed_manifest = tmp_path / "seed.json"
    post_manifest = tmp_path / "post.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    _write_manifest(seed_dir, seed_manifest)
    stdout.write_text(
        "selfen_elec_ : 1.00s CPU 1.00s WALL ( 216 calls)\n"
        "Total program execution\n",
        encoding="utf-8",
    )
    stderr.write_text("", encoding="utf-8")
    (replay_dir / "EPW.bib").write_text("citation\n", encoding="utf-8")
    (replay_dir / "linewidth.elself.300.000K").write_text(
        "# output\n1.0 2.0 3.0\n", encoding="utf-8"
    )
    _write_manifest(replay_dir, post_manifest)
    return {
        "seed_manifest": seed_manifest,
        "post_manifest": post_manifest,
        "replay_dir": replay_dir,
        "stdout": stdout,
        "stderr": stderr,
    }


def _analyze(case: dict[str, Path], *, exit_code: int = 0) -> dict:
    return analyze(
        execution_contract=CONTRACT,
        boundary_contract=BOUNDARY,
        seed_manifest=case["seed_manifest"],
        post_manifest=case["post_manifest"],
        replay_dir=case["replay_dir"],
        stdout_path=case["stdout"],
        stderr_path=case["stderr"],
        exit_code=exit_code,
    )


def test_contract_authorizes_exactly_one_bounded_replay() -> None:
    contract = _contract()
    assert contract["stage"] == "B0_epw_nonmutating_replay_validation"
    assert contract["issue"] == 371
    assert contract["design_issue"] == 355
    assert contract["design_merge_commit"] == (
        "4cb0b9fef65a67e56a794fd3676ef2e687d0e1c3"
    )
    assert contract["phase"] == "one_pinned_execution"
    authorization = contract["authorization"]
    for key in (
        "source_clone_and_verify",
        "apply_exact_patch",
        "exactly_one_build",
        "exactly_one_preparation",
        "exactly_one_serial_replay",
        "repository_analysis",
    ):
        assert authorization[key] is True
    for key in (
        "automatic_retry",
        "patch_adjustment_after_execution",
        "enabled_exporter_replay",
        "second_disabled_replay",
        "mpi_execution",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "parameter_sweep",
        "automatic_successor",
    ):
        assert authorization[key] is False


def test_source_patch_boundary_and_replay_input_are_pinned() -> None:
    contract = _contract()
    assert contract["source"]["commit_sha"] == (
        "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    )
    assert contract["source"]["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert len(contract["source"]["source_tree_archive_sha256"]) == 64
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest() == contract["patch"][
        "sha256"
    ]
    assert hashlib.sha256(REPLAY_INPUT.read_bytes()).hexdigest() == contract[
        "fixture"
    ]["replay_input_sha256"]
    assert contract["boundary_design"]["contract_git_blob_sha"] == (
        "daf45bab4df80d0762a115460757d11098dcc1ae"
    )
    assert contract["fixture"]["replay_input_git_blob_sha"] == (
        "480ad888c3c24f84d516b3daeb6a2558cd8044e1"
    )


def test_patch_is_the_exact_allocation_move() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    allocation = (
        "ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), "
        "STAT = ierr)"
    )
    assert patch.count("+      " + allocation) == 1
    assert patch.count("-      " + allocation) == 1
    assert patch.count("+      epmatwp = czero") == 1
    assert patch.count("-      epmatwp = czero") == 1
    assert "EPW/src/io/io.f90" in patch
    assert "selfen" not in patch.lower()
    assert "epf17" not in patch
    assert "MPI_FILE_READ_AT_ALL" not in patch
    assert "MPI_BCAST" not in patch


def test_replay_input_is_nonmutating_and_exporter_disabled() -> None:
    text = REPLAY_INPUT.read_text(encoding="utf-8")
    assert "epbwrite    = .false." in text
    assert "epbread     = .false." in text
    assert "epwwrite    = .false." in text
    assert "epwread     = .true." in text
    assert "wannierize  = .false." in text
    assert "elecselfen  = .true." in text
    assert "nest_fn     = .false." in text
    fixture = _contract()["fixture"]
    assert fixture["exporter_enabled"] is False
    assert fixture["soc_enabled"] is False
    assert fixture["epb_creation_allowed"] is False
    assert fixture["raw_vertex_creation_allowed"] is False


def test_driver_has_one_build_six_preparation_commands_and_one_replay() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert text.count("./configure --disable-parallel --enable-openmp") == 1
    assert text.count("make -j2 pw ph epw") == 1
    assert text.count("build_count=1") == 1
    for line in (
        "run_command 01 pw-scf",
        "run_command 02 ph",
        "run_command 03 pp",
        "run_command 04 pw-scf-epw",
        "run_command 05 pw-nscf-epw",
        "run_command 06 epw",
    ):
        assert text.count(line) == 1
    assert text.count("replay_count=1") == 1
    assert text.count('"$EPW_X" -input "$REPLAY_INPUT"') == 1
    assert "disabled_b" not in text
    assert "R02_EXPORT_RAW_VERTEX=1" not in text


def test_driver_projects_seed_and_opens_streams_before_launch() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "project_immutable_seed" in text
    assert "build_tree_manifest" in text
    assert "projected replay seed is not byte-identical" in text
    assert ': > "$EVIDENCE/replay/stdout.txt"' in text
    assert ': > "$EVIDENCE/replay/stderr.txt"' in text
    assert text.index(': > "$EVIDENCE/replay/stdout.txt"') < text.index(
        '"$EPW_X" -input "$REPLAY_INPUT"'
    )
    assert text.index(': > "$EVIDENCE/replay/stderr.txt"') < text.index(
        '"$EPW_X" -input "$REPLAY_INPUT"'
    )


def test_driver_prohibits_mpi_retry_and_sweeps() -> None:
    text = DRIVER.read_text(encoding="utf-8").lower()
    assert "mpirun" not in text
    assert "mpiexec" not in text
    assert "while true" not in text
    assert "until " not in text
    assert "rerun" not in text
    assert "for cutoff" not in text
    assert "for kgrid" not in text
    assert "for qgrid" not in text
    assert '"automatic_retry"' in text
    assert '"mpi_execution"' in text


def test_analyzer_passes_clean_complete_replay(tmp_path: Path) -> None:
    result = _analyze(_evidence_case(tmp_path))
    assert result["status"] == "pass"
    assert result["classification"] == "PASS_NONMUTATING_SERIAL_REPLAY"
    assert result["filesystem_integrity"]["passed"] is True
    assert result["completion_evidence"]["passed"] is True
    assert result["completion_evidence"]["selfen_timer_calls"] == [216]
    assert result["automatic_successor_authorized"] is False


def test_analyzer_stops_on_replay_runtime_failure(tmp_path: Path) -> None:
    case = _evidence_case(tmp_path)
    result = _analyze(case, exit_code=139)
    assert result["status"] == "stop"
    assert result["classification"] == "STOP_REPLAY_RUNTIME"


def test_analyzer_stops_on_immutable_mutation(tmp_path: Path) -> None:
    case = _evidence_case(tmp_path)
    (case["replay_dir"] / "epwdata.fmt").write_text("mutated\n", encoding="utf-8")
    _write_manifest(case["replay_dir"], case["post_manifest"])
    result = _analyze(case)
    assert result["classification"] == "STOP_STATE_MUTATION"
    assert result["filesystem_integrity"]["mutated_immutable_paths"] == [
        "epwdata.fmt"
    ]


def test_analyzer_stops_on_epb_or_unknown_output(tmp_path: Path) -> None:
    case = _evidence_case(tmp_path)
    (case["replay_dir"] / "diam.epb1").write_bytes(b"forbidden")
    _write_manifest(case["replay_dir"], case["post_manifest"])
    result = _analyze(case)
    assert result["classification"] == "STOP_FORBIDDEN_OUTPUT"
    assert result["filesystem_integrity"]["forbidden_created_paths"] == [
        "diam.epb1"
    ]


def test_analyzer_stops_on_missing_completion_evidence(tmp_path: Path) -> None:
    case = _evidence_case(tmp_path)
    case["stdout"].write_text("Total program execution\n", encoding="utf-8")
    result = _analyze(case)
    assert result["classification"] == "STOP_COMPLETION_EVIDENCE"
    assert result["completion_evidence"]["selfen_timer_positive_call_count"] is False


def test_terminal_evidence_is_written_on_every_driver_exit() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "trap finish EXIT" in text
    assert 'EVIDENCE/validated/result.json' in text
    assert 'EVIDENCE/runtime/status.json' in text
    assert "evidence_sha256.txt" in text
    for classification in _contract()["failure_classifications"]:
        assert classification in text or classification in ANALYZER.read_text(
            encoding="utf-8"
        )


def test_claim_boundary_keeps_exporter_soc_and_material_work_closed() -> None:
    boundary = _contract()["claim_boundary"]
    assert "only one patched" in boundary
    assert "exporter-disabled" in boundary
    assert "does not validate exporter noninterference" in boundary
    assert "SOC" in boundary
    assert "CdTe" in boundary
    assert "A1 readiness" in boundary
