"""Joint-symmetry space purification; explicitly not a density-preserving repair."""
import hashlib,json,sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'antiunitary_closure_2026-10-15'))
sys.path.insert(0,str(BASE/'native_matched_pilot_2026-10-11'))
from audit_native import gather,orthonormal,ROOT
from packets import packet
from reference_irrep_check import td_operations


def main():
    private=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/jg_20261015')
    if private.exists():raise FileExistsError('preserve new joint-space evidence')
    phi,_,theta,_,wg=gather(1)
    assert np.flatnonzero(wg>1e-8).tolist()==list(range(146))
    records=[packet(ROOT,'before',r,1) for r in [0,1]]
    G=np.array(sorted(tuple(g) for b in records for g in b['G']));N=len(G)
    lookup={tuple(g):i for i,g in enumerate(G)}
    P=np.empty((2*N,6),complex)
    for rank,b in enumerate(records):
        n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        P[glob]=packet(ROOT,'after',rank,1)['probe'][ix]
    operations=td_operations()
    indices=[np.array([lookup[tuple(g)] for g in G@v['spatial'].T]) for v in operations]
    def rotate(S,i):
        out=np.empty_like(S).reshape(2,N,S.shape[1])
        out[:,indices[i],:]=np.einsum('st,tgn->sgn',operations[i]['spin'],S.reshape(2,N,S.shape[1]))
        return out.reshape(S.shape)
    phases=[np.tile((-1.)**((G[:,i]+G[:,j])%2),2) for i,j in [(0,1),(0,2),(1,2)]]
    def apply_twirled_projector(S,images):
        out=np.zeros_like(S)
        for T in images:out+=T@(T.conj().T@S)
        return np.linalg.qr(out,mode='reduced')[0]
    def purify(S):
        S=orthonormal(S)[0]
        S=apply_twirled_projector(S,[S,theta(S)])
        S=apply_twirled_projector(S,[S]+[p[:,None]*S for p in phases])
        # Generator spin-lift signs cancel in a projector twirl.
        out=np.zeros_like(S)
        for i in range(24):
            T=rotate(S,i);out+=T@(T.conj().T@S)
        return np.linalg.qr(out,mode='reduced')[0]
    def audit(S):
        residual=lambda T:float(np.linalg.norm(T-S@(S.conj().T@T),'fro'))
        td=[residual(rotate(S,i)) for i in range(24)]
        return dict(dimension=S.shape[1],Gram_error_F=float(np.linalg.norm(S.conj().T@S-np.eye(S.shape[1]),'fro')),
            all24_Td_leakage_F=td,max_Td_leakage_F=max(td),Theta_leakage_F=residual(theta(S)),
            primitive_translation_leakage_F=[residual(p[:,None]*S) for p in phases])
    occ=purify(phi[:,:146]);ref=np.column_stack((purify(P[:,:2]),purify(P[:,2:])))
    U,s,_=np.linalg.svd(np.column_stack((occ,ref)),full_matrices=False)
    assert min(s)>1e-7 and len(s)==152
    union=purify(U)
    rows={k:audit(S) for k,S in [('occupied146',occ),('reference2',ref[:,:2]),('reference4',ref[:,2:]),('joint152',union)]}
    for k,v in rows.items():
        assert max(v['Gram_error_F'],v['max_Td_leakage_F'],v['Theta_leakage_F'],*v['primitive_translation_leakage_F'])<1e-10,k
    source_distance=float(np.linalg.norm(phi[:,:146]-union@(union.conj().T@phi[:,:146]),2))
    reference_distance=float(np.linalg.norm(P-union@(union.conj().T@P),2))
    private.mkdir(mode=0o700)
    f=private/'joint_basis.npz';np.savez(f,Q=union,occupied=occ,reference=ref,G=G)
    result=dict(status='CALCULATED explicitly NEW purified spaces; no native/state qualification',
        parent='60894e0',rows=rows,original_occupied_source_coverage_op=source_distance,
        original_reference_coverage_op=reference_distance,union_smallest_singular_value=float(min(s)),
        original_native_occupations_changed=False,does_not_preserve_original_source_subspace=True,
        old_coverage_gates_not_reclassified=True,density_is_not_native_FD_solution=True,
        direct_Fock_on_new_space_missing=True,source_resolved_Hamiltonian_residual_missing=True,
        HSE_native_release=False,physical_xc=None,basis=str(f),basis_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'space_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2),flush=True)
    print(json.dumps(rows,indent=2),flush=True)


if __name__=='__main__':main()
