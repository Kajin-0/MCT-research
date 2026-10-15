"""Read-only protected-state/links and focused result validation (no QE/MPI)."""
import ast
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
DFT = Path('/home/User/opencode_workspace/DFT')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1024*1024), b''):
            h.update(data)
    return h.hexdigest()


def git(*args, repo=REPO):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def main():
    branch = git('branch', '--show-current').decode().strip()
    assert branch == 'research/hgcdte-impurity-tmatrix-20261010'
    pins = json.loads((HERE/'protected_inputs.json').read_text())
    old = {}
    for rel, expected in pins['prior_files'].items():
        actual = sha(REPO/rel)
        assert actual == expected, rel
        old[rel] = actual
    dft_diff = hashlib.sha256(git('diff', '--binary', repo=DFT)).hexdigest()
    assert dft_diff == pins['DFT_tracked_diff_sha256']
    stock = DFT/'.local/qe-env/bin/pw.x'
    stock_sha = sha(stock)
    assert stock_sha == '1d66c7856f5d6b3cd9c66b8578e01512b16bbe907b4360e54234890712ccd6a1'
    touched = git('diff', '--name-only', '89ef0f1').decode().splitlines()
    for path in touched:
        assert (path.startswith('research/programs/microscopic_bandgap/') or
                path in ['research/contribution_registry.md',
                         'research/portfolio_state.md']), path
    source_hashes = {}
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text(), filename=str(p))
        source_hashes[p.name] = sha(p)
    link_count = 0
    for p in HERE.glob('*.md'):
        for rel in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text()):
            if rel.startswith(('https://', 'http://', '#')):
                continue
            path = rel.split('#')[0]
            assert (p.parent/path).exists(), (p.name, rel)
            link_count += 1
    results = {}
    for name in ['accounting', 'sharp_atom', 'identifiability']:
        result = json.loads((HERE/f'{name}_checks.json').read_text())
        assert result['status'] == 'PASS'
        assert result['material_validation'] is False
        assert result['physical_xc'] is None
        results[name] = result
    assert results['accounting']['projected_difference_positive_Im'] > 0
    assert results['accounting']['own_reference_responses_identical']
    assert len(results['sharp_atom']['continuum_atom_checks']) == 6
    for row in results['sharp_atom']['continuum_atom_checks']:
        assert row['atom_root_distance'] <= row['guaranteed_radius']
        assert row['actual_perturbed_root_error'] <= row['perturbation_root_bound']
    assert results['identifiability']['N3_invisible_on_all_sampled_environments']
    assert results['identifiability']['actual_retained16_geometry_histograms'][
        'shared_x25'] == [2, 4, 2, 0, 0]
    t = results['identifiability']['threshold_inverse_zero_atom_counterexamples']
    assert t[0]['sharp_weight'] == 0 and t[0]['zero_boundary_damping']
    assert t[1]['sharp_weight'] > .75
    out = dict(status='PASS', timestamp_UTC=datetime.now(timezone.utc).isoformat(),
        baseline='89ef0f1', branch=branch,
        focused_checks=['accounting', 'sharp_atom', 'identifiability'],
        source_sha256=source_hashes, local_markdown_links_checked=link_count,
        prior_frozen_files_verified=old, DFT_tracked_diff_sha256=dft_diff,
        stock_QE_sha256=stock_sha, native_jobs_launched=0,
        protected_state_preserved=True, material_validation=False,
        physical_xc=None, paper_novelty='UNVERIFIED',
        Alowa_full_text_comparison='INCOMPLETE; publisher preview only')
    (HERE/'verification.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
