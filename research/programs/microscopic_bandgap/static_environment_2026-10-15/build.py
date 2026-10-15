"""One private run driver replacement; untouched stock Hamiltonian objects."""
from pathlib import Path
import json,hashlib,subprocess,shutil,difflib,time
HERE=Path(__file__).resolve().parent;DFT=Path('/home/User/opencode_workspace/DFT');BASE=DFT/'.local/qe75_lowram_20261011';NEW=BASE/'p16h_20261015/build2'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if NEW.exists():raise FileExistsError('fresh build only')
    NEW.mkdir(parents=True);old=BASE/'h8c_20261015/build1/source/pristine_run_pwscf.f90';source=old.read_text();anchor='  CALL init_run()\n  !\n  !  read external force';assert source.count(anchor)==1
    text=source.replace(anchor,'  CALL init_run()\n  CALL r07_static_H()\n  exit_status=0\n  CALL qexsd_set_status(exit_status)\n  RETURN ! read-only saved-charge operator; no electrons/punch\n  !\n  !  read external force')+'\n'+(HERE/'native_probe.inc').read_text();src=NEW/'run_pwscf.f90';src.write_text(text)
    t=json.loads((BASE/'link_result.json').read_text());cmd=[x for x in t['main_compile'] if not x.startswith('-O')];cmd+=['-O2','-fno-fast-math'];cmd[cmd.index('-J')+1]=str(NEW);cmd[cmd.index('-c')+1]=str(src);cmd[cmd.index('-o')+1]=str(NEW/'run_pwscf.f90.o');records=[]
    def run(c):
        start=time.monotonic();v=subprocess.run(c,capture_output=True,text=True,timeout=120);records.append(dict(command=c,returncode=v.returncode,elapsed_s=time.monotonic()-start,stdout=v.stdout,stderr=v.stderr));(HERE/'build_result.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n');assert v.returncode==0,v.stderr
    run(cmd);stock=DFT/'.local/qe-env/lib/libqe_pw.a';pin=sha(stock);lib=NEW/'libqe_pw_static.a';shutil.copy2(stock,lib);run(['/usr/bin/ar','r',str(lib),str(NEW/'run_pwscf.f90.o')]);link=[str(lib) if x.endswith('libqe_pw_candidate.a') else x for x in t['link_command']];elf=NEW/'pw.static';link[link.index('-o')+1]=str(elf);run(link);assert sha(stock)==pin
    backends={}
    for line in subprocess.check_output(['/usr/bin/ldd',str(elf)],text=True).splitlines():
        for word in line.split():
            p=Path(word)
            if p.is_absolute() and p.exists():backends[str(p.resolve())]=sha(p.resolve())
    (HERE/'source.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True),text.splitlines(True),fromfile='pristine/run_pwscf.f90',tofile='private/run_pwscf.f90')))
    (HERE/'build_result.json').write_text(json.dumps(dict(passed=True,binary=str(elf),binary_sha256=sha(elf),stock_archive_sha256=pin,records=records,source_pins={str(p):sha(p) for p in [old,src,HERE/'native_probe.inc',HERE/'build.py',BASE/'q-e/PW/src/init_run.f90',BASE/'q-e/PW/src/potinit.f90',BASE/'q-e/PW/src/h_psi.f90',BASE/'q-e/PW/src/wfcinit.f90']},backends=backends,no_native_execution=True,only_replaced_archive_member='run_pwscf.f90.o'),indent=2)+'\n');print('PASS private static driver compile/link; stock Hamiltonian objects unchanged')


if __name__=='__main__':main()
