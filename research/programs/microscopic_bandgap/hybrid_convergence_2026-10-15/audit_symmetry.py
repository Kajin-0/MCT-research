"""Independent Gamma-frame density/EXX time-reversal and Schur witnesses."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.special import expit
from packets import packet,Reader
from spectral_evolution import project,fd_root
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def time_reversal_frame(root):
    f=Reader(root/'reference.bin');h=f.take('<i8',(4,));assert tuple(h)==(70251406,7809,6,1)
    f.take('<f8',(3,3));f.take('<f8',(3,));G=f.take('<i8',(3,7809)).T
    C=f.take('<c16',(15618,6));f.end()
    lookup={tuple(g):j for j,g in enumerate(G)}
    minus=np.array([lookup[tuple(-g)] for g in G])
    theta=np.r_[C[7809+minus].conj(),-C[minus].conj()]
    J=C.conj().T@theta
    residual=float(np.linalg.norm(theta-C@J,2))
    assert np.linalg.norm(C.conj().T@C-np.eye(6),2)<1e-8
    return J,G,theta,dict(TR_frame_residual_op=residual,TR_square_minus_identity_error=float(np.linalg.norm(J@J.conj()+np.eye(6),2)),
                  reference_Gram_error=float(np.linalg.norm(C.conj().T@C-np.eye(6),2)),
                  TR_invariant_frame_assumed=False)

def main(member='host',cycles=None):
    root=r.PAIR/member;J,refG,thetaC,frame=time_reversal_frame(root)
    text=(root/'pw.out').read_text();completed=text.count('R07_RELAX_SOURCE_OPERATOR')
    cycles=cycles or list(range(1,completed+1));assert max(cycles)<=completed
    # All selected sources precede a subsequent collective boundary OR final punch.
    assert max(cycles)<completed or 'R07_BOUNDED_OUTER_PUNCH_COMPLETE' in text
    rows=[];arrays={};lookup={tuple(g):i for i,g in enumerate(refG)}
    for c in cycles:
        O=np.zeros((6,176),complex);Ot=O.copy();X=np.zeros((6,6),complex);local=X.copy();found=set()
        for rank in [0,1]:
            b=packet(root,'before',rank,c);a=packet(root,'after',rank,c);v=packet(root,'local1',rank,c)
            n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
            theta=np.zeros((p*2,6),complex)
            for i,g in enumerate(b['G']):
                if tuple(g) in lookup:
                    j=lookup[tuple(g)];theta[i]=thetaC[j];theta[i+p]=thetaC[j+7809];found.add(tuple(g))
            O+=a['probe'][ix].conj().T@b['phi'][ix]
            Ot+=theta[ix].conj().T@b['phi'][ix]
            X+=a['probe'][ix].conj().T@a['direct_probe'][ix]
            local+=v['probe'][ix].conj().T@v['action'][ix]
        assert len(found)==7809
        et,wg=b['et'],b['wg'];mu=fd_root(et)
        D=(O*wg[None,:])@O.conj().T
        Dtheta=((Ot*wg[None,:])@Ot.conj().T).conj()
        DD=D-Dtheta
        # Schur witness: an invariant irreducible Gamma8 density block is scalar.
        schur=D[2:,2:]-np.eye(4)*np.trace(D[2:,2:])/4
        rows.append(dict(cycle=c,total_charge_e=float(sum(wg)),FD_charge_residual_e=float(sum(expit((mu-et)/.001))-144),
            Gamma8_projected_density_eigenvalues=np.linalg.eigvalsh(D[2:,2:]).tolist(),
            projected_density_TR_defect_op=float(np.linalg.norm(DD,2)),
            Gamma8_density_Schur_defect_op=float(np.linalg.norm(schur,2)),
            Gamma8_direct_EXX_scalar_defect_Ry=float(np.linalg.norm(X[2:,2:]-np.eye(4)*np.trace(X[2:,2:])/4,2)),
            Gamma8_local_scalar_defect_Ry=float(np.linalg.norm(local[2:,2:]-np.eye(4)*np.trace(local[2:,2:])/4,2)),
            source_bands143_146_spread_eV=float(np.ptp(et[142:146])*13.605693122994),
            source_bands143_146_occupations=wg[142:146].tolist()))
        arrays['c'+str(c)+'_density']=D;arrays['c'+str(c)+'_Theta_density']=Dtheta;arrays['c'+str(c)+'_EXX']=X;arrays['c'+str(c)+'_local']=local
    tag=member+('_partial' if max(cycles)<completed else '')
    result=dict(status='CALCULATED actual complex symmetry witnesses; physical instability mechanism is a HYPOTHESIS',member=member,rows=rows,frame=frame,
                reference_matrix_convention='Theta(up(G),down(G))=(down*(-G),-up*(-G)); exact compressed Theta-density=[(Theta P)dagger D(Theta P)]star; J only describes approximate frame closure',
                no_native_or_Fermi_gate_retroactively_changed=True,native_crystal_symmetry_flag_is_not_Fock_state_symmetry_proof=True,
                physical_magnetism_or_material_phase_claim=False,physical_xc=None)
    np.savez(HERE/(tag+'_symmetry_matrices.npz'),J=J,**arrays)
    (HERE/(tag+'_symmetry_audit.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'host',[int(v) for v in sys.argv[2:]] or None)
