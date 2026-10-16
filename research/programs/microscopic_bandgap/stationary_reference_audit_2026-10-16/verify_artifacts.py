"""Read-only provenance and inference guards; no commands executed in DFT."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE='9a83424'


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def main():
    report=json.loads((HERE/'native_audit.json').read_text())
    independent=json.loads((HERE/'independent_checks.json').read_text())
    metadata=json.loads((HERE/'metadata_audit.json').read_text())
    assert metadata['source_audit_sha256']==sha(HERE/'native_audit.json')
    assert report['baseline']==BASE and report['native_jobs']==0
    assert independent['physical_xc'] is None and not independent['stationary_FD_certified']
    for path,pin in report['preserved_source_hashes'].items():
        assert not path.endswith('/state.json')
        assert sha(path)==pin,path
    for pin in independent['protected_MCT']:
        p=ROOT/pin['path']
        assert sha(p)==pin['sha256'],str(p)
        baseline=subprocess.check_output(['git','show',BASE+':'+pin['path']],cwd=ROOT)
        assert hashlib.sha256(baseline).hexdigest()==pin['sha256']
    for row in report['records']:
        assert row['accepted_scf'] and row['exx_converged']
        assert abs(row['electron_count']-36)<1e-12
        assert row['Gamma_density_Td_compressed_witness_max']>1e-8
        assert row['Gamma_ACE_Td_probe_defect']>1e-8
        assert not row['Gamma_original_equals_expanded_bytes']
        assert 'mv' in row['smearing'] and row['sigma_Ry']==.001
    assert metadata['native_lattice_origin_species_PP_frames_equal']
    assert all(row['SCF_expanded_charge_datasets_equal'] for row in metadata['records'])
    for row in metadata['records']:
        assert sha(Path(row['run'])/'gamma/open_grid.out')==row['open_grid_stdout_sha256']
        assert row['open_grid_EXX_grid']==[54,54,54]
    memory=independent['memory_arithmetic']
    assert memory['original_16atom_f120_nominal_B']>memory['cap_12GiB_B']
    oldpins=json.loads((ROOT/'research/programs/microscopic_bandgap/public_optical_intake_2026-10-15/protected_inputs.json').read_text())
    stock=Path('/home/User/opencode_workspace/DFT/.local/qe-env/bin/pw.x')
    assert sha(stock)==oldpins['stock_QE_sha256']

    handoff=ROOT/'research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md'
    s=handoff.read_text()
    start=s.index('## Latest original-host reuse audit COMPLETE')
    end=s.index('## Latest finite public optical intake COMPLETE',start)
    old=subprocess.check_output(['git','show',BASE+':'+str(handoff.relative_to(ROOT))],cwd=ROOT,text=True)
    assert s[:start]+s[end:]==old
    count=0
    for p in HERE.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if urlparse(link).scheme or link.startswith('#'):continue
            assert (p.parent/link.split('#')[0]).exists(),(p.name,link)
            count+=1
    for p in HERE.glob('*.py'):ast.parse(p.read_text())
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    assert branch=='research/hgcdte-impurity-tmatrix-20261010'
    allowed={'research/programs/microscopic_bandgap/state.md',
             'research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md','research/contribution_registry.md'}
    prefix=str(HERE.relative_to(ROOT))+'/'
    changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=ROOT,text=True).splitlines()
    assert all(p in allowed or p.startswith(prefix) for p in changed)
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
    result=dict(status='PASS_SCOPED_READ_ONLY_ASSESSMENT',timestamp_UTC=datetime.now(timezone.utc).isoformat(),
        baseline=BASE,branch=branch,native_sources_rehashed=len(report['preserved_source_hashes']),
        protected_MCT_rehashed=len(independent['protected_MCT']),links_checked=count,
        entire_prior_handoff_preserved=True,stock_QE_sha256=sha(stock),
        reusable_numerical_reference_frame=True,strict_FD_or_DIRECT_H_state_certified=False,
        matched_16atom_stock_12GiB_admitted=False,native_jobs=0,physical_xc=None,
        source_hashes={p.name:sha(p) for p in HERE.iterdir() if p.is_file() and p.name!='verification.json'},
        limits='No native full-H/whole-FD/material certificate. Newly pinned private state files '
               'are not hosted here and not asserted historically fingerprinted. No DFT Git command '
               'or driver/write, no rerun of old examples/refused jobs.')
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_hashes'},indent=2))


if __name__=='__main__':main()
