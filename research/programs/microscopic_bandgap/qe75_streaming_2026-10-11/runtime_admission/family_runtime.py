"""Bounded foreground family owner and cleanup monitor. NO QE/MPI launch gate passed.

All runnable tests use a fixed tiny fake launcher. A native job must be admitted
by the separate exact fixture preflight; this phase never issues that admission.
The cleanup monitor is an owned foreground child, not a detached supervisor.
"""
from __future__ import annotations
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import select
import signal
import socket
import struct
import subprocess
import sys
import time
import uuid

from process_identity import (Identity,Refusal,proc,table,descendants,pin_descendant,subreaper,
                              parent_death,reap,mpi_inventory)

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'native_bridge'))
from native_bundle import artifact_sha256
from checkpoint_capsule import read_meta,encode,no_symlink,sync_dir,durable_bytes,BASE
from resource_guard import LinuxGuard,admission,live_limits,integer,multiply,quota_headroom,round_blocks

PRIVATE=BASE/'qe75_lowram_20261011/runtime_admission'
LOCK=PRIVATE/'MPI_FAMILY.lock'
REGISTRY=PRIVATE/'CURRENT_FAMILY.json'
LIB=BASE/'qe75_lowram_20261011/checkpoint_phase/storage_guard.so'
SAMPLE_SECONDS=.02
TEARDOWN_SECONDS=3.


def atomic_json(path,value):
    path=Path(path);tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    durable_bytes(tmp,encode(value));os.replace(tmp,path);sync_dir(path.parent)


def memory():
    return {key:int(value.split()[0])*1024 for key,value in
            (line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())}


def exact_extent(shape):
    if len(shape)!=3: raise Refusal('rank extent needs R,band,q')
    result=16
    for value in shape:
        if integer(value)<=0: raise Refusal('nonpositive rank shape')
        result=multiply(result,value)
    return result


def create_fake_job(root,scenario='normal',wall=2.,rss_cap=256*(1<<20),fault=None):
    root=Path(root).absolute()
    if not root.is_relative_to(PRIVATE): raise Refusal('private runtime root required')
    no_symlink(root.parent);root.mkdir(mode=0o700,exist_ok=False)
    job={'version':1,'kind':'EXPLICIT_FAKE_WORKERS_NO_MPI','id':uuid.uuid4().hex,'uid':os.getuid(),
         'root':str(root),'rank_count':2,'rank_shapes':[[3,2,2],[3,2,2]],
         'rank_bytes':[192,192],'output_envelope_bytes':32768,
         'wall_seconds':wall,'rss_cap_bytes':rss_cap,'scenario':scenario,'fault':fault,
         'files':{str(p):artifact_sha256(p) for p in [HERE/'fake_launcher.py',HERE/'fake_worker.py',
               HERE/'exec_worker.py',HERE/'family_runtime.py',HERE/'process_identity.py',
               HERE/'runtime_client.py',Path(sys.executable).resolve(),LIB]}}
    durable_bytes(root/'JOB.json',encode(job))
    for name in ['scratch','out','logs']: (root/name).mkdir(mode=0o700)
    sync_dir(root);return job


