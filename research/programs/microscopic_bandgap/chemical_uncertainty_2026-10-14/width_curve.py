"""Preregistered real retained-spectrum sensitivity; no native run or fit."""
from pathlib import Path
import json
import hashlib
import numpy as np

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'chemical_pbe_pilot_2026-10-14'
WIDTHS=[1.,1.5,2.,2.5,3.]
OFFSETS=[-.5,-.25,0.,.25,.5]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def bounded_centroid(weights,t,W,epsilon,round_budget):
    phi=np.exp(-t*t/(2*W*W));M=float(weights@phi);N=float(weights@(t*phi));c=N/M
    r=max(0.,float(1-sum(weights)));den=M-2*epsilon-round_budget
    if M<.05 or den<=0:raise ValueError('unchanged mass/perturbation gate')
    B=W/np.sqrt(np.e);factor=(B+abs(c))/den
    return dict(mass=M,centroid_relative_reference_eV=c,omitted_probability=r,
        conditional_tail_eV=r*factor,conditional_projector_eV=2*epsilon*factor,
        conditional_arithmetic_eV=round_budget*factor,
        conditional_total_eV=(r+2*epsilon+round_budget)*factor,
        joint_denominator=den)


def response(data,W,offsets,envelopes,round_budget):
    per={}
    for member in ['host','cd']:
        b={label:bounded_centroid(v['weights'],v['energy_relative_Fermi_eV']-offsets[member],W,envelopes[label],round_budget) for label,v in data[member].items()}
        per[member]=dict(branches=b,ordering_eV=b['Gamma6']['centroid_relative_reference_eV']-b['Gamma8']['centroid_relative_reference_eV'])
    delta=per['cd']['ordering_eV']-per['host']['ordering_eV'];bound=sum(v['conditional_total_eV'] for m in per.values() for v in m['branches'].values())
    return dict(W_eV=W,reference_offsets_from_own_Fermi_eV=offsets,delta_eV=delta,conditional_bound_eV=bound,conditional_interval_eV=[delta-bound,delta+bound],members=per)


def old_data():
    prior=json.loads((OLD/'numerical_result.json').read_text());overlap=np.load(OLD/'complex_overlaps.npz');data={m:{} for m in ['host','cd']};pins={}
    for member in data:
        for label,d in [('Gamma6',2),('Gamma8',4)]:
            path=OLD/(member+'_'+label+'_spectrum.csv');v=np.loadtxt(path,delimiter=',',skiprows=1)
            # Decode retained complex coefficients independently, keep unitary
            # trace normalization; no normalization by retained band weight.
            w=np.sum(abs(overlap[member+'_'+label])**2,axis=0)/d
            np.testing.assert_allclose(w,v[:,2],rtol=0,atol=2e-16)
            data[member][label]=dict(weights=w,energy_relative_Fermi_eV=v[:,1]);pins[str(path)]=sha(path)
    pins[str(OLD/'complex_overlaps.npz')]=sha(OLD/'complex_overlaps.npz');pins[str(OLD/'numerical_result.json')]=sha(OLD/'numerical_result.json')
    env={l:prior['host_sector_symmetry'][l]['nearby_invariant_projector_distance_upper_model'] for l in ['Gamma6','Gamma8']}
    n=2*prior['host']['native_plane_waves'];u=2.**-53
    gamma=lambda m:m*u/(1-m*u)
    entry=4*gamma(32*n)+16*u;rho=176*(2*entry+entry*entry)+64*gamma(176)
    return data,env,rho,pins


def evaluate():
    data,envelopes,rho,pins=old_data();rows=[]
    for offset in OFFSETS:
        for W in WIDTHS:
            rows.append(dict(reference_kind='own_Fermi_plus_common_offset',common_offset_eV=offset,**response(data,W,{m:offset for m in data},envelopes,rho)))
    anchors={m:float(np.mean(data[m]['Gamma8']['energy_relative_Fermi_eV'][np.argsort(data[m]['Gamma8']['weights'])[-4:]])) for m in data}
    for W in WIDTHS:rows.append(dict(reference_kind='own_dominant_Gamma8_quartet',common_offset_eV=None,**response(data,W,anchors,envelopes,rho)))
    primary=next(r for r in rows if r['W_eV']==2 and r['common_offset_eV']==0)
    prior=json.loads((OLD/'numerical_result.json').read_text())
    assert abs(primary['delta_eV']-prior['delta_Gaussian_ordering_eV'])<1e-14
    # Actual global energy-origin change at fixed physical reference cancels.
    shifted={m:{l:dict(v,energy_relative_Fermi_eV=v['energy_relative_Fermi_eV']+3.14159) for l,v in branches.items()} for m,branches in data.items()}
    gauge=response(shifted,2,{m:3.14159 for m in data},envelopes,rho)
    assert abs(gauge['delta_eV']-primary['delta_eV'])<1e-14
    result=dict(status='CALCULATED retained native complex spectral-probe sensitivity; conditional positive-tail/projector/IEEE bounds',parent='b776a9e',widths_eV=WIDTHS,reference_offsets_eV=OFFSETS,rows=rows,
        primary_W2_Fermi_delta_eV=primary['delta_eV'],delta_min_eV=min(r['delta_eV'] for r in rows),delta_max_eV=max(r['delta_eV'] for r in rows),
        union_conditional_interval_eV=[min(r['conditional_interval_eV'][0] for r in rows),max(r['conditional_interval_eV'][1] for r in rows)],
        all_conditional_intervals_positive=all(r['conditional_interval_eV'][0]>0 for r in rows),minimum_mass=min(b['mass'] for r in rows for m in r['members'].values() for b in m['branches'].values()),
        Gamma8_anchor_offsets_from_own_Fermi_eV=anchors,gauge_check_delta_error_eV=abs(gauge['delta_eV']-primary['delta_eV']),
        physical_material_or_k_grid_error=False,new_native_job=False,physical_xc=None,
        source_sha256={**pins,str(Path(__file__)):sha(__file__),str(HERE/'preregistration.md'):sha(HERE/'preregistration.md')})
    (HERE/'width_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    with (HERE/'width_curve.csv').open('w') as f:
        f.write('reference_kind,common_offset_eV,W_eV,delta_eV,conditional_bound_eV,lower_eV,upper_eV\n')
        for r in rows:f.write(','.join(map(str,[r['reference_kind'],r['common_offset_eV'],r['W_eV'],r['delta_eV'],r['conditional_bound_eV'],*r['conditional_interval_eV']]))+'\n')
    print(json.dumps({k:result[k] for k in ['delta_min_eV','delta_max_eV','union_conditional_interval_eV','all_conditional_intervals_positive','minimum_mass','Gamma8_anchor_offsets_from_own_Fermi_eV']},indent=2))
    for r in rows:
        if r['common_offset_eV']==0:print('Fermi',r['W_eV'],r['delta_eV'],r['conditional_bound_eV'])
    return result


if __name__=='__main__':
    if (HERE/'width_result.json').exists():raise FileExistsError('retain original analysis evidence')
    evaluate()
