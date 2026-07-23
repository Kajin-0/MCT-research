from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.model_epw_serial_epmatwp_allocation import (
    AllocationModelError,
    AllocationShape,
    allocation_shape,
    assert_all_local_indices_fit,
    assert_exactly_one_allocation,
    assert_serial_direct_read_fits,
    derive_distribution,
    diagnose_path,
    explicit_dummy_extent_risk,
    local_index_pairs,
    modeled_paths,
    serial_distribution,
)

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "first_principles/b0/r02_epw_serial_epmatwp_source_audit.json"
PATCH = ROOT / "research/patch_proposals/qe76-epw61-serial-epwread-epmatwp-allocation.patch"
CAPABILITY = ROOT / "research/capability_audits/qe76_epw61_serial_epwread_epmatwp_diagnosis.md"
DECISION = ROOT / "research/decision_records/2026-07-23-r02-serial-epwread-source-diagnosis.md"
STATE = ROOT / "research/programs/finite_temperature_kane/state_updates/2026-07-23-serial-epwread-source-diagnosis.md"
UPSTREAM = ROOT / "research/upstream_reports/qe-epw-serial-epwread-epmatwp-segfault-draft.md"
MODEL = ROOT / "tools/model_epw_serial_epmatwp_allocation.py"


def _audit() -> dict:
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_diagnosis_is_supported_but_runtime_validation_is_closed() -> None:
    audit = _audit()
    assert audit["stage"] == "B0_epw_serial_epmatwp_source_diagnosis"
    assert audit["issue"] == 335
    assert audit["phase"] == "design_only"
    assert audit["classification"] == "SOURCE_DIAGNOSIS_SUPPORTED"
    diagnosis = audit["diagnosis"]
    assert diagnosis["classification"] == "SOURCE_DIAGNOSIS_SUPPORTED"
    assert diagnosis["observed_failure_explained"] is True
    assert diagnosis["runtime_patch_validated"] is False
    assert diagnosis["mpi_behavior_validated"] is False
    assert diagnosis["scientific_behavior_changed"] is False


def test_pinned_source_and_later_comparison_are_exact() -> None:
    source = _audit()["source"]
    assert source["pinned_commit"] == "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    assert source["pinned_git_blob_ids"] == {
        "EPW/src/global_var.f90": "45ece671c03903d2186b118827cc5f7a31145da5",
        "EPW/src/io/io.f90": "73fb24ecbf4b690c460006ec354d0b9a7772a044",
        "EPW/src/wannier.f90": "a2b706939505a84b2d082e5a83a3dbb1ae8eef57",
        "EPW/src/wigner.f90": "85e7498a89e43632a5392f11828da9b247212223",
    }
    assert source["later_checked_commit"] == (
        "61569eb480231b649c47f631df9c5c83537df461"
    )
    assert source["later_io_blob_id"] == source["pinned_git_blob_ids"][
        "EPW/src/io/io.f90"
    ]
    assert source["later_source_retains_same_serial_branch"] is True
    assert [item["sha"] for item in source["historical_commits"]] == [
        "cbd08e75df513def922f37272d5f3c1ef1b78928",
        "9707a90417d4b2915c2345c23d2f7aeb8f752c9c",
        "a3e738ab6e6f436d08ee54d68406eac196b784c2",
    ]


def test_failure_identity_excludes_exporter_and_self_energy() -> None:
    failure = _audit()["observed_failure"]
    assert failure["workflow_run"] == 30020494017
    assert failure["artifact_id"] == 8569280948
    assert failure["replay"] == "disabled_a"
    assert failure["exporter_enabled"] is False
    assert failure["exit_code"] == 139
    assert failure["signal"] == "SIGSEGV"
    assert failure["routine"] == "wigner_divide_ndegen_epmat"
    assert failure["source_line"] == 1009
    assert failure["caller"] == "build_wannier"
    assert failure["caller_source_line"] == 452
    assert failure["occurred_before_self_energy_evaluation"] is True


def test_control_flow_contains_one_missing_allocation_path() -> None:
    flow = _audit()["control_flow"]
    assert any("allocates epmatwp" in step for step in flow["normal_preparation_etf_mem_0"])
    assert any("bypass" in step for step in flow["restart_common"])
    assert any("allocates epmatwp" in step for step in flow["restart_mpi"])
    assert any("no allocation" in step for step in flow["restart_serial"])
    assert any("davcio" in step for step in flow["restart_serial"])
    assert any("observed execution terminates" in step for step in flow["restart_serial"])


def test_serial_distribution_covers_global_ws_extent() -> None:
    distribution = serial_distribution(nrr_g=17, nmodes=6)
    assert distribution.irn_start == 1
    assert distribution.irn_stop == 102
    assert distribution.irg_start == 1
    assert distribution.irg_stop == 17
    assert distribution.nirg_loc == 17
    assert distribution.nirn_loc == 102
    shape = allocation_shape(nbndsub=4, nrr_k=9, distribution=distribution)
    assert shape.dimensions == (4, 4, 9, 6, 17)
    assert_serial_direct_read_fits(distribution, shape)
    assert_all_local_indices_fit(distribution, shape)
    pairs = local_index_pairs(distribution)
    assert pairs[0] == (1, 1, 1)
    assert pairs[-1] == (17, 6, 17)