def verify_job(root):
    root=Path(root).absolute();no_symlink(root)
    if not root.is_relative_to(PRIVATE): raise Refusal('project-local runtime job required')
    job=read_meta(root/'JOB.json')
    if job.get('version')!=1 or job.get('uid')!=os.getuid() or job.get('root')!=str(root):
        raise Refusal('job owner/version/path mismatch')
    if job['kind']!='EXPLICIT_FAKE_WORKERS_NO_MPI':
        # A Boolean or renamed kind cannot bypass the native diagnostics/readback
        # and certified extent/envelope gates; native admission is not issued.
        raise Refusal('native fixture BLOCKED: diagnostic/readback and certified layout gates incomplete')
    if job['rank_count']!=2 or len(job['rank_shapes'])!=2:
        raise Refusal('two ranks required')
    if [exact_extent(s) for s in job['rank_shapes']]!=job['rank_bytes']:
        raise Refusal('byte-checked rank extents mismatch')
    if job['rank_shapes']!=[[3,2,2],[3,2,2]] or job['output_envelope_bytes']!=32768:
        raise Refusal('fake fixture allocation/envelope cannot be enlarged')
    if not 0<job['wall_seconds']<=600 or not 0<integer(job['rss_cap_bytes'])<=12*(1<<30):
        raise Refusal('cannot weaken runtime limits')
    if job['scenario'] not in ['normal','hold','fail','detach','ignore_term','race_orphan']:
        raise Refusal('unregistered fake scenario')
    if job['fault'] not in [None,'mem','disk','probe','envelope']:
        raise Refusal('unregistered fake fault')
    required=[HERE/'fake_launcher.py',HERE/'fake_worker.py',HERE/'exec_worker.py',HERE/'family_runtime.py',
              HERE/'process_identity.py',HERE/'runtime_client.py',Path(sys.executable).resolve(),LIB]
    if set(job['files'])!=set(map(str,required)): raise Refusal('exact fake command/backend allowlist mismatch')
    for path,sha in job['files'].items():
        if artifact_sha256(Path(path))!=sha: raise Refusal('job source/backend changed')
    if (root/'LEASE_ENDPOINT.json').exists() or (root/'RESULT.json').exists():
        raise Refusal('run root cannot be reused/restarted')
    return job


