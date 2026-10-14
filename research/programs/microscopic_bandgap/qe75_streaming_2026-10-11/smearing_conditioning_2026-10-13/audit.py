"""Retained all-rank/all-k audit. Serial replay of unedited QE Fermi source;
no QE process, MPI initialization, SCF, empirical fitting or old verdict edit.
"""
import ctypes, hashlib, json, math, os, subprocess, sys, importlib.util
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent; BASE=HERE.parent
spec=importlib.util.spec_from_file_location('qe75_historical_obs',BASE/'full_scf_2026-10-13/observables.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
DFT=Path('/home/User/opencode_workspace/DFT'); ROOT=DFT/'.local/qe75_lowram_20261011'
QE=ROOT/'q-e'; PRIVATE=ROOT/'smearing_conditioning_20261013'; WK=np.array([.125,.5,.375]); SIGMA=.001

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def build():
 PRIVATE.mkdir(mode=0o700,exist_ok=True)
 stub='''module kinds
 integer,parameter::DP=selected_real_kind(14,200)
end module
module io_global
 integer,parameter::stdout=6
end module
module mp_pools
 integer,parameter::inter_pool_comm=0
end module
module mp
 use kinds
 contains
 subroutine mp_max(x,c)
 real(DP),intent(inout)::x
 integer,intent(in)::c
 end subroutine
 subroutine mp_min(x,c)
 real(DP),intent(inout)::x
 integer,intent(in)::c
 end subroutine
 subroutine mp_sum(x,c)
 real(DP),intent(inout)::x
 integer,intent(in)::c
 end subroutine
end module
subroutine errore(a,b,c)
 character(*)::a,b
 integer::c
 write(6,*) a,b,c
 stop 1
end subroutine
'''
 wrapper='''subroutine replay(et,mu,wg) bind(C)
 use iso_c_binding
 implicit none
 real(c_double),intent(in)::et(48,3)
 real(c_double),intent(out)::mu,wg(48,3)
 real(c_double)::wk(3),demet
 integer::isk(3)
 wk=[.125d0,.5d0,.375d0];isk=1
 call gweights(3,wk,48,36.d0,.001d0,-1,et,mu,demet,wg,0,isk)
end subroutine
subroutine at_mu(et,mu,wg) bind(C)
 use iso_c_binding
 implicit none
 real(c_double),intent(in)::et(48,3),mu
 real(c_double),intent(out)::wg(48,3)
 real(c_double)::wk(3),demet
 integer::isk(3)
 wk=[.125d0,.5d0,.375d0];isk=1
 call gweights_only(3,wk,0,isk,48,36.d0,.001d0,-1,et,mu,demet,wg)
end subroutine
function cold(x) result(f) bind(C)
 use iso_c_binding
 implicit none
 real(c_double),value::x
 real(c_double)::f,wgauss
 external wgauss
 f=wgauss(x,-1)
end function
'''
 (PRIVATE/'serial_only.f90').write_text(stub);(PRIVATE/'wrap.f90').write_text(wrapper)
 files=[PRIVATE/'serial_only.f90',QE/'Modules/constants.f90',QE/'Modules/wgauss.f90',QE/'Modules/w0gauss.f90',QE/'Modules/w1gauss.f90',QE/'PW/src/sumkg.f90',QE/'PW/src/efermig.f90',QE/'PW/src/gweights.f90',PRIVATE/'wrap.f90']
 compiler='/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/toolchain/bin/x86_64-conda-linux-gnu-gfortran'
 if not Path(compiler).exists():compiler=subprocess.check_output(['which','gfortran'],text=True).strip()
 cmd=[compiler,'-cpp','-O2','-fno-fast-math','-fcheck=all','-fPIC','-shared','-J',str(PRIVATE),'-I',str(PRIVATE),*[str(p) for p in files],'-o',str(PRIVATE/'replay.so')]
 r=subprocess.run(cmd,cwd=PRIVATE,capture_output=True,text=True,timeout=90)
 record=dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,source_hashes={str(p):sha(p) for p in files},serial_stubs_not_native_MPI=True)
 if r.returncode:raise RuntimeError(r.stderr)
 record['binary_sha256']=sha(PRIVATE/'replay.so');(HERE/'serial_build.json').write_text(json.dumps(record,indent=2)+'\n')

