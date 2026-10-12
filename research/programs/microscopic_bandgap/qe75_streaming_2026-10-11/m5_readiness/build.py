"""Bounded private compilation + serial I/O decoder. No PW/HSE/MPI execution."""
from pathlib import Path
import json
import os
import resource
import shutil
import subprocess
import sys
import time

from binding import HERE,artifact_sha256
sys.path.insert(0,str(HERE.parent/'runtime_admission'))
from family_runtime import LinuxGuard,LIB,memory
from patch_sources import generate

DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011'
PRIVATE=ROOT/'m5_readiness'
FC=ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran'
INCLUDES=[]
for path in sorted((DFT/'.local/qe-env/include/qe').iterdir()):
    if path.is_dir(): INCLUDES+=['-I',str(path)]
INCLUDES+=['-I',str(DFT/'.local/qe-env/include')]
FLAGS=['-cpp','-D__MPI','-D__HDF5','-D__SCALAPACK','-D__ELPA','-D__QE75_M5','-fopenmp',
       '-ffree-line-length-none','-fallow-argument-mismatch','-O0','-g','-fcheck=all','-fcheck=array-temps']


def run(command,timeout=60):
    started=time.monotonic()
    r=subprocess.run(list(map(str,command)),cwd=DFT,capture_output=True,text=True,timeout=timeout)
    record={'command':list(map(str,command)),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,
            'wall_seconds':time.monotonic()-started}
    if r.returncode: raise RuntimeError(record)
    return record


