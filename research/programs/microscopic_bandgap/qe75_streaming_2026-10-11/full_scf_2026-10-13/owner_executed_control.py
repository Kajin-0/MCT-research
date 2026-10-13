"""Fixed Fock canonical-setup capture then ONE streamed first-ACE member; live UID/cgroup/lease/phase owner.

No original host-wide inventory or private-network claim. Nothing in a saved
JSON result or component-test Boolean authorizes a rank. Native stages require
kernel peers in this exact invocation and verified closed state/FFT/extent data.
"""
import ctypes
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import resource
import select
import shutil
import signal
import socket
import struct
import subprocess
import sys
import time
import uuid

HERE=Path(__file__).resolve().parent; BASE=HERE.parent
for name in ['cgroup_owned_2026-10-13','native_pair_2026-10-13','native_envelope_2026-10-13',
             'software_2026-10-13','runtime_admission','checkpoint_phase','m5_readiness','native_bridge']:
    sys.path.insert(0,str(BASE/name))
from contracts import manager_env,show,ctl,own_cgroup,cgroup_path,counters,members
from process_identity import Identity,proc,flock_owner,Refusal
from family_runtime import LOCK,REGISTRY as OLD_REGISTRY,LIB,memory,atomic_json
from resource_guard import LinuxGuard,admission,quota_headroom,multiply,integer
from common_state import decode as initial_decode,all_rank_certificate
from fft_descriptor import read as fft_read,compare as fft_compare
from compare_pair import compare as action_compare
from sampled_output import OutputAccount
import observables

DFT=Path('/home/User/opencode_workspace/DFT'); ROOT=DFT/'.local/qe75_lowram_20261011'
PRIVATE=ROOT/'full_scf_pair_v2_20261013'
SEED_CAPTURE_ROOT=ROOT/'first_ace_sampled_v6_20261013/control'
CONTROL_ROOT=PRIVATE/'control'; REFERENCE=ROOT/'hse_native_probe_20261013'
GIB=1<<30; MEMORY=12*GIB; AS=896*(1<<20); TASKS=12
OUTPUT=14*GIB; ESCROW=1*GIB; STREAM_MAX=[805306368]*2
REGISTRY=PRIVATE/'CURRENT_FAMILY.json'
REQUEST=struct.Struct('!4sIIII64s64s32s'); REPLY=struct.Struct('!4sIII32s')


def completed_native_retirement(mode,history,terminal,invocation,cgroup_exists):
    """Only recognize disappearance AFTER live all-rank completed numerics.
    Final log/empty-group/result acceptance is still mandatory in finally.
    This helper never grants a rank, lease, or skipped live-resource sample.
    """
    stage=10
    rows=[v for v in history if v['action']==stage]
    return (not cgroup_exists and len(rows)==2 and {v['rank'] for v in rows}=={0,1}
        and all(v['invocation']==invocation for v in rows)
        and terminal.get('InvocationID')==invocation
        and terminal.get('ActiveState') in ['failed','inactive']
        and terminal.get('Result')=='exit-code' and terminal.get('ExecMainStatus')=='0')


def atomic_large_json(path,value):
    payload=json.dumps(value,separators=(',',':'),sort_keys=True).encode()
    if len(payload)>32*(1<<20):raise Refusal('bounded pilot telemetry 32-MiB cap')
    path=Path(path);temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        with os.fdopen(fd,'wb') as f:f.write(payload);f.flush();os.fsync(f.fileno())
        os.replace(temp,path)
        directory=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(directory)
        finally:os.close(directory)
    except BaseException:
        if temp.exists():temp.unlink()
        raise


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda:f.read(1<<20),b''):h.update(x)
    return h.hexdigest()