def test_underallocation_and_invalid_distribution_fail_closed() -> None:
    distribution = serial_distribution(nrr_g=5, nmodes=6)
    too_small = AllocationShape(nbndsub=4, nrr_k=7, nmodes=6, fifth_extent=4)
    with pytest.raises(AllocationModelError, match="direct-read loop exceeds"):
        assert_serial_direct_read_fits(distribution, too_small)
    with pytest.raises(AllocationModelError, match="invalid combined"):
        derive_distribution(nrr_g=5, nmodes=6, irn_start=0, irn_stop=30)
    with pytest.raises(AllocationModelError, match="must be positive"):
        serial_distribution(nrr_g=0, nmodes=6)


def test_allocation_lifetime_model_matches_pinned_and_proposed_paths() -> None:
    paths = modeled_paths()
    assert diagnose_path(paths["normal_preparation"]) == "ALLOCATION_LIFETIME_VALID"
    assert diagnose_path(paths["restart_mpi_pinned"]) == "ALLOCATION_LIFETIME_VALID"
    assert diagnose_path(paths["restart_serial_pinned"]) == "MISSING_ALLOCATION"
    assert diagnose_path(paths["restart_mpi_proposed"]) == "ALLOCATION_LIFETIME_VALID"
    assert diagnose_path(paths["restart_serial_proposed"]) == "ALLOCATION_LIFETIME_VALID"
    assert_exactly_one_allocation(paths["restart_mpi_proposed"])
    assert_exactly_one_allocation(paths["restart_serial_proposed"])
    with pytest.raises(AllocationModelError, match="observed 0"):
        assert_exactly_one_allocation(paths["restart_serial_pinned"])
    with pytest.raises(AllocationModelError, match="observed 2"):
        assert_exactly_one_allocation(
            ["allocate_epmatwp", "allocate_epmatwp", "read_epmatwp"]
        )
    assert diagnose_path(
        ["allocate_epmatwp", "allocate_epmatwp", "read_epmatwp"]
    ) == "DOUBLE_ALLOCATION"


def test_mpi_dummy_extent_risk_is_separate_from_serial_cause() -> None:
    assert explicit_dummy_extent_risk(global_nrr_g=20, actual_fifth_extent=5) is True
    assert explicit_dummy_extent_risk(global_nrr_g=20, actual_fifth_extent=20) is False
    candidate = _audit()["candidate_causes"][3]
    assert candidate["candidate"] == (
        "MPI local fifth-dimension versus explicit dummy global bound mismatch"
    )
    assert candidate["assessment"] == "latent_separate_risk"
    assert candidate["causal_confidence"] == (
        "not_applicable_to_observed_serial_failure"
    )


def test_root_cause_ranking_is_not_overstated() -> None:
    causes = _audit()["candidate_causes"]
    assert [item["rank"] for item in causes] == [1, 2, 3, 4]
    assert causes[0]["candidate"] == "missing serial restart allocation of epmatwp"
    assert causes[0]["assessment"] == "supported"
    assert causes[0]["causal_confidence"] == "high"
    assert causes[1]["assessment"] == "unlikely_primary"
    assert causes[2]["assessment"] == "not_supported_as_observed_cause"


def test_inert_patch_moves_one_unchanged_allocation_above_mpi_split() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    allocation = (
        "ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)"
    )
    assert patch.count(f"+      {allocation}") == 1
    assert patch.count(f"-      {allocation}") == 1
    assert patch.index(f"+      {allocation}") < patch.index(" #if defined(__MPI)")
    assert "MPI_FILE_READ_AT_ALL" not in patch
    assert "epmatwp_offset" not in patch
    assert "lrepmatw =" not in patch
    assert "selfen" not in patch.lower()
    assert "This patch is an inert proposal" in patch
    assert "has not been compiled or run" in patch


def test_patch_proof_obligations_and_authorization_are_fail_closed() -> None:
    audit = _audit()
    patch = audit["minimal_patch_design"]
    assert patch["strategy"].startswith("Move the existing epmatwp allocation")
    assert patch["restart_format_changed"] is False
    assert patch["scientific_contraction_changed"] is False
    assert patch["file_io_layout_changed"] is False
    assert patch["executed"] is False
    obligations = audit["proof_obligations"]
    assert obligations["allocation_exactly_once"] == (
        "supported_by_static_patch_structure"
    )
    assert obligations["mpi_shape_unchanged"] == (
        "supported_by moving rather than changing the allocation expression"
    )
    assert obligations["runtime_success"] == "not_evaluated"
    authorization = audit["authorization"]
    for field in (
        "configure_or_build",
        "serial_execution",
        "mpi_execution",
        "patch_application_and_execution",
        "preparation_or_replay",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "automatic_executable_successor",
    ):
        assert authorization[field] is False


def test_documents_preserve_design_only_boundary() -> None:
    capability = CAPABILITY.read_text(encoding="utf-8")
    decision = DECISION.read_text(encoding="utf-8")
    state = STATE.read_text(encoding="utf-8")
    upstream = UPSTREAM.read_text(encoding="utf-8")
    assert "SOURCE_DIAGNOSIS_SUPPORTED" in capability
    assert "has not been compiled or executed" in capability
    assert "latent separate risk" in capability
    assert "patch execution                   not authorized" in decision
    assert "does not create or authorize" in decision
    assert "minimal patch validation\n  -> NOT AUTHORIZED" in state
    assert "proposed source change has not been compiled or executed" in upstream
    assert "not a claim of a validated fix" in upstream


def test_static_model_cannot_launch_or_apply_external_code() -> None:
    text = MODEL.read_text(encoding="utf-8")
    for forbidden in (
        "subprocess",
        "os.system",
        "Popen",
        "execv",
        "spawn",
        "requests",
        "urllib",
    ):
        assert forbidden not in text
