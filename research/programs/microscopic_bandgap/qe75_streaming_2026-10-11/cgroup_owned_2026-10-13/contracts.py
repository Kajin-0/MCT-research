"""User-manager owned-family contracts. Native execution is NEVER issued here."""
from pathlib import Path
import fcntl
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import uuid

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
BASE=DFT/'.local/qe75_lowram_20261011'
PRIVATE=BASE/'cgroup_owned_20261013'
WORKER=PRIVATE/'rank_worker.v2'
sys.path.insert(0,str(HERE.parent/'m5_readiness'))
from binding import REQUEST,REPLY,MAGIC,VERSION,SCOPE_ABI_NO_MPI,digest
from family_runtime import LOCK,LIB,REGISTRY,atomic_json,memory,encode,integer,quota_headroom
from native_bundle import artifact_sha256
from process_identity import Identity,proc,pin_descendant,flock_owner,Refusal
from resource_guard import LinuxGuard,round_blocks

CGROOT=Path('/sys/fs/cgroup')
CASES={'normal','hold','log_flood','file_limit','task_limit','oom','guard_crash','orphan','native_scope'}
COMMON={'version':1,'kind':'R07_SYSTEMD_COMPILED_ABI_NO_MPI','memory_max':128*(1<<20),
        'swap_max':0,'tasks_max':16,'file_max':128*(1<<10),'log_max':32*(1<<10),
        'output_max':1*(1<<20),'wall_seconds':8,'stop_seconds':1,'rank_bytes':[4096,4096]}


