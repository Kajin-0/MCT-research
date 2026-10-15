"""Actual PBE16 composition spectra with fixed physical primitive-Gamma frame."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json,sys
import numpy as np
from science import original,frames,read_spinors,cross_spinor_overlap,EV_HA,cell
import cd_owner as r

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'chemical_uncertainty_2026-10-14'))
import width_curve as curves


def read(member):
    if member=='host':
        root=r.HOST;h=json.loads((HERE/'host_readback_v2.json').read_text())
        final=dict(accepted=h['scientific_pass'] and h['terminal']['terminal'],terminal_pass=h['terminal']['terminal'],science=h['science'],guard=h['guard'],source_hashes=h['source_hashes'],readback_scope='correct native reciprocal units v2; original assertion failure preserved')
    else:
        root=r.PAIR/member;final=json.loads((root/'FINAL.json').read_text())
    assert final['accepted'] and final['terminal_pass']
    for path,h in final['source_hashes'].items():assert r.sha(path)==h
    t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml')
    c,g,k=read_spinors(root/'out/r07pbe.save/wfc1.hdf5')
    e=np.fromstring(t.findtext('.//output/band_structure/ks_energies/eigenvalues'),sep=' ')*EV_HA
    ef=float(t.findtext('.//output/band_structure/fermi_energy'))*EV_HA
    fs,transport=frames(g,k,t)
    return c,g,k,e,ef,fs,transport,final


def scalar_inverse(w,e,eta,epsilon,rho):
    z=complex(0,eta);g=np.sum(w/(z-e));tail=max(0.,1-float(sum(w)))
    delta=(tail+2*epsilon+rho)/eta
    if abs(g)<=delta:raise ValueError('inverse scalar resolvent margin failed')
    bound=delta/(abs(g)*(abs(g)-delta))
    return dict(g=[float(g.real),float(g.imag)],inverse=[float((1/g).real),float((1/g).imag)],omitted_probability=tail,delta_g_bound=delta,inverse_error_bound_eV=bound)


def matrix_inverse(C,e,eta,rho):
    z=complex(0,eta);G=(C/(z-e))@C.conj().T
    residue=np.eye(6)-C@C.conj().T
    ev=np.linalg.eigvalsh((residue+residue.conj().T)/2)
    assert min(ev)>-6*rho
    tail=max(0.,float(max(ev)));delta=(tail+6*rho)/eta
    inv=np.linalg.inv(G);a=float(np.linalg.norm(inv,2));margin=1-a*delta
    if margin<=0:raise ValueError('full matrix inversion margin failed')
    H=z*np.eye(6)-inv;h6=np.trace(H[:2,:2])/2;h8=np.trace(H[2:,2:])/4
    error=a*a*delta/margin
    gram=np.linalg.eigvalsh(-(G-G.conj().T)/(2j))
    damping=np.linalg.eigvalsh(-(H-H.conj().T)/(2j))
    assert min(gram)>-1e-12 and min(damping)>-1e-10
    return dict(eta_eV=eta,ordering_eV=float((h6-h8).real),mass_eV=float((h6-h8).real/2),common_eV=float((h6+h8).real/2),fixed_frame_Heff_operator_error_bound_eV=error,fixed_frame_ordering_error_bound_eV=2*error,inversion_margin=margin,omitted_measure_operator_norm=tail,omitted_measure_eigenvalues=ev.tolist(),min_positive_Stieltjes_imag_eigenvalue=float(min(gram)),min_causal_Heff_damping_eigenvalue_eV=float(min(damping)),offdiagonal_6_8_operator_eV=float(np.linalg.norm(H[:2,2:],2)),Gamma6_scalar_block_defect_eV=float(np.linalg.norm(H[:2,:2]-h6*np.eye(2),2)),Gamma8_scalar_block_defect_eV=float(np.linalg.norm(H[2:,2:]-h8*np.eye(4),2)),Heff_real_eV=H.real.tolist(),Heff_imag_eV=H.imag.tolist(),bound_includes_nearby_projector=False)


def evaluate():
    if (HERE/'numerical_result.json').exists():raise FileExistsError('preserve numerical evidence')
    prior=json.loads((original.HERE/'numerical_result.json').read_text())
    epsilon={l:prior['host_sector_symmetry'][l]['nearby_invariant_projector_distance_upper_model'] for l in ['Gamma6','Gamma8']}
    data={};members={};overlaps={};transport={};rounds={};native={};checks={}
    for member in ['host','cd']:
        c,g,k,e,ef,fs,tr,final=read(member);members[member]=final;transport[member]=tr
        entry=4*original.gamma(32*2*len(g))+16*2.**-53
        rho=352*(2*entry+entry*entry)+64*original.gamma(352);rounds[member]=rho
        data[member]={};native[member]=(e-ef,[])
        for l,f in fs.items():
            ov=cross_spinor_overlap(f,g,k,c,g,k);w=np.sum(abs(ov)**2,axis=0)/len(f)
            assert sum(w)<=1+rho
            data[member][l]=dict(weights=w,energy_relative_Fermi_eV=e-ef)
            overlaps[member+'_'+l]=ov;native[member][1].append(ov)
            np.savetxt(HERE/(member+'_'+l+'_spectrum.csv'),np.column_stack((np.arange(1,353),e-ef,w)),delimiter=',',header='band_1based,energy_minus_own_Fermi_eV,fixed_original_Gamma_projector_weight_div_dimension',comments='',fmt=['%d','%.17g','%.17g'])
            u=np.linalg.qr(np.array([[complex(i+j+1,i-j) for j in range(len(f))] for i in range(len(f))])+np.eye(len(f)))[0]
            alternate=cross_spinor_overlap(np.einsum('ij,jsg->isg',u,f),g,k,c,g,k)
            checks[member+'_'+l+'_internal_unitary_weight_error']=float(max(abs(w-np.sum(abs(alternate)**2,axis=0)/len(f))))
            alternate=cross_spinor_overlap(f[:,:,::-1],g[::-1],k,c[:,:,::-1],g[::-1],k)
            checks[member+'_'+l+'_physical_G_reorder_overlap_error']=float(np.max(abs(ov-alternate)))
    assert max(checks.values())<1e-12
    rho=max(rounds.values());rows=[]
    anchors={m:float(np.mean(v['Gamma8']['energy_relative_Fermi_eV'][np.argsort(v['Gamma8']['weights'])[-4:]])) for m,v in data.items()}
    for recipe,offsets in [('own_Fermi',{m:0. for m in data}),('own_dominant_Gamma8_quartet',anchors)]:
        for W in curves.WIDTHS:rows.append(dict(reference_kind=recipe,**curves.response(data,W,offsets,epsilon,rho)))
    scalar=[];matrix=[]
    for eta in [.025,.05,.1]:
        sm={m:{l:scalar_inverse(v['weights'],v['energy_relative_Fermi_eV'],eta,epsilon[l],rho) for l,v in branches.items()} for m,branches in data.items()}
        order={m:sm[m]['Gamma8']['inverse'][0]-sm[m]['Gamma6']['inverse'][0] for m in sm}
        delta=order['cd']-order['host'];bound=sum(v['inverse_error_bound_eV'] for mm in sm.values() for v in mm.values())
        scalar.append(dict(eta_eV=eta,ordering_eV=order,delta_eV=delta,conditional_bound_eV=bound,conditional_interval_eV=[delta-bound,delta+bound],members=sm))
        mm={m:matrix_inverse(np.vstack(C),e,eta,rho) for m,(e,C) in native.items()}
        md=mm['cd']['ordering_eV']-mm['host']['ordering_eV'];mb=sum(v['fixed_frame_ordering_error_bound_eV'] for v in mm.values())
        matrix.append(dict(eta_eV=eta,delta_eV=md,fixed_frame_conditional_bound_eV=mb,fixed_frame_conditional_interval_eV=[md-mb,md+mb],members=mm,not_a_sharp_gap=True))
    W2=next(v for v in rows if v['W_eV']==2 and v['reference_kind']=='own_Fermi')
    old=json.loads((HERE.parent/'chemical_k3_2026-10-14/grid_result.json').read_text())
    oldW2=next(v for v in old['rows'] if v['W_eV']==2 and v['reference_kind']=='own_Fermi')['k3']['delta_eV']
    result=dict(status='CALCULATED ONE ordered PBE16 x=.125 chemistry pair; conditional spectral bounds only',x=.125,member_count=2,method='stock QE7.5 PBE+SOC SG15 FR NC 50/200Ry FD.001Ry Gamma fixed6.46A',members=members,physical_frame_transport=transport,original_frame_replaced=False,Gaussian_rows=rows,scalar_causal_rows=scalar,matrix_causal_rows=matrix,actual_complex_invariance_checks=checks,IEEE_weight_budgets=rounds,primary_W2_eV=W2['delta_eV'],primary_conditional_interval_eV=W2['conditional_interval_eV'],prior_x025_k3_W2_eV=oldW2,comparison_difference_eV=W2['delta_eV']-oldW2,comparison_is_composition_cell_and_sampling_confounded=True,not_a_dilute_slope=True,not_a_gap=True,material_error_bar=False,HSE_launched=False,physical_xc=None,unquantified_errors=['PBE vs hybrid/quasiparticles','cell/ordered environment, not random alloy','Gamma BZ sampling, no finite-size separation','fixed lattice, no ionic relaxation/zero point','FD finite regulator','native Hamiltonian eigenpair residual norms missing'],source_hashes={str(p):r.sha(p) for p in [Path(__file__),HERE/'preregistration.md',HERE/'science.py',original.HERE/'numerical_result.json',HERE.parent/'chemical_k3_2026-10-14/grid_result.json']})
    np.savez(HERE/'complex_overlaps.npz',**overlaps)
    (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ['primary_W2_eV','primary_conditional_interval_eV','prior_x025_k3_W2_eV','comparison_difference_eV']},indent=2))
    for rr in rows:
        if rr['reference_kind']=='own_Fermi':print('Gaussian',rr['W_eV'],rr['delta_eV'],rr['conditional_interval_eV'])
    for rr in scalar:print('Causal scalar',rr['eta_eV'],rr['delta_eV'],rr['conditional_interval_eV'])
    for rr in matrix:print('Causal matrix',rr['eta_eV'],rr['delta_eV'],rr['fixed_frame_conditional_interval_eV'])


if __name__=='__main__':evaluate()