def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def certificate(native_release=False):
    """Check the concrete bootstrap inputs, enforced caps and finite scope.

    AS bounds resident mappings, not an error-free /proc RSS theorem. Actual
    reported summed RSS is checked independently throughout. The disk contract
    uses a fixed first-ACE producer list and refuses any unexpected output.
    """
    build=json.loads((HERE/'build_results.json').read_text())
    if not build['passed']:raise Refusal('candidate compilation')
    for f,h in build['source_and_exchange_archive_pins'].items():
        if sha(f)!=h:raise Refusal('transport source or unchanged exchange archive pin')
    for c in build['candidates'].values():
        if sha(c['binary'])!=c['sha256']:raise Refusal('candidate ELF pin')
        for p,h in c['backends'].items():
            if sha(p)!=h:raise Refusal('backend pin')
    if build['candidates']['control']['backends']!=build['candidates']['stream']['backends']:
        raise Refusal('paired backends')
    evidence=json.loads((BASE/'native_first_ace_2026-10-13/reference_evidence.json').read_text())
    for name in ['pw.in','pw.out','result.json','manifest.json']:
        if sha(REFERENCE/name)!=evidence['hashes'][name]:raise Refusal('actual reference changed')
    # This is a real compatible 48-band state, not a relabelled 44-band save.
    seed=REFERENCE/'out/r07m4.save'
    names=['data-file-schema.xml','charge-density.hdf5','wfc1.hdf5','wfc2.hdf5','wfc3.hdf5']
    pins={n:sha(seed/n) for n in names}
    for s,h in evidence['current_PP_sha256'].items():
        if sha(DFT/'pseudopotentials'/(s+'_sg15_pbe_fr_v12.UPF'))!=h:raise Refusal('PP pin')
    info=LinuxGuard(LIB).probe(PRIVATE)
    policy=admission(info,STREAM_MAX,OUTPUT+ESCROW,memory()['MemAvailable'])
    # USER revised acceptance: sampled, risk-bounded LOCAL pilot only.
    # NOT an adversarial continuous bound or quota; never pass the original gate.
    if json.loads(OLD_REGISTRY.read_text())['phase']!='FINISHED':
        raise Refusal('protected prior family not finished')
    return_local_scope = 'R07_LOCAL_FULL_SCF_SCOPE5_20261013'
    return dict(candidates=build['candidates'],seed_sha256=pins,reference_seed=str(seed),
        PP=evidence['current_PP_sha256'],resource_policy=policy,
        resident_mapping_upper_bytes=TASKS*AS+832*(1<<20),
        reported_RSS_independent_sampled_guard=True,stock_peak_is_measurement_not_bound=True,
        bounded_fixture_only=True,physical_xc=False,
        producer_generation_bound_complete=False,native_release_issued=native_release,
        acceptance_scope=return_local_scope,sampled_disk_contract=True,
        residual_risk='producer bursts/external allocation between samples may cross the reserve before detection')


