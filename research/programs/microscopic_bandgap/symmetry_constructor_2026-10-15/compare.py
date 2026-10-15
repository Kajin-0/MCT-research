"""Actual native direct actions, independent TR and new auxiliary compression."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, solve_triangular

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hybrid_convergence_2026-10-15'))
from packets import Reader,packet


def input_record(root,rank):
    r=Reader(root/'pilot'/f'input.rank{rank}');h=r.take('<i8',(8,));p,n,nt=map(int,h[[3,4,7]])
    assert tuple(h)==(70251501,1,rank,p,n,176,2,376)
    x=dict(h=h,B=r.take('<f8',(3,3)),k=r.take('<f8',(3,)),G=r.take('<i8',(3,n)).T,et=r.take('<f8',(176,)),wg=r.take('<f8',(176,)),phi=r.take('<c16',(p*2,176)),reverse=r.take('<c16',(p*2,176)),trial=r.take('<c16',(p*2,nt)))
    r.end();return x


def output_record(root,rank,source):
    r=Reader(root/'pilot'/f's{source}.rank{rank}');h=r.take('<i8',(8,));p,n,nt=map(int,h[[4,5,7]])
    assert tuple(h[[0,1,2,6,7]])==(70251502,1,rank,source,376)
    x=dict(h=h,extent=r.take('<i8',(10,)),B=r.take('<f8',(3,3)),k=r.take('<f8',(3,)),scalars=r.take('<f8',(4,)),bounds=r.take('<f8',(4,)),G=r.take('<i8',(3,n)).T,et=r.take('<f8',(176,)),wg=r.take('<f8',(176,)),phi=r.take('<c16',(p*2,176)),trial=r.take('<c16',(p*2,nt)),action=r.take('<c16',(p*2,nt)))
    r.end();return x


def relative(x,y):
    return float(np.linalg.norm(x-y)/max(1.,np.linalg.norm(x),np.linalg.norm(y)))


def validate_native(root):
    old=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8c_20261015/p1/host')
    ranks=json.loads((root/'RANKS.json').read_text());ins=[input_record(root,r) for r in [0,1]]
    G=np.array(sorted(tuple(g) for b in ins for g in b['G']));N=len(G)
    assert N==len(set(map(tuple,G)))==10827
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G])
    Y={s:np.empty((2*N,376),complex) for s in [1,2]}
    X=np.empty_like(Y[1]); phi=np.empty((2*N,176),complex); oldW=np.empty_like(phi)
    bound=[]; checks=[]
    for rank,b in enumerate(ins):
        p,n=map(int,b['h'][3:5]);ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        X[glob]=b['trial'][ix];phi[glob]=b['phi'][ix]
        prior=packet(old,'before',rank,1);prior_a=packet(old,'after',rank,1)
        assert b['phi'].tobytes()==prior['phi'].tobytes()
        assert b['trial'][:,364:370].tobytes()==prior_a['probe'].tobytes()
        oldW[glob]=prior['direct'][ix]
        for source in [1,2]:
            v=output_record(root,rank,source)
            assert int(v['h'][3])==ranks[str(rank)]['pid']
            assert tuple(v['h'][4:6])==(p,n)
            for key in ['B','k','G','et','wg','trial']:
                assert v[key].tobytes()==b[key].tobytes(),(rank,source,key)
            assert v['phi'].tobytes()==b['phi' if source==1 else 'reverse'].tobytes()
            assert tuple(v['extent'][:3])==(60,60,60) and tuple(v['extent'][6:])==(1,146,176,1)
            np.testing.assert_allclose(v['scalars'],[1.,.25,200.,.106],rtol=0,atol=1e-12)
            assert v['bounds'][0]>=0 and min(v['bounds'][1:])>0
            Y[source][glob]=v['action'][ix]
            bound.append(v['bounds'].tolist())
            checks.append(dict(source=source,rank=rank,canonical_actual_input_byte_exact=True))
    wg=ins[0]['wg']; assert abs(sum(wg)-144)<1e-8
    theta=lambda v:np.r_[v[N+minus].conj(),-v[minus].conj()]
    Q=X[:,:364];P=X[:,364:370]
    assert np.array_equal(X[:,370:],theta(P))
    J=np.zeros((376,376))
    for j in range(0,364,2):J[j+1,j]=1;J[j,j+1]=-1
    for j in range(6):J[370+j,364+j]=1;J[364+j,370+j]=-1
    assert np.linalg.norm(theta(X)-X@J,2)<1e-10
    gerr=float(np.linalg.norm(Q.conj().T@Q-np.eye(364),2))
    dphi=float(np.linalg.norm(phi-Q@(Q.conj().T@phi),2))
    dp=float(np.linalg.norm(P-Q@(Q.conj().T@P),2))
    assert max(gerr,dphi,dp)<1e-10
    covariance=relative(Y[2]@J,theta(Y[1]))
    covariance2=relative(Y[1]@J,theta(Y[2]))
    assert max(covariance,covariance2)<=1e-8
    Vbar=(Y[1]+Y[2])/2
    W=-Vbar[:,:364]
    H=Q.conj().T@W
    herm=relative(H,H.conj().T); assert herm<=1e-8
    H=(H+H.conj().T)/2
    he,U=eigh(H); assert min(he)>1e-6 and max(he)/min(he)<1e8
    a=max(v[3] for v in bound)
    source_action_bound=a*dphi;reference_action_bound=a*dp
    assert max(source_action_bound,reference_action_bound)<=1e-8
    L=np.linalg.cholesky(H)
    Xi=solve_triangular(L,W.conj().T,lower=True).conj().T
    # Independent eigendecomposition-based factorization, not native ACE calls.
    Xi2=(W@U)/np.sqrt(he)
    aceQ=Xi@(Xi.conj().T@Q)
    source_action=relative(aceQ,W)
    factorization=relative(Xi@(Xi.conj().T@P),Xi2@(Xi2.conj().T@P))
    aceP=-Xi@(Xi.conj().T@P)
    directP=Vbar[:,364:370]
    probe_action=relative(aceP,directP)
    TR_ace=relative(-Xi@(Xi.conj().T@theta(Q)),theta(-aceQ))
    # New independent norm control; OLD BYTE REFUSAL is not changed or retested.
    C=Q.conj().T@phi;CT=Q.conj().T@theta(phi)
    retained_source=relative(Y[1][:,:364]@C,oldW)
    assert max(source_action,factorization,probe_action,TR_ace,retained_source)<=1e-8
    Dq=((C*wg)@C.conj().T+(CT*wg)@CT.conj().T)/2
    energy_matrix=float(-np.trace(Dq@H).real/2)
    vp=Vbar[:,:364]@C;vt=Vbar[:,:364]@CT
    energy_contraction=float(.25*sum(wg*(np.sum(phi.conj()*vp,axis=0).real+np.sum(theta(phi).conj()*vt,axis=0).real)))
    energy_old=float(.5*wg@np.sum(phi.conj()*oldW,axis=0).real)
    energy_reconstructed_old=float(.5*wg@np.sum(phi.conj()*(Y[1][:,:364]@C),axis=0).real)
    assert abs(energy_matrix-energy_contraction)<=1e-8
    assert abs(energy_old-energy_reconstructed_old)<=1e-8
    Jq=J[:364,:364]
    density_TR=float(np.linalg.norm(Dq-Jq@Dq.conj()@Jq.T,2))
    exchange_pair_splits=float(max(abs(he[::2]-he[1::2])))
    assert density_TR<=1e-8 and exchange_pair_splits<=1e-8
    # These are fixed projected exchange matrices, NOT HSE energy eigenvalues.
    F=P.conj().T@directP;F0=P.conj().T@Y[1][:,364:370]
    trace=lambda M:float(np.trace(M[:2,:2]).real/2-np.trace(M[2:,2:]).real/4)
    natural=eigh((Dq+Dq.conj().T)/2,eigvals_only=True)
    text=(root/'pw.out').read_text()
    assert text.count('R07_PAIRED_FOCK_SOURCE_COMPLETE')==2 and 'R07_PAIRED_FOCK_DONE' in text and 'JOB DONE.' in text
    result=dict(scientific_pass=True,status='CALCULATED native direct actions and OFFLINE TR-constrained ensemble compression',
        source_checks=checks,auxiliary_dimension=364,physical_solved_bands_unchanged=176,
        native_ACE_built=False,offline_ACE_constructor=True,SCF_performed=False,HSE_converged=False,
        source_cover_op=dphi,reference_cover_op=dp,auxiliary_Gram_error_op=gerr,
        actual_native_kernel_bounds=bound,operator_norm_upper_Ry=a,
        source_projection_action_upper_Ry=source_action_bound,reference_projection_action_upper_Ry=reference_action_bound,
        direct_covariance_all_trials_relative=covariance,direct_covariance_second_identity_relative=covariance2,
        enlarged_positive_Gram_min_Ry=float(min(he)),enlarged_positive_Gram_max_Ry=float(max(he)),enlarged_Gram_condition=float(max(he)/min(he)),
        enlarged_Gram_Hermiticity_relative=herm,offline_ACE_source_action_relative=source_action,
        independent_factorization_relative=factorization,offline_ACE_direct_reference_action_relative=probe_action,
        offline_ACE_TR_commutator_relative=TR_ace,new_retained_source_norm_control_relative=retained_source,
        old_BYTE_refusal_unchanged=True,TR_constrained_density_charge_e=float(np.trace(Dq).real),TR_constrained_density_TR_op=density_TR,
        natural_occupation_min=float(min(natural)),natural_occupation_max=float(max(natural)),
        exchange_Gram_pair_split_max_Ry=exchange_pair_splits,not_a_HSE_Kramers_band_splitting=True,
        constrained_ensemble_half_Fock_Ry=energy_matrix,independent_weighted_energy_Ry=energy_contraction,
        original_half_Fock_Ry=energy_old,half_Fock_change_Ry=energy_matrix-energy_old,
        projected_Gamma6_minus8_exchange_change_meV=(trace(F)-trace(F0))*13.605693122994*1000,
        physical_xc=None,qualified_self_consistent_nonmagnetic_host=False)
    np.savez(HERE/'operator_matrices.npz',positive_Gram=H,positive_Gram_eigenvalues=he,constrained_density=Dq,reference_exchange=F,original_reference_exchange=F0)
    (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
