"""Focused read-only verification of one native negative result; no jobs or repairs."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

P = Path(__file__).resolve().parent
B = P.parent
REPO = P.parents[3]
DFT = Path('/home/User/opencode_workspace/DFT')
BASE = 'a3f49cb5ab7b229eccc413084cace906b37150c6'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def check(condition, name):
    if not condition:
        raise RuntimeError(name)


def git(*args, cwd=REPO):
    return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=cwd)


def main():
    f = json.loads((P / 'preregistration.json').read_text())
    state = json.loads((P / 'host_state_result.json').read_text())
    readback = json.loads((P / 'native_readback.json').read_text())
    res = json.loads((P / 'resources.json').read_text())
    term = json.loads((P / 'host_terminal_manager.json').read_text())
    raw = json.loads((P / 'raw_manifest.json').read_text())
    for path, info in raw['files'].items():
        check(sha(path) == info['sha256'], 'native file changed: ' + path)
    host = Path(f['members']['host']['root'])
    for archived, original in [('host_pw.out', host / 'pw.out'),
                               ('host_pw.err', host / 'pw.err'),
                               ('host_data-file-schema.xml', host / 'out/r07hse8.save/data-file-schema.xml')]:
        check((P / archived).read_bytes() == original.read_bytes(), 'byte-exact native archive: ' + archived)
    check(json.loads((P / 'analysis_stdout.json').read_text()) == state, 'actual analysis stdout')
    for member, info in f['members'].items():
        root = Path(info['root'])
        check(sha(root / 'pw.in') == info['input_sha256'], 'input')
        check(sha(root / 'reference.bin') == info['reference_sha256'], 'physical reference')
        for pp, h in info['PP'].items():
            check(sha(root / 'pp' / pp) == h, 'PP')
    check(sha(f['stock_ELF']) == f['stock_sha256'], 'stock ELF')
    for p, h in f['backends'].items():
        check(sha(p) == h, 'stock backend')
    check(len(state['trajectory']) == 78 and not state['native_outer_converged'], '79 builds, no outer SCF')
    check(state['XML_convergence'] == 'false' and state['trajectory'][-1]['dexx_Ry'] > 1e-9, 'native failure')
    text = (P / 'host_pw.out').read_bytes()
    check(text.startswith((P / 'checkpoint_stdout.txt').read_bytes()), 'continuous native stdout prefix')
    check(b'Maximum CPU time exceeded' in text and b'10486.87' in text
          and b'EXX self-consistency reached' not in text, 'native time-stop evidence')
    check(abs(state['charge_error_e']) < 1e-8 and state['FD_max_error'] < 1e-8, 'FD/charge')
    check(abs(readback['density_charge_residual_e']) < 1e-8
          and abs(readback['density_charge_residual_e'] - state['charge_error_e']) < 1e-10,
          'independent saved scalar density and orbital charge')
    qr = state['full_density_Theta_independent_QR_op']
    prior = state['full_density_Theta']
    check(prior['compressed_operator_witness'] - 1e-10 <= qr
          <= prior['full_F_upper_arithmetic'] + 1e-10, 'independent whole-density norms')
    check(qr > 1e-8 and state['independent_scalar_Theta_check_error'] < 1e-10, 'independent scalar negative witness')
    check(not state['symmetry_certified'] and not state['stationary_nonmagnetic_host_accepted'], 'no false nonmagnetism')
    check(not state['Cd_launched'] and state['physical_xc'] is None, 'scientific withholding')
    check(not list(Path(f['members']['cd']['root']).glob('pw.out')), 'Cd never launched')
    check(res['elapsed_OS_wall_s'] < 10800 and res['retained_manager_memory_peak_B'] < 12*(1 << 30), 'bounded native run')
    check(res['swap_current_max_B'] == 0 and res['sampled_tasks_peak'] <= 12, 'kernel resources')
    check(res['sampled_host_available_min_B'] >= 4*(1 << 30)
          and res['sampled_disk_free_min_B'] >= 10*(1 << 30), 'host floors')
    check(res['fresh_retained_blocks_B'] <= 14*(1 << 30), 'retained own output')
    check(term['manager']['NRestarts'] == '0' and term['native_processes_gone'], 'single unit, original ranks gone')
    check(not Path(term['original_cgroup_path']).exists(), 'old own cgroup absent')
    check('LoadState=not-found' in json.loads((P / 'cleanup.json').read_text())['after'], 'unit cleanup')
    check(json.loads((P / 'monitor_terminal_failure.json').read_text())['exit_code'] == 1,
          'terminal sampler failure preserved')

    old = B / 'static_environment_2026-10-15'
    pins = dict(json.loads((old / 'frozen_protocol.json').read_text())['profile']['pins'])
    pins.update({n: v['sha256'] for n, v in json.loads((old / 'evidence_manifest.json').read_text())['raw'].items()})
    build = json.loads((B / 'pbe_density_driver_2026-10-16/source_build_evidence.json').read_text())
    for key in ('linked_archive_pins', 'compiler_object_pins', 'compiled_module_pins'):
        pins.update(build[key])
    protection = json.loads((old / 'protected_before.json').read_text())
    pins.update(protection['files'])
    check(len(pins) == 822, 'original pin count')
    for path, h in pins.items():
        check(sha(path) == h, 'protected file changed: ' + path)
    check(git('status', '--short', cwd=DFT).decode() == protection['DFT_status'], 'DFT status unchanged')
    check(hashlib.sha256(git('diff', '--binary', cwd=DFT)).hexdigest()
          == protection['DFT_tracked_diff_sha256'], 'DFT tracked bytes unchanged')
    historical = []
    folders = ('pbe_density_driver_2026-10-16', 'pbe_static_lifecycle_2026-10-16',
               'pbe_static_completion_2026-10-16', 'pbe_density_only_feasibility_2026-10-16')
    for folder in (*folders, 'pbe_final_admission_2026-10-16', 'hse_pair_admission_2026-10-16'):
        names = git('ls-tree', '-r', '--name-only', BASE, str((B / folder).relative_to(REPO))).decode().splitlines()
        for name in names:
            check((REPO / name).read_bytes() == git('show', BASE + ':' + name), 'historical file changed: ' + name)
        if folder in folders:
            historical.extend(names)
    check(len(historical) == 76, 'historical originals count')
    check(git('branch', '--show-current').decode().strip()
          == 'research/hgcdte-impurity-tmatrix-20261010', 'research branch')
    result = dict(UTC=datetime.now(timezone.utc).isoformat(), verified=True,
                  meaning='Verification of measured NEGATIVE result; not host/monitor scientific PASS',
                  protected_pins_unchanged=822, original_historical_files_unchanged=76,
                  closed_PBE_and_prior_HSE_audit_unchanged=True,
                  native_families=1, native_restarts=0, Cd_runs=0,
                  source_or_stock_changes=0, old_REFUSALS_unchanged=True,
                  raw_file_count=len(raw['files']), native_outer_converged=False,
                  independent_Theta_norm=qr, unit_cleaned=True,
                  monitor_failure_not_reclassified=True, physical_xc=None,
                  package_pins={p.name: sha(p) for p in sorted(P.iterdir())
                                if p.is_file() and p.name != 'verification.json'})
    (P / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'package_pins'}, indent=2))


if __name__ == '__main__':
    main()
