"""Independent scalar native witness and exact antiunitary algebra countercheck."""
import json,math
from pathlib import Path
import numpy as np
from packets import Reader,packet
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main():
    a=np.load(HERE/'host_symmetry_matrices.npz');D=a['c8_density'];T=a['c8_Theta_density']
    ev,z=np.linalg.eigh(D-T);j=int(np.argmax(abs(ev)));z=z[:,j];expected=float(ev[j])
    root=r.PAIR/'host';f=Reader(root/'reference.bin');f.take('<i8',(4,));f.take('<f8',(3,3));f.take('<f8',(3,))
    G=f.take('<i8',(3,7809)).T;C=f.take('<c16',(15618,6));f.end();lookup={tuple(g):i for i,g in enumerate(G)}
    minus=np.array([lookup[tuple(-g)] for g in G]);TC=np.r_[C[7809+minus].conj(),-C[minus].conj()]
    v=C@z;tv=TC@z.conj();amp=np.zeros(176,complex);tamp=amp.copy();norm=0.
    for rank in [0,1]:
        b=packet(root,'before',rank,8);n,p=b['nnpw'],b['npwx'];vloc=np.zeros(2*p,complex);tloc=vloc.copy()
        for i,g in enumerate(b['G']):
            if tuple(g) in lookup:
                k=lookup[tuple(g)];vloc[i]=v[k];vloc[i+p]=v[k+7809];tloc[i]=tv[k];tloc[i+p]=tv[k+7809]
        norm+=np.vdot(vloc,vloc).real
        for k in range(176):amp[k]+=np.vdot(b['phi'][:,k],vloc);tamp[k]+=np.vdot(b['phi'][:,k],tloc)
    observed=math.fsum(float(b['wg'][k])*(abs(amp[k])**2-abs(tamp[k])**2) for k in range(176))
    assert abs(norm-1)<1e-12 and abs(observed-expected)<1e-10
    # Arbitrary non-TR-closed projector: direct full-space compression identity.
    rng=np.random.default_rng(702515);S=np.kron(np.array([[0,1],[-1,0]]),np.eye(3))
    U=np.linalg.qr(rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)))[0]
    P=U[:,:2];Q=S@P.conj();H=U@np.diag([.1,.2,.3,.6,.8,.9])@U.conj().T
    exact=P.conj().T@S@H.conj()@S.conj().T@P
    compressed=(Q.conj().T@H@Q).conj();error=float(np.max(abs(exact-compressed)))
    assert error<1e-14
    result=dict(passed=True,actual_native_scalar_witness=observed,stored_compressed_eigenvalue=expected,scalar_witness_error=abs(observed-expected),test_vector_norm=norm,
                full_native_TR_defect_operator_lower_bound=abs(observed)/norm,
                synthetic_nonclosed_projector_identity_error=error,synthetic_not_material_validation=True,new_native_invocations=0)
    (HERE/'symmetry_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
