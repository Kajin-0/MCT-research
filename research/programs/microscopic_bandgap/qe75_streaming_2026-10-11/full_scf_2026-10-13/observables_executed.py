"""Actual native SCF observations; no fitted gaps or relaxed old byte gate."""
from pathlib import Path
import json,struct,sys,numpy as np
BASE=Path(__file__).resolve().parent.parent
for n in ['software_2026-10-13','runtime_admission','m5_readiness','checkpoint_phase']:sys.path.insert(0,str(BASE/n))
from common_state import decode as checked
TOL=dict(initial_rhoR=5e-14,initial_vrs_Ry=5e-12,energy_Ry=1e-8,eigenvalue_Ry=2e-7,occupation=1e-8,rhoR=1e-9,rhoG=1e-9,vrs_Ry=1e-8,orbital_density_relative_F=1e-7,NC_Gram=1e-10)
class Refusal(ValueError):pass

def decode(path):
 raw=Path(path).read_bytes();meta=checked(path);h=meta['header'];_,r,k,pad,act,spin,nb,nt,nr,ns,ng,nl,_=h
 pos=208
 def take(dtype,n):
  nonlocal pos
  d=np.frombuffer(raw,dtype=dtype,count=n,offset=pos).copy();pos+=d.itemsize*n;return d
 layout=take('=i8',nl);mill=take('=i8',3*act).reshape((3,act),order='F').T
 w=take('=c16',pad*spin*nb).reshape((pad*spin,nb),order='F');ids=np.r_[np.arange(act),pad+np.arange(act)]
 et=np.empty((nb,nt));wg=et.copy()
 for j in range(nt):et[:,j]=take('=f8',nb);wg[:,j]=take('=f8',nb)
 rr=np.empty((nr,ns));rg=np.empty((ng,ns),complex);v=rr.copy()
 for j in range(ns):rr[:,j]=take('=f8',nr);rg[:,j]=take('=c16',ng);v[:,j]=take('=f8',nr)
 if pos!=len(raw):raise Refusal('state parser extent')
 return dict(meta=meta,layout=layout,mill=mill,wave=w[ids],et=et,wg=wg,rhoR=rr,rhoG=rg,vrs=v,density_mill=layout[-3*ng:].reshape((3,ng),order='F').T)

def maxdiff(a,b):return float(np.max(np.abs(a-b)))
def bit_equal(a,b):return np.ascontiguousarray(a).tobytes()==np.ascontiguousarray(b).tobytes()

def pair_states(a,b,initial=False):
 result={};wk=[.125,.5,.375]
 for k in [1,2,3]:
  aa=[decode(a[(r,k)]) for r in [0,1]];bb=[decode(b[(r,k)]) for r in [0,1]]
  for x,y in zip(aa,bb):
   if x['meta']['header']!=y['meta']['header'] or not bit_equal(x['layout'],y['layout']) or not bit_equal(x['mill'],y['mill']):raise Refusal('physical reciprocal/FFT basis mismatch')
   if x['meta']['kpoint']!=y['meta']['kpoint']:raise Refusal('physical k point mismatch')
  A=np.concatenate([x['wave'] for x in aa]);B=np.concatenate([x['wave'] for x in bb]);ga=maxdiff(A.conj().T@A,np.eye(48));gb=maxdiff(B.conj().T@B,np.eye(48))
  if max(ga,gb)>TOL['NC_Gram']:raise Refusal('native NC Gram')
  fa=aa[0]['wg'][:,k-1]/wk[k-1];fb=bb[0]['wg'][:,k-1]/wk[k-1]
  S=A.conj().T@B;R=B-A@S;M=R.conj().T@R;C=S*fb[None,:]
  D=np.diag(fa)-(S*fb[None,:])@S.conj().T
  off=2*np.trace(C@M@C.conj().T).real
  # Stable block decomposition, avoids cancellation of O(1) traces for equal states.
  norm=np.sqrt(max(0.,np.vdot(D,D).real+off+np.sum(fb[:,None]*fb[None,:]*np.abs(M)**2)))
  rel=float(norm/max(np.linalg.norm(fa),1.))
  d=dict(eigenvalue_Ry=maxdiff(aa[0]['et'],bb[0]['et']),occupation=maxdiff(fa,fb),orbital_density_relative_F=rel,NC_Gram_control=ga,NC_Gram_stream=gb)
  for field in ['rhoR','rhoG','vrs']:
   d[field]=max(maxdiff(x[field],y[field]) for x,y in zip(aa,bb))
  if initial:
   if not all(bit_equal(x['wave'],y['wave']) and bit_equal(x['rhoG'],y['rhoG']) and bit_equal(x['et'],y['et']) and bit_equal(x['wg'],y['wg']) for x,y in zip(aa,bb)):raise Refusal('initial source waves/rhoG/et/wg must remain byte equal')
   if d['rhoR']>TOL['initial_rhoR'] or d['vrs']>TOL['initial_vrs_Ry']:raise Refusal('initial reconstructed rhoR/vrs exceeds NEW preregistered numerical domain')
  else:
   limits=dict(eigenvalue_Ry=TOL['eigenvalue_Ry'],occupation=TOL['occupation'],orbital_density_relative_F=TOL['orbital_density_relative_F'],rhoR=TOL['rhoR'],rhoG=TOL['rhoG'],vrs=TOL['vrs_Ry'])
   if any(d[n]>limit for n,limit in limits.items()):raise Refusal('SCF state mismatch '+str(d))
  result[str(k)]=d
 return result

