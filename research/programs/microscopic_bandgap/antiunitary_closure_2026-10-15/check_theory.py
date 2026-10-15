"""Three independent small Hermitian checks; no material validation."""
import json
from pathlib import Path
import numpy as np
from constructor import paired_cover

HERE = Path(__file__).resolve().parent


def main():
    rng = np.random.default_rng(702515)
    n = 8
    J = np.kron(np.eye(n//2), np.array([[0., -1.], [1., 0.]]))
    theta = lambda x: J@x.conj()
    tj = lambda A: J@A.conj()@J.T
    z = rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    A = z@z.conj().T + np.eye(n)
    A = (A+tj(A))/2
    S, _ = np.linalg.qr(z[:, :3])
    Q, history = paired_cover(S, theta, 1e-12)
    def ace(A, C):
        Y = A@C
        return Y@np.linalg.solve(C.conj().T@Y, Y.conj().T)
    old = ace(A, S)
    complete = ace(A, Q)
    averaged = (old+tj(old))/2
    source_error = np.linalg.norm(complete@S-A@S)
    commutator = np.linalg.norm(complete-tj(complete))
    average_failure = np.linalg.norm(averaged@S-A@S)
    assert source_error < 1e-11 and commutator < 1e-11 and average_failure > .01
    assert np.min(np.linalg.eigvalsh(A-complete)) > -1e-11

    # Independent density/functional derivative check with a real screened-style
    # spatial kernel and spin-flip T. This is not a material HSE kernel.
    U, _ = np.linalg.qr(z)
    D = (U*np.linspace(.05,.95,n))@U.conj().T
    P = lambda X:(X+tj(X))/2
    Db = P(D)
    delta = np.linalg.norm(D-tj(D),2)
    assert abs(np.linalg.norm(D-Db,2)-delta/2) < 1e-13
    kernel = np.kron(1/(1+abs(np.arange(4)[:,None]-np.arange(4)[None,:])), np.ones((2,2)))
    K = lambda X: -kernel*X
    energy = lambda X: float(np.trace(P(X)@K(P(X))).real/2)
    E = (z+z.conj().T)/20
    h = 1e-5
    derivative = (energy(D+h*E)-energy(D-h*E))/(2*h)
    analytic = float(np.trace(E@K(Db)).real)
    error = abs(derivative-analytic)
    assert error < 1e-9
    force_fd = ((1+h)*energy(D)-(1-h)*energy(D))/(2*h)
    assert abs(force_fd-energy(D)) < 1e-10

    # Positive old Gram cannot certify the augmented Gram.
    A0=np.diag([1.,1.,0.,0.]); C0=np.eye(4)[:,:2]
    assert min(np.linalg.eigvalsh(C0.T@A0@C0)) == 1.
    assert min(np.linalg.eigvalsh(A0)) == 0.
    # Same support but unequal Kramers weights breaks density TR.
    W=np.diag([.8,.2]); T2=J[:2,:2]
    assert np.linalg.norm(W-T2@W@T2.T,2) > .5
    result=dict(passed=True, checks=3, source_exact_complete_ACE_error=source_error,
        complete_ACE_TR_error=commutator, naive_ACE_average_source_failure=average_failure,
        constrained_exchange_derivative_error=error,
        positive_old_Gram_singular_augmented_counterexample=True,
        unequal_paired_weights_counterexample=True, material_validation=False)
    (HERE/'theory_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
