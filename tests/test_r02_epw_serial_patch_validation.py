from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "first_principles/b0/r02_epw_serial_patch_validation_contract.json"
PATCH = ROOT / "patches/qe76-epw61-serial-epwread-epmatwp-allocation.patch"
REPLAY_INPUT = ROOT / "first_principles/b0/r02_epw_same_state_replay.in"
DRIVER = ROOT / "tools/run_epw_serial_patch_validation_ci.sh"
DIAGNOSIS_PATCH = ROOT / "research/patch_proposals/qe76-epw61-serial-epwread-epmatwp-allocation.patch"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_contract_authorizes_exactly_one_bounded_serial_validation() -> None:
    contract = _contract()
    assert contract["stage"] == "B0_epw_serial_patch_validation"
    assert contract["issue"] == 350
    assert contract["source_diagnosis_commit"] == (
        "2fcd412581fe55e69d722effb2f9a93b10ddb490"
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


def test_source_patch_and_replay_input_are_hash_pinned() -> None:
    contract = _contract()
    assert contract["source"]["commit_sha"] == (
        "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    )
    assert contract["source"]["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c8c2b7f7eaf8e05ecafbbcbac849"
    )
    assert contract["source"]["io_f90_git_blob_sha"] == (
        "73fb24ecbf4b690c460006ec354d0b9a7772a044"
    )
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest() == (
        contract["patch"]["sha256"]
    )
    assert hashlib.sha256(REPLAY_INPUT.read_bytes()).hexdigest() == (
        contract["fixture"]["replay_input_sha256"]
    )
    assert len(contract["source"]["source_tree_archive_sha256"]) == 64


def test_executable_patch_is_exactly_the_inert_design_change() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    diagnosis = DIAGNOSIS_PATCH.read_text(encoding="utf-8")
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
    for line in (
        allocation,
        "IF (ierr /= 0) CALL errore('epw_read', 'Error allocating epmatwp', 1)",
        "epmatwp = czero",
    ):
        assert line in diagnosis
        assert line in patch


def test_fixture_is_upstream_nonpolar_and_exporter_disabled() -> None:
    fixture = _contract()["fixture"]
    assert fixture["upstream_path"] == "test-suite/epw_base"
    assert fixture["material"] == "diamond"
    assert fixture["material_role"] == "upstream_nonpolar_software_fixture_only"
    assert fixture["soc_enabled"] is False
    assert fixture["long_range_included"] is False
    assert fixture["thermal_expansion_included"] is False
    assert fixture["exporter_enabled"] is False
    assert fixture["replay_input_sha256"] == (
        "6e36c722d58c90cb6d58ffdee06568d1803fdea41c1d1196f57c583e8add7b73"
    )
    text = REPLAY_INPUT.read_text(encoding="utf-8")
    assert "epwwrite    = .false." in text
    assert "epwread     = .true." in text
    assert "wannierize  = .false." in text
    assert "elecselfen  = .true." in text
    assert "nest_fn     = .false." in text


def test_driver_has_one_build_six_preparation_commands_and_one_replay() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert text.count("./configure --disable-parallel --enable-openmp") == 1
    assert text.count("make -j2 pw ph epw") == 1
    assert text.count("build_count=1") == 1
    preparation_lines = [
        "run_command 01 pw-scf",
        "run_command 02 ph",
        "run_command 03 pp",
        "run_command 04 pw-scf-epw",
        "run_command 05 pw-nscf-epw",
        "run_command 06 epw",
    ]
    assert all(text.count(line) == 1 for line in preparation_lines)
    assert text.count("replay_count=1") == 1
    assert text.count('"$EPW_X" -input "$REPLAY_INPUT"') == 1
    assert "disabled_b" not in text
    assert "enabled" not in text.lower() or "enabled_exporter_replay" in text


def test_driver_opens_replay_streams_before_process_launch() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    stdout_open = text.index(': > "$EVIDENCE/replay/stdout.txt"')
    stderr_open = text.index(': > "$EVIDENCE/replay/stderr.txt"')
    launch = text.index('"$EPW_X" -input "$REPLAY_INPUT"')
    assert stdout_open < launch
    assert stderr_open < launch
    assert 'printf \'%s\\n\' "$replay_exit_code"' in text


def test_driver_enforces_complete_state_integrity() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "build_tree_manifest" in text
    assert "require_paths" in text
    assert "compare_pre_post_manifests" in text
    assert "replay clone is not byte-identical" in text
    assert 'comparison["passed"]' in text
    assert _contract()["fixture"]["preexisting_file_mutation_allowed"] is False
    assert _contract()["fixture"]["preexisting_file_deletion_allowed"] is False


def test_driver_prohibits_exporter_mpi_retry_and_parameter_sweeps() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "unset R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH" in text
    assert "mpirun" not in text.lower()
    assert "mpiexec" not in text.lower()
    assert "while true" not in text.lower()
    assert "until " not in text.lower()
    assert "rerun" not in text.lower()
    assert "for cutoff" not in text.lower()
    assert "for kgrid" not in text.lower()
    assert "for qgrid" not in text.lower()
    assert '"automatic_retry"' in text
    assert '"mpi_execution"' in text


def test_terminal_evidence_is_written_for_pass_and_stop() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "trap finish EXIT" in text
    assert 'evidence / "runtime" / "status.json"' in text
    assert "validated/result.json" in text
    assert "evidence_sha256.txt" in text
    assert "SERIAL_EPWREAD_HARNESS_PASS" in text
    assert "SERIAL_EPWREAD_PATCH_VALIDATION_STOP" in text
    assert "JOB DONE." in CONTRACT.read_text(encoding="utf-8")
    assert "Electron Self-Energy" in CONTRACT.read_text(encoding="utf-8")


def test_claim_boundary_does_not_reopen_material_work() -> None:
    contract = _contract()
    boundary = contract["claim_boundary"]
    assert "only one patched serial epwread restart" in boundary
    assert "does not validate exporter noninterference" in boundary
    assert "SOC" in boundary
    assert "CdTe" in boundary
    assert "A1 readiness" in boundary
