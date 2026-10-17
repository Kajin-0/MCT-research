"""Independent offline checks on actual source mathematics and native metadata."""
from fractions import Fraction as F
import ast
import importlib.util
import itertools as it
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import numpy as np

P = Path(__file__).resolve().parent
B = P.parent


def main():
    spec=importlib.util.spec_from_file_location('bounded_readonly_audit',P/'audit.py')
    a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
    r=json.loads((P/'audit.json').read_text())
    checks=[]
    def check(v,name):
        if not v:raise AssertionError(name)
        checks.append(name)

    # Different representation: primitive crystallographic integer rotation
    # matrices. Reproduce the ALREADY accepted native k4 XML, not a new run.
    t=np.array([[-1,1,1],[1,-1,1],[1,1,-1]])
    ainv=np.array([[0,1,1],[1,0,1],[1,1,0]])
    rotations=[]
    for perm,signs in a.OPS:
        cart=np.zeros((3,3),int)
        for j in range(3):cart[j,perm[j]]=signs[j]
        mat=t@cart.T@ainv
        check(np.all(mat%2==0),'integer fcc reciprocal symmetry')
        rotations.append(mat//2)
    points=a.regular(4);left=set(points);reps=[]
    for k in sorted(points):
        if k in left:
            orbit={a.wrap(tuple(tr*sum(k[j]*mat[j,i] for j in range(3)) for i in range(3)))
                   for mat in rotations for tr in [-1,1]} & points
            reps.append((k,len(orbit)));left-=orbit
    xt=ET.parse(B/'primitive_k4_hse_2026-10-17/final_qualification/native/data-file-schema.xml')
    bg=np.array([np.fromstring(xt.findtext('output/basis_set/reciprocal_lattice/'+s),sep=' ')
                 for s in ['b1','b2','b3']])
    native=[]
    for row in xt.findall('output/band_structure/ks_energies'):
        k=np.fromstring(row.findtext('k_point'),sep=' ')@np.linalg.inv(bg)
        native.append((tuple(F(int(round(v*4))%4,4) for v in k),
                       round(float(row.find('k_point').attrib['weight'])*64)))
    check(sorted(native)==sorted(reps),'same source enumeration reproduces native primitive k4 irreps and weights')
    qsrc,ok=a.exx_sources(reps,points,4)
    check(ok and len(qsrc)==64,'source method reproduces native primitive64 source points')

    # Independent analytic star multiplicities and half-grid parity classes.
    conv4=r['grid_models'][3]
    check([v['multiplicity'] for v in conv4['representatives']]==[1,6,3,12,12,3,8,12,6,1],
          'ten simple-cubic star multiplicities sum64')
    parity={tuple(int(round(x*4))%2 for x in z['k']) for z in conv4['representatives']}
    check(len(parity)==7 and conv4['source_union_count']==7*8,'seven q2 cosets give56 unique sources')
    check(r['grid_models'][1]['effective_q']==[1]*3 and r['grid_models'][1]['irreducible_count']==1,
          'single-irrep shifted k2 triggers stock q1 rule')
    check(r['grid_models'][2]['effective_q']==[1]*3 and not r['grid_models'][2]['requested_translations_supported'],
          'k3/q2 cannot preserve its requested transfer grid')
    check(r['folded16']['q2_source_count']==16,'exact folded electronic16 still requires16 source storage')
    check(sum(r['grid_models'][0]['representatives'][j]['multiplicity'] for j in range(4))==8,
          'candidate centered k2 weights partition full eight points')

    # Bound distinguishes retained occupied count from unoccupied coverage.
    pp=r['PP'];check([float(pp[s]['z_valence']) for s in ['Hg','Cd','Te']]==[20,20,16],
                     'independent isovalent36 per HgTe or CdTe pair')
    check(r['retained_nonstationary_data']['host']['atomic_starting_columns']==152 and
          r['retained_nonstationary_data']['cd']['atomic_starting_columns']==152,'actual atomic152 branch in both native archives')
    eps=1e-8;sigma=.001*a.RY
    threshold=r['spinor_bands']['FD_24state_charge_tail_1e8_requires_margin_eV']
    check(abs(24/(1+np.exp(threshold/sigma))-eps)<1e-21,'FD24-state conditional tail formula')
    check(max(r['retained_nonstationary_data']['rejected_stock79build_host']['projection_probability_in_bands153_176'])>1e-4,
          'actual nonstationary physical-reference spectral weight above152 is nonzero')

    # Exact allocation arithmetic, plus the fact that it is NOT a peak bound.
    m=r['memory']
    check(216000*2*152*8*16==m['band152_q8_nominal_B']==8404992000,'independent integer buffer byte count')
    check(sum(m['nominal_known_ACE_phase_payload'].values())==m['nominal_known_ACE_phase_sum_B'],
          'named payload subtotal adds consistently')
    check(m['complete_peak_upper_B'] is None and m['execution_under_12GiB']=='NO-GO',
          'no inference of safe peak from positive nominal headroom')
    tag='qe-7.5'
    def source(name):return subprocess.check_output(['git','--no-optional-locks','-C',str(a.QE),'show',tag+':'+name],text=True)
    base=source('PW/src/exx_base.f90');exx=source('PW/src/exx.f90')
    check('IF (nkstot == nspin_lsda)' in base and 'nq1=1; nq2=1; nq3=1' in base,'actual singleton-irrep source override')
    check('max_buff_bands_per_egrp-1,nkqs)' in exx,'stock buffer uses nkqs rather than nqs')
    check('temppsic_nc(nrxxs,npol,ialloc), result_nc(nrxxs,npol,ialloc)' in exx,
          'simultaneous two full spinor FFT batches')
    check('diago_david_ndim = 2' in source('Modules/read_namelists.f90'),
          'effective namelist Davidson default2 overrides module initializer4')
    check('n_starting_wfc == n_starting_atomic_wfc' in source('PW/src/wfcinit.f90'),
          'reducing176to152 changes atomic+random initialization branch')
    for name,pin in r['source_pins'].items():
        data=subprocess.check_output(['git','--no-optional-locks','-C',str(a.QE),'show',tag+':'+name])
        import hashlib
        check(hashlib.sha256(data).hexdigest()==pin['sha256'],'exact source tag pin '+name)
    for path,h in r['raw_pins'].items():check(a.sha(path)==h,'native/PP retained pin '+path)
    check(r['protected_pins_unchanged']==822 and r['historical_files_unchanged']==76,
          'completed full protection audit preserved')
    for q in P.glob('*.py'):ast.parse(q.read_text())
    check(r['native_jobs']==r['builds']==r['services']==0,'read-only phase, no execution/build/service')
    check(subprocess.check_output(['git','branch','--show-current'],text=True).strip()==
          'research/hgcdte-impurity-tmatrix-20261010','existing research branch')
    result=dict(verified=True,check_names=checks,checks_passed=len(checks),
                no_native_runs=True,no_builds=True,execution_admitted=False,
                verdict='NO-GO under12GiB; unresolved complete resident peak for k2/q2/152',
                physical_xc=None,artifact_pins={'audit.py':a.sha(P/'audit.py'),'audit.json':a.sha(P/'audit.json'),
                                               'verify.py':a.sha(__file__)})
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='check_names'},indent=2))


if __name__=='__main__':main()
