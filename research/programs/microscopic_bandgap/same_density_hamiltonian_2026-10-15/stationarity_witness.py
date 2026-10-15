"""Read-only full-space commutator witness and occupied residual completion."""
from pathlib import Path
import json,hashlib
import numpy as np
from readback import decode,td_operations
HERE=Path(__file__).resolve().parent;DFT=Path('/home/User/opencode_workspace/DFT');ROOT=DFT/'.local/qe75_lowram_20261011/h8h_20261015'


def main():
    if (HERE/'stationarity_result.json').exists():raise FileExistsError('retain first witness')
    result=json.loads((HERE/'native_result.json').read_text());assert result['accepted']
    f=np.load(ROOT/'trial.npz');Q=f['Q'];S=f['source'][:,:146];w=f['weights'][:146];G=f['G'];N=len(G);lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    HQ=np.zeros_like(Q)
    for rank in [0,1]:
        b=decode(ROOT/'p1/host/pilot'/f'H.rank{rank}');p,n=map(int,b['h'][4:6]);ix=np.r_[np.arange(n),np.arange(p,p+n)];loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc];HQ[glob]=sum(b[k][ix,:152] for k in ['kin','loc','nl','fock'])
    d=(Q.conj().T@S*w)@(S.conj().T@Q);d=(d+d.conj().T)/2;Hq=Q.conj().T@HQ;R=HQ-Q@Hq;HD=HQ@d
    # No sqrt(1-s^2), no inversion of a near-singular Gram matrix.
    X=np.column_stack((HD,Q));U,T=np.linalg.qr(X,mode='reduced');J=np.block([[np.zeros((152,152)),np.eye(152)],[-np.eye(152),np.zeros((152,152))]])
    C=T@J@T.conj().T;Ce=np.linalg.eigvalsh((1j*C+(1j*C).conj().T)/2);commop=float(max(abs(Ce)));commF=float(np.linalg.norm(C,'fro'))
    old=result['science'];assert abs(commF-old['fullspace_commutator_F_Ry'])<1e-9
    M=old['H_operator_norm_upper_Ry'];u=2.**-53;gamma=lambda n:n*u/(1-n*u)
    E=X-U@T;eH=float(np.linalg.norm(E[:,:152],'fro'));eQ=float(np.linalg.norm(E[:,152:],'fro'));a=float(np.linalg.norm(HD,'fro'));bq=float(np.linalg.norm(Q,'fro'))
    outside=S-Q@(Q.conj().T@S);d_allow=2*float(np.linalg.norm(outside,'fro'))*float(np.linalg.norm(S,'fro'))
    arithmetic=16*gamma(32*2*N)*a*bq+2*(eH*bq+a*eQ+eH*eQ)+2*M*d_allow
    lower=max(0.,commop-arithmetic)/(2*M)
    B=R@d;left,s,vh=np.linalg.svd(B,full_matrices=False);thresholds=[1e-3,1e-4,1e-5,1e-6,1e-7,1e-8];ranks={str(t):int(sum(s>t)) for t in thresholds};r=ranks['1e-08']
    V=np.linalg.qr(np.column_stack((Q,left[:,:r])),mode='reduced')[0]
    def rotate(A,op):
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);out=np.empty_like(A).reshape(2,N,A.shape[1]);out[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],A.reshape(2,N,A.shape[1]));return out.reshape(A.shape)
    covariance=[]
    for op in td_operations():
        A=rotate(V,op);covariance.append(float(np.linalg.norm(A-V@(V.conj().T@A),'fro')))
    A=theta(V);covariance.append(float(np.linalg.norm(A-V@(V.conj().T@A),'fro')))
    for i,j in [(0,1),(0,2),(1,2)]:
        A=np.tile((-1.)**((G[:,i]+G[:,j])%2),2)[:,None]*V;covariance.append(float(np.linalg.norm(A-V@(V.conj().T@A),'fro')))
    remaining=float(np.linalg.norm(B-V@(V.conj().T@B),2));smax=max(covariance)
    path=ROOT/'occupied_residual_basis.npz';np.savez(path,Q=V,G=G)
    out=dict(status='CALCULATED complete same-D commutator witness and NEW residual-space audit',fullspace_commutator_op_Ry=commop,fullspace_commutator_F_Ry=commF,finite_model_roundoff_allowance_Ry=arithmetic,whole_space_FD_density_error_lower_op=lower,universal_whole_space_density_error_upper_op=1.,bound_is_conditional_on_captured_finite_operator_and_roundoff_model=True,excludes_1e8_operator_density_stationarity=lower>1e-8,occupied_residual_singular_values_Ry=s.tolist(),residual_ranks_by_Ry_threshold=ranks,next_space_dimension=V.shape[1],remaining_HD_offspace_operator_Ry=remaining,max_all24_Theta_translation_new_space_leakage_F=smax,new_space_passes_UNCHANGED_1e8_symmetry_gate=smax<=1e-8,basis_path=str(path),basis_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),old_space_or_FD_failure_not_reclassified=True,does_not_contain_unknown_H_on_new_directions=True,new_native_jobs=0,physical_xc=None,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'native_result.json',ROOT/'trial.npz',*[(ROOT/'p1/host/pilot'/f'H.rank{i}') for i in [0,1]]]})
    (HERE/'stationarity_result.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['source_sha256','occupied_residual_singular_values_Ry']},indent=2))


if __name__=='__main__':main()
