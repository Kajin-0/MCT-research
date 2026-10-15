"""Actual distributed complex source spectra; no empirical gap law or new QE."""
import csv
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np
from scipy.special import expit
from packets import packet, Reader
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent
RY_EV=13.605693122994
WIDTHS=[1.,1.5,2.,2.5,3.]


def project(root,cycle):
    """Sum rank amplitudes BEFORE squaring, using physical G and spin indices."""
    overlap=np.zeros((6,176),complex);norm=np.zeros((6,6),complex)
    for rank in [0,1]:
        b=packet(root,'before',rank,cycle);a=packet(root,'after',rank,cycle)
        n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
        overlap+=a['probe'][ix].conj().T@b['phi'][ix]
        norm+=a['probe'][ix].conj().T@a['probe'][ix]
    assert np.linalg.norm(norm-np.eye(6),2)<1e-8
    retained=overlap@overlap.conj().T
    assert np.min(np.linalg.eigvalsh(np.eye(6)-retained))>=-1e-8
    return overlap,b['et'],b['wg'],norm


def fd_root(et):
    lo,hi=float(min(et)-1),float(max(et)+1)
    for _ in range(100):
        mid=(lo+hi)/2
        if np.sum(expit((mid-et)/.001))<144:lo=mid
        else:hi=mid
    return (lo+hi)/2


def bounded(weights,energy,W,eps,round_budget):
    """Positive missing mass bound for bounded Gaussian moment; conditional FP."""
    phi=np.exp(-energy**2/(2*W**2));M=float(weights@phi)
    N=float(weights@(energy*phi));c=N/M
    missing=max(0.,1-float(sum(weights)));den=M-2*eps-round_budget
    assert M>=.05 and den>0
    factor=(W/np.sqrt(np.e)+abs(c))/den
    return dict(mass=M,centroid_eV=c,retained_probability=float(sum(weights)),
                missing_probability=missing,conditional_tail_eV=missing*factor,
                conditional_frame_eV=2*eps*factor,
                conditional_roundoff_eV=round_budget*factor,
                conditional_bound_eV=(missing+2*eps+round_budget)*factor)


def main(members=('host','cd')):
    prior=json.loads((HERE.parent/'chemical_pbe_pilot_2026-10-14/numerical_result.json').read_text())
    eps={s:prior['host_sector_symmetry'][s]['nearby_invariant_projector_distance_upper_model'] for s in ['Gamma6','Gamma8']}
    u=2.**-53;gamma=lambda n:n*u/(1-n*u)
    entry=4*gamma(32*21654)+16*u
    round_budget=176*(2*entry+entry**2)+64*gamma(176)
    out={};arrays={};checks={}
    for member in members:
        root=r.PAIR/member;f=json.loads((root/'FINAL.json').read_text());assert f['accepted']
        rows=[]
        for cycle in range(1,f['science']['last_cycle']+1):
            overlap,et,wg,refnorm=project(root,cycle);mu=fd_root(et)
            assert max(abs(expit((mu-et)/.001)-wg))<=1e-9
            arrays[f'{member}_c{cycle}_overlap']=overlap
            arrays[f'{member}_c{cycle}_et_Ry']=et
            spectral={}
            for sector,sl,d in [('Gamma6',slice(0,2),2),('Gamma8',slice(2,6),4)]:
                weight=np.sum(abs(overlap[sl])**2,axis=0)/d
                # A second per-band scalar contraction, independent of axis sum.
                w2=np.array([np.vdot(overlap[sl,j],overlap[sl,j]).real/d for j in range(176)])
                assert max(abs(weight-w2))<1e-15
                energy=(et-mu)*RY_EV
                curves={str(W):bounded(weight,energy,W,eps[sector],round_budget) for W in WIDTHS}
                rotation=np.array([[0,1],[-1,0]],complex) if d==2 else np.eye(4,dtype=complex)[::-1]
                assert max(abs(np.sum(abs(rotation@overlap[sl])**2,axis=0)/d-weight))<1e-15
                gauge=bounded(weight,((et+.375)-(mu+.375))*RY_EV,2,eps[sector],round_budget)
                assert abs(gauge['centroid_eV']-curves['2.0']['centroid_eV'])<1e-13
                spectral[sector]=curves
                arrays[f'{member}_c{cycle}_{sector}_weights']=weight
            row=dict(cycle=cycle,FD_reference_Ry=mu,FD_reference_kind='independently reconstructed monotone root; native XML separately verified at final source',
                     spectral=spectral,source_scf_error_Ry=f['science']['source_cycles'][str(cycle)]['source_scf_error_Ry'],
                     outer_dexx_Ry=f['science']['residuals'].get(str(cycle),{}).get('dexx_Ry'),
                     ordering_eV={str(W):spectral['Gamma6'][str(W)]['centroid_eV']-spectral['Gamma8'][str(W)]['centroid_eV'] for W in WIDTHS},
                     retained_frame_mass_eigenvalues=np.linalg.eigvalsh(overlap@overlap.conj().T).tolist())
            rows.append(row)
        out[member]=rows
        checks[member]=dict(physical_G_spin_embedding=True,amplitudes_summed_before_square=True,
                            independent_column_trace=True,within_sector_unitary_invariance=True,energy_gauge_check=True)
    chemical=[]
    if set(members)=={'host','cd'}:
        for h,c in zip(out['host'],out['cd']):
            assert h['cycle']==c['cycle']
            for W in WIDTHS:
                s=str(W);value=c['ordering_eV'][s]-h['ordering_eV'][s]
                bound=sum(z['spectral'][a][s]['conditional_bound_eV'] for z in [h,c] for a in ['Gamma6','Gamma8'])
                chemical.append(dict(cycle=h['cycle'],W_eV=W,delta_eV=value,conditional_bound_eV=bound,conditional_interval_eV=[value-bound,value+bound]))
    result=dict(status='CALCULATED actual native source spectra; conditional positive-tail/frame/IEEE estimates',members=out,chemical=chemical,
                widths_eV=WIDTHS,round_budget=round_budget,original_frame_envelopes=eps,checks=checks,
                source_eigenvalues_solve_previous_ACE=True,
                does_not_bound_outer_limit_or_material_error=True,HSE_converged=all(json.loads((r.PAIR/m/'FINAL.json').read_text())['HSE_converged'] for m in members),physical_xc=None)
    tag='' if len(members)==2 else members[0]+'_'
    np.savez(HERE/(tag+'spectral_overlaps.npz'),**arrays)
    (HERE/(tag+'spectral_evolution.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    with (HERE/(tag+'spectral_response.csv')).open('w') as f:
        writer=csv.DictWriter(f,fieldnames=['cycle','W_eV','delta_eV','conditional_bound_eV','conditional_interval_eV'],lineterminator='\n');writer.writeheader();writer.writerows(chemical)
    print(json.dumps(dict(checks=checks,chemical_W2=[v for v in chemical if v['W_eV']==2]),indent=2))


if __name__=='__main__':main(tuple(sys.argv[1:]) or ('host','cd'))
