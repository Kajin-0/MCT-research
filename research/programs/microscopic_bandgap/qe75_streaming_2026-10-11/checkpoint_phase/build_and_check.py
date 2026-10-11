"""Reproduce bounded source/storage/guard tests. NEVER launches PW or MPI."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011'
PRIVATE=ROOT/'checkpoint_phase'


def run(command,timeout=90):
    start=time.monotonic()
    result=subprocess.run(command,cwd=DFT,capture_output=True,text=True,timeout=timeout)
    record={'command':[str(x) for x in command],'returncode':result.returncode,
            'stdout':result.stdout,'stderr':result.stderr,'wall_seconds':time.monotonic()-start}
    if result.returncode: raise RuntimeError(record)
    return record


def main():
    PRIVATE.mkdir(exist_ok=True)
    fc=ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran'
    includes=[]
    for directory in sorted((DFT/'.local/qe-env/include/qe').iterdir()):
        if directory.is_dir(): includes+=['-I',str(directory)]
    records=[]
    records.append(run(['/usr/bin/gcc','-O2','-Wall','-Wextra','-Werror','-std=c11','-fPIC','-shared',
                        str(HERE/'storage_guard.c'),'-o',str(PRIVATE/'storage_guard.so')]))
    records.append(run([str(fc),'-O2','-g','-fcheck=all','-fcheck=array-temps','-ffree-line-length-none',
                        '-J',str(PRIVATE),*includes,str(HERE/'exx_qstream_v2.f90'),str(HERE/'ownership_unit.f90'),
                        '-o',str(PRIVATE/'ownership_unit')]))
    records.append(run([sys.executable,str(HERE/'test_checkpoint_phase.py')]))
    from close_outer_stop_gate import patch_source
    source=PRIVATE/'source'; source.mkdir(exist_ok=True)
    corrected=source/'electrons.f90'
    baseline=ROOT/'q-e/PW/src/electrons.f90'
    corrected.write_bytes(baseline.read_bytes()); patch_source(corrected)
    records.append(run([str(fc),'-cpp','-D__MPI','-D__HDF5','-D__SCALAPACK','-D__ELPA','-D__EXX_QSTREAM',
                        '-fopenmp','-ffree-line-length-none','-fallow-argument-mismatch','-O0','-g','-fcheck=all',
                        '-J',str(PRIVATE),'-I',str(ROOT/'stream-objects'),*includes,'-c',str(corrected),
                        '-o',str(PRIVATE/'electrons_guarded.o')]))
    report={'records':records,'native_QE_or_MPI_launched':False,'native_state_qualified':False,
            'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file() and p.suffix in ['.py','.c','.f90']}}
    (PRIVATE/'build_and_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: bounded code/storage/guard tests. Native state bridge still NOT QUALIFIED.')


if __name__=='__main__': main()
