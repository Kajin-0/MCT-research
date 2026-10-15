"""Complete same-D native action/readback, Galerkin FD and whole-space tests."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.special import expit

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'hybrid_convergence_2026-10-15'))
sys.path.insert(0,str(BASE/'native_matched_pilot_2026-10-11'))
from packets import Reader
from reference_irrep_check import td_operations


def decode(path):
    r=Reader(path);h=r.take('<i8',(16,));assert tuple(h[[0,1,6,7,13,14,15]])==(70251511,1,176,164,8,4,146)
    p,n,ng,nr,ns=map(int,h[[4,5,8,9,10]]);assert 0<n<=p<=10827 and ng<216000 and nr<=216000 and ns<=216000
    dims=r.take('<i8',(15,));fft=r.take('<i8',(14,3));B=r.take('<f8',(3,3));k=r.take('<f8',(3,));scalars=r.take('<f8',(6,));bounds=r.take('<f8',(12,));energies=r.take('<f8',(3,))
    G=r.take('<i8',(3,n)).T;density_G=r.take('<i8',(3,ng)).T;wg=r.take('<f8',(176,));mat=lambda m:r.take('<c16',(2*p,m))
    source=mat(176);trial=mat(164);kin=mat(164);loc=mat(164);nl=mat(164);fock=mat(164);control=mat(6)
    rhoG=r.take('<c16',(ng,4));rhoR=r.take('<f8',(nr,4));vrs=r.take('<f8',(ns,4));r.end()
    return dict(h=h,dims=dims,fft=fft,B=B,k=k,scalars=scalars,bounds=bounds,energies=energies,G=G,density_G=density_G,wg=wg,source=source,trial=trial,kin=kin,loc=loc,nl=nl,fock=fock,control=control,rhoG=rhoG,rhoR=rhoR,vrs=vrs)


def validate_native(root):
    f=np.load(root.parent.parent/'trial.npz');Q=f['Q'];G=f['G'];D=f['D_Q'];N=len(G);lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    rec=[decode(root/'pilot'/f'H.rank{r}') for r in [0,1]];ranks=json.loads((root/'RANKS.json').read_text());seen=set();assembled={k:np.zeros((2*N,m),complex) for k,m in [('source',176),('trial',164),('kin',164),('loc',164),('nl',164),('fock',164),('control',6)]};rho=np.zeros((60,60,60,4));rslices=set();errors={}
    for rank,b in enumerate(rec):
        assert b['h'][2]==rank and b['h'][3]==ranks[str(rank)]['pid']
        for field in ['B','k','scalars','bounds','energies','wg']:np.testing.assert_array_equal(b[field],rec[0][field])
        assert abs(b['scalars'][1]-1)<1e-12 and abs(b['scalars'][2]-.25)<1e-12 and abs(b['scalars'][3]-200)<1e-10 and abs(b['scalars'][4]-.106)<1e-12 and abs(b['scalars'][5]-.001)<1e-14
        assert b['dims'][3]==146 and b['dims'][7]==1
        p,n=map(int,b['h'][4:6]);ix=np.r_[np.arange(n),np.arange(p,p+n)];loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        assert not(seen & set(map(tuple,b['G'])));seen.update(map(tuple,b['G']))
        for key in assembled:assembled[key][glob]=b[key][ix]
        np.testing.assert_array_equal(b['wg'],f['weights'])
        for key,wanted in [('source',f['source']),('trial',f['trial'])]:
            assert b[key][ix].tobytes()==np.ascontiguousarray(wanted[glob]).tobytes(),key+' byte readback'
        for j in range(3):
            fft=b['fft'][:,j];assert tuple(fft[:6])==(60,60,60,60,60,60) and tuple(fft[[6,8,10,11]])==(60,0,1,2)
        fft=b['fft'][:,0];z0,nz=map(int,fft[[9,7]]);physical=60*60*nz;assert len(b['rhoR'])>=physical
        assert not(rslices & set(range(z0,z0+nz)));rslices.update(range(z0,z0+nz));rho[:,:,z0:z0+nz]=b['rhoR'][:physical].reshape(60,60,nz,4,order='F')
    assert len(seen)==N and len(rslices)==60
    H=sum(assembled[k] for k in ['kin','loc','nl','fock']);HQ=H[:,:152];HQsmall=Q.conj().T@HQ;scale=max(1.,float(np.linalg.norm(HQsmall,2)))
    control=float(np.linalg.norm(H[:,152:158]-assembled['control'],'fro')/max(1.,np.linalg.norm(assembled['control'],'fro')));assert control<=1e-8
    B=rec[0]['B'];T=np.tile(np.sum((G@B.T)**2,axis=1),2);errors['kinetic_physicalG_action_abs_Ry']=float(np.max(abs(assembled['kin']-T[:,None]*f['trial'])));assert errors['kinetic_physicalG_action_abs_Ry']<1e-10
    predicted=np.load(root.parent.parent/'expected_density.npz');erho=float(np.max(abs(rho-predicted['rhoR'])));assert erho<1e-10
    bounds=rec[0]['bounds'];omega=rec[0]['scalars'][0];charge=float(rho[:,:,:,0].sum()*omega/60**3);assert abs(charge-144)<1e-8 and abs(bounds[9]-144)<1e-8 and abs(bounds[10]-4*np.log(2))<1e-12
    zero=[]
    for b in rec:
        ix=np.flatnonzero(np.all(b['density_G']==0,axis=1))
        if len(ix):zero.extend(b['rhoG'][ix,0].real.tolist())
    assert len(zero)==1 and abs(zero[0]*omega-144)<1e-8
    herm=float(np.linalg.norm(HQsmall-HQsmall.conj().T,'fro')/scale);assert herm<1e-8
    cov=[]
    def rotate(S,op):
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);out=np.empty_like(S).reshape(2,N,S.shape[1]);out[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],S.reshape(2,N,S.shape[1]));return out.reshape(S.shape)
    for op in td_operations():
        U=Q.conj().T@rotate(Q,op);cov.append(float(np.linalg.norm(rotate(HQ,op)-HQ@U,'fro')/scale))
    U=Q.conj().T@theta(Q);tr=float(np.linalg.norm(theta(HQ)-HQ@U,'fro')/scale)
    translations=[]
    for i,j in [(0,1),(0,2),(1,2)]:
        phase=np.tile((-1.)**((G[:,i]+G[:,j])%2),2);U=Q.conj().T@(phase[:,None]*Q);translations.append(float(np.linalg.norm(phase[:,None]*HQ-HQ@U,'fro')/scale))
    independentTR=float(np.linalg.norm(H[:,158:164]-theta(H[:,152:158]),'fro')/max(1.,np.linalg.norm(H[:,152:158],'fro')))
    assert max(cov+[tr,independentTR]+translations)<1e-8
    eig,vec=np.linalg.eigh((HQsmall+HQsmall.conj().T)/2);lo=float(min(eig)-1);hi=float(max(eig)+1)
    for _ in range(100):
        mu=(lo+hi)/2
        if sum(expit((mu-eig)/.001))<144:lo=mu
        else:hi=mu
    mu=(lo+hi)/2;occ=expit((mu-eig)/.001);FD=(vec*occ)@vec.conj().T;chargeFD=float(sum(occ));assert abs(chargeFD-144)<1e-8
    residual=HQ-Q@HQsmall;comm=HQsmall@D-D@HQsmall
    commF=float(np.sqrt(np.linalg.norm(comm,'fro')**2+2*np.linalg.norm(residual@D,'fro')**2))
    assert bounds[4]>=-1e-12 and bounds[8]>0
    lower=commF/(2*bounds[8]);lowerOp=lower/np.sqrt(2*N)
    eval_residual=HQ@vec-Q@vec*eig
    P=f['P'];Href=P.conj().T@H[:,152:158];tr6=np.trace(Href[:2,:2])/2;tr8=np.trace(Href[2:,2:])/4
    gram=-Q.conj().T@assembled['fock'][:,:152];exHerm=float(np.linalg.norm(gram-gram.conj().T,'fro'));assert exHerm<1e-8*max(1.,float(np.linalg.norm(gram,2)))
    pos=np.linalg.eigvalsh((gram+gram.conj().T)/2);assert min(pos)>-1e-8
    exchange=float(.5*np.trace(D@(Q.conj().T@assembled['fock'][:,:152])).real)
    # Universal finite-complement tail upper, reported as uninformative rather
    # than inventing a positive complement lower bound from kinetic Ritz values.
    coupling=float(np.linalg.norm(residual,'fro'));whole_upper=float(min(np.sqrt(2*N),np.linalg.norm(D-FD,'fro')+np.sqrt(2)*coupling/.004+np.sqrt(2*N-152)))
    result=dict(scientific_pass=True,same_density_complete_native_action=True,source_byte_readback=True,native_density_reconstruction_max_abs=erho,independent_density_charge_e=charge,native_charge_e=float(bounds[9]),trial_entropy_kB=float(bounds[10]),full_native_hpsi_vs_component_error_relative=control,kinetic_check=errors,Hermiticity_relative_F=herm,all24_H_Td_covariance_relative_F=cov,Theta_H_covariance_relative_F=tr,primitive_translation_H_covariance_relative_F=translations,independent_original_probe_Theta_covariance_relative_F=independentTR,projected_FD_charge_e=chargeFD,projected_FD_mu_Ry=mu,projected_FD_density_error_F=float(np.linalg.norm(D-FD,'fro')),projected_FD_density_error_op=float(np.linalg.norm(D-FD,2)),projected_FD_natural_occupations=occ.tolist(),Galerkin_ritz_energies_Ry=eig.tolist(),Ritz_fullspace_residuals_Ry=np.linalg.norm(eval_residual,axis=0).tolist(),offspace_HQ_F_Ry=coupling,occupied_weighted_offspace_HQ_F_Ry=float(np.linalg.norm(residual@D,'fro')),fullspace_commutator_F_Ry=commF,H_operator_norm_upper_Ry=float(bounds[8]),H_norm_bound_components=bounds[:9].tolist(),whole_space_FD_density_error_lower_F=lower,whole_space_FD_density_error_lower_op=lowerOp,whole_space_FD_density_error_upper_F=whole_upper,whole_space_upper_is_noninformative=True,positive_complement_lower_bound_available=False,fixed_original_reference_H_ordering_eV=float((tr6-tr8).real*13.605693122994),fixed_reference_Gamma6_block_defect_Ry=float(np.linalg.norm(Href[:2,:2]-tr6*np.eye(2),2)),fixed_reference_Gamma8_block_defect_Ry=float(np.linalg.norm(Href[2:,2:]-tr8*np.eye(4),2)),direct_Fock_half_energy_Ry=exchange,positive_Fock_Gram_min_Ry=float(min(pos)),positive_Fock_Gram_max_Ry=float(max(pos)),native_Hartree_XC_VXC_Ry=rec[0]['energies'].tolist(),HSE_SCF_converged=False,FD_stationarity_qualified=False,no_native_solved_spectrum_claim=True,physical_xc=None)
    np.savez(HERE/'native_matrices.npz',H_QQ=HQsmall,D_Q=D,FD_Q=FD,H_reference=Href,Fock_QQ=-gram,offspace_Gram=residual.conj().T@residual)
    (HERE/'native_science.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');return result
