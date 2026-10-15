"""Independent tiny exact Hermitian bath check; not material validation."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm,block_diag


def main():
    rng=np.random.default_rng(1502026)
    A=rng.normal(size=(12,12))+1j*rng.normal(size=(12,12))
    U=expm(.003*(A-A.conj().T));C=U[:6]
    e=np.linspace(-4,4,12);eta=.05;z=1j*eta
    G=(C/(z-e))@C.conj().T;Cp=C[:,:10]
    Gp=(Cp/(z-e[:10]))@Cp.conj().T
    R=np.eye(6)-Cp@Cp.conj().T
    delta=np.linalg.norm(R,2)/eta
    assert min(np.linalg.eigvalsh(R))>-1e-13
    assert np.linalg.norm(G-Gp,2)<=delta+1e-13
    a=np.linalg.norm(np.linalg.inv(Gp),2);assert a*delta<1
    inverse_bound=a*a*delta/(1-a*delta)
    inverse_error=np.linalg.norm(np.linalg.inv(G)-np.linalg.inv(Gp),2)
    assert inverse_error<=inverse_bound
    H=z*np.eye(6)-np.linalg.inv(G)
    assert min(np.linalg.eigvalsh(-(H-H.conj().T)/(2j)))>-1e-12
    V=block_diag(*[np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))[0] for n in [2,4]])
    Ha=z*np.eye(6)-np.linalg.inv(V@G@V.conj().T)
    ordering=lambda h:float((np.trace(h[:2,:2])/2-np.trace(h[2:,2:])/4).real)
    assert abs(ordering(Ha)-ordering(H))<1e-12
    # Necessity counterexample: no omitted-mass bound follows from visible G
    # if its full normalized measure/projector is unspecified.
    extra_weight=100.
    unbounded_error=extra_weight/eta
    assert unbounded_error>1000*delta
    out=dict(status='independent exact synthetic bath only',positive_omitted_measure=True,delta_G_bound=delta,actual_delta_G=float(np.linalg.norm(G-Gp,2)),inverse_error=float(inverse_error),inverse_bound=float(inverse_bound),block_gauge_ordering_error_eV=abs(ordering(Ha)-ordering(H)),native_material_validation=False)
    (Path(__file__).parent/'resolvent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
