"""New private root-qualified binaries. Existing stock/archives/results immutable."""
import json,hashlib,shutil,subprocess,time,difflib
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011');NEW=ROOT/'rooted_full_scf_build_20261014'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 qualification=json.loads((HERE/'root_qualification.json').read_text());validation=json.loads((HERE/'validation.json').read_text())
 assert qualification['all_passed'] and validation['passed'] and qualification['candidate_source_sha256']==sha(HERE/'cold_root.f90')
 old=json.loads((BASE/'full_scf_2026-10-13/build_results.json').read_text());previous=json.loads((BASE/'smearing_conditioning_2026-10-13/build_results.json').read_text());NEW.mkdir(mode=0o700,exist_ok=False)
 original=(ROOT/'q-e/PW/src/efermig.f90').read_text()
 s=original.replace('  USE io_global, ONLY : stdout','  USE r07_cold_root, ONLY:strict_root,last_certificate\n  USE io_global, ONLY : stdout,ionode',1).replace('ONLY : inter_pool_comm','ONLY : inter_pool_comm,npool',1)
 anchor='  Elw = 1.0E+8';assert s.count(anchor)==1
 block='''  ! Private R07 cold-only change: certify sign root and refuse ambiguity.
  IF(Ngauss == -1) THEN
    IF(npool/=1) CALL errore('r07_cold_root','qualified one-pool fixture only',1)
    CALL strict_root(et,nbnd,nks,nelec,wk,Degauss,is,isk,Ef,info)
    IF(info/=0) CALL errore('r07_cold_root','untrusted or competing cold root',info)
    efermig=Ef
    IF(ionode) WRITE(stdout,'(A,12(ES26.17E3,1X))') 'R07_COLD_ROOT ',Ef,nelec,last_certificate
    RETURN
  ENDIF
'''
 s=s.replace(anchor,block+anchor,1);(HERE/'efermig.f90').write_text(s)
 (HERE/'solver.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='QE7.5/PW/src/efermig.f90',tofile='PRIVATE/efermig.f90')))
 original=(BASE/'smearing_conditioning_2026-10-13/full_state.f90').read_text();observer=original.replace('  USE ener, ONLY:etot,hwf_energy,ef','  USE r07_cold_root, ONLY:last_certificate\n  USE ener, ONLY:etot,hwf_energy,ef').replace('values(11)','values(21)').replace('tr2_final,ef]','tr2_final,ef,last_certificate]')
 assert observer.count('tr2_final,ef,last_certificate]')==1;(HERE/'full_state.f90').write_text(observer)
 records=[];candidates={};pins={};library=ROOT/'smearing_conditioning_20261013/replay.so'
 for mode in ['control','stream']:
  out=NEW/mode;out.mkdir();archive=out/'libqe_pw_rooted.a';oldarchive=ROOT/'conditioned_full_scf_build_20261013'/mode/'libqe_pw_conditioned.a';pins[str(oldarchive)]=sha(oldarchive);shutil.copy2(oldarchive,archive)
  template=[r['command'] for r in old['records'] if '-c' in r['command'] and Path(r['command'][r['command'].index('-c')+1]).name=='full_state.f90' and str(ROOT/'full_scf_build3_20261013'/mode) in r['command']];assert len(template)==1
  def run(c):
   t=time.monotonic();r=subprocess.run(c,capture_output=True,text=True,timeout=90);records.append(dict(command=c,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,elapsed=time.monotonic()-t));(HERE/'build_results.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
   if r.returncode:raise RuntimeError(r.stderr)
  objects=[]
  for name in ['cold_root','efermig','full_state']:
   c=list(template[0]);c[c.index('-c')+1]=str(HERE/(name+'.f90'));obj=out/(name+'.f90.o');c[c.index('-o')+1]=str(obj);c[c.index('-J')+1]=str(out)
   c[1:1]=['-I',str(out),'-I',str(ROOT/'full_scf_build3_20261013'/mode)]
   run(c);objects.append(obj)
  run(['/usr/bin/ar','r',str(archive),*[str(p) for p in objects]])
  link=[r['command'] for r in previous['records'] if '-o' in r['command'] and r['command'][r['command'].index('-o')+1]==previous['candidates'][mode]['binary']];assert len(link)==1
  c=[str(archive) if x==str(oldarchive) else x for x in link[0]];binary=out/('pw.'+mode+'.rooted');c[c.index('-o')+1]=str(binary);run(c)
  names=subprocess.check_output(['/usr/bin/ar','t',str(archive)],text=True).splitlines();oldnames=subprocess.check_output(['/usr/bin/ar','t',str(oldarchive)],text=True).splitlines();changed=[];added=[]
  for name in names:
   b=subprocess.check_output(['/usr/bin/ar','p',str(archive),name])
   if name not in oldnames:added.append(name)
   elif b!=subprocess.check_output(['/usr/bin/ar','p',str(oldarchive),name]):changed.append(name)
  assert sorted(changed)==['efermig.f90.o','full_state.f90.o'] and added==['cold_root.f90.o'],(changed,added)
  dependencies={}
  for line in subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True).splitlines():
   for v in line.split():
    p=Path(v)
    if p.is_absolute() and p.exists():dependencies[str(p.resolve())]=sha(p.resolve())
  assert dependencies==previous['candidates'][mode]['backends']
  candidates[mode]=dict(binary=str(binary),sha256=sha(binary),backends=dependencies,archive_sha256=sha(archive),changed_archive_members=changed,added_archive_members=added)
 for p in [HERE/'cold_root.f90',HERE/'efermig.f90',HERE/'full_state.f90',library]:pins[str(p)]=sha(p)
 (HERE/'build_results.json').write_text(json.dumps(dict(passed=True,records=records,candidates=candidates,source_and_exchange_archive_pins=pins,exchange_wave_density_ACE_lease_objects_byte_identical=True,occupation_solver_changed=True,native_executed=False),indent=2)+'\n');print('PRIVATE rooted native links passed: only Fermi solver + observer differ')
if __name__=='__main__':main()
