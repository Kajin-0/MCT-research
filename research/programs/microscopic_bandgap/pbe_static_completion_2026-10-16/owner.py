"""New PBE-only OUTSIDE-family owner. Native release is NOT granted this phase.

The real production loop calls the exact Protocol/Account/Reader tested here.
No wrapper exec receipt, JOBDONE authority, caller boolean or fake-manager
mode. Native execution additionally needs a separately reviewed frozen release
and complete resource certificate; neither is manufactured by this module.
"""
from pathlib import Path
import fcntl
import hashlib
import importlib.util
import json
import os
import select
import socket
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3]
BASE=HERE.parent/'qe75_streaming_2026-10-11'
for folder in ['runtime_admission','checkpoint_phase','native_bridge','cgroup_owned_2026-10-13']:
    sys.path.insert(0,str(BASE/folder))
from protocol import Protocol,Refusal,Peer,kernel,sha,durable,GIB
from account import Account
from reader import inspect
from contracts import show,ctl,counters,cgroup_path,own_cgroup,manager_env
from family_runtime import LOCK,REGISTRY,LIB,memory
_s=importlib.util.spec_from_file_location('_r07_pbe_static_resources',HERE.parent/'static_environment_2026-10-15/environment_resource_guard.py')
_guard=importlib.util.module_from_spec(_s);_s.loader.exec_module(_guard)
LinuxGuard,admission,live_limits=_guard.LinuxGuard,_guard.admission,_guard.live_limits
PRIVATE=REPO/'.tmp/r07spc16';PAIR=PRIVATE/'jobs'
PENDING=PRIVATE/'PENDING_UNIT.json'
KIND='R07_PBE16_STATIC_NATIVE_COMPLETION_V2'


