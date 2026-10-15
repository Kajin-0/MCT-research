"""Finite data-sufficiency counterexamples; NOT alternative HSE Hamiltonians."""
from pathlib import Path
import json
import numpy as np
from analyze import HERE,SOURCE,PRIVATE,RYEV,norm

def main():
    f=np.load(PRIVATE/'trial.npz');q=f['Q'];P=f['P'];d=np.load(PRIVATE/'full_actions.npz');A=(d['H']+d['H'].conj().T)/2;R=d['HV']-q@A;R-=q@(q.conj().T@R);W=R.conj().T@R;B=q.conj().T@P
    s=json.loads((SOURCE/'native_science.json').read_text());mu=s['projected_FD_mu_Ry'];bounds=s['H_operator_norm_upper_Ry'];rows=[];Anorm=norm(A);Rnorm=norm(R)
    # Every C=cI is causal, Hermitian, symmetry-compatible in the exact
    # covariance model and preserves ALL known H(V) columns and ||R||.
    for dc in [-1.,-.5,-.1,-.05,-.01,-.001,0.,.001,.01,.05,.1,.5,1.]:
        c=mu+dc
        for eta_eV in [.05,.5,2.]:
            z=mu+1j*eta_eV/RYEV
            G=B.conj().T@np.linalg.solve(z*np.eye(304)-A-W/(z-c),B)
            vals=[complex(np.trace(G[:2,:2])/2),complex(np.trace(G[2:,2:])/4)]
            ordering=float((1/vals[1]-1/vals[0]).real*RYEV)
            coarse=float(max(Anorm,abs(c))+Rnorm);assert coarse<bounds
            rows.append(dict(dc_Ry=dc,eta_eV=eta_eV,ordering_eV=ordering,coarse_completion_H_norm_bound_Ry=coarse,compatible_with_captured_coarse_H_norm_bound=True,causal_min_eigen_minus_Im_g=float(min(np.linalg.eigvalsh(-(G-G.conj().T)/(2j))))))
    out=dict(status='CALCULATED_SYMMETRY_COMPATIBLE_DATA_COMPLETIONS_NOT_HSE_MODELS',all304_basis_HV_retained=True,independent_12_physical_probe_actions_NOT_imposed=True,no_specific_material_complement_asserted=True,no_PHYSICAL_nonidentifiability_when_full_HSE_operator_is_known_claim=True,assumptions=['finiteHermiticity','sameA and fullR','exactjointTdTheta representation up to captured roundoff','captured coarseHnorm bound'],rows=rows,ranges={str(e):[min(x['ordering_eV'] for x in rows if x['eta_eV']==e),max(x['ordering_eV'] for x in rows if x['eta_eV']==e)] for e in [.05,.5,2.]})
    assert min(x['causal_min_eigen_minus_Im_g'] for x in rows)>-1e-8
    (HERE/'completion_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['ranges']))
if __name__=='__main__':main()
