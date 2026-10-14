"""Actual native helper and stock QE scalar-function objects, NO MPI init/run."""
import json,subprocess,ctypes,hashlib
from pathlib import Path
import numpy as np
import qualify as q
HERE=Path(__file__).resolve().parent;ROOT=q.ROOT;PRIVATE=ROOT/'fermi_root_native_float_20261014'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 PRIVATE.mkdir(mode=0o700,exist_ok=True)
 native=json.loads((HERE/'build_results.json').read_text());link=next(r['command'] for r in native['records'] if any(str(x).endswith('pw.control.rooted') for x in r['command']))
 module=next(Path(x) for x in link if str(x).endswith('libqe_modules.a'))
 records=[];pins={str(module):sha(module)}
 for n in ['wgauss.f90.o','w0gauss.f90.o','w1gauss.f90.o']:
  p=PRIVATE/n;p.write_bytes(subprocess.check_output(['/usr/bin/ar','p',str(module),n]));pins[str(p)]=sha(p)
 # Compile only serial reduction sumkg and ordinary wrapper: actual helper and
 # actual QE wgauss objects are used, not MPI process code.
 driver='''program native_scalar
 use kinds
 use r07_cold_root
 implicit none
 real(DP)::et(48,3),mu,wg(48,3),wk(3),demet
 integer::isk(3),code,u,i,k
 character(1024)::path
 call get_command_argument(1,path)
 open(newunit=u,file=trim(path),access='stream',form='unformatted',status='old',action='read')
 read(u)et
 close(u)
 wk=[.125d0,.5d0,.375d0];isk=1
 call strict_root(et,48,3,36.d0,wk,.001d0,0,isk,mu,code)
 write(6,'(I0)')code
 write(6,'(ES26.17E3)')mu
 do i=1,10
 write(6,'(ES26.17E3)')last_certificate(i)
 enddo
 if(code==0)then
 call gweights_only(3,wk,0,isk,48,36.d0,.001d0,-1,et,mu,demet,wg)
 do k=1,3
 do i=1,48
 write(6,'(ES26.17E3)')wg(i,k)
 enddo
 enddo
 endif
end program
'''
 (PRIVATE/'driver.f90').write_text(driver)
 files=[ROOT/'smearing_conditioning_20261013/serial_only.f90',ROOT/'q-e/Modules/constants.f90',ROOT/'q-e/PW/src/sumkg.f90',ROOT/'q-e/PW/src/efermig.f90',ROOT/'q-e/PW/src/gweights.f90',PRIVATE/'driver.f90']
 cc=ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran'
 cmd=[str(cc),'-cpp','-O2','-fno-fast-math','-fcheck=all','-no-pie','-J',str(PRIVATE),'-I',str(ROOT/'rooted_full_scf_build_20261014/control'),'-I',str(PRIVATE),*[str(p) for p in files],str(ROOT/'rooted_full_scf_build_20261014/control/cold_root.f90.o'),*[str(PRIVATE/n) for n in ['wgauss.f90.o','w0gauss.f90.o','w1gauss.f90.o']],'-o',str(PRIVATE/'native_scalar')]
 r=subprocess.run(cmd,cwd=PRIVATE,capture_output=True,text=True,timeout=90);records.append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
 if r.returncode:raise RuntimeError(r.stderr)
 original=json.loads((HERE/'root_qualification.json').read_text());data=np.load(HERE/'retained_inputs.npz',allow_pickle=False);result=[]
 for row in original['records']:
  et=np.array(data['et_'+str(row['id'])],order='F');path=PRIVATE/('et'+str(row['id'])+'.bin');path.write_bytes(et.tobytes(order='F'))
  run=subprocess.run([str(PRIVATE/'native_scalar'),str(path)],capture_output=True,text=True,timeout=10)
  assert run.returncode==0,run.stderr
  lines=run.stdout.splitlines();code=int(lines[0]);mu=float(lines[1]);c=np.array([float(v) for v in lines[2:12]]);w=np.array([float(v) for v in lines[12:]]).reshape((48,3),order='F')
  assert code==0
  delta=float(abs(c-np.array(row['certificate'])).max());err=q.cond.evaluation_check(mu,et,w/np.array([.125,.5,.375]))
  result.append(dict(id=row['id'],native_helper_source_root_mu_Ry=mu,pure_source_mu_delta=abs(mu-row['mu_Ry']),certificate_max_delta=delta,charge_residual=float(w.sum()-36),independent_f_error=err))
 for p in files+[ROOT/'rooted_full_scf_build_20261014/control/cold_root.f90.o']:pins[str(p)]=sha(p)
 result=dict(passed=True,records=result,build=records,pins=pins,binary_sha256=sha(PRIVATE/'native_scalar'),actual_native_helper_and_stock_QE_function_objects=True,serial_sumkg_single_pool_no_MPI=True)
 (HERE/'native_float_validation.json').write_text(json.dumps(result,indent=2)+'\n');print('Actual native scalar-object qualification PASS; no MPI/QE run')
if __name__=='__main__':main()
