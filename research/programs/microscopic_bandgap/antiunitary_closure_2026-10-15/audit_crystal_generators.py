"""Independent retained-data Td generator check: TR alone cannot certify Gamma8."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.linalg import svd
from audit_native import gather, orthonormal, ROOT, sha

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'native_matched_pilot_2026-10-11'))
from reference_irrep_check import td_operations
sys.path.insert(0,str(HERE.parent/'symmetry_constructor_2026-10-15'))
from compare import input_record


def main():
    # Explicit independent group generation, not an assumption that two named
    # operations suffice. Overall spin-lift signs do not change subspaces.
    C3=np.array([[0,0,1],[1,0,0],[0,1,0]])
    S4=np.array([[0,-1,0],[1,0,0],[0,0,-1]])
    group={tuple(np.eye(3,dtype=int).ravel())}
    while True:
        expanded=group|{tuple((np.array(g).reshape(3,3)@a).ravel()) for g in group for a in [C3,S4]}
        if expanded==group:break
        group=expanded
    assert len(group)==24
    phi,_,_,_,_=gather(1);U,_=orthonormal(phi)
    records=[input_record(ROOT.parents[2]/'h8s_20261015/p1/host',r) for r in [0,1]]
    G=np.array(sorted(tuple(g) for b in records for g in b['G']));N=len(G)
    lookup={tuple(g):i for i,g in enumerate(G)}
    Q=np.empty((2*N,364),complex)
    for b in records:
        p,n=map(int,b['h'][3:5]);ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        Q[glob]=b['trial'][ix,:364]
    out=[]
    for name,spatial in [('C3',C3),('S4',S4)]:
        op=next(v for v in td_operations() if np.array_equal(v['spatial'],spatial))
        idx=np.array([lookup[tuple(g)] for g in G@spatial.T])
        for basis_name,S in [('native176',U),('paired364_with_reference',Q)]:
            T=np.empty_like(S).reshape(2,N,S.shape[1])
            T[:,idx,:]=np.einsum('st,tgn->sgn',op['spin'],S.reshape(2,N,S.shape[1]))
            T=T.reshape(S.shape)
            R=T-S@(S.conj().T@T)
            ss=svd(R,compute_uv=False,lapack_driver='gesvd')
            out.append(dict(generator=name,spatial=spatial.tolist(),basis=basis_name,
                leakage_op=float(max(ss)),ranks={str(t):int(sum(ss>t)) for t in [1e-3,1e-5,1e-8]},
                singular_values=ss.tolist()))
            print(name,basis_name,float(max(ss)),int(sum(ss>1e-8)),flush=True)
    result=dict(status='CALCULATED actual complex generator leakage, no new native run',
        group_order=24, generators_generate_full_spatial_Td=True,rows=out,
        TR_completion_not_point_group_completion=True,
        native_job_was_not_assumed_to_qualify_Gamma8_quartet=True,
        physical_xc=None,code_sha256=sha(Path(__file__)))
    (HERE/'crystal_generator_audit.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
