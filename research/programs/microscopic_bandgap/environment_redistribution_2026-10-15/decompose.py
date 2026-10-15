"""Exact retained-measure decomposition; post-acquisition diagnostic only."""
from pathlib import Path
import hashlib,json,sys
import numpy as np

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
OLD=BASE/'pair_environment_2026-10-15'
sys.path.insert(0,str(BASE/'chemical_pbe16_p2_2026-10-15'))
from analyze_pair import scalar_inverse


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if (HERE/'result.json').exists():raise FileExistsError('preserve original decomposition')
    old=json.loads((OLD/'numerical_result.json').read_text());over=np.load(OLD/'complex_overlaps.npz');data={};rows={};errors=[]
    for m in ['unshared','shared']:
        data[m]={};rows[m]={}
        for l,d in [('Gamma6',2),('Gamma8',4)]:
            v=np.loadtxt(OLD/(m+'_'+l+'_spectrum.csv'),delimiter=',',skiprows=1);e=v[:,2];w=np.sum(abs(over[m+'_'+l])**2,axis=0)/d
            assert np.max(abs(w-v[:,3]))<1e-15
            ix=np.array(old['weight_redistribution'][m][l]['largest_dimension_count_bands_1based'])-1;take=np.zeros(352,bool);take[ix]=True
            phi=np.exp(-e*e/8);M=w@phi;N=w@(e*phi);Md=w[take]@phi[take];Nd=w[take]@(e[take]*phi[take]);Mr=w[~take]@phi[~take];Nr=w[~take]@(e[~take]*phi[~take]);cd=Nd/Md;c=N/M;shift=(Nr-cd*Mr)/(Md+Mr)
            z=.05j;g=sum(w/(z-e));gd=sum(w[take]/(z-e[take]));gr=sum(w[~take]/(z-e[~take]));invshift=-gr/(gd*g)
            errors += [abs(c-cd-shift),abs((1/g-1/gd)-invshift)]
            rows[m][l]=dict(selected_bands_1based=(ix+1).tolist(),selected_measure_mass=float(sum(w[take])),rest_retained_measure_mass=float(sum(w[~take])),Gaussian_full_eV=float(c),Gaussian_selected_only_eV=float(cd),Gaussian_rest_correction_eV=float(shift),inverse_real_full_eV=float((1/g).real),inverse_real_selected_only_eV=float((1/gd).real),inverse_real_rest_correction_eV=float(invshift.real),not_complete_selected_measure=True,shared_split_energies_not_averaged=True)
            data[m][l]=(w,e)
    gaussian={};inverse={}
    for m,b in rows.items():
        gaussian[m]={key:b['Gamma6'][key]-b['Gamma8'][key] for key in ['Gaussian_full_eV','Gaussian_selected_only_eV','Gaussian_rest_correction_eV']}
        inverse[m]={key:b['Gamma8'][key]-b['Gamma6'][key] for key in ['inverse_real_full_eV','inverse_real_selected_only_eV','inverse_real_rest_correction_eV']}
    dg={k:gaussian['shared'][k]-gaussian['unshared'][k] for k in gaussian['shared']};di={k:inverse['shared'][k]-inverse['unshared'][k] for k in inverse['shared']}
    errors += [abs(dg['Gaussian_full_eV']-old['primary_W2_eV']),abs(di['inverse_real_full_eV']-next(r for r in old['scalar_causal_rows'] if r['eta_eV']==.05)['delta_eV'])]
    assert max(errors)<1e-12
    centered=[];rho=max(old['IEEE_weight_budgets'].values())
    for t in [-.1,0.,.1]:
        mm={m:{l:scalar_inverse(w,e-t,.05,old['nearby_frame_distance_upper_model'][l],rho) for l,(w,e) in b.items()} for m,b in data.items()}
        order={m:b['Gamma8']['inverse'][0]-b['Gamma6']['inverse'][0] for m,b in mm.items()};delta=order['shared']-order['unshared'];bound=sum(v['inverse_error_bound_eV'] for b in mm.values() for v in b.values());centered.append(dict(center_from_each_own_Fermi_eV=t,eta_eV=.05,delta_eV=delta,conditional_bound_eV=bound,conditional_interval_eV=[delta-bound,delta+bound]))
    result=dict(status='CALCULATED exact post-acquisition decomposition; no new material model',members=rows,Gaussian_contrast_decomposition=dg,scalar_inverse_contrast_decomposition=di,center_sensitivity=centered,max_exact_identity_error_eV=float(max(errors)),new_native_jobs=0,not_a_gap_or_N2operator=True,physical_xc=None,source_sha256={str(p):sha(p) for p in [Path(__file__),HERE/'protocol.md',OLD/'numerical_result.json',OLD/'complex_overlaps.npz',BASE/'chemical_pbe16_p2_2026-10-15/analyze_pair.py']})
    (HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({k:result[k] for k in ['Gaussian_contrast_decomposition','scalar_inverse_contrast_decomposition','center_sensitivity','max_exact_identity_error_eV']},indent=2))


if __name__=='__main__':main()
