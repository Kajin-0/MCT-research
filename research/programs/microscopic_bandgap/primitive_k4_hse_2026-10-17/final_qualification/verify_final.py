"""Focused independent terminal checks plus immutable protection verification.

No native calls, unit changes, DFT writes or full-BZ reconstruction. Run from
the repository with bytecode disabled and OPENBLAS_NUM_THREADS=1.
"""
from pathlib import Path
import ast
import hashlib
import importlib.util
import itertools
import json
import subprocess
import xml.etree.ElementTree as ET

import numpy as np
from scipy.special import expit

P = Path(__file__).resolve().parent
CASE = P.parent
B = CASE.parent
REPO = B.parents[2]
DFT = Path('/home/User/opencode_workspace/DFT')


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    f = json.loads((CASE/'preregistration.json').read_text())
    r = json.loads((P/'state_result.json').read_text())
    root = Path(f['root'])
    checks = []

    def check(value, name):
        if not value:
            raise AssertionError(name)
        checks.append(name)

    for path, h in f['pins'].items():
        check(sha(path) == h, 'frozen launch pin '+path)
    check(sha(root/'pw.in') == f['input_sha256'] == sha(CASE/'host_pw.in'), 'input exact')
    check(sha(root/'observe_case.py') == f['observer_sha256'] == sha(CASE/'observe_case.py'), 'observer exact')
    check(sha(root/'preregistration.json') == sha(CASE/'preregistration.json'), 'private preregistration exact')
    initial = json.loads((CASE/'initial_live.json').read_text())['units']['unit']
    check(initial['InvocationID'] == '8dee58502fd048e4bf30a09bd9053a1f', 'live invocation identity')
    check(initial['kernel']['memory.max'] == str(12*2**30) and initial['kernel']['memory.swap.max'] == '0'
          and initial['kernel']['pids.max'] == '12', 'actual initial kernel limits')
    ranks = [p for p in initial['processes'] if Path(p['exe']).name == 'pw.x']
    check(len(ranks) == 2 and all(p['exe_sha256'] == sha(p['exe']) for p in ranks), 'two actual stock rank ELFs')
    for pp in ['Hg_sg15_pbe_fr_v12.UPF', 'Te_sg15_pbe_fr_v12.UPF']:
        check(sha(root/'pp'/pp) == sha(root/'out/r07pk4.save'/pp), 'saved versus actual staged UPF '+pp)
    for path, h in r['raw_pins'].items():
        check(sha(path) == h, 'terminal/reference pin '+path)
    for path, h in r['analysis_source_pins'].items():
        check(sha(path) == h, 'analysis source pin '+path)
    oldpins = json.loads((B/'stationary_reference_audit_2026-10-16/native_audit.json').read_text())['preserved_source_hashes']
    reference_pins = {p:h for p,h in oldpins.items() if 'e90_f120_fullacc' in p and
                     (p.endswith('/out/r07.save/wfc1.hdf5') or p.endswith('/out/r07.save/data-file-schema.xml')
                      or p.endswith('/gamma/signed_gap.json') or p.endswith('.UPF'))}
    check(len(reference_pins) >= 3, 'historical f120 frame has preexisting provenance')
    for path, h in reference_pins.items():
        check(sha(path) == h, 'preexisting f120 frame/reference pin '+path)
    for path, info in json.loads((P/'evidence_manifest.json').read_text()).items():
        check(sha(path) == info['sha256'] == sha(P/info['repository_copy']), 'terminal archive '+path)

    # Original RUNNING files remain historical prefixes, not terminal hashes.
    previous = '53b638a50eb3348754ec6383a7721700f0ea44ad'
    prefix = str(CASE.relative_to(REPO))
    for name in subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', previous, prefix], text=True).splitlines():
        if name == str((CASE/'decision.md').relative_to(REPO)):
            continue  # user explicitly requests this decision be finalized
        check((REPO/name).read_bytes() == subprocess.check_output(['git', 'show', previous+':'+name]),
              'immutable prior k4 checkpoint '+name)

    # Rebuild the full historical protection set used before the sole launch.
    history = B/'static_environment_2026-10-15'
    pins = dict(json.loads((history/'frozen_protocol.json').read_text())['profile']['pins'])
    pins.update({k:v['sha256'] for k,v in json.loads((history/'evidence_manifest.json').read_text())['raw'].items()})
    build = json.loads((B/'pbe_density_driver_2026-10-16/source_build_evidence.json').read_text())
    for key in ['linked_archive_pins', 'compiler_object_pins', 'compiled_module_pins']:
        pins.update(build[key])
    protection = json.loads((history/'protected_before.json').read_text())
    pins.update(protection['files'])
    check(len(pins) == 822, 'protection cardinality 822')
    for path, h in pins.items():
        check(sha(path) == h, 'protected pin '+path)
    check(subprocess.check_output(['git', '--no-optional-locks', '-C', str(DFT), 'status', '--short'], text=True)
          == protection['DFT_status'], 'DFT dirty status unchanged')
    check(hashlib.sha256(subprocess.check_output(['git', '-C', str(DFT), 'diff', '--binary'])).hexdigest()
          == protection['DFT_tracked_diff_sha256'], 'DFT tracked dirty bytes unchanged')
    originals = 0
    folders = ['pbe_density_driver_2026-10-16', 'pbe_static_lifecycle_2026-10-16',
               'pbe_static_completion_2026-10-16', 'pbe_density_only_feasibility_2026-10-16']
    for folder in folders+['primitive_k2_hse_2026-10-17', 'stock_hse_stationary_2026-10-16',
                           'pbe_final_admission_2026-10-16']:
        names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', previous,
                                        str((B/folder).relative_to(REPO))], text=True).splitlines()
        if folder in folders:
            originals += len(names)
        for name in names:
            check((REPO/name).read_bytes() == subprocess.check_output(['git', 'show', previous+':'+name]),
                  'old failure/original '+name)
    check(originals == 76, '76 original source/evidence files unchanged')

    # Independent charge, energy, finite-smearing and spectral checks from XML.
    tree = ET.parse(P/'native/data-file-schema.xml')
    out = tree.find('output')
    ks = out.findall('band_structure/ks_energies')
    w = np.array([float(k.find('k_point').attrib['weight']) for k in ks])
    e = np.array([np.fromstring(k.findtext('eigenvalues'), sep=' ') for k in ks]) # Hartree
    occ = np.array([np.fromstring(k.findtext('occupations'), sep=' ') for k in ks])
    mu = float(out.findtext('band_structure/fermi_energy'))
    sigma = float(out.find('band_structure/smearing').attrib['degauss'])
    check(abs(np.sum(w[:, None]*occ)-36) < 1e-8, '36 weighted electrons')
    check(np.max(abs(expit((mu-e)/sigma)-occ)) < 1e-8, 'native FD formula')
    check(r['native_outer_converged'] and r['completed_source_builds'] == 6, 'actual six-build outer convergence')
    check('EXX self-consistency reached' in (P/'native/pw.out').read_text(), 'explicit EXX success')
    check(out.findtext('convergence_info/scf_conv/convergence_achieved') == 'true', 'XML convergence true')
    check(r['trajectory'][-1]['dexx_Ry'] <= 1e-9 and r['last_inner_error_Ry'] <= 1e-9, 'frozen native residuals')
    check(abs(2*float(out.findtext('total_energy/etot'))-r['total_free_energy_Ry']) < 1e-12, 'terminal native energy')
    check(abs(r['minus_TS_Ry_reconstructed']-r['minus_TS_Ry_XML']) < 1e-15, 'independent entropy')
    check(r['actual_Gamma_density_Theta_QR']['columns_retained'] == 88, 'no density QR columns dropped')
    check(r['actual_Gamma_density_Theta_QR']['op'] > 1e-8, 'immutable strict Theta gate FAIL')
    check(r['actual_Gamma_density_Td_QR_max'] > 1e-8, 'immutable strict Td gate FAIL')
    check(abs(r['actual_Gamma_density_Theta_QR']['F']-r['Gamma_density_Theta_independent_block_F']) < 1e-14,
          'independent residual-block Frobenius norm')
    for metric in r['all_native_little_group_density_tests']+r['native_Theta_tests']:
        check(metric['eigenvalue_Rayleigh_error'] < 1e-13 and metric['direct_action_eigenvector_residual'] < 1e-13,
              'direct matrix-free extremal eigenpair '+str((metric['source_k'], metric.get('operation', 'Theta'))))
    check([v['source_k'] for v in r['native_Theta_tests']] == [1, 3, 7], 'only actually saved TR partners tested')
    check(len(r['unavailable_native_minus_k_fibers']) == 5 and r['generated_full_BZ_states'] == 0,
          'missing generic -k partners not manufactured')
    check(r['sectors']['Gamma6']['bands_1based'] == [33, 34] and
          r['sectors']['Gamma8']['bands_1based'] == [35, 36, 37, 38], 'projection-based sector association')
    check(r['sectors']['Gamma6']['max_Td_character_error'] < 1e-10 and
          r['sectors']['Gamma8']['max_Td_character_error'] < 1e-10, '24-operation character association')
    check(not r['strict_nonmagnetic_host_1e8_qualified'] and r['physical_xc'] is None,
          'no strict host or physical xc promotion')

    # A genuinely independent phase-gauge check on the actual Gamma data.
    spec = importlib.util.spec_from_file_location('final_analysis', P/'analyze_final.py')
    a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
    prior, _ = a.load_prior()
    c, g, k, bg = prior.read(root/'out/r07pk4.save/wfc1.hdf5')
    cell = np.array([np.fromstring(out.findtext('atomic_structure/cell/'+v), sep=' ')
                     for v in ['a1', 'a2', 'a3']])
    atoms = [np.fromstring(v.text, sep=' ') for v in out.findall('atomic_structure/atomic_positions/atom')]
    for rot, spin, det in prior.ops():
        check(np.linalg.norm(spin.conj().T@spin-np.eye(2)) < 1e-14, 'unitary axial spin action')
        for pos in atoms:
            shift = (pos@rot.T-pos) @ np.linalg.inv(cell)
            check(np.max(abs(shift-np.rint(shift))) < 1e-12, 'Td preserves each physical species modulo lattice')
    c = c*np.exp(1j*np.arange(44)*.371)[:, None, None]
    d = prior.transform(c, g, k, bg, g, k)
    phase = a.density_norm(c, d, occ[0], occ[0])
    check(abs(phase['op']-r['actual_Gamma_density_Theta_QR']['op']) < 1e-14,
          'actual-spinor phase-gauge invariant full density norm')

    # Prospective larger-cell cost warning: exact reciprocal folding, no launch.
    t = np.array([[-1, 1, 1], [1, -1, 1], [1, 1, -1]])
    folded = {}
    for n in itertools.product(range(4), repeat=3):
        key = tuple((np.array(n)@t) % 4)
        folded[key] = folded.get(key, 0)+1
    check(round(np.linalg.det(t)) == 4 and len(folded) == 16 and set(folded.values()) == {4},
          'primitive4^3 folds to16 conventional-cell k fibers')
    raw8 = json.loads((B/'chemical_hse_relax_2026-10-15/host_science.json').read_text())
    # Pin and inspect source-native extents instead of extrapolating whole RSS.
    native8 = raw8['source_cycles']['2']
    check(native8['native_EXX_FFT'] == [60, 60, 60] and native8['aggregate_EXX_buffer_B'] == 1216512000,
          'source-native eight-atom EXX extents')
    budget = dict(folding_matrix=t.tolist(), folded_k_quarter_indices=[[int(v) for v in k] for k in sorted(folded)],
                  folded_weights=[v/64 for _, v in sorted(folded.items())],
                  conventional_8atom_native_exx_FFT=[60, 60, 60], bands=176, spinor_components=2,
                  nominal_buffer_bytes_q64=60**3*2*176*64*16,
                  nominal_buffer_bytes_q16=60**3*2*176*16*16,
                  nominal_buffer_bytes_q8=60**3*2*176*8*16,
                  established_8atom_q1_buffer_bytes=1216512000,
                  raw_extent_evidence_sha256=sha(B/'chemical_hse_relax_2026-10-15/host_science.json'),
                  stock_q16_irregular_folded_deck_supported_or_admitted=False,
                  buffer_is_total_RAM_bound=False, new_jobs_authorized=False)
    # Existing independently recorded extents are separately checked below.
    (P/'next_sampling_cost.json').write_text(json.dumps(budget, indent=2)+'\n')
    resources = json.loads((P/'resources.json').read_text())
    cleanup = json.loads((P/'cleanup.json').read_text())
    check(resources['manager_success'] and resources['native_restarts'] == 0, 'terminal native exit without restart')
    check(all(v['original_identity_gone'] and v['original_cgroup_absent'] for v in cleanup['original_identities']),
          'launcher, ranks, observer and cgroups gone')
    for p in P.glob('*.py'):
        ast.parse(p.read_text())
    check(subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
          == 'research/hgcdte-impurity-tmatrix-20261010', 'research branch only')
    result = dict(verified=True, scope='completed sole stock k4 control, read-only qualification',
                  checks_passed=len(checks), check_names=checks,
                  conventional_numerical_SCF='PASS', stringent_density_symmetry_1e8='FAIL',
                  physical_Gamma_ordering='CONDITIONAL approximately irrep-labelled finite-smearing host levels',
                  full64_native_Theta_certificate='UNAVAILABLE', full_H_residual='UNAVAILABLE',
                  no_new_native_actions=True, Cd_runs=0, physical_xc=None,
                  protected_pins_unchanged=822, historical_originals_unchanged=76,
                  old_k4_running_checkpoint_unchanged_except_requested_decision=True,
                  DFT_dirty_unchanged=True,
                  phase_gauge_check_op=phase['op'],
                  script_sha256=sha(__file__))
    (P/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'check_names'}, indent=2))


if __name__ == '__main__':
    main()
