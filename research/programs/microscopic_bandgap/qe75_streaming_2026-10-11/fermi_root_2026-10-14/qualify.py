"""Small actual-source root checks over ALL retained control spectra; no MPI/QE."""
import json,ctypes,hashlib,subprocess,math,sys,importlib.util
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011');PRIVATE=ROOT/'fermi_root_serial_20261014'
spec=importlib.util.spec_from_file_location('cold_conditioning',HERE.parent/'smearing_conditioning_2026-10-13/conditioning.py');cond=importlib.util.module_from_spec(spec);spec.loader.exec_module(cond)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build():
 PRIVATE.mkdir(mode=0o700,exist_ok=True)
 wrapper='''subroutine qualify(et,mu,wg,cert,code) bind(C)
 use iso_c_binding
 use r07_cold_root
 implicit none
 real(c_double),intent(in)::et(48,3)
 real(c_double),intent(out)::mu,wg(48,3),cert(10)
 integer(c_int),intent(out)::code
 real(c_double)::wk(3),demet
 integer::isk(3)
 wk=[.125d0,.5d0,.375d0];isk=1
 call strict_root(et,48,3,36.d0,wk,.001d0,0,isk,mu,code)
 cert=last_certificate
 wg=0
 if(code==0)call gweights_only(3,wk,0,isk,48,36.d0,.001d0,-1,et,mu,demet,wg)
end subroutine
'''
 (PRIVATE/'wrap.f90').write_text(wrapper)
 stub=ROOT/'smearing_conditioning_20261013/serial_only.f90';q=ROOT/'q-e'
 files=[stub,q/'Modules/constants.f90',q/'Modules/wgauss.f90',q/'Modules/w0gauss.f90',q/'Modules/w1gauss.f90',q/'PW/src/sumkg.f90',q/'PW/src/efermig.f90',q/'PW/src/gweights.f90',HERE/'cold_root.f90',PRIVATE/'wrap.f90']
 cc=ROOT/'toolchain/bin/x86_64-conda-linux-gnu-gfortran';cmd=[str(cc),'-cpp','-O2','-fno-fast-math','-fcheck=all','-fPIC','-shared','-J',str(PRIVATE),'-I',str(PRIVATE),*[str(p) for p in files],'-o',str(PRIVATE/'root.so')]
 r=subprocess.run(cmd,cwd=PRIVATE,capture_output=True,text=True,timeout=90)
 (HERE/'serial_build.json').write_text(json.dumps(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,pins={str(p):sha(p) for p in files}),indent=2)+'\n')
 if r.returncode:raise RuntimeError(r.stderr)
def main():
 if not PRIVATE.exists():build()
 lib=ctypes.CDLL(str(PRIVATE/'root.so'));ptr=ctypes.POINTER(ctypes.c_double);ip=ctypes.POINTER(ctypes.c_int)
 lib.qualify.argtypes=[ptr,ptr,ptr,ptr,ip]
 data=np.load(HERE/'retained_inputs.npz',allow_pickle=False);audit=json.loads((HERE/'input_audit.json').read_text());records=[]
 for r in audit['records']:
  et=np.array(data['et_'+str(r['id'])],order='F');mu=ctypes.c_double();w=np.empty((48,3),order='F');cert=np.empty(10);code=ctypes.c_int()
  lib.qualify(et.ctypes.data_as(ptr),ctypes.byref(mu),w.ctypes.data_as(ptr),cert.ctypes.data_as(ptr),ctypes.byref(code))
  row=dict(id=r['id'],outer=r['outer'],archive=Path(r['root']).parent.name,code=code.value,mu_Ry=mu.value)
  if code.value==0:
   independent=cond.evaluation_check(mu.value,et,w/np.array([.125,.5,.375]));expected=np.array([[cond.high_precision_cold(mu.value,e) for e in band] for band in et])
   row.update(certificate=cert.tolist(),charge_error=float(w.sum()-36),independent_analytic_charge_error=float((expected*np.array([.125,.5,.375])).sum()-36),independent_analytic_occupation_error=independent,old_mu_shift_Ry=mu.value-r['source_replayed_mu_Ry'],WG_max_change=float(abs(w-data['wg_'+str(r['id'])]).max()))
  records.append(row)
 result=dict(all_passed=all(r['code']==0 and abs(r['charge_error'])<=1e-8 and abs(r['independent_analytic_charge_error'])<=1e-8 for r in records),records=records,candidate_source_sha256=sha(HERE/'cold_root.f90'),serial_binary_sha256=sha(PRIVATE/'root.so'),no_native_MPI_QE=True)
 (HERE/'root_qualification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
