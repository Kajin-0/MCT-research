"""Minimal private source-matched firstACE build; no QE/MPI execution."""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import time

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'qe75_streaming_2026-10-11'
DFT=Path('/home/User/opencode_workspace/DFT')
ROOT=DFT/'.local/qe75_lowram_20261011'
NEW=ROOT/'h8c_20261015'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if not NEW.exists():NEW.mkdir(mode=0o700)
    out=NEW/'build1'
    if out.exists() and (list(out.glob('*.o')) or list(out.glob('pw.*'))):raise FileExistsError('preserve compiledcandidate')
    out.mkdir(exist_ok=True);src=out/'source';src.mkdir(exist_ok=True)
    records=[];patch=[];originals={}
    def run(command):
        start=time.monotonic();v=subprocess.run(command,capture_output=True,text=True,timeout=120)
        records.append(dict(command=command,returncode=v.returncode,stdout=v.stdout,stderr=v.stderr,elapsed_s=time.monotonic()-start))
        (HERE/'build_results.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
        if v.returncode:raise RuntimeError(v.stderr)
    for name in ['exx.f90','electrons.f90','run_pwscf.f90']:
        text=subprocess.check_output(['git','-C',str(ROOT/'q-e'),'show','HEAD:PW/src/'+name],text=True)
        originals[name]=text;(src/('pristine_'+name)).write_text(text)
    manifest=json.loads((BASE/'source_manifest.json').read_text())
    assert sha(src/'pristine_exx.f90')==manifest['files']['exx.f90']['sha256']
    exx=originals['exx.f90']
    exx=exx.replace(' CONTAINS',' LOGICAL,SAVE::pilot_done=.FALSE.\n INTEGER,SAVE::pilot_cycle=0\n COMPLEX(DP),ALLOCATABLE,PRIVATE::pilot_probe(:,:)\n CONTAINS\n'+(HERE/'pilot_native.inc').read_text(),1)
    a=exx.index('  SUBROUTINE aceinit_k(');b=exx.index('  END SUBROUTINE aceinit_k',a)
    body=exx[a:b]
    anchor="                      phi, xitmp, mexx, exxe )\n    ENDIF"
    assert body.count(anchor)==1
    body=body.replace(anchor,anchor.replace('\n    ENDIF','\n      CALL pilot_before(nnpw,nbnd,phi,xitmp,mexx,exxe)\n    ENDIF'))
    anchor='    DEALLOCATE( mexx )';assert body.count(anchor)==1
    body=body.replace(anchor,'    CALL pilot_after(nnpw,nbnd,phi,xitmp,becpsi)\n'+anchor)
    exx=exx[:a]+body+exx[b:]
    electrons=originals['electrons.f90']
    electrons=electrons.replace('  USE kinds,','  USE exx, ONLY:pilot_begin,pilot_local,pilot_finish,pilot_done\n  USE kinds,',1)
    anchor='\n        CALL exxinit(DoLoc)';assert electrons.count(anchor)==2
    electrons=electrons.replace(anchor,'\n        CALL pilot_begin()\n        CALL pilot_local(0)'+anchor)
    anchor='             nspin, doublegrid )\n        !\n     ELSE';assert electrons.count(anchor)==1
    electrons=electrons.replace(anchor,'             nspin, doublegrid )\n        CALL pilot_local(1)\n        CALL pilot_finish(exxen,fock2,etot)\n        ! No stop: allow exactly one hybrid inner solve.\n        !\n     ELSE')
    anchor="        IF ( dexx < tr2_final ) THEN\n           IF ( do_makov_payne )"
    assert electrons.count(anchor)==1
    electrons=electrons.replace(anchor,"        CALL pilot_local(1)\n        CALL pilot_finish(exxen,fock2,etot)\n        IF(pilot_done.AND.dexx>=tr2_final)THEN\n          conv_elec=.FALSE. ! exhausted8 budget is not convergence\n          RETURN\n        ENDIF\n"+anchor)
    runpw=originals['run_pwscf.f90']
    runpw=runpw.replace('  USE kinds,','  USE exx, ONLY:pilot_done,pilot_publish\n  USE kinds,',1)
    anchor='     ! ... code stopped by user or not converged'
    assert runpw.count(anchor)==1
    runpw=runpw.replace(anchor,"     IF(pilot_done)THEN\n        exit_status=0 ! diagnostic completion only; conv_elec remainsFALSE\n        CALL qexsd_set_status(exit_status)\n        CALL punch('all')\n        CALL pilot_publish()\n        RETURN\n     ENDIF\n     !\n"+anchor)
    modified={'exx.f90':exx,'electrons.f90':electrons,'run_pwscf.f90':runpw}
    # Source arithmetic functions untouched; only firstACE observation points differ.
    def routine(text,start,end):
        name=start.split()[1].split('(')[0]
        first=re.search(r'^ *SUBROUTINE +'+name+r' *\(',text,re.M|re.I).start()
        last=re.search(r'^ *END SUBROUTINE +'+name+r'\b',text[first:],re.M|re.I).end()+first
        return text[first:last]
    for name in ['vexx_k','aceupdate_k','vexxace_k']:
        start=('  SUBROUTINE '+name+'(');end='  END SUBROUTINE '+name
        assert routine(originals['exx.f90'],start,end)==routine(exx,start,end)
    for name,text in modified.items():
        (src/name).write_text(text)
        patch.extend(difflib.unified_diff(originals[name].splitlines(True),text.splitlines(True),fromfile='pristine/'+name,tofile='pilot/'+name))
    template=json.loads((ROOT/'link_result.json').read_text());compile_template=template['main_compile']
    for name in ['exx.f90','electrons.f90','run_pwscf.f90']:
        c=[v for v in compile_template if not v.startswith('-O')]
        c[1:1]=['-I',str(out)];c+=['-O2','-fno-fast-math']
        c[c.index('-J')+1]=str(out);c[c.index('-c')+1]=str(src/name);c[c.index('-o')+1]=str(out/(name+'.o'))
        run(c)
    archive=out/'libqe_pw_pilot.a';stock=DFT/'.local/qe-env/lib/libqe_pw.a';stockhash=sha(stock);shutil.copy2(stock,archive)
    listing=subprocess.check_output(['/usr/bin/ar','t',str(archive)],text=True).splitlines()
    for name in modified:
        assert listing.count(name+'.o')==1
    run(['/usr/bin/ar','r',str(archive),*[str(out/(name+'.o')) for name in modified]])
    c=template['link_command'];binary=out/'pw.hse8.outer'
    c=[str(archive) if v.endswith('libqe_pw_candidate.a') else v for v in c]
    c[c.index('-o')+1]=str(binary);run(c)
    backends={}
    for line in subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True).splitlines():
        for word in line.split():
            f=Path(word)
            if f.is_absolute() and f.exists():backends[str(f.resolve())]=sha(f.resolve())
    assert sha(stock)==stockhash
    (HERE/'native_changes.patch').write_text(''.join(patch))
    result=dict(passed=True,native_executed=False,records=records,binary=str(binary),binary_sha256=sha(binary),
        compiler=compile_template[0],compiler_sha256=sha(compile_template[0]),backends=backends,stock_archive_sha256=stockhash,
        upstream_commit=manifest['upstream_git_commit'],modified_objects=list(modified),
        arithmetic_byte_unchanged=['vexx_k','aceupdate_k','vexxace_k'],
        source_pins={str(f):sha(f) for f in src.iterdir()},observer_include_sha256=sha(HERE/'pilot_native.inc'))
    (HERE/'build_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Three private object compiles and link PASS; no native QE run')


if __name__=='__main__':main()
