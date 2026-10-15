"""Focused analytical-result/protected-state verification; never native execution."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
DFT=Path('/home/User/opencode_workspace/DFT')


def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def git(*args,repo=REPO):
    return subprocess.check_output(['git','-C',str(repo),*args])


def main():
    pins=json.loads((HERE/'protected_inputs.json').read_text())
    branch=git('branch','--show-current').decode().strip()
    assert branch=='research/hgcdte-impurity-tmatrix-20261010'
    verified={}
    for rel,expected in pins['prior_files'].items():
        actual=sha(REPO/rel);assert actual==expected,rel;verified[rel]=actual
    r02=sha(REPO/'tools/analyze_kane_symmetry_intertwiner.py')
    assert r02==pins['R02_readonly_source_sha256']
    diffsha=hashlib.sha256(git('diff','--binary',repo=DFT)).hexdigest()
    assert diffsha==pins['DFT_tracked_diff_sha256']
    stock=sha(DFT/'.local/qe-env/bin/pw.x')
    assert stock=='1d66c7856f5d6b3cd9c66b8578e01512b16bbe907b4360e54234890712ccd6a1'
    for rel in git('diff','--name-only','c80147f').decode().splitlines():
        assert (rel.startswith('research/programs/microscopic_bandgap/competing_inversion_routes_2026-10-15/') or
                rel in ['research/programs/microscopic_bandgap/state.md',
                        'research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md',
                        'research/contribution_registry.md']),rel
    sources={}
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text(),filename=str(p));sources[p.name]=sha(p)
    links=0
    for p in HERE.glob('*.md'):
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
            if link.startswith(('http://','https://','#')):continue
            assert (p.parent/link.split('#')[0]).exists(),(p.name,link)
            links+=1
    results={}
    for name in ['route_A','route_B','resolution']:
        rr=json.loads((HERE/f'{name}_checks.json').read_text())
        assert rr['status']=='PASS' and rr['material_validation'] is False
        assert rr['physical_xc'] is None and rr['native_jobs']==0
        results[name]=rr
    a,b,c=[results[n] for n in ['route_A','route_B','resolution']]
    assert a['Td_operation_count']==24 and not a['exact_alloy_IR_exponent_claim']
    for row in a['Bernoulli_examples']:
        assert row['mean_vector_norm']<1e-12 and min(row['Gamma6_to_HH_weights'])>0
    mixture=b['zero_mean_mass_mixture']
    assert mixture['equal_weight_Mopt']>0 and mixture['actual_current_Mopt']>0
    assert abs(mixture['actual_current_third_field_discrepancy'])>1e-3
    assert b['same_G_different_optics']['g_difference']<1e-12
    ll=b['Liouvillian'];assert 0<ll['exact_resolvent_error']<=ll['certified_bound']
    critical=c['arbitrarily_pole_like_without_atom']
    assert critical['eta']==critical['delta_min']
    assert critical['exact_atom_weight']==0
    assert critical['actual_relative_eta_error']<=critical['relative_eta_error_bound']<critical['required_relative_tolerance']
    source=c['source_contracted_closure']
    assert source['actual_error']<=source['remainder_bound']
    out=dict(status='PASS',timestamp_UTC=datetime.now(timezone.utc).isoformat(),
        baseline='c80147f',branch=branch,focused_checks=list(results),
        source_sha256=sources,prior_frozen_sha256=verified,R02_source_sha256=r02,
        DFT_tracked_diff_sha256=diffsha,stock_QE_sha256=stock,
        local_links_checked=links,native_jobs=0,material_validation=False,
        physical_xc=None,novelty='UNVERIFIED',raw_optical_package_accessible=False,
        original_Stage0_NO_GO_preserved=True,old_goal_unchanged=True,
        synthetic_model_values_not_material_coefficients=True)
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