def digest(j):return hashlib.sha256(json.dumps(j,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def service(server,protocol):
    """Shared by production loop and compiled NON-MPI wire tests."""
    while select.select([server],[],[],0)[0]:
        conn,_=server.accept();protocol.accept(conn)


def make_protocol(root,job,profile,cgroup,invocation,pre_ack):
    return Protocol(root,job,profile,cgroup,invocation,inspect,pre_ack)


def sample_owned(protocol,accounts,active,identities,root):
    """Production accounting caller; no refusal can be caught and retropassed."""
    try:
        while True:
            protocol.live()
            if protocol.deadline is not None and time.monotonic()>=protocol.deadline:
                raise Refusal('3s terminal pending bound')
            try:
                parts=[a.sample(active if a.root==root else ()) for a in accounts]
                # Reservation allocation remains owned disk, even though the
                # inherited constituent account reports it separately.
                if sum(a['budget_charge_bytes']+a['escrow_blocks_bytes'] for a in parts)>14*GIB:
                    raise Refusal('aggregate output including escrow crossed')
                return parts
            except kernel.TerminalPending:
                active=[p for p in active if not identities[p].exited()]
    except Exception as e:protocol.fail(e)


def load(member):
    if member not in ['unshared','shared']:raise Refusal('fixed pair members only')
    # The present qualification file says NOT_GRANTED. Updating it to another
    # string cannot grant execution: a frozen separately reviewed profile,
    # sources, release hash AND complete resource certificate are also needed.
    release=json.loads((HERE/'execution_boundary.json').read_text())
    if release.get('status')!='SEPARATELY_REVIEWED_NATIVE_RELEASE':raise Refusal('no native execution release in this phase')
    frozen=json.loads((HERE/'frozen_execution.json').read_text())
    profile=frozen['profile'];job=frozen['jobs'][member]
    certificate=json.loads((HERE/'resource_certificate.json').read_text())
    if (sha(HERE/'frozen_execution.json')!=release['frozen_execution_sha256']
        or sha(HERE/'resource_certificate.json')!=release['resource_certificate_sha256']
        or certificate['kind']!='SOURCE_COMPLETE_STATIC_PAIR_ENVELOPE'
        or certificate['profile_sha256']!=digest(profile)
        or type(certificate['RAM_upper_B']) is not int or not 0<certificate['RAM_upper_B']<=12*GIB
        or not 0<certificate['wall_upper_s']<600
        or not 0<certificate['retained_output_upper_B']<=14*GIB
        or not 0<certificate['action_error_eV_per_member']<=.0005
        or certificate['frame_transport']!='BYTE_EXACT'):
        raise Refusal('resource/source release certificate absent/incompatible')
    if profile['kind']!=KIND or profile['limits']!=dict(memory_B=12*GIB,swap_B=0,tasks=12,wall_s=600,
        host_floor_B=4*GIB,disk_floor_B=10*GIB,output_B=14*GIB):raise Refusal('new exact PBE physical/resource domain')
    if job['profile_sha256']!=digest(profile):raise Refusal('PROFILE binding')
    expected=digest({k:v for k,v in job.items() if k!='job_sha256'})
    if job['job_sha256']!=expected or job['root']!=str(PAIR/member):raise Refusal('JOB/root binding')
    for p,h in profile['pins'].items():
        if sha(p)!=h:raise Refusal('pinned source/ELF/PP/input changed')
    return profile,job,Path(job['root'])


def run(member):
    """Implemented production path, NOT called or released in this assignment."""
    profile,job,root=load(member)
    if member=='shared':
        first=json.loads((PAIR/'unshared/OUTSIDE_FINAL.json').read_text())
        if not first.get('terminal') or not first.get('source_input_pass'):raise Refusal('qualified fresh first member missing')
        for p,h in first['pins'].items():
            if sha(p)!=h:raise Refusal('first member changed')
    address=str(root/'s')
    if len(address.encode())>107 or any((root/p).exists() for p in ['s','LIVE_FINAL.json','RESULT.json','OUTSIDE_FINAL.json','output.escrow']):
        raise Refusal('fresh short socket/state only; no retry')
    ledger=REGISTRY.read_bytes()
    j=json.loads(ledger)
    if j.get('phase')!='FINISHED' or j.get('members')!=[]:raise Refusal('protected old ledger not empty/finished')
    lock=os.open(LOCK,os.O_RDONLY|os.O_CLOEXEC);fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if PENDING.exists():raise Refusal('previous scoped unit lacks outside-holder signoff')
    guard=LinuxGuard(LIB);admission(guard.probe(root),[64*(1<<20)],14*GIB,memory()['MemAvailable'])
    escrow=os.open(root/'output.escrow',os.O_RDWR|os.O_CREAT|os.O_EXCL,0o600)
    try:os.posix_fallocate(escrow,0,64*(1<<20));os.fsync(escrow)
    finally:os.close(escrow)
    server=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);server.bind(address);server.listen(4);server.setblocking(False)
    env=manager_env();env.update(R07_STATIC_SOCKET=address,R07_STATIC_ROOT=str(root),
        R07_STATIC_OWNER=str(os.getpid()),R07_STATIC_OWNER_TICKS=str(kernel.proc(os.getpid())['start_ticks']),
        R07_STATIC_JOB=job['job_sha256'],R07_STATIC_PROFILE=job['profile_sha256'],R07_STATIC_NONCE=job['nonce'],
        R07_STATIC_LOCK=str(LOCK),TMPDIR=str(root/'tmp'),PMIX_SYSTEM_TMPDIR=str(root/'tmp'),
        PRTE_MCA_prte_tmpdir_base=str(root/'tmp'),OMPI_MCA_plm='isolated',OMPI_MCA_btl='self,sm',OMPI_MCA_pml='ob1')
    # INVOCATION_ID is assigned by systemd, not supplied by an arbitrary caller.
    # Native C uses it when R07_STATIC_INVOCATION is absent (compiled contract).
    env.pop('R07_STATIC_INVOCATION',None)
    props=dict(Type='exec',MemoryMax=str(12*GIB),MemorySwapMax='0',TasksMax='12',RuntimeMaxSec='600s',
        TimeoutStopSec='3s',OOMPolicy='kill',KillMode='control-group',Restart='no',Delegate='no',
        SendSIGKILL='yes',LimitFSIZE=str(GIB),LimitCORE='0',NoNewPrivileges='yes',Nice='10',
        CPUQuota='200%',CPUWeight='10',IOWeight='10',WorkingDirectory=str(root))
    command=['/usr/bin/systemd-run','--user','--pipe','--wait','--quiet','--unit='+job['unit']]
    for k,v in props.items():command+=['--property='+k+'='+v]
    # systemd-run forwards these explicitly to the managed MPI family.
    for k,v in env.items():
        if k.startswith(('R07_STATIC_','OMPI_MCA_','PMIX_','PRTE_')) or k in ['TMPDIR','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','PYTHONDONTWRITEBYTECODE']:
            command+=['--setenv='+k+'='+v]
    command += [profile['mpirun'],'--host','localhost:2','-np','2',*job['argv']['0']]
    log=open(root/'pw.out','xb',buffering=0);client=None;ref=None;protocol=None;ids={};start=time.monotonic();cg=None;logged=0;inv=None
    try:
        # Persist BEFORE creation. Crash/unknown cleanup cannot authorize the
        # next member through a released flock. The protected old ledger is
        # never changed. Unknown setup/manager remains BLOCKED, never retried.
        durable(PENDING,dict(job=job['job_sha256'],unit=job['unit'],owner=os.getpid()))
        client=subprocess.Popen(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # Pin our unreaped direct foreground child before the first poll.
        client_identity=kernel.os.pidfd_open(client.pid,0)
        deadline=start+5
        while True:
            fields=show(job['unit'])
            if fields.get('ActiveState')=='active':break
            if client.poll() is not None or time.monotonic()>=deadline:raise Refusal('owned unit setup incomplete')
            time.sleep(.01)
        ref=kernel.UnitReference(job['unit']);inv=fields['InvocationID'];cg=cgroup_path(fields['ControlGroup'])
        s=cg.stat();cg_identity=(s.st_dev,s.st_ino)
        if own_cgroup(os.getpid())==fields['ControlGroup']:raise Refusal('holder must remain outside family')
        for key,value in [('MemoryMax',12*GIB),('MemorySwapMax',0),('TasksMax',12),('LimitFSIZE',GIB)]:
            if int(fields.get(key,-1))!=value:raise Refusal('manager hard limit '+key)
        for key,value in [('Restart','no'),('Delegate','no'),('KillMode','control-group'),('OOMPolicy','kill')]:
            if fields.get(key)!=value:raise Refusal('manager lifecycle '+key)
        if fields.get('RuntimeMaxUSec') not in ['10min','600s']:raise Refusal('manager deadline')
        def resource_check():
            live_limits(guard.probe(root),memory()['MemAvailable'],rss[0],time.monotonic()-start)
            if cg.exists():
                c=counters(cg)
                if (c['memory_max'],c['swap_max'],c['tasks_max'],c['oom_group'])!=(str(12*GIB),'0','12','1'):
                    raise Refusal('kernel hard limit changed')
                if c['memory_events'].get('oom',0) or c['pids_events'].get('max',0):raise Refusal('kernel resource event')
                peaks['kernel_B']=max(peaks['kernel_B'],c['memory_peak'])
        protocol=make_protocol(root,job,profile,fields['ControlGroup'],inv,resource_check)
        accounts=[Account(PAIR/m,14*GIB,64*(1<<20),guard,protocol if m==member else None) for m in ['unshared','shared']]
        def drain():
            nonlocal logged
            while select.select([client.stdout],[],[],0)[0]:
                b=os.read(client.stdout.fileno(),65536)
                if not b:return
                logged+=len(b)
                if logged>4*(1<<20):raise Refusal('log output burst')
                log.write(b)
        peaks=dict(kernel_B=0,rss_B=0);rss=[0]
        while True:
            drain();service(server,protocol)
            if protocol.deadline is not None and time.monotonic()>=protocol.deadline:raise Refusal('3s terminal pending bound')
            active=[];rss[0]=0
            if cg.exists():
                if (cg.stat().st_dev,cg.stat().st_ino)!=cg_identity:raise Refusal('cgroup identity changed')
                if any(cg.glob('*/cgroup.procs')):raise Refusal('unexpected delegated descendants')
                for value in (cg/'cgroup.procs').read_text().split():
                    pid=int(value)
                    if pid not in ids:
                        # A failure before kernel identity is bound is fatal.
                        ids[pid]=PeerFromMembership(pid,fields['ControlGroup'])
                    i=ids[pid]
                    if i.exited():continue
                    row=i.live_identity();active.append(pid);rss[0]+=row['rss_bytes']
            peaks['rss_B']=max(peaks['rss_B'],rss[0]);resource_check()
            charges=sample_owned(protocol,accounts,active,ids,root)
            if client.poll() is not None:break
            time.sleep(.02)
        drain();log.flush();os.fsync(log.fileno())
        class PairAccount:
            def sample(self):
                values=[a.sample() for a in accounts]
                if sum(v['budget_charge_bytes']+v['escrow_blocks_bytes'] for v in values)>14*GIB:
                    raise Refusal('final aggregate output including escrow crossed')
        proof=protocol.terminal(client,job['unit'],cg_identity,PairAccount(),resource_check)
        if REGISTRY.read_bytes()!=ledger:raise Refusal('protected ledger changed')
        pins={str(root/p):sha(root/p) for p in ['pw.out','LIVE_FINAL.json','pilot/H.rank0','pilot/H.rank1']}
        durable(root/'OUTSIDE_FINAL.json',dict(proof,source_input_pass=True,pins=pins,peaks=peaks,
            numerical_2meV_error_certified=False,not_a_material_gap=True))
        PENDING.unlink() # only after the real terminal AND durable outside result
    except BaseException as e:
        if protocol:protocol.refused=str(e)
        # Never guess or signal a foreign process. Stop ONLY the retained bound
        # unit/invocation; setup before a retained reference remains a boundary.
        if ref is not None and inv is not None and show(job['unit']).get('InvocationID')==inv:
            ctl(job['unit'],'stop')
        raise
    finally:
        if client is not None:
            try:client.wait(timeout=3)
            except subprocess.TimeoutExpired:pass
        if protocol:protocol.close()
        if ref:ref.close()
        if 'client_identity' in locals():os.close(client_identity)
        for peer in ids.values():peer.close()
        log.close();server.close();os.close(lock)


class PeerFromMembership:
    """Known cgroup actor, without granting it a native-rank final receipt."""
    def __init__(self,pid,cgroup):
        before=kernel.proc(pid);self.fd=os.pidfd_open(pid,0)
        try:
            after=kernel.proc(pid)
            if before['start_ticks']!=after['start_ticks'] or kernel.own_cgroup(pid)!=cgroup or kernel.exit_events(self.fd):
                raise Refusal('cgroup actor identity acquisition raced')
            self.pid=pid;self.start_ticks=after['start_ticks'];self.cgroup=cgroup
            s=os.fstat(self.fd);self.fd_identity=(s.st_dev,s.st_ino)
        except BaseException:os.close(self.fd);raise
    exited=Peer.exited
    live_identity=Peer.live_identity
    close=Peer.close


if __name__=='__main__':
    raise SystemExit('No QE/MPI invocation is authorized by this implementation phase.')
