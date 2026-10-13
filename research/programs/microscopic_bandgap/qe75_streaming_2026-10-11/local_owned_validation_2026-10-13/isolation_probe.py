"""One fixed non-MPI namespace prerequisite; no arbitrary payload or launch API."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'cgroup_owned_2026-10-13'))
from contracts import (BASE, DFT, LOCK, REGISTRY, Refusal, atomic_json, cgroup_path,
                       counters, ctl, manager_env, memory, own_cgroup, proc, show)
PRIVATE = BASE / 'local_owned_mpi_20261013'
BINARY = PRIVATE / 'isolation_probe.v2'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fixed_command(unit):
    # No unrestricted command parameter. An unavailable namespace must fail,
    # not fall back to the host namespace. No inherited network socket is sent.
    properties = dict(Type='exec', MemoryMax=str(64 << 20), MemorySwapMax='0',
                      TasksMax='4', RuntimeMaxSec='8s', TimeoutStopSec='1s',
                      OOMPolicy='kill', KillMode='control-group', Delegate='no',
                      Restart='no', SendSIGKILL='yes', LimitFSIZE='16384', LimitCORE='0',
                      NoNewPrivileges='yes', PrivateUsers='yes', PrivateNetwork='yes',
                      RestrictAddressFamilies='AF_UNIX AF_INET AF_INET6 AF_NETLINK',
                      SystemCallArchitectures='native', WorkingDirectory=str(DFT),
                      UnsetEnvironment='LD_PRELOAD LD_AUDIT LD_LIBRARY_PATH PYTHONPATH PYTHONHOME')
    return ['/usr/bin/systemd-run', '--user', '--pipe', '--wait', '--quiet', '--unit='+unit,
            *['--property='+k+'='+v for k,v in properties.items()], str(BINARY)]


def run():
    PRIVATE.mkdir(exist_ok=True)
    root=PRIVATE / ('isolation-'+uuid.uuid4().hex); root.mkdir(mode=0o700)
    unit='r07-owned-'+uuid.uuid4().hex+'.service'
    pin=json.loads((PRIVATE/'isolation_build.v2.json').read_text())
    if pin['binary_sha256'] != sha(BINARY) or pin['source_sha256'] != sha(HERE/'isolation_probe.c'):
        raise Refusal('probe build/source fingerprint mismatch')
    legacy=REGISTRY.read_bytes()
    if json.loads(legacy)['phase']!='FINISHED': raise Refusal('legacy family not closed')
    if json.loads((BASE/'cgroup_owned_20261013/CURRENT_UNIT.json').read_text())['phase']!='FINISHED':
        raise Refusal('owned family not closed')
    lock=os.open(LOCK,os.O_RDWR|os.O_CLOEXEC)
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    client=None; identity=None; cg=None; samples=[]; out=bytearray(); fields={}
    started=time.monotonic(); host_ns=os.stat('/proc/self/ns/net').st_ino
    result=dict(kind='FIXED_NON_MPI_NAMESPACE_PREREQUISITE',unit=unit,root=str(root),
                command=fixed_command(unit),source_pin=pin,host_netns_inode=host_ns,
                native_MPI_launched=False,original_inventory_gate='UNPASSED')
    atomic_json(root/'intent.json',result)
    try:
        if memory()['MemAvailable']<4*(1<<30) or os.statvfs(PRIVATE).f_bavail*os.statvfs(PRIVATE).f_frsize<10*(1<<30):
            raise Refusal('host pressure headroom')
        if show(unit)['LoadState']!='not-found':raise Refusal('unit collision')
        client=subprocess.Popen(fixed_command(unit),env=manager_env(),stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        os.set_blocking(client.stdout.fileno(),False)
        sel=selectors.DefaultSelector();sel.register(client.stdout,selectors.EVENT_READ)
        while True:
            free=os.statvfs(PRIVATE);available=free.f_bavail*free.f_frsize
            mem=memory()['MemAvailable']
            if mem<4*(1<<30) or available<10*(1<<30):raise Refusal('host pressure changed')
            if time.monotonic()-started>10:raise Refusal('probe owner timeout')
            for _,_ in sel.select(.05):
                chunk=os.read(client.stdout.fileno(),4096)
                if chunk:out.extend(chunk)
                else:sel.unregister(client.stdout)
            if len(out)>16384:raise Refusal('probe output cap')
            f=show(unit)
            if f.get('MainPID','0')!='0' and f.get('ActiveState')=='active':
                pid=int(f['MainPID']);row=proc(pid)
                if identity is None:
                    identity=dict(pid=pid,start_ticks=row['start_ticks'],invocation=f['InvocationID'])
                    cg=cgroup_path(own_cgroup(pid))
                    if f['ControlGroup']!=own_cgroup(pid):raise Refusal('unit cgroup mismatch')
                if pid!=identity['pid'] or row['start_ticks']!=identity['start_ticks'] or f['InvocationID']!=identity['invocation']:
                    raise Refusal('unit identity changed')
                c=counters(cg)
                if (c['memory_max'],c['swap_max'],c['tasks_max'],c['oom_group'])!=('67108864','0','4','1'):
                    raise Refusal('kernel limits mismatch')
                samples.append(dict(elapsed=time.monotonic()-started,kernel=c,MemAvailable=mem,disk_free=available))
            if client.poll() is not None:
                # Drain after exit, bounded; manager metadata captured before reset.
                while True:
                    chunk=os.read(client.stdout.fileno(),4096)
                    if not chunk:break
                    out.extend(chunk)
                    if len(out)>16384:raise Refusal('probe output cap')
                fields=show(unit);break
        data=[json.loads(line) for line in out.decode(errors='replace').splitlines() if line.startswith('{')]
        obs=data[0] if len(data)==1 else None
        passed=(client.returncode==0 and obs is not None and 'failed_step' not in obs and identity is not None and
                obs['pid']==identity['pid'] and obs['uid']==1001 and obs['netns_inode']!=host_ns and
                obs['nonloop_addresses']==0 and obs['loop_addresses']>0 and obs['fsize']==16384 and obs['core']==0)
        result.update(passed=passed,exit_status=client.returncode,observation=obs,manager=fields,
                      identity=identity,samples=samples,stdout=out.decode(errors='replace'))
    except Exception as exc:
        result.update(passed=False,error=type(exc).__name__+': '+str(exc),stdout=out.decode(errors='replace'))
    finally:
        fields=show(unit)
        if fields['LoadState']!='not-found':
            if identity and fields.get('InvocationID')!=identity['invocation']:raise Refusal('cleanup identity mismatch')
            if fields.get('ActiveState') in ['active','activating','deactivating']:ctl(unit,'stop')
            terminal=show(unit)
            result['terminal_manager']=terminal
            if terminal.get('MainPID','0')!='0':raise Refusal('owned probe still alive')
            if cg and cg.exists() and (cg/'cgroup.events').read_text().find('populated 1')>=0:
                raise Refusal('owned probe cgroup still populated')
            atomic_json(root/'result.json',result)
            if terminal.get('ActiveState')=='failed':ctl(unit,'reset-failed')
        if client and client.poll() is None:client.wait(timeout=3)
        result['unit_unloaded']=show(unit)['LoadState']=='not-found'
        result['legacy_byte_exact']=REGISTRY.read_bytes()==legacy
        result['elapsed_seconds']=time.monotonic()-started
        atomic_json(root/'result.json',result)
        os.close(lock)
    return result


if __name__=='__main__':
    result=run(); print(json.dumps(result,indent=2));sys.exit(0 if result['passed'] else 2)
