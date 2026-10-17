"""Read-only verification of the running checkpoint; no native/manager mutation."""
from pathlib import Path
import hashlib
import json
import subprocess

P = Path(__file__).resolve().parent
B = P.parent
REPO = P.parents[3]
DFT = Path('/home/User/opencode_workspace/DFT')


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as stream:
        for block in iter(lambda:stream.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()


def main():
    f=json.loads((P/'preregistration.json').read_text())
    checkpoint=json.loads((P/'active_checkpoint.json').read_text())
    root=Path(f['root'])
    ck=Path(checkpoint['checkpoint_dir'])
    assert checkpoint['status']=='RUNNING' and checkpoint['native_outer_converged'] is None
    for p,h in f['pins'].items():
        assert sha(p)==h,p
    assert sha(root/'pw.in')==f['input_sha256']==sha(P/'host_pw.in')
    assert sha(root/'observe_case.py')==f['observer_sha256']==sha(P/'observe_case.py')
    text=(P/'host_pw.in').read_text()
    old=B/'primitive_k2_hse_2026-10-17'
    oldf=json.loads((old/'preregistration.json').read_text())
    original=text.replace("prefix='r07pk4'","prefix='r07pk2'").replace(str(root),oldf['root'])
    original=original.replace('max_seconds=82800','max_seconds=21000').replace(
        'nqx1=4, nqx2=4, nqx3=4','nqx1=2, nqx2=2, nqx3=2').replace(
        '4 4 4 0 0 0','2 2 2 0 0 0')
    assert original==(old/'host_pw.in').read_text()
    for name,info in checkpoint['snapshot_prefixes'].items():
        saved=ck/name
        assert sha(saved)==info['sha256'] and saved.stat().st_size==info['bytes']
        with Path(info['source']).open('rb') as stream:
            assert stream.read(info['bytes'])==saved.read_bytes()
    manager=json.loads((ck/'manager.json').read_text())
    m=manager['unit'];o=manager['observer_unit']
    assert m['SubState']=='running' and o['SubState']=='running'
    assert m['InvocationID']==checkpoint['worker_invocation']
    assert m['NRestarts']==o['NRestarts']=='0'
    assert m['kernel']['memory.max']==str(12*2**30)
    assert m['kernel']['memory.swap.max']=='0' and m['kernel']['pids.max']=='12'
    assert m['BindsTo']==f['observer_unit']
    live=json.loads((P/'initial_live.json').read_text())['units']['unit']
    ranks=[v for v in live['processes'] if Path(v['exe']).name=='pw.x']
    assert len(ranks)==2 and all(v['exe_sha256']==f['pins'][v['exe']] for v in ranks)
    readback=json.loads((P/'initial_native_readback.json').read_text())
    assert readback['native_Gamma_weight']==1/64 and readback['native_q_full_count']==64
    assert len(readback['native_k_points_crystal_stdout'])==8
    assert len({tuple(round(v*4)%4 for v in q['crystal_quarter_rounded'])
                for q in readback['native_q_source_points_stdout']})==64
    assert checkpoint['kernel_memory_peak_B']<12*2**30 and checkpoint['swap_peak_B']==0
    assert checkpoint['sampled_host_available_min_B']>=4*2**30
    assert checkpoint['sampled_disk_free_min_B']>=10*2**30
    assert checkpoint['sampled_owned_output_max_B']<=14*2**30
    assert checkpoint['qualified_nonmagnetic_state'] is None and checkpoint['physical_xc'] is None

    historic=B/'static_environment_2026-10-15'
    pins=dict(json.loads((historic/'frozen_protocol.json').read_text())['profile']['pins'])
    pins.update({k:v['sha256'] for k,v in json.loads((historic/'evidence_manifest.json').read_text())['raw'].items()})
    build=json.loads((B/'pbe_density_driver_2026-10-16/source_build_evidence.json').read_text())
    for key in ['linked_archive_pins','compiler_object_pins','compiled_module_pins']:
        pins.update(build[key])
    protection=json.loads((historic/'protected_before.json').read_text())
    pins.update(protection['files'])
    assert len(pins)==822
    for name,h in pins.items():
        assert sha(name)==h,name
    assert subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)==protection['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','-C',str(DFT),'diff','--binary'])).hexdigest()==protection['DFT_tracked_diff_sha256']
    originals=0
    folders=['pbe_density_driver_2026-10-16','pbe_static_lifecycle_2026-10-16',
             'pbe_static_completion_2026-10-16','pbe_density_only_feasibility_2026-10-16']
    for folder in folders+['pbe_final_admission_2026-10-16','primitive_k2_hse_2026-10-17',
                            'stock_hse_stationary_2026-10-16']:
        prefix=str((B/folder).relative_to(REPO))
        names=subprocess.check_output(['git','ls-tree','-r','--name-only','ab6fbd0',prefix],text=True).splitlines()
        if folder in folders:
            originals+=len(names)
        for name in names:
            assert (REPO/name).read_bytes()==subprocess.check_output(['git','show','ab6fbd0:'+name]),name
    assert originals==76
    branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
    assert branch=='research/hgcdte-impurity-tmatrix-20261010'
    result=dict(verified=True,scope='immutable RUNNING checkpoint, not terminal SCF/symmetry PASS',
                status_at_checkpoint='RUNNING',native_case_count=1,native_restarts=0,
                Gamma_weight_measured=1/64,q_points_measured=64,
                kernel_peak_at_checkpoint_B=checkpoint['kernel_memory_peak_B'],
                source_physics_delta_only_kq=True,protected_pins_unchanged=822,
                historical_originals_unchanged=76,old_k2_HSE8_and_PBE_closure_unchanged=True,
                DFT_dirty_unchanged=True,native_final_state_unavailable_at_checkpoint=True,
                worker_unit=f['unit'],worker_invocation=checkpoint['worker_invocation'],
                protected_future_action='inspect existing job; never launch/retry a second case',physical_xc=None)
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
