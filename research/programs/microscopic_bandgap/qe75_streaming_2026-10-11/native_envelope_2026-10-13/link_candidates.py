"""Integrate the tested status fix + actual FFT observer. NO executable run."""
import json
import shutil
from build_transport import PRIVATE,ROOT,FC,run,LinuxGuard,LIB,memory
from native_bundle import artifact_sha256
from fixture_preflight import backends


def main():
    for name in ['transport_tests','descriptor_build','descriptor_tests']:
        if not json.loads((PRIVATE/f'{name}.json').read_text())['passed']:raise RuntimeError('unpassed component '+name)
    if LinuxGuard(LIB).probe(PRIVATE)['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):
        raise RuntimeError('link headroom')
    old=ROOT/'m5_software_20261013'
    recipe=json.loads((old/'capture_link.json').read_text())
    folder=PRIVATE/'link-only';folder.mkdir(exist_ok=False);records=[];candidates={}
    c=folder/'lease_client.o'
    records.append(run(['/usr/bin/cc','-std=c11','-Wall','-Wextra','-Werror','-O2','-c',PRIVATE/'transport/lease_client.c','-o',c]))
    for mode in ['stock','stream']:
        prior=old/'link-only'/mode/'libqe_pw_capture.a';pin=artifact_sha256(prior)
        target=folder/mode;target.mkdir();archive=target/'libqe_pw_envelope.a';shutil.copy2(prior,archive)
        records.append(run(['/usr/bin/ar','d',archive,'exx.f90.o','qe75_native_lease.f90.o']))
        objects=[]
        for name,path in [('exx.f90.o',PRIVATE/'descriptor'/mode/'exx.o'),
                          ('qe75_native_lease.f90.o',PRIVATE/'transport'/mode/'native_lease.o'),
                          ('qe75_resource_descriptor.f90.o',PRIVATE/'descriptor'/mode/'resource_descriptor.o')]:
            obj=target/name;shutil.copy2(path,obj);objects.append(obj)
        records.append(run(['/usr/bin/ar','r',archive,*objects]))
        binary=target/'pw.envelope.NATIVE_UNADMITTED'
        command=next(list(row['command']) for row in recipe['records'] if row['command'][-1]==str(old/'link-only'/mode/'pw.capture.NATIVE_UNADMITTED'))
        command=[str(archive) if arg==str(prior) else str(c) if arg.endswith('/m5_readiness/link-only/lease_client.o') else arg for arg in command]
        command[-1]=str(binary);records.append(run(command))
        symbols=run(['/usr/bin/nm','--defined-only',binary])['stdout']
        expected=['__qe75_resource_descriptor_MOD_resource_write','qe75_capture_fft_','qe75_lease_call']
        for name in expected:
            if len([line for line in symbols.splitlines() if line.split()[-1]==name])!=1:raise RuntimeError('missing/duplicate integrated symbol '+name)
        candidates[mode]={'binary':str(binary),'sha256':artifact_sha256(binary),'backends':backends(binary),
                          'integrated_symbols_once':expected,'objects_sha256':{str(o):artifact_sha256(o) for o in objects}}
        if artifact_sha256(prior)!=pin:raise RuntimeError('prior archive changed')
    baseline=backends(old/'link-only/stock/pw.capture.NATIVE_UNADMITTED')
    if candidates['stock']['backends']!=baseline or candidates['stream']['backends']!=baseline:raise RuntimeError('backend mismatch')
    report={'passed':True,'records':records,'candidates':candidates,'native_MPI_PW_executed':False,'native_admission_issued':False}
    (PRIVATE/'link.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: hardened lease and actual FFT observer integrated in both candidates. UNEXECUTED.')


if __name__=='__main__':main()
