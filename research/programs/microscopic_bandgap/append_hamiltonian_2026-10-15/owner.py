"""Append-only same-D H query; accepted native binary, no arbitrary command interface.

Reuses tested kernel identity, storage and sampled accounting primitives. No
claim of original host-wide/bridge acceptance. All output is project local.
"""
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
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'qe75_streaming_2026-10-11'
DFT = Path('/home/User/opencode_workspace/DFT')
PAIR = DFT / '.local/qe75_lowram_20261011/h8h_20261015/p2'
QE = DFT / '.local/qe75_lowram_20261011/h8h_20261015/b3/pw.hse8.sameD'
MPI = DFT / '.local/qe-env/bin/mpirun'
for folder in ['runtime_admission', 'checkpoint_phase', 'native_bridge',
               'cgroup_owned_2026-10-13', 'terminal_owner_2026-10-14']:
    sys.path.insert(0, str(BASE / folder))
from contracts import manager_env, own_cgroup, cgroup_path, counters, members, show, ctl
from family_runtime import LOCK, REGISTRY, LIB, memory, atomic_json
from sameD_resource_guard import LinuxGuard, admission, live_limits
from process_identity import Identity, Refusal
from retirement import Peer, UnitReference, exit_events
from address_admission import checked_address, refuse_reuse
from sampled_output import SingleMemberAccount, OutputRefusal

