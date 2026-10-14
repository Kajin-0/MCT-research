"""ONE bounded non-MPI owner proof sequence, then one nonzero-exit control.

No QE/mpi, /proc scan, foreign signal, service modification or historical write.
Real sockets/pidfds/owned user cgroups; injected failures labelled separately.
"""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import select
import socket
import subprocess
import sys
import time
import uuid
from unittest.mock import patch

import retirement as rt
from contracts import manager_env, show, ctl, own_cgroup, counters, members
from family_runtime import LOCK, REGISTRY, memory

HERE = Path(__file__).resolve().parent
DFT = Path('/home/User/opencode_workspace/DFT')
ROOT = DFT / '.local/qe75_lowram_20261011/terminal_owner_repro_v2_20261014'
GIB = 1 << 30


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def refused(function, text=None):
    try:
        function()
    except (rt.Refusal, PermissionError) as e:
        if text is not None:
            assert text in str(e), (text, str(e))
        return dict(refused=True, reason=str(e))
    raise AssertionError('negative accepted')


def case(exitcode):
    unit = 'r07-owned-' + uuid.uuid4().hex + '.service'
    name = 'r07-retirement-' + uuid.uuid4().hex
    server = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    server.bind('\0' + name)
    server.listen(4)
    server.settimeout(4)
    root = ROOT / ('exit' + str(exitcode))
    root.mkdir(mode=0o700)
    props = dict(Type='exec', MemoryMax=str(128 << 20), MemorySwapMax='0', TasksMax='8',
        LimitFSIZE='65536', LimitCORE='0', OOMPolicy='kill', KillMode='control-group',
        Delegate='no', Restart='no', RuntimeMaxSec='12s', TimeoutStopSec='1s',
        NoNewPrivileges='yes', WorkingDirectory=str(root))
    cmd = ['/usr/bin/systemd-run', '--user', '--pipe', '--wait', '--quiet', '--unit=' + unit]
    for k, v in props.items():
        cmd += ['--property=' + k + '=' + v]
    cmd += [str(Path(sys.executable).resolve()), str(HERE/'reproducer_worker.py'), 'parent', name, str(exitcode)]
    started = time.monotonic()
    child = subprocess.Popen(cmd, env=manager_env(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    record = dict(unit=unit, non_MPI=True, source_sha256=sha(HERE/'reproducer_worker.py'),
        command=cmd, negatives={}, injected_failures={}, samples=[])
    registry = None
    sockets = []
    invocation = None
    try:
        parent, _ = server.accept()
        sockets.append(parent)
        parent.settimeout(4)
        assert parent.recv(128) == ('parent:' + str(exitcode)).encode()
        pid, uid, _ = __import__('struct').unpack('3i', parent.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
        f = show(unit)
        invocation = f['InvocationID']
        assert uid == os.getuid() and pid == int(f['MainPID'])
        assert f['ControlGroup'] == own_cgroup(pid) and f['ActiveState'] == 'active'
        registry = rt.Retirement(unit, invocation, f['ControlGroup'], 'a'*64, 'b'*64)
        initial = counters(registry.cg)
        assert initial['memory_max'] == str(128 << 20) and initial['swap_max'] == '0'
        assert initial['tasks_max'] == '8' and initial['oom_group'] == '1'
        record['kernel_initial'] = initial
        parent.send(b'bound')
        connections = {}
        for _ in (0, 1):
            conn, _ = server.accept()
            sockets.append(conn)
            conn.settimeout(4)
            message = conn.recv(128).decode()
            role, rank = message.split(':')
            rank = int(rank)
            assert role == 'rank' and rank not in connections
            registry.receipt(conn, rank, 1, 'a'*64, 'b'*64)
            connections[rank] = conn
            conn.send(b'bound')
        # Actual foreign kernel cgroup: fresh connection created by this outside owner.
        outside = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
        sockets.append(outside)
        outside.connect('\0' + name)
        foreign, _ = server.accept()
        sockets.append(foreign)
        record['negatives']['foreign_kernel_peer'] = refused(lambda: rt.Peer(foreign, os.getuid(), registry.cgroup), 'foreign')
        for rank in (0, 1):
            conn = connections[rank]
            assert conn.recv(128) == b'final'
            record['negatives']['fake_binding_rank' + str(rank)] = refused(lambda: registry.receipt(conn, rank, 10, 'c'*64, 'b'*64), 'typed')
            registry.receipt(conn, rank, 10, 'a'*64, 'b'*64)
            if rank == 0:
                record['negatives']['incomplete_final_pair'] = refused(lambda: registry.inventory_failure(registry.ranks[0].pid, PermissionError(13, 'probe')), 'before authenticated')
            conn.send(b'final-accepted')
        assert connections[0].recv(128) == b'live-fd-denial'
        assert connections[1].recv(128) == b'live-normal'
        denied = registry.ranks[0].pid
        try:
            list(Path(f'/proc/{denied}/fd').iterdir())
        except PermissionError as error:
            record['actual_live_EACCES'] = dict(errno=error.errno, pid=denied, pidfd_exit=registry.ranks[0].exited())
            record['negatives']['live_EACCES_after_both_final'] = refused(lambda: registry.inventory_failure(denied, error), 'STILL LIVE')
        else:
            raise AssertionError('own nondumpable actor did not reproduce actual EACCES')
        record['negatives']['missing_proc_while_live'] = refused(lambda: registry.inventory_failure(denied, FileNotFoundError(2, 'injected disappearance')), 'STILL LIVE')
        record['negatives']['unregistered_missing_task'] = refused(lambda: registry.inventory_failure(pid, FileNotFoundError(2, 'injected missing parent')), 'before authenticated')
        record['negatives']['incomplete_FDinfo'] = refused(lambda: registry.inventory_failure(denied, PermissionError(13, 'injected FDinfo denied')), 'STILL LIVE')
        record['negatives']['still_live_terminal'] = refused(lambda: registry.terminal(child), 'still live')
        # Explicit injection, not a claim that this host denied pidfd_open.
        with patch.object(rt.os, 'pidfd_open', side_effect=PermissionError(13, 'injected pidfd permission')):
            record['injected_failures']['pidfd_open_denied'] = refused(lambda: rt.Peer(connections[1], os.getuid(), registry.cgroup))
        with patch.object(rt, 'proc', side_effect=lambda p: dict(pid=p, start_ticks=-1)):
            record['injected_failures']['stale_reused_PID_identity'] = refused(lambda: registry.ranks[1].live_identity(), 'replaced')
        # Real FD retargeting counterexample; never redirect the registry's pidfds.
        shadow = rt.Peer(connections[1], os.getuid(), registry.cgroup)
        foreign_fd = os.pidfd_open(os.getpid(), 0)
        try:
            os.dup2(foreign_fd, shadow.fd)
            record['negatives']['descriptor_retargeted_to_foreign_live_task'] = refused(shadow.exited, 'descriptor reused')
        finally:
            os.close(foreign_fd)
            shadow.close()
        for conn in connections.values():
            conn.send(b'exit')
        deadline = time.monotonic() + 3
        while not all(p.exited() for p in registry.ranks.values()):
            assert time.monotonic() < deadline, 'actor exit deadline'
            time.sleep(.005)
        record['actual_unreaped_exit'] = [dict(pid=p.pid, poll_mask=rt.exit_events(p.fd), proc_state=rt.proc(p.pid)['state']) for p in registry.ranks.values()]
        try:
            registry.inventory_failure(denied, PermissionError(13, 'injected post-exit FD denial'))
        except rt.TerminalPending as e:
            record['terminal_pending_is_not_omission'] = str(e)
        else:
            raise AssertionError('pending transition failed')
        record['negatives']['exited_ranks_but_parent_group_live'] = refused(lambda: registry.terminal(child), 'manager')
        parent.send(b'reap')
        assert parent.recv(128) == b'reaped'
        while child.poll() is None:
            assert time.monotonic() - started < 10, 'outside hard deadline'
            mem = memory()['MemAvailable']
            disk = os.statvfs(root).f_bavail * os.statvfs(root).f_frsize
            if mem < 4*GIB or disk < 10*GIB:
                raise rt.Refusal('host resource floor')
            record['samples'].append(dict(MemAvailable=mem, disk=disk))
            time.sleep(.01)
        record['wait_client_returncode'] = child.returncode
        record['terminal_manager_while_RefUnit_held'] = show(unit)
        if exitcode == 0:
            record['valid_terminal_certificate'] = registry.terminal(child)
        else:
            record['negatives']['actual_nonzero_manager_exit'] = refused(lambda: registry.terminal(child), 'manager')
        record['pidfd_after_reap'] = [dict(pid=p.pid, poll_mask=rt.exit_events(p.fd)) for p in registry.ranks.values()]
        assert not registry.cg.exists() or not members(registry.cg)
        output = child.stdout.read(65537)
        assert len(output) <= 65536
        record['log'] = output.decode(errors='replace')
        record['elapsed_seconds'] = time.monotonic() - started
    finally:
        f = show(unit)
        if f['LoadState'] != 'not-found' and f['ActiveState'] not in ('inactive', 'failed'):
            if invocation and f['InvocationID'] == invocation:
                ctl(unit, 'stop')
            else:
                raise rt.Refusal('cannot stop unbound fixture unit')
        child.wait(timeout=3)
        if registry is not None:
            assert not registry.cg.exists() or not members(registry.cg)
            if show(unit)['ActiveState'] == 'failed':
                ctl(unit, 'reset-failed')
            registry.close()
        for s in sockets:
            s.close()
        server.close()
        deadline = time.monotonic() + 2
        while show(unit)['LoadState'] != 'not-found' and time.monotonic() < deadline:
            time.sleep(.02)
        record['own_unit_collected'] = show(unit)['LoadState'] == 'not-found'
        assert record['own_unit_collected']
    return record


def main():
    if ROOT.exists():
        raise rt.Refusal('fixed reproducer sequence already attempted; no rerun')
    if memory()['MemAvailable'] < 4*GIB or os.statvfs(DFT).f_bavail * os.statvfs(DFT).f_frsize < 10*GIB:
        raise rt.Refusal('preflight host floors')
    old = REGISTRY.read_bytes()
    assert json.loads(old)['phase'] == 'FINISHED'
    fd = os.open(LOCK, os.O_RDWR | os.O_NOFOLLOW)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    ROOT.mkdir(mode=0o700)
    result = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), kernel=os.uname().release,
        scope='bounded actual Linux non-MPI two-child retirement proof; no native pair', cases=[])
    try:
        result['cases'].append(case(0))
        result['cases'].append(case(2))
        result['passed'] = True
    except BaseException:
        import traceback
        result['passed'] = False
        result['first_failure'] = traceback.format_exc()
        raise
    finally:
        result['protected_old_registry_unchanged'] = REGISTRY.read_bytes() == old
        result['source_sha256'] = {p.name:sha(p) for p in [HERE/'retirement.py', HERE/'reproduce.py', HERE/'reproducer_worker.py']}
        (HERE/'reproducer_result.json').write_text(json.dumps(result, indent=2) + '\n')
        os.close(fd)
        print(json.dumps(dict(passed=result['passed'], cases=len(result['cases']), no_MPI=True), indent=2))


if __name__ == '__main__':
    main()
