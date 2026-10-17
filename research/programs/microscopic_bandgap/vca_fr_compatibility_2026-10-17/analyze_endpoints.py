"""Saved native endpoint comparison; no executable launch or UPF rewriting."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import h5py
import numpy as np
from scipy.special import expit

HERE = Path(__file__).resolve().parent
RY_EV = 13.605693122994


def state(case):
    case = Path(case); save = case/'out/vcaqual.save'
    root = ET.parse(save/'data-file-schema.xml').getroot(); out = root.find('output')
    assert out.findtext('convergence_info/scf_conv/convergence_achieved') == 'true'
    assert out.findtext('magnetization/lsda') != 'true'
    assert root.findtext('input/spin/noncolin') == 'true'
    assert root.findtext('input/spin/spinorbit') == 'true'
    assert abs(float(out.findtext('band_structure/nelec'))-36) < 1e-14
    ks = out.findall('band_structure/ks_energies'); assert len(ks) == 1
    k = np.fromstring(ks[0].findtext('k_point'), sep=' '); assert np.linalg.norm(k) == 0
    w = float(ks[0].find('k_point').attrib['weight']); assert abs(w-1) < 1e-14
    e = 2*np.fromstring(ks[0].findtext('eigenvalues'), sep=' ')
    f = np.fromstring(ks[0].findtext('occupations'), sep=' ')
    mu = 2*float(out.findtext('band_structure/fermi_energy'))
    cell = np.array([np.fromstring(out.findtext('atomic_structure/cell/'+n), sep=' ')
                     for n in ['a1', 'a2', 'a3']])
    volume = abs(np.linalg.det(cell))
    with h5py.File(save/'charge-density.hdf5', 'r') as h:
        g = h['MillerIndices'][:]
        rho = np.ascontiguousarray(h['rhotot_g'][:]).view(complex).reshape(-1)
    order = sorted(range(len(g)), key=lambda i: tuple(g[i])); g=g[order]; rho=rho[order]
    zero = np.flatnonzero(np.all(g == 0, axis=1)); assert len(zero) == 1
    summary = dict(accepted_native_SCF=True, energy_Ry=2*float(out.findtext('total_energy/etot')),
        fermi_Ry=mu, eigenvalues_Ry=e.tolist(), occupations=f.tolist(),
        charge_error_e=float(f.sum()-36), rhoG_charge_error_e=float(rho[zero[0]].real*volume-36),
        FD_formula_max_error=float(np.max(abs(f-expit((mu-e)/.001)))),
        SCF_accuracy_Hartree=float(out.findtext('convergence_info/scf_conv/scf_error')),
        iterations=int(out.findtext('convergence_info/scf_conv/n_scf_steps')),
        nsym=int(out.findtext('symmetries/nsym')), npw_count=int(ks[0].findtext('npw')),
        volume_bohr3=float(volume), cell_bohr=cell.tolist(),
        highest_occupation=float(f[-1]))
    assert len(e) == len(f) == 44
    assert max(abs(summary['charge_error_e']), abs(summary['rhoG_charge_error_e'])) <= 1e-8
    assert summary['FD_formula_max_error'] <= 1e-10
    return summary, g, rho, volume


def compare(root, species):
    a, ga, ra, va = state(Path(root)/('scf_'+species+'_original'))
    b, gb, rb, vb = state(Path(root)/('scf_'+species+'_virtual'))
    assert np.array_equal(ga, gb) and va == vb
    assert np.array_equal(a['cell_bohr'], b['cell_bohr'])
    ea=np.array(a['eigenvalues_Ry']); eb=np.array(b['eigenvalues_Ry'])
    de=eb-ea; dm=b['fermi_Ry']-a['fermi_Ry']
    df=np.abs(np.array(a['occupations'])-np.array(b['occupations']))
    # FD globally has derivative <=1/(4sigma). This is a conditioning check,
    # not a fitted occupation tolerance or a material uncertainty estimate.
    f_bound=(np.abs(de)+abs(dm))/(4*.001)+2e-12
    result=dict(species=species, original=a, virtual=b,
        total_energy_difference_meV=(b['energy_Ry']-a['energy_Ry'])*RY_EV*1000,
        fermi_difference_meV=dm*RY_EV*1000,
        all44_raw_eigenvalue_max_difference_meV=float(np.max(abs(de)))*RY_EV*1000,
        all44_mu_aligned_eigenvalue_max_difference_meV=float(np.max(abs(de-dm)))*RY_EV*1000,
        occupation_max_difference=float(np.max(df)), FD_conditioning_bound_max=float(np.max(f_bound)),
        FD_conditioning_check=bool(np.all(df<=f_bound)),
        rhoG_relative_L2=float(np.linalg.norm(rb-ra)/np.linalg.norm(ra)),
        rhoG_max_abs_difference_e=float(np.max(abs(rb-ra))*va),
        operator_equality_inferred_from_eigenvalues=False)
    result['pass'] = bool(abs(result['total_energy_difference_meV']) <= .1 and
        result['all44_raw_eigenvalue_max_difference_meV'] <= .1 and
        result['all44_mu_aligned_eigenvalue_max_difference_meV'] <= .1 and
        result['rhoG_relative_L2'] <= 1e-5 and result['rhoG_max_abs_difference_e'] <= 1e-5 and
        result['FD_conditioning_check'])
    return result


if __name__ == '__main__':
    p=json.loads((HERE/'preregistration.json').read_text())
    for s in ['hg', 'cd']:
        result=compare(p['root'], s)
        (HERE/(s+'_endpoint_result.json')).write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ['original', 'virtual']}, indent=2))
        if not result['pass']:
            raise SystemExit('STOP: endpoint difference exceeds prospective gate')
