"""Matched Gamma spectroscopy at new SCF charge using SAME old host frame."""
from pathlib import Path
import json
import sys
import importlib.util
from xml.etree import ElementTree as ET
import numpy as np
from scipy.special import expit
import width_curve as curves

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'chemical_pbe_pilot_2026-10-14'
DFT=Path('/home/User/opencode_workspace/DFT')
PAIR=DFT/'.local/qe75_lowram_20261011/chemical_pbe8_k2_20261014'
sys.path.insert(0,str(DFT/'src'))
from mct_dft.qe_wavefunctions import read_spinors,cross_spinor_overlap
spec=importlib.util.spec_from_file_location('original_projection',OLD/'analyze.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
EV_HA=27.211386245988


def read_member(member):
    root=PAIR/member;final=json.loads((root/'FINAL.json').read_text())
    if not final['accepted']:raise ValueError('both new science and terminal gates required')
    for name,pin in final['source_hashes'].items():
        if old.sha(name)!=pin:raise ValueError('new native source changed')
    schema=root/'out/r07pbe.save/data-file-schema.xml';t=ET.parse(schema);b=t.find('.//output/band_structure');ks=b.findall('ks_energies')
    weights=np.array([float(v.find('k_point').attrib['weight']) for v in ks]);vec=np.array([np.fromstring(v.findtext('k_point'),sep=' ') for v in ks])
    eig=np.array([np.fromstring(v.findtext('eigenvalues'),sep=' ') for v in ks])*EV_HA
    occ=np.array([np.fromstring(v.findtext('occupations'),sep=' ') for v in ks]);ef=float(b.findtext('fermi_energy'))*EV_HA
    fd=expit((ef-eig)/(EV_HA*.0005));charge=float(np.sum(weights[:,None]*fd))
    assert abs(charge-144)<1e-8 and np.max(abs(fd-occ))<1e-9 and abs(sum(weights)-1)<1e-12
    ix=np.flatnonzero(np.linalg.norm(vec,axis=1)<1e-12);assert len(ix)==1;i=int(ix[0])
    wave=root/f'out/r07pbe.save/wfc{i+1}.hdf5';c,g,k=read_spinors(wave)
    assert len(c)==176 and np.linalg.norm(k)<1e-12
    lattice=np.array([np.fromstring(t.findtext('.//output/atomic_structure/cell/a'+str(j)),sep=' ') for j in [1,2,3]])
    assert np.max(abs(lattice-np.eye(3)*lattice[0,0]))<1e-10
    flat=c.reshape(176,-1);gram=float(np.linalg.norm(flat.conj()@flat.T-np.eye(176),2));assert gram<1e-8
    fields=dict(accepted=True,Gamma_index_1based=i+1,k_weights=weights.tolist(),k_XML_vectors=vec.tolist(),fermi_eV=ef,charge_residual_e=charge-144,
        occupation_max_error=float(np.max(abs(fd-occ))),all176_Gamma_Gram_defect_op=gram,native_Gamma_PW=len(g),
        lattice_bohr=lattice.tolist(),scf_iterations=int(t.findtext('.//output/convergence_info/scf_conv/n_scf_steps')),
        scf_error_Ry=float(t.findtext('.//output/convergence_info/scf_conv/scf_error'))*2,total_energy_Ry=float(t.findtext('.//output/total_energy/etot'))*2,
        source_hashes=final['source_hashes'],guard=final['guard'])
    return c,g,k,eig[i],ef,fields


def evaluate():
    prior=json.loads((OLD/'numerical_result.json').read_text());old_source=old.intake('host');oc,og,ok,oe,oef,oinfo=old_source
    frames={label:oc[np.array(prior['host_sector_selection'][label]['native_host_bands_1based'])-1] for label in ['Gamma6','Gamma8']}
    old_data,envelopes,rho,oldpins=curves.old_data();data={};overlaps={};members={};newframe_checks={};native={};newframes={}
    for member in ['host','cd']:
        c,g,k,e,ef,info=read_member(member);members[member]=info;data[member]={};native[member]=(c,g,k,e,ef)
        assert info['lattice_bohr']==oinfo['lattice_bohr']
        for label,frame in frames.items():
            ov=cross_spinor_overlap(frame,og,ok,c,g,k);overlaps[member+'_'+label]=ov
            w=np.sum(abs(ov)**2,axis=0)/len(frame);data[member][label]=dict(weights=w,energy_relative_Fermi_eV=e-ef)
            np.savetxt(HERE/(member+'_'+label+'_k2_spectrum.csv'),np.column_stack([np.arange(1,177),e-ef,w]),delimiter=',',header='band_1based,energy_minus_Fermi_eV,fixed_original_host_sector_weight_div_rank',comments='',fmt=['%d','%.17g','%.17g'])
            if member=='host':
                selected=np.sort(np.argsort(w)[-len(frame):]);nf=c[selected];s=old.td_check(nf,g)
                newframes[label]=nf
                expected=[1,0,0] if label=='Gamma6' else [0,0,1]
                assert s['nearest_integer_classification_admitted_under_model'] and s['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==expected
                mask=np.all(g%2==0,axis=1)|np.all(g%2==1,axis=1)
                trans=np.sum(abs(nf[:,:,mask])**2,axis=(1,2));assert np.min(trans)>1-1e-8
                sv=np.linalg.svd(ov[:,selected],compute_uv=False)
                newframe_checks[label]=dict(new_host_native_bands_1based=(selected+1).tolist(),new_host_eigenenergies_eV=e[selected].tolist(),primitive_Gamma_probabilities=trans.tolist(),physical_Td_check=s,
                    original_to_newhost_frame_principal_overlap_singular_values=sv.tolist(),projector_distance_comparison=float(np.sqrt(max(0,1-float(min(sv))**2))),
                    original_frame_replaced_in_primary_observable=False)
    anchors={m:float(np.mean(data[m]['Gamma8']['energy_relative_Fermi_eV'][np.argsort(data[m]['Gamma8']['weights'])[-4:]])) for m in data}
    oldanchors={m:float(np.mean(old_data[m]['Gamma8']['energy_relative_Fermi_eV'][np.argsort(old_data[m]['Gamma8']['weights'])[-4:]])) for m in old_data}
    rows=[]
    for kind,offsets,old_offsets in [('own_Fermi',{m:0. for m in data},{m:0. for m in data}),('own_dominant_Gamma8_quartet',anchors,oldanchors)]:
        for W in curves.WIDTHS:
            current=curves.response(data,W,offsets,envelopes,rho);original=curves.response(old_data,W,old_offsets,envelopes,rho)
            d=current['delta_eV']-original['delta_eV'];error=current['conditional_bound_eV']+original['conditional_bound_eV']
            rows.append(dict(reference_kind=kind,W_eV=W,new=current,original=original,k_grid_change_eV=d,conditional_grid_difference_interval_eV=[d-error,d+error]))
    # Separately labelled optional frame-choice check. NEVER replaces the
    # frozen original frame in the primary k-refinement comparison.
    secondary={m:{} for m in native}
    gh=native['host'][1];kh=native['host'][2]
    for m,(c,g,k,e,ef) in native.items():
        for l,frame in newframes.items():
            ov=cross_spinor_overlap(frame,gh,kh,c,g,k)
            secondary[m][l]=dict(weights=np.sum(abs(ov)**2,axis=0)/len(frame),energy_relative_Fermi_eV=e-ef)
    second_env={l:newframe_checks[l]['physical_Td_check']['nearby_invariant_projector_distance_upper_model'] for l in newframes}
    second_anchor={m:float(np.mean(secondary[m]['Gamma8']['energy_relative_Fermi_eV'][np.argsort(secondary[m]['Gamma8']['weights'])[-4:]])) for m in secondary}
    frame_choice=[]
    for kind,offsets in [('own_Fermi',{m:0. for m in secondary}),('own_dominant_Gamma8_quartet',second_anchor)]:
        obs=curves.response(secondary,2,offsets,second_env,rho)
        primary=next(r['new'] for r in rows if r['W_eV']==2 and r['reference_kind']==kind)
        frame_choice.append(dict(reference_kind=kind,secondary_newhost_frame=obs,primary_fixed_old_frame=primary,
            frame_choice_effect_on_new_pair_eV=obs['delta_eV']-primary['delta_eV']))
    result=dict(status='CALCULATED one matched native k-refinement, same fixed physical host projectors; conditional bounds, NOT BZ convergence',parent='b776a9e',original_grid=[1,1,1],refined_grid=[2,2,2],
        members=members,newhost_physical_frame_checks=newframe_checks,Gamma8_reference_offsets_from_own_Fermi_eV=anchors,rows=rows,
        original_reference_offsets_from_own_Fermi_eV=oldanchors,secondary_frame_choice_checks=frame_choice,
        physical_BZ_convergence_claim=False,material_error_bar=False,original_host_terminal_uncertainty_preserved=True,physical_xc=None,
        source_sha256={**oldpins,str(HERE/'analyze_grid.py'):old.sha(__file__),str(HERE/'width_curve.py'):old.sha(HERE/'width_curve.py'),str(HERE/'preregistration.md'):old.sha(HERE/'preregistration.md'),str(OLD/'analyze.py'):old.sha(OLD/'analyze.py')})
    np.savez(HERE/'k2_complex_overlaps.npz',**overlaps)
    (HERE/'grid_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for row in rows:
        if row['W_eV']==2:print(json.dumps(dict(recipe=row['reference_kind'],old_delta=row['original']['delta_eV'],new_delta=row['new']['delta_eV'],k_grid_change=row['k_grid_change_eV'],interval=row['conditional_grid_difference_interval_eV']),indent=2))
    print('Gamma8 reference offsets relativeEF',anchors)
    return result


if __name__=='__main__':
    if (HERE/'grid_result.json').exists():raise FileExistsError('retain original new result')
    evaluate()
