"""Focused source/data/proof preservation; no DFT command or native invocation."""
import ast
import csv
from datetime import datetime, timezone
from fractions import Fraction as F
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse
import numpy as np
from analyze import HERE, PARENT, RY, old

BASE='4cfc16b'
REPO=HERE.parents[3]


def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)


def main():
    r=json.loads((HERE/'result.json').read_text())
    independent=json.loads((HERE/'independent_results.json').read_text())
    assert r['baseline']==BASE and r['native_jobs']==0 and independent['passed']
    assert not r['closure']['inherited_1e_8_gate_pass']
    assert not r['physically_stationary_state'] and r['material_gap_or_xc'] is None
    previous=json.loads((PARENT/'verification.json').read_text())
    assert old.digest(PARENT/'contracted_actions.npz')==previous['source_hashes']['contracted_actions.npz']
    assert len(r['native_packet_pins'])==32
    for path,pin in r['native_packet_pins'].items():
        assert Path(path).stat().st_size==pin['bytes'] and old.digest(path)==pin['sha256']
    for path,sha in r['source_ELF_PP_pins'].items():assert old.digest(path)==sha
    cert=r['source_norm_certificate']; assert old.digest(cert['source'])==cert['sha256']
    assert not cert['raw_kernel_multiplier_packet_available']
    assert max(v['centered_local_bound_Ry'] for v in r['local_checks'].values())<7
    assert all(v['magnetic_potential_max_Ry']==0 for v in r['local_checks'].values())
    # Exact rational upper arithmetic, independently of floating spectral norms.
    box=sum(F(24)+F(2,m*m) for m in range(1,31)); assert box<724
    regular=F(16)*box/(7*3*12); assert regular<46
    aa=F(13,10)+F(2,3)*(F(1,5000)+F(1,4)); assert aa<2
    zero=F(46)+2*F(2); assert zero==50
    kappa=F(1,4)*(46+50); member=kappa*(1+F(1,10**8))+7
    assert member<32
    assert r['observations']['chemical_2']['even']['Q_op_interval_meV'][0]>95.46
    assert r['observations']['chemical_2']['odd']['Q_op_interval_meV'][1]<.332
    assert max(abs(v) for v in r['observations']['chemical_2']['odd']['trace_interval_meV'])<1.12e-8
    assert all(v['op_interval'][0]>1e-8 for v in r['source_density_Theta_defects'].values())
    rows=list(csv.DictReader((HERE/'response_table.csv').open()))
    assert len(rows)==7 and {v['response'] for v in rows}==set(r['observations'])
    tail={}; member_traces={}
    for m in ('host','cd'):
        for c in (1,2):
            b=old.Packet(old.ROOT/m/'pilot'/f'c{c}_before.rank0',0,2,c)
            b.take('<i8',(10,));b.take('<f8',(3,3));b.take('<f8',(3,));b.take('<f8',(4,))
            b.take('<i8',(3,b.n));b.take('<f8',(176,));f=b.take('<f8',(176,));t=f[f<1e-8]
            tail[f'{m}_{c}']=dict(native_cutoff=1e-8,max_omitted_weight=float(max(t,default=0)),
                                omitted_charge_e=float(sum(t)))
            assert max(t,default=0)<4.25e-53
            d1=np.load(old.OLD/f'{m}_c1_matrices.npz');dc=np.load(old.OLD/f'{m}_c{c}_matrices.npz')
            A=dc['exchange']+dc['local_total']-d1['local_total']+d1['local']
            value=old.observable(A)
            err=abs(value-r['observations'][f'{m}_{c}']['original_trace_meV'])
            assert err<1e-9
            member_traces[f'{m}_{c}']=dict(old_matrix_trace_meV=value,new_native_trace_difference_meV=err)
    for m in ('host','cd'):
        p=old.OLD/'evidence'/m/'reference.bin'
        assert old.digest(p)==json.loads((PARENT/'source_and_budget.json').read_text())['fixed_reference_embedding']['reference_sha256']
    protected={}
    for p in list(previous['protected_MCT'])+['research/contribution_registry.md',
              'research/programs/microscopic_bandgap/screening_feasibility_2026-10-16/verification.json']:
        assert (REPO/p).read_bytes()==git('show',BASE+':'+p),p
        protected[p]=old.digest(REPO/p)
    hp='research/programs/microscopic_bandgap/SUCCESSOR_HANDOFF.md';hand=(REPO/hp).read_text()
    a=hand.index('## Latest frozen-response Theta decomposition COMPLETE')
    b=hand.index('## Latest science-first screening feasibility COMPLETE',a)
    assert hand[:a]+hand[b:]==git('show',BASE+':'+hp).decode()
    branch=git('branch','--show-current').decode().strip()
    assert branch=='research/hgcdte-impurity-tmatrix-20261010'
    allowed={hp,'research/programs/microscopic_bandgap/state.md'};prefix=str(HERE.relative_to(REPO))+'/'
    changes=git('diff','--name-only',BASE).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()
    assert all(p in allowed or p.startswith(prefix) for p in changes)
    links=0
    for p in HERE.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if urlparse(link).scheme or link.startswith('#'):continue
            assert (p.parent/link.split('#')[0]).exists(),(p,link)
            links+=1
    for p in HERE.glob('*.py'):ast.parse(p.read_text())
    subprocess.run(['git','diff','--check'],cwd=REPO,check=True)
    subprocess.run(['git','diff','--cached','--check'],cwd=REPO,check=True)
    output=dict(status='PASS_DISTINCT_RETAINED_DATA_THEORY; EXACT_CLOSURE_NO_GO; CONDITIONAL_FROZEN_RESPONSE_BOUNDS',
      timestamp_UTC=datetime.now(timezone.utc).isoformat(),baseline=BASE,branch=branch,native_jobs=0,
      private_packet_pins_rechecked=32,source_ELF_PP_pins_rechecked=len(r['source_ELF_PP_pins']),
      rational_norm_bound_check=dict(cube_shell_sum=str(box),regular_kernel_upper=float(regular),
        aa_upper=float(aa),centered_member_upper_Ry=float(member)),
      native_occupation_tail_checks=tail,independent_member_matrix_checks=member_traces,
      protected_MCT=protected,entire_old_handoff_preserved=True,contribution_registry_unchanged=True,
      local_links_checked=links,physical_xc=None,native_admission=False,
      source_hashes={p.name:old.digest(p) for p in HERE.iterdir() if p.is_file() and p.name!='verification.json'},
      limits='Source-conditioned finite-grid operator intervals, not original kernel byte replay, '
        'directed-rounding or material error bounds. No stationary FD/HSE state or exact six-column '
        'closure. No DFT Git/driver/build/native command or protected-tree write.')
    (HERE/'verification.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('source_hashes','protected_MCT','native_occupation_tail_checks')},indent=2))


if __name__=='__main__':main()
