"""Read-only real host physical-frame gate, run before Cd acquisition."""
from pathlib import Path
import json
import numpy as np
from xml.etree import ElementTree as ET
import analyze_k3 as a
import run_k3 as r

HERE=Path(__file__).resolve().parent


def evaluate():
    if (HERE/'host_frame_precheck.json').exists():raise FileExistsError('preserve host gate')
    r.load('host');final=json.loads((r.PAIR/'host/FINAL.json').read_text())
    assert final['accepted'] and final['terminal_pass'] and not r.cgroup_path(final['guard']['cgroup']).exists()
    a.previous.PAIR=a.PAIR;c,g,k,e,ef,info=a.previous.read_member('host')
    c0,g0,k0,_,_,oldinfo=a.old.intake('host');assert oldinfo['lattice_bohr']==info['lattice_bohr']
    source=a.old.PAIR/'host/out/r07pbe.save/wfc1.hdf5';target=r.PAIR/'host/out/r07pbe.save/wfc1.hdf5'
    xml=ET.parse(target.parent/'data-file-schema.xml');oldxml=ET.parse(source.parent/'data-file-schema.xml')
    positions=lambda t:np.array([np.fromstring(v.text,sep=' ') for v in t.find('.//output/atomic_structure/atomic_positions')])
    np.testing.assert_array_equal(positions(xml),positions(oldxml))
    native_sym=set()
    crystal=[v for v in xml.findall('.//output/symmetries/symmetry') if v.findtext('info')=='crystal_symmetry']
    assert len(crystal)==24
    for v in crystal:
        rotation=np.fromstring(v.findtext('rotation'),sep=' ').reshape(3,3)
        assert np.array_equal(rotation,np.rint(rotation))
        native_sym.add(tuple(rotation.astype(int).ravel()))
        np.testing.assert_array_equal(np.fromstring(v.findtext('fractional_translation'),sep=' '),np.zeros(3))
    assert native_sym=={tuple(v['spatial'].astype(int).ravel()) for v in a.old.td_operations()}
    prior=json.loads((a.previous.OLD/'numerical_result.json').read_text());checks={}
    for label,expected in [('Gamma6',[1,0,0]),('Gamma8',[0,0,1])]:
        frame=c0[np.array(prior['host_sector_selection'][label]['native_host_bands_1based'])-1]
        f,index,proof=a.embed_same_cell(frame,g0,k0,a.Bmatrix(source),g,k,a.Bmatrix(target))
        overlap=a.cross_spinor_overlap(f,g,k,c,g,k);weights=np.sum(abs(overlap)**2,axis=0)/len(frame)
        ix=np.sort(np.argsort(weights)[-len(frame):]);native=c[ix]
        ir=a.old.td_check(native,g)
        assert ir['nearest_integer_classification_admitted_under_model'] and ir['rounded_Gamma6_Gamma7_Gamma8_multiplicities']==expected
        mask=np.all(g%2==0,axis=1)|np.all(g%2==1,axis=1);prob=np.sum(abs(native[:,:,mask])**2,axis=(1,2));assert min(prob)>1-1e-8
        checks[label]=dict(mapping=proof,native_bands_1based=(ix+1).tolist(),energies_relative_Fermi_eV=(e[ix]-ef).tolist(),primitive_Gamma_probabilities=prob.tolist(),Td=ir)
    result=dict(admitted_for_Cd_acquisition=True,host_source_terminal_pass=True,actual_native_symmetry_matches_all24_Td=True,
        actual_cell_origin_matched=True,host=info,checks=checks,code_sha256=r.sha(__file__))
    (HERE/'host_frame_precheck.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(admitted=True,charge_e=info['charge_residual_e'],scf_steps=info['scf_iterations'],native_Gamma_PW=info['native_Gamma_PW'],labels={l:v['native_bands_1based'] for l,v in checks.items()}),indent=2))


if __name__=='__main__':evaluate()
