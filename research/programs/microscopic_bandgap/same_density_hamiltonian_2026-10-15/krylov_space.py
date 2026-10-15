"""Minimal one-step H-action completion using actual native vectors only."""
from pathlib import Path
import json,hashlib
import numpy as np
from readback import decode,td_operations
HERE=Path(__file__).resolve().parent;DFT=Path('/home/User/opencode_workspace/DFT');ROOT=DFT/'.local/qe75_lowram_20261011/h8h_20261015'


def main():
    if (HERE/'krylov_result.json').exists():raise FileExistsError('preserve measured completion')
    old=json.loads((HERE/'native_result.json').read_text());assert old['accepted'];f=np.load(ROOT/'trial.npz');Q=f['Q'];G=f['G'];N=len(G);lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);theta=lambda a:np.r_[a[N+minus].conj(),-a[minus].conj()]
    HQ=np.zeros_like(Q)
    for rank in [0,1]:
        b=decode(ROOT/'p1/host/pilot'/f'H.rank{rank}');p,n=map(int,b['h'][4:6]);active=np.r_[np.arange(n),np.arange(p,p+n)];i=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[i,N+i];HQ[glob]=sum(b[k][active,:152] for k in ['kin','loc','nl','fock'])
    Hq=Q.conj().T@HQ;R=HQ-Q@Hq;L,s,_=np.linalg.svd(R,full_matrices=False);rank=int(sum(s>1e-8));assert rank==152
    V=np.linalg.qr(np.column_stack((Q,L[:,:rank])),mode='reduced')[0]
    def rotate(A,op):
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);out=np.empty_like(A).reshape(2,N,A.shape[1]);out[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],A.reshape(2,N,A.shape[1]));return out.reshape(A.shape)
    residual=lambda A:float(np.linalg.norm(A-V@(V.conj().T@A),'fro'))
    cov=[residual(rotate(V,op)) for op in td_operations()]+[residual(theta(V))]
    for i,j in [(0,1),(0,2),(1,2)]:cov.append(residual(np.tile((-1.)**((G[:,i]+G[:,j])%2),2)[:,None]*V))
    assert max(cov)<1e-8
    e,U=np.linalg.eigh((Hq+Hq.conj().T)/2);partial=np.argsort(abs(e-old['science']['projected_FD_mu_Ry']))[:4];Vocc=np.load(ROOT/'occupied_residual_basis.npz')['Q']
    Rocc=HQ-Vocc@(Vocc.conj().T@HQ);Rfull=HQ-V@(V.conj().T@HQ);before=np.linalg.norm(R@U[:,partial],axis=0);afterocc=np.linalg.norm(Rocc@U[:,partial],axis=0);after=np.linalg.norm(Rfull@U[:,partial],axis=0)
    path=ROOT/'full_action_basis.npz';np.savez(path,Q=V,new_queries=L[:,:rank],G=G)
    result=dict(status='CALCULATED minimal one-step action completion; not FD/selfconsistent solution',dimension=V.shape[1],additional_action_directions=rank,residual_singular_values_Ry=s.tolist(),smallest_residual_singular_Ry=float(s[-1]),maximum_all_group_Theta_translation_leakage_F=max(cov),full_HQ_outside_new_space_F_Ry=float(np.linalg.norm(Rfull,'fro')),partial_Ritz_indices_1based=(partial+1).tolist(),old_Ritz_Gamma8_like_residuals_Ry=before.tolist(),after_occupied_only_completion_Ry=afterocc.tolist(),after_full_action_completion_Ry=after.tolist(),actual_Ritz_eigenvectors_unchanged=True,new_304_Hamiltonian_lower_right_block_UNKNOWN=True,not_native_solved_bands=True,next_minimum_independent_native_action_columns=rank,new_query_forecast_same_D_using_measured170action185s=True,one_additional_query_needs_NEW_frozen_profile_and_complete_same_D_controls=True,new_native_jobs=0,basis_path=str(path),basis_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),physical_xc=None,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'native_result.json',ROOT/'trial.npz',ROOT/'occupied_residual_basis.npz']})
    (HERE/'krylov_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','residual_singular_values_Ry']},indent=2))


if __name__=='__main__':main()
