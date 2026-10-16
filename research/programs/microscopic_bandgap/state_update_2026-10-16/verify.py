"""Focused provenance/source/gate checks; no protected writes or native calls."""
from pathlib import Path
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = HERE.parents[3]
DFT = Path('/home/User/opencode_workspace/DFT')


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    r = json.loads((HERE/'result.json').read_text())
    t = json.loads((HERE/'independent_results.json').read_text())
    assert r['source_state_admission'] is False and t['passed']
    assert r['numeric_chemical_2meV_certified'] is False
    assert t['native_reader_implemented_or_compiled'] is False
    assert r['owner_admission'] == 'NOT_ATTEMPTED_AFTER_SOURCE_REFUSAL'
    for p, h in r['source_pins'].items():
        assert sha(p) == h, p
    frozen = json.loads((BASE/'single_state304_2026-10-15/frozen_protocol.json').read_text())
    for p in ['trial.npz', 'expected_density.npz']:
        path = DFT/'.local/qe75_lowram_20261011/h8u_20261015'/p
        assert sha(path) == frozen['profile']['pins'][str(path)]
    rawpin = json.loads((BASE/'hse_residual_response_2026-10-15/result.json').read_text())
    assert sha(DFT/'.local/qe75_lowram_20261011/h8u_20261015/full_actions.npz') == rawpin['source_full_action_sha256']
    guard = json.loads((BASE/'same_density_hamiltonian_2026-10-15/protected_after.json').read_text())
    for p, h in guard['files'].items():
        assert sha(p) == h
    qsrc = DFT/'.local/qe75_lowram_20261011/q-e'
    reviewed = {}
    for rel, markers in {
        'PW/src/h_psi.f90': ['IF ( use_ace ) THEN', 'CALL vexx( lda, n, m, psi, hpsi, becp )'],
        'PW/src/sum_band.f90': ['CALL weights ( )', 'CALL sym_rho( nspin_mag, rho%of_g )'],
        'PW/src/exx.f90': ['occ(1:nbnd,ik) = wg(1:nbnd,ik) / wk(ik)',
                          'CALL poolcollect( nbnd, nks, occ, nkstot, x_occupation )'],
        'Modules/wgauss.f90': ['if (n.eq. - 99) then', 'maxarg = 200.d0'],
    }.items():
        p = qsrc/rel
        text = p.read_text()
        assert all(v in text for v in markers), rel
        reviewed[str(p)] = dict(sha256=sha(p),
            marker_lines={v: text[:text.index(v)].count('\n')+1 for v in markers})
    private = DFT/'.local/qe75_lowram_20261011/h8u_20261015/build1/source'
    run = (private/'run_pwscf.f90').read_text()
    assert run.index('CALL r07_same_density_H()') < run.index('RETURN ! fixed trial only')
    probe = (BASE/'single_state304_2026-10-15/probe_native.inc').read_text()
    assert 'IF(ANY(wg(1:142,1)/=1._DP)' in probe
    assert 'entropy=4._DP*LOG(2._DP)' in probe
    assert 'tfixed_occ=.TRUE.;et=0._DP' in probe
    weights = np.load(HERE/'trial_coordinates.npz')['occupations'][:176]
    assert np.any(weights[142:146] != .5)
    geometry = {}
    for member, species in [('host', ['Hg']*4+['Te']*4), ('cd', ['Cd']+['Hg']*3+['Te']*4)]:
        p = BASE/'chemical_hse_relax_2026-10-15/evidence'/member/'pw.in'
        text = p.read_text()
        lines = text.split('ATOMIC_POSITIONS crystal\n')[1].splitlines()[:8]
        actual = [s.split()[0] for s in lines]
        positions = np.array([[float(v) for v in s.split()[1:4]] for s in lines])
        assert actual == species
        np.testing.assert_array_equal(4*positions,
            np.load(HERE/'trial_coordinates.npz')['host_quarter_positions'])
        assert '6.46 0 0' in text and 'ecutwfc=50' in text and 'ecutrho=200' in text
        geometry[member] = dict(path=str(p), sha256=sha(p), actual_species=actual)
    # All previously tracked files, except the two requested navigation updates,
    # must remain byte-identical. This includes frozen failures and registry.
    changed = subprocess.check_output(['git', 'diff', '--name-only', 'be13479'],
                                      cwd=REPO, text=True).splitlines()
    allowed = {str((BASE/n).relative_to(REPO)) for n in ['state.md', 'SUCCESSOR_HANDOFF.md']}
    prefix = str(HERE.relative_to(REPO))+'/'
    assert all(p in allowed or p.startswith(prefix) for p in changed), changed
    old_handoff = subprocess.check_output(['git', 'show',
        'be13479:research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md'], cwd=REPO).decode()
    new_handoff = (BASE/'SUCCESSOR_HANDOFF.md').read_text()
    start = '<!-- STATE_UPDATE_20261016_BEGIN -->\n'
    end = '<!-- STATE_UPDATE_20261016_END -->\n\n'
    assert new_handoff.count(start) == new_handoff.count(end) == 1
    begin = new_handoff.index(start)
    finish = new_handoff.index(end)+len(end)
    assert new_handoff[:begin]+new_handoff[finish:] == old_handoff
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text())
    memory = {line.split(':')[0]: int(line.split()[1])*1024
              for line in Path('/proc/meminfo').read_text().splitlines()
              if line.startswith(('MemAvailable:', 'MemTotal:'))}
    st = os.statvfs(REPO)
    out = dict(status='PASS_READ_ONLY_STATE_AND_PROSPECTIVE_PROTOCOL; NATIVE_NOT_ADMITTED',
        timestamp_UTC=datetime.now(timezone.utc).isoformat(), baseline='be13479',
        branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip(),
        immutable_input_source_ELF_PP_pins=len(r['source_pins']),
        derived_trial_and_full_action_match_original_pins=True,
        original_geometry_independently_verified=geometry,
        native_source_paths=reviewed,
        first_blocker='Existing executable enforces the old fixed-occupation template and returns before any occupied solve/state update.',
        old_reader_refuses_D1=True,
        protected_pinned_DFT_files_and_stock_unchanged=True,
        all_old_MCT_files_except_requested_navigation_unchanged=True,
        entire_previous_successor_handoff_preserved=True,
        contribution_registry_status_unchanged=True,
        informational_host_capacity_NOT_admission={**memory,'available_disk_B':st.f_bavail*st.f_frsize},
        new_owner_or_resource_admission_attempted=False,
        native_jobs=0, builds=0, DFT_writes=0, Cd_runs=0,
        numeric_chemical_2meV_certified=False, physical_xc=None,
        new_package_source_sha256={p.name:sha(p) for p in sorted(HERE.iterdir())
                                   if p.is_file() and p.name != 'verification.json'})
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','immutable_input_source_ELF_PP_pins',
        'first_blocker','native_jobs','numeric_chemical_2meV_certified']},indent=2))


if __name__ == '__main__':
    main()
