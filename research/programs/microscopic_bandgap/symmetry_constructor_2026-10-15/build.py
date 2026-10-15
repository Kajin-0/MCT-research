"""Two private objects; retain direct-exchange arithmetic and original binaries."""
import difflib,hashlib,json,re,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT');ROOT=DFT/'.local/qe75_lowram_20261011'
OLD=ROOT/'h8c_20261015/build1/source';NEW=ROOT/'h8s_20261015/b1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    if NEW.exists():raise FileExistsError('preserve private candidate')
    NEW.mkdir(parents=True,mode=0o700);src=NEW/'source';src.mkdir();records=[]
    exx=(OLD/'exx.f90').read_text().replace('/h8c_20261015/','/h8s_20261015/')
    exx=exx.replace(' CONTAINS',' CONTAINS\n'+(HERE/'probe_native.inc').read_text(),1)
    run=(OLD/'pristine_run_pwscf.f90').read_text()
    run=run.replace('  USE kinds,','  USE exx, ONLY:r07_fixed_TR_probe\n  USE kinds,',1)
    anchor='  CALL init_run()\n  !\n  !  read external force'
    assert run.count(anchor)==1
    run=run.replace(anchor,"  CALL init_run()\n  CALL r07_fixed_TR_probe()\n  exit_status=0\n  CALL qexsd_set_status(exit_status)\n  RETURN ! fixed operator only; NO electrons or SCF punch\n  !\n  !  read external force")
    patches=[]
    for name,text in [('exx.f90',exx),('run_pwscf.f90',run)]:
        (src/name).write_text(text)
        before=(OLD/name).read_text() if name=='exx.f90' else (OLD/('pristine_'+name)).read_text()
        patches+=list(difflib.unified_diff(before.splitlines(True),text.splitlines(True),fromfile='accepted/'+name,tofile='fixedTR/'+name))
    for name in ['vexx_k','vexx','vexxace_k','aceupdate_k']:
        routine=lambda t:re.search(r'^ *SUBROUTINE +'+name+r' *\([\s\S]*?^ *END SUBROUTINE +'+name+r'\b',t,re.M|re.I).group()
        assert routine(exx)==routine((OLD/'exx.f90').read_text())
    template=json.loads((ROOT/'link_result.json').read_text())
    def call(cmd):
        start=time.monotonic();v=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
        records.append(dict(command=cmd,returncode=v.returncode,elapsed_s=time.monotonic()-start,stdout=v.stdout,stderr=v.stderr))
        (HERE/'build_results.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
        if v.returncode:raise RuntimeError(v.stderr)
    for name in ['exx.f90','run_pwscf.f90']:
        c=[v for v in template['main_compile'] if not v.startswith('-O')];c[1:1]=['-I',str(NEW)]
        c+=['-O2','-fno-fast-math'];c[c.index('-J')+1]=str(NEW);c[c.index('-c')+1]=str(src/name);c[c.index('-o')+1]=str(NEW/(name+'.o'));call(c)
    stock=DFT/'.local/qe-env/lib/libqe_pw.a';pin=sha(stock);archive=NEW/'libqe_pw_symmetry.a';shutil.copy2(stock,archive)
    call(['/usr/bin/ar','r',str(archive),*[str(NEW/(name+'.o')) for name in ['exx.f90','run_pwscf.f90']]])
    binary=NEW/'pw.hse8.symmetry';c=[str(archive) if v.endswith('libqe_pw_candidate.a') else v for v in template['link_command']];c[c.index('-o')+1]=str(binary);call(c)
    backends={}
    for line in subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True).splitlines():
        for word in line.split():
            f=Path(word)
            if f.is_absolute() and f.exists():backends[str(f.resolve())]=sha(f.resolve())
    assert sha(stock)==pin
    (HERE/'native_changes.patch').write_text(''.join(patches))
    result=dict(passed=True,records=records,binary=str(binary),binary_sha256=sha(binary),native_executed=False,
        source_pins={str(f):sha(f) for f in [*src.iterdir(),OLD/'exx.f90',OLD/'pristine_run_pwscf.f90',HERE/'probe_native.inc']},
        backends=backends,stock_archive_sha256=pin,unchanged_arithmetic=['vexx_k','vexx','vexxace_k','aceupdate_k'],
        no_electrons_or_ACE_build=True,no_SCF_save_or_restart_claim=True)
    (HERE/'build_results.json').write_text(json.dumps(result,indent=2)+'\n');print('Private exx/run compile and link PASS; no native invocation')

if __name__=='__main__':main()
