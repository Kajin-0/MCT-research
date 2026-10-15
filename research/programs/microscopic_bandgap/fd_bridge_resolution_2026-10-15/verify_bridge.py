"""Independent finite-matrix falsification/derivative checks, not material validation."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.linalg import block_diag
from scipy.special import expit

HERE=Path(__file__).resolve().parent


def fd(H,mu=0.,sigma=.001):
    w,V=np.linalg.eigh(H);return (V*expit((mu-w)/sigma))@V.conj().T


def main():
    rng=np.random.default_rng(20261015);herm=lambda n:(lambda X:(X+X.conj().T)/2)(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
    J=block_diag(np.array([[0,1],[-1,0]]),np.array([[0,1],[-1,0]]));S=np.diag([1,1,-1,-1])
    def twirl(X):
        Y=(X+S@X@S)/2;return (Y+J@Y.conj()@J.conj().T)/2
    X=.5*np.eye(4)+.03*herm(4);Y=herm(4);H0=herm(4);sigma=.001;a=.2;b=.13
    def energy(X):
        D=twirl(X);v=np.linalg.eigvalsh(D);assert min(v)>0 and max(v)<1
        return float(np.trace(H0@D).real-a/2*np.trace(D@D).real+b/2*np.trace(D).real**2+sigma*sum(v*np.log(v)+(1-v)*np.log(1-v)))
    D=twirl(X);v,V=np.linalg.eigh(D);logit=(V*np.log(v/(1-v)))@V.conj().T
    gradient=twirl(H0-a*D+b*np.trace(D)*np.eye(4)+sigma*logit)
    target=float(np.trace(gradient@Y).real);errors=[]
    for h in [1e-5,1e-6,1e-7]:errors.append(abs((energy(X+h*Y)-energy(X-h*Y))/(2*h)-target))
    assert max(errors)<1e-7
    fd_rows=[]
    for i in range(12):
        A=.001*herm(6);B=A+.0003*herm(6);actual=float(np.linalg.norm(fd(A)-fd(B),'fro'));bound=float(np.linalg.norm(A-B,'fro')/(4*sigma));assert actual<=bound*(1+1e-12)
        # Independently check the exact two-eigenbasis identity used in proof.
        av,AU=np.linalg.eigh(A);bv,BU=np.linalg.eigh(B);z=abs(AU.conj().T@BU)**2
        independent=float(np.sqrt(np.sum((expit(-av[:,None]/sigma)-expit(-bv[None,:]/sigma))**2*z)))
        assert abs(actual-independent)<1e-13
        fd_rows.append(dict(actual_F=actual,bound_F=bound,two_basis_identity_error=abs(actual-independent)))
    HS=.001*herm(2);HQ=.012*np.eye(4)+.0001*herm(4);L=float(min(np.linalg.eigvalsh(HQ)));B=.00005*(rng.normal(size=(4,2))+1j*rng.normal(size=(4,2)))
    H=np.block([[HS,B.conj().T],[B,HQ]]);trial=block_diag(fd(HS),np.zeros((4,4)))
    actual=float(np.linalg.norm(fd(H)-trial,'fro'));coupling=float(np.sqrt(2)*np.linalg.norm(B,'fro')/(4*sigma));tail=float(2*expit(-L/sigma));assert actual<=coupling+tail
    # Two identical Gamma8-copy scalar blocks commute with every representation
    # operation and its antiunitary lift. All known first-copy actions coincide.
    U=np.eye(8)[:,:4];E=.001;counter=[]
    for e2 in [-.006,.008]:
        H=block_diag(E*np.eye(4),e2*np.eye(4));np.testing.assert_array_equal(H@U,E*U)
        mu=(E+e2)/2;density=fd(H,mu);assert abs(np.trace(density).real-4)<1e-12
        counter.append(dict(unmeasured_copy_energy_Ry=e2,chemical_potential_Ry=mu,known_copy_FD_charge=float(np.trace(density[:4,:4]).real),total_FD_charge=float(np.trace(density).real)))
    assert abs(counter[0]['known_copy_FD_charge']-counter[1]['known_copy_FD_charge'])>3
    # Saturation/logit is a genuine limitation, never silently regularized.
    saturated=np.diag([1.,1.,.5,.5,0.,0.]);assert min(np.linalg.eigvalsh(saturated))==0 and max(np.linalg.eigvalsh(saturated))==1
    result=dict(status='PASS finite-matrix proof checks only; no material validation',twirled_energy_entropy_derivative_errors=errors,FD_two_basis_rows=fd_rows,offspace_bound=dict(actual_F=actual,coupling_bound_F=coupling,tail_bound_F=tail,complement_lower_bound_Ry=L),invariant_unknown_copy_counterexample=counter,saturated_logit_refused=True,new_native_jobs=0,physical_xc=None,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'theory.md',HERE/'preregistration.md']})
    (HERE/'independent_checks.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
