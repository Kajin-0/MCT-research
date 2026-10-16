"""Focused provenance/protection checks, no DFT commands or native invocation."""
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse
from audit_retained import HERE, digest

BASE = '5dc77a9'
REPO = HERE.parents[3]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def main():
    report = json.loads((HERE/'retained_result.json').read_text())
    checks = json.loads((HERE/'independent_results.json').read_text())
    budget = json.loads((HERE/'source_and_budget.json').read_text())
    assert report['baseline'] == BASE and report['native_invocations'] == 0
    assert checks['passed'] and checks['native_invocations'] == budget['native_jobs'] == 0
    assert len(report['native_packet_pins']) == 32
    for p, v in report['native_packet_pins'].items():
        assert Path(p).stat().st_size == v['bytes'] and digest(p) == v['sha256']
    for p, s in budget['preserved_private_source_ELF_PP_pins'].items(): assert digest(p) == s
    for k in ('c1', 'c2', 'change'):
        a = report['chemical'][k]
        assert abs(a['trace_meV']-checks['actions'][k]['compensated_trace_meV']) < 1e-9
    assert report['chemical']['c2']['action_Q_leakage_opnorm_meV'] > 95
    assert min(report['chemical']['c2']['action_Q_leakage_singular_meV']) > 91
    assert report['chemical']['c2']['all_sector_Rayleigh_difference_interval_meV'][0] > 39
    assert checks['density_scalar_checks']['host_2']['absolute_witness'] > .001
    assert not budget['conditional_observable_contraction']['q_measured_or_certified']
    assert budget['memory_and_storage']['B_stream_exceeds_output_cap_B'] == 8*(1 << 30)
    assert budget['fixed_reference_embedding']['bitwise_embedded']

    # No edit to old acceptance/refusal files, including the repo guardrails.
    protected = ['AGENTS.md',
      'research/programs/microscopic_bandgap/chemical_hse_relax_2026-10-15/decision.md',
      'research/programs/microscopic_bandgap/hybrid_convergence_2026-10-15/decision.md',
      'research/programs/microscopic_bandgap/append_hamiltonian_2026-10-15/strict_refusal.json',
      'research/programs/microscopic_bandgap/static_environment_2026-10-15/decision.md',
      'research/programs/microscopic_bandgap/single_state304_2026-10-15/decision.md',
      'research/programs/microscopic_bandgap/qe75_streaming_2026-10-11/full_scf_2026-10-13/decision.md',
      'research/programs/microscopic_bandgap/qe75_streaming_2026-10-11/fermi_root_2026-10-14/decision.md',
      'research/programs/microscopic_bandgap/stationary_reference_audit_2026-10-16/verification.json']
    pins = {}
    for p in protected:
        assert (REPO/p).read_bytes() == git('show', BASE+':'+p)
        pins[p] = digest(REPO/p)
    hp = 'research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md'
    hand = (REPO/hp).read_text()
    start = hand.index('## Latest science-first screening feasibility COMPLETE')
    stop = hand.index('## Latest original-host reuse audit COMPLETE', start)
    assert hand[:start]+hand[stop:] == git('show', BASE+':'+hp).decode()
    branch = git('branch', '--show-current').decode().strip()
    assert branch == 'research/hgcdte-impurity-tmatrix-20261010'
    allowed = {'research/programs/microscopic_bandgap/state.md', hp, 'research/contribution_registry.md'}
    prefix = str(HERE.relative_to(REPO))+'/'
    changes = git('diff', '--name-only', BASE).decode().splitlines()
    untracked = git('ls-files', '--others', '--exclude-standard').decode().splitlines()
    assert all(p in allowed or p.startswith(prefix) for p in changes+untracked)
    links = 0
    for p in HERE.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if urlparse(link).scheme or link.startswith('#'): continue
            assert (p.parent/link.split('#')[0]).exists(), (p, link)
            links += 1
    for p in HERE.glob('*.py'): ast.parse(p.read_text())
    subprocess.run(['git', 'diff', '--check'], cwd=REPO, check=True)
    out = dict(status='PASS_READ_ONLY_SCIENTIFIC_FEASIBILITY_NO_NATIVE_ADMISSION',
      timestamp_UTC=datetime.now(timezone.utc).isoformat(), baseline=BASE, branch=branch,
      native_invocations=0, private_packet_pins_rechecked=32,
      private_source_ELF_PP_pins_rechecked=len(budget['preserved_private_source_ELF_PP_pins']),
      protected_MCT=pins, entire_prior_handoff_preserved=True, local_links_checked=links,
      physical_xc=None, new_native_acquisition_admitted=False,
      source_hashes={p.name:digest(p) for p in HERE.iterdir() if p.is_file() and p.name!='verification.json'},
      limitations='Shared packet layout with independent old-matrix reconstruction, QR and direct scalar methods; '
        'floating checks without directed-rounding enclosure. No full-H/state/material qualification. '
        'No DFT Git command/driver, source build/edit, native command or protected-tree write.')
    (HERE/'verification.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('protected_MCT','source_hashes')},indent=2))


if __name__ == '__main__': main()
