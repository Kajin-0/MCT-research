"""Focused science/provenance verification only; cannot launch native code."""
from pathlib import Path
import ast,hashlib,json,math
import numpy as np

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    pin_count=0
    for f in [HERE.parent/'chemical_pbe16_2026-10-15/frozen_protocol.json',HERE/'frozen_protocol.json',HERE/'frozen_cd_protocol.json']:
        profile=json.loads(f.read_text())['profile']
        for path,h in profile['pins'].items():
            assert sha(path)==h,path;pin_count+=1
    for f in [*HERE.glob('*.py'),*(HERE.parent/'chemical_pbe16_2026-10-15').glob('*.py')]:ast.parse(f.read_text(),filename=str(f))
    r=json.loads((HERE/'numerical_result.json').read_text())
    mp=json.loads((HERE/'multiplet_result.json').read_text())
    assert r['physical_xc'] is None and mp['physical_xc'] is None and not r['HSE_launched']
    assert all(v['accepted'] and v['terminal_pass'] for v in r['members'].values())
    assert all(v['science']['SCF_converged'] and v['science']['scf_error_Ry']<=1e-9 and abs(v['science']['charge_residual_e'])<=1e-8 for v in r['members'].values())
    ov=np.load(HERE/'complex_overlaps.npz');reconstructed={}
    for member in ['host','cd']:
        gs={};inverse={}
        for label,d in [('Gamma6',2),('Gamma8',4)]:
            a=np.loadtxt(HERE/(member+'_'+label+'_spectrum.csv'),delimiter=',',skiprows=1)
            w=np.sum(abs(ov[member+'_'+label])**2,axis=0)/d
            assert max(abs(a[:,2]-w))<1e-16
            # Independent Python complex sum and math.exp reductions.
            mass=sum(float(v)*math.exp(-float(e)**2/8) for v,e in zip(w,a[:,1]))
            gs[label]=sum(float(v)*float(e)*math.exp(-float(e)**2/8) for v,e in zip(w,a[:,1]))/mass
            inverse[label]=1/sum(float(v)/complex(-float(e),.05) for v,e in zip(w,a[:,1]))
            assert mp['members'][member][label]['mean_taken_only_AFTER_symmetry_and_degeneracy_pass']
        reconstructed[member]=dict(Gaussian=gs['Gamma6']-gs['Gamma8'],inverse=(inverse['Gamma8']-inverse['Gamma6']).real)
    gd=reconstructed['cd']['Gaussian']-reconstructed['host']['Gaussian']
    cd=reconstructed['cd']['inverse']-reconstructed['host']['inverse']
    assert abs(gd-r['primary_W2_eV'])<1e-14
    expected=next(v for v in r['scalar_causal_rows'] if v['eta_eV']==.05)
    assert abs(cd-expected['delta_eV'])<1e-14
    assert all(row['conditional_interval_eV'][0]>0 for row in r['Gaussian_rows'])
    assert all(row['conditional_interval_eV'][0]>0 for row in r['scalar_causal_rows'])
    assert all(row['fixed_frame_conditional_interval_eV'][0]>0 for row in r['matrix_causal_rows'])
    failed=json.loads((HERE.parent/'chemical_pbe16_2026-10-15/owner_failure.json').read_text())
    assert not failed['guard']['pass_guard'] and failed['no_rank_release']
    for path,h in failed['files'].items():assert sha(path)==h
    original_failure=json.loads((HERE/'original_readback_failure.json').read_text())
    assert not original_failure['original_scientific_gate_pass'] and sha(HERE/'science.py')==original_failure['source_sha256']
    after=json.loads((HERE/'protected_after.json').read_text())
    assert after['stock_and_DFT_unchanged'] and after['old_ledger_unchanged'] and after['exclusive_lock_free']
    for row in after['new_owned_families_terminal_and_gone']:assert row['cgroup_gone']
    out=dict(passed=True,conditions='focused offline native-data science/provenance checks; not a substitute for the two actual SCFs',immutable_source_pin_checks=pin_count,independent_python_Gaussian_delta_eV=gd,independent_python_inverse_delta_eV=cd,old_owner_and_readback_failures_still_failed=True,no_HSE_or_material_gap_claim=True)
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
