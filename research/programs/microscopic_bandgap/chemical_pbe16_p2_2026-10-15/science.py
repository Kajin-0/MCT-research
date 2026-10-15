"""Physical cell/NC-spinor admission, original Gamma frame, no solver changes."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json,sys
import h5py
import numpy as np
from scipy.special import expit

HERE=Path(__file__).resolve().parent
DFT=Path('/home/User/opencode_workspace/DFT')
OLD=HERE.parent/'chemical_pbe_pilot_2026-10-14'
sys.path[:0]=[str(OLD),str(DFT/'src')]
import analyze as original
from mct_dft.qe_wavefunctions import read_spinors,cross_spinor_overlap,embed_primitive_spinors,self_time_reversal_overlap
Q=np.ones((3,3),int)-np.eye(3,dtype=int)
EV_HA=27.211386245988


def cell(t):
    return np.array([np.fromstring(t.findtext('.//output/atomic_structure/cell/a'+str(i)),sep=' ') for i in [1,2,3]])


def frames(g,k,t):
    c0,g0,k0,e0,ef0,i0=original.intake('host')
    rec=json.loads((OLD/'numerical_result.json').read_text())
    A0=np.array(i0['lattice_bohr']);A=cell(t)
    assert np.max(abs(A-Q@A0))<1e-9
    ix={tuple(v):i for i,v in enumerate(g)}
    mapping=np.array([ix[tuple(v)] for v in g0@Q.T])
    assert np.max(abs((g0@Q.T)@np.linalg.inv(A).T-g0@np.linalg.inv(A0).T))<1e-12
    out={}
    for label in ['Gamma6','Gamma8']:
        f=c0[np.array(rec['host_sector_selection'][label]['native_host_bands_1based'])-1]
        out[label]=embed_primitive_spinors(f,g0,k0,Q,g,k)
        assert np.max(abs(out[label][:,:,mapping]-f))==0
        assert abs(np.linalg.norm(out[label])**2-len(f))<1e-12
    return out,dict(integer_repeat=Q.tolist(),volume_ratio=round(np.linalg.det(Q)),source_PW=len(g0),target_PW=len(g),coefficient_rescale=1.,physical_wavevector_error_max= float(np.max(abs((g0@Q.T)@np.linalg.inv(A).T-g0@np.linalg.inv(A0).T))),original_projectors_replaced=False)


def td_check(c,g,A):
    lookup={tuple(v):i for i,v in enumerate(g)};flat=c.reshape(len(c),-1)
    chars=[];leak=0.;physical_g=g@np.linalg.inv(A).T
    for op in original.td_operations():
        mapped_float=physical_g@op['spatial'].T@A.T
        mapped=np.rint(mapped_float).astype(int)
        assert np.max(abs(mapped_float-mapped))<1e-10
        ix=np.array([lookup[tuple(v)] for v in mapped])
        transformed=np.empty_like(c);transformed[:,:,ix]=np.einsum('st,atg->asg',op['spin'],c)
        mat=flat.conj()@transformed.reshape(len(c),-1).T
        chars.append(np.trace(mat));leak=max(leak,float(np.linalg.norm(np.eye(len(c))-mat.conj().T@mat,'fro')))
    gram=float(np.linalg.norm(flat.conj()@flat.T-np.eye(len(c)),'fro'))
    ideal=np.array([op['characters'] for op in original.td_operations()])
    return dict(Gram_defect_F=gram,max_span_defect_F=leak,**original.nearby_irrep_envelope(gram,leak,np.array(chars),ideal,len(c),2*len(g)))


def validate(root,member):
    t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml');b=t.find('.//output/band_structure');ks=b.findall('ks_energies')
    assert len(ks)==1 and float(ks[0].find('k_point').attrib['weight'])==1.
    eig=np.fromstring(ks[0].findtext('eigenvalues'),sep=' ')*2
    wg=np.fromstring(ks[0].findtext('occupations'),sep=' ')
    ef=float(b.findtext('fermi_energy'))*2;fd=expit((ef-eig)/.001)
    charge=float(sum(fd));occ_error=float(max(abs(wg-fd)))
    assert float(b.findtext('nelec'))==288 and eig.shape==(352,)
    cuts=[float(t.findtext('.//output/basis_set/'+name))*2 for name in ['ecutwfc','ecutrho']]
    assert cuts==[50.,200.]
    nsym=int(t.findtext('.//output/symmetries/nsym'))
    flags=t.find('.//input/symmetry_flags')
    assert nsym==24 and all(flags.findtext(k)=='false' for k in ['nosym','noinv','no_t_rev'])
    c,g,k=read_spinors(root/'out/r07pbe.save/wfc1.hdf5')
    assert len(c)==352 and np.linalg.norm(k)<1e-12
    flat=c.reshape(len(c),-1);gram=float(np.linalg.norm(flat.conj()@flat.T-np.eye(len(c)),2))
    assert gram<1e-8
    with h5py.File(root/'out/r07pbe.save/wfc1.hdf5') as f:
        B=np.array([f['MillerIndices'].attrs['bg'+str(i)] for i in [1,2,3]])
    alat=float(t.find('.//output/atomic_structure').attrib['alat'])
    assert np.max(abs(B/alat-np.linalg.inv(cell(t)).T))<1e-10
    fs,transport=frames(g,k,t);hostchecks={}
    if member=='host':
        for label,frame in fs.items():
            ov=cross_spinor_overlap(frame,g,k,c,g,k);w=np.sum(abs(ov)**2,axis=0)/len(frame)
            chosen=np.sort(np.argsort(w)[-len(frame):]);native=c[chosen]
            sym=td_check(native,g,cell(t));expected=[1,0,0] if label=='Gamma6' else [0,0,1]
            assert sym['nearest_integer_classification_admitted_under_model'] and sym['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==expected
            primitive=np.sum(abs(native[:,:,np.all(g%2==0,axis=1)])**2,axis=(1,2))
            sv,ge=self_time_reversal_overlap(native,g,k)
            spread=float(np.ptp(eig[chosen])*EV_HA/2)
            assert min(primitive)>1-1e-8 and spread<1e-5 and min(sv)>1-1e-8
            hostchecks[label]=dict(native_bands_1based=(chosen+1).tolist(),eigenvalues_eV=(eig[chosen]*EV_HA/2).tolist(),spread_eV=spread,primitive_Gamma_weights=primitive.tolist(),Theta_overlap_singular_values=sv.tolist(),Td=sym,original_frame_weight_in_selected=float(sum(w[chosen])))
    scf_error=float(t.findtext('.//output/convergence_info/scf_conv/scf_error'))*2
    achieved=t.findtext('.//output/convergence_info/scf_conv/convergence_achieved')=='true'
    passed=bool(achieved and scf_error<=1e-9 and 'JOB DONE.' in (root/'pw.out').read_text() and abs(charge-288)<=1e-8 and occ_error<1e-9)
    return dict(scientific_pass=passed,SCF_converged=achieved,charge_e=charge,charge_residual_e=charge-288,occupation_error_max=occ_error,scf_error_Ry=scf_error,scf_iterations=int(t.findtext('.//output/convergence_info/scf_conv/n_scf_steps')),total_energy_Ry=float(t.findtext('.//output/total_energy/etot'))*2,fermi_Ry=ef,cutoffs_Ry=cuts,nsym=nsym,all352_Gram_defect_op=gram,native_Gamma_PW=len(g),physical_HDF5_basis_check=True,frame_transport=transport,host_checks=hostchecks)