def manager_env():
    if os.getuid()!=1001:raise Refusal('fixed user-manager UID1001 required')
    env=dict(os.environ,XDG_RUNTIME_DIR='/run/user/1001',DBUS_SESSION_BUS_ADDRESS='unix:path=/run/user/1001/bus',
             PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    for name in ['LD_PRELOAD','LD_AUDIT','PYTHONPATH','PYTHONHOME']:env.pop(name,None)
    return env


def ctl(unit,*args,timeout=5):
    if not re.fullmatch(r'r07-owned-[0-9a-f]{32}\.service',unit):raise Refusal('unowned unit name')
    r=subprocess.run(['/usr/bin/systemctl','--user',*args,unit],env=manager_env(),capture_output=True,text=True,timeout=timeout)
    return r


def show(unit):
    keys=['Id','LoadState','ActiveState','SubState','MainPID','ControlGroup','InvocationID','Result',
          'MemoryMax','MemorySwapMax','TasksMax','KillMode','OOMPolicy','Delegate','Restart','RuntimeMaxUSec',
          'TimeoutStopUSec','LimitFSIZE','LimitCORE','NoNewPrivileges','ExecStart','FragmentPath','Transient',
          'ExecMainCode','ExecMainStatus','MemoryPeak','CollectMode','SendSIGKILL']
    r=ctl(unit,'show','--property='+','.join(keys))
    fields=dict(line.split('=',1) for line in r.stdout.splitlines() if '=' in line)
    if 'LoadState' not in fields:raise Refusal('user-manager query unavailable: '+r.stderr.strip())
    return fields


def own_cgroup(pid):
    rows=Path(f'/proc/{pid}/cgroup').read_text().splitlines()
    v=[s[3:] for s in rows if s.startswith('0::')]
    if len(v)!=1 or not v[0].startswith('/') or '..' in Path(v[0]).parts:raise Refusal('cgroup v2 path')
    return v[0]


def cgroup_path(relative):
    if not relative.startswith('/user.slice/user-1001.slice/user@1001.service/') or '..' in Path(relative).parts:
        raise Refusal('unit outside UID1001 manager subtree')
    p=CGROOT/relative.lstrip('/')
    if p.resolve()!=p:raise Refusal('cgroup symlink/path')
    return p


def counters(path):
    def read(name):return (path/name).read_text().strip()
    def numbers(name):return dict((k,int(v)) for k,v in (line.split() for line in read(name).splitlines()))
    return {'memory_max':read('memory.max'),'swap_max':read('memory.swap.max'),
            'tasks_max':read('pids.max'),'oom_group':read('memory.oom.group'),
            'memory_current':int(read('memory.current')),'memory_peak':int(read('memory.peak')),
            'pids_current':int(read('pids.current')),'pids_events':numbers('pids.events'),
            'memory_events':numbers('memory.events'),'cgroup_events':numbers('cgroup.events')}


def members(path):
    # Only this verified unit's kernel membership is inspected. No foreign
    # /proc scan, mapping inventory, global table() or guessed MPI name.
    result={}
    for leaf in [path,*[p for p in path.rglob('*') if p.is_dir()]]:
        for value in (leaf/'cgroup.procs').read_text().split():
            pid=int(value)
            try:
                row=proc(pid)
                cg=own_cgroup(pid)
                candidate=cgroup_path(cg)
                if candidate!=path and not candidate.is_relative_to(path):
                    raise Refusal('cgroup member moved during observation')
                result[pid]=row
            except (FileNotFoundError,ProcessLookupError):pass
    return result


def verify_unit(job,fields,main_pid,invocation):
    if fields.get('Id')!=job['unit'] or fields.get('LoadState')!='loaded' or fields.get('ActiveState')!='active':
        raise Refusal('owned unit inactive/unbound')
    if fields.get('InvocationID')!=invocation or int(fields.get('MainPID','0'))!=main_pid:raise Refusal('unit invocation/MainPID mismatch')
    for key,wanted in [('MemoryMax',job['limits']['memory_max']),('MemorySwapMax',0),('TasksMax',16),
                       ('LimitFSIZE',job['limits']['file_max']),('LimitCORE',0)]:
        if int(fields.get(key,'-1'))!=wanted:raise Refusal('manager limit mismatch '+key)
    for key,wanted in [('KillMode','control-group'),('OOMPolicy','kill'),('Delegate','no'),('Restart','no'),
                       ('NoNewPrivileges','yes'),('Transient','yes'),('SendSIGKILL','yes'),('CollectMode','inactive'),
                       ('RuntimeMaxUSec',str(job['limits']['wall_seconds'])+'s'),('TimeoutStopUSec','1s')]:
        if fields.get(key)!=wanted:raise Refusal('manager lifecycle mismatch '+key)
    if fields['ControlGroup']!=own_cgroup(main_pid):raise Refusal('manager/kernel cgroup mismatch')
    cg=cgroup_path(fields['ControlGroup']);c=counters(cg)
    for key,wanted in [('memory_max',job['limits']['memory_max']),('swap_max',0),('tasks_max',16),('oom_group',1)]:
        if c[key]!=str(wanted):raise Refusal('kernel control mismatch '+key)
    # Effective ancestors can be stricter. This is a safety certificate, not
    # an availability guarantee or claim that 128 MiB is reserved.
    return cg,c


def create_job(case='normal'):
    if case not in CASES:raise Refusal('unregistered cheap case; native unissued')
    root=PRIVATE/('case-'+uuid.uuid4().hex);root.mkdir(mode=0o700)
    for name in ['scratch','out','logs']:(root/name).mkdir(mode=0o700)
    limits=dict(COMMON)
    if case=='oom':limits['memory_max']=64*(1<<20)
    if case=='hold':limits['wall_seconds']=3
    profile={'kind':'R07_CGROUP_ABI_NO_MPI','limits':limits,'worker_sha256':artifact_sha256(WORKER),
             'guard_sha256':artifact_sha256(HERE/'guard.py'),'manager_UID':1001}
    job={'version':2,'binding_version':1,'kind':'EXPLICIT_COMPILED_ABI_NO_MPI','id':uuid.uuid4().hex,
         'unit':'r07-owned-'+uuid.uuid4().hex+'.service','root':str(root),'rank_count':2,'case':case,'limits':limits,
         'profile_sha256':digest(profile),'executable_sha256':profile['worker_sha256'],
         'files':{str(p):artifact_sha256(p) for p in [HERE/'contracts.py',HERE/'guard.py',HERE/'controller.py',
                    HERE/'rank_worker.c',WORKER,Path(sys.executable).resolve(),LIB]}}
    atomic_json(root/'PROFILE.json',profile);atomic_json(root/'JOB.json',job)
    return root


def load_job(root,expect_absent=True):
    root=Path(root).absolute()
    if root.is_symlink() or not root.is_relative_to(PRIVATE) or root.parent!=PRIVATE:raise Refusal('owned job root')
    job=json.loads((root/'JOB.json').read_text());profile=json.loads((root/'PROFILE.json').read_text())
    if job.get('kind')!='EXPLICIT_COMPILED_ABI_NO_MPI' or job.get('root')!=str(root):raise Refusal('native execution unissued')
    if job.get('case') not in CASES or job.get('rank_count')!=2 or job.get('profile_sha256')!=digest(profile):raise Refusal('JOB/PROFILE mismatch')
    wanted=dict(COMMON)
    if job['case']=='oom':wanted['memory_max']=64*(1<<20)
    if job['case']=='hold':wanted['wall_seconds']=3
    if job['limits']!=wanted or profile['limits']!=wanted:raise Refusal('bounded limits cannot be enlarged or weakened')
    expected_profile={'kind':'R07_CGROUP_ABI_NO_MPI','limits':wanted,'worker_sha256':artifact_sha256(WORKER),
                      'guard_sha256':artifact_sha256(HERE/'guard.py'),'manager_UID':1001}
    if profile!=expected_profile:raise Refusal('exact PROFILE fields/source mismatch')
    expected_files={str(p) for p in [HERE/'contracts.py',HERE/'guard.py',HERE/'controller.py',HERE/'rank_worker.c',
                                   WORKER,Path(sys.executable).resolve(),LIB]}
    if set(job.get('files',{}))!=expected_files:raise Refusal('exact source/executable allowlist')
    for p,h in job['files'].items():
        if artifact_sha256(Path(p))!=h:raise Refusal('source/executable pin mismatch')
    if profile['worker_sha256']!=artifact_sha256(WORKER):raise Refusal('compiled worker mismatch')
    if expect_absent and show(job['unit']).get('LoadState')!='not-found':raise Refusal('unit already exists')
    return job,profile


def launch_command(root,job):
    l=job['limits']
    props={'Type':'exec','MemoryMax':str(l['memory_max']),'MemorySwapMax':'0','TasksMax':'16',
           'OOMPolicy':'kill','KillMode':'control-group','Delegate':'no','Restart':'no','SendSIGKILL':'yes',
           'RuntimeMaxSec':str(l['wall_seconds'])+'s','TimeoutStopSec':'1s','LimitFSIZE':str(l['file_max']),
           'LimitCORE':'0','NoNewPrivileges':'yes','WorkingDirectory':str(DFT),
           'UnsetEnvironment':'LD_PRELOAD LD_AUDIT PYTHONHOME PYTHONPATH LD_LIBRARY_PATH'}
    # Failed-unit metadata must survive until independently audited. Automatic
    # --collect can remove Result/InvocationID before a sampled observer reads
    # the OOM result. Reset ONLY this unique failed unit after durable evidence.
    command=['/usr/bin/systemd-run','--user','--pipe','--wait','--quiet','--unit='+job['unit']]
    for k,v in props.items():command+=['--property='+k+'='+v]
    command+=['--setenv=PYTHONDONTWRITEBYTECODE=1','--setenv=OMP_NUM_THREADS=1','--setenv=OPENBLAS_NUM_THREADS=1',
              '--setenv=MKL_NUM_THREADS=1',str(Path(sys.executable).resolve()),str(HERE/'guard.py'),str(root)]
    return command


def hostwide_gate(_):raise Refusal('host-wide exclusion/inventory HARD_BLOCKED; cgroup ownership is insufficient')