class Family:
    def __init__(self,root):
        self.root=Path(root);self.job=verify_job(root);self.members={};self.ever={};self.ranks={}
        self.unresolved={}
        self.peak_rss=0;self.peak_pss=0;self.peak_shared_indicator=0
        self.minimum_available=2**63-1;self.minimum_disk=2**63-1
        self.max_output=0;self.samples=0;self.signals=[];self.reaped=[];self.pss_unavailable=0
        self.guard=LinuxGuard(LIB);self.start=time.monotonic();self.phase='SETUP';self.reservations=[]
        self.owner_identity=Identity(os.getppid())

    def discover(self):
        rows=table();owned=descendants(os.getpid(),rows)
        if len(owned)>64: raise Refusal('owned process count exceeds finite bound')
        self.unresolved={}
        for pid in owned:
            if pid in self.members and rows[pid]['start_ticks']!=self.members[pid].start_ticks:
                self.members.pop(pid).close() # retained pidfd is retired, never retarget it
            if pid not in self.members:
                try:
                    identity=pin_descendant(pid,os.getpid(),rows)
                    self.members[pid]=identity;self.ever[(pid,identity.start_ticks)]=identity.record()
                except (Refusal,FileNotFoundError,ProcessLookupError):
                    self.unresolved[pid]=rows[pid] # retry; unknown is never authority or verified cleanup
        return rows

    def alive(self): return [p for p in self.members.values() if p.live()]

    def output_bytes(self):
        seen=set();total=0
        prepaid={(row['dev'],row['inode']) for row in self.reservations}
        for path in self.root.rglob('*'):
            no_symlink(path)
            if path.is_file():
                st=path.stat();key=(st.st_dev,st.st_ino)
                if key not in seen and key not in prepaid: total+=st.st_blocks*512;seen.add(key)
        return total

    def measure(self,inject=True):
        self.discover();rss=0;pss=0
        # Include the foreground owner and guardian, as well as all workers.
        # The owner identity is separately pinned and is never signal authority.
        owner_row=self.owner_identity.row()
        if owner_row is None: raise Refusal('owner disappeared')
        for pid in [self.owner_identity.pid,os.getpid(),*self.members]:
            try:
                row=proc(pid)
                if row['state']=='Z': continue
                rss+=row['rss_bytes']
                try:
                    fields=Path(f'/proc/{pid}/smaps_rollup').read_text().splitlines()
                    pss+=sum(int(line.split()[1])*1024 for line in fields if line.startswith('Pss:'))
                except PermissionError: self.pss_unavailable+=1
            except (FileNotFoundError,ProcessLookupError): pass
        mem=memory()['MemAvailable'];info=self.guard.probe(self.root/'scratch')
        elapsed=time.monotonic()-self.start;output=self.output_bytes()
        self.peak_rss=max(self.peak_rss,rss);self.peak_pss=max(self.peak_pss,pss)
        self.peak_shared_indicator=max(self.peak_shared_indicator,max(0,rss-pss))
        self.minimum_available=min(self.minimum_available,mem)
        self.minimum_disk=min(self.minimum_disk,info['available_bytes']);self.max_output=max(self.max_output,output)
        self.samples+=1
        report={'monotonic':time.monotonic(),'elapsed_seconds':elapsed,'family_rss_bytes':rss,
                'family_pss_bytes':pss,'mem_available_bytes':mem,'disk_available_bytes':info['available_bytes'],
                'output_allocated_bytes':output,'members':[p.record() for p in self.alive()]}
        actual=dict(report)
        if inject and self.job['fault'] and self.phase=='RUNNING' and self.ranks:
            # Explicit synthetic predicate injection, never reported as native
            # physical resource data. Actual telemetry is retained above.
            if self.job['fault']=='mem': mem=4*(1<<30)-1
            if self.job['fault']=='disk': info=dict(info,available_bytes=10*(1<<30)-1)
            if self.job['fault']=='probe': info=dict(info,probe_errno=5)
            if self.job['fault']=='envelope': output=self.job['output_envelope_bytes']+1
        live_limits(info,mem,rss,elapsed)
        if rss>self.job['rss_cap_bytes']: raise Refusal('stricter fake family RSS cap')
        if elapsed>=self.job['wall_seconds']: raise Refusal('monotonic wall cap')
        if output>self.job['output_envelope_bytes']: raise Refusal('output envelope exceeded')
        return actual

    def reserve(self):
        mem=memory()['MemAvailable'];info=self.guard.probe(self.root/'scratch')
        # Escrow itself AND future output budget are charged: never count one
        # preallocated inode as permission for unrelated additional native output.
        policy=admission(info,self.job['rank_bytes'],2*self.job['output_envelope_bytes'],mem)
        paths=[(self.root/'scratch'/f'rank{r}.stream',n) for r,n in enumerate(self.job['rank_bytes'])]
        paths.append((self.root/'scratch'/'output.escrow',self.job['output_envelope_bytes']))
        created=[]
        try:
            for path,size in paths:
                fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
                inode=os.fstat(fd).st_ino;created.append((path,fd,inode))
                for quota in self.guard.probe_fd(fd)['quotas']: quota_headroom(quota)
                allocated=ctypes.c_int64();code=self.guard.lib.qe_reserve_fd(fd,integer(size),ctypes.byref(allocated))
                if code: raise Refusal('fallocate errno='+str(code))
                if self.guard.probe(self.root/'scratch')['available_bytes']<10*(1<<30): raise Refusal('post-reservation disk floor')
                self.reservations.append({'path':str(path),'bytes':size,'allocated_bytes':allocated.value,
                                          'dev':os.fstat(fd).st_dev,'inode':inode})
            sync_dir(self.root/'scratch')
            return policy
        except BaseException:
            for path,fd,inode in created:
                if path.exists() and not path.is_symlink() and path.stat().st_ino==inode: path.unlink()
            sync_dir(self.root/'scratch');raise
        finally:
            for path,fd,inode in created: os.close(fd)

    def authorize(self,peer,payload):
        self.discover()
        if peer not in self.members or not self.members[peer].live(): raise Refusal('peer outside owned family')
        if payload.get('profile_sha256')!=hashlib.sha256(encode(self.job)).hexdigest(): raise Refusal('peer profile mismatch')
        command=Path(f'/proc/{peer}/cmdline').read_bytes().split(b'\0')
        if len(command)<2 or os.fsdecode(command[1])!=str(HERE/'fake_worker.py'):
            raise Refusal('peer is not the whitelisted worker')
        if artifact_sha256(Path(os.readlink(f'/proc/{peer}/exe')))!=self.job['files'][str(Path(sys.executable).resolve())]:
            raise Refusal('peer executable fingerprint mismatch')
        action=payload.get('action')
        if action=='register':
            rank=payload.get('rank')
            if type(rank) is not int or not 0<=rank<2 or payload.get('size')!=2:
                raise Refusal('rank/communicator mismatch')
            # Fake rank argument originates in a hashed fixed launcher. Native
            # registration will instead originate in compiled QE MPI state.
            if os.fsdecode(command[3])!=str(rank): raise Refusal('rank claim differs from launch argument')
            if rank in self.ranks and self.ranks[rank]!=self.members[peer].record(): raise Refusal('rank replacement refused')
            self.ranks[rank]=self.members[peer].record()
        elif action=='authorize':
            if set(self.ranks)!=set(range(2)): raise Refusal('all-rank registration incomplete')
            if any(not self.members[row['pid']].live() for row in self.ranks.values()): raise Refusal('registered rank died')
        else: raise Refusal('RPC action refused')
        measured=self.measure()
        return {'ok':True,**measured,'ranks':self.ranks,'guardian':{'pid':os.getpid(),'start_ticks':proc(os.getpid())['start_ticks']}}

    def teardown(self):
        started=time.monotonic();self.phase='TEARDOWN'
        while time.monotonic()-started<TEARDOWN_SECONDS:
            self.discover();self.reaped+=reap();alive=self.alive()
            if not alive and not self.unresolved: break
            number=signal.SIGTERM if time.monotonic()-started<.2 else signal.SIGKILL
            for identity in alive:
                identity.send(number);self.signals.append({**identity.record(),'signal':number})
            time.sleep(.02)
        self.discover();self.reaped+=reap()
        return [p.record() for p in self.alive()]+[
                {'pid':row['pid'],'start_ticks':row['start_ticks'],'unresolved':True}
                for row in self.unresolved.values() if row['state']!='Z']


