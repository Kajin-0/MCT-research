"""Private diagnostic objects; no stock modification or native execution."""
import difflib,hashlib,json,re,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;DFT=Path('/home/User/opencode_workspace/DFT');ROOT=DFT/'.local/qe75_lowram_20261011'
OLD=ROOT/'h8c_20261015/build1/source';NEW=ROOT/'h8u_20261015/build1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if NEW.exists():raise FileExistsError('preserve private build attempt')
    NEW.mkdir(parents=True,mode=0o700);src=NEW/'source';src.mkdir();records=[]
    exx=(OLD/'exx.f90').read_text().replace('/h8c_20261015/','/h8u_20261015/')
    exx=exx.replace(' CONTAINS',' CONTAINS\n'+(HERE/'probe_native.inc').read_text(),1)
    run=(OLD/'pristine_run_pwscf.f90').read_text().replace('  USE kinds,','  USE exx, ONLY:r07_same_density_H\n  USE kinds,',1)
    anchor='  CALL init_run()\n  !\n  !  read external force';assert run.count(anchor)==1
    run=run.replace(anchor,'  CALL init_run()\n  CALL r07_same_density_H()\n  exit_status=0\n  CALL qexsd_set_status(exit_status)\n  RETURN ! fixed trial only: no electrons, ACE or SCF punch\n  !\n  !  read external force')
    patch=[]
    for name,text in [('exx.f90',exx),('run_pwscf.f90',run)]:
        (src/name).write_text(text);before=(OLD/(name if name=='exx.f90' else 'pristine_'+name)).read_text();patch+=list(difflib.unified_diff(before.splitlines(True),text.splitlines(True),fromfile='accepted/'+name,tofile='sameD/'+name))
    for name in ['vexx_k','vexx','vexxace_k','aceupdate_k','exxinit']:
        routine=lambda t:re.search(r'^ *SUBROUTINE +'+name+r' *\([\s\S]*?^ *END SUBROUTINE +'+name+r'\b',t,re.M|re.I).group()
        assert routine(exx)==routine((OLD/'exx.f90').read_text())
    template=json.loads((ROOT/'link_result.json').read_text())
    def call(cmd):
        start=time.monotonic();v=subprocess.run(cmd,capture_output=True,text=True,timeout=120);records.append(dict(command=cmd,returncode=v.returncode,elapsed_s=time.monotonic()-start,stdout=v.stdout,stderr=v.stderr));(HERE/'build_results.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
        if v.returncode:raise RuntimeError(v.stderr)
    for name in ['exx.f90','run_pwscf.f90']:
        c=[v for v in template['main_compile'] if not v.startswith('-O')];c[1:1]=['-I',str(NEW)];c+=['-O2','-fno-fast-math'];c[c.index('-J')+1]=str(NEW);c[c.index('-c')+1]=str(src/name);c[c.index('-o')+1]=str(NEW/(name+'.o'));call(c)
    stock=DFT/'.local/qe-env/lib/libqe_pw.a';pin=sha(stock);archive=NEW/'libqe_pw_sameD.a';shutil.copy2(stock,archive)
    call(['/usr/bin/ar','r',str(archive),*[str(NEW/(n+'.o')) for n in ['exx.f90','run_pwscf.f90']]])
    binary=NEW/'pw.hse8.sameD';cmd=[str(archive) if v.endswith('libqe_pw_candidate.a') else v for v in template['link_command']];cmd[cmd.index('-o')+1]=str(binary);call(cmd)
    backends={}
    for line in subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True).splitlines():
        for word in line.split():
            p=Path(word)
            if p.is_absolute() and p.exists():backends[str(p.resolve())]=sha(p.resolve())
    assert sha(stock)==pin
    (HERE/'native_changes.patch').write_text(''.join(patch))
    result=dict(passed=True,records=records,binary=str(binary),binary_sha256=sha(binary),source_pins={str(p):sha(p) for p in [*src.iterdir(),OLD/'exx.f90',OLD/'pristine_run_pwscf.f90',HERE/'probe_native.inc']},backends=backends,stock_archive_sha256=pin,native_executed=False,unchanged_arithmetic=['vexx_k','vexx','vexxace_k','aceupdate_k','exxinit'],no_SCF_or_ACE=True)
    (HERE/'build_results.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS private compile/link and arithmetic identity; no native launch')


if __name__=='__main__':main()
