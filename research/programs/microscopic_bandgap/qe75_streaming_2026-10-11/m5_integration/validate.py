"""Finite sequential production-path validation and preservation. No QE/MPI."""
from datetime import datetime,timezone
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys
import time
from production_transport import HERE,BUILD,artifact_sha256
from family_runtime import LOCK,REGISTRY,read_meta,memory,LIB,LinuxGuard
from process_identity import flock_owner,table

DFT=Path('/home/User/opencode_workspace/DFT')


def run(argv,cwd=DFT,seconds=60):
    started=time.monotonic()
    result=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,text=True,timeout=seconds)
    record={'command':list(map(str,argv)),'cwd':str(cwd),'returncode':result.returncode,
            'stdout':result.stdout,'stderr':result.stderr,'wall_seconds':time.monotonic()-started}
    if result.returncode: raise RuntimeError(record)
    return record


def main():
    # The executable is retained in the private project build tree. Its only
    # dynamic dependencies are libc/loader; this test never links MPI or QE.
    compiler=Path('/usr/bin/cc').resolve()
    command=[compiler,'-std=c11','-O2','-Wall','-Wextra','-Werror',HERE/'rank_worker.c',
             HERE.parent/'m5_readiness/lease_client.c','-o',BUILD/'rank_worker']
    build=run(command)
    dependencies=run(['ldd',BUILD/'rank_worker'])
    if 'libmpi' in dependencies['stdout'] or 'libmpich' in dependencies['stdout']:
        raise RuntimeError('serial integration worker unexpectedly links MPI')
    build_report={'compile':build,'compiler':str(compiler),'compiler_sha256':artifact_sha256(compiler),
                  'compiler_version':run([compiler,'--version'])['stdout'],
                  'binary':str(BUILD/'rank_worker'),'binary_sha256':artifact_sha256(BUILD/'rank_worker'),
                  'dependencies':dependencies,'source_sha256':{str(p):artifact_sha256(p) for p in
                  [HERE/'rank_worker.c',HERE.parent/'m5_readiness/lease_client.c']},'MPI_PW_executed':False}
    (BUILD/'build.json').write_text(json.dumps(build_report,indent=2)+'\n')
    records=[run([sys.executable,HERE/'test_integration.py'])]
    for name in ['test_runtime.py','test_preflight.py']:
        records.append(run([sys.executable,HERE.parent/'runtime_admission'/name]))
    focused=[(HERE.parent/'m5_readiness',[
        'test_readiness.ReadinessTest.test_native_hook_accepts_distinct_digests_but_refuses_unearned_scope',
        'test_readiness.ReadinessTest.test_dual_hash_binding_is_not_hash_equality']),
        (HERE.parent/'native_bridge',[
        'test_native_bridge.NativeBridgeTest.test_native_runtime_fails_closed',
        'test_native_bridge.NativeBridgeTest.test_boolean_cannot_promote_synthetic_profile'])]
    for folder,names in focused:
        records.append(run([sys.executable,'-m','unittest','-v',*names],cwd=folder))
    before=read_meta(BUILD/'preservation_before.json');mismatches=[]
    for path,expected in before['pins'].items():
        if artifact_sha256(Path(path))!=expected: mismatches.append(path)
    for path,expected in before['stock'].items():
        if artifact_sha256(DFT/path)!=expected: mismatches.append(path)
    root=BUILD.parent
    for key,path in [('previous_candidate',root/'link-only/pw.qstream.UNVALIDATED'),
                     ('bridge_binary_sha256',root/'native_bridge/link-only/pw.bridge.RUNTIME_REFUSED'),
                     ('M4_control_sha256',root/'runtime_admission/link-only/pw.control.M4_UNVALIDATED')]:
        if artifact_sha256(path)!=before[key]: mismatches.append(str(path))
    for path,expected in before['readiness_candidates'].items():
        if artifact_sha256(Path(path))!=expected: mismatches.append(path)
    head=run(['git','rev-parse','HEAD'])['stdout'].strip()
    dirty=run(['git','status','--porcelain'])['stdout']
    sessions=run(['tmux','list-sessions','-F','#{session_name}:#{session_id}'])['stdout'].splitlines()
    if head!=before['DFT_head'] or dirty!=before['DFT_status']: mismatches.append('DFT HEAD/status')
    if sessions!=before['sessions']: mismatches.append('tmux sessions')
    live=[]
    for pid,row in table().items():
        try:
            exe=Path(f'/proc/{pid}/exe').readlink()
            command=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
            if row['state']!='Z' and (exe==BUILD/'rank_worker' or len(command)>1 and
                  os.fsdecode(command[1]) in [str(HERE/'fixture_launcher.py'),str(HERE/'fixture_hook.py')]): live.append(row)
        except (FileNotFoundError,ProcessLookupError,PermissionError): pass
    lease=flock_owner(LOCK);registry=read_meta(REGISTRY)
    if live or lease or registry['phase']!='FINISHED': mismatches.append('owned worker/lease remains')
    storage=LinuxGuard(LIB).probe(BUILD);mem=memory()['MemAvailable']
    if storage['available_bytes']<10*(1<<30) or mem<4*(1<<30): mismatches.append('resource floor')
    component=read_meta(BUILD/'integration_tests.json')
    # Preserve the first observed blocker; do not rerun inventories to fish for
    # a convenient passing snapshot or to authorize a new native campaign.
    inventory=read_meta(BUILD/'inventory.json')
    count=sum(int(re.search(r'Ran (\d+) tests?',r['stderr']).group(1)) for r in records)
    report={'timestamp_UTC':datetime.now(timezone.utc).isoformat(),'starting_MCT_commit':'6b5fc5e',
            'passed_component_validation':not mismatches,'focused_methods':count,'test_records':records,
            'gates':{'production_M4_binary_dispatch_and_typed_live_hook':'PASS SMALL-SCALE ABI_NO_MPI',
                     'actual_native_MPI_registration_collectives':'NOT RUN / NOT QUALIFIED',
                     'native_scope_and_checkpoint_publication':'UNISSUED / NOT QUALIFIED',
                     'global_exclusivity_inventory':inventory['native_inventory_gate'],
                     'native_fixture':'BLOCKED / NOT RUN'},
            'first_unpassed_native_gate':'GLOBAL_INVENTORY: mapping permission denied for live PID 1',
            'peak_integration_family_RSS_bytes':max(r.get('peak_summed_RSS_bytes',0) for r in component['real_guardian_component_evidence']),
            'preservation':{'mismatches':mismatches,'DFT_head':head,'dirty_status_unchanged':dirty==before['DFT_status'],
                           'protected_pins':len(before['pins']),'sessions':sessions,
                           'stock_and_all_prior_private_candidates_unchanged':not mismatches},
            'closure':{'live_integration_workers':live,'kernel_lease_holders':lease,'registry':registry},
            'MemAvailable_bytes':mem,'free_disk_bytes':storage['available_bytes'],
            'native_QE_HSE_MPI_executed':False,'no_permissions_changed':True,
            'source_sha256':{p.name:artifact_sha256(p) for p in HERE.glob('*.py')},
            'modified_sources_sha256':{str(p):artifact_sha256(p) for p in
                 [HERE.parent/'runtime_admission/family_runtime.py',HERE.parent/'runtime_admission/runtime_client.py',
                  HERE.parent/'native_bridge/native_bundle.py']}}
    for source,target in [('build.json','build_results.json'),('integration_tests.json','integration_results.json'),
                          ('inventory.json','inventory_results.json')]: shutil.copy2(BUILD/source,HERE/target)
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    if mismatches: raise RuntimeError(mismatches)
    print(f'PASS {count} focused methods; production guardian ABI gate advanced. STOP at inventory; native NOT RUN.')


if __name__=='__main__': main()
