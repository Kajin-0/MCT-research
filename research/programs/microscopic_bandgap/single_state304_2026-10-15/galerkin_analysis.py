"""Read-only fixed-H scientific follow-through after accepted single-native acquisition.

No previous action columns, no native execution, no density/occupation modification.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy.special import expit,xlogy
HERE=Path(__file__).resolve().parent
PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8u_20261015')
sys.path.insert(0,str(HERE.parent/'native_matched_pilot_2026-10-11'))
from reference_irrep_check import td_operations
SIGMA=.001

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def fd(H):
    e,U=np.linalg.eigh((H+H.conj().T)/2)
    lo=float(min(e)-1);hi=float(max(e)+1)
    for _ in range(100):
        mu=(lo+hi)/2
        if expit((mu-e)/SIGMA).sum()<144:lo=mu
        else:hi=mu
    mu=(lo+hi)/2;w=expit((mu-e)/SIGMA)
    assert abs(w.sum()-144)<1e-8
    F=(U*w)@U.conj().T
    entropy=float(-sum(xlogy(w,w)+xlogy(1-w,1-w)))
    return e,U,mu,w,F,entropy

def main():
    accepted=json.loads((PRIVATE/'p1/host/FINAL.json').read_text())
    assert accepted['accepted'] and accepted['terminal_pass'] and accepted['scientific_pass']
    f=np.load(PRIVATE/'trial.npz');a=np.load(PRIVATE/'full_actions.npz');V=f['Q'];HV=a['HV'];H=a['H'];D=f['D_Q'];P=f['P'];G=f['G'];N=len(G);M=2*N
    assert H.shape==(304,304) and HV.shape==V.shape
    A=(H+H.conj().T)/2;R=HV-V@A
    old=np.load(PRIVATE.parent/'h8h_20261015/trial.npz')['Q']
    C=V.conj().T@old;coverage=float(np.linalg.norm(old-V@C,'fro'))
    assert coverage<1e-8
    H152=C.conj().T@A@C;D152=C.conj().T@D@C
    e,U,mu,w,F,S=fd(A);e0,U0,mu0,w0,F0,S0=fd(H152)
    fullvectors=V@U;fullres=HV@U-fullvectors*e
    # Whole-H commutator norms for the two supported densities. This is not
    # their unknown whole-space FD error, and needs no complement spectral gap.
    def comm(B):
        return float(np.sqrt(np.linalg.norm(A@B-B@A,'fro')**2+2*np.linalg.norm(R@B,'fro')**2))
    mlookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([mlookup[tuple(-g)] for g in G])
    def theta(X):return np.r_[X[N+minus].conj(),-X[minus].conj()]
    def rotate(X,op):
        dest=np.array([mlookup[tuple(g)] for g in G@op['spatial'].T]);Y=np.empty_like(X).reshape(2,N,X.shape[1]);Y[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],X.reshape(2,N,X.shape[1]));return Y.reshape(X.shape)
    J=V.conj().T@theta(V);tr=float(np.linalg.norm(F-J@F.conj()@J.conj().T,'fro'))
    cubic=[]
    for op in td_operations():
        K=V.conj().T@rotate(V,op);cubic.append(float(np.linalg.norm(F-K@F@K.conj().T,'fro')))
    # Actual energy clusters: no averaging or forced Kramers/quartet restoration.
    groups=[];start=0
    for i in range(1,305):
        if i==304 or e[i]-e[i-1]>1e-8:
            ix=slice(start,i);X=fullvectors[:,ix];Pweight=abs(P.conj().T@X)**2
            groups.append(dict(bands_1based=[start+1,i],multiplicity=i-start,min_Ry=float(e[start]),max_Ry=float(e[i-1]),width_Ry=float(e[i-1]-e[start]),Gamma6_weight=float(Pweight[:2].sum()),Gamma8_weight=float(Pweight[2:].sum()),occupation_min=float(min(w[ix])),occupation_max=float(max(w[ix])),full_residual_max_Ry=float(max(np.linalg.norm(fullres[:,ix],axis=0)))))
            start=i
    eigR=np.linalg.eigvalsh(R.conj().T@R)
    RF=float(np.linalg.norm(R,'fro'));Rop=float(np.sqrt(max(0,max(eigR))))
    omitted=M-304
    # If independently known C >= L, its block-diagonal FD charge <=
    # omitted/(1+exp((L-mu)/sigma)). No such L is inferred from Ritz bands.
    required_L=float(mu+SIGMA*np.log(omitted/1e-8-1))
    unit_FD_error_bound=float(np.sqrt(2)*RF/(4*SIGMA))
    free_delta=float(np.trace(A@(F-D)).real-SIGMA*(S-4*np.log(2)))
    assert free_delta<1e-10
    result=dict(status='CALCULATED_FIXED_NATIVE_H_ONLY',source_result_sha256=sha(PRIVATE/'p1/host/FINAL.json'),full_action_sha256=sha(PRIVATE/'full_actions.npz'),all_H_columns_one_state=True,old_action_columns_used=False,old_space_containment_F=coverage,finite_plane_wave_spinor_dimension=M,dimensions=[152,304],sigma_Ry=SIGMA,mu152_Ry=mu0,mu304_Ry=mu,mu_shift_Ry=mu-mu0,charge152_e=float(w0.sum()),charge304_e=float(w.sum()),entropy152_kB=S0,entropy304_kB=S,trial_entropy_kB=float(4*np.log(2)),FD152_vs_D0_op=float(np.linalg.norm(D152-F0,2)),FD304_vs_D0_op=float(np.linalg.norm(D-F,2)),FD304_vs_D0_F=float(np.linalg.norm(D-F,'fro')),FD304_vs_lifted_FD152_op=float(np.linalg.norm(F-C@F0@C.conj().T,2)),fixed_linear_H_free_energy_change_Ry=free_delta,NOT_nonlinear_HSE_free_energy_change=True,D0_full_commutator_F_Ry=comm(D),FD304_full_commutator_F_Ry=comm(F),FD304_weighted_eigen_residual_F_Ry=float(np.linalg.norm(fullres*w,'fro')),FD304_Fermi_143_146_eigen_residuals_Ry=np.linalg.norm(fullres[:,142:146],axis=0).tolist(),FD304_all_Ritz_residuals_Ry=np.linalg.norm(fullres,axis=0).tolist(),FD304_occupation_above176_e=float(w[176:].sum()),FD304_occupation_above146_e=float(w[146:].sum()),FD304_holes_below143_e=float(sum(1-w[:142])),FD304_Td_density_defects_F=cubic,FD304_Theta_density_defect_F=tr,offspace_R_F_Ry=RF,offspace_R_op_Ry=Rop,gap_free_full_vs_block_diagonal_FD_HS_upper=unit_FD_error_bound,bound_noninformative=unit_FD_error_bound>1,missing_independent_complement_lower_bound_Ry=required_L,complement_bound_target_charge_e=1e-8,complement_bound_is_CONDITIONAL=True,chemical_potential_frozen_for_complement_bound=True,actual_energy_clusters=groups,fullspace_FD_stationary=False,nonlinear_HSE_converged=False,physical_xc=None)
    assert max(cubic+[tr])<1e-8
    (HERE/'galerkin_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    np.savez(PRIVATE/'FD304_diagnostics.npz',e=e,U=U,occupations=w,FD=F,fullres=fullres)
    print(json.dumps({k:result[k] for k in ['dimensions','mu304_Ry','FD304_vs_D0_op','FD304_full_commutator_F_Ry','FD304_Fermi_143_146_eigen_residuals_Ry','FD304_occupation_above176_e','gap_free_full_vs_block_diagonal_FD_HS_upper','missing_independent_complement_lower_bound_Ry']}))
if __name__=='__main__':main()
