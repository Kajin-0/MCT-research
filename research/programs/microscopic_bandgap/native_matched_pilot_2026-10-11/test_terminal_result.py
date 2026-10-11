"""Saved terminal and ownership checks; no QE launch or process mutation."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GIB = 1024**3


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def test_native_terminal_failure_and_conditional_Cd_rejection():
    result = json.loads((HERE/'host_result.json').read_text())
    audit = json.loads((HERE/'terminal_audit.json').read_text())
    gate = json.loads((HERE/'host_gate.json').read_text())
    assert gate == audit['gate']
    assert result['all_native_processes_terminated']
    assert result['inner_scf_converged'] and not result['exx_converged']
    assert result['final_reported_scf_accuracy_Ry'] > 1e-10
    assert not result['accepted_scf'] and not result['job_done']
    assert result['forced_termination'] and result['exit_requested']
    assert not gate['accepted_for_substitution'] and gate['Cd_stage'] == 'NOT_RUN'
    assert not audit['Cd_output_directory_exists']
    assert not audit['implicit_retry_authorized_by_RAM_recovery']
    assert gate['host_projector_irrep_and_1meV_gates'] == 'NOT_EVALUABLE'
    assert result['physical_xc'] is None


def test_telemetry_independently_identifies_RSS_not_time_disk_or_foreign_MPI():
    result = json.loads((HERE/'host_result.json').read_text())
    audit = json.loads((HERE/'terminal_audit.json').read_text())
    rows = [json.loads(line) for line in (HERE/'host_telemetry.jsonl').read_text().splitlines()]
    assert len(rows) == audit['telemetry_rows'] == 354
    assert all(b['elapsed_seconds']>a['elapsed_seconds'] for a,b in zip(rows, rows[1:]))
    last = rows[-1]
    assert last['RSS_bytes'] > result['process_family_RSS_limit_bytes']
    assert last['elapsed_seconds'] < 3600
    assert min(r['available_RAM_bytes'] for r in rows) == result['minimum_sampled_available_RAM_bytes'] > 2*GIB
    assert min(r['disk_free_bytes'] for r in rows) == result['minimum_sampled_disk_free_bytes'] > 8*GIB
    assert all(not r['foreign_MPI'] for r in rows)
    assert max(r['process_count'] for r in rows) == 7
    assert max(r['RSS_bytes'] for r in rows) <= result['measured_peak_process_family_RSS_bytes']
    assert not audit['sampled_peak_is_full_SCF_peak_bound']
    assert audit['last_sample_hard_stop_triggers'] == {
        'family_RSS':True, 'available_RAM_hard_floor':False, 'disk_hard_floor':False,
        'wall_hard_cap':False, 'foreign_MPI':False}


def test_terminal_byte_pins_sources_and_existing_supervisors_unchanged():
    audit = json.loads((HERE/'terminal_audit.json').read_text())
    native = Path(audit['native_run'])
    for name, expected in audit['record_sha256'].items():
        assert digest(native/name) == expected
    assert digest(HERE/'host_result.json') == audit['record_sha256']['result.json']
    assert digest(HERE/'host_telemetry.jsonl') == audit['record_sha256']['telemetry.jsonl']
    assert digest(HERE/'collect_terminal.py') == audit['driver_sha256']
    assert len(audit['source_and_supervisor_sha256_checked']) == 17
    for path, expected in audit['source_and_supervisor_sha256_checked'].items():
        assert digest(path) == expected
    assert audit['source_and_supervisor_mismatches'] == []
    assert audit['process_ownership_after_stop']['exclusive_MPI_snapshot']
    assert audit['process_ownership_after_stop']['exclusive_MPI_lock_acquired'] is False
