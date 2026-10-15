"""Actual retained PBE causal contractions and positive-tail inverse bounds."""
import hashlib
import json
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
DATA=HERE.parent/'chemical_k3_2026-10-14'
EPS_SOURCE=HERE.parent/'chemical_pbe_pilot_2026-10-14/numerical_result.json'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    prior=json.loads(EPS_SOURCE.read_text())
    epsilon={a:prior['host_sector_symmetry'][a]['nearby_invariant_projector_distance_upper_model'] for a in ['Gamma6','Gamma8']}
    overlap=np.load(DATA/'k3_complex_overlaps.npz')
    u=2.**-53; gamma=lambda n:n*u/(1-n*u)
    entry=4*gamma(32*21654)+16*u
    b=176*(2*entry+entry*entry)+64*gamma(176)
    raw={};pins={}
    for m in ['host','cd']:
        for a,d in [('Gamma6',2),('Gamma8',4)]:
            p=DATA/(m+'_'+a+'_k3_spectrum.csv');v=np.loadtxt(p,delimiter=',',skiprows=1)
            O=overlap[m+'_'+a];assert O.shape==(d,176)
            w=np.sum(abs(O)**2,axis=0)/d
            np.testing.assert_allclose(v[:,2],w,rtol=0,atol=2e-16)
            raw[m,a]=(v[:,1],w,O);pins[str(p)]=sha(p)
    rows=[]
    for t in [-.05,0.,.05]:
        for eta in [.025,.05,.1]:
            items={};order={};radii={}
            for m in ['host','cd']:
                items[m]={}
                for a in ['Gamma6','Gamma8']:
                    e,w,O=raw[m,a];z=t+1j*eta
                    g=np.sum(w/(z-e))
                    matrix=(O/(z-e)[None,:])@O.conj().T
                    independent=np.trace(matrix)/len(O)
                    assert abs(g-independent)<1e-13 and g.imag<0
                    assert abs(np.sum(w/((z+.375)-(e+.375)))-g)<1e-12
                    r=max(0.,1-float(sum(w)))
                    delta=(r+2*epsilon[a]+b)/eta
                    safe=bool(delta<abs(g))
                    radius=float(delta/(abs(g)*(abs(g)-delta))) if safe else None
                    items[m][a]=dict(g_inverse_eV=[float((1/g).real),float((1/g).imag)],
                        g_eV_inverse=[float(g.real),float(g.imag)],retained_probability=float(sum(w)),
                        omitted_probability=r,complex_resolvent_error_upper_eV_inverse=delta,
                        inversion_margin_eV_inverse=float(abs(g)-delta),inverse_error_upper_eV=radius,
                        certified_under_tail_frame_IEEE_model=safe)
                order[m]=items[m]['Gamma8']['g_inverse_eV'][0]-items[m]['Gamma6']['g_inverse_eV'][0]
                rs=[items[m][a]['inverse_error_upper_eV'] for a in ['Gamma6','Gamma8']]
                radii[m]=sum(rs) if all(v is not None for v in rs) else None
            response=order['cd']-order['host']
            radius=sum(radii.values()) if all(v is not None for v in radii.values()) else None
            interval=[response-radius,response+radius] if radius is not None else None
            rows.append(dict(t_relative_own_Fermi_eV=t,eta_eV=eta,member=items,
                host_ordering_functional_eV=order['host'],cd_ordering_functional_eV=order['cd'],
                chemical_response_eV=response,conditional_bound_eV=radius,
                conditional_interval_eV=interval,positive_response_certified=bool(interval and interval[0]>0)))
            print(t,eta,response,interval,flush=True)
    # Independent single-pole identity; positivity alone supplies no gap claim.
    z=.05+.1j;E6=-.8;E8=.1
    assert abs((1/(1/(z-E8))-1/(1/(z-E6))).real-(E6-E8))<1e-14
    for p in [DATA/'k3_complex_overlaps.npz',EPS_SOURCE,Path(__file__),HERE/'preregistration.md']:pins[str(p)]=sha(p)
    out=dict(status='CALCULATED actual retained accepted PBE spectra; conditional causal bounds',
        rows=rows,original_frame_error_epsilon=epsilon,weight_L1_rounding_budget=b,
        all_tested_response_signs_certified=all(r['positive_response_certified'] for r in rows),
        source_sha256=pins,new_native_jobs=0,HSE_result=False,
        inverse_resolvent_ordering_is_not_general_signed_gap=True,physical_xc=None,
        conditional_bounds_do_not_include_Hamiltonian_material_or_SCF_eigenpair_errors=True)
    (HERE/'result.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
