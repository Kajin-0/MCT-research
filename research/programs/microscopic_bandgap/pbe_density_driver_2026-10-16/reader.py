"""R07D1 singleton finite packet reader, NEVER a science/owner release."""
import os,stat
from pathlib import Path
import numpy as np
MAGIC=71601002
class Refusal(ValueError):pass
def read(path,*,science=False):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
 try:
  st=os.fstat(fd)
  if not stat.S_ISREG(st.st_mode) or st.st_size>1<<30:raise Refusal('packet type/extent')
  with os.fdopen(fd,'rb',closefd=False) as f:
   def take(dtype,shape):
    count=int(np.prod(shape,dtype=np.int64));a=np.fromfile(f,dtype=dtype,count=count)
    if a.size!=count:raise Refusal('truncated packet')
    a=a.reshape(shape,order='F')
    if np.issubdtype(a.dtype,np.inexact) and not np.isfinite(a).all():raise Refusal('nonfinite')
    return a
   h=take('<i8',(20,));_,version,world,rank,pid,lda,n,ng,nr,ns,nb,m,nspin,nkb,nat,case,nsym,*reserved=map(int,h)
   if h[0]!=MAGIC or version!=1 or world!=1 or rank!=0 or pid<=0 or any(reserved):raise Refusal('new singleton schema only')
   if not (0<n<=lda<=21595 and 0<ng<=173631 and 0<nr<=1000000 and 0<ns<=1000000):raise Refusal('bounded dimensions')
   if (nb,m,nspin,nkb,nat)!=(352,12,4,712,16) or case not in (0,1) or nsym!=(24 if case==0 else 4):raise Refusal('physical metadata')
   if science and (lda,n,ng,nr,ns)!=(21595,21595,173631,512000,512000):raise Refusal('unqualified physical dimensions')
   # Exact byte formula includes padded descriptors and four spin channels.
   extent=160+224+72+24+64+24*(n+ng)+5*16*(2*lda)*12+16*ng*4+8*nr*4*2
   if extent!=st.st_size:raise Refusal('exact extent/trailing bytes')
   d=dict(header=h,fft=take('<i8',(14,2)),B=take('<f8',(3,3)),k=take('<f8',(3,)),scalars=take('<f8',(8,)))
   d['G']=take('<i8',(3,n));d['rhoG_labels']=take('<i8',(3,ng))
   for key in ('P','kin','local','nonlocal','H'):d[key]=take('<c16',(2*lda,m))
   d['rhoG']=take('<c16',(ng,4));d['rhoR']=take('<f8',(nr,4));d['vrs']=take('<f8',(nr,4))
   if f.read(1):raise Refusal('trailing')
   if os.fstat(fd)!=st:raise Refusal('packet changed during read')
   for key in ('G','rhoG_labels'):
    if np.unique(d[key],axis=1).shape[1]!=d[key].shape[1]:raise Refusal('duplicate physical G')
   if np.any(d['k']) or np.any(d['rhoG'][:,1:]) or np.any(d['rhoR'][:,1:]) or np.any(d['vrs'][:,1:]):raise Refusal('spin/Gamma')
   return d
 finally:os.close(fd)
def theta(X,G):
 """Theta(up,down)(G)=(down*(-G),-up*(-G)); no span-closure assumption."""
 n=G.shape[1]
 if X.shape[0]!=2*n:raise Refusal('Theta needs full unpadded physical G')
 lookup={tuple(v):i for i,v in enumerate(G.T)}
 try:minus=np.array([lookup[tuple(-v)] for v in G.T])
 except KeyError as e:raise Refusal('G inversion incomplete') from e
 return np.concatenate((X[n+minus].conj(),-X[minus].conj()),axis=0)
def theta_controls(d):
 P=d['P'];Y=d['H']
 if not np.array_equal(P[:,6:],theta(P[:,:6],d['G'])):raise Refusal('explicit Theta probe bytes')
 defect=float(np.linalg.norm(Y[:,6:]-theta(Y[:,:6],d['G']),2)/max(1.,np.linalg.norm(Y,2)))
 if defect>1e-8:raise Refusal('measured Theta action')
 return defect
def diagnostics(d):
 """Defined finite-frame arithmetic only; missing error certificate is explicit."""
 F=d['P'][:,:6];HF=d['H'][:,:6]
 gram=F.conj().T@F
 if np.linalg.norm(gram-np.eye(6),2)>1e-8:raise Refusal('physical F normalization')
 A=F.conj().T@HF
 err=np.linalg.norm(A-A.conj().T,2)
 if err>1e-8*max(1,np.linalg.norm(A,2)):raise Refusal('Hermiticity')
 # Keep the original columns; do not silently turn rounded F into a new frame.
 omega=np.trace(np.linalg.solve(gram[:2,:2],A[:2,:2]))/2-np.trace(np.linalg.solve(gram[2:,2:],A[2:,2:]))/4
 complement=HF-F@np.linalg.solve(gram,A)
 comp=d['kin']+d['local']+d['nonlocal']
 return dict(Omega_Ry=float(omega.real),QHP_norm_Ry=float(np.linalg.norm(complement,2)),component_error_Ry=float(np.linalg.norm(d['H']-comp,2)),Hermiticity_Ry=float(err),science_release=False,numerical_2meV_certificate=False)
