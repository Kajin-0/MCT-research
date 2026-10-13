"""Compile only. Never starts MPI_Init, mpirun, QE or a service."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
BASE=DFT/'.local/qe75_lowram_20261011'
PRIVATE=BASE/'local_owned_mpi_20261013'
ENV=DFT/'.local/qe-env'
TOOLCHAIN=BASE/'toolchain/bin'
PINNED_CLIENT=BASE/'native_envelope_20261013/transport/lease_client.c'
CLIENT_SHA='ecab5af0b06e011004fa2132b5f7332551845faa6f0354896542c942c8aa7736'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    PRIVATE.mkdir(exist_ok=True)
    if sha(PINNED_CLIENT)!=CLIENT_SHA:raise RuntimeError('retained client source changed')
    original=PINNED_CLIENT.read_text()
    changes=[('int qe75_lease_call(int rank,int size,int action,int required_scope) {',
              'int r07_collective_lease_call(int rank,int size,int action) {\n    const int required_scope=3;'),
             ('if(rank<0||rank>=2||size!=2||(action!=1&&action!=2)||(required_scope!=1&&required_scope!=2))return EINVAL;',
              'if(action==3) { if(rank!=-1||size!=0)return EINVAL; }\n'
              '    else if(rank<0||rank>=2||size!=2||(action!=1&&action!=2))return EINVAL;'),
             ('"R07L"','"R07C"')]
    candidate=original
    for old,new in changes:
        expected=2 if old=='"R07L"' else 1
        if candidate.count(old)!=expected:raise RuntimeError('exact client transformation site changed')
        candidate=candidate.replace(old,new)
    client=PRIVATE/'collective_lease.v2.c'
    if client.exists() and client.read_text()!=candidate:raise RuntimeError('do not overwrite distinct private source')
    client.write_text(candidate)
    patch=''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True),
                                     fromfile='retained/lease_client.c',tofile='private/collective_lease.c',n=0))
    (PRIVATE/'collective_lease.patch').write_text(patch)
    compiler=ENV/'bin/mpicc'
    binary=PRIVATE/'collective_harness.COMPILE_ONLY.v2'
    so=PRIVATE/'collective_lease.v2.so'
    if binary.exists() or so.exists():raise RuntimeError('one build; preserve existing outputs')
    flags=['-std=c11','-O2','-Wall','-Wextra','-Werror']
    commands=[[str(compiler),*flags,'-I'+str(HERE),str(HERE/'collective_harness.c'),str(client),'-o',str(binary)],
              ['/usr/bin/cc',*flags,'-fPIC','-shared',str(client),'-o',str(so)]]
    runs=[]
    env=dict(os.environ,PATH=str(TOOLCHAIN)+os.pathsep+os.environ['PATH'])
    for key in ['OMPI_CC','OMPI_CFLAGS','OMPI_LDFLAGS','OMPI_LIBS','LD_PRELOAD','LD_AUDIT']:
        env.pop(key,None)
    for command in commands:
        r=subprocess.run(command,cwd=DFT,env=env,capture_output=True,text=True,timeout=60)
        runs.append(dict(command=command,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
        (PRIVATE/'harness_build_attempt.json').write_text(json.dumps(runs,indent=2)+'\n')
        if r.returncode:raise RuntimeError(json.dumps(runs))
    wrapper={}
    for opt in ['command','compile','link','version']:
        r=subprocess.run([str(compiler),'--showme:'+opt],env=env,capture_output=True,text=True,timeout=5)
        wrapper[opt]=dict(returncode=r.returncode,text=r.stdout+r.stderr)
    paths=[HERE/'collective_harness.c',HERE/'status.h',PINNED_CLIENT,client,binary,so,
           compiler.resolve(),(ENV/'bin/mpirun').resolve(),(ENV/'bin/prterun').resolve(),
           (ENV/'lib/libmpi.so').resolve(),(ENV/'lib/libpmix.so').resolve(),
           (TOOLCHAIN/'x86_64-conda-linux-gnu-cc').resolve()]
    result=dict(passed=True,runs=runs,wrapper=wrapper,pins={str(p):sha(p) for p in paths},
                new_wire_magic='R07C',new_scope=3,MPI_Init_executed=False,MPI_job_executed=False,
                candidate_status='COMPILE_ONLY_RUNTIME_UNADMITTED')
    (PRIVATE/'harness_build.v2.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':print(json.dumps(run(),indent=2))
