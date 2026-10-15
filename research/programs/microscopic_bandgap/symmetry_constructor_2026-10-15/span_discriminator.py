"""Post-preregistration diagnostic: old ACE vs actual new direct off-span action.

This does not change native acceptance, source, weights, or any old verdict.
The measured operator-norm/cover bound controls reconstruction on ThetaPhi.
"""
import json
from pathlib import Path
import numpy as np
from compare import input_record,output_record,packet,relative

HERE=Path(__file__).resolve().parent
ROOT=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8s_20261015/p1/host')
OLD=ROOT.parents[2]/'h8c_20261015/p1/host'


def main():
    final=json.loads((ROOT/'FINAL.json').read_text());assert final['accepted']
    ins=[input_record(ROOT,r) for r in [0,1]]
    G=np.array(sorted(tuple(g) for b in ins for g in b['G']));N=len(G)
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G])
    Q=np.empty((2*N,364),complex);Phi=np.empty((2*N,176),complex);Xi=np.empty_like(Phi);VQ=np.empty_like(Q)
    for rank,b in enumerate(ins):
        n,p=int(b['h'][4]),int(b['h'][3]);ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        Q[glob]=b['trial'][ix,:364];Phi[glob]=b['phi'][ix]
        Xi[glob]=packet(OLD,'after',rank,1)['xi'][ix]
        VQ[glob]=output_record(ROOT,rank,1)['action'][ix,:364]
    theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    TPhi=theta(Phi);direct=VQ@(Q.conj().T@TPhi)
    previous=-Xi@(Xi.conj().T@TPhi);err=previous-direct
    wg=ins[0]['wg'];norms=np.linalg.norm(err,axis=0)
    result=dict(status='CALCULATED post-preregistration diagnostic, not a changed acceptance gate',
        same_original_D_operator=True,direct_ThetaPhi_action_reconstruction_upper_Ry=final['science']['source_projection_action_upper_Ry'],
        original_ACE_vs_direct_on_ThetaPhi_relative=relative(previous,direct),
        original_ACE_vs_direct_on_ThetaPhi_error_op_Ry=float(np.linalg.norm(err,2)),
        original_ACE_vs_direct_on_ThetaPhi_max_column_Ry=float(max(norms)),
        occupied_weighted_error_op_Ry=float(np.linalg.norm(err*np.sqrt(wg),2)),
        bands143_146_error_column_Ry=norms[142:146].tolist(),
        empty147_176_error_max_column_Ry=float(max(norms[146:])),
        original_ACE_source_interpolation_control_relative=relative(-Xi@(Xi.conj().T@Phi),VQ@(Q.conj().T@Phi)),
        no_material_instability_causation_proven=True,HSE_converged=False,physical_xc=None)
    (HERE/'offspan_discriminator.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
