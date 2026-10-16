"""Compile separate tiny NON_SCIENCE programs, never the QE ELF."""
import hashlib,json,os,resource,subprocess,uuid
from pathlib import Path
P=Path(__file__).resolve().parent;REPO=P.parents[3];ENV=Path('/home/User/opencode_workspace/DFT/.local/qe-env')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(1<<30,1<<30));resource.setrlimit(resource.RLIMIT_CPU,(30,30));resource.setrlimit(resource.RLIMIT_FSIZE,(64<<20,64<<20))
def main():
 assert not (P/'runtime_build.json').exists(), 'frozen build attempt already recorded; no rerun'
 root=REPO/'.tmp/r07spc16'/('density-runtime-build-'+uuid.uuid4().hex);root.mkdir()
 src=root/'runtime_probe.c';src.write_bytes((P/'runtime_probe.c').read_bytes())
 cmds=[['/usr/bin/cc','-std=c11','-O2','-Wall','-Wextra','-Werror',str(src),'-o',str(root/'fs_probe')],[str(ENV/'bin/mpicc'),'-std=c11','-O2','-Wall','-Wextra','-Werror','-DR07_MPI',str(src),'-Wl,-rpath,'+str(ENV/'lib'),'-o',str(root/'singleton_probe')]]
 result={'scope':'NON_SCIENCE_BUILD','root':str(root),'source_sha256':sha(src),'records':[],'passed':False}
 for cmd in cmds:
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=45,preexec_fn=limits,env={**os.environ,'OMPI_CC':'/usr/bin/cc','TMPDIR':str(root)})
  result['records'].append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
  if r.returncode:break
 else:
  result['passed']=True;result['elf_pins']={str(root/n):sha(root/n) for n in ('fs_probe','singleton_probe')}
 (P/'runtime_build.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