def main():
 if not (PRIVATE/'replay.so').exists():build()
 lib=ctypes.CDLL(str(PRIVATE/'replay.so'));double=ctypes.c_double;ptr=ctypes.POINTER(double)
 lib.replay.argtypes=[ptr,ptr,ptr];lib.cold.argtypes=[double];lib.cold.restype=double
 def replay(et):
  e=np.array(et,order='F');w=np.zeros((48,3),order='F');mu=double()
  lib.replay(e.ctypes.data_as(ptr),ctypes.byref(mu),w.ctypes.data_as(ptr));return mu.value,w
 def cold(x):return np.array([lib.cold(float(v)) for v in np.ravel(x)]).reshape(np.shape(x))
 native=ROOT/'full_scf_pair_v2_20261013';records=[];pins={}
 for step in range(1,5):
  pair={}
  for mode in ['control','stream']:
   packets={key:old.decode(p) for key,p in old.paths(native/mode,step,1).items()}
   for p in old.paths(native/mode,step,1).values():pins[str(p)]=sha(p)
   d=packets[(0,1)]
   assert all(old.bit_equal(d['et'],v['et']) and old.bit_equal(d['wg'],v['wg']) for v in packets.values())
   et,wg=d['et'],d['wg'];mu,wnew=replay(et);f=wg/WK
   x=(mu-et)/SIGMA;y=x-1/math.sqrt(2)
   deriv=np.exp(-np.minimum(y*y,200))*(1-math.sqrt(2)*y)/math.sqrt(math.pi)/SIGMA
   partial=[]
   for b,k in zip(*np.where((f>1e-8)&(f<1-1e-8))):
    partial.append(dict(k=int(k+1),band=int(b+1),eps_Ry=float(et[b,k]),occupation=float(f[b,k]),weighted=float(wg[b,k]),slope_per_Ry=float(deriv[b,k])))
   # Expected Kramers pairing in nonmagnetic time reversal + inversion? HgTe has
   # no inversion: k1 Gamma degeneracy only; do not assume all k pairwise degenerate.
   pair[mode]=dict(mu_Ry=mu,charge_weighted=float(wg.sum()),charge_residual_electrons=float(wg.sum()-36),replay_charge_residual=float(wnew.sum()-36),replay_weighted_max=float(np.max(abs(wnew-wg))),replay_occupation_max=float(np.max(abs(wnew/WK-f))),charge_response_electrons_per_Ry=float((deriv*WK).sum()),negative_charge_response=float((np.minimum(deriv,0)*WK).sum()),partial=partial,k1_bands35_36_split_Ry=float(abs(et[34,0]-et[35,0])),k1_bands37_38_split_Ry=float(abs(et[36,0]-et[37,0])))
   pair[mode]['_et']=et;pair[mode]['_f']=f
  dm=abs(pair['control']['mu_Ry']-pair['stream']['mu_Ry']);de=abs(pair['control']['_et']-pair['stream']['_et']);df=abs(pair['control']['_f']-pair['stream']['_f'])
  L=.7541710171545021;bound=L/SIGMA*(de+dm);j=np.unravel_index(np.argmax(df),df.shape);ej=np.unravel_index(np.argmax(de),de.shape)
  row=dict(step=step,mu_delta_Ry=dm,eigen_max_Ry=float(de.max()),eigen_max_location=dict(band=int(ej[0]+1),k=int(ej[1]+1)),occupation_max=float(df.max()),occupation_max_location=dict(band=int(j[0]+1),k=int(j[1]+1)),global_MVT_upper=float(bound.max()),band_MVT_upper_at_max=float(bound[j]),max_df_minus_band_bound=float((df-bound).max()),member={})
  for mode,d in pair.items():row['member'][mode]={k:v for k,v in d.items() if not k.startswith('_')}
  row['independent_orbital_density_and_charge_comparison']=old.pair_states(old.paths(native/'control',step,1),old.paths(native/'stream',step,1),enforce=False)
  records.append(row)
 result=dict(records=records,source_hashes=json.loads((HERE/'serial_build.json').read_text())['source_hashes'],retained_packet_sha256=pins,exact_QE_source_serial_one_pool_replay=True,not_native_MPI_reexecution=True,old_occupation_verdict='FAIL step4 preserved',chemical_potential_observation='replayed from et using actual efermig, independent of wg; no high-precision native ef capture existed',no_new_SCF=True)
 (HERE/'retained_audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps([{k:v for k,v in d.items() if k not in ['member','independent_orbital_density_and_charge_comparison']}|{'neutrality':[d['member'][m]['charge_residual_electrons'] for m in ['control','stream']],'occupation_reconstruction':[d['member'][m]['replay_occupation_max'] for m in ['control','stream']]} for d in records],indent=2))
if __name__=='__main__':main()
