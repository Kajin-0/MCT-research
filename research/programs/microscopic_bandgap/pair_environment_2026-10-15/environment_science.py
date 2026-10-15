"""Native PBE pair validation in EACH actual crystal group, same accepted host frame."""
from pathlib import Path
from xml.etree import ElementTree as ET
import json,sys
import h5py
import numpy as np
from scipy.special import expit
from geometry import Q,XYZ,symbols,compute

HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'chemical_pbe16_p2_2026-10-15'
sys.path.insert(0,str(PREV))
from science_units_v2 import cell,td_check,read_spinors,cross_spinor_overlap,self_time_reversal_overlap,EV_HA,original
HOST=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/p16p2_20261015/host')


def reference():
    rec=json.loads((PREV/'host_readback_v2.json').read_text())
    assert rec['scientific_pass'] and rec['terminal']['terminal']
    c,g,k=read_spinors(HOST/'out/r07pbe.save/wfc1.hdf5')
    f={l:c[np.array(rec['science']['host_checks'][l]['native_bands_1based'])-1] for l in ['Gamma6','Gamma8']}
    return f,g,k,rec


def symmetry(t,member):
    pred=compute()['members'][member];expected={tuple(np.array(R).ravel()) for R in pred['point_rotations']}
    A=cell(t);atoms=t.find('.//output/atomic_structure/atomic_positions')
    coords=np.array([np.fromstring(a.text,sep=' ') for a in atoms])@np.linalg.inv(A)
    names=[a.attrib['name'] for a in atoms]
    assert names==symbols(member) and np.max(abs(coords-XYZ))<1e-10
    actual=set();records=[]
    for item in t.findall('.//output/symmetries/symmetry'):
        # QE also writes rejected Bravais-lattice operations without a chemical
        # permutation. They are not symmetries of this crystal.
        if item.findtext('info')!='crystal_symmetry':continue
        S=np.fromstring(item.findtext('rotation'),sep=' ').reshape(3,3)
        R=A.T@S@np.linalg.inv(A.T);Ri=np.rint(R).astype(int)
        assert np.max(abs(R-Ri))<1e-10
        ft=np.fromstring(item.findtext('fractional_translation'),sep=' ')
        transformed=coords@S.T+ft
        eq=np.fromstring(item.findtext('equivalent_atoms'),sep=' ',dtype=int)-1
        assert len(eq)==16 and sorted(eq.tolist())==list(range(16))
        delta=transformed-coords[eq]
        assert np.max(abs(delta-np.rint(delta)))<1e-9
        assert all(names[i]==names[j] for i,j in enumerate(eq))
        actual.add(tuple(Ri.ravel()));records.append(dict(cartesian=Ri.tolist(),fractional_translation=ft.tolist()))
    assert actual==expected and len(records)==len(expected)
    flags=t.find('.//input/symmetry_flags')
    assert all(flags.findtext(k)=='false' for k in ['nosym','noinv','no_t_rev'])
    return dict(native_linear_group_order=len(actual),exact_predicted_group_match=True,all_native_chemical_permutations_pass=True,operations=records,shared_Gamma8_quartet_NOT_required=member=='shared')


