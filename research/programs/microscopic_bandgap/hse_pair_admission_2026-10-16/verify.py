"""Independent read-only checks of this finite admission decision; no native launch.

Run from any cwd with PYTHONDONTWRITEBYTECODE=1 python3 /absolute/path/verify.py.
Writes only this new package's verification.json. Does not import old runners.
"""
import hashlib
import json
import struct
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

P = Path(__file__).resolve().parent
B = P.parent
REPO = P.parents[3]
DFT = Path('/home/User/opencode_workspace/DFT')
BASELINE = 'bd71deacf79e670419a80e8f4c9262dcaeed3274'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def check(value, name):
    if not value:
        raise RuntimeError(name)


def git(*args, cwd=REPO):
    return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=cwd)


def main():
    a = json.loads((P / 'audit.json').read_text())
    check(a['verdict'] == 'NO_GO_BEFORE_EXECUTION', 'verdict')
    pins = dict(a['pinned_sources_inputs'])
    pins.update(a['backends'])
    for name, value in pins.items():
        check(sha(name) == value, 'audit pin changed: ' + name)

    # Separate native guard/manager/final records, not the timing summary alone.
    guards = {}
    for member, m in a['matched_archived_model'].items():
        root = Path(m['input']).parent
        paths = [root / n for n in ('GUARD_RESULT.json', 'FINAL.json', 'READY.json')]
        guard, final, ready = (json.loads(p.read_text()) for p in paths)
        check(guard['pass_guard'] and not final['HSE_converged'], 'finite scope vs SCF')
        expected = a['accepted_two_build_timing'][member]
        check(guard['elapsed_s'] == expected['guard_wall_s'], 'native elapsed')
        check(guard['peak_kernel_memory_B'] == expected['kernel_peak_B'], 'native peak')
        check(guard['peak_sampled_RSS_B'] == expected['sampled_RSS_shared_overcount_B'], 'native RSS')
        check(abs(final['charge_residual_e']) < 1e-8, 'old finite charge')
        manager = ready['manager']
        for key, wanted in [('MemoryMax', 12 << 30), ('MemorySwapMax', 0), ('TasksMax', 12)]:
            check(int(manager[key]) == wanted, 'old recorded limit: ' + key)
        # These are archived observations, NOT a new live unit/cgroup check.
        guards[member] = dict(
            record_pins={str(p): sha(p) for p in paths},
            finite_acquisition_accepted=final['accepted'],
            outer_converged=final['HSE_converged'],
            charge_residual_e=final['charge_residual_e'],
            elapsed_s=guard['elapsed_s'], kernel_peak_B=guard['peak_kernel_memory_B'])

        # Independently recover raw distributed array capacities.
        total = 0
        for rank in (0, 1):
            path = root / 'pilot' / f'c2_before.rank{rank}'
            with path.open('rb') as f:
                h, ex = struct.unpack('<16q', f.read(128)), struct.unpack('<10q', f.read(80))
            check(h[3] == rank and h[7] == 176 and h[8] == 2, 'rank/band/spin header')
            check(ex[:3] == (60, 60, 60) and ex[4:7] == (216000, 176, 1), 'EXX extents')
            total += 16 * ex[4] * ex[5] * ex[6]
        check(total == 1216512000, 'independent EXX byte count')
        out = ET.parse(m['XML']).find('output')
        check(float(out.findtext('basis_set/ecutwfc')) == 25, 'Ha vs Ry cutoff')
        check(float(out.find('band_structure/smearing').attrib['degauss']) == .0005, 'Ha vs Ry sigma')
        atoms = out.find('atomic_structure/atomic_positions')
        check(len(atoms) == 8 and float(out.findtext('band_structure/nelec')) == 144, 'cell/charge metadata')

    eight = B / 'hybrid_convergence_2026-10-15'
    eight_job = json.loads((eight / 'frozen_protocol.json').read_text())['jobs']['host']
    eight_guard_path = Path(eight_job['root']) / 'GUARD_RESULT.json'
    eight_guard = json.loads(eight_guard_path.read_text())
    eight_native = json.loads((eight / 'host_native_result.json').read_text())
    check(abs(eight_guard['elapsed_s'] - a['rejected_eight_build_observed']['wall_s']) < .0005,
          'rounded historical eight-build wall')
    check(eight_guard['elapsed_s'] > 600 and not eight_native['HSE_converged']
          and eight_native['completed_source_builds'] == 8, 'rejected eight-build scope')

    # Verify the original 822-pin and 76-file protection contract independently.
    static = B / 'static_environment_2026-10-15'
    protected_pins = dict(json.loads((static / 'frozen_protocol.json').read_text())['profile']['pins'])
    protected_pins.update({n: v['sha256'] for n, v in json.loads((static / 'evidence_manifest.json').read_text())['raw'].items()})
    build = json.loads((B / 'pbe_density_driver_2026-10-16/source_build_evidence.json').read_text())
    for key in ('linked_archive_pins', 'compiler_object_pins', 'compiled_module_pins'):
        protected_pins.update(build[key])
    protected = json.loads((static / 'protected_before.json').read_text())
    protected_pins.update(protected['files'])
    check(len(protected_pins) == 822, 'protected inventory count')
    for name, value in protected_pins.items():
        check(sha(name) == value, 'protected pin changed: ' + name)
    check(git('status', '--short', cwd=DFT).decode() == protected['DFT_status'], 'DFT dirty status changed')
    dirty_hash = hashlib.sha256(git('diff', '--binary', cwd=DFT)).hexdigest()
    check(dirty_hash == protected['DFT_tracked_diff_sha256'], 'DFT dirty bytes changed')

    historical = []
    folders = ('pbe_density_driver_2026-10-16', 'pbe_static_lifecycle_2026-10-16',
               'pbe_static_completion_2026-10-16', 'pbe_density_only_feasibility_2026-10-16')
    for folder in (*folders, 'pbe_final_admission_2026-10-16'):
        relative = str((B / folder).relative_to(REPO))
        names = git('ls-tree', '-r', '--name-only', BASELINE, relative).decode().splitlines()
        for name in names:
            check((REPO / name).read_bytes() == git('show', BASELINE + ':' + name), 'historical change: ' + name)
        if folder in folders:
            historical.extend(names)
    check(len(historical) == 76, 'historical inventory count')
    gate_a = json.loads((B / 'pbe_static_lifecycle_2026-10-16/evidence/RESULT.json').read_text())['status']
    check(gate_a == 'REFUSED_ABSORBING', 'original Gate A')

    unknowns = ('complete_direct_SCF_peak_B', 'direct_full_SCF_wall_upper_s', 'full_scientific_output_upper_B')
    check(all(a[n] is None for n in unknowns), 'no fabricated upper bound')
    check(all(a[n] == 0 for n in ('new_material_jobs', 'new_services', 'new_builds', 'solver_ELFs_executed')), 'scope')
    check(a['PBE_closed'] and a['physical_xc'] is None, 'scientific boundary')
    check(git('branch', '--show-current').decode().strip() == 'research/hgcdte-impurity-tmatrix-20261010', 'research branch')

    result = dict(UTC=datetime.now(timezone.utc).isoformat(), passed=True,
                  baseline=BASELINE, audit_pin_count=len(pins),
                  protected_pins_unchanged=len(protected_pins),
                  original_historical_files_unchanged=len(historical),
                  final_PBE_package_byte_exact=True,
                  DFT_dirty_diff_sha256=dirty_hash, old_Gate_A=gate_a,
                  independent_native_records=guards,
                  eight_build_guard_sha256=sha(eight_guard_path),
                  eight_build_elapsed_s=eight_guard['elapsed_s'],
                  eight_build_stationary=False,
                  independent_EXX_bytes=1216512000,
                  new_native_executions=0,
                  evidence_pins={p.name: sha(p) for p in sorted(P.iterdir())
                                 if p.is_file() and p.name != 'verification.json'})
    (P / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('independent_native_records', 'evidence_pins')}, indent=2))


if __name__ == '__main__':
    main()
