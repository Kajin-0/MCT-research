"""Actual matched native spinor spectroscopy. No native launch or gap fit."""
from pathlib import Path
import hashlib
import json
import sys
from xml.etree import ElementTree as ET
import numpy as np
from scipy.special import expit

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
PAIR=DFT/'.local/qe75_lowram_20261011/chemical_pbe8_20261014_v2'
REF=DFT/'calculations/r07/hgte_hse_sg15_k4_q4_e90_f120_fullacc_c1e-10_t3600_g1800'
sys.path.insert(0,str(DFT/'src'))
sys.path.insert(0,str(HERE.parent/'native_matched_pilot_2026-10-11'))
from mct_dft.qe_wavefunctions import read_spinors,cross_spinor_overlap
from reference_irrep_check import td_operations,nearby_irrep_envelope,gamma
EV_HA=27.211386245988
W=2.


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for v in iter(lambda:f.read(1<<20),b''):h.update(v)
    return h.hexdigest()


def write(p,j):
    Path(p).write_text(json.dumps(j,indent=2,sort_keys=True,allow_nan=False)+'\n')


def intake(member):
    root=PAIR/member;schema=root/'out/r07pbe.save/data-file-schema.xml'
    t=ET.parse(schema);b=t.find('.//output/band_structure')
    assert t.findtext('.//output/convergence_info/scf_conv/convergence_achieved')=='true'
    assert float(b.findtext('nelec'))==144 and len(b.findall('ks_energies'))==1
    e=np.fromstring(b.findtext('ks_energies/eigenvalues'),sep=' ')*EV_HA
    ef=float(b.findtext('fermi_energy'))*EV_HA
    wg=np.fromstring(b.findtext('ks_energies/occupations'),sep=' ')
    f=expit((ef-e)/(EV_HA/2*.001))
    assert abs(sum(f)-144)<1e-8 and max(abs(f-wg))<1e-9
    c,g,k=read_spinors(root/'out/r07pbe.save/wfc1.hdf5')
    assert c.shape[0]==176 and np.linalg.norm(k)<1e-12 and np.all(np.isfinite(c))
    lattice=np.array([np.fromstring(t.findtext('.//output/atomic_structure/cell/a'+str(i)),sep=' ') for i in [1,2,3]])
    assert np.max(abs(lattice-np.eye(3)*lattice[0,0]))<1e-10
    flat=c.reshape(176,-1)
    defect=float(np.linalg.norm(flat.conj()@flat.T-np.eye(176),2))
    assert defect<1e-8
    fields=dict(total_energy_Ry=float(t.findtext('.//output/total_energy/etot'))*2,
        scf_error_Ry=float(t.findtext('.//output/convergence_info/scf_conv/scf_error'))*2,
        scf_iterations=int(t.findtext('.//output/convergence_info/scf_conv/n_scf_steps')),
        charge_residual_e=float(sum(f)-144),occupation_reconstruction_max=float(max(abs(f-wg))),fermi_eV=ef,
        native_plane_waves=len(g),all176_Gram_defect_op=defect,lattice_bohr=lattice.tolist(),
        hashes={str(p):sha(p) for p in [root/'pw.in',root/'pw.out',schema,root/'out/r07pbe.save/wfc1.hdf5']})
    return c,g,k,e,ef,fields


def reference_candidates(c,g,e):
    # Old qualified primitive HSE sector; restriction is EXPLICIT and only
    # identifies candidates, not the final physical PBE projector.
    assignment=json.loads((REF/'gamma/signed_gap.json').read_text())
    rc,rg,rk=read_spinors(REF/'out/r07_open.save/wfc1.hdf5')
    assert np.linalg.norm(rk)<1e-12
    repeat=np.ones((3,3),int)-2*np.eye(3,dtype=int)
    lookup={tuple(v):i for i,v in enumerate(g)};mapped=rg@repeat.T
    keep=np.array([tuple(v) in lookup for v in mapped]);cols=np.array([lookup[tuple(v)] for v in mapped[keep]])
    gamma_mask=np.all(g%2==0,axis=1)|np.all(g%2==1,axis=1)
    gamma_p=np.sum(abs(c[:,:,gamma_mask])**2,axis=(1,2))
    result={};frames={}
    for label,d in [('Gamma6',2),('Gamma8',4)]:
        lo,hi=assignment[label+'_bands_1based'];s=rc[lo-1:hi]
        partial=np.zeros((d,2,len(g)),complex);partial[:,:,cols]=s[:,:,keep]
        f=partial.reshape(d,-1);gram=f.conj()@f.T
        w=np.sum(abs(f.conj()@c.reshape(176,-1).T)**2,axis=0)
        chosen=np.sort(np.argsort(w)[-d:]);selected=c[chosen]
        assert np.min(w[chosen])>.95 and np.min(gamma_p[chosen])>1-1e-8
        assert np.ptp(e[chosen])<1e-5
        frames[label]=selected
        result[label]=dict(native_host_bands_1based=(chosen+1).tolist(),native_host_eigenvalues_eV=e[chosen].tolist(),
            native_host_multiplet_spread_eV=float(np.ptp(e[chosen])),primitive_Gamma_translation_probabilities=gamma_p[chosen].tolist(),
            restricted_HSE_reference_norm_eigenvalues=np.linalg.eigvalsh(gram).tolist(),
            restricted_reference_weight_in_selected_host_states=w[chosen].tolist(),
            restricted_reference_max_missing_norm=float(np.max(1-np.linalg.eigvalsh(gram))),
            HSE_reference_used_only_for_candidate_selection=True)
    return frames,result