def prepare():
    PRIVATE.mkdir(mode=0o700,exist_ok=False)
    if REGISTRY.exists():raise Refusal('full SCF pair already prepared')
    cert=certificate(); atomic_json(PRIVATE/'CERTIFICATE.json',cert)
    atomic_json(REGISTRY,dict(phase='FINISHED',version=1))
    atomic_json(PRIVATE/'PROTECTED_LEDGER.json',dict(path=str(OLD_REGISTRY),sha256=sha(OLD_REGISTRY)))
    originals=(REFERENCE/'pw.in').read_text()
    common=digest(dict(physical_deck=originals.replace(str(REFERENCE/'out'),'OWNED_OUT').replace(str(DFT/'pseudopotentials'),'OWNED_PP').replace('420.0','480.0'),seed=cert['seed_sha256'],PP=cert['PP'],backends=cert['candidates']['control']['backends'],ranks=2))
    for mode,key in [('control','control'),('stream','stream')]:
        root=PRIVATE/mode;root.mkdir(mode=0o700)
        for n in ['out','initial','fft','diag','tmp','pp','trajectory']:(root/n).mkdir(mode=0o700)
        save=root/'out/r07m4.save';save.mkdir(mode=0o700)
        for species,h in cert['PP'].items():
            name=species+'_sg15_pbe_fr_v12.UPF';shutil.copy2(DFT/'pseudopotentials'/name,root/'pp'/name)
            if sha(root/'pp'/name)!=h:raise Refusal('private PP byte parity')
        for name,h in cert['seed_sha256'].items():
            shutil.copy2(Path(cert['reference_seed'])/name,save/name)
            if sha(save/name)!=h or (save/name).stat().st_nlink!=1:raise Refusal('private independent seed copy')
        deck=originals.replace(str(REFERENCE/'out'),str(root/'out')).replace('max_seconds = 420.0','max_seconds = 480.0')
        deck=deck.replace(str(DFT/'pseudopotentials'),str(root/'pp'))
        deck=deck.replace('&ELECTRONS\n',"&ELECTRONS\n startingwfc = 'file'\n startingpot = 'file'\n")
        (root/'pw.in').write_text(deck)
        profile=dict(kind='R07_LOCAL_QE_FULL_SCF_FRESH_V1',mode=mode,common_input_sha256=common,SCF_tolerances=observables.TOL,preregistration_sha256=sha(HERE/'preregistration.md'),
            binary_sha256=cert['candidates'][key]['sha256'],input_sha256=sha(root/'pw.in'),seed=cert['seed_sha256'],
            memory_max=MEMORY,swap_max=0,tasks_max=TASKS,per_process_AS=AS,wall_seconds=600,
            file_max=GIB,output_max=OUTPUT,disk_contract='sampled-retained-inodes-blocks-metadata-open-deleted',compiler_backends=cert['candidates'][key]['backends'])
        ph=digest(profile); ident=uuid.uuid4().hex
        command=[str((DFT/'.local/qe-env/bin/mpirun').resolve()),'--oversubscribe','--host','localhost:2','-np','2',
            cert['candidates'][key]['binary'],'-npool','1','-nb','1','-nt','1','-nd','1','-in',str(root/'pw.in')]
        safe_names={'PATH','HOME','USER','LOGNAME','LANG','LC_ALL','TZ','XDG_RUNTIME_DIR',
                    'DBUS_SESSION_BUS_ADDRESS','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS',
                    'MKL_NUM_THREADS','PYTHONDONTWRITEBYTECODE'}
        env={k:v for k,v in manager_env().items() if k in safe_names}
        env.update(OMPI_MCA_shmem_mmap_relocate_backing_file='1',
            OMPI_MCA_shmem_mmap_backing_file_base_dir=str(root/'tmp'),
            OMPI_MCA_plm='isolated',OMPI_MCA_btl='self,sm',OMPI_MCA_pml='ob1',
            TMPDIR=str(root/'tmp'),PMIX_SYSTEM_TMPDIR=str(root/'tmp'),PRTE_MCA_prte_tmpdir_base=str(root/'tmp'),
            OMPI_MCA_btl_sm_backing_directory=str(root/'tmp'),
            QE75_PROFILE_SHA256=ph,QE75_BRIDGE_FINGERPRINT=ph,QE75_COMMON_INPUT_SHA256=common,
            QE75_TRAJECTORY_ROOT=str(root/'trajectory'),
            QE75_INITIAL_ROOT=str(root/'initial'),QE75_RESOURCE_ROOT=str(root/'fft'),QE75_DIAG_ROOT=str(root/'diag'),
            QE75_LEASE_LOCK=str(LOCK))
        job=dict(version=1,kind=profile['kind'],mode=mode,unit='r07-owned-'+ident+'.service',
            profile_sha256=ph,root=str(root),command=command,environment=env,
            launch_pins={str(p):sha(p) for p in [Path(command[0]),Path(command[6]),root/'pw.in',HERE/'launcher_gate.py',HERE/'owned_pair.py',HERE/'sampled_output.py',HERE/'observables.py',HERE/'preregistration.md',*[root/'pp'/(species+'_sg15_pbe_fr_v12.UPF') for species in cert['PP']]]})
        atomic_json(root/'PROFILE.json',profile);atomic_json(root/'JOB.json',job)
    print('PREPARED full SCF pair: same physical input/48-band seed; no native process launched')


