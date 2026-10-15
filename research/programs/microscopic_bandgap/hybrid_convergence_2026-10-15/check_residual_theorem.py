"""Independent tiny exact rational counterexample; no MPI, material, or fitting."""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent

def main():
    W=[[F(1),F(-1,2)],[F(-1,2),F(1)]]
    plus=[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]
    minus=[[F(1,2),F(-1,2)],[F(-1,2),F(1,2)]]
    delta=[[plus[i][j]-minus[i][j] for j in range(2)] for i in range(2)]
    form=sum(delta[i][j]*W[i][j]*delta[j][i] for i in range(2) for j in range(2))
    assert form==F(-1)
    # Independently evaluate cross and diagonal energies as rational numbers.
    form2=lambda a,b:sum(a[i][j]*W[j][i]*b[j][i] for i in range(2) for j in range(2))
    direct=-form2(plus,minus)+(form2(plus,plus)+form2(minus,minus))/2
    assert direct==F(-1,2)
    for a in [plus,minus]:assert min(np.linalg.eigvalsh(np.array(W,float)*np.array(a,float)))>0
    # Nontrivial complex ACE positivity and the exact quadratic decomposition.
    X=np.array([[1,1j,0],[0,2,1],[1,0,2j]],complex)
    A=X@X.conj().T;S=np.array([[1],[1j],[.5]],complex)
    compressed=A@S@np.linalg.inv(S.conj().T@A@S)@S.conj().T@A
    assert min(np.linalg.eigvalsh(A-compressed))>-1e-13
    result=dict(passed=True,checks=3,rational_superoperator_counterexample=str(form),
                direct_outer_counterexample_Ry=str(direct),
                ACE_remainder_min_eigenvalue=float(min(np.linalg.eigvalsh(A-compressed))),
                synthetic_only=True,new_native_invocations=0,novelty_claim=False)
    (HERE/'residual_theorem_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
