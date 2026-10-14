"""Actual cutoff comparison with an explicit physical PW isometry."""
from pathlib import Path
import sys
import json
import importlib.util
import h5py
import numpy as np

HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'chemical_uncertainty_2026-10-14'
sys.path.insert(0,str(PREV))
import width_curve as curves
spec=importlib.util.spec_from_file_location('previous_grid',PREV/'analyze_grid.py');previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
old=previous.old
from embedding import embed_same_cell
from mct_dft.qe_wavefunctions import cross_spinor_overlap,read_spinors
PAIR=previous.DFT/'.local/qe75_lowram_20261011/chemical_pbe8_k2_e50_20261014'


def Bmatrix(path):
    with h5py.File(path) as f:return np.array([f['MillerIndices'].attrs['bg'+str(i)] for i in [1,2,3]])


def base_data():
    data={m:{} for m in ['host','cd']};ov=np.load(PREV/'k2_complex_overlaps.npz');pins={}
    for m in data:
        for label,d in [('Gamma6',2),('Gamma8',4)]:
            p=PREV/(m+'_'+label+'_k2_spectrum.csv');v=np.loadtxt(p,delimiter=',',skiprows=1);w=np.sum(abs(ov[m+'_'+label])**2,axis=0)/d
            np.testing.assert_allclose(v[:,2],w,rtol=0,atol=2e-16)
            data[m][label]=dict(weights=w,energy_relative_Fermi_eV=v[:,1]);pins[str(p)]=old.sha(p)
    for p in [PREV/'grid_result.json',PREV/'k2_complex_overlaps.npz']:pins[str(p)]=old.sha(p)
    return data,pins


def rounding_budget(ng):
    entry=4*old.gamma(32*2*ng)+16*2.**-53
    return 176*(2*entry+entry*entry)+64*old.gamma(176)


def anchor(data):
    return {m:float(np.mean(v['Gamma8']['energy_relative_Fermi_eV'][np.argsort(v['Gamma8']['weights'])[-4:]])) for m,v in data.items()}


