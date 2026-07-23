from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXECUTION_CONTRACT = (
    ROOT / "first_principles/b0/r02_epw_direct_fixture_execution_contract.json"
)
ANALYSIS_CONTRACT = (
    ROOT / "first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
)
DESIGN_CONTRACT = (
    ROOT / "first_principles/b0/r02_epw_direct_fixture_design_contract.json"
)
DRIVER = ROOT / "tools/run_epw_direct_fixture_ci.sh"
PATCH = ROOT / "patches/qe76-epw61-r02-raw-vertex-export.patch"
ANALYZER = ROOT / "tools/analyze_epw_raw_vertex_fixture.py"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_execution_contract_is_one_pinned_nonpolar_fixture() -> None:
    contract = _json(EXECUTION_CONTRACT)
    assert contract["stage"] == "B0_epw_direct_fixture_execution"
    assert contract["issue"] == 313
    assert contract["design_issue"] == 309
    assert contract["design_merge_commit"] == (
        "cd87a414b645a773724ffde9699695954aad36ed"
    )
    assert contract["phase"] == "one_pinned_execution"
    assert contract["source"]["commit_sha"] == (
        "9f93ddec427d2b9a45bb72d828c6d324f62fcabd"
    )
    assert contract["source"]["source_tree_archive_sha256"] == (
        "34ab80c2ed8a0e30d1aef01ac847c68106c8c2b7f7eaf8e05ecafbbcbac849"
    )
    fixture = contract["fixture"]
    assert fixture["material"] == "diamond"
    assert fixture["material_role"] == "upstream_nonpolar_software_fixture_only"
    assert fixture["long_range_included"] is False
    assert fixture["thermal_expansion_included"] is False
    assert fixture["testcode_used"] is False
    assert fixture["output_discovery_used"] is False
    assert fixture["outputs_opened_before_process_start"] is True


def test_authorization_is_exactly_one_build_and_two_sequences() -> None:
    authorization = _json(EXECUTION_CONTRACT)["authorization"]
    for field in (
        "source_clone_and_verify",
        "observational_patch_application",
        "exactly_one_pinned_build",
        "exactly_one_disabled_sequence",
        "exactly_one_enabled_sequence",
        "repository_analysis",
    ):
        assert authorization[field] is True
    for field in (
        "automatic_retry",
        "testcode_execution",
        "alternate_build",
        "parameter_sweep",
        "soc_fixture",
        "cdte_hgte_or_alloy_calculation",
        "a1_a2_a3",
        "automatic_phase_transition",
    ):
        assert authorization[field] is False


def test_execution_and_analysis_contracts_have_identical_thresholds() -> None:
    execution = _json(EXECUTION_CONTRACT)
    analysis = _json(ANALYSIS_CONTRACT)
    for key in (
        "exporter_enabled_disabled_standard_output_max_abs_ev",
        "normalization_identity_max_abs_ry2",
        "per_state_real_diagonal_max_abs_ev",
        "summed_real_diagonal_max_abs_ev",
        "synthetic_external_covariance_max_abs_ev",
        "q_weight_sum_max_abs",
    ):
        assert analysis["thresholds"][key] == execution["thresholds"][key]
    assert analysis["issue"] == 313
    assert analysis["phase"] == "fixture_execution"
    assert analysis["fixture"]["selected_export_window"]["ik_global"] == 1


def test_driver_preserves_upstream_relative_pseudopotential_path() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert 'DISABLED_FIXTURE="$WORK/qe/test-suite/r02_direct_disabled"' in text
    assert 'ENABLED_FIXTURE="$WORK/qe/test-suite/r02_direct_enabled"' in text
    assert 'cp -a "$WORK/qe/test-suite/epw_base" "$DISABLED_FIXTURE"' in text
    assert 'cp -a "$WORK/qe/test-suite/epw_base" "$ENABLED_FIXTURE"' in text
    assert 'local fixture="$DISABLED_FIXTURE"' not in text
    assert 'local fixture="$WORK/fixtures/$sequence"' not in text


