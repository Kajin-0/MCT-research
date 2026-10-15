"""Independent FFT normalization, trial positivity and finite-state bound checks."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.special import expit
HERE=Path(__file__).resolve().parent;DFT=Path('/home/User/opencode_workspace/DFT');ROOT=DFT/'.local/qe75_lowram_20261011/h8h_20261015'


def main():
    if (ROOT/'expected_density.npz').exists():raise FileExistsError('preserve independent density')
    a=np.load(ROOT/'trial.npz');G=a['G'];N=len(G);phi=a['source'][:,:146];w=a['weights'][:146];omega=(6.46/.529177210903)**3
    # Native alat conversion may differ at relative~1e-9. Instead pin native
    # physical B from the retained two-rank packet and use its exact determinant.
    import sys
    sys.path.insert(0,str(HERE.parent/'antiunitary_closure_2026-10-15'))
    from audit_native import ROOT as OLD
    from packets import packet
    B=packet(OLD,'before',0,1)['B'];omega=float((2*np.pi)**3/np.linalg.det(B))
    rho=np.zeros((60,60,60,4));ix=tuple((G%60).T)
    for j in range(146):
        z=np.zeros((2,60,60,60),complex)
        for spin in [0,1]:z[spin][ix]=phi[spin*N:(spin+1)*N,j]
        p=np.fft.ifftn(z,axes=(1,2,3))*60**3;u,d=p
        rho[:,:,:,0]+=w[j]*(abs(u)**2+abs(d)**2)/omega
        rho[:,:,:,1]+=w[j]*2*(u.conj()*d).real/omega
        rho[:,:,:,2]+=w[j]*2*(u.conj()*d).imag/omega
        rho[:,:,:,3]+=w[j]*(abs(u)**2-abs(d)**2)/omega
    charge=float(rho[:,:,:,0].sum()*omega/60**3);spin=float(np.max(abs(rho[:,:,:,1:])));assert abs(charge-144)<1e-8 and spin<1e-10
    assert np.min(rho[:,:,:,0])>=0
    np.savez(ROOT/'expected_density.npz',rhoR=rho,omega=omega)
    # Independent exact finite-dimensional full-space commutator lower bound.
    rng=np.random.default_rng(7126);X=rng.normal(size=(10,10))+1j*rng.normal(size=(10,10));H=(X+X.conj().T)/2;P=np.eye(10)[:,:4];D=np.diag([1.,1.,.5,.5]);full=P@D@P.T;HQ=H@P;small=P.T@HQ;R=HQ-P@small
    CF=float(np.sqrt(np.linalg.norm(small@D-D@small,'fro')**2+2*np.linalg.norm(R@D,'fro')**2));assert abs(CF-np.linalg.norm(H@full-full@H,'fro'))<1e-12
    e,U=np.linalg.eigh(H);FD=(U*expit(-e/.001))@U.conj().T;lower=CF/(2*np.linalg.norm(H,2));actual=float(np.linalg.norm(full-FD,'fro'));assert lower<=actual
    out=dict(status='PASS independent FFT/source and whole-space lower-bound checks',independent_charge_e=charge,maximum_spin_density_abs=spin,omega_Bohr3=omega,entropy_kB=float(-sum(np.where(w==.5,w*np.log(.5)+(1-w)*np.log(.5),0.))),matrix_commutator_identity_error=float(abs(CF-np.linalg.norm(H@full-full@H,'fro'))),matrix_FD_error_actual_F=actual,matrix_FD_error_lower_F=lower,not_material_FD_validation=True,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'trial.npz',ROOT/'expected_density.npz',HERE/'preregistration.md']})
    (HERE/'qualification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
