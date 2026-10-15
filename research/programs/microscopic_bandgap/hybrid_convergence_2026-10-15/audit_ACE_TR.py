"""Actual first-source ACE time-reversal commutator, no exchange re-execution."""
import json
from pathlib import Path
import numpy as np
from packets import packet
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main():
    root=r.PAIR/'host';assert json.loads((root/'FINAL.json').read_text())['accepted']
    Gs=np.concatenate([packet(root,'before',rank,1)['G'] for rank in [0,1]])
    G=np.array(sorted(map(tuple,Gs)));ng=len(G);assert ng==10827
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G])
    phi=np.empty((2*ng,176),complex);xi=phi.copy();ace=phi.copy()
    for rank in [0,1]:
        b=packet(root,'before',rank,1);a=packet(root,'after',rank,1)
        n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
        target=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[target,ng+target]
        phi[glob]=b['phi'][ix];xi[glob]=a['xi'][ix];ace[glob]=a['ace'][ix]
    theta=lambda x:np.r_[x[ng+minus].conj(),-x[minus].conj()]
    Tphi=theta(phi);cross=phi.conj().T@Tphi;gram=phi.conj().T@phi
    assert np.linalg.norm(gram-np.eye(176),2)<1e-8
    leak=np.eye(176)-cross.conj().T@cross
    assert min(np.linalg.eigvalsh((leak+leak.conj().T)/2))>-1e-8
    # This is an ACE/ACE antiunitary commutator, not a direct/ACE off-span test.
    commutator=-xi@(xi.conj().T@Tphi)-theta(ace)
    source_error=-xi@(xi.conj().T@phi)-ace
    result=dict(status='CALCULATED actual first-source ACE operator and full176-column symmetry',
        source_Gram_error_op=float(np.linalg.norm(gram-np.eye(176),2)),
        source_span_TR_leakage_squared_op=float(np.linalg.norm(leak,2)),
        source_span_TR_cross_singular_values=np.linalg.svd(cross,compute_uv=False).tolist(),
        ACE_source_action_reconstruction_relative=float(np.linalg.norm(source_error)/max(1.,np.linalg.norm(ace))),
        ACE_TR_commutator_on_source_relative=float(np.linalg.norm(commutator)/max(1.,np.linalg.norm(ace))),
        ACE_TR_commutator_on_source_max_column_Ry=float(max(np.linalg.norm(commutator,axis=0))),
        ACE_TR_commutator_on_bands143_146_Ry=[float(v) for v in np.linalg.norm(commutator[:,142:146],axis=0)],
        direct_TR_action_on_Theta_source_not_measured=True,
        not_an_offspan_direct_ACE_equivalence_claim=True,physical_xc=None,new_native_invocations=0)
    assert result['ACE_source_action_reconstruction_relative']<1e-8
    (HERE/'first_ACE_TR_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_span_TR_cross_singular_values'},indent=2))

if __name__=='__main__':main()