def test_driver_opens_outputs_before_each_process_and_records_exit_code() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    stdout_open = text.index(
        "printf '# R02 direct fixture command=%s sequence=%s\\n' "
        '"$identifier" "$sequence" > "$stdout"'
    )
    stderr_open = text.index(
        "printf '# R02 direct fixture command=%s sequence=%s\\n' "
        '"$identifier" "$sequence" > "$stderr"'
    )
    process_launch = text.index('(cd "$fixture" && "$executable"')
    assert stdout_open < process_launch
    assert stderr_open < process_launch
    assert "local process_code=0" in text
    assert 'printf \'%s\\n\' "$process_code" > "$exit_code_path"' in text
    assert 'if (( process_code != 0 )); then' in text


def test_driver_has_exact_direct_sequence_and_no_testcode() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    expected = (
        'run_command "$sequence" "$fixture" 01 pw-scf "$PW_X" - -input scf.in',
        'run_command "$sequence" "$fixture" 02 ph "$PH_X" - -input ph.in',
        'run_command "$sequence" "$fixture" 03 pp "$PYTHON_X" pp.in "$EPW_BIN/pp.py"',
        'run_command "$sequence" "$fixture" 04 pw-scf-epw "$PW_X" - -input scf_epw.in',
        'run_command "$sequence" "$fixture" 05 pw-nscf-epw "$PW_X" - -input nscf_epw.in',
        'run_command "$sequence" "$fixture" 06 epw "$EPW_X" - -input epw1.in',
    )
    positions = [text.index(line) for line in expected]
    assert positions == sorted(positions)
    assert text.count("run_sequence disabled") == 1
    assert text.count("run_sequence enabled") == 1
    assert "run-custom-test" not in text
    assert "testcode.py" not in text
    assert "capture_epw_output" not in text
    assert "rglob(" not in text


def test_driver_has_one_build_no_retry_or_parameter_loop() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert text.count("./configure --disable-parallel --enable-openmp") == 1
    assert text.count("make -j2 pw ph epw") == 1
    assert text.count("build_count=1") == 1
    assert "while true" not in text.lower()
    assert "until " not in text.lower()
    assert "for cutoff" not in text
    assert "for kgrid" not in text
    assert "rerun" not in text.lower()
    assert "retry" not in text.lower()


def test_driver_enforces_command_and_evidence_counts() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert 'test "$sequence_count" -eq 2' in text
    assert 'test "$command_count" -eq 12' in text
    assert 'test "$OUTPUT_COUNT" -eq 24' in text
    assert 'test "$EXIT_COUNT" -eq 12' in text
    thresholds = _json(EXECUTION_CONTRACT)["thresholds"]
    assert thresholds["required_command_count"] == 12
    assert thresholds["required_output_file_count"] == 24
    assert thresholds["maximum_workflow_minutes"] == 120
    assert thresholds["maximum_evidence_bytes"] == 2_147_483_648


def test_enabled_export_is_explicit_and_disabled_sequence_unsets_it() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "export R02_EXPORT_RAW_VERTEX=1" in text
    assert "export R02_EXPORT_IK_GLOBAL=1" in text
    assert 'export R02_RAW_VERTEX_PATH="$EVIDENCE/raw/epw-raw-vertex.txt"' in text
    assert "unset R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH" in text
    assert 'test -s "$EVIDENCE/raw/epw-raw-vertex.txt"' in text


def test_patch_and_analyzer_remain_observational() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    analyzer = ANALYZER.read_text(encoding="utf-8")
    assert "r02_export_raw_vertex = .FALSE." in patch
    assert "epf17(jbnd, ibnd, imode, ik)" in patch
    assert "r02_real_increment = g2 * weight" in patch
    assert "MATMUL" not in patch
    assert "ibnd2" not in patch
    assert "fan_matrix" in analyzer
    assert "scalar_diagonal_reference" in analyzer
    assert '"automatic_followup_authorized": False' in analyzer


def test_design_contract_remains_the_controlling_command_manifest() -> None:
    design = _json(DESIGN_CONTRACT)
    execution = _json(EXECUTION_CONTRACT)
    assert design["issue"] == 309
    assert design["phase"] == "design_only"
    assert execution["fixture"]["commands_per_sequence"] == len(
        design["command_sequence"]
    )
    assert [command["id"] for command in design["command_sequence"]] == [
        "pw_scf",
        "ph",
        "pp",
        "pw_scf_epw",
        "pw_nscf_epw",
        "epw",
    ]
