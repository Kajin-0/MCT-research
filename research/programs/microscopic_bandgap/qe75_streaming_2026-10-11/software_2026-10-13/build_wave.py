"""Private serial codec + compile-only actual QE initial-state hook."""
from pathlib import Path
import json
import subprocess
import sys
import time
from source_capture import generate,HERE,ROOT,DFT
sys.path.insert(0,str(HERE.parent/'m5_readiness'))
from build import FC,INCLUDES,FLAGS
from family_runtime import LinuxGuard,LIB,memory
from native_bundle import artifact_sha256
PRIVATE=ROOT/'m5_software_20261013'


def run(argv):
    started=time.monotonic();p=subprocess.run(list(map(str,argv)),cwd=DFT,capture_output=True,text=True,timeout=60)
    r={'command':list(map(str,argv)),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,
       'wall_seconds':time.monotonic()-started}
    if p.returncode: raise RuntimeError(r)
    return r


def main():
    info=LinuxGuard(LIB).probe(PRIVATE)
    if info['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30): raise RuntimeError('small build headroom')
    folder=PRIVATE/'wave';folder.mkdir(exist_ok=True)
    audit=generate(folder/'init_run.f90');records=[]
    for mode in ['stock','stream']:
        obj=folder/mode;obj.mkdir(exist_ok=True)
        records.append(run([FC,'-O0','-g','-fcheck=all','-ffree-line-length-none','-J',obj,*INCLUDES,
                            '-c',HERE/'initial_state.f90','-o',obj/'initial_state.o']))
        records.append(run([FC,'-O0','-g','-fcheck=all','-ffree-line-length-none','-I',obj,*INCLUDES,
                            HERE/'initial_unit.f90',obj/'initial_state.o','-o',obj/'initial_unit']))
        flag=FLAGS+['-D__QE75_INITIAL_CAPTURE']+(['-D__EXX_QSTREAM'] if mode=='stream' else [])
        records.append(run([FC,*flag,'-I',obj,'-I',ROOT/'m5_readiness'/f'{mode}-objects','-J',obj,*INCLUDES,
                            '-c',folder/'init_run.f90','-o',obj/'init_run.o']))
    records.append(run([FC,'-O0','-fcheck=all','-J',folder,*INCLUDES,'-c',ROOT/'q-e/Modules/random_numbers.f90',
                        '-o',folder/'random_numbers.o']))
    records.append(run([FC,'-O0','-fcheck=all','-I',folder,*INCLUDES,HERE/'rng_unit.f90',
                        folder/'random_numbers.o','-o',folder/'rng_unit']))
    report={'passed':True,'records':records,'source_audit':audit,'native_PW_MPI_run':False,
            'native_initial_seed_generated':False,'source_sha256':{str(p):artifact_sha256(p) for p in
                    [HERE/'initial_state.f90',HERE/'initial_unit.f90',HERE/'source_capture.py',folder/'init_run.f90',
                     ROOT/'q-e/Modules/random_numbers.f90',HERE/'rng_unit.f90']},
            'binaries':{str(folder/m/'initial_unit'):artifact_sha256(folder/m/'initial_unit') for m in ['stock','stream']}}
    (PRIVATE/'wave_build.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: serial 48-band capture and both real-QE init_run objects compile; native NOT RUN.')


if __name__=='__main__': main()