def evaluate():
    prior=json.loads((previous.OLD/'numerical_result.json').read_text());baseline=json.loads((PREV/'grid_result.json').read_text())
    c0,g0,k0,e0,ef0,info0=old.intake('host');source=old.PAIR/'host/out/r07pbe.save/wfc1.hdf5';B0=Bmatrix(source)
    oldframes={l:c0[np.array(prior['host_sector_selection'][l]['native_host_bands_1based'])-1] for l in ['Gamma6','Gamma8']}
    data40,pins=base_data();epsilon={l:prior['host_sector_symmetry'][l]['nearby_invariant_projector_distance_upper_model'] for l in oldframes}
    # Reuse independently verified native all-k/Gamma intake with NEW root.
    previous.PAIR=PAIR;data={};native={};members={};overlaps={};transport={};checks={};frames50={}
    from xml.etree import ElementTree as ET
    origin0=ET.parse(source.parent/'data-file-schema.xml').find('.//output/atomic_structure/atomic_positions')
    positions0=np.array([np.fromstring(v.text,sep=' ') for v in origin0])
    for m in ['host','cd']:
        c,g,k,e,ef,info=previous.read_member(m);wave=PAIR/m/f'out/r07pbe.save/wfc{info["Gamma_index_1based"]}.hdf5';B=Bmatrix(wave)
        t=ET.parse(wave.parent/'data-file-schema.xml');pos=np.array([np.fromstring(v.text,sep=' ') for v in t.find('.//output/atomic_structure/atomic_positions')])
        assert np.max(abs(pos-positions0))<1e-12 and info['lattice_bohr']==info0['lattice_bohr']
        cuts=[float(t.findtext('.//output/basis_set/'+tag))*2 for tag in ['ecutwfc','ecutrho']];assert cuts==[50.,200.]
        info['actual_cutoffs_Ry']=cuts;members[m]=info;native[m]=(c,g,k,e,ef,B);data[m]={};transport[m]={}
        for l,frame in oldframes.items():
            embedded,index,proof=embed_same_cell(frame,g0,k0,B0,g,k,B);transport[m][l]=proof
            ov=cross_spinor_overlap(embedded,g,k,c,g,k);overlaps[m+'_'+l]=ov
            w=np.sum(abs(ov)**2,axis=0)/len(frame);data[m][l]=dict(weights=w,energy_relative_Fermi_eV=e-ef)
            np.savetxt(HERE/(m+'_'+l+'_e50_spectrum.csv'),np.column_stack([np.arange(1,177),e-ef,w]),delimiter=',',header='band_1based,energy_minus_Fermi_eV,original_frame_isometrically_embedded_trace_weight_div_rank',comments='',fmt=['%d','%.17g','%.17g'])
            if m=='host':
                # Full native50Ry host frame, NOT restricted/normalized back.
                selected=np.sort(np.argsort(w)[-len(frame):]);f=c[selected];s=old.td_check(f,g)
                expected=[1,0,0] if l=='Gamma6' else [0,0,1]
                assert s['nearest_integer_classification_admitted_under_model'] and s['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==expected
                mask=np.all(g%2==0,axis=1)|np.all(g%2==1,axis=1);prob=np.sum(abs(f[:,:,mask])**2,axis=(1,2));assert min(prob)>1-1e-8
                high=np.ones(len(g),bool);high[index]=False;sv=np.linalg.svd(ov[:,selected],compute_uv=False)
                checks[l]=dict(native_bands_1based=(selected+1).tolist(),native_energies_eV=e[selected].tolist(),primitive_Gamma_probabilities=prob.tolist(),Td_check=s,
                    original40_to_native50_overlap_singular_values=sv.tolist(),principal_projector_distance=float(np.sqrt(max(0,1-float(min(sv))**2))),
                    native50_highG_probability_outside40_by_state=np.sum(abs(f[:,:,high])**2,axis=(1,2)).tolist(),
                    primary_original_frame_replaced=False)
                frames50[l]=f
    gh=native['host'][1];kh=native['host'][2];B50=native['host'][5]
    # Independently check label intertwining for all24 Td operations.
    lookup={tuple(v):i for i,v in enumerate(gh)};_,mapping,_=embed_same_cell(oldframes['Gamma6'],g0,k0,B0,gh,kh,B50)
    ilookup={tuple(v):i for i,v in enumerate(g0)}
    for op in old.td_operations():
        rotation=op['spatial'].T
        srcperm=np.array([ilookup[tuple(v)] for v in (g0@rotation).astype(int)])
        targetperm=np.array([lookup[tuple(v)] for v in (gh@rotation).astype(int)])
        assert np.array_equal(targetperm[mapping],mapping[srcperm])
    rho40=rounding_budget(len(g0));rho50=rounding_budget(len(gh));a50=anchor(data);a40=anchor(data40);rows=[]
    for recipe,newrefs,oldrefs in [('own_Fermi',{m:0. for m in data},{m:0. for m in data40}),('own_dominant_Gamma8_quartet',a50,a40)]:
        for W in curves.WIDTHS:
            new=curves.response(data,W,newrefs,epsilon,rho50);before=curves.response(data40,W,oldrefs,epsilon,rho40)
            d=new['delta_eV']-before['delta_eV'];rad=new['conditional_bound_eV']+before['conditional_bound_eV']
            rows.append(dict(reference_kind=recipe,W_eV=W,cutoff50=new,baseline40=before,cutoff_change_eV=d,conditional_difference_interval_eV=[d-rad,d+rad]))
    secondary={m:{} for m in native}
    for m,(c,g,k,e,ef,B) in native.items():
        for l,f in frames50.items():
            ov=cross_spinor_overlap(f,gh,kh,c,g,k);secondary[m][l]=dict(weights=np.sum(abs(ov)**2,axis=0)/len(f),energy_relative_Fermi_eV=e-ef)
    env50={l:checks[l]['Td_check']['nearby_invariant_projector_distance_upper_model'] for l in frames50};secanchor=anchor(secondary);frame_choice=[]
    for recipe,refs in [('own_Fermi',{m:0. for m in secondary}),('own_dominant_Gamma8_quartet',secanchor)]:
        sec=curves.response(secondary,2,refs,env50,rho50);primary=next(r for r in rows if r['W_eV']==2 and r['reference_kind']==recipe)
        baseframe=next(r for r in baseline['secondary_frame_choice_checks'] if r['reference_kind']==recipe)
        frame_choice.append(dict(reference_kind=recipe,new_native50_host_frame=sec,fixed_original40_embedded=primary['cutoff50'],
            frame_choice_effect_at50_eV=sec['delta_eV']-primary['cutoff50']['delta_eV'],frame_choice_effect_at40_eV=baseframe['frame_choice_effect_on_new_pair_eV'],
            following_host_frame_cutoff_change_eV=sec['delta_eV']-baseframe['secondary_newhost_frame']['delta_eV']))
    # Native40K2 vs native50 host principal angles, with a second EXACT embed.
    previous.PAIR=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/chemical_pbe8_k2_20261014')
    cb,gb,kb,eb,efb,ib=previous.read_member('host');Bb=Bmatrix(previous.PAIR/'host/out/r07pbe.save/wfc1.hdf5')
    for l in frames50:
        ix=np.array(baseline['newhost_physical_frame_checks'][l]['new_host_native_bands_1based'])-1
        fb=cb[ix];bf,_,p=embed_same_cell(fb,gb,kb,Bb,gh,kh,B50)
        sv=np.linalg.svd(cross_spinor_overlap(bf,gh,kh,frames50[l],gh,kh),compute_uv=False)
        checks[l]['native40K2_to_native50_host_overlap_singular_values']=sv.tolist()
        checks[l]['native40K2_to_native50_host_projector_distance']=float(np.sqrt(max(0,1-float(min(sv))**2)))
    W2=next(r for r in rows if r['reference_kind']=='own_Fermi' and r['W_eV']==2)
    result=dict(status='CALCULATED ONE matched native50/200Ry cutoff test; conditional spectral bounds, no full convergence/material claim',parent='31e872e',baseline_cutoffs_Ry=[40,160],new_cutoffs_Ry=[50,200],
        members=members,physical_transport=transport,Td_isometry_all24_intertwining_pass=True,host_frame_checks=checks,rows=rows,secondary_frame_choice_checks=frame_choice,
        baseline_reference_offsets_eV=a40,new_reference_offsets_eV=a50,poor_for_few_meV_goal_by_preregistered_10meV_change=abs(W2['cutoff_change_eV'])>.01,
        full_cutoff_or_BZ_convergence_claim=False,material_error_bar=False,physical_xc=None,HSE_launched=False,
        source_sha256={**pins,str(source):old.sha(source),str(HERE/'analyze_cutoff.py'):old.sha(__file__),str(HERE/'embedding.py'):old.sha(HERE/'embedding.py'),str(HERE/'preregistration.md'):old.sha(HERE/'preregistration.md')})
    np.savez(HERE/'e50_complex_overlaps.npz',**overlaps);(HERE/'cutoff_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for r in rows:
        if r['reference_kind']=='own_Fermi':print(json.dumps(dict(W=r['W_eV'],response40=r['baseline40']['delta_eV'],response50=r['cutoff50']['delta_eV'],change=r['cutoff_change_eV'],interval=r['conditional_difference_interval_eV'])))
    print('FRAME CHOICE',json.dumps(frame_choice,indent=2));return result


if __name__=='__main__':
    if (HERE/'cutoff_result.json').exists():raise FileExistsError('preserve measured result')
    evaluate()
