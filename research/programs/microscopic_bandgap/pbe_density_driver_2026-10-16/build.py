"""One compile/link per immutable source snapshot; never execute the QE ELF."""
import hashlib,json,os,resource,shutil,subprocess,time,uuid
from pathlib import Path
P=Path(__file__).resolve().parent
REPO=P.parents[3]
DFT=Path('/home/User/opencode_workspace/DFT'); ENV=DFT/'.local/qe-env'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(2<<30,2<<30))
 resource.setrlimit(resource.RLIMIT_CPU,(60,60))
 resource.setrlimit(resource.RLIMIT_FSIZE,(512<<20,512<<20))
def main():
 assert not (P/'build_result.json').exists(), 'frozen build attempt already recorded; no rerun'
 archive=ENV/'lib/libqe_pw.a'; before=sha(archive)
 assert before=='65349164becf7adab64d8c4cc1ad02be16d4ac3c86b1635fe840bcaf5116f0a2'
 root=REPO/'.tmp/r07spc16'/('density-build-'+uuid.uuid4().hex)
 root.mkdir(parents=True); records=[]
 for n in ('density_driver.f90','build_gate.c'):shutil.copyfile(P/n,root/n)
 pins={str(root/n):sha(root/n) for n in ('density_driver.f90','build_gate.c')}
 old=json.loads((P.parent/'pbe_static_completion_2026-10-16/build_result.json').read_text())
 cc=old['records'][0]['command'].copy(); cc[cc.index('-J')+1]=str(root)
 cc[cc.index('-c')+1]=str(root/'density_driver.f90');cc[cc.index('-o')+1]=str(root/'density_driver.o')
 c=['/usr/bin/cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-c',str(root/'build_gate.c'),'-o',str(root/'build_gate.o')]
 link=old['records'][3]['command'].copy();link[2]=str(root/'build_gate.o');link[3]=str(root/'density_driver.o')
 link[link.index('-Wl,--start-group')+1]=str(archive)
 link[link.index('-o')+1]=str(root/'r07_density_only_v1.UNEXECUTED')
 link.insert(2,'-Wl,-Map='+str(root/'link.map'))
 result={'scope':'BUILD_ONLY_NO_QE_EXECUTION','source_pins':pins,'root':str(root),'records':records,'passed':False,'stock_archive_before':before}
 try:
  for command in (cc,c,link):
   t=time.monotonic();r=subprocess.run(command,cwd=root,capture_output=True,text=True,timeout=90,preexec_fn=limits,env={**os.environ,'TMPDIR':str(root),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
   records.append(dict(command=command,returncode=r.returncode,wall_s=time.monotonic()-t,stdout=r.stdout,stderr=r.stderr))
   if r.returncode:break
  result['passed']=len(records)==3 and all(r['returncode']==0 for r in records)
  if result['passed']:
   elf=root/'r07_density_only_v1.UNEXECUTED';result['elf']=str(elf);result['elf_sha256']=sha(elf)
   result['nm']=subprocess.run(['/usr/bin/nm',str(elf)],capture_output=True,text=True,check=True).stdout
   (root/'nm.txt').write_text(result.pop('nm'))
   result['nm_sha256']=sha(root/'nm.txt');result['link_map_sha256']=sha(root/'link.map')
 finally:
  result['stock_archive_after']=sha(archive);assert result['stock_archive_after']==before
  result['QE_ELF_executed']=False
  (P/'build_result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ('passed','root','records')},indent=2))
if __name__=='__main__':main()
