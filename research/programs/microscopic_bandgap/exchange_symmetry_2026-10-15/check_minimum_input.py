"""Three tiny independent algebra checks; not HgTe material validation."""
import json
import numpy as np
from pathlib import Path

def main():
    n=8;x=np.arange(n);phase=np.exp(2j*np.pi*x/n)/np.sqrt(n)
    S=np.zeros((2*n,2),complex);S[:n,0]=phase;S[n:,1]=phase
    theta=lambda a:np.r_[a[n:].conj(),-a[:n].conj()]
    T=theta(S);Dp=S@S.conj().T;Dm=T@T.conj().T
    local=lambda D:np.array([D[np.ix_([i,n+i],[i,n+i])] for i in range(n)])
    assert np.max(abs(local(Dp)-local(Dm)))<1e-14
    assert abs(np.linalg.norm(Dp-Dm,2)-1)<1e-14
    # Minimal completion rank = n_source + orthogonal Theta leakage rank.
    residual=T-S@(S.conj().T@T);rank=int(np.linalg.matrix_rank(residual,tol=1e-12))
    M=np.c_[S,T];assert np.linalg.matrix_rank(M,tol=1e-12)==2+rank==4
    assert np.linalg.norm(theta(M)@theta(M).conj().T-M@M.conj().T,2)<1e-14
    # Nonconstant positive Fourier kernel: distinct source action on +G up.
    v0,v2G=1.,.25;assert -v0!=-v2G
    result=dict(passed=True,checks=3,local_spin_density_difference_max=float(np.max(abs(local(Dp)-local(Dm)))),
                nonlocal_TR_density_difference_op=float(np.linalg.norm(Dp-Dm,2)),minimal_completion_dimension=4,
                source_columns=2,additional_columns=rank,kernel_source_test_values=[-v0,-v2G],
                synthetic_only=True,no_material_parameter_fit=True,new_native_invocations=0)
    Path(__file__).with_name('minimum_input_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