def initial_paths(root):return {(r,k):root/'initial'/f'rank{r}.k{k}.initial' for r in [0,1] for k in [1,2,3]}
def action_paths(root):return {(r,k,s):root/'diag'/f'rank{r}.k{k}.{name}' for r in [0,1] for k in [1,2,3] for s,name in [(1,'before'),(2,'after')]}


def reserve(path,size,guard):
    fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        for q in guard.probe_fd(fd)['quotas']:quota_headroom(q)
        allocated=ctypes.c_int64();err=guard.lib.qe_reserve_fd(fd,integer(size),ctypes.byref(allocated))
        if err:raise Refusal('actual reservation errno '+str(err))
        s=os.fstat(fd)
        if s.st_size!=size or s.st_nlink!=1 or allocated.value<size or s.st_uid!=os.getuid():raise Refusal('reservation readback')
        return dict(path=str(path),logical=size,allocated=allocated.value,dev=s.st_dev,inode=s.st_ino)
    finally:os.close(fd)


def run_member(mode):
    root=PRIVATE/mode; job=json.loads((root/'JOB.json').read_text());profile=json.loads((root/'PROFILE.json').read_text())
    if (root/'RESULT.json').exists() or (root/'ATTEMPT.json').exists():raise Refusal('one native member already attempted; no retry')
    if mode not in ['control','stream']:raise Refusal('full SCF mode')
    if profile['SCF_tolerances']!=observables.TOL or sha(HERE/'preregistration.md')!=profile['preregistration_sha256']:raise Refusal('preregistration changed')
    if mode=='stream':
        control=json.loads((CONTROL_ROOT/'RESULT.json').read_text())
        if not control['native_execution_complete'] or not control['owned_cgroup_empty']:raise Refusal('control native execution unqualified')
        if show(control['unit'])['LoadState']!='not-found':raise Refusal('control unit still loaded')
    try:cert=certificate(native_release=True)
    except Refusal as e:
        atomic_json(HERE/'native_release_refusal.json',dict(
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),reason=str(e),
            refusal_before_flock_registry_reservation_systemd_MPI=True,
            native_QE_MPI_started=False,source_candidate_not_native_qualified=True))
        raise
    if sha(OLD_REGISTRY)!=json.loads((PRIVATE/'PROTECTED_LEDGER.json').read_text())['sha256']:raise Refusal('protected old ledger changed')
    if digest(profile)!=job['profile_sha256']:raise Refusal('JOB/PROFILE')
    old=REGISTRY.read_bytes()
    if json.loads(old)['phase']!='FINISHED':raise Refusal('existing protected owner unfinished')
    lockfd=os.open(LOCK,os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(lockfd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if flock_owner(LOCK)!=[os.getpid()]:raise Refusal('live kernel lease')
    guard=LinuxGuard(LIB); escrow=reserve(root/'output.escrow',ESCROW,guard)
    jh=digest(job);ph=digest(profile);owner=Identity(os.getpid()); socket_id=uuid.uuid4().hex
    gate=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);gate.bind('\0r07-gate-'+socket_id);gate.listen(1);gate.settimeout(5)
    server=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET);server.bind('\0r07-native-'+socket_id);server.listen(8);server.setblocking(False)
    atomic_json(root/'OWNER.json',dict(pid=os.getpid(),gate_socket='r07-gate-'+socket_id,job_sha256=jh))
    # Native env changes are operational authorization, not PROFILE identity.
    env=job['environment']|dict(QE75_LEASE_SOCKET='r07-native-'+socket_id,QE75_JOB_SHA256=jh,
        QE75_LEASE_PID=str(os.getpid()),QE75_LEASE_TICKS=str(owner.start_ticks))
    job['environment']=env
    # The launch gate's JOB digest remains the sealed pre-authentication digest;
    # native requests carry that same digest. Operational endpoint fields are
    # added only to a separate fixed launch job, never an altered scientific ID.
    atomic_json(root/'JOB_LAUNCH.json',job)
    original_job=root/'JOB.json'; launch_path=root/'JOB_LAUNCH.json'
    props=dict(Type='exec',MemoryMax=str(MEMORY),MemorySwapMax='0',TasksMax=str(TASKS),
        LimitAS=str(AS),LimitFSIZE=str(GIB),LimitCORE='0',OOMPolicy='kill',KillMode='control-group',
        Delegate='no',Restart='no',RuntimeMaxSec='600s',TimeoutStopSec='1s',NoNewPrivileges='yes',
        WorkingDirectory=str(root))
    cmd=['/usr/bin/systemd-run','--user','--pipe','--wait','--quiet','--unit='+job['unit']]
    for k,v in props.items():cmd+=['--property='+k+'='+v]
    cmd += [str(Path(sys.executable).resolve()),str(HERE/'launcher_gate.py'),str(root)]
    atomic_json(REGISTRY,dict(phase='CGROUP_RUNNING',version=1,unit=job['unit'],job_sha256=jh,root=str(root)))
    atomic_json(root/'ATTEMPT.json',dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),unit=job['unit'],job_sha256=jh))
    started=time.monotonic(); child=subprocess.Popen(cmd,env=manager_env(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,close_fds=True)
    client_identity=Identity(child.pid)
    resource.prlimit(child.pid,resource.RLIMIT_AS,(64*(1<<20),64*(1<<20)))
    cg=None; invocation=None; ranks={};history=[];approved=set();identities={};pending=[];done=False;reason='';peak_rss=0;peak_pss=0;minmem=2**63;mindisk=2**63;last={}; reservations=[escrow];logged=0;kernel_samples=[]; account=OutputAccount(root,OUTPUT,ESCROW,guard)
    log=(root/'pw.out').open('xb'); cancelled=[]
    for sig in [signal.SIGTERM,signal.SIGINT]:signal.signal(sig,lambda s,f:cancelled.append(s))
    try:
        g,_=gate.accept()
        with g:
            pid,uid,_=struct.unpack('3i',g.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12));msg=json.loads(g.recv(4096))
            fields=show(job['unit']);invocation=fields['InvocationID']
            if uid!=os.getuid() or pid!=int(fields['MainPID']) or pid!=msg['pid'] or msg['job']!=jh:
                raise Refusal('actual unit/launcher kernel peer identity')
            if fields['ActiveState']!='active' or fields['ControlGroup']!=own_cgroup(pid):raise Refusal('owned cgroup identity')
            for key,value in [('MemoryMax',MEMORY),('MemorySwapMax',0),('TasksMax',TASKS),('LimitFSIZE',GIB)]:
                if int(fields[key])!=value:raise Refusal('kernel-manager hard limit '+key)
            cg=cgroup_path(fields['ControlGroup']);last=counters(cg)
            if resource.prlimit(pid,resource.RLIMIT_AS)[1]!=AS:raise Refusal('actual launcher hard AS')
            for key,value in [('memory_max',MEMORY),('swap_max',0),('tasks_max',TASKS),('oom_group',1)]:
                if int(last[key])!=value:raise Refusal('actual cgroup hard limit '+key)
            if fields['KillMode']!='control-group' or fields['Restart']!='no' or fields['RuntimeMaxUSec']!='10min':
                raise Refusal('manager lifecycle')
            atomic_json(root/'KERNEL_ADMISSION.json',dict(fields=fields,cgroup_inode=cg.stat().st_ino,kernel=last,lease_owner=owner.record()))
            identities[pid]=Identity(pid)
            g.send(json.dumps(dict(action='EXECUTE_PINNED_FIRST_ACE',challenge=msg['challenge'],job=jh)).encode())
        gate.close()
        while child.poll() is None:
            if cancelled or time.monotonic()-started>=600:raise Refusal('cancel/deadline')
            if cg.exists():
                rows=members(cg);rss=proc(os.getpid())['rss_bytes'];pss=0
                if client_identity.live():rss+=proc(child.pid)['rss_bytes']
                for pid,row in rows.items():
                    if row['state']=='Z':continue
                    rss+=row['rss_bytes']
                    if pid not in identities:identities[pid]=Identity(pid)
                    identity_row=identities[pid].row()
                    if identity_row is None or identity_row['state']=='Z':continue
                    try:actual_as=resource.prlimit(pid,resource.RLIMIT_AS)[1]
                    except ProcessLookupError:continue
                    if actual_as>AS:raise Refusal('inherited AS hard limit lost')
                    try:pss+=sum(int(l.split()[1])*1024 for l in Path(f'/proc/{pid}/smaps_rollup').read_text().splitlines() if l.startswith('Pss:'))
                    except (PermissionError,FileNotFoundError,ProcessLookupError):pass # PSS is diagnostic; retired peer is not a native failure.
                try:last=counters(cg)
                except FileNotFoundError:
                    if not cg.exists() and {v['rank'] for v in history if v['action']==10}=={0,1}:
                        try:child.wait(timeout=2)
                        except subprocess.TimeoutExpired:raise Refusal('completed group vanished but wait-client not terminal')
                        if child.returncode==0:break
                    if completed_native_retirement(mode,history,show(job['unit']),invocation,cg.exists()):break
                    raise # unreadable/incomplete/live counter inventory still refuses
                peak_rss=max(peak_rss,rss);peak_pss=max(peak_pss,pss)
                mem=memory()['MemAvailable'];info=guard.probe(root);minmem=min(minmem,mem);mindisk=min(mindisk,info['available_bytes'])
                if mem<4*GIB or info['available_bytes']<10*GIB or rss>MEMORY:raise Refusal('measured resource floor/cap')
                if any(last['memory_events'][k] for k in ['oom','oom_kill','max']) or last['pids_events'].get('max',0):raise Refusal('kernel pressure/limit event')
                usage=account.sample(rows)
                total=usage['budget_charge_bytes']
                if not kernel_samples or time.monotonic()-started-kernel_samples[-1]['elapsed']>=.25:kernel_samples.append(dict(elapsed=time.monotonic()-started,RSS=rss,MemAvailable=mem,disk=info['available_bytes'],output=total,output_account=usage,charged=last['memory_current']))
            ready,_,_=select.select([server,child.stdout],[],[],.02)
            if child.stdout in ready:
                b=os.read(child.stdout.fileno(),65536)
                if logged+len(b)>4*(1<<20):raise Refusal('hard bounded captured log sink')
                log.write(b);log.flush();logged+=len(b)
            if server in ready:
                c,_=server.accept();c.settimeout(.1);pid,uid,_=struct.unpack('3i',c.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12));raw=c.recv(181)
                if len(raw)!=REQUEST.size:raise Refusal('native wire extent')
                magic,version,action,rank,size,a,b,nonce=REQUEST.unpack(raw)
                if (magic,version,size)!=(b'R07L',1,2) or rank not in [0,1] or uid!=os.getuid() or (a.decode(),b.decode())!=(jh,ph):raise Refusal('native typed JOB/PROFILE/world')
                if pid not in rows or own_cgroup(pid)!=fields['ControlGroup']:raise Refusal('rank outside owned local cgroup')
                exe=Path(os.readlink(f'/proc/{pid}/exe')).resolve()
                if str(exe)!=job['command'][6] or sha(exe)!=profile['binary_sha256']:raise Refusal('actual native ELF')
                ident=identities[pid]
                if rank in ranks and ranks[rank].record()!=ident.record():raise Refusal('rank replacement')
                if any(r!=rank and v.pid==pid for r,v in ranks.items()):raise Refusal('rank spoof')
                argv=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
                if [os.fsdecode(v) for v in argv if v]!=job['command'][6:]:raise Refusal('actual rank argv mismatch')
                current=pid;seen=set()
                while current!=int(fields['MainPID']):
                    if current in seen or current not in rows:raise Refusal('owned launcher lineage incomplete')
                    seen.add(current);current=rows[current]['ppid']
                if action==1:ranks[rank]=ident
                if action!=1 and (set(ranks)!={0,1} or not all(i.live() for i in ranks.values())):raise Refusal('all real ranks not registered')
                if action not in [1,2,4,5,7,8,10]:raise Refusal('operation')
                pending.append((c,rank,pid,action,nonce))
            for entry in pending[:]:
                c,rank,pid,action,nonce=entry
                if action==1 and set(ranks)!={0,1}:continue
                occurrence=1+sum(v['action']==action and v['rank']==rank for v in history)
                key=(action,occurrence)
                if action in [4,5,7,8,10] and key not in approved:
                    if {v[1] for v in pending if v[3]==action}!={0,1}:continue
                    if action==4:
                        pp=initial_paths(root)
                        all_rank_certificate(pp,pp,profile['common_input_sha256'],[1,2,3])
                        reference=initial_paths(CONTROL_ROOT if mode=='stream' else SEED_CAPTURE_ROOT)
                        observation=observables.pair_states(reference,pp,initial=True)
                        atomic_json(root/'INITIAL_CERTIFICATE.json',observation)
                    elif action==5:
                        pp=[root/'fft'/f'rank{r}.fft' for r in [0,1]]
                        descriptors=[fft_read(p) for p in pp]
                        if any(d['scope']['nks']!=3 for d in descriptors):raise Refusal('actual k count')
                        if mode=='stream':fft_compare([CONTROL_ROOT/'fft'/f'rank{r}.fft' for r in [0,1]],pp,dict(stock=digest(json.loads((CONTROL_ROOT/'PROFILE.json').read_text())),stream=ph),profile['common_input_sha256'])
                        atomic_json(root/'FFT_CERTIFICATE.json',dict(descriptors=descriptors))
                    elif action==7:
                        if mode!='stream' or not 1<=occurrence<=20:raise Refusal('stream generation domain')
                        requests=[root/'out'/f'r07m4.stream_request.{occurrence}.{r}' for r in [0,1]]
                        descriptors=json.loads((root/'FFT_CERTIFICATE.json').read_text())['descriptors'];extents=[]
                        for r,p in enumerate(requests):
                            lines=p.read_text().splitlines();n=int(lines[1]);d=descriptors[r]
                            if len(lines)!=2 or lines[0]!=ph:raise Refusal('stream generation fingerprint')
                            unit=multiply(multiply(16*d['descriptors']['fock']['nnr'],d['scope']['npol']),d['scope']['nkqs'])
                            if n!=unit*48 or n>STREAM_MAX[r]:raise Refusal('exact 64bit full-SCF store extent')
                            if (root/'out'/f'r07m4.exx_qstream.{r}').exists():raise Refusal('old operator not retired; no overwrite')
                            extents.append(n)
                        admission(guard.probe(root),extents,OUTPUT,memory()['MemAvailable'])
                        current=[]
                        for r,n in enumerate(extents):current.append(reserve(root/'out'/f'r07m4.exx_qstream.{r}',n,guard))
                        reservations.extend(current);atomic_json(root/f'STREAM_RESERVED_{occurrence}.json',current)
                    elif action==8:
                        step=occurrence
                        match=CONTROL_ROOT if mode=='stream' and (CONTROL_ROOT/'trajectory'/f'rank0.step{step}.stage1.scalars').exists() else None
                        data=observables.step_certificate(root,step,1,match)
                        if data['scalar']['fingerprint']!=profile['common_input_sha256']:raise Refusal('native trajectory physical fingerprint')
                        atomic_json(root/f'STEP_{step}.json',data)
                    elif action==10:
                        endings=sorted((root/'trajectory').glob('rank0.step*.stage2.scalars'))
                        if len(endings)!=1:raise Refusal('exact final capture count')
                        step=int(endings[0].name.split('.step')[1].split('.')[0])
                        data=observables.step_certificate(root,step,2)
                        data['native_readback']=observables.final_readback(root,step)
                        atomic_json(root/'FINAL_CERTIFICATE.json',data);done=True
                    approved.add(key)
                c.send(REPLY.pack(b'R07L',1,0,5,nonce));c.close();pending.remove(entry)
                history.append(dict(rank=rank,pid=pid,action=action,occurrence=occurrence,cgroup=fields['ControlGroup'],invocation=invocation,job_sha256=jh,profile_sha256=ph))
        reason='FULL_SCF_NATIVE_RETURN' if done else 'native exited before complete post-punch evidence'
    except BaseException as e:
        import traceback
        reason=str(e)
        atomic_large_json(root/'ERROR_TRACE.json',dict(error=reason,traceback=traceback.format_exc(),receipts=history))
    finally:
        for c,*_ in pending:c.close()
        fields_now=show(job['unit'])
        if fields_now['LoadState']!='not-found' and fields_now['ActiveState'] not in ['inactive','failed']:
            if invocation and fields_now['InvocationID']==invocation:ctl(job['unit'],'stop')
            else:reason+='; unbound unit stop refused'
        try:child.wait(timeout=4)
        except subprocess.TimeoutExpired:reason+='; manager-client cleanup deadline'
        if child.poll() is not None:
            tail=child.stdout.read(4*(1<<20)-logged+1)
            if len(tail)+logged<=4*(1<<20):log.write(tail)
            else:reason+='; terminal log cap exceeded'
        terminal=show(job['unit']);empty=not cg or not cg.exists() or (not counters(cg)['cgroup_events']['populated'] and not members(cg))
        if empty and child.poll() is not None:
            if REGISTRY.exists() and json.loads(REGISTRY.read_text()).get('job_sha256')==jh:
                temporary=REGISTRY.with_name(REGISTRY.name+'.'+socket_id);temporary.write_bytes(old);os.replace(temporary,REGISTRY)
            if terminal['LoadState']=='loaded' and terminal['ActiveState']=='failed' and terminal['InvocationID']==invocation:ctl(job['unit'],'reset-failed')
            os.close(lockfd)
        completed_ranks={h['rank'] for h in history if h['action']==10}
        log.flush()
        exact_stop='JOB DONE.' in (root/'pw.out').read_text()
        terminal_match=child.returncode==0 and exact_stop
        result=dict(mode=mode,native_execution_complete=done and reason=='FULL_SCF_NATIVE_RETURN' and empty and completed_ranks=={0,1} and terminal_match,
            reason=reason,unit_returncode=child.returncode,manager_terminal=terminal,unit=job['unit'],invocation=invocation,
            elapsed_seconds=time.monotonic()-started,peak_family_RSS_bytes=peak_rss,peak_PSS_diagnostic_bytes=peak_pss,
            shared_RSS_overcount_included=True,minimum_MemAvailable_bytes=minmem,minimum_free_disk_bytes=mindisk,
            final_kernel=last,real_rank_receipts=history,reservations=reservations,owned_cgroup_empty=empty,
            native_convergence_not_yet_assessed=True,physical_xc=False,hostwide_exclusion_proven=False,
            acceptance_scope=cert['acceptance_scope'],sampled_disk_contract=True,
            between_sample_external_writer_and_burst_risk=True,
            output_maximum_sampled_charge_bytes=account.maximum,output_samples=account.samples,
            maximum_output_sample_gap_seconds=account.max_gap,
            actual_MPI_transient_tmpfs_inodes=account.shmem_seen,
            protected_old_ledger_unchanged=sha(OLD_REGISTRY)==json.loads((PRIVATE/'PROTECTED_LEDGER.json').read_text())['sha256'])
        atomic_json(root/'RESULT.json',result);atomic_large_json(root/'SAMPLES.json',kernel_samples)
        log.close();server.close();gate.close();owner.close();client_identity.close()
        for i in identities.values():i.close()
        print(json.dumps(result,indent=2))
    return result['native_execution_complete']


def main():
    if sys.argv[1:]==['prepare']:prepare();return
    if sys.argv[1:]!=['run']:raise Refusal('fixed prepare or ONE paired run only')
    # Bound the outside owner; apply after numpy/library startup, before IO.
    resource.setrlimit(resource.RLIMIT_AS,(768*(1<<20),768*(1<<20)))
    if not run_member('control'):raise SystemExit(1)
    if (PRIVATE/'control/output.escrow').exists():(PRIVATE/'control/output.escrow').unlink()
    if not run_member('stream'):raise SystemExit(1)


if __name__=='__main__':main()
