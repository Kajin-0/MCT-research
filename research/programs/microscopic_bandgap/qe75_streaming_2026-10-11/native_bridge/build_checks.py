"""Compile changed native units plus small serial codec. NEVER executes PW/MPI."""
from pathlib import Path
import json
import subprocess
import time
import hashlib
import tempfile
import resource
import shutil
from patch_native_bridge import build_sources

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011'
PRIVATE=ROOT/'native_bridge'


def run(cmd,timeout=90):
    start=time.monotonic()
    result=subprocess.run(list(map(str,cmd)),cwd=DFT,capture_output=True,text=True,timeout=timeout)
    record={'command':list(map(str,cmd)),'returncode':result.returncode,'stdout':result.stdout,
            'stderr':result.stderr,'wall_seconds':time.monotonic()-start}
    return record


def main():
    source=Path(tempfile.mkdtemp(dir=PRIVATE,prefix='source-generated-'))
    build_sources(source)
    fc=ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran'
    includes=[]
    for p in sorted((DFT/'.local/qe-env/include/qe').iterdir()):
        if p.is_dir(): includes+=['-I',str(p)]
    records=[]
    flags=['-cpp','-D__MPI','-D__HDF5','-D__SCALAPACK','-D__ELPA','-fopenmp',
           '-ffree-line-length-none','-fallow-argument-mismatch','-O0','-g','-fcheck=all','-fcheck=array-temps']
    for mode in ['stream','stock']:
        obj=PRIVATE/(mode+'-objects');obj.mkdir(exist_ok=True)
        for name in ['exx_checkpoint_state','exx_qstream','exx','electrons','punch','run_pwscf','wfcinit']:
            record=run([fc,*flags,*(['-D__EXX_QSTREAM'] if mode=='stream' else []),
                        '-J',obj,'-I',obj,*includes,'-c',source/(name+'.f90'),'-o',obj/(name+'.o')])
            record.update({'mode':mode,'unit':name});records.append(record)
            if record['returncode']:
                (PRIVATE/'build_checks.json').write_text(json.dumps({'passed':False,'records':records},indent=2)+'\n')
                raise RuntimeError(record)
    for optimization in ['O0','O2']:
        obj=PRIVATE/('unit-'+optimization);obj.mkdir(exist_ok=True)
        record=run([fc,'-'+optimization,'-g','-fcheck=all','-fcheck=array-temps','-ffree-line-length-none',
                    '-J',obj,*includes,HERE/'exx_checkpoint_state.f90',HERE/'state_unit.f90',
                    '-o',obj/'state_unit'])
        records.append(record)
        if record['returncode']: raise RuntimeError(record)
    obj=PRIVATE/'unit-O0'
    record=run([fc,'-O0','-g','-fcheck=all','-fcheck=array-temps','-ffree-line-length-none',
                '-J',obj,*includes,source/'exx_qstream.f90',HERE/'reserved_unit.f90','-o',obj/'reserved_unit'])
    records.append(record)
    if record['returncode']: raise RuntimeError(record)
    obj=PRIVATE/'zero-counter';obj.mkdir(exist_ok=True)
    # Modules in this directory are explicit small stubs, isolated from native
    # object/module builds. Routines themselves are pristine pinned QE source.
    record=run([fc,'-cpp','-O0','-g','-fcheck=all','-ffree-line-length-none','-J',obj,'-I',obj,*includes,
                HERE/'zero_counter_unit.f90',ROOT/'q-e/PW/src/save_in_electrons.f90',
                ROOT/'q-e/PW/src/restart_in_electrons.f90','-o',obj/'zero_counter_unit'])
    records.append(record)
    if record['returncode']: raise RuntimeError(record)
    # Independently compare the reader/ACE bodies to the previously validated
    # streaming source. The bridge must not edit action/energy arithmetic.
    original=(ROOT/'q-e/PW/src/exx.f90').read_text()
    updated=(source/'exx.f90').read_text()
    audit={}
    for start,end in [('  SUBROUTINE vexx_k(', '  END SUBROUTINE vexx_k'),
                      ('  FUNCTION exxenergy2_k(', '  END FUNCTION  exxenergy2_k'),
                      ('  SUBROUTINE aceinit(', '  END SUBROUTINE aceinit'),
                      ('  SUBROUTINE aceinit_k(', '  END SUBROUTINE aceinit_k'),
                      ('  SUBROUTINE aceupdate_k(', '  END SUBROUTINE aceupdate_k'),
                      ('  SUBROUTINE vexxace_k(', '  END SUBROUTINE vexxace_k')]:
        def body(s):
            i=s.index(start);j=s.index(end,i)+len(end);return s[i:j]
        assert body(original)==body(updated),start
        audit[start.strip()]={'byte_identical_to_validated_storage_candidate':True}
    # Link only, never execute. Preserve the stock archive and previous binary.
    link=PRIVATE/'link-only';link.mkdir(exist_ok=True)
    record=run([fc,*flags,'-J',link,*includes,'-c',ROOT/'q-e/PW/src/pwscf.f90','-o',link/'pwscf.o'])
    records.append(record)
    if record['returncode']: raise RuntimeError(record)
    qelib=DFT/'.local/qe-env/lib';archive=link/'libqe_pw_bridge.a'
    shutil.copy2(qelib/'libqe_pw.a',archive)
    replaced=['exx','electrons','punch','run_pwscf','wfcinit']
    subprocess.run(['/usr/bin/ar','d',str(archive),*[n+'.f90.o' for n in replaced]],check=True)
    names=['exx_checkpoint_state','exx_qstream',*replaced]
    for name in names: shutil.copy2(PRIVATE/'stream-objects'/(name+'.o'),link/(name+'.f90.o'))
    subprocess.run(['/usr/bin/ar','r',str(archive),*[str(link/(n+'.f90.o')) for n in names]],check=True)
    libs=['device_lapack','lax','kssolver_davidson','kssolver_cg','kssolver_paro','kssolver_rmmdiis','kssolver_dense',
          'upflib','modules','modules_c','fftx','fftx_c','dftd3','xclib','libbeef','devxlib','xml','utilx','utilx_c']
    binary=link/'pw.bridge.RUNTIME_REFUSED'
    record=run([fc,'-fopenmp',link/'pwscf.o','-Wl,--start-group',archive,
                *[qelib/('libqe_'+n+'.a') for n in libs],qelib/'libmbd.a','-Wl,--end-group',
                '-L',qelib,'-Wl,-rpath,'+str(qelib),'-lelpa','-lscalapack','-lhdf5_fortran','-lhdf5',
                '-lfftw3','-lfftw3_omp','-lmpi_mpifh','-lmpi','-llapack','-lblas','-lm','-o',binary])
    records.append(record)
    if record['returncode']: raise RuntimeError(record)
    dynamic=run(['/usr/bin/ldd',binary]);assert 'not found' not in dynamic['stdout']
    report={'passed':True,'records':records,'native_PW_or_MPI_executed':False,'source_directory':str(source),
            'reader_ACE_source_audit':audit,'link':{'binary':str(binary),
              'sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'ldd':dynamic},
            'maximum_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir()}}
    (PRIVATE/'build_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 14 native-unit compiles, O0/O2 serial codec, reserved store, six reader/ACE audits, private link. PW/MPI not executed.')


if __name__=='__main__':
    try: main()
    except Exception as error:
        (PRIVATE/'build_checks.json').write_text(json.dumps({'passed':False,'error':str(error),
          'native_PW_or_MPI_executed':False},indent=2)+'\n')
        raise
