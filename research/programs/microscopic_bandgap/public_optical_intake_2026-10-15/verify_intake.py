"""Offline evidence consistency/preservation check; no network, spectra or native jobs."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DFT = Path('/home/User/opencode_workspace/DFT')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    pins = json.loads((HERE / 'protected_inputs.json').read_text())
    evidence = json.loads((HERE / 'sources.json').read_text())
    assert git('branch', '--show-current') == 'research/hgcdte-impurity-tmatrix-20261010'
    subprocess.run(['git', 'merge-base', '--is-ancestor', pins['baseline'], 'HEAD'],
                   cwd=ROOT, check=True)
    for rel, pin in pins['frozen_files'].items():
        path = ROOT / rel
        assert path.stat().st_size == pin['bytes'], rel
        assert digest(path) == pin['sha256'], rel
    dft_diff = sha256(subprocess.check_output(['git', 'diff', '--binary'], cwd=DFT)).hexdigest()
    assert dft_diff == pins['DFT_tracked_diff_sha256']
    assert digest(DFT / '.local/qe-env/bin/pw.x') == pins['stock_QE_sha256']

    ids = {s['id'] for s in evidence['sources']}
    assert len(ids) == len(evidence['sources'])
    for item in evidence['sources']:
        assert urlparse(item['url']).scheme == 'https'
        assert all(item.get(k) for k in ['kind', 'access', 'location', 'finding'])
    assert len(evidence['queries']) == 8
    for c in evidence['candidates']:
        assert set(c['sources']) <= ids
        assert len(c['criteria']) == 8
        assert c['criteria']['public_authentic_raw_profiles'] == 'NOT_LOCATED'
        assert c['public_complete_package'] == 'NO' and c['accepted'] is False
        assert c['retained_raw_existence'] == 'UNKNOWN'
    assert evidence['physical_xc'] is None
    assert evidence['outreach_sent'] is False
    assert evidence['author_request'] == 'UNSENT_DRAFT'
    assert all(evidence[k] == 0 for k in
               ['binary_downloads', 'new_raw_datasets_accepted', 'new_spectral_analyses', 'native_jobs'])
    assert evidence['original_Stage0_unchanged'] is True
    draft = (HERE / 'draft_request.md').read_text()
    assert 'DRAFT ONLY — NOT SENT' in draft
    assert '[Your name / affiliation]' in draft
    assert 'Frederic.Teppe@umontpellier.fr' in draft

    # Protect the complete old handoff, not just selected numerical claims.
    handoff = ROOT / 'research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md'
    old = subprocess.check_output(['git', 'show', f"{pins['baseline']}:{handoff.relative_to(ROOT)}"],
                                  cwd=ROOT, text=True)
    current = handoff.read_text()
    start = current.index('## Latest finite public optical intake COMPLETE')
    end = current.index('## Latest competing-route phase COMPLETE', start)
    assert current[:start] + current[end:] == old

    links = 0
    for md in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', md.read_text()):
            if urlparse(target).scheme or target.startswith('#'):
                continue
            assert (md.parent / target.split('#', 1)[0]).exists(), (md.name, target)
            links += 1
    allowed = {'research/programs/microscopic_bandgap/state.md',
               'research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md',
               'research/contribution_registry.md'}
    prefix = str(HERE.relative_to(ROOT)) + '/'
    changed = set(git('diff', '--name-only', pins['baseline']).splitlines())
    assert all(s in allowed or s.startswith(prefix) for s in changed), changed
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)

    result = dict(status='PASS_EVIDENCE_CONSISTENCY_AND_PRESERVATION_ONLY',
                  timestamp_UTC=datetime.now(timezone.utc).isoformat(),
                  baseline=pins['baseline'],
                  decision=evidence['decision'],
                  public_raw_intake='NO_GO',
                  independently_qualified_material_dataset=False,
                  physical_xc=None,
                  frozen_files_checked=len(pins['frozen_files']),
                  source_routes_checked=len(ids), specimen_candidates=len(evidence['candidates']),
                  targeted_queries=len(evidence['queries']), local_links_checked=links,
                  prior_handoff_content_preserved=True,
                  DFT_tracked_diff_sha256=dft_diff,
                  stock_QE_sha256=pins['stock_QE_sha256'],
                  package_sha256={f.name: digest(f) for f in sorted(HERE.iterdir())
                                  if f.is_file() and f.name != 'verification.json'},
                  limits='Offline checks do not prove global archive absence or current retention, '
                         'remote content immutability, calibration, raw-data rights or mailbox operation. '
                         'Web evidence is the manually audited source chronology; no scientific test rerun.')
    (HERE / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'package_sha256'}, indent=2))


if __name__ == '__main__':
    main()
