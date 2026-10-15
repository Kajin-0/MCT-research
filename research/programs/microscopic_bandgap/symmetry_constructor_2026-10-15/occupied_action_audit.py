"""Physical source/reference action and crystal tests of new occupied compression."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import solve_triangular,svd
from compare import input_record,output_record,relative

HERE=Path(__file__).resolve().parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8s_20261015/p1/host')
sys.path.insert(0,str(HERE.parent/'native_matched_pilot_2026-10-11'))
from reference_irrep_check import td_operations


def main():
    records=[input_record(ROOT,r) for r in [0,1]]
    G=np.array(sorted(tuple(g) for b in records for g in b['G']));N=len(G)
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G])
    Q=np.empty((2*N,364),complex);WQ=np.empty_like(Q);P=np.empty((2*N,6),complex);VP=np.empty_like(P)
    for rank,b in enumerate(records):
        n,p=int(b['h'][4]),int(b['h'][3]);ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        Q[glob]=b['trial'][ix,:364];P[glob]=b['trial'][ix,364:370]
        Y=[output_record(ROOT,rank,s)['action'][ix] for s in [1,2]]
        WQ[glob]=-(Y[0][:,:364]+Y[1][:,:364])/2
        VP[glob]=(Y[0][:,364:370]+Y[1][:,364:370])/2
    del records,Y
    C=np.load(HERE/'occupied_reduction_matrices.npz')['occupied_basis_in_Q']
    F=Q@C;W=WQ@C;H=F.conj().T@W
    L=np.linalg.cholesky((H+H.conj().T)/2)
    Xi=solve_triangular(L,W.conj().T,lower=True).conj().T
    A=lambda X:Xi@(Xi.conj().T@X)
    theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    rows=[]
    generators=[('C3',np.array([[0,0,1],[1,0,0],[0,1,0]])),('S4',np.array([[0,-1,0],[1,0,0],[0,0,-1]]))]
    for name,M in generators:
        spin=next(op['spin'] for op in td_operations() if np.array_equal(op['spatial'],M))
        idx=np.array([lookup[tuple(g)] for g in G@M.T])
        def transform(S):
            T=np.empty_like(S).reshape(2,N,S.shape[1]);T[:,idx,:]=np.einsum('st,tgn->sgn',spin,S.reshape(2,N,S.shape[1]));return T.reshape(S.shape)
        TF=transform(F)
        residual=svd(TF-F@(F.conj().T@TF),compute_uv=False)
        rows.append(dict(generator=name,occupied_support_leakage_op=float(max(residual)),
            occupied_ACE_self_commutator_relative=relative(A(TF),transform(W)),
            not_direct_Fock_crystal_covariance_measurement=True))
    result=dict(status='CALCULATED post-acquisition physical occupied-compression diagnostic',
        physical_occupied_source_action_relative=relative(A(F),W),
        physical_occupied_TR_commutator_relative=relative(A(theta(F)),theta(W)),
        fixed_reference_ACE_direct_action_relative=relative(-A(P),VP),
        fixed_reference_ACE_direct_action_op_Ry=float(np.linalg.norm(-A(P)-VP,2)),
        fixed_reference_cover_by_occupied_support_op=float(np.linalg.norm(P-F@(F.conj().T@P),2)),
        crystal_generators=rows,original_reference_not_changed=True,native_ACE_not_integrated=True,
        no_replacement_of364constructor_acceptance=True,physical_xc=None,HSE_converged=False)
    (HERE/'occupied_action_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
