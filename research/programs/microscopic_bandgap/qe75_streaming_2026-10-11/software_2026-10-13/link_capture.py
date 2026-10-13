"""Exact retained private link recipe, new capture objects. Never executes PW."""
import json
import shutil
from build_wave import PRIVATE,ROOT,HERE,DFT,run
from family_runtime import LinuxGuard,LIB,memory
from native_bundle import artifact_sha256
from fixture_preflight import backends


def main():
    info=LinuxGuard(LIB).probe(PRIVATE)
    if info['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):raise RuntimeError('link headroom')
    old=json.loads((ROOT/'m5_readiness/link.json').read_text())
    folder=PRIVATE/'link-only';folder.mkdir(exist_ok=False)
    records=[];candidates={}
    for mode in ['stock','stream']:
        prior=ROOT/'m5_readiness/link-only'/mode/'libqe_pw_readiness.a'
        prior_sha=artifact_sha256(prior)
        target=folder/mode;target.mkdir();archive=target/'libqe_pw_capture.a';shutil.copy2(prior,archive)
        records.append(run(['/usr/bin/ar','d',archive,'init_run.f90.o']))
        objects=[]
        for name,source in [('init_run.f90.o',PRIVATE/'wave'/mode/'init_run.o'),
                            ('qe75_initial_state.f90.o',PRIVATE/'wave'/mode/'initial_state.o')]:
            dest=target/name;shutil.copy2(source,dest);objects.append(dest)
        records.append(run(['/usr/bin/ar','r',archive,*objects]))
        binary=target/'pw.capture.NATIVE_UNADMITTED'
        command=list(old['records'][-1]['command'])
        for i,item in enumerate(command):
            if item.endswith('/libqe_pw_readiness.a'):command[i]=str(archive)
        command[-1]=str(binary);records.append(run(command))
        if artifact_sha256(prior)!=prior_sha:raise RuntimeError('prior readiness archive changed')
        candidates[mode]={'binary':str(binary),'sha256':artifact_sha256(binary),
                          'objects_sha256':{str(p):artifact_sha256(p) for p in objects},
                          'runtime_backends':backends(binary)}
    if candidates['stock']['runtime_backends']!=candidates['stream']['runtime_backends']:
        raise RuntimeError('capture candidates have different backends')
    baseline=backends(ROOT/'m5_readiness/link-only/stock/pw.m5.READINESS_REFUSED')
    if candidates['stock']['runtime_backends']!=baseline:raise RuntimeError('backend drift from retained recipe')
    report={'passed':True,'records':records,'candidates':candidates,'retained_runtime_backends_match':True,
            'native_PW_MPI_executed':False,'native_admission_issued':False}
    (PRIVATE/'capture_link.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: both new private capture candidates linked; identical retained FFT/MPI backends; never executed.')


if __name__=='__main__':main()
