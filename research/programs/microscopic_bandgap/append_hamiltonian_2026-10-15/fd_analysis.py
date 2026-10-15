"""304-space FD response and actual full-vector residuals, not nonlinear SCF."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.special import expit,xlogy
from accepted import HERE,PRIVATE,OLD,frames,td_operations,sha


def main():
    target=HERE/'fd_result.json'
    if target.exists():raise FileExistsError('preserve first fixed-H FD outcome')
    science=json.loads((HERE/'native_science.json').read_text());assert science['scientific_pass']
    assert sha(science['assembled_action_path'])==science['assembled_action_sha256']
    f,b,G,Q,L,V=frames();a=np.load(science['assembled_action_path']);HV=a['HV'];raw=a['H'];H=(raw+raw.conj().T)/2;N=len(G);d=2*N
    eig,U=np.linalg.eigh(H);lo=float(eig[0]-1);hi=float(eig[-1]+1)
    for _ in range(120):
        mu=(lo+hi)/2
        if sum(expit((mu-eig)/.001))<144:lo=mu
        else:hi=mu
    mu=(lo+hi)/2;occ=expit((mu-eig)/.001);charge=float(sum(occ));assert abs(charge-144)<1e-8
    FD=(U*occ)@U.conj().T;S=f['source'][:,:146];w=f['weights'][:146];A=V.conj().T@S;D=(A*w)@A.conj().T
    entropy=float(-sum(xlogy(occ,occ)+xlogy(1-occ,1-occ)));entropy0=float(4*np.log(2))
    R=HV-V@raw;RU=R@U;resnorm=np.linalg.norm(RU,axis=0);fullres=HV@U-(V@U)*eig
    assert np.max(abs(np.linalg.norm(fullres,axis=0)-resnorm))<1e-10
    pairspread=float(max(abs(eig[1::2]-eig[::2])))
    P=f['P'];PU=P.conj().T@(V@U);weights6=np.sum(abs(PU[:2])**2,axis=0);weights8=np.sum(abs(PU[2:])**2,axis=0);frame_missing=float(np.linalg.norm(np.eye(6)-P.conj().T@V@(V.conj().T@P),2))
    # Fixed absolute clustering threshold; weights, not sorted labels, identify probes.
    clusters=[];start=0
    for stop in range(1,305):
        if stop==304 or eig[stop]-eig[stop-1]>1e-8:
            z=slice(start,stop);clusters.append(dict(indices_1based=[start+1,stop],dimension=stop-start,energy_min_Ry=float(eig[start]),energy_max_Ry=float(eig[stop-1]),spread_Ry=float(eig[stop-1]-eig[start]),Gamma6_weight=float(sum(weights6[z])),Gamma8_weight=float(sum(weights8[z])),occupation_sum=float(sum(occ[z])),maximum_whole_eigenstate_residual_Ry=float(max(resnorm[z]))));start=stop
    top6=sorted(clusters,key=lambda x:x['Gamma6_weight'],reverse=True)[:6];top8=sorted(clusters,key=lambda x:x['Gamma8_weight'],reverse=True)[:6]
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    def rotate(X,op):
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);out=np.empty_like(X).reshape(2,N,X.shape[1]);out[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],X.reshape(2,N,X.shape[1]));return out.reshape(X.shape)
    cov=[]
    for op in td_operations():
        Ug=V.conj().T@rotate(V,op);cov.append(float(np.linalg.norm(Ug@FD@Ug.conj().T-FD,2)))
    Ut=V.conj().T@theta(V);tr=float(np.linalg.norm(Ut@FD.conj()@Ut.conj().T-FD,2));symmetry=max(cov+[tr])
    # Charge-matched FD is the unique finite-space free-energy minimizer at FIXED H.
    linear_energy=float(np.trace(H@(FD-D)).real);linear_free=linear_energy-.001*(entropy-entropy0);assert linear_free<1e-10
    # Full commutator for the new supported density, independently of complement.
    W=HV@FD;X=np.column_stack((W,V));_,T=np.linalg.qr(X,mode='reduced');J=np.block([[np.zeros((304,304)),np.eye(304)],[-np.eye(304),np.zeros((304,304))]])
    comm=T@J@T.conj().T;evc=np.linalg.eigvalsh((1j*comm+(1j*comm).conj().T)/2);commop=float(max(abs(evc)))
    M=json.loads((OLD/'stationarity_result.json').read_text())['H_operator_norm_upper_Ry'] if 'H_operator_norm_upper_Ry' in json.loads((OLD/'stationarity_result.json').read_text()) else json.loads((OLD/'native_science.json').read_text())['H_operator_norm_upper_Ry']
    residualF=float(np.linalg.norm(R,'fro'));differenceF=float(np.linalg.norm(D-FD,'fro'));taildim=d-304
    gapfree_upperF=min(np.sqrt(d),differenceF+np.sqrt(2)*residualF/(4*.001)+np.sqrt(taildim))
    needed_tail_charge=1e-8;required_offset=.001*np.log(taildim/needed_tail_charge-1)
    active=np.flatnonzero((occ>1e-8)&(occ<1-1e-8));old=np.load(OLD/'native_matrices.npz');e0=np.linalg.eigvalsh((old['H_QQ']+old['H_QQ'].conj().T)/2)
    path=PRIVATE/'p2/fixed_H_FD_candidate.npz';np.savez(path,energies_Ry=eig,coefficients_in_V=U,occupations=occ,D_V=FD)
    result=dict(status='CALCULATED fixed-H304 FD response, NOT whole-space or outer HSEstationarity',finite_state_symmetry_gate_pass=symmetry<1e-8 and pairspread<1e-8,charge_e=charge,mu_Ry=mu,sigma_Ry=.001,entropy_kB=entropy,old_trial_entropy_kB=entropy0,density_change_from_D0_op=float(np.linalg.norm(D-FD,2)),density_change_from_D0_F=differenceF,all24_FD_density_Td_defects_op=cov,FD_density_Theta_defect_op=tr,max_Kramers_pair_splitting_Ry=pairspread,all_Ritz_energies_Ry=eig.tolist(),all_occupations=occ.tolist(),whole_eigenstate_residuals_Ry=resnorm.tolist(),occupied_weighted_whole_residual_F_Ry=float(np.linalg.norm(RU*occ,'fro')),occupied_sqrt_weighted_whole_residual_F_Ry=float(np.linalg.norm(RU*np.sqrt(occ),'fro')),offspace_full_HV_F_Ry=residualF,partially_occupied_indices_1based=(active+1).tolist(),partially_occupied_eigenstate_residuals_Ry=resnorm[active].tolist(),partially_occupied_max_residual_Ry=float(max(resnorm[active])) if len(active) else None,old152_partial_residual_Ry=.02625424168,old152_lowest146_to_new_Ritz_max_change_Ry=float(max(abs(eig[:146]-e0[:146]))),original_physical_frame_missing_op=frame_missing,largest_Gamma6_weight_clusters=top6,largest_Gamma8_weight_clusters=top8,fixed_H_linear_energy_change_Ry=linear_energy,fixed_H_FD_free_energy_change_Ry=linear_free,NOT_nonlinear_HSE_energy_change=True,new_supported_FD_fullspace_commutator_op_Ry=commop,new_supported_FD_commutator_lower_before_rounding=commop/(2*M),new_supported_FD_lower_not_interval_certified=True,D0_whole_space_lower_previous=1.221127813e-7,gapfree_D0_to_wholeFD_upper_F_at_same_mu=gapfree_upperF,upper_is_noninformative=True,complement_dimension=taildim,complement_lower_spectral_bound_available=False,required_complement_lower_above_mu_Ry_for_tailcharge1e8=required_offset,tailcharge_condition_is_sufficient_conditional_NOT_measured=True,FD_occupation_beyond176_e=sum(occ[176:]),candidate_path=str(path),candidate_sha256=sha(path),H_at_new_density_NOT_acquired=True,HSE_converged=False,physical_xc=None,source_sha256={str(p):sha(p) for p in [Path(__file__),HERE/'native_science.json',science['assembled_action_path'],PRIVATE/'trial.npz',PRIVATE/'full_action_basis.npz']})
    np.savez(HERE/'fd_matrices.npz',H=H,D0=D,FD=FD,eigenvalues_Ry=eig,occupations=occ,coefficients=U,whole_residual_Gram=R.conj().T@R)
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['all24_FD_density_Td_defects_op','all_Ritz_energies_Ry','all_occupations','whole_eigenstate_residuals_Ry','source_sha256']},indent=2))


if __name__=='__main__':main()
