"""Third analytical cycle: exact critical-IR scale and source-only closure."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad

HERE=Path(__file__).resolve().parent
norm=lambda a:float(np.linalg.norm(a,2))


def liouvillian(H):
    d=len(H)
    return np.kron(np.eye(d),H)-np.kron(H.T,np.eye(d))


def main():
    records=[]
    for c in [.01,.001]:
        Lambda=1.;scale=(np.pi*c)**2
        values=[]
        for delta in [.01*scale,scale,100*scale]:
            a=2*c/np.sqrt(delta)*np.arctan(np.sqrt(Lambda/delta))
            indicator=1/(1+a)
            relative_error=1-indicator
            bound=np.pi*c/np.sqrt(delta)
            assert 0<relative_error<=bound
            values.append(dict(delta=delta,atom_indicator_at_finite_offset=indicator,
                relative_free_pole_error=relative_error,error_bound=bound))
        assert .5<values[1]['atom_indicator_at_finite_offset']<.52
        records.append(dict(c=c,Lambda=Lambda,exact_atom_weight=0,
            tuned_static_shift=2*c*np.sqrt(Lambda),gap_side_crossover_scale=scale,
            checks=values))
    # Check uniform pole-like finite-offset behavior while exact atom stays0.
    delta_min=.01;tolerance=.001
    c=tolerance*np.sqrt(delta_min)/(2*np.pi)
    a=2*c/np.sqrt(delta_min)*np.arctan(np.sqrt(1/delta_min))
    relative=a/(1+a)
    assert relative<tolerance
    eta_IR=delta_min;zeta=1j*eta_IR
    integrand=lambda u:1/(zeta-u*u)
    ir=quad(lambda u:integrand(u).real,0,1)[0]+1j*quad(lambda u:integrand(u).imag,0,1)[0]
    analytic=np.arctanh(1/np.sqrt(zeta))/np.sqrt(zeta)
    assert abs(ir-analytic)<1e-11
    gi=1/zeta/(1-2*c*ir)
    relative_eta=float(abs(gi-1/zeta)/abs(1/zeta))
    aeta=4*c/np.sqrt(eta_IR);bound_eta=aeta/(1-aeta)
    assert aeta<1 and relative_eta<=bound_eta<tolerance

    # L3 uses only the transition-source contraction, independently checked
    # against complete small dense resolvents and perturbed source bounds.
    H0=np.diag([.2,-.3]);W1=np.array([[0.,.005],[.005,0.]])
    W2=np.array([[.003,-.002j],[.002j,-.003]])
    LW=[liouvillian(w) for w in [W1,W2,-W1-W2]]
    LL=liouvillian(H0);eta=.2;z=.4+1j*eta;I=np.eye(4)
    R0=np.linalg.inv(z*I-LL)
    RR=[np.linalg.inv(z*I-LL-w) for w in LW]
    Rav=sum(RR)/3;B=sum(w@R0@w for w in LW)/3
    v=np.array([0,0,1,0],complex)
    contraction=v.conj()@R0@B@R0@v
    predicted=v.conj()@R0@v+contraction
    actual=v.conj()@Rav@v
    r=max(norm(w) for w in LW)/eta
    remainder=r**3/(eta*(1-r))
    assert abs(actual-predicted)<=remainder
    eA=.001
    vv=[v+eA*np.eye(4)[i] for i in [0,1,3]]
    with_sources=sum(u.conj()@R@u for u,R in zip(vv,RR))/3
    source_error=abs(with_sources-actual)
    source_bound=(2*eA+eA*eA)/eta
    assert source_error<=source_bound

    # Only a finite spectral gap perturbation check, NOT a topological
    # computation or proof that cubic inverted HgTe has a gap.
    Hk=np.diag([-1.,-1.,1.,1.]);rng=np.random.default_rng(26015)
    X=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));X=(X+X.conj().T)/2
    W=.2*X/norm(X);minimum=1.
    for t in [0.,.5,1.]:
        gap=float(np.min(abs(np.linalg.eigvalsh(Hk+t*W))))
        assert gap>=1-t*.2-1e-13
        minimum=min(minimum,gap)
    out=dict(status='PASS',material_validation=False,physical_xc=None,native_jobs=0,
        values_are_synthetic=True,critical_IR_checks=records,
        arbitrarily_pole_like_without_atom=dict(c=c,delta_min=delta_min,
            required_relative_tolerance=tolerance,actual_relative_error=relative,
            eta=eta_IR,actual_relative_eta_error=relative_eta,
            relative_eta_error_bound=bound_eta,
            exact_atom_weight=0),
        source_contracted_closure=dict(actual_error=float(abs(actual-predicted)),
            remainder_bound=remainder,source_change_error=float(source_error),
            source_change_bound=source_bound),
        finite_gap_perturbation_check=dict(minimum_measured_gap=minimum,
            uniform_lower_bound=.8,not_topological_validation=True))
    (HERE/'resolution_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
