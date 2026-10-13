"""Read-only verification of the USER's completed native run. Never reruns MPI."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent
DFT = Path('/home/User/opencode_workspace/DFT')
PROBE = DFT / '.local/qe75_lowram_20261011/direct_local_probe_20261013'
UNIT = 'r07-direct-mpi-smoke-20261013.service'
INVOCATION = '4cb067dcd8614e6fa51ad6881168c2f8'
PINS = {
    'mpi_probe': 'b3b61b7ef1de2c928ba86949e252cfa1c5cccf3f4742875767d8e026cd29cadd',
    'mpi_probe.c': 'fc30a6357c7b0031b36584cc34a74da64db442c0f5886882d04932aa76c260ba',
}


def run(argv, env=None):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=10, env=env)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout


def verify(events):
    # Collection removes current unit properties. Only historical records with
    # the exact invocation are admissible; default not-found properties are NOT
    # the old service's limits or successful rank stdout.
    selected = [e for e in events if e.get('USER_UNIT') == UNIT
                and e.get('USER_INVOCATION_ID') == INVOCATION]
    starts = [e for e in selected if e.get('JOB_TYPE') == 'start'
              and e.get('JOB_RESULT') == 'done']
    finals = [e for e in selected if 'MEMORY_PEAK' in e]
    if len(starts) != 1 or len(finals) != 1:
        raise ValueError('exact single historical start/resource record required')
    a, b = starts[0], finals[0]
    for key in ['_BOOT_ID', '_MACHINE_ID', '_UID']:
        if a[key] != b[key]:
            raise ValueError('historical identity changed')
    if a['_UID'] != '1001' or b['MEMORY_SWAP_PEAK'] != '0':
        raise ValueError('owner/swap record mismatch')
    command = a['MESSAGE']
    for token in ['mpirun', '--host localhost:2', '-np 2', '/mpi_probe',
                  'OMPI_MCA_plm=isolated', 'OMPI_MCA_btl=self,sm', 'OMPI_MCA_pml=ob1']:
        if token not in command:
            raise ValueError('historical launcher command not corroborated: ' + token)
    elapsed = (int(b['__MONOTONIC_TIMESTAMP']) - int(a['__MONOTONIC_TIMESTAMP'])) / 1e6
    if not 0 < elapsed < 45:
        raise ValueError('historical interval outside scope')
    return dict(invocation=INVOCATION, unit=UNIT, journal_interval_seconds=elapsed,
                memory_peak_bytes=int(b['MEMORY_PEAK']), swap_peak_bytes=0,
                cpu_seconds=int(b['CPU_USAGE_NSEC']) / 1e9,
                boot_id=a['_BOOT_ID'], started_realtime_us=int(a['__REALTIME_TIMESTAMP']))


def main():
    observed = {}
    for name, expected in PINS.items():
        p = PROBE / name
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if p.is_symlink() or actual != expected:
            raise RuntimeError('user-reported artifact pin mismatch: ' + name)
        observed[name] = dict(path=str(p), sha256=actual)
    events = [json.loads(s) for s in run([
        'journalctl', '--user', '-u', UNIT, '--no-pager', '-o', 'json']).splitlines()]
    historical = verify(events)
    env = dict(os.environ, XDG_RUNTIME_DIR='/run/user/1001',
               DBUS_SESSION_BUS_ADDRESS='unix:path=/run/user/1001/bus')
    current = run(['systemctl', '--user', 'show', UNIT, '-p', 'LoadState',
                   '-p', 'ActiveState', '-p', 'InvocationID'], env)
    report = dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  verified_historical=historical, observed_artifacts=observed,
                  current_collected_unit=current,
                  user_reported_rank_output=dict(pids=[1841538, 1841539], sum=3,
                      gathered=[0, 1], invalid=0, persisted_stdout_recovered=False),
                  user_reported_limits=dict(memory_max_bytes=512*2**20,
                      swap_max_bytes=0, tasks_max=32, runtime_max_seconds=45,
                      historical_config_recovered=False),
                  interpretation='Native MPI run corroborated; rank values and hard limits user-reported. '
                    'Journal resource peak independently recovered. Not authenticated R07C/QE.',
                  hostwide_MPI_absence_proven=False, private_network_proven=False,
                  native_QE_EXX_equivalence_proven=False, MPI_reexecuted=False)
    (HERE / 'smoke_journal.json').write_text(json.dumps(events, indent=2) + '\n')
    (HERE / 'smoke_verification.json').write_text(json.dumps(report, indent=2) + '\n')
    (HERE / 'user_mpi_probe.c').write_bytes((PROBE / 'mpi_probe.c').read_bytes())
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