def td_check(c,g):
    lookup={tuple(v):i for i,v in enumerate(g)};ops=td_operations()
    chars=[];leak=0;flat=c.reshape(len(c),-1)
    gram=float(np.linalg.norm(flat.conj()@flat.T-np.eye(len(c)),'fro'))
    for op in ops:
        idx=np.array([lookup[tuple(v)] for v in (g@op['spatial'].T).astype(int)])
        transformed=np.empty_like(c);transformed[:,:,idx]=np.einsum('st,atg->asg',op['spin'],c)
        mat=flat.conj()@transformed.reshape(len(c),-1).T
        chars.append(np.trace(mat));leak=max(leak,float(np.linalg.norm(np.eye(len(c))-mat.conj().T@mat,'fro')))
    ideal=np.array([op['characters'] for op in ops]);char=np.array(chars)
    cert=nearby_irrep_envelope(gram,leak,char,ideal,len(c),2*len(g))
    return dict(Gram_defect_frobenius=gram,maximum_span_leakage_defect_frobenius=leak,
        character_complex=[[float(z.real),float(z.imag)] for z in char],**cert)


def centroid(weights,t,r,epsilon,round_budget):
    phi=np.exp(-t*t/(2*W*W));M=float(weights@phi);N=float(weights@(t*phi));C=N/M
    assert M>=.05 and M>2*epsilon+round_budget
    bound=(W/np.sqrt(np.e)+abs(C))
    denominator=M-2*epsilon-round_budget
    return dict(retained_weight_sum=float(sum(weights)),omitted_probability=r,
        Gaussian_mass=M,Gaussian_centroid_relative_Fermi_eV=C,
        # Joint denominator: signed projector/arithmetic perturbations may
        # lower mass AFTER a positive omitted-spectrum completion. Separately
        # summing bounds with different denominators misses a cross term.
        conditional_omitted_spectrum_bound_eV=r*bound/denominator,
        conditional_nearby_projector_bound_eV=2*epsilon*bound/denominator,
        conditional_arithmetic_bound_eV=round_budget*bound/denominator,
        joint_denominator_lower=denominator,
        conditional_total_bound_eV=(r+2*epsilon+round_budget)*bound/denominator,
        full_retained_band_centroid_relative_Fermi_eV=float(weights@t/sum(weights)),
        full_unbounded_centroid_tail_bound=None,
        largest_projected_bands=[dict(band_1based=int(i+1),weight=float(weights[i]),energy_relative_Fermi_eV=float(t[i])) for i in np.argsort(weights)[-8:][::-1]])