def paths(root,step,stage):return {(r,k):Path(root)/'trajectory'/f'rank{r}.step{step}.stage{stage}.k{k}.state' for r in [0,1] for k in [1,2,3]}
def scalars(root,step,stage):
 values=[]
 for r in [0,1]:
  p=Path(root)/'trajectory'/f'rank{r}.step{step}.stage{stage}.scalars';lines=p.read_text().splitlines();header=[int(x) for x in lines[1].split()]
  if header[:3]!=[r,step,stage] or len(lines)!=12:raise Refusal('native scalar shape/labels')
  data=np.array([float(v) for v in lines[2:]])
  if not np.all(np.isfinite(data)):raise Refusal('nonfinite scalar')
  values.append((lines[0],header,data))
 if values[0][0]!=values[1][0] or not bit_equal(values[0][2],values[1][2]):raise Refusal('replicated native scalars mismatch')
 return dict(fingerprint=values[0][0],header=values[0][1],values=dict(zip(['etot_Ry','hwf_Ry','fock0_Ry','fock1_Ry','fock2_Ry','fock3_Ry','dexx_Ry','tr2_Ry','ethr_Ry','tr2_final_Ry'],values[0][2].tolist())))

def step_certificate(root,step,stage,control=None):
 pp=paths(root,step,stage)
 if not all(p.is_file() for p in pp.values()):raise Refusal('closed complete native step missing')
 s=scalars(root,step,stage)
 state=pair_states(pp,pp)
 result=dict(step=step,stage=stage,scalar=s,self_state=state,physical_gap_inferred=False)
 if control is not None:
  q=scalars(control,step,stage)
  differences={n:abs(s['values'][n]-q['values'][n]) for n in ['etot_Ry','hwf_Ry','fock0_Ry','fock1_Ry','fock2_Ry','fock3_Ry','dexx_Ry']}
  if any(v>TOL['energy_Ry'] for v in differences.values()):raise Refusal('native HSE energy trajectory mismatch '+str(differences))
  result.update(paired_states=pair_states(paths(control,step,stage),pp),paired_scalar_difference=differences)
 return result

def final_readback(root,step):
 import h5py
 root=Path(root);pp=paths(root,step,2);results=[]
 for k in [1,2,3]:
  with h5py.File(root/'out/r07m4.save'/f'wfc{k}.hdf5') as f:
   if int(f.attrs['nbnd'])!=48 or int(f.attrs['npol'])!=2 or float(f.attrs['scale_factor'])!=1:raise Refusal('native collected wave metadata')
   labels=f['MillerIndices'][...];wave=np.ascontiguousarray(f['evc'][...]).view(np.complex128).T
  lookup={tuple(v):i for i,v in enumerate(labels)};N=len(labels)
  for rank in [0,1]:
   d=decode(pp[(rank,k)]);rows=np.array([lookup[tuple(v)] for v in d['mill']]);actual=np.concatenate([wave[rows],wave[N+rows]])
   if not bit_equal(actual,d['wave']):raise Refusal('native wave HDF5/buffer bit readback mismatch')
  results.append(dict(k=k,native_wave_readback_bitwise=True))
 with h5py.File(root/'out/r07m4.save/charge-density.hdf5') as f:
  labels=f['MillerIndices'][...];density=np.ascontiguousarray(f['rhotot_g'][...]).view(np.complex128);lookup={tuple(v):i for i,v in enumerate(labels)}
 for rank in [0,1]:
  d=decode(pp[(rank,1)]);rows=[lookup[tuple(v)] for v in d['density_mill']]
  if not bit_equal(density[rows],d['rhoG'][:,0]):raise Refusal('native rhoG HDF5/buffer bit readback mismatch')
 return dict(waves=results,reciprocal_density_readback_bitwise=True,SCF_native_restart_semantics_not_qualified=True)
