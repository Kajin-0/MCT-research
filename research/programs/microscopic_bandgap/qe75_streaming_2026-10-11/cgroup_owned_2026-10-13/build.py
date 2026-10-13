"""Bounded C-only worker build; no MPI linker, launcher or QE invocation."""
import json
import resource
import subprocess
from contracts import HERE,PRIVATE,BASE,WORKER,artifact_sha256,LinuxGuard,LIB,memory


def main():
    if LinuxGuard(LIB).probe(PRIVATE)['available_bytes']<11*(1<<30) or memory()['MemAvailable']<4*(1<<30):
        raise RuntimeError('tiny build headroom')
    binary=WORKER
    if binary.exists():raise RuntimeError('one-shot compiled worker preserved')
    source=BASE/'native_envelope_20261013/transport/lease_client.c'
    cmd=['/usr/bin/cc','-std=c11','-O2','-Wall','-Wextra','-Werror',str(HERE/'rank_worker.c'),str(source),'-o',str(binary)]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
    report={'passed':r.returncode==0,'command':cmd,'stdout':r.stdout,'stderr':r.stderr,
            'worker_sha256':artifact_sha256(binary) if r.returncode==0 else None,'fixed_lease_source_sha256':artifact_sha256(source),
            'maximum_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'QE_MPI_execution':False}
    (PRIVATE/'build_v2.json').write_text(json.dumps(report,indent=2)+'\n')
    if r.returncode:raise RuntimeError(report)
    print('PASS: tiny C-only ABI worker compiled; no MPI/PW link or execution.')


if __name__=='__main__':main()