GIB = 1 << 30


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def digest(j):
    return hashlib.sha256(json.dumps(j, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class Account(SingleMemberAccount):
    def permitted(self, path, kind):
        p = path.relative_to(self.root).parts
        if not p: return kind == 'directory'
        if len(p) == 1:
            if kind == 'directory': return p[0] in ['out', 'tmp', 'pp', 'pilot']
            if kind == 'socket': return p[0] == 's'
            return kind == 'regular' and (p[0].endswith('.json') or p[0].endswith('.jsonl') or p[0] in ['pw.in', 'pw.out', 'reference.bin', 'output.escrow', 'CRASH'])
        if p[0]=='pilot':
            import re
            return len(p)==2 and kind=='regular' and bool(re.fullmatch(r'(input|H)\.rank[01]',p[1]))
        if p[0] == 'tmp': return kind in ['directory', 'regular', 'socket', 'fifo']
        if p[0] == 'pp': return len(p) == 2 and kind == 'regular' and p[1] in [v + '_sg15_pbe_fr_v12.UPF' for v in ['Hg', 'Cd', 'Te']]
        if p[0] == 'out':
            return kind in ['regular', 'directory'] and (p[1] == 'r07hse8.save' or len(p) == 2 and p[1].startswith('r07hse8.'))
        return False


def prepare():
    from prepare import prepare
    prepare()


def load(member):
    if member not in ['host']: raise Refusal('fixed two-member allowlist')
    profile = json.loads((PAIR / 'PROFILE.json').read_text())
    job = json.loads((PAIR / member / 'JOB.json').read_text())
    frozen = json.loads((HERE / 'frozen_protocol.json').read_text())
    if profile != frozen['profile'] or job != frozen['jobs'][member] or digest(profile) != job['profile_sha256']:
        raise Refusal('prospective fixed profile/job changed')
    for p, h in profile['pins'].items():
        if sha(p) != h: raise Refusal('pinned input/ELF/source changed: ' + p)
    return profile, job, PAIR / member


def rank(member):
    profile, job, root = load(member)
    rank = int(os.environ['OMPI_COMM_WORLD_RANK'])
    if rank not in [0, 1] or os.environ['OMPI_COMM_WORLD_SIZE'] != '2': raise Refusal('actual MPI world')
    conn = socket.socket(socket.AF_UNIX)
    conn.settimeout(20)
    conn.connect(checked_address(root))
    conn.sendall(json.dumps(dict(rank=rank, nonce=job['nonce'], job=digest(job), profile=job['profile_sha256'], cgroup=own_cgroup(os.getpid()), elf=sha(QE))).encode()+b'\n')
    if conn.recv(128) != b'LIVE_SAME_D_APPEND_H_EXEC\n': raise Refusal('owner live lease refused')
    conn.close()
    os.execve(QE, [str(QE), '-npool', '1', '-nb', '1', '-nt', '1', '-nd', '1', '-in', str(root / 'pw.in')], dict(os.environ))


def guard(member):
    profile, job, root = load(member)
    l = profile['limits']; started = time.monotonic(); owner = os.getpid()
    lock = os.open(LOCK, os.O_RDONLY | os.O_CLOEXEC)
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    old = json.loads(REGISTRY.read_text())
    if old.get('phase') != 'FINISHED' or old.get('members') != []: raise Refusal('protected old ledger not finished/empty')
    fields = show(job['unit']); cgrel = own_cgroup(owner); cg = cgroup_path(cgrel)
    invocation = fields['InvocationID']
    for k, value in [('MemoryMax', l['memory']), ('MemorySwapMax', 0), ('TasksMax', 12), ('LimitFSIZE', GIB)]:
        if int(fields.get(k, -1)) != value: raise Refusal('manager resource mismatch ' + k)
    for k, value in [('ControlGroup', cgrel), ('KillMode', 'control-group'), ('OOMPolicy', 'kill'), ('Restart', 'no'), ('Delegate', 'no')]:
        if fields.get(k) != value: raise Refusal('manager lifecycle mismatch ' + k)
    c = counters(cg)
    if fields.get('RuntimeMaxUSec') not in ['10min', '600s']: raise Refusal('600-second manager deadline mismatch')
    if (cg/'cpu.max').read_text().strip()!='200000 100000' or (cg/'cpu.weight').read_text().strip()!='10':raise Refusal('bounded low-priority CPU controller mismatch')
    if (c['memory_max'], c['swap_max'], c['tasks_max'], c['oom_group']) != (str(l['memory']), '0', '12', '1'): raise Refusal('kernel limits mismatch')
    storage = LinuxGuard(LIB)
    info = storage.probe(root)
    admission(info, [l['escrow']], l['aggregate_output'], memory()['MemAvailable'])
    escrow = os.open(root/'output.escrow', os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
    os.posix_fallocate(escrow, 0, l['escrow']); os.fsync(escrow); os.close(escrow)
    atomic_json(root/'READY.json', dict(owner=owner, cgroup=cgrel, invocation=invocation, storage=info, manager=fields))
    while not (root/'REFERENCED.json').exists():
        if time.monotonic()-started > 15: raise Refusal('terminal manager reference absent')
        time.sleep(.05)
    server = socket.socket(socket.AF_UNIX); server.bind(checked_address(root)); server.listen(2); server.setblocking(False)
    env = manager_env()
    env.update(R07_FIRSTACE_ROOT=str(root),TMPDIR=str(root/'tmp'), PMIX_SYSTEM_TMPDIR=str(root/'tmp'), PRTE_MCA_prte_tmpdir_base=str(root/'tmp'),
               OMPI_MCA_plm='isolated', OMPI_MCA_btl='self,sm', OMPI_MCA_pml='ob1')
    output = open(root/'pw.out', 'xb', buffering=0)
    command = [str(MPI), '--host', 'localhost:2', '-np', '2', str(Path(sys.executable).resolve()), str(HERE/'owner.py'), 'rank', member]
    launcher = subprocess.Popen(command, env=env, stdout=output, stderr=subprocess.STDOUT, cwd=root)
    peers={}; conns={}; identities={}; stats=[]; error=None
    accounts=[Account(PAIR/m, l['aggregate_output'], l['escrow'], storage) for m in ['host']]
    atomic_json(root/'LAUNCH.json', dict(command=command, launcher=launcher.pid, profile=job['profile_sha256'], invocation=invocation))
    try:
        while launcher.poll() is None:
            if select.select([server],[],[],0)[0]:
                conn,_=server.accept(); conn.settimeout(5)
                peer=Peer(conn, os.getuid(), cgrel)
                data=b''
                while not data.endswith(b'\n') and len(data)<2048:
                    block=conn.recv(2048)
                    if not block: raise Refusal('incomplete live rank packet')
                    data+=block
                pkt=json.loads(data); r=pkt['rank']
                if r not in [0,1] or r in peers or pkt != dict(rank=r,nonce=job['nonce'],job=digest(job),profile=job['profile_sha256'],cgroup=cgrel,elf=sha(QE)):
                    peer.close(); conn.close(); raise Refusal('typed actual rank lease mismatch')
                peers[r]=peer; conns[r]=conn
                if len(peers)==2:
                    atomic_json(root/'RANKS.json', {str(r):dict(pid=p.pid,start_ticks=p.start_ticks,cgroup=p.cgroup) for r,p in peers.items()})
                    for s in conns.values(): s.sendall(b'LIVE_SAME_D_APPEND_H_EXEC\n'); s.close()
            if time.monotonic()-started > 30 and len(peers)!=2: raise Refusal('both real rank leases missing')
            now=members(cg)
            for pid,row in now.items():
                if pid not in identities: identities[pid]=Identity(pid)
                if identities[pid].start_ticks!=row['start_ticks']: raise Refusal('owned PID reuse')
            active=[]
            for pid in now:
                i=identities[pid]
                if not exit_events(i.fd): active.append(pid)
            rss=sum(row['rss_bytes'] for row in now.values()); mem=memory()['MemAvailable']; disk=storage.probe(root)
            live_limits(disk, mem, rss, time.monotonic()-started)
            c=counters(cg)
            if c['memory_events'].get('oom',0) or c['pids_events'].get('max',0): raise Refusal('kernel memory/tasks event')
            # Live inventory denial NEVER permits omission. A just-exited task
            # causes a pending sample; final terminal conjunction must resolve it.
            try:
                parts=[a.sample(active if a.root==root else ()) for a in accounts]
                charged=sum(a['budget_charge_bytes'] for a in parts)
            except (OutputRefusal, PermissionError, FileNotFoundError, ProcessLookupError):
                if not any(exit_events(identities[p].fd) for p in active): raise
                # Re-sample all still-live identities; removes only KERNEL exited.
                active=[p for p in active if not exit_events(identities[p].fd)]
                parts=[a.sample(active if a.root==root else ()) for a in accounts]
                charged=sum(a['budget_charge_bytes'] for a in parts)
            if charged>l['aggregate_output']: raise Refusal('sampled aggregate14GiB crossed')
            row=dict(elapsed_s=time.monotonic()-started,rss_shared_overcount_B=rss,host_available_B=mem,disk_available_B=disk['available_bytes'],output_charge_B=charged,kernel=c)
            stats.append(row)
            with open(root/'telemetry.jsonl','a') as log: log.write(json.dumps(row)+'\n')
            time.sleep(.25)
        if launcher.returncode!=0 or len(peers)!=2 or not all(p.exited() for p in peers.values()): raise Refusal('launcher/rank exit gate')
        # Launcher has reaped both ranks; all remaining FD inventories must be
        # readable. No phase10 assertion for unmodified stock QE.
        parts=[a.sample() for a in accounts]
        if sum(v['budget_charge_bytes'] for v in parts)>l['aggregate_output']: raise Refusal('final aggregate14GiB crossed')
    except BaseException as exc:
        error=repr(exc)
    finally:
        output.close(); server.close()
        atomic_json(root/'GUARD_RESULT.json', dict(pass_guard=error is None,error=error,elapsed_s=time.monotonic()-started,launcher_returncode=launcher.poll(),samples=len(stats),peak_sampled_RSS_B=max([r['rss_shared_overcount_B'] for r in stats],default=0),peak_kernel_memory_B=max([r['kernel']['memory_peak'] for r in stats],default=0),min_host_available_B=min([r['host_available_B'] for r in stats],default=0),min_free_disk_B=min([r['disk_available_B'] for r in stats],default=0),max_aggregate_output_B=max([r['output_charge_B'] for r in stats],default=0),rank_kernel_exits={str(r):p.exited() for r,p in peers.items()},invocation=invocation,cgroup=cgrel,sampled_not_continuous=True))
        for p in peers.values(): p.close()
        for i in identities.values(): i.close()
        os.close(lock)
    if error: raise Refusal(error)  # systemd kills only this owned control group


def launch(member):
    profile,job,root=load(member)
    checked_address(root)
    refuse_reuse(root)
    if (root/'LAUNCH.json').exists() or (root/'GUARD_RESULT.json').exists(): raise Refusal('no retries/reused state')
    props=dict(Type='exec',MemoryMax=str(12*GIB),MemorySwapMax='0',TasksMax='12',OOMPolicy='kill',KillMode='control-group',Delegate='no',Restart='no',SendSIGKILL='yes',RuntimeMaxSec='600s',TimeoutStopSec='3s',LimitFSIZE=str(GIB),LimitCORE='0',NoNewPrivileges='yes',Nice='10',CPUQuota='200%',CPUWeight='10',IOWeight='10',WorkingDirectory=str(DFT),UnsetEnvironment='LD_PRELOAD LD_AUDIT PYTHONHOME PYTHONPATH LD_LIBRARY_PATH')
    cmd=['/usr/bin/systemd-run','--user','--pipe','--wait','--quiet','--unit='+job['unit']]
    for k,v in props.items(): cmd+=['--property='+k+'='+v]
    cmd += ['--setenv=PYTHONDONTWRITEBYTECODE=1','--setenv=OMP_NUM_THREADS=1','--setenv=OPENBLAS_NUM_THREADS=1','--setenv=MKL_NUM_THREADS=1',str(Path(sys.executable).resolve()),str(HERE/'owner.py'),'guard',member]
    ref=None;client=subprocess.Popen(cmd,env=manager_env(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        start=time.monotonic()
        while not (root/'READY.json').exists():
            if client.poll() is not None: raise Refusal('guard setup failed before MPI: '+client.communicate()[1].decode())
            if time.monotonic()-start>15: raise Refusal('guard setup timeout')
            time.sleep(.05)
        ref=UnitReference(job['unit']);atomic_json(root/'REFERENCED.json',dict(reference=True))
        out,err=client.communicate(timeout=610)
        f=show(job['unit']);g=json.loads((root/'GUARD_RESULT.json').read_text()); cg=cgroup_path(g['cgroup'])
        terminal=(client.returncode==0 and g['pass_guard'] and f.get('InvocationID')==g['invocation'] and f.get('ActiveState')=='inactive' and f.get('Result')=='success' and f.get('ExecMainCode')=='1' and f.get('ExecMainStatus')=='0' and (not cg.exists() or not members(cg)))
        atomic_json(root/'TERMINAL.json',dict(manager=f,client_returncode=client.returncode,terminal=bool(terminal),stderr=err.decode()))
        from readback import validate_native
        science=validate_native(root)
        files=[root/'pw.in',root/'pw.out']+sorted((root/'pilot').glob('*.rank*'))
        result=dict(member=member,accepted=bool(terminal and science['scientific_pass']),terminal_pass=bool(terminal),scientific_pass=science['scientific_pass'],
                    SCF_performed=False,same_D_complete_H_operator=True,HSE_converged=False,physical_xc=None,science=science,guard=g,terminal_manager=f,client_returncode=client.returncode,
                    stderr=err.decode(),stdout=out.decode(),source_hashes={str(p):sha(p) for p in files})
        atomic_json(root/'FINAL.json',result);atomic_json(HERE/'native_result.json',result)
        print(json.dumps(result,indent=2),flush=True)
        if not result['accepted']:raise Refusal('fixed direct-Fock operator gate failed; no retry')
    except BaseException:
        # No foreign PID or guessed process group is ever signalled.
        ctl(job['unit'],'stop');raise
    finally:
        if ref: ref.close()


def np_array(s):
    import numpy as np
    return np.fromstring(s or '',sep=' ')


if __name__=='__main__':
    action=sys.argv[1]
    if action=='prepare': prepare()
    elif action=='launch': launch(sys.argv[2])
    elif action=='guard': guard(sys.argv[2])
    elif action=='rank': rank(sys.argv[2])
    else: raise Refusal('no arbitrary command action')
