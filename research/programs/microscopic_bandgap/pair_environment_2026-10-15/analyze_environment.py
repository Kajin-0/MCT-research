"""Actual same-composition complex projected spectra; no fitted alloy law."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json,sys
import numpy as np
import owner as r
from environment_science import reference,read_spinors,cross_spinor_overlap,EV_HA,original

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'chemical_pbe16_p2_2026-10-15'))
from analyze_pair import scalar_inverse,matrix_inverse
sys.path.insert(0,str(HERE.parent/'chemical_uncertainty_2026-10-14'))
from width_curve import bounded_centroid,WIDTHS


def evaluate():
    if (HERE/'numerical_result.json').exists():raise FileExistsError('immutable original numerical result')
    fs,g0,k0,ref=reference();epsilon={l:ref['science']['host_checks'][l]['Td']['nearby_invariant_projector_distance_upper_model'] for l in fs}
    states={};finals={};overlaps={};checks={};rounds={};spectra={};summary={}
    for m in ['unshared','shared']:
        root=r.PAIR/m;f=json.loads((root/'FINAL.json').read_text());assert f['accepted'] and f['terminal_pass']
        for p,pin in f['source_hashes'].items():assert r.sha(p)==pin
        t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml');e=np.fromstring(t.findtext('.//output/band_structure/ks_energies/eigenvalues'),sep=' ')*EV_HA;ef=float(t.findtext('.//output/band_structure/fermi_energy'))*EV_HA
        c,g,k=read_spinors(root/'out/r07pbe.save/wfc1.hdf5');entry=4*original.gamma(32*2*len(g))+16*2.**-53;rho=352*(2*entry+entry*entry)+64*original.gamma(352);rounds[m]=rho
        states[m]=dict(e=e,ef=ef,C=[],weights={});finals[m]=f;summary[m]={}
        for l,P in fs.items():
            C=cross_spinor_overlap(P,g0,k0,c,g,k);w=np.sum(abs(C)**2,axis=0)/len(P);assert sum(w)<=1+rho
            states[m]['C'].append(C);states[m]['weights'][l]=w;overlaps[m+'_'+l]=C
            path=HERE/(m+'_'+l+'_spectrum.csv');np.savetxt(path,np.column_stack((np.arange(1,353),e,e-ef,w)),delimiter=',',header='band_1based,QE_energy_eV,energy_minus_own_Fermi_eV,fixed_native50_host_weight_div_dimension',comments='',fmt=['%d','%.17g','%.17g','%.17g']);spectra[str(path)]=r.sha(path)
            # Independent invariances act on physical G labels and projector basis.
            alt=cross_spinor_overlap(P[:,:,::-1],g0[::-1],k0,c[:,:,::-1],g[::-1],k)
            checks[m+'_'+l+'_physical_G_permutation']=float(np.max(abs(C-alt)))
            U=np.linalg.qr(np.array([[complex(i+j+1,i-j) for j in range(len(P))] for i in range(len(P))])+np.eye(len(P)))[0]
            alt=cross_spinor_overlap(np.einsum('ij,jsg->isg',U,P),g0,k0,c,g,k)
            checks[m+'_'+l+'_projector_unitary_weight']=float(max(abs(w-np.sum(abs(alt)**2,axis=0)/len(P))))
            selected=np.sort(np.argsort(w)[-len(P):]);summary[m][l]=dict(retained_probability=float(sum(w)),omitted_probability=max(0.,1-float(sum(w))),largest_dimension_count_bands_1based=(selected+1).tolist(),selected_energies_minus_own_Fermi_eV=(e[selected]-ef).tolist(),selected_normalized_weight=float(sum(w[selected])),selected_spread_eV=float(np.ptp(e[selected])))
    assert max(checks.values())<1e-12
    rho=max(rounds.values());rows=[]
    # Own EF is primary. A common +/-0.5eV probe displacement is only probe
    # sensitivity, not an invented alignment or error bar on material physics.
    for shift in [-.5,0.,.5]:
        for W in WIDTHS:
            per={}
            for m,s in states.items():
                b={l:bounded_centroid(w,s['e']-s['ef']-shift,W,epsilon[l],rho) for l,w in s['weights'].items()}
                per[m]=dict(branches=b,ordering_eV=b['Gamma6']['centroid_relative_reference_eV']-b['Gamma8']['centroid_relative_reference_eV'])
            delta=per['shared']['ordering_eV']-per['unshared']['ordering_eV'];bound=sum(v['conditional_total_eV'] for mm in per.values() for v in mm['branches'].values())
            rows.append(dict(W_eV=W,common_displacement_from_own_Fermi_eV=shift,delta_shared_minus_unshared_eV=delta,conditional_bound_eV=bound,conditional_interval_eV=[delta-bound,delta+bound],members=per))
    scalar=[];matrix=[]
    for eta in [.025,.05,.1]:
        sm={m:{l:scalar_inverse(w,s['e']-s['ef'],eta,epsilon[l],rho) for l,w in s['weights'].items()} for m,s in states.items()}
        order={m:b['Gamma8']['inverse'][0]-b['Gamma6']['inverse'][0] for m,b in sm.items()};delta=order['shared']-order['unshared'];bound=sum(v['inverse_error_bound_eV'] for b in sm.values() for v in b.values())
        scalar.append(dict(eta_eV=eta,ordering_eV=order,delta_eV=delta,conditional_bound_eV=bound,conditional_interval_eV=[delta-bound,delta+bound],members=sm))
        mm={m:matrix_inverse(np.vstack(s['C']),s['e']-s['ef'],eta,rho) for m,s in states.items()};delta=mm['shared']['ordering_eV']-mm['unshared']['ordering_eV'];bound=sum(v['fixed_frame_ordering_error_bound_eV'] for v in mm.values())
        matrix.append(dict(eta_eV=eta,delta_eV=delta,fixed_frame_conditional_bound_eV=bound,fixed_frame_conditional_interval_eV=[delta-bound,delta+bound],members=mm))
    # Same composition and cell: total-energy difference is meaningful in the
    # same PP convention. QE etot includes demet=-T*S, not a zero-T pair binding.
    energy={m:dict(etot_Ry=f['science']['total_energy_Ry'],demet_Ry=float(ET.parse(r.PAIR/m/'out/r07pbe.save/data-file-schema.xml').findtext('.//output/total_energy/demet'))*2) for m,f in finals.items()}
    deltaF=(energy['shared']['etot_Ry']-energy['unshared']['etot_Ry'])*EV_HA/2
    deltaE=deltaF-(energy['shared']['demet_Ry']-energy['unshared']['demet_Ry'])*EV_HA/2
    primary=next(a for a in rows if a['W_eV']==2 and a['common_displacement_from_own_Fermi_eV']==0)
    np.savez(HERE/'complex_overlaps.npz',**overlaps)
    result=dict(status='CALCULATED native PBE ordered same-composition environment contrast',parent='892079f',x=.25,reference='accepted16atom50Ry host native Gamma6/8 fixed before acquisitions',members=finals,Gaussian_rows=rows,scalar_causal_rows=scalar,matrix_causal_rows=matrix,weight_redistribution=summary,actual_complex_checks=checks,IEEE_weight_budgets=rounds,nearby_frame_distance_upper_model=epsilon,primary_W2_eV=primary['delta_shared_minus_unshared_eV'],primary_conditional_interval_eV=primary['conditional_interval_eV'],native_total_energy=energy,delta_shared_minus_unshared_free_energy_eV_cell=deltaF,delta_shared_minus_unshared_internal_energy_eV_cell=deltaE,not_isolated_pair_binding=True,not_N2_operator_extraction=True,N3_undetermined=True,absolute_QE_energy_alignment_NOT_used=True,not_a_gap=True,not_HSE=True,not_material_error_bar=True,physical_xc=None,unquantified_errors=['PBE functional and quasiparticle self-energy','periodic pair geometry, Gamma sampling and finite size','ionic relaxation/zero point','native eigenpair-residual operator bound absent','FD regulator'],source_hashes={str(p):r.sha(p) for p in [Path(__file__),HERE/'frozen_protocol.json',HERE/'geometry_result.json',HERE.parent/'chemical_pbe16_p2_2026-10-15/analyze_pair.py',HERE.parent/'chemical_uncertainty_2026-10-14/width_curve.py']},spectra_sha256=spectra)
    (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ['primary_W2_eV','primary_conditional_interval_eV','delta_shared_minus_unshared_free_energy_eV_cell','delta_shared_minus_unshared_internal_energy_eV_cell']},indent=2))
    for a in rows:
        if a['common_displacement_from_own_Fermi_eV']==0:print('Gaussian',a['W_eV'],a['delta_shared_minus_unshared_eV'],a['conditional_interval_eV'])
    for a in scalar:print('Causal scalar',a['eta_eV'],a['delta_eV'],a['conditional_interval_eV'])
    for a in matrix:print('Causal matrix',a['eta_eV'],a['delta_eV'],a['fixed_frame_conditional_interval_eV'])


if __name__=='__main__':evaluate()