def validate(root,member):
    t=ET.parse(root/'out/r07pbe.save/data-file-schema.xml');b=t.find('.//output/band_structure');ks=b.findall('ks_energies')
    assert len(ks)==1 and float(ks[0].find('k_point').attrib['weight'])==1.
    E=np.fromstring(ks[0].findtext('eigenvalues'),sep=' ')*2
    wg=np.fromstring(ks[0].findtext('occupations'),sep=' ');ef=float(b.findtext('fermi_energy'))*2
    fd=expit((ef-E)/.001);charge=float(sum(fd));oe=float(max(abs(fd-wg)))
    assert float(b.findtext('nelec'))==288 and E.shape==(352,) and np.min(np.diff(E))>-1e-12
    assert [float(t.findtext('.//output/basis_set/'+n))*2 for n in ['ecutwfc','ecutrho']]==[50.,200.]
    sym=symmetry(t,member)
    c,g,k=read_spinors(root/'out/r07pbe.save/wfc1.hdf5')
    assert len(c)==352 and np.linalg.norm(k)<1e-12
    flat=c.reshape(352,-1);gram=float(np.linalg.norm(flat.conj()@flat.T-np.eye(352),2));assert gram<1e-8
    with h5py.File(root/'out/r07pbe.save/wfc1.hdf5') as f:B=np.array([f['MillerIndices'].attrs['bg'+str(i)] for i in [1,2,3]])
    alat=float(t.find('.//output/atomic_structure').attrib['alat'])
    assert np.max(abs(B/(2*np.pi)-np.linalg.inv(cell(t)).T))<1e-10
    xmlB=np.array([np.fromstring(t.findtext('.//output/basis_set/reciprocal_lattice/b'+str(i)),sep=' ') for i in [1,2,3]])
    assert np.max(abs(B-xmlB*2*np.pi/alat))<1e-10
    fs,g0,k0,rec=reference();A0=cell(ET.parse(HOST/'out/r07pbe.save/data-file-schema.xml'))
    assert np.max(abs(cell(t)-A0))<1e-12
    weights={l:np.sum(abs(cross_spinor_overlap(f,g0,k0,c,g,k))**2,axis=0)/len(f) for l,f in fs.items()}
    # Clusters are actual degenerate eigenspaces; no arbitrary adjacent pairing
    # within a quartet and no averaging of a split shared quartet.
    bounds=np.r_[0,np.flatnonzero(np.diff(E)*EV_HA/2>=1e-5)+1,352]
    clusters=[];dominant={}
    for a,z in zip(bounds[:-1],bounds[1:]):
        relevant=any(sum(w[a:z])>=.01 for w in weights.values())
        sv,_=self_time_reversal_overlap(c[a:z],g,k)
        passed=bool((z-a)%2==0 and min(sv)>1-1e-8)
        if relevant:assert passed,'physically relevant Kramers cluster failed'
        clusters.append(dict(first_band_1based=int(a+1),last_band_1based=int(z),projected_weights={l:float(sum(w[a:z])) for l,w in weights.items()},energy_range_eV=(E[[a,z-1]]*EV_HA/2).tolist(),minimum_Theta_singular_value=float(min(sv)),Kramers_pass=passed,relevant_by_preregistration=relevant))
    if member=='unshared':
        for l,d,expected in [('Gamma6',2,[1,0,0]),('Gamma8',4,[0,0,1])]:
            chosen=np.sort(np.argsort(weights[l])[-d:]);s=td_check(c[chosen],g,cell(t))
            spread=float(np.ptp(E[chosen])*EV_HA/2)
            assert s['nearest_integer_classification_admitted_under_model'] and s['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==expected and spread<1e-5
            dominant[l]=dict(bands_1based=(chosen+1).tolist(),spread_eV=spread,Td=s)
    error=float(t.findtext('.//output/convergence_info/scf_conv/scf_error'))*2
    conv=t.findtext('.//output/convergence_info/scf_conv/convergence_achieved')=='true'
    passed=bool(conv and error<=1e-9 and abs(charge-288)<=1e-8 and oe<1e-9 and 'JOB DONE.' in (root/'pw.out').read_text())
    return dict(scientific_pass=passed,SCF_converged=conv,scf_error_Ry=error,scf_iterations=int(t.findtext('.//output/convergence_info/scf_conv/n_scf_steps')),total_energy_Ry=float(t.findtext('.//output/total_energy/etot'))*2,fermi_Ry=ef,charge_residual_e=charge-288,occupation_reconstruction_error=oe,all352_Gram_defect_op=gram,native_Gamma_PW=len(g),physical_HDF5_XML_cell_basis_pass=True,symmetry=sym,Kramers_clusters=clusters,unshared_Td_multiplets=dominant,reference_frame='accepted16atomhost native50Ry Gamma6/8, frozen',not_HSE_source_qualification=True)
