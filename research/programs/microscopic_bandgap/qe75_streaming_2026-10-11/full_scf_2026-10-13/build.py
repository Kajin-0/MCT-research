"""Private fresh full-SCF build. No run; no fixed-operator source reexecution."""
from pathlib import Path
import json,hashlib,shutil,subprocess,time,difflib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011');NEW=ROOT/'full_scf_build3_20261013'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 NEW.mkdir(mode=0o700,exist_ok=False);src=NEW/'source';src.mkdir();records=[];pins={};candidates={};patches=[]
 old=json.loads((BASE/'native_pair_2026-10-13/build_results.json').read_text())['records']
 link=json.loads((BASE/'native_pair_execution_2026-10-13/runtime_build_results.json').read_text())['records']
 def run(c):
  t=time.monotonic();p=subprocess.run(c,capture_output=True,text=True,timeout=120);records.append(dict(command=c,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,wall_seconds=time.monotonic()-t))
  (HERE/'build_results.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
  if p.returncode:raise RuntimeError(p.stderr)
 lease=(ROOT/'native_pair_20261013/v3/source/native_lease.f90').read_text().replace('4_c_int','5_c_int').replace('stage==7)','stage==7 .OR. stage==8 .OR. stage==10)')
 (src/'native_lease.f90').write_text(lease)
 client=(ROOT/'first_ace_transport_fix_20261013/lease_client.c').read_text().replace('action!=7)','action!=7&&action!=8&&action!=10)').replace('(required_scope!=1&&required_scope!=2&&required_scope!=4)','(required_scope!=5)').replace('action>=4&&required_scope!=4','action>=4&&required_scope!=5')
 (src/'lease_client.c').write_text(client)
 run(['/usr/bin/cc','-std=c11','-Wall','-Wextra','-Werror','-O2','-c',str(src/'lease_client.c'),'-o',str(NEW/'lease_client.o')])
 templates={}
 for f in (BASE/'m5_readiness').glob('*.json'):
  d=json.loads(f.read_text())
  for r in d.get('records',[]) if isinstance(d,dict) else []:
   c=r.get('command',[])
   if '-c' in c:
    n=Path(c[c.index('-c')+1]).name
    if n in ['electrons.f90','punch.f90','run_pwscf.f90']:templates[n]=c
 for mode,idx,basearchive,originalexx in [('control',3,ROOT/'native_pair_20261013/v3/stock/libqe_pw_pair.a',ROOT/'native_pair_20261013/v3/source/exx.f90'),('stream',9,ROOT/'fresh_scope4_fix_20261013/libqe_pw_pair.a',ROOT/'fresh_scope4_fix_20261013/exx.f90')]:
  out=NEW/mode;out.mkdir();original=originalexx.read_text();exx=original
  # Diagnostic capture/stop is retired ONLY in new private full-SCF source.
  assert exx.count("    CALL errore('r07_first_ace','first ACE captured; intentional fixture stop, not SCF',85)")==1
  exx=exx.replace("    CALL native_phase(6)\n    CALL errore('r07_first_ace','first ACE captured; intentional fixture stop, not SCF',85)",'')
  # Avoid extra off-span Fock/ACE diagnostics (already independently qualified).
  exx=exx.replace('    capture=.NOT.qdiag_seen(current_k)','    capture=.FALSE.')
  exx=exx.replace(' CONTAINS',' LOGICAL,PRIVATE::full_fft_seen=.FALSE.\n INTEGER,PRIVATE::full_store_generation=0\n CONTAINS',1)
  exx=exx.replace('    CALL qe75_capture_fft(dfftt)','    IF(.NOT.full_fft_seen) THEN\n      CALL qe75_capture_fft(dfftt)\n      full_fft_seen=.TRUE.\n    ENDIF')
  if mode=='stream':
   exx=exx.replace("    IF(action=='pre_import') THEN", "    IF(action=='post_punch') THEN\n      CALL native_check()\n      RETURN ! fresh capture only: no qualified restart publication\n    ENDIF\n    IF(action=='pre_import') THEN")
   exx=exx.replace('    CHARACTER(32) :: rank\n    CHARACTER(1024) :: path\n    WRITE(rank', '    CHARACTER(32) :: rank,generation\n    CHARACTER(1024) :: path\n    IF(full_store_generation>=20) CALL errore(\'qbridge\',\'outer generation cap\',1)\n    full_store_generation=full_store_generation+1\n    WRITE(generation,\'(I0)\') full_store_generation\n    WRITE(rank',1)
   exx=exx.replace("'.stream_request.'//TRIM(rank)","'.stream_request.'//TRIM(generation)//'.'//TRIM(rank)",1)
   exx=exx.replace("    CALL native_phase(7)\n  END SUBROUTINE", "    CALL native_phase(7)\n  END SUBROUTINE",1)
  exxp=src/(mode+'_exx.f90');exxp.write_text(exx)
  patches+=list(difflib.unified_diff(original.splitlines(True),exx.splitlines(True),fromfile=str(originalexx),tofile=str(exxp)))
  def compile(template,p,obj):
   c=[x for x in template if mode=='stream' or x!='-D__EXX_QSTREAM']
   # Same safe optimization for both members, no fast-math, all bounds checks.
   c=[x for x in c if not x.startswith('-O')];c+=['-O2','-fno-fast-math','-D__QE75_FULL_SCF']
   c[1:1]=['-I',str(out)];c[c.index('-J')+1]=str(out);c[c.index('-c')+1]=str(p);c[c.index('-o')+1]=str(obj);run(c)
  compile(old[1 if mode=='control' else 7]['command'],src/'native_lease.f90',out/'qe75_native_lease.f90.o')
  compile(old[idx]['command'],exxp,out/'exx.f90.o')
  compile(old[idx]['command'],HERE/'full_state.f90',out/'full_state.f90.o')
  modified=[]
  for n in ['electrons.f90','punch.f90','run_pwscf.f90']:
   original=(ROOT/'m5_readiness/source-retry1'/n).read_text();s=original
   if n=='electrons.f90':
    s=s.replace('  USE kinds,','  USE qe75_full_state, ONLY:full_observe\n  USE kinds,',1)
    anchor='             nspin, doublegrid )\n        !\n     ELSE';assert s.count(anchor)==1
    s=s.replace(anchor,'             nspin, doublegrid )\n        CALL full_observe(iter,1,tr2_final)\n        !\n     ELSE',1)
    anchor='        exxen = 0.5D0*fock2 ';assert s.count(anchor)==1
    s=s.replace(anchor,anchor+'\n        CALL full_observe(iter,1,tr2_final)')
   if n=='punch.f90':
    s=s.replace('  USE io_global,','  USE qe75_full_state, ONLY:full_observe\n  USE kinds, ONLY:DP\n  USE io_global,',1)
    anchor='  IF ( la2F ) CALL a2Fsave()';assert s.count(anchor)==1
    s=s.replace(anchor,anchor+"\n  IF(TRIM(what)=='all') CALL full_observe(0,2,0._DP)")
   p=src/(mode+'_'+n);p.write_text(s);pins[str(ROOT/'m5_readiness/source-retry1'/n)]=sha(ROOT/'m5_readiness/source-retry1'/n)
   patches+=list(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile=n,tofile=str(p)))
   compile(templates.get(n,old[idx]['command']),p,out/n.replace('.f90','.f90.o'));modified.append(out/n.replace('.f90','.f90.o'))
  archive=out/'libqe_pw_full_scf.a';shutil.copy2(basearchive,archive);pins[str(basearchive)]=sha(basearchive);pins[str(originalexx)]=sha(originalexx)
  run(['/usr/bin/ar','r',str(archive),str(out/'qe75_native_lease.f90.o'),str(out/'exx.f90.o'),str(out/'full_state.f90.o'),*[str(p) for p in modified]])
  c=list(link[1 if mode=='control' else 5]['command']);c=[str(archive) if x.endswith('libqe_pw_pair.a') else str(NEW/'lease_client.o') if x.endswith('lease_client.o') else x for x in c]
  binary=out/('pw.'+mode+'.full_scf');c[c.index('-o')+1]=str(binary);run(c)
  dependencies={}
  for line in subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True).splitlines():
   for w in line.split():
    p=Path(w)
    if p.is_absolute() and p.exists():dependencies[str(p.resolve())]=sha(p.resolve())
  candidates[mode]=dict(binary=str(binary),sha256=sha(binary),backends=dependencies,archive_sha256=sha(archive))
 for p in src.iterdir():pins[str(p)]=sha(p)
 pins[str(HERE/'full_state.f90')]=sha(HERE/'full_state.f90')
 assert candidates['control']['backends']==candidates['stream']['backends']
 (HERE/'native_changes.patch').write_text(''.join(patches))
 (HERE/'build_results.json').write_text(json.dumps(dict(passed=True,records=records,candidates=candidates,source_and_exchange_archive_pins=pins,native_executed=False,same_O2_no_fast_math_bounds_checks=True),indent=2)+'\n')
 print('Private full-SCF builds PASS; no QE run yet')
if __name__=='__main__':main()
