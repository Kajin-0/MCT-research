from __future__ import annotations

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools/run_epw_same_state_attribution_ci.sh"
WORKFLOW = ROOT / ".github/workflows/r02-epw-same-state-execution.yml"


def test_driver_has_valid_bash_syntax() -> None:
    completed = subprocess.run(
        ["bash", "-n", str(DRIVER)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def test_driver_has_one_build_and_no_retry_path() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert text.count("./configure --disable-parallel --enable-openmp") == 1
    assert text.count("make -j2 pw ph epw") == 1
    assert text.count("build_count=1") == 1
    assert "while true" not in text.lower()
    assert "until " not in text.lower()
    assert "rerun" not in text.lower()
    assert 'assert auth["automatic_retry"] is False' in text
    assert 'assert auth["alternate_build"] is False' in text
    assert 'assert auth["parameter_sweep"] is False' in text


def test_driver_has_exact_preparation_sequence() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    expected = (
        'run_preparation_command 01 pw-scf "$PW_X" - -input scf.in',
        'run_preparation_command 02 ph "$PH_X" - -input ph.in',
        'run_preparation_command 03 pp "$PYTHON_X" pp.in "$EPW_BIN/pp.py"',
        'run_preparation_command 04 pw-scf-epw "$PW_X" - -input scf_epw.in',
        'run_preparation_command 05 pw-nscf-epw "$PW_X" - -input nscf_epw.in',
        'run_preparation_command 06 epw "$EPW_X" - -input epw1.in',
    )
    positions = [text.index(line) for line in expected]
    assert positions == sorted(positions)
    assert text.count("run_preparation_command 0") == 6
    assert 'test "$preparation_command_count" -eq 6' in text
    assert "unset R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH" in text


def test_driver_freezes_complete_tree_before_cloning() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    preparation_complete = text.index('test "$preparation_command_count" -eq 6')
    prepared_manifest = text.index('"$EVIDENCE/state/prepared-manifest.json"')
    clone_copy = text.index('cp -a "$PREPARATION_STATE" "$CLONE_ROOT/$replay"')
    first_replay = text.index("run_replay disabled_a")
    assert preparation_complete < prepared_manifest < clone_copy < first_replay
    assert "build_tree_manifest(root)" in text
    assert "require_paths(entries, contract[\"prepared_state\"][\"required_paths\"])" in text
    assert "assert_identical_manifests(manifests, clone_ids)" in text
    assert "rm -f \"$PREPARATION_STATE" not in text
    assert "find \"$PREPARATION_STATE\" -delete" not in text


def test_driver_has_exact_three_replays_and_no_fourth() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert text.count("run_replay disabled_a") == 1
    assert text.count("run_replay disabled_b") == 1
    assert text.count("run_replay enabled") == 1
    assert 'test "$replay_count" -eq 3' in text
    assert "disabled_c" not in text
    assert "replay_4" not in text
    assert 'export R02_EXPORT_RAW_VERTEX=1' in text
    assert 'export R02_EXPORT_IK_GLOBAL=1' in text
    assert 'export R02_RAW_VERTEX_PATH="$EVIDENCE/raw/epw-raw-vertex.txt"' in text


def test_process_streams_are_opened_outside_state_before_launch() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    prep_stdout = text.index('local stdout="$EVIDENCE/preparation/commands/')
    prep_open = text.index('> "$stdout"', prep_stdout)
    prep_launch = text.index('(cd "$PREPARATION_STATE" && "$executable"', prep_open)
    assert prep_stdout < prep_open < prep_launch

    replay_stdout = text.index('local stdout="$EVIDENCE/replays/$replay/epw.stdout.txt"')
    replay_open = text.index('> "$stdout"', replay_stdout)
    replay_launch = text.index('(cd "$state_dir" && "$EPW_X"', replay_open)
    assert replay_stdout < replay_open < replay_launch
    assert 'local state_dir="$CLONE_ROOT/$replay"' in text
    assert 'local stdout="$state_dir' not in text
    assert 'local stderr="$state_dir' not in text


def test_driver_compares_every_preexisting_file_after_replay() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert "pre_entries = [TreeEntry(**record) for record in pre_payload[\"files\"]]" in text
    assert "post_entries = build_tree_manifest(root / clone_id)" in text
    assert "compare_pre_post_manifests(pre_entries, post_entries, allowed)" in text
    assert '"replay_comparisons": comparisons' in text
    assert "output_removal_or_manifest_relaxation" in text


def test_driver_preserves_fixed_evidence_counts() -> None:
    text = DRIVER.read_text(encoding="utf-8")
    assert 'test "$PREP_STREAMS" -eq 12' in text
    assert 'test "$REPLAY_STREAMS" -eq 6' in text
    assert 'test "$EXIT_FILES" -eq 9' in text
    assert 'test -s "$EVIDENCE/raw/epw-raw-vertex.txt"' in text
    assert "--disabled-a-stdout" in text
    assert "--disabled-b-stdout" in text
    assert "--enabled-stdout" in text
    assert "--state-integrity" in text


def test_workflow_is_bounded_and_always_uploads_evidence() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "timeout-minutes: 120" in text
    assert "bash tools/run_epw_same_state_attribution_ci.sh" in text
    assert "if: always()" in text
    assert "r02-epw-same-state-evidence" in text
    assert "workflow_dispatch:" in text
    assert "cancel-in-progress: true" in text
