"""Pre-exit production packet checks; no old result or JOBDONE authority."""
from pathlib import Path
import hashlib
import importlib.util
import numpy as np
import h5py

HERE=Path(__file__).resolve().parent
_path=HERE/'packet_reader.py'
if hashlib.sha256(_path.read_bytes()).hexdigest()!='053de9faddb54a67ec6fa257894c3d7e90512d6ac91f1ff9df6d69eb86e70ff9':
    raise ImportError('missing/corrupt pinned packet Reader')
_spec=importlib.util.spec_from_file_location('_r07_static_completion_reader',_path)
_module=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_module)
Reader=_module.Reader


def decode(path):
    if Path(path).stat().st_size>1<<30:raise ValueError('packet exceeds per-file bound')
    r=Reader(path);h=r.take('<i8',(16,))
    if tuple(h[[0,1,9,10,12,13]])!=(70251521,1,352,4,16,12):raise ValueError('native static header')
    p,n,ng,nr,ns=map(int,h[[4,5,6,7,8]])
    if not (0<n<=p<=50000 and 0<min(ng,nr,ns)<=max(ng,nr,ns)<=2**22):raise ValueError('packet extents')
    fft=r.take('<i8',(14,2));B=r.take('<f8',(3,3));k=r.take('<f8',(3,));scalars=r.take('<f8',(6,))
    G=r.take('<i8',(3,n)).T;densityG=r.take('<i8',(3,ng)).T
    fields={s:r.take('<c16',(2*p,12)) for s in ['trial','kin','loc','nl','full']}
    rhoG=r.take('<c16',(ng,4));rhoR=r.take('<f8',(nr,4));vrs=r.take('<f8',(ns,4));r.end()
    return dict(h=h,fft=fft,B=B,k=k,scalars=scalars,G=G,densityG=densityG,
                rhoG=rhoG,rhoR=rhoR,vrs=vrs,**fields)


def inspect(root,profile,peers):
    from protocol import sha,Refusal
    root=Path(root)
    if root.name not in ['unshared','shared'] or str(root)!=profile['roots'][root.name]:
        raise Refusal('new roots only; old refused evidence is excluded')
    for path,pin in profile['pins'].items():
        if sha(path)!=pin:raise Refusal('source/ELF/PP/frame pin changed')
    for name,pin in profile['saves'][root.name].items():
        if sha(pin['source'])!=pin['sha256'] or sha(root/'out/r07pbe.save'/name)!=pin['sha256']:
            raise Refusal('accepted/copied saved source changed')
    f=np.load(profile['frame']);P,G,B=f['P'],f['G'],f['B'];N=len(G)
    if N!=21595 or P.shape!=(2*N,6):raise Refusal('original physical frame extent')
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G])
    theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    if not np.array_equal(theta(P),f['ThetaP']):raise Refusal('spinor Theta convention')
    trial=np.column_stack((P,f['ThetaP']));parts={k:np.zeros_like(trial) for k in ['kin','loc','nl','full']}
    S=P.conj().T@P
    if np.linalg.norm(S-np.eye(6),2)>1e-8:raise Refusal('NC frame normalization')
    with h5py.File(root/'out/r07pbe.save/charge-density.hdf5') as saved:
        rg=np.array(saved['MillerIndices']);rv=np.asarray(saved['rhotot_g']).view(np.complex128).reshape(-1)
    rlookup={tuple(g):i for i,g in enumerate(rg)};seen=set();seenrho=set()
    for rank in [0,1]:
        row=decode(root/'pilot'/f'H.rank{rank}')
        if tuple(row['h'][2:4])!=(rank,peers[rank].pid):raise Refusal('native packet kernel rank/PID binding')
        for key in ['h','fft']:
            if row[key].tolist()!=profile['layout'][str(rank)][key]:
                # Runtime PID is the only changing header field.
                if key!='h':raise Refusal('native FFT layout')
                header=row['h'].copy();header[3]=0
                if header.tolist()!=profile['layout'][str(rank)]['h']:raise Refusal('native header layout')
        if np.max(abs(row['B']-B))>1e-12 or np.any(row['k']):raise Refusal('G+k/cell physical frame')
        if abs(row['scalars'][1]-288)>1e-8 or abs(row['scalars'][2]-.001)>1e-14:raise Refusal('saved charge/FD sigma')
        p,n=map(int,row['h'][4:6]);local=np.r_[np.arange(n),np.arange(p,p+n)]
        ids=np.array([lookup[tuple(g)] for g in row['G']]);global_=np.r_[ids,N+ids]
        keys=set(map(tuple,row['G']))
        if len(keys)!=n or seen&keys:raise Refusal('duplicate physical G')
        seen|=keys
        if row['trial'][local].tobytes()!=np.ascontiguousarray(trial[global_]).tobytes():raise Refusal('original probes not byte-exact')
        padding=np.r_[np.arange(n,p),np.arange(p+n,2*p)]
        for key in parts:
            if np.any(row[key][padding]):raise Refusal('nonzero native padding')
            parts[key][global_]=row[key][local]
        keys=set(map(tuple,row['densityG']))
        if len(keys)!=len(row['densityG']) or seenrho&keys:raise Refusal('density G duplicate')
        seenrho|=keys;ix=np.array([rlookup[tuple(g)] for g in row['densityG']])
        if row['rhoG'][:,0].tobytes()!=np.ascontiguousarray(rv[ix]).tobytes():raise Refusal('saved rhoG not exact')
        if any(np.any(row[k][:,1:]) for k in ['rhoG','rhoR','vrs']):raise Refusal('nonmagnetic local model changed')
    if len(seen)!=N or len(seenrho)!=len(rv):raise Refusal('incomplete reciprocal coverage')
    Y=parts['full'][:,:6];A=P.conj().T@Y;scale=max(1.,np.linalg.norm(parts['full'],'fro'))
    component=np.linalg.norm(parts['full']-sum(parts[k] for k in ['kin','loc','nl']),'fro')/scale
    TR=np.linalg.norm(parts['full'][:,6:]-theta(Y),'fro')/max(1.,np.linalg.norm(Y,'fro'))
    herm=np.linalg.norm(A-A.conj().T,'fro')/max(1.,np.linalg.norm(A,2))
    kinetic=np.max(abs(parts['kin']-np.tile(np.sum((G@B.T)**2,axis=1),2)[:,None]*trial))
    if max(component,TR,herm)>1e-8 or kinetic>1e-10:raise Refusal('full-H component/Theta/Hermiticity/kinetic gate')
    QY=Y-P@np.linalg.solve(S,A)
    sector=lambda start,end:np.trace(np.linalg.solve(S[start:end,start:end],A[start:end,start:end])).real/(end-start)
    return dict(packet_readback=True,original_frame_unchanged=True,static_trace_eV=float((sector(0,2)-sector(2,6))*13.605693122994),
        complement_singulars_Ry=np.linalg.svd(QY,compute_uv=False).tolist(),component_relative=float(component),
        Theta_relative=float(TR),Hermiticity_relative=float(herm),kinetic_error_Ry=float(kinetic),
        full_saved_eigenpair_residual_certified=False,numerical_2meV_error_certified=False,
        numerical_consistency_only=True,physical_gap=False,physical_xc=None)