def evaluate():
    host=intake('host');cd=intake('cd')
    hc,hg,hk,he,hf,hinfo=host;cc,cg,ck,ce,cf,cinfo=cd
    assert hinfo['lattice_bohr']==cinfo['lattice_bohr']
    frames,selection=reference_candidates(hc,hg,he)
    symmetry={label:td_check(frame,hg) for label,frame in frames.items()}
    for label,expected in [('Gamma6',[1,0,0]),('Gamma8',[0,0,1])]:
        assert symmetry[label]['nearest_integer_classification_admitted_under_model']
        assert symmetry[label]['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==expected
    branches={'host':{},'cd':{}}; overlaps={}; checks={}
    for label,frame in frames.items():
        eps=symmetry[label]['nearby_invariant_projector_distance_upper_model']
        for member,c,g,k,e,ef in [('host',hc,hg,hk,he,hf),('cd',cc,cg,ck,ce,cf)]:
            ov=cross_spinor_overlap(frame,hg,hk,c,g,k);overlaps[member+'_'+label]=ov
            weights=np.sum(abs(ov)**2,axis=0)/len(frame)
            r=max(0.,float(1-sum(weights)))
            entry=4*gamma(32*2*len(hg))+16*2.**-53
            round_budget=176*(2*entry+entry*entry)+64*gamma(176)
            assert sum(weights)<=1+round_budget
            branches[member][label]=centroid(weights,e-ef,r,eps,round_budget)
            # Exact actual-span unitary change and reciprocal reordering.
            rng=np.random.default_rng(7102026);u=np.linalg.qr(rng.normal(size=(len(frame),len(frame)))+1j*rng.normal(size=(len(frame),len(frame))))[0]
            alternate=cross_spinor_overlap(np.einsum('ij,jsg->isg',u,frame),hg,hk,c,g,k)
            checks[member+'_'+label+'_unitary_weight_max_error']=float(np.max(abs(weights-np.sum(abs(alternate)**2,axis=0)/len(frame))))
            alternate=cross_spinor_overlap(frame[:,:,::-1],hg[::-1],hk,c[:,:,::-1],g[::-1],k)
            checks[member+'_'+label+'_Miller_relabel_overlap_max_error']=float(np.max(abs(ov-alternate)))
            csv=HERE/(member+'_'+label+'_spectrum.csv')
            np.savetxt(csv,np.column_stack([np.arange(1,177),e-ef,weights]),delimiter=',',header='band_1based,energy_minus_Fermi_eV,host_sector_trace_weight_div_rank',comments='',fmt=['%d','%.17g','%.17g'])
    assert max(checks.values())<1e-12
    obs={}
    for member in ['host','cd']:
        b=branches[member]
        omega=b['Gamma6']['Gaussian_centroid_relative_Fermi_eV']-b['Gamma8']['Gaussian_centroid_relative_Fermi_eV']
        terms={k:sum(b[label][k] for label in ['Gamma6','Gamma8']) for k in ['conditional_omitted_spectrum_bound_eV','conditional_nearby_projector_bound_eV','conditional_arithmetic_bound_eV']}
        obs[member]=dict(Gaussian_projected_ordering_eV=omega,**terms)
    delta=obs['cd']['Gaussian_projected_ordering_eV']-obs['host']['Gaussian_projected_ordering_eV']
    bounds={k:obs['host'][k]+obs['cd'][k] for k in ['conditional_omitted_spectrum_bound_eV','conditional_nearby_projector_bound_eV','conditional_arithmetic_bound_eV']}
    full_bound=sum(bounds.values())
    result=dict(status='CALCULATED native exploratory PBE+SOC periodic CdHg3Te4 response; bounds PROVEN UNDER ASSUMPTIONS, no material validation',
        cell_cations=4,Cd_count=1,x=.25,W_eV=W,host=hinfo,cd=cinfo,host_sector_selection=selection,host_sector_symmetry=symmetry,
        branches=branches,observables=obs,delta_Gaussian_ordering_eV=delta,delta_conditional_completion_and_projector_interval_eV=[delta-full_bound,delta+full_bound],
        delta_bound_terms_eV=bounds,actual_complex_invariance_checks=checks,
        native_host_Gamma_signed_eigenvalue_gap_eV=float(np.mean(selection['Gamma6']['native_host_eigenvalues_eV'])-np.mean(selection['Gamma8']['native_host_eigenvalues_eV'])),
        unquantified_errors=['40Ry cutoff/160Ry density','single supercell Gamma grid','x=.25 periodic finite cell, not dilute','PBE functional vs HSE/quasiparticles','fixed lattice/no ionic relaxation','finite FD occupation regulator','native eigenpair/operator residual norms unavailable','many-body/zero point conventions','unknown thermodynamic/random alloy mapping'],
        rigorous_material_error_bar=False,physical_xc=None,HSE_convergence_claim=False,
        source_hashes={str(p):sha(p) for p in [Path(__file__),HERE/'analysis_protocol.md',DFT/'src/mct_dft/qe_wavefunctions.py',HERE.parent/'native_matched_pilot_2026-10-11/reference_irrep_check.py',REF/'gamma/signed_gap.json',REF/'out/r07_open.save/wfc1.hdf5']})
    np.savez(HERE/'complex_overlaps.npz',**overlaps)
    write(HERE/'numerical_result.json',result)
    print(json.dumps(dict(delta_eV=delta,conditional_interval_eV=result['delta_conditional_completion_and_projector_interval_eV'],observables=obs,branches=branches,host_symmetry={l:{k:symmetry[l][k] for k in ['rounded_Gamma6_Gamma7_Gamma8_multiplicities','nearby_invariant_projector_distance_upper_model']} for l in symmetry}),indent=2))
    return result


if __name__=='__main__':
    if (HERE/'numerical_result.json').exists():raise FileExistsError('preserve original result')
    evaluate()
