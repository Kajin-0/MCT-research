"""Native static actions, exact saved rhoG and genuine independent Theta trials."""
from pathlib import Path
import json,sys,re
import numpy as np
import h5py
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16h_20261015')
sys.path.insert(0,str(BASE/'native_matched_pilot_2026-10-11'))
from packets import Reader


def decode(path):
    r=Reader(path);h=r.take('<i8',(16,));assert tuple(h[[0,1,9,10,12,13]])==(70251521,1,352,4,16,12)
    p,n,ng,nr,ns=map(int,h[[4,5,6,7,8]]);assert 0<n<=p<=50000 and max(ng,nr,ns)<=2**22
    fft=r.take('<i8',(14,2));B=r.take('<f8',(3,3));k=r.take('<f8',(3,));scalars=r.take('<f8',(6,));G=r.take('<i8',(3,n)).T;densityG=r.take('<i8',(3,ng)).T
    fields={x:r.take('<c16',(2*p,12)) for x in ['trial','kin','loc','nl','full']};rhoG=r.take('<c16',(ng,4));rhoR=r.take('<f8',(nr,4));vrs=r.take('<f8',(ns,4));r.end()
    return dict(h=h,fft=fft,B=B,k=k,scalars=scalars,G=G,densityG=densityG,rhoG=rhoG,rhoR=rhoR,vrs=vrs,**fields)


def validate(root,member):
    f=np.load(PRIVATE/'physical_frame.npz');P=f['P'];G=f['G'];B=f['B'];N=len(G);lookup={tuple(g):i for i,g in enumerate(G)};trial=np.column_stack((P,f['ThetaP']));minus=np.array([lookup[tuple(-g)] for g in G]);theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    rows=[decode(root/'pilot'/f'H.rank{i}') for i in [0,1]];ranks=json.loads((root/'RANKS.json').read_text());parts={x:np.zeros_like(trial) for x in ['kin','loc','nl','full']};seen=set();seenrho=set();charges=[];rhoerr=0.;spin=0.
    with h5py.File(root/'out/r07pbe.save/charge-density.hdf5') as h:
        rg=np.array(h['MillerIndices']);rv=np.asarray(h['rhotot_g']).view(np.complex128);rlookup={tuple(g):i for i,g in enumerate(rg)}
    for rank,b in enumerate(rows):
        assert b['h'][2]==rank and b['h'][3]==ranks[str(rank)]['pid'];assert np.max(abs(b['B']-B))<1e-12 and np.max(abs(b['k']))<1e-12
        assert abs(b['scalars'][1]-288)<1e-8 and abs(b['scalars'][2]-.001)<1e-14;charges.append(float(b['scalars'][1]))
        p,n=map(int,b['h'][4:6]);i=np.r_[np.arange(n),np.arange(p,p+n)];ix=np.array([lookup[tuple(g)] for g in b['G']]);j=np.r_[ix,N+ix];assert not seen.intersection(map(tuple,b['G']));seen.update(map(tuple,b['G']))
        assert b['trial'][i].tobytes()==np.ascontiguousarray(trial[j]).tobytes()
        for k in parts:parts[k][j]=b[k][i];assert np.all(np.isfinite(b[k]))
        rix=np.array([rlookup[tuple(g)] for g in b['densityG']]);assert not seenrho.intersection(map(tuple,b['densityG']));seenrho.update(map(tuple,b['densityG']))
        assert b['rhoG'][:,0].tobytes()==np.ascontiguousarray(rv[rix]).tobytes(),'saved rhoG changed'
        assert np.max(abs(b['rhoG'][:,1:]))==0;spin=max(spin,float(np.max(abs(b['vrs'][:,1:]))));assert spin==0
    assert len(seen)==N and len(seenrho)==len(rv)
    component_error=float(np.linalg.norm(parts['full']-sum(parts[k] for k in ['kin','loc','nl']),'fro')/max(1.,np.linalg.norm(parts['full'],'fro')));assert component_error<1e-8
    T=np.tile(np.sum((G@B.T)**2,axis=1),2);kinetic=float(np.max(abs(parts['kin']-T[:,None]*trial)));assert kinetic<1e-10
    HP=parts['full'][:,:6];H=P.conj().T@HP;scale=max(1.,float(np.linalg.norm(H,2)));herm=float(np.linalg.norm(H-H.conj().T,'fro')/scale);TR=float(np.linalg.norm(parts['full'][:,6:]-theta(HP),'fro')/max(1.,np.linalg.norm(HP,'fro')));assert max(herm,TR)<1e-8
    projections={k:P.conj().T@parts[k][:,:6] for k in ['kin','loc','nl']};stdout=(root/'pw.out').read_text();assert 'The initial density is read from file' in stdout and 'Initial potential from superposition' not in stdout and 'R07_STATIC_H_COMPLETE' in stdout and 'JOB DONE.' in stdout
    groups=re.findall(r'(\d+) Sym\. Ops\.',stdout);assert groups and int(groups[0])==({'unshared':24,'shared':4}[member])
    profile=json.loads((PRIVATE/'jobs/PROFILE.json').read_text());import hashlib
    sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    for p,row in profile['copied_saves'][member].items():assert sha(p)==row['sha256'] and sha(row['source'])==row['sha256']
    np.savez(HERE/(member+'_matrices.npz'),H=H,**projections,HP=HP)
    ordering=lambda M:float((np.trace(M[:2,:2])/2-np.trace(M[2:,2:])/4).real*13.605693122994)
    result=dict(scientific_pass=True,member=member,saved_rhoG_bitwise=True,saved_source_files_unchanged=True,native_charge_e=charges,original_reference_probe_byte_readback=True,full_native_vs_components_relative=component_error,Hermiticity_relative=herm,independent_Theta_kernel_relative=TR,kinetic_max_abs_Ry=kinetic,zero_native_local_magnetic_potential=True,native_chemical_group_order=int(groups[0]),static_trace_ordering_eV=ordering(H),component_orderings_eV={k:ordering(M) for k,M in projections.items()},static_physical_probe_outside_frame_F_Ry=float(np.linalg.norm(HP-P@H,'fro')),not_a_material_gap=True,no_SCF_or_HSE_run=True,physical_xc=None)
    (HERE/(member+'_science.json')).write_text(json.dumps(result,indent=2)+'\n');return result
