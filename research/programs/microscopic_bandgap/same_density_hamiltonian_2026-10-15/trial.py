"""Construct an explicit positive symmetric trial; never a solved FD state."""
from pathlib import Path
import json,hashlib,sys
import numpy as np

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
DFT=Path('/home/User/opencode_workspace/DFT');PRIVATE=DFT/'.local/qe75_lowram_20261011/h8h_20261015'
sys.path.insert(0,str(BASE/'antiunitary_closure_2026-10-15'))
sys.path.insert(0,str(BASE/'native_matched_pilot_2026-10-11'))
from audit_native import gather,ROOT
from packets import packet
from reference_irrep_check import td_operations


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if (PRIVATE/'trial.npz').exists():raise FileExistsError('preserve trial')
    prior=json.loads((BASE/'joint_symmetry_2026-10-15/space_result.json').read_text());assert sha(prior['basis'])==prior['basis_sha256'];f=np.load(prior['basis']);Q=f['Q'];G=f['G'];N=len(G)
    D=np.load(BASE/'fd_bridge_resolution_2026-10-15/reduced_matrices.npz')['new_constrained_D'];v,V=np.linalg.eigh(D);hi=v>.75;mid=(v>.25)&(v<.75);assert sum(hi)==142 and sum(mid)==4 and sum(v<.25)==6
    source=Q@np.column_stack((V[:,hi],V[:,mid]));weights=np.r_[np.ones(142),np.full(4,.5),np.zeros(30)]
    native=np.column_stack((source,np.zeros((2*N,30),complex)));_,_,theta,_,_=gather(1)
    lookup={tuple(g):i for i,g in enumerate(G)};P=np.empty((2*N,6),complex)
    for rank in [0,1]:
        b=packet(ROOT,'before',rank,1);n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)];loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc];P[glob]=packet(ROOT,'after',rank,1)['probe'][ix]
    trial=np.column_stack((Q,P,theta(P)));small=Q.conj().T@source;Dr=(small*weights[:146])@small.conj().T
    def density_error(image):
        a=Q.conj().T@image;return float(np.linalg.norm((a*weights[:146])@a.conj().T-Dr,2))
    errors=[]
    for op in td_operations():
        dest=np.array([lookup[tuple(g)] for g in G@op['spatial'].T]);image=np.empty_like(source).reshape(2,N,146);image[:,dest,:]=np.einsum('st,tgn->sgn',op['spin'],source.reshape(2,N,146));errors.append(density_error(image.reshape(source.shape)))
    errors.append(density_error(theta(source)))
    for i,j in [(0,1),(0,2),(1,2)]:errors.append(density_error(np.tile((-1.)**((G[:,i]+G[:,j])%2),2)[:,None]*source))
    gram=float(np.linalg.norm(source.conj().T@source-np.eye(146),2));charge=float(np.dot(weights[:146],np.sum(abs(source)**2,axis=0)));assert max(errors)<1e-8 and gram<1e-10 and abs(charge-144)<1e-8
    PRIVATE.mkdir(mode=0o700,exist_ok=True);out=PRIVATE/'trial.npz';np.savez(out,G=G,source=native,weights=weights,trial=trial,Q=Q,D_Q=Dr,P=P)
    report=dict(status='PASS explicit positive symmetric trial only',charge_e=charge,entropy_kB=float(4*np.log(2)),sigma_Ry=.001,source_Gram_op=gram,max_density_group_covariance_op=max(errors),all24_density_Td_errors=errors[:24],natural_occupied_count=146,source_storage_capacity=176,joint_auxiliary_count=152,independent_trials=12,total_trials=164,no_FD_HSE_state_claim=True,no_original_source_preservation_claim=True,source_natural_weights=weights.tolist(),prior_D_spectral_gap_to_threshold=float(min(abs(v-.25).min(),abs(v-.75).min())),trial_path=str(out),trial_sha256=sha(out),source_sha256={str(p):sha(p) for p in [Path(__file__),HERE/'preregistration.md',Path(prior['basis']),BASE/'fd_bridge_resolution_2026-10-15/reduced_matrices.npz']})
    (HERE/'trial_result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['source_natural_weights','all24_density_Td_errors','source_sha256']},indent=2))


if __name__=='__main__':main()
