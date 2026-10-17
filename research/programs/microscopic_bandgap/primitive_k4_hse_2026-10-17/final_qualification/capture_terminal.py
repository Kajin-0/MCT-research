"""Archive already terminated evidence; queries only, never stops/unrefs units."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess

P = Path(__file__).resolve().parent
CASE = P.parent


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    frozen = json.loads((CASE/'preregistration.json').read_text())
    root = Path(frozen['root'])
    terminal = json.loads((root/'terminal_manager.json').read_text())
    manager = terminal['manager']
    assert manager['InvocationID'] == '8dee58502fd048e4bf30a09bd9053a1f'
    assert manager['SubState'] == 'exited' and manager['ExecMainStatus'] == '0'
    assert manager['MainPID'] == '0' and manager['NRestarts'] == '0'
    env = os.environ.copy()
    env.update(XDG_RUNTIME_DIR='/run/user/1001', DBUS_SESSION_BUS_ADDRESS='unix:path=/run/user/1001/bus')
    capture = dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), queries=[])
    for unit in [frozen['unit'], frozen['observer_unit']]:
        cmd = ['systemctl', '--user', 'show', unit, '-p', 'LoadState', '-p', 'ActiveState',
               '-p', 'SubState', '-p', 'MainPID', '-p', 'InvocationID', '-p', 'Result']
        res = subprocess.run(cmd, env=env, text=True, capture_output=True, timeout=15)
        props = dict(s.split('=', 1) for s in res.stdout.splitlines() if '=' in s)
        assert props.get('LoadState') == 'not-found' and props.get('MainPID') == '0'
        capture['queries'].append(dict(argv=cmd, returncode=res.returncode,
                                      stdout=res.stdout, stderr=res.stderr))
    cmd = ['journalctl', '--user', '-u', frozen['unit'], '-u', frozen['observer_unit'],
           '--since', '2026-10-17 01:34:20 UTC', '--until', '2026-10-17 03:26:00 UTC',
           '--no-pager', '-o', 'short-iso-precise']
    log = subprocess.run(cmd, env=env, text=True, capture_output=True, timeout=15)
    assert log.returncode == 0
    (P/'systemd_journal.txt').write_text(log.stdout)
    capture['queries'].append(dict(argv=cmd, returncode=log.returncode, stderr=log.stderr))

    initial = json.loads((CASE/'initial_live.json').read_text())['units']
    identities = []
    for info in initial.values():
        cg = Path('/sys/fs/cgroup'+info['ControlGroup'])
        assert not cg.exists()
        for proc in info['processes']:
            original = proc['stat'].split(') ', 1)[1].split()[19]
            path = Path('/proc')/str(proc['pid'])/'stat'
            now = path.read_text() if path.exists() else None
            same_start = now is not None and now.split(') ', 1)[1].split()[19] == original
            assert not same_start
            identities.append(dict(pid=proc['pid'], original_start_ticks=original,
                                   pid_present=now is not None, original_identity_gone=not same_start,
                                   original_cgroup=str(cg), original_cgroup_absent=not cg.exists()))
    capture['original_identities'] = identities
    capture['no_unit_or_process_mutation'] = True
    capture['no_new_science_jobs_or_native_actions'] = True

    destination = P/'native'
    destination.mkdir(exist_ok=True)
    files = [root/q for q in ['pw.in', 'pw.out', 'pw.err', 'observer.out', 'observer.err',
                              'resource_samples.jsonl', 'science_progress.json', 'terminal_manager.json']]
    files += [root/'out/r07pk4.save/data-file-schema.xml']
    pins = {}
    for source in files:
        name = source.name
        target = destination/name
        before = sha(source)
        if target.exists():
            assert sha(target) == before
        else:
            shutil.copyfile(source, target)
        assert sha(target) == before == sha(source)
        pins[str(source)] = dict(sha256=before, bytes=source.stat().st_size,
                                repository_copy=str(target.relative_to(P)))
    (P/'evidence_manifest.json').write_text(json.dumps(pins, indent=2)+'\n')
    rows = [json.loads(s) for s in (root/'resource_samples.jsonl').read_text().splitlines()]
    live = [r for r in rows if 'kernel' in r]
    events = sorted({r['kernel']['memory.events'] for r in live})
    resources = dict(elapsed_OS_wall_s=(int(manager['ExecMainExitTimestampMonotonic'])-
                                      int(manager['ExecMainStartTimestampMonotonic']))/1e6,
                     native_stdout_start_UTC='2026-10-17 01:34:29',
                     native_stdout_termination_UTC='2026-10-17 03:24:51',
                     terminal_observation_UTC=terminal['UTC'],
                     worker_InvocationID=manager['InvocationID'],
                     kernel_MemoryPeak_B=int(manager['MemoryPeak']),
                     kernel_MemorySwapPeak_B=int(manager['MemorySwapPeak']),
                     sampled_family_RSS_peak_B=max(r.get('family_RSS_B_shared_overcount', 0) for r in live),
                     RSS_shared_pages_overcount=True,
                     sampled_tasks_peak=max(int(r['kernel']['pids.current']) for r in live),
                     sampled_MemAvailable_min_B=min(r['host_available_B'] for r in rows),
                     sampled_disk_free_min_B=min(r['disk_free_B'] for r in rows),
                     sampled_owned_output_max_B=max(r['owned_sampled_B'] for r in rows),
                     memory_events_observed=events, samples=len(rows),
                     manager_success=True, native_restarts=0, native_cases=1,
                     worker_memory_cap_B=12*2**30, worker_swap_cap_B=0,
                     worker_tasks_cap=12, worker_wall_cap_s=86400, native_max_seconds=82800,
                     scientific_stop_requested=(root/'scientific_stop_request.json').exists(),
                     resource_refusal=(root/'resource_refusal.json').exists(),
                     native_EXIT_file=(root/'r07pk4.EXIT').exists(),
                     observer_stderr_bytes=(root/'observer.err').stat().st_size,
                     observer_kernel_peak='journal rounded 9.1M; exact terminal observer byte peak unavailable',
                     output_floors_sampled_not_continuous_or_quota=True)
    assert resources['kernel_MemoryPeak_B'] < 12*2**30
    assert resources['kernel_MemorySwapPeak_B'] == 0 and resources['sampled_tasks_peak'] <= 12
    assert resources['sampled_MemAvailable_min_B'] >= 4*2**30
    assert resources['sampled_disk_free_min_B'] >= 10*2**30
    assert resources['sampled_owned_output_max_B'] <= 14*2**30
    assert not resources['scientific_stop_requested'] and not resources['resource_refusal']
    (P/'resources.json').write_text(json.dumps(resources, indent=2)+'\n')
    (P/'cleanup.json').write_text(json.dumps(capture, indent=2)+'\n')
    print(json.dumps(resources, indent=2))


if __name__ == '__main__':
    main()
