"""Independent exact dense/symbolic counterexamples; no native calculations."""
from pathlib import Path
import json
import numpy as np
from fractions import Fraction as F
from numpy.polynomial import Polynomial as Poly
HERE=Path(__file__).resolve().parent
I=np.eye(2)
herm=lambda X:(X-X.conj().T)/(2j)
norm=lambda X:float(np.linalg.norm(X,2))

def main():
    a,t,d=2.,1.,.25;Hp=np.array([[0,t+d],[t+d,a]]);Hm=np.array([[0,t-d],[t-d,a]]);H=(Hp+Hm)/2;W=(Hp-Hm)/2;z=a+.01j
    G=(np.linalg.inv(z*I-Hp)+np.linalg.inv(z*I-Hm))/2;S=z*I-H-np.linalg.inv(G);Sf=W@np.linalg.inv(z*I-H)@W
    assert norm(S-Sf)<1e-12 and np.linalg.eigvalsh(-herm(S)).min()>-1e-12
    g=G[0,0];Ktotal=z-1/g;Kch=t*t/(z-a);delta=Ktotal-Kch
    exact=d*d/(z-a)*(1+4*t*t/(z*(z-a)-t*t-d*d))
    assert abs(delta-exact)<1e-10 and delta.imag>0 and Ktotal.imag<0
    reduced=(S[0,0]+(H[0,1]+S[0,1])/(z-H[1,1]-S[1,1])*(H[1,0]+S[1,0])-Kch)
    assert abs(reduced-delta)<1e-10
    # One symbolic proof is independent of the numerical dense inversion.
    Z=Poly([F(0),F(1)]);T,D,A=F(1),F(1,4),F(2);N=Z*(Z-A)-T*T-D*D
    # Cross-multiply the rational Green expressions, checking every exact
    # polynomial coefficient (independent of the floating dense inversion).
    polynomial=Z*(Z-A)*N-(N*N-4*T*T*D*D)-T*T*N-D*D*(N+4*T*T)
    assert all(c==0 for c in polynomial.coef)
    # Identical own-reference data and variances, opposite aligned mass kernels.
    aa,bb=.3,.2;zz=.7+.11j;results=[];relative=[]
    for sign in [-1,1]:
        c=[sign*aa*u for u in [-1,1]];m=[bb*u for u in [-1,1]]
        gs=[sum(1/(zz-cc-j*mm) for cc,mm in zip(c,m))/2 for j in [1,-1]]
        se=[zz-1/g for g in gs];mass=(se[0]-se[1])/2
        assert abs(mass-sign*2*aa*bb/zz)<1e-12
        relative.append([sum(1/(zz-j*mm) for mm in m)/2 for j in [1,-1]])
        results.append(dict(correlation_sign=sign,aligned_mass_kernel=[mass.real,mass.imag],variance_scalar=aa**2,variance_mass=bb**2))
    assert np.max(abs(np.array(relative[0])-np.array(relative[1])))==0
    # General cross contraction, preserving off-diagonal coherent propagation.
    J=np.diag([1.,1.,-1.,-1.,-1.,-1.]);rng=np.random.default_rng(7315);X=rng.normal(size=(6,6))+1j*rng.normal(size=(6,6));H6=(X+X.conj().T)/2;Gc=np.linalg.inv((.5+.2j)*np.eye(6)-H6)
    C=np.array([[.09,.04],[.04,.04]]);S6=C[0,0]*Gc+C[1,1]*J@Gc@J+C[0,1]*Gc@J+C[1,0]*J@Gc
    errs=[]
    for sl,j in [(slice(0,2),1),(slice(2,6),-1)]:
        actual=np.trace(S6[sl,sl]);wanted=(C[0,0]+C[1,1]+2*j*C[0,1])*np.trace(Gc[sl,sl]);errs.append(abs(actual-wanted))
    assert max(errs)<1e-12
    # Fano zero is not an eigenvalue. Host/residual T subtraction is exact.
    Hf=np.array([[0.,1.],[1.,2.]]);assert abs(np.linalg.inv(2*I-Hf)[0,0])<1e-12 and abs(np.linalg.det(2*I-Hf))>0
    z0,V,h=F(5,3),F(2,5),F(1,7);g0=1/(z0-h);gB=1/(z0-h-V)
    exact_derivative=(gB-g0)/(g0*g0)-V
    assert exact_derivative==V/(1-g0*V)-V
    out=dict(status='PASS',symbolic_projected_difference_identity=True,full_self_energy_causality_min=float(np.linalg.eigvalsh(-herm(S)).min()),full_augmented_dense_identity_error=norm(S-Sf),projected_difference_positive_Im=float(delta.imag),projected_Schur_formula_error=abs(reduced-delta),own_reference_responses_identical=True,aligned_counterexamples=results,covariance_quotient_trace_errors=[float(x) for x in errs],Fano_zero_not_eigenvalue=True,full_residual_T_identity=True,material_validation=False,physical_xc=None)
    (HERE/'accounting_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
