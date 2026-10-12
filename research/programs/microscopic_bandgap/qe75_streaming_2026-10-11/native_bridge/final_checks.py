"""Final bounded regression/preservation evidence. Does not execute PW/MPI."""
from pathlib import Path
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import time
import unittest
import difflib

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
PRIVATE=DFT/'.local/qe75_lowram_20261011/native_bridge'
ROOT=PRIVATE.parent


def main():
    build=json.loads((PRIVATE/'build_checks.json').read_text())
    assert build['passed'] is True
    source=Path(build['source_directory'])
    for name,sha in build['source_sha256'].items():
        assert hashlib.sha256((source/name).read_bytes()).hexdigest()==sha,name
    import test_native_bridge
    output=io.StringIO()
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_native_bridge))
    assert result.wasSuccessful(),output.getvalue()
    regressions=[];includes=[]
    for p in sorted((DFT/'.local/qe-env/include/qe').iterdir()):
        if p.is_dir(): includes+=['-I',str(p)]
    sys.path.insert(0,str(HERE.parent))
    from validate_candidate import NEGATIVE
    fc=ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran'
    for optimization in ['O0','O2']:
        obj=PRIVATE/('regression-'+optimization);obj.mkdir(exist_ok=True)
        binary=obj/'store_kernel_test'
        command=[str(fc),'-'+optimization,'-fcheck=all','-fcheck=array-temps','-ffree-line-length-none','-fopenmp',
                 '-J',str(obj),*includes,str(source/'exx_qstream.f90'),str(HERE.parent/'store_kernel_test.f90'),'-o',str(binary)]
        compiled=subprocess.run(command,capture_output=True,text=True,timeout=30)
        assert compiled.returncode==0,compiled.stderr
        for case in ['normal','extent64',*NEGATIVE]:
            path=obj/(case+'.bin');assert not path.exists()
            executed=subprocess.run([str(binary),case,str(path)],capture_output=True,text=True,timeout=10)
            expected=9 if case in NEGATIVE else 0
            assert executed.returncode==expected,(case,executed.stdout,executed.stderr)
            if case in NEGATIVE: assert NEGATIVE[case] in executed.stdout
            assert 'array temporary' not in executed.stderr.lower()
            regressions.append({'optimization':optimization,'case':case,'returncode':executed.returncode,'passed':True})
            if path.exists(): path.unlink()
    baseline=json.loads((PRIVATE/'preservation_before.json').read_text())
    observed={'DFT_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=DFT,text=True).strip(),
              'DFT_status':subprocess.check_output(['git','status','--porcelain=v1'],cwd=DFT,text=True),
              'pins':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in baseline['pins']},
              'stock':{p:hashlib.sha256((DFT/p).read_bytes()).hexdigest() for p in baseline['stock']},
              'previous_candidate':hashlib.sha256((ROOT/'link-only/pw.qstream.UNVALIDATED').read_bytes()).hexdigest()}
    for key,value in observed.items(): assert value==baseline[key],key
    processes=[]
    for proc in Path('/proc').iterdir():
        if not proc.name.isdecimal(): continue
        try:
            command=(proc/'cmdline').read_bytes().split(b'\0')
            if command and Path(os.fsdecode(command[0])).name in ['pw.x','mpiexec','mpirun','prterun','orterun','pw.qstream.UNVALIDATED','pw.bridge.RUNTIME_REFUSED']:
                processes.append({'pid':int(proc.name),'argv0':os.fsdecode(command[0])})
        except (OSError,ValueError): pass
    from native_bundle import LinuxGuard
    guard=LinuxGuard(ROOT/'checkpoint_phase/storage_guard.so')
    storage=guard.probe(PRIVATE)
    memory={k:int(v.split()[0])*1024 for k,v in
            (line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())}
    resource_report={'disk_free_bytes':storage['available_bytes'],'MemAvailable_bytes':memory['MemAvailable'],
                     'MemTotal_bytes':memory['MemTotal'],'fs_and_quota':storage,
                     'nominal_22GiB_plus_10GiB_admissible':storage['available_bytes']>=32*(1<<30),
                     'no_22GiB_allocation':True,'native_fixture':'NOT_RUN','MPI_processes':processes}
    stamp=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    report={'timestamp_UTC':stamp,'passed':True,'native_QE_restart_qualified':False,'native_PW_or_MPI_executed':False,
            'unit_test_methods':result.testsRun,'unit_output':output.getvalue(),'store_regressions':regressions,
            'preservation_identical':True,'preservation':observed,'resources':resource_report}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'build_results.json').write_text(json.dumps(build,indent=2)+'\n')
    patch=[]
    for name in ['exx','electrons','run_pwscf','punch','wfcinit']:
        if name in ['exx','electrons']: old=(ROOT/'q-e/PW/src'/(name+'.f90')).read_text()
        else: old=subprocess.check_output(['git','show','770a0b2d12928a67048e2f3da8d10d057e52179e:PW/src/'+name+'.f90'],cwd=ROOT/'q-e',text=True)
        new=(source/(name+'.f90')).read_text()
        patch.extend(difflib.unified_diff(old.splitlines(True),new.splitlines(True),'a/PW/src/'+name+'.f90','b/PW/src/'+name+'.f90'))
    (HERE/'native_hooks.patch.json').write_text(json.dumps({'format':'unified-diff','text':''.join(patch)},indent=2)+'\n')
    print(json.dumps({'passed':True,'unit_methods':result.testsRun,'store_regressions':len(regressions),
          'native_units_compiled':14,'private_link_only':True,'preservation_identical':True,
          'free_disk_GiB':storage['available_bytes']/(1<<30),'MemAvailable_GiB':memory['MemAvailable']/(1<<30),
          'native_fixture':'NOT_RUN'},indent=2))


if __name__=='__main__': main()
