"""Read-only audit of the supplied stock-virtual_v2 Hg/Cd potentials."""
from pathlib import Path
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET

import numpy as np

HERE = Path(__file__).resolve().parent
DFT = Path('/home/User/opencode_workspace/DFT')
QE = DFT / '.local/qe75_lowram_20261011/q-e'
GENERATED = Path('/tmp/r07_vca_20261017_compatibility')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def array(root, key):
    return np.fromstring(root.findtext(key), sep=' ')


def main():
    paths = {s: DFT / 'pseudopotentials' / f'{s}_sg15_pbe_fr_v12.UPF'
             for s in ['Hg', 'Cd', 'Te']}
    paths.update({name: GENERATED / name / 'NewPseudo.UPF'
                  for name in ['x_1_0', 'x_0_875', 'x_0_0']})
    pp = {s: ET.parse(p).getroot() for s, p in paths.items()}
    records = {}
    for s, root in pp.items():
        head = root.find('PP_HEADER').attrib
        beta = root.findall('PP_NONLOCAL/*')
        beta = [v for v in beta if v.tag.startswith('PP_BETA.')]
        so = root.findall('PP_SPIN_ORB/*')
        relbeta = [v for v in so if v.tag.startswith('PP_RELBETA.')]
        relwfc = [v for v in so if v.tag.startswith('PP_RELWFC.')]
        assert head['has_so'].lower() in ['t', 'true']
        assert head['pseudo_type'] == 'NC' and head['relativistic'] == 'full'
        assert head['core_correction'].lower() in ['f', 'false']
        assert len(beta) == len(relbeta) == int(head['number_of_proj'])
        for b, sb in zip(beta, relbeta):
            l = int(b.attrib['angular_momentum']); j = float(sb.attrib['jjj'])
            assert int(sb.attrib['lll']) == l and abs(j-l) == .5
            cutoff = int(b.attrib['cutoff_radius_index'])
            assert 0 < cutoff <= int(head['mesh_size'])
        records[s] = dict(header=head, radial_points=len(array(root, 'PP_MESH/PP_R')),
                          rmax_bohr=float(array(root, 'PP_MESH/PP_R')[-1]),
                          radial_beta_count=len(beta),
                          angular_beta_count=sum(2*int(v.attrib['angular_momentum'])+1 for v in beta),
                          jjj=[float(v.attrib['jjj']) for v in relbeta],
                          jchi=[float(v.attrib['jchi']) for v in relwfc],
                          labels=[v.attrib.get('label') for v in root.findall('PP_PSWFC/*')])
    comparisons = {}
    hg, cd = pp['Hg'], pp['Cd']
    dh = array(hg, 'PP_NONLOCAL/PP_DIJ').reshape(14, 14)
    dc = array(cd, 'PP_NONLOCAL/PP_DIJ').reshape(10, 10)
    for name, weight in [('x_1_0', 1.), ('x_0_875', .875), ('x_0_0', 0.)]:
        root = pp[name]; n = int(root.find('PP_HEADER').attrib['mesh_size'])
        assert np.array_equal(array(root, 'PP_MESH/PP_R'), array(hg, 'PP_MESH/PP_R'))
        assert np.array_equal(array(root, 'PP_MESH/PP_R'), array(cd, 'PP_MESH/PP_R')[:n])
        d = array(root, 'PP_NONLOCAL/PP_DIJ').reshape(24, 24)
        assert np.array_equal(d[:14, :14], weight*dh)
        assert np.array_equal(d[14:, 14:], (1-weight)*dc)
        assert np.count_nonzero(d[:14, 14:]) == np.count_nonzero(d[14:, :14]) == 0
        assert records[name]['jjj'] == records['Hg']['jjj']+records['Cd']['jjj']
        assert records[name]['jchi'] == records['Hg']['jchi'] == records['Cd']['jchi']
        beta_errors = []
        for species, offset in [('Hg', 0), ('Cd', 14)]:
            for i in range(records[species]['radial_beta_count']):
                a = array(root, f'PP_NONLOCAL/PP_BETA.{i+1+offset}')
                b = array(pp[species], f'PP_NONLOCAL/PP_BETA.{i+1}')[:n]
                beta_errors.append(float(np.max(abs(a-b))))
        assert max(beta_errors) == 0
        comparisons[name] = dict(Hg_weight=weight, Cd_fraction=1-weight,
            D_blocks_exact=True, cross_D_zero=True, beta_prefix_max_error=max(beta_errors),
            local_average_max_error_Ry=float(np.max(abs(array(root, 'PP_LOCAL')-
                  weight*array(hg, 'PP_LOCAL')-(1-weight)*array(cd, 'PP_LOCAL')[:n]))),
            rhoatom_average_max_error=float(np.max(abs(array(root, 'PP_RHOATOM')-
                  weight*array(hg, 'PP_RHOATOM')-(1-weight)*array(cd, 'PP_RHOATOM')[:n]))))
    r = array(cd, 'PP_MESH/PP_R'); tail = r > array(hg, 'PP_MESH/PP_R')[-1]
    delta = array(cd, 'PP_LOCAL')[tail]+40/r[tail]
    source_pins = {}
    for name in ['upflib/virtual_v2.f90', 'upflib/read_upf_new.f90',
                 'upflib/init_us_1.f90', 'upflib/vloc_mod.f90',
                 'Modules/atomic_wfc_mod.f90', 'PW/src/wfcinit.f90']:
        tag = subprocess.check_output(['git', '--no-optional-locks', '-C', str(QE),
                                       'show', 'qe-7.5:'+name])
        assert (QE/name).read_bytes() == tag
        source_pins[name] = hashlib.sha256(tag).hexdigest()
    result = dict(pseudo_checks_pass=True, PP=records, comparisons=comparisons,
          Cd_discarded_local_tail_Coulomb_deviation_max_Ry=float(np.max(abs(delta))),
          Cd_discarded_rhoatom_max=float(np.max(abs(array(cd, 'PP_RHOATOM')[tail]))),
          source_pins=source_pins,
          file_pins={str(p): sha(p) for p in paths.values()},
          executable_pins={str(DFT/'.local/qe-env/bin'/name): sha(DFT/'.local/qe-env/bin'/name)
                           for name in ['pw.x', 'virtual_v2.x']},
          operator_equality_claim=False, HSE_execution_admitted=False)
    (HERE/'upf_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(pseudo_checks_pass=True, comparisons=comparisons,
                         Cd_tail_max_Ry=result['Cd_discarded_local_tail_Coulomb_deviation_max_Ry']), indent=2))


if __name__ == '__main__':
    main()
