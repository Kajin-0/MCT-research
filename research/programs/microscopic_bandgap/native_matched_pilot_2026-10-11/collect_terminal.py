"""Archive the sole approved host result, read-only except new MCT files.

No launch, wait, signal, cleanup, native rewrite, goal or supervisor action.
Never overwrite a record. Native scratch and wavefunctions are not copied.
"""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil

HERE = Path(__file__).resolve().parent
RUN = Path('/home/User/opencode_workspace/DFT/calculations/r07/approved_pair_pilot_20261011T195000_scope52e7915/host')
GIB = 1024**3


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def collect():
    targets = ['host_result.json', 'host_telemetry.jsonl', 'host_gate.json',
               'host_stdout_excerpt.txt', 'terminal_audit.json']
    if any((HERE/name).exists() for name in targets):
        raise FileExistsError('Terminal record already present; do not overwrite')
    result = json.loads((RUN/'result.json').read_text())
    launch = json.loads((HERE/'host_launch_provenance.json').read_text())
    for key, value in launch.items():
        if result.get(key) != value:
            raise ValueError(f'Launch provenance changed: {key}')
    if not result['all_native_processes_terminated'] or result['accepted_scf']:
        raise ValueError('Collector only covers this terminal rejected host')
    if (RUN.parent/'impurity').exists():
        raise ValueError('Unexpected Cd stage')
    for name, field in [('pw.out', 'stdout_sha256'), ('pw.err', 'stderr_sha256'),
                        ('pw.in', 'input_sha256')]:
        if digest(RUN/name) != result[field]:
            raise ValueError(f'Native file changed: {name}')
    source_hashes = dict(result['source_and_supervisor_hashes'])
    original = json.loads((HERE/'preflight.json').read_text())
    # Original collector stores all source pins, not just host launch subset.
    for field in ('source_sha256', 'supervisor_sha256'):
        source_hashes.update(original.get(field, {}))
    mismatches = [p for p, h in source_hashes.items() if digest(p) != h]
    if mismatches:
        raise ValueError(f'Immutable source change: {mismatches}')
    rows = [json.loads(line) for line in (RUN/'telemetry.jsonl').read_text().splitlines()]
    last = rows[-1]
    triggers = {
        'family_RSS': last['RSS_bytes'] > result['process_family_RSS_limit_bytes'],
        'available_RAM_hard_floor': last['available_RAM_bytes'] < 2*GIB,
        'disk_hard_floor': last['disk_free_bytes'] < 4*GIB,
        'wall_hard_cap': last['elapsed_seconds'] > 5400,
        'foreign_MPI': bool(last['foreign_MPI']),
    }
    if triggers != dict.fromkeys(triggers, False) | {'family_RSS': True}:
        raise ValueError('Terminal telemetry does not isolate the RSS trigger')
    spec = importlib.util.spec_from_file_location('saved_preflight', HERE/'collect_preflight.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ownership = module.process_ownership()
    if not ownership['exclusive_MPI_snapshot']:
        raise ValueError('MPI/R07 driver remains; preserve but do not operate it')
    mem = module.parse_memory(Path('/proc/meminfo').read_text())
    text = (RUN/'pw.out').read_text()
    markers = [line.strip() for line in text.splitlines() if re.search(
        r'Program PWSCF|estimated scf accuracy|convergence has been achieved|EXX self-consistency reached|Using ACE|ACE projected|JOB DONE', line)]
    excerpt = '\n'.join(markers) + '\n\nFinal native stdout lines:\n' + '\n'.join(text.splitlines()[-18:]) + '\n'
    gate = {
        'decision': 'HOST_RESOURCE_STOP_CD_NOT_ADMITTED',
        'accepted_for_substitution': False,
        'host_native_SCF_gate': 'FAILED',
        'host_projector_irrep_and_1meV_gates': 'NOT_EVALUABLE',
        'Cd_stage': 'NOT_RUN',
        'new_native_restart_variant_or_retry_authorized': False,
        'physical_xc': None,
        'source_only_irrep_check_cannot_admit_this_host': True,
    }
    audit = {
        'collected_utc': datetime.now(timezone.utc).isoformat(),
        'driver_sha256': digest(__file__),
        'native_run': str(RUN),
        'record_sha256': {name: digest(RUN/name) for name in
                          ('result.json', 'provenance.json', 'telemetry.jsonl', 'process.json', 'pw.in', 'pw.out', 'pw.err')},
        'source_and_supervisor_sha256_checked': source_hashes,
        'source_and_supervisor_mismatches': mismatches,
        'process_ownership_after_stop': ownership,
        'memory_after_stop_bytes': mem,
        'disk_free_after_stop_bytes': shutil.disk_usage(RUN).free,
        'telemetry_rows': len(rows),
        'last_sample_hard_stop_triggers': triggers,
        'telemetry_maximum_RSS_bytes': max(r['RSS_bytes'] for r in rows),
        'monitored_family_peak_RSS_bytes': result['measured_peak_process_family_RSS_bytes'],
        'sampled_peak_is_full_SCF_peak_bound': False,
        'implicit_retry_authorized_by_RAM_recovery': False,
        'native_postprocessor_run': False,
        'Cd_output_directory_exists': False,
        'gate': gate,
    }
    shutil.copyfile(RUN/'result.json', HERE/'host_result.json')
    shutil.copyfile(RUN/'telemetry.jsonl', HERE/'host_telemetry.jsonl')
    (HERE/'host_stdout_excerpt.txt').write_text(excerpt)
    (HERE/'host_gate.json').write_text(json.dumps(gate, indent=2, sort_keys=True)+'\n')
    (HERE/'terminal_audit.json').write_text(json.dumps(audit, indent=2, sort_keys=True)+'\n')
    return {'decision': gate['decision'], 'hard_stop_triggers': triggers,
            'peak_family_RSS_GiB': result['measured_peak_process_family_RSS_bytes']/GIB,
            'sample_count': len(rows), 'source_pins_checked': len(source_hashes)}


if __name__ == '__main__':
    print(json.dumps(collect(), indent=2))