def main():
    report={'passed':False,'PW_HSE_MPI_executed':False,'records':[]}
    try:
        info=LinuxGuard(LIB).probe(PRIVATE)
        if info['probe_errno'] or info['fs_type']!=0xef53 or info['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):
            raise RuntimeError('small build resource headroom unsafe')
        source=PRIVATE/'source'
        if source.exists():
            previous=json.loads((PRIVATE/'build.json').read_text())
            if previous['passed']: raise RuntimeError('completed build preserved; no unrequested rebuild')
            report['source_sha256']=generate(PRIVATE/'source-retry1')
            for name,sha in report['source_sha256'].items():
                if artifact_sha256(source/name)!=sha: raise RuntimeError('retained generated source changed')
        else: report['source_sha256']=generate(source)
        records=report['records']
        # Compiled wire worker is deliberately free of MPI/PW/HSE dependencies.
        records.append(run(['/usr/bin/cc','-std=c11','-D_DEFAULT_SOURCE','-Wall','-Wextra','-Werror','-O2',
                            HERE/'lease_client.c',HERE/'abi_worker.c','-o',PRIVATE/'abi_worker']))
        for mode in ['stock','stream']:
            obj=PRIVATE/(mode+'-objects');obj.mkdir(exist_ok=True)
            flags=FLAGS+(['-D__EXX_QSTREAM'] if mode=='stream' else [])
            for name,path in [('qe75_native_lease',HERE/'native_lease.f90'),('qe75_diagnostics',HERE/'diagnostics.f90'),
                              ('exx_checkpoint_state',source/'exx_checkpoint_state.f90'),('exx_qstream',source/'exx_qstream.f90'),
                              ('exx',source/'exx.f90'),('run_pwscf',source/'run_pwscf.f90')]:
                records.append(run([FC,*flags,'-J',obj,'-I',obj,*INCLUDES,'-c',path,'-o',obj/(name+'.o')]))
                records[-1].update(mode=mode,unit=name)
        # Pristine pinned serial QE HDF5 component, independent of mp/io_base.
        h5=PRIVATE/'hdf5-serial';h5.mkdir(exist_ok=True)
        records.append(run([FC,'-cpp','-D__HDF5','-ffree-line-length-none','-fallow-argument-mismatch',
                            '-O0','-g','-fcheck=all','-J',h5,*INCLUDES,'-c',
                            ROOT/'q-e/Modules/qeh5_module.f90','-o',h5/'qeh5.o']))
        qelib=DFT/'.local/qe-env/lib'
        records.append(run(['/usr/bin/cc','-std=c11','-Wall','-Wextra','-Werror','-O2','-c',
                            HERE/'no_mpi_init.c','-o',h5/'no_mpi_init.o']))
        records.append(run(['/usr/bin/cc','-std=c11','-Wall','-Wextra','-Werror','-O2',HERE/'guard_unit.c',
                            h5/'no_mpi_init.o','-o',PRIVATE/'guard_unit']))
        records.append(run([FC,'-ffree-line-length-none','-fcheck=all','-I',h5,*INCLUDES,
                            HERE/'hdf5_readback.f90',h5/'qeh5.o',h5/'no_mpi_init.o','-Wl,--export-dynamic',
                            '-L',qelib,'-Wl,-rpath,'+str(qelib),
                            '-lhdf5_fortran','-lhdf5','-o',PRIVATE/'hdf5_readback']))
        records.append(run([FC,'-ffree-line-length-none','-fcheck=all','-I',PRIVATE/'stock-objects',*INCLUDES,
                            HERE/'diagnostic_unit.f90',PRIVATE/'stock-objects/qe75_diagnostics.o',
                            '-o',PRIVATE/'diagnostic_unit']))
        # Six core action/energy/ACE bodies are byte-identical; diagnostic hooks
        # live only in aceinit_k and the new adapter. Noninterference remains a
        # source-conditioned claim until the actual matched fixture.
        old=Path(json.loads((HERE.parent/'native_bridge/build_results.json').read_text())['source_directory'])
        baseline=(old/'exx.f90').read_text();updated=(source/'exx.f90').read_text()
        audit={}
        for a,b in [('  SUBROUTINE vexx_k(', '  END SUBROUTINE vexx_k'),
                    ('  FUNCTION exxenergy2_k(', '  END FUNCTION  exxenergy2_k'),
                    ('  SUBROUTINE aceupdate_k(', '  END SUBROUTINE aceupdate_k'),
                    ('  SUBROUTINE vexxace_k(', '  END SUBROUTINE vexxace_k')]:
            def body(text):
                i=text.index(a);j=text.index(b,i)+len(b);return text[i:j]
            if body(baseline)!=body(updated): raise RuntimeError('native arithmetic body changed')
            audit[a.strip()]=True
        report.update(passed=True,arithmetic_source_equality=audit,
                      compiler_sha256=artifact_sha256(FC),
                      serial_qeh5_source_sha256=artifact_sha256(ROOT/'q-e/Modules/qeh5_module.f90'),
                      binaries={name:artifact_sha256(PRIVATE/name) for name in ['abi_worker','hdf5_readback','diagnostic_unit','guard_unit']},
                      maximum_child_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    except Exception as exc:
        report['error']=str(exc)
        raise
    finally:
        (PRIVATE/'build.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 12 native-unit compiles, serial typed ABI and pristine QE HDF5 component built. No PW/HSE/MPI run.')


def link_candidates():
    """Exact previous backend/link recipe, private replacements, never execute."""
    report=json.loads((PRIVATE/'build.json').read_text())
    if not report['passed']: raise RuntimeError('unit build failed; no link')
    info=LinuxGuard(LIB).probe(PRIVATE)
    if info['available_bytes']<11*(1<<30) or memory()['MemAvailable']<16*(1<<30):
        raise RuntimeError('link-only headroom unsafe')
    destination=PRIVATE/'link-only';destination.mkdir(exist_ok=False)
    old=json.loads((HERE.parent/'native_bridge/build_results.json').read_text())
    stock=DFT/'.local/qe-env/lib/libqe_pw.a';stock_sha=artifact_sha256(stock)
    records=[]
    records.append(run(['/usr/bin/cc','-std=c11','-Wall','-Wextra','-Werror','-O2','-c',HERE/'lease_client.c',
                        '-o',destination/'lease_client.o']))
    hashes={}
    for mode in ['stock','stream']:
        folder=destination/mode;folder.mkdir()
        archive=folder/'libqe_pw_readiness.a';shutil.copy2(stock,archive)
        replaced=['exx','electrons','punch','run_pwscf','wfcinit']
        records.append(run(['/usr/bin/ar','d',archive,*[n+'.f90.o' for n in replaced]]))
        paths=[]
        for name in ['exx_checkpoint_state','exx_qstream',*replaced]:
            local=PRIVATE/(mode+'-objects')/(name+'.o')
            if not local.exists(): local=ROOT/'native_bridge'/(mode+'-objects')/(name+'.o')
            path=folder/(name+'.f90.o');shutil.copy2(local,path);paths.append(path)
        for name in ['qe75_native_lease','qe75_diagnostics']:
            path=folder/(name+'.f90.o');shutil.copy2(PRIVATE/(mode+'-objects')/(name+'.o'),path);paths.append(path)
        records.append(run(['/usr/bin/ar','r',archive,*paths]))
        binary=folder/'pw.m5.READINESS_REFUSED'
        command=list(old['records'][-1]['command'])
        command[command.index(str(ROOT/'native_bridge/link-only/libqe_pw_bridge.a'))]=str(archive)
        command.insert(command.index('-Wl,--start-group'),str(destination/'lease_client.o'))
        command[-1]=str(binary);records.append(run(command))
        hashes[mode]={'binary':str(binary),'sha256':artifact_sha256(binary),
                      'objects':{str(p):artifact_sha256(p) for p in paths}}
    if artifact_sha256(stock)!=stock_sha: raise RuntimeError('stock archive changed')
    result={'passed':True,'PW_HSE_MPI_executed':False,'candidates':hashes,'records':records,
            'stock_archive_preserved':True,'maximum_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (PRIVATE/'link.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: both readiness candidates link with typed C lease and native diagnostics; neither executed.')


if __name__=='__main__':
    if sys.argv[1:]==['link-only']: link_candidates()
    elif not sys.argv[1:]: main()
    else: raise RuntimeError('build or explicit link-only; no launch command')
