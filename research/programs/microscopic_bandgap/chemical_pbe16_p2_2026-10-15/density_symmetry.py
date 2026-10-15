"""Stable low-rank NONLOCAL density symmetry at retained actual FD states."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json
import numpy as np
from scipy.special import expit
from science_units_v2 import cell,read_spinors,original
import cd_owner as r

HERE=Path(__file__).resolve().parent


def audit(root):
    t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml')
    c,g,k=read_spinors(root/'out/r07pbe.save/wfc1.hdf5');assert np.linalg.norm(k)<1e-12
    e=np.fromstring(t.findtext('.//output/band_structure/ks_energies/eigenvalues'),sep=' ')*2
    ef=float(t.findtext('.//output/band_structure/fermi_energy'))*2
    occ=expit((ef-e)/.001);mask=occ>1e-12;tail=float(sum(occ[~mask]))
    assert tail<1e-10
    phi=c[mask].reshape(sum(mask),-1).T;del c
    gram=phi.conj().T@phi;ev,V=np.linalg.eigh(gram)
    sqrt=(V*np.sqrt(ev))@V.conj().T;inverse=(V/np.sqrt(ev))@V.conj().T
    Q=phi@inverse;del phi
    W=(sqrt*occ[mask])@sqrt
    denominator=float(np.linalg.norm(W,'fro'))
    N=len(g);lookup={tuple(v):i for i,v in enumerate(g)}
    minus=np.array([lookup[tuple(-v)] for v in g])
    def residual(T,antiunitary):
        S=Q.conj().T@T;B=T-Q@S;CB=B.conj().T@B
        Z=W.conj() if antiunitary else W
        A=W-S@Z@S.conj().T
        # Orthogonal Q/B blocks: stable sum of positive HS contributions,
        # avoiding subtraction of two nearly equal density norms.
        square=float(np.linalg.norm(A,'fro')**2+2*np.trace(Z@S.conj().T@S@Z@CB).real+np.trace(Z@CB@Z@CB).real)
        assert square>=-1e-20
        return dict(relative_density_HS_defect=float(np.sqrt(max(0,square))/denominator),basis_leakage_F=float(np.linalg.norm(B,'fro')),omitted_charge_density_defect_upper=2*tail/denominator,roundoff_not_interval_certified=True)
    T=np.r_[Q[N+minus].conj(),-Q[minus].conj()]
    rows={'Theta':residual(T,True)};del T
    ops=original.td_operations()
    chosen={}
    for op in ops:
        R=op['spatial']
        if round(np.linalg.det(R))==1 and np.trace(R)==0:chosen.setdefault('C3',op)
        if round(np.linalg.det(R))==-1 and np.trace(R)==-1:chosen.setdefault('S4',op)
    assert set(chosen)=={'C3','S4'}
    A=cell(t);physical=g@np.linalg.inv(A).T
    for name,op in chosen.items():
        mapped=physical@op['spatial'].T@A.T
        assert np.max(abs(mapped-np.rint(mapped)))<1e-10
        ix=np.array([lookup[tuple(v)] for v in np.rint(mapped).astype(int)])
        T=np.empty_like(Q).reshape(2,N,Q.shape[1])
        T[:,ix,:]=np.einsum('st,tgn->sgn',op['spin'],Q.reshape(2,N,Q.shape[1]))
        rows[name]=residual(T.reshape(Q.shape),False);del T
    return dict(occupation_cutoff=1e-12,retained_positive_rank=int(sum(mask)),dropped_charge_e=tail,full_FD_charge_e=float(sum(occ)),density_HS_norm=denominator,orthonormalization_Gram_error_F=float(np.linalg.norm(Q.conj().T@Q-np.eye(Q.shape[1]),'fro')),symmetry=rows,not_just_local_spin=True,native_FD_occupations_preserved=True,not_HSE_state_qualification=True)


def main():
    assert json.loads((r.PAIR/'cd/FINAL.json').read_text())['accepted']
    out={m:audit(root) for m,root in [('host',r.HOST),('cd',r.PAIR/'cd')]}
    (HERE/'density_symmetry_result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