def stale_refusal():
    if REGISTRY.exists():
        old=read_meta(REGISTRY)
        if old.get('phase')!='FINISHED':
            # A released kernel flock is not permission to overlap an orphaned
            # family after an unacknowledged owner+guardian crash.
            raise Refusal('previous family not durably closed; orphan/recovery boundary')
        for row in old.get('members',[]):
            try:
                current=proc(row['pid'])
                if current['start_ticks']==row['start_ticks'] and current['state']!='Z':
                    raise Refusal('retained orphan family still live; no new admission')
            except (FileNotFoundError,ProcessLookupError): pass
    foreign=mpi_inventory()
    if foreign: raise Refusal('preexisting MPI family: '+str([p['pid'] for p in foreign]))


def guardian(root,life_fd,parent_pid):
    stopped=[]
    for number in [signal.SIGTERM,signal.SIGINT]: signal.signal(number,lambda s,f:stopped.append(s))
    parent_death(signal.SIGTERM,parent_pid);subreaper()
    life=socket.socket(fileno=life_fd);life.setblocking(False)
    lease=os.open(LOCK,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    family=None;server=None;reason='PASS';survivors=[];launcher=None
    try:
        try: fcntl.flock(lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError as exc: raise Refusal('another family holds exclusive lease') from exc
        stale_refusal();family=Family(root)
        atomic_json(REGISTRY,{'version':1,'job':str(family.root),'members':[],'phase':'INITIALIZING',
                             'owner':{'pid':parent_pid,'start_ticks':proc(parent_pid)['start_ticks']}})
        family.reserve()
        # No subprocess inherits the lease FD; only this guardian owns it.
        server=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
        address='qe75-r07-'+family.job['id'];server.bind('\0'+address);server.listen(8)
        ticket={'version':1,'abstract_socket':address,'global_lock':str(LOCK),
                'profile_sha256':hashlib.sha256(encode(family.job)).hexdigest(),
                'guardian':{'pid':os.getpid(),'start_ticks':proc(os.getpid())['start_ticks']}}
        atomic_json(family.root/'LEASE_ENDPOINT.json',ticket)
        if stopped or os.getppid()!=parent_pid: raise Refusal('owner died before launcher creation')
        env=dict(os.environ,OMP_NUM_THREADS='1')
        out=open(family.root/'logs/worker.stdout','wb');err=open(family.root/'logs/worker.stderr','wb')
        command=[sys.executable,str(HERE/'exec_worker.py'),str(os.getpid()),sys.executable,
                 str(HERE/'fake_launcher.py'),str(family.root)]
        launcher=subprocess.Popen(command,stdout=out,stderr=err,env=env,process_group=0,close_fds=True)
        out.close();err.close();family.phase='RUNNING'
        leader=Identity(launcher.pid);family.members[launcher.pid]=leader
        family.ever[(launcher.pid,leader.start_ticks)]=leader.record()
        life.send(encode({'event':'READY',**ticket,'launch':leader.record()}))
        while True:
            if stopped: raise Refusal('owner cancellation/parent death')
            readable,_,_=select.select([life,server],[],[],SAMPLE_SECONDS)
            if life in readable:
                message=life.recv(65536)
                if not message: raise Refusal('owner lifeline closed')
                if json.loads(message).get('event')=='CANCEL': raise Refusal('owner cancellation')
            if server in readable:
                connection,_=server.accept();connection.settimeout(.25)
                payload={}
                try:
                    peer,uid,gid=struct.unpack('3i',connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
                    payload=json.loads(connection.recv(8192))
                    if uid!=os.getuid(): raise Refusal('foreign peer UID')
                    reply=family.authorize(peer,payload)
                except (Refusal,ValueError,OSError,KeyError,TypeError) as error:
                    reply={'ok':False,'reason':str(error)}
                reply['challenge']=payload.get('challenge')
                try: connection.send(encode(reply))
                except (BrokenPipeError,ConnectionResetError): pass
                connection.close()
            measured=family.measure()
            atomic_json(REGISTRY,{'version':1,'job':str(family.root),'guardian':ticket['guardian'],
                                  'members':measured['members'],'phase':'RUNNING',
                                  'owner':{'pid':parent_pid,'start_ticks':proc(parent_pid)['start_ticks']}})
            family.reaped+=reap()
            leader_row=leader.row()
            if leader_row is None or leader_row['state']=='Z':
                statuses=[row['status'] for row in family.reaped if row['pid']==launcher.pid]
                if not statuses or statuses[-1]!=0: raise Refusal('launcher/worker failure')
                if family.alive() or family.unresolved: raise Refusal('launcher exited with orphan/unresolved descendants')
                if set(family.ranks)!={0,1}: raise Refusal('all-rank registration absent at completion')
                break
    except BaseException as error: reason=str(error)
    finally:
        if family:
            survivors=family.teardown()
            result={'reason':reason,'passed':reason=='PASS' and not survivors,'survivors':survivors,
                    'rank_registration':family.ranks,'members':list(family.ever.values()),'signals':family.signals,
                    'reaped':family.reaped,'reservations':family.reservations,'samples':family.samples,
                    'peak_summed_RSS_bytes':family.peak_rss,'peak_summed_PSS_bytes':family.peak_pss,
                    'shared_RSS_overcount_indicator_bytes':family.peak_shared_indicator,
                    'PSS_unavailable_samples':family.pss_unavailable,'minimum_MemAvailable_bytes':family.minimum_available,
                    'minimum_free_disk_bytes':family.minimum_disk,'maximum_output_allocated_bytes':family.max_output,
                    'elapsed_seconds':time.monotonic()-family.start,'native_PW_MPI_executed':False}
            result['injected_predicate']=family.job['fault']
            result['resource_guard_semantics']='sampled stop predicates; not cgroup/continuous hard resource bounds'
            atomic_json(family.root/'RESULT.json',result)
            atomic_json(REGISTRY,{'version':1,'job':str(family.root),'members':survivors,'phase':'FINISHED' if not survivors else 'ORPHANED'})
            for identity in family.members.values(): identity.close()
            family.owner_identity.close()
        else:
            atomic_json(Path(root)/'RESULT.json',{'passed':False,'reason':reason,'survivors':[],
                                                 'native_PW_MPI_executed':False})
        if server: server.close()
        os.close(lease);life.close()


def owner(root):
    # A dedicated foreground process, with no preexisting children, may safely
    # adopt this guardian's descendants if the guardian itself dies.
    subreaper()
    if descendants(os.getpid(),table()): raise Refusal('owner must start without unrelated children')
    job=verify_job(root);parent,child=socket.socketpair(socket.AF_UNIX,socket.SOCK_SEQPACKET)
    child_fd=child.fileno();log=open(Path(root)/'logs/guardian.stderr','wb')
    command=[sys.executable,str(HERE/'family_runtime.py'),'guardian',str(root),str(child_fd),str(os.getpid())]
    monitor=subprocess.Popen(command,pass_fds=(child_fd,),stdout=log,stderr=log,close_fds=True)
    child.close();log.close();identity=Identity(monitor.pid);cancelled=[]
    for number in [signal.SIGTERM,signal.SIGINT]: signal.signal(number,lambda s,f:cancelled.append(s))
    started=time.monotonic();ready=None
    try:
        while identity.live():
            if cancelled:
                try: parent.send(encode({'event':'CANCEL'}))
                except (BrokenPipeError,ConnectionResetError): pass
                cancelled.clear()
            readable,_,_=select.select([parent],[],[],.05)
            if readable:
                payload=parent.recv(65536)
                if payload: ready=json.loads(payload)
            if time.monotonic()-started>job['wall_seconds']+TEARDOWN_SECONDS+2:
                identity.send(signal.SIGKILL);break
        monitor.wait(timeout=1)
        # Guardian crash fallback: all adopted direct children descend from the
        # one guardian spawned here. No PGID/argv/environment token is authority.
        deadline=time.monotonic()+TEARDOWN_SECONDS
        fallback={}
        while time.monotonic()<deadline:
            reap();rows=table();owned=descendants(os.getpid(),rows)
            unresolved=[]
            for pid in owned:
                if pid not in fallback:
                    try: fallback[pid]=pin_descendant(pid,os.getpid(),rows)
                    except (Refusal,FileNotFoundError,ProcessLookupError): unresolved.append(pid)
            alive=[p for p in fallback.values() if p.live()]
            if not alive and not unresolved: break
            for p in alive: p.send(signal.SIGKILL)
            time.sleep(.02)
        reap();survivors=[p.record() for p in fallback.values() if p.live()]
        # A racing/unpinned adopted process cannot be silently counted as gone.
        rows=table();reported={p['pid'] for p in survivors}
        for pid in descendants(os.getpid(),rows):
            if pid not in reported and rows[pid]['state']!='Z':
                survivors.append({'pid':pid,'start_ticks':rows[pid]['start_ticks'],'unresolved':True})
        for p in fallback.values(): p.close()
        if monitor.returncode or not (Path(root)/'RESULT.json').exists():
            atomic_json(Path(root)/'RESULT.json',{'passed':False,'reason':'guardian died; owner fallback',
              'survivors':survivors,'ready':ready,'native_PW_MPI_executed':False})
            # Only this old family's still-live owner can acknowledge its
            # verified cleanup. Do not overwrite a successor's registry.
            fd=os.open(LOCK,os.O_RDWR|os.O_NOFOLLOW)
            try:
                fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
                current=read_meta(REGISTRY)
                if current.get('job')!=str(root): raise Refusal('another registry replaced owned family')
                atomic_json(REGISTRY,{'version':1,'job':str(root),'members':survivors,
                                     'phase':'FINISHED' if not survivors else 'ORPHANED'})
            finally: os.close(fd)
        result=read_meta(Path(root)/'RESULT.json')
        if survivors: result.update(passed=False,survivors=survivors)
        return result
    finally:
        parent.close();identity.close()


if __name__=='__main__':
    if sys.argv[1]=='guardian': guardian(Path(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
    elif sys.argv[1]=='owner':
        outcome=owner(Path(sys.argv[2]));print(json.dumps(outcome));sys.exit(0 if outcome['passed'] else 2)
    else: raise Refusal('unsupported runtime entry')
