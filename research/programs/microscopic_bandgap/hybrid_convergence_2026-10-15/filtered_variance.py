"""Bounded spectral dispersion and dominant-character clusters from real overlaps."""
import json,sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
RY_EV=13.605693122994

def variance(weights,t,W,delta):
    phi=np.exp(-t*t/(2*W*W));M=float(weights@phi)
    mean=float(weights@(t*phi))/M;second=float(weights@(t*t*phi))/M
    v=second-mean*mean
    assert v>=-1e-12 and M>=.05 and M>delta
    dc=delta*(W/np.sqrt(np.e)+abs(mean))/(M-delta)
    dq=delta*(2*W*W/np.e+abs(second))/(M-delta)
    bound=dq+dc*(2*abs(mean)+dc)
    return dict(variance_eV2=v,dispersion_eV=float(np.sqrt(max(0,v))),conditional_variance_error_eV2=bound,
                conditional_interval_eV2=[max(0,v-bound),v+bound],mass=M)

def main(tag=''):
    spec=json.loads((HERE/(tag+'spectral_evolution.json')).read_text());a=np.load(HERE/(tag+'spectral_overlaps.npz'))
    rows={}
    for member,series in spec['members'].items():
        rows[member]=[]
        for record in series:
            c=record['cycle'];O=a[f'{member}_c{c}_overlap'];et=a[f'{member}_c{c}_et_Ry'];mu=record['FD_reference_Ry']
            bands={};vr={}
            for label,sl,d in [('Gamma6',slice(0,2),2),('Gamma8',slice(2,6),4)]:
                w=a[f'{member}_c{c}_{label}_weights'];ids=np.argsort(-w)[:d]
                discarded=np.ones(176,bool);discarded[ids]=False
                bands[label]=dict(native_bands_1based=(ids+1).tolist(),retained_dominant_character=float(sum(w[ids])),
                    leakage_outside_dominant_cluster=max(0.,1-float(sum(w[ids]))),
                    energy_mean_relative_reference_eV=float(np.mean(et[ids]-mu)*RY_EV),
                    energy_spread_eV=float(np.ptp(et[ids])*RY_EV),
                    nearest_other_eigenvalue_separation_eV=float(min(abs(et[ids,None]-et[discarded][None,:]).ravel())*RY_EV),
                    dominant_trace_weight_gap=float(min(w[ids])-max(w[discarded])))
                r=max(0.,1-float(sum(w)));eps=spec['original_frame_envelopes'][label]
                vr[label]={str(W):variance(w,(et-mu)*RY_EV,W,r+2*eps+spec['round_budget']) for W in spec['widths_eV']}
                # Exact two-point measure check: variance is its scalar formula.
                v2=variance(np.array([.4,.6]),np.array([-1.,1.]),2.,0.)
                assert abs(v2['variance_eV2']-.96)<1e-14
            rows[member].append(dict(cycle=c,dominant_character_clusters=bands,filtered_dispersion=vr,
                dominant_cluster_ordering_eV=bands['Gamma6']['energy_mean_relative_reference_eV']-bands['Gamma8']['energy_mean_relative_reference_eV']))
    result=dict(status='CALCULATED bounded spectral dispersion and fixed-frame character clusters',members=rows,
                not_intrinsic_disorder_linewidth=True,not_unbounded_PHQ_norm=True,not_quasiparticle_gap_or_physical_xc=True,
                physical_xc=None,missing_high_energy_first_second_moments_cannot_be_bounded_from_probability_alone=True)
    (HERE/(tag+'filtered_variance.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({m:rows[m][-1] for m in rows},indent=2))

if __name__=='__main__':main((sys.argv[1]+'_') if len(sys.argv)>1 else '')
