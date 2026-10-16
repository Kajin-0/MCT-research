"""Fresh compile, read-only native dependencies/preflight; never launches MPI."""
from pathlib import Path
from datetime import datetime,timezone
import ast
import json
import os
import shutil
import subprocess
import sys
import uuid
sys.path.insert(0,str(Path(__file__).resolve().parent))
import owner
from protocol import sha,durable,GIB,kernel,Refusal
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3]
DFT=Path('/home/User/opencode_workspace/DFT');ENV=DFT/'.local/qe-env'

def main():
    if (HERE/'frozen_execution.json').exists():raise Refusal('already frozen; no new identity/retry')
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip().startswith('9f59814')
    private=REPO/'.tmp/r07spc16'/('a'+uuid.uuid4().hex[:8]);private.mkdir(mode=0o700)
    build=private/'build';build.mkdir();elf=build/'mpi_lifecycle'
    command=[str(ENV/'bin/mpicc'),'-std=c11','-O2','-Wall','-Wextra','-Werror',str(HERE/'mpi_fixture.c'),str(HERE/'native_lease.c'),'-o',str(elf)]
    env=dict(os.environ,OMPI_CC='/usr/bin/cc',PYTHONDONTWRITEBYTECODE='1')
    compiled=subprocess.run(command,env=env,capture_output=True,text=True,timeout=30)
    durable(HERE/'build.json',dict(argv=command,OMPI_CC='/usr/bin/cc',returncode=compiled.returncode,stdout=compiled.stdout,stderr=compiled.stderr))
    if compiled.returncode:raise Refusal('compile failed, no service')
    ldd=subprocess.run(['/usr/bin/ldd',str(elf)],capture_output=True,text=True,timeout=5)
    if ldd.returncode or 'not found' in ldd.stdout:raise Refusal('native runtime linkage unavailable')
    pins={str(p.resolve()):sha(p.resolve()) for p in [elf,ENV/'bin/mpirun',ENV/'bin/mpicc',Path('/usr/bin/cc'),Path('/usr/bin/systemd-run'),Path('/usr/bin/systemctl'),Path(sys.executable),owner.LIB]}
    for line in ldd.stdout.splitlines():
        for word in line.split():
            if word.startswith('/') and Path(word).is_file():pins[word]=sha(word)
    # Import closure includes the actual production-derived owner/guard/kernel,
    # not a modeled manager implementation or alternative permissive monitor.
    for m in list(sys.modules.values()):
        file=getattr(m,'__file__',None)
        if file and Path(file).is_file() and (Path(file).is_relative_to(REPO) or Path(file).is_relative_to(DFT)):
            pins[str(Path(file).resolve())]=sha(file)
    for p in HERE.iterdir():
        if p.suffix in ['.py','.c','.md']:pins[str(p)]=sha(p)
    for p in HERE.glob('*.py'):ast.parse(p.read_text())
    cpus=sorted(os.sched_getaffinity(0))[:2]
    if len(cpus)!=2:raise Refusal('two allowed CPUs unavailable')
    limits=dict(memory_B=12*GIB,swap_B=0,tasks=12,wall_s=600,host_floor_B=4*GIB,disk_floor_B=10*GIB,output_B=14*GIB)
    profile=dict(kind=owner.KIND,scope=1601,science_release=False,root=str(private),elf=str(elf),elf_sha256=sha(elf),
        mpirun=str(ENV/'bin/mpirun'),pins=pins,limits=limits,cpus=cpus,PP='NOT_APPLICABLE_NON_SCIENCE',
        network='localhost:2,isolated_plm,self_sm_ob1; NO private-netns or hostwide-exclusion claim')
    jobs={}
    for member in ['positive','missing_final']:
        root=private/member;root.mkdir(mode=0o700)
        for p in ['pilot','tmp']:(root/p).mkdir(mode=0o700)
        if len(str(root/'s').encode())>107:raise Refusal('socket pathname too long')
        job=dict(kind=owner.KIND,case=member,root=str(root),unit='r07-owned-'+uuid.uuid4().hex+'.service',
            nonce=uuid.uuid4().hex,profile_sha256=owner.digest(profile),argv={str(r):[str(elf),str(root),member] for r in [0,1]})
        job['job_sha256']=owner.digest(job);jobs[member]=job
        durable(root/'PROFILE.json',profile);durable(root/'JOB.json',job)
        if owner.show(job['unit']).get('LoadState')!='not-found':raise Refusal('unit name not fresh')
    guard=owner.LinuxGuard(owner.LIB);storage=guard.probe(private);mem=owner.memory()['MemAvailable']
    policy=owner.admission(storage,[64*(1<<20)],14*GIB,mem)
    if mem<16*GIB+128*(1<<20):raise Refusal('physical reserve including holder')
    # Read-only manager access + real bus RefUnit support on the existing manager
    # itself, without creating a preliminary service or invoking mpirun.
    manager=subprocess.run(['/usr/bin/systemctl','--user','show','--property=Version'],env=owner.manager_env(),capture_output=True,text=True,timeout=5)
    if manager.returncode:raise Refusal('user manager unavailable')
    reference=kernel.UnitReference('default.target');reference.close()
    ledger=owner.REGISTRY.read_bytes();j=json.loads(ledger)
    if j.get('phase')!='FINISHED' or j.get('members')!=[]:raise Refusal('historical family ledger active')
    if (REPO/'.tmp/r07spc16/PENDING_UNIT.json').exists():raise Refusal('historical pending unit')
    # No host-wide proc scan. Serialize cooperating owners with actual old lock.
    import fcntl
    lock=os.open(owner.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(lock)
    before=dict(UTC=datetime.now(timezone.utc).isoformat(),baseline='9f59814',
        DFT_status=subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True),
        DFT_tracked_diff_sha256=__import__('hashlib').sha256(subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'diff','--binary'])).hexdigest(),
        ledger_sha256=sha(owner.REGISTRY),storage=storage,MemAvailable_B=mem,resource_admission=policy,
        manager=manager.stdout,ldd=ldd.stdout,sockets={m:len(str(Path(j['root'])/'s').encode()) for m,j in jobs.items()},
        hostwide_MPI_absence_proved=False,private_network_namespace_proved=False,native_QE_authorized=False)
    durable(HERE/'preflight.json',before)
    durable(HERE/'frozen_execution.json',dict(profile=profile,jobs=jobs,maximum_positive_attempts=1,
        maximum_negative_attempts=1,negative_requires_positive_terminal_pass=True,UTC=before['UTC']))
    print(json.dumps(dict(preflight='PASS_BEFORE_ANY_SERVICE',root=str(private),elf_sha256=sha(elf),sockets=before['sockets'])))

if __name__=='__main__':main()
