"""Read-only native source/basis/FD ensemble audit; no SCF or native execution."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy.special import xlogy

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'antiunitary_closure_2026-10-15'))
sys.path.insert(0,str(BASE/'native_matched_pilot_2026-10-11'))
from audit_native import gather,orthonormal,ROOT
from packets import packet
from reference_irrep_check import td_operations


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if (HERE/'native_basis_result.json').exists():raise FileExistsError('preserve original audit')
    prior=json.loads((BASE/'joint_symmetry_2026-10-15/space_result.json').read_text());path=Path(prior['basis']);assert sha(path)==prior['basis_sha256']
    f=np.load(path);Q=f['Q'];G=f['G'];N=len(G);phi,direct,theta,et,w=gather(1);U,ge=orthonormal(phi)
    records=[packet(ROOT,'before',i,1) for i in [0,1]]
    GG=np.array(sorted(tuple(g) for p in records for g in p['G']));np.testing.assert_array_equal(G,GG)
    B=records[0]['B'];Bexpected=np.eye(3)*(2*np.pi/(6.46/0.529177210903))
    # Conventional8atom cube, native absolute reciprocal vectors in2pi/bohr.
    assert np.max(abs(B-Bexpected))<1e-8 and max(abs(records[0]['k']))<1e-12
    kinetic=np.tile(np.sum((G@B.T)**2,axis=1),2);assert 49<max(kinetic)<=50
    R=Q-U@(U.conj().T@Q);L,s,Vh=np.linalg.svd(R,full_matrices=False)
    rank={str(t):int(sum(s>t)) for t in [1e-3,1e-6,1e-8,1e-10]};assert rank['0.001']==rank['1e-06']==6
    A=Q@Vh[:6].conj().T;outside=L[:,:6]
    KT=(A.conj().T*kinetic)@A;Kout=(outside.conj().T*kinetic)@outside
    summation=np.array([sum(kinetic*abs(A[:,i])**2) for i in range(6)])
    assert max(abs(np.diag(KT).real-summation))<1e-10
    coeff=Q.conj().T@phi;D=(coeff*w)@coeff.conj().T;D=(D+D.conj().T)/2
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);ops=td_operations()
    def rotate(S,op):
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);out=np.empty_like(S).reshape(2,N,S.shape[1]);out[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],S.reshape(2,N,S.shape[1]));return out.reshape(S.shape)
    transforms=[Q.conj().T@rotate(Q,op) for op in ops]
    J=Q.conj().T@theta(Q)
    phases=[np.tile((-1.)**((G[:,i]+G[:,j])%2),2) for i,j in [(0,1),(0,2),(1,2)]]
    translations=[np.eye(152)]+[Q.conj().T@(p[:,None]*Q) for p in phases]
    Dtr=sum(T@D@T.conj().T for T in translations)/4
    Dcr=sum(T@Dtr@T.conj().T for T in transforms)/24
    Dt=(Dcr+J@Dcr.conj()@J.conj().T)/2;Dt=(Dt+Dt.conj().T)/2
    eig=np.linalg.eigvalsh(Dt);assert min(eig)>-1e-12 and max(eig)<1+1e-12
    assert abs(np.trace(Dt).real-144)<1e-8
    entropy=lambda ev:float(-sum(xlogy(np.clip(ev,0,1),np.clip(ev,0,1))+xlogy(1-np.clip(ev,0,1),1-np.clip(ev,0,1))))
    allcov=[float(np.linalg.norm(T@Dt@T.conj().T-Dt,2)) for T in transforms+translations]+[float(np.linalg.norm(J@Dt.conj()@J.conj().T-Dt,2))]
    densityR=phi*np.sqrt(w)-Q@(coeff*np.sqrt(w));tail=float(np.linalg.norm(densityR,2));bound=2*float(np.linalg.norm(phi*np.sqrt(w),2))*tail
    de=np.linalg.eigvalsh(Dt-D)
    result=dict(status='CALCULATED retained native source and explicitly NEW constrained ensemble only',joint_basis=str(path),residual_singular_values=s.tolist(),residual_ranks=rank,source_Gram_error=ge,auxiliary_kinetic_Ritz_Ry=np.linalg.eigvalsh(KT).tolist(),complement_kinetic_Ritz_Ry=np.linalg.eigvalsh(Kout).tolist(),auxiliary_high_G_above40Ry_probability=np.sum(abs(A[kinetic>40])**2,axis=0).tolist(),auxiliary_old_occupied_weight=np.sum(abs(phi[:,:146].conj().T@A)**2*w[:146,None],axis=0).tolist(),auxiliary_reference_weight=np.sum(abs(f['reference'].conj().T@A)**2,axis=0).tolist(),all152_kinetic_extrema_Ry=np.linalg.eigvalsh((Q.conj().T*kinetic)@Q)[[0,-1]].tolist(),occupied146_kinetic_extrema_Ry=np.linalg.eigvalsh((f['occupied'].conj().T*kinetic)@f['occupied'])[[0,-1]].tolist(),old_native_charge=float(sum(w)),projected_charge=float(np.trace(D).real),new_twirl_charge=float(np.trace(Dt).real),new_twirl_natural_occupations=eig.tolist(),old_entropy_kB=entropy(w),projected_entropy_kB=entropy(np.linalg.eigvalsh(D)),new_twirl_entropy_kB=entropy(eig),new_twirl_max_all_symmetry_covariance_op=max(allcov),reduced_density_change_op=float(max(abs(de))),reduced_density_change_trace_norm=float(sum(abs(de))),original_density_outside_joint_op_upper=bound,charge_projection_loss_e=float(sum(w)-np.trace(D).real),native_full_Hamiltonian_exported=False,native_HSE_FD_qualified=False,new_native_jobs=0,physical_xc=None,raw_sha256={str(p):sha(p) for p in [path,*[ROOT/'pilot'/f'c1_before.rank{i}' for i in [0,1]],BASE/'joint_symmetry_2026-10-15/space_result.json',Path(__file__),HERE/'preregistration.md']})
    np.savez(HERE/'reduced_matrices.npz',old_projected_D=D,new_constrained_D=Dt,kinetic_auxiliary=KT,source_complement_singular=s)
    (HERE/'native_basis_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['raw_sha256','new_twirl_natural_occupations','residual_singular_values']},indent=2))


if __name__=='__main__':main()
