"""New-query self-block and cross-query diagnostic; NEVER constructs a304splice."""
from pathlib import Path
import json
import numpy as np
from accepted import HERE,PRIVATE,OLD,frames,decode,global_indices,old_action,td_operations,sha


def main():
    target=HERE/'query_only_result.json'
    if target.exists():raise FileExistsError('retain first raw-action audit')
    refused=json.loads((HERE/'strict_refusal.json').read_text());assert refused['no_splice_performed']
    f,b,G,Q,L,V=frames();HR=np.zeros_like(L);kin=np.zeros_like(L)
    for rank in [0,1]:
        a=decode(PRIVATE/'p2/host/pilot'/f'H.rank{rank}');i,j=global_indices(a,G);HR[j]=sum(a[k][i,:152] for k in ['kin','loc','nl','fock']);kin[j]=a['kin'][i,:152]
    Hnew=L.conj().T@HR;scale=max(1.,float(np.linalg.norm(Hnew,2)));herm=float(np.linalg.norm(Hnew-Hnew.conj().T,'fro')/scale);assert herm<1e-8
    HQold=old_action(G);cross=Q.conj().T@HR-(L.conj().T@HQold).conj().T;crossop=float(np.linalg.norm(cross,2));crossF=float(np.linalg.norm(cross,'fro'))
    N=len(G);lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);theta=lambda A:np.r_[A[N+minus].conj(),-A[minus].conj()]
    def rotate(A,op):
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);out=np.empty_like(A).reshape(2,N,A.shape[1]);out[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],A.reshape(2,N,A.shape[1]));return out.reshape(A.shape)
    cov=[]
    for op in td_operations():
        U=L.conj().T@rotate(L,op);cov.append(float(np.linalg.norm(U.conj().T@Hnew@U-Hnew,'fro')/scale))
    U=L.conj().T@theta(L);tr=float(np.linalg.norm(U.conj().T@Hnew@U-Hnew.conj(),'fro')/scale)
    e=np.linalg.eigvalsh((Hnew+Hnew.conj().T)/2);T=L.conj().T@kin;te=np.linalg.eigvalsh((T+T.conj().T)/2)
    out=dict(status='CALCULATED new152query self-block only; strict304splice remains REFUSED',new_query_H_RR_Hermiticity_relative=herm,new_query_all24_projected_Td_relative=cov,new_query_projected_Theta_relative=tr,new_query_H_RR_min_max_Ry=[float(e[0]),float(e[-1])],new_query_kinetic_RR_min_max_Ry=[float(te[0]),float(te[-1])],cross_DIFFERENT_native_operator_reciprocity_norm_Ry=crossop,cross_DIFFERENT_native_operator_reciprocity_F_Ry=crossF,small_cross_defect_NOT_operator_identity_certificate=True,no304matrix_constructed=True,no_FD_or_HSE_convergence_or_xc=True,auxiliary_directions_NOT_solved_bands=True,source_sha256={str(p):sha(p) for p in [Path(__file__),HERE/'strict_refusal.json',PRIVATE/'full_action_basis.npz',*list((PRIVATE/'p2/host/pilot').iterdir())]})
    np.savez(HERE/'query_only_matrices.npz',H_new_RR=Hnew,kinetic_RR=T,cross_DIFFERENT_operator_defect=cross)
    target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['new_query_all24_projected_Td_relative','source_sha256']},indent=2))


if __name__=='__main__':main()
