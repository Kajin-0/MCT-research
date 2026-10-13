"""Private bounded compile/link. No QE execution; old source/archives untouched."""
import hashlib,json,subprocess,time,shutil,difflib
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011');NEW=ROOT/'fixed_operator_20261013/build3'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 NEW.mkdir(exist_ok=False);records=[];pins={};candidates={}
 def run(cmd):
  t=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
  records.append(dict(command=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,wall_seconds=time.monotonic()-t))
  (HERE/'build_results.json').write_text(json.dumps(dict(passed=False,records=records),indent=2)+'\n')
  if p.returncode:raise RuntimeError(p.stderr)
 old=json.loads((BASE/'native_pair_2026-10-13/build_results.json').read_text())['records']
 link=json.loads((BASE/'native_pair_execution_2026-10-13/runtime_build_results.json').read_text())['records']
 run_template=None
 for f in (BASE/'m5_readiness').glob('*.json'):
  d=json.loads(f.read_text())
  for r in d.get('records',[]) if isinstance(d,dict) else []:
   c=r.get('command',[])
   if '-c' in c and any(x.endswith('run_pwscf.f90') for x in c):run_template=c
 if run_template is None:raise RuntimeError('pinned run_pwscf compile template absent')
 src=NEW/'source';src.mkdir()
 lease=(ROOT/'native_pair_20261013/v3/source/native_lease.f90').read_text().replace('stage==7)','stage==7 .OR. stage==8 .OR. stage==9)')
 (src/'native_lease.f90').write_text(lease)
 client=(ROOT/'first_ace_transport_fix_20261013/lease_client.c').read_text().replace('action!=7)','action!=7&&action!=8&&action!=9)')
 (src/'lease_client.c').write_text(client)
 runsource=(ROOT/'m5_readiness/source-retry1/run_pwscf.f90').read_text()
 assert runsource.count('CALL electrons()')==1
 runsource=runsource.replace('  USE kinds,', '#if defined(__QE75_FIXED_OPERATOR)\n  USE exx, ONLY: fixed_driver\n#endif\n  USE kinds,',1)
 runsource=runsource.replace('        CALL electrons()', '#if defined(__QE75_FIXED_OPERATOR)\n        CALL fixed_driver()\n#else\n        CALL electrons()\n#endif')
 (src/'run_pwscf.f90').write_text(runsource)
 run(['/usr/bin/cc','-std=c11','-Wall','-Wextra','-Werror','-O2','-c',str(src/'lease_client.c'),'-o',str(NEW/'lease_client.o')])
 patches=[]
 for mode,index,basearchive,basex in [
  ('setup',3,ROOT/'native_pair_20261013/v3/stock/libqe_pw_pair.a',ROOT/'native_pair_20261013/v3/source/exx.f90'),
  ('stream',9,ROOT/'fresh_scope4_fix_20261013/libqe_pw_pair.a',ROOT/'fresh_scope4_fix_20261013/exx.f90')]:
  out=NEW/mode;out.mkdir();original=basex.read_text();exx=original
  exx=exx.replace(' CONTAINS', ' INTEGER(8), ALLOCATABLE, PRIVATE :: fixed_layout(:)\n REAL(DP), ALLOCATABLE, PRIVATE :: fixed_occ(:,:)\n COMPLEX(DP), ALLOCATABLE, PRIVATE :: fixed_probes(:,:)\n CONTAINS',1)
  exx=exx.replace(' CONTAINS',' CONTAINS\n'+(HERE/'fixed_native.inc').read_text(),1)
  anchor='    CALL divide( inter_egrp_comm, x_nbnd_occ, ibnd_start, ibnd_end )'
  assert exx.count(anchor)==1
  exx=exx.replace(anchor,'    CALL fixed_kernel_capture(d_spin)\n'+anchor)
  a=exx.index('      CALL make_probe(npwx,nnpw,npol,current_k,diag_globals,diag_probe(:,1:1))')
  z=exx.index('      CALL qdiag_layout(diag_layout)',a)
  exx=exx[:a]+'      diag_probe(:,1)=fixed_probes(:,current_k)\n'+exx[z:]
  path=src/(mode+'_exx.f90');path.write_text(exx)
  patches+=list(difflib.unified_diff(original.splitlines(True),exx.splitlines(True),fromfile=str(basex),tofile=str(path)))
  def compile(template,source,obj):
   c=[x for x in template if mode=='stream' or x!='-D__EXX_QSTREAM']; c+=['-D__QE75_FIXED_OPERATOR']
   for opt in ['-J']:
    c[c.index(opt)+1]=str(out)
   c[c.index('-c')+1]=str(source);c[c.index('-o')+1]=str(obj)
   # Newly generated module must precede old exx/native modules.
   c[1:1]=['-I',str(out)]
   run(c)
  compile(old[1 if mode=='setup' else 7]['command'],src/'native_lease.f90',out/'qe75_native_lease.f90.o')
  compile(old[index]['command'],path,out/'exx.f90.o')
  compile(run_template,src/'run_pwscf.f90',out/'run_pwscf.f90.o')
  archive=out/'libqe_pw_fixed.a';shutil.copy2(basearchive,archive);pins[str(basearchive)]=sha(basearchive);pins[str(basex)]=sha(basex)
  run(['/usr/bin/ar','r',str(archive),str(out/'qe75_native_lease.f90.o'),str(out/'exx.f90.o'),str(out/'run_pwscf.f90.o')])
  # Ensure there is one object with each replaced name, no old native module alias.
  listing=subprocess.check_output(['/usr/bin/ar','t',str(archive)],text=True).splitlines()
  for n in ['qe75_native_lease.f90.o','exx.f90.o','run_pwscf.f90.o']:assert listing.count(n)==1
  c=list(link[1 if mode=='setup' else 5]['command'])
  c=[str(archive) if x.endswith('libqe_pw_pair.a') else str(NEW/'lease_client.o') if x.endswith('lease_client.o') else x for x in c]
  binary=out/('pw.'+mode+'.fixed');c[c.index('-o')+1]=str(binary);run(c)
  dependencies={}
  for line in subprocess.check_output(['/usr/bin/ldd',str(binary)],text=True).splitlines():
   for word in line.split():
    p=Path(word)
    if p.is_absolute() and p.exists():dependencies[str(p.resolve())]=sha(p.resolve())
  candidates[mode]=dict(binary=str(binary),sha256=sha(binary),backends=dependencies,archive_sha256=sha(archive))
 for p in src.iterdir():pins[str(p)]=sha(p)
 (HERE/'native_changes.patch').write_text(''.join(patches))
 assert candidates['setup']['backends']==candidates['stream']['backends']
 (HERE/'build_results.json').write_text(json.dumps(dict(passed=True,records=records,candidates=candidates,source_and_exchange_archive_pins=pins,native_executed=False),indent=2)+'\n')
 print('Private fixed-operator objects and two links PASS; native unexecuted')
if __name__=='__main__':main()
