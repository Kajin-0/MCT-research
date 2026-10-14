"""Incremental private observer build; old native exchange and solver objects unchanged."""
import json,hashlib,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011')
NEW=ROOT/'conditioned_full_scf_build_20261013'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 old=json.loads((BASE/'full_scf_2026-10-13/build_results.json').read_text());NEW.mkdir(mode=0o700,exist_ok=False)
 original=(BASE/'full_scf_2026-10-13/full_state.f90').read_text()
 s=original.replace('ONLY:etot,hwf_energy','ONLY:etot,hwf_energy,ef').replace('values(10)','values(11)').replace('ethr,tr2_final]','ethr,tr2_final,ef]')
 assert s.count('tr2_final,ef]')==1
 (HERE/'full_state.f90').write_text(s)
 records=[];candidates={};pins={}
 for mode in ['control','stream']:
  out=NEW/mode;out.mkdir()
  archive=out/'libqe_pw_conditioned.a';oldarchive=ROOT/'full_scf_build3_20261013'/mode/'libqe_pw_full_scf.a';pins[str(oldarchive)]=sha(oldarchive)
  shutil.copy2(oldarchive,archive)
  templates=[r['command'] for r in old['records'] if '-c' in r['command'] and Path(r['command'][r['command'].index('-c')+1]).name=='full_state.f90' and str(ROOT/'full_scf_build3_20261013'/mode) in r['command']]
  assert len(templates)==1
  c=list(templates[0]);c[c.index('-c')+1]=str(HERE/'full_state.f90');c[c.index('-o')+1]=str(out/'full_state.f90.o');c[c.index('-J')+1]=str(out)
  c[1:1]=['-I',str(ROOT/'full_scf_build3_20261013'/mode)]
  def run(c):
   t=time.monotonic();r=subprocess.run(c,capture_output=True,text=True,timeout=90);records.append(dict(command=c,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,elapsed=time.monotonic()-t))
   (HERE/'build_results.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
   if r.returncode:raise RuntimeError(r.stderr)
  run(c);run(['/usr/bin/ar','r',str(archive),str(out/'full_state.f90.o')])
  link=[r['command'] for r in old['records'] if '-o' in r['command'] and r['command'][r['command'].index('-o')+1]==old['candidates'][mode]['binary']];assert len(link)==1
  c=[str(archive) if x==str(oldarchive) else x for x in link[0]];binary=out/('pw.'+mode+'.conditioned');c[c.index('-o')+1]=str(binary);run(c)
  # Compare archive contents: only observer object may change.
  names=subprocess.check_output(['/usr/bin/ar','t',str(archive)],text=True).splitlines();changed=[]
  for name in names:
   a=subprocess.check_output(['/usr/bin/ar','p',str(oldarchive),name]);b=subprocess.check_output(['/usr/bin/ar','p',str(archive),name])
   if a!=b:changed.append(name)
  assert changed==['full_state.f90.o'],changed
  dependencies={}
  for line in subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True).splitlines():
   for v in line.split():
    p=Path(v)
    if p.is_absolute() and p.exists():dependencies[str(p.resolve())]=sha(p.resolve())
  assert dependencies==old['candidates'][mode]['backends']
  candidates[mode]=dict(binary=str(binary),sha256=sha(binary),backends=dependencies,archive_sha256=sha(archive),changed_archive_members=changed)
 pins[str(HERE/'full_state.f90')]=sha(HERE/'full_state.f90');pins[str(ROOT/'smearing_conditioning_20261013/replay.so')]=sha(ROOT/'smearing_conditioning_20261013/replay.so')
 (HERE/'build_results.json').write_text(json.dumps(dict(passed=True,records=records,candidates=candidates,source_and_exchange_archive_pins=pins,all_exchange_solver_lease_objects_byte_identical=True,native_executed=False),indent=2)+'\n')
 print('Only full_state observer changed; both private links PASS')
if __name__=='__main__':main()
