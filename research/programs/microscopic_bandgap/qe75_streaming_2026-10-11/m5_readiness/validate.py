"""One finite sequential readiness verification; never launches PW/MPI/HSE."""
from pathlib import Path
from datetime import datetime,timezone
import json
import os
import re
import shutil
import subprocess
import sys

from binding import HERE,artifact_sha256,Refusal
from build import PRIVATE,ROOT,DFT,run
from layout_budget import inventory
from family_runtime import LOCK,REGISTRY,read_meta,memory,LinuxGuard,LIB
from process_identity import flock_owner,mpi_inventory,table
from fixture_preflight import backends


def main():
    records=[]
    folders=[(HERE,'test_readiness.py'),(HERE.parent/'runtime_admission','test_preflight.py'),
             (HERE.parent/'runtime_admission','test_runtime.py'),(HERE.parent/'native_bridge','test_native_bridge.py'),
             (HERE.parent/'checkpoint_phase','test_checkpoint_phase.py'),(HERE.parent,'test_qstream_package.py')]
    for folder,name in folders:
        records.append(run([sys.executable,folder/name],60))
    build=read_meta(PRIVATE/'build.json');link=read_meta(PRIVATE/'link.json')
    if not build['passed'] or not link['passed']: raise Refusal('build/link unsuccessful')
    for name,sha in build['source_sha256'].items():
        if artifact_sha256(PRIVATE/'source'/name)!=sha: raise Refusal('compiled native source changed')
    for name,sha in build['binaries'].items():
        if artifact_sha256(PRIVATE/name)!=sha: raise Refusal('tested serial binary changed')
    for mode,item in link['candidates'].items():
        if artifact_sha256(Path(item['binary']))!=item['sha256']: raise Refusal('private native candidate changed')
    current_backends={mode:backends(Path(item['binary'])) for mode,item in link['candidates'].items()}
    if current_backends['stock']!=current_backends['stream']: raise Refusal('unmatched native backends')
    before=read_meta(PRIVATE/'preservation_before.json');mismatches=[]
    for name,sha in before['pins'].items():
        if artifact_sha256(Path(name))!=sha: mismatches.append(name)
    for name,sha in before['stock'].items():
        if artifact_sha256(DFT/name)!=sha: mismatches.append(name)
    candidates={'previous_candidate':ROOT/'link-only/pw.qstream.UNVALIDATED',
                'bridge_binary_sha256':ROOT/'native_bridge/link-only/pw.bridge.RUNTIME_REFUSED',
                'M4_control_sha256':ROOT/'runtime_admission/link-only/pw.control.M4_UNVALIDATED'}
    for key,path in candidates.items():
        if artifact_sha256(path)!=before[key]: mismatches.append(key)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=DFT,text=True).strip()
    dirty=subprocess.check_output(['git','status','--porcelain'],cwd=DFT,text=True)
    sessions=subprocess.check_output(['tmux','list-sessions','-F','#{session_name}:#{session_id}'],text=True).splitlines()
    if head!=before['DFT_head'] or dirty!=before['DFT_status']: mismatches.append('DFT HEAD/dirty status changed')
    if sessions!=before['sessions']: mismatches.append('pre-existing sessions changed')
    workers=[]
    for pid,row in table().items():
        try:
            command=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
            if command and os.fsdecode(command[0])==str(PRIVATE/'abi_worker') and row['state']!='Z': workers.append(row)
        except (FileNotFoundError,ProcessLookupError): pass
    if workers or flock_owner(LOCK): mismatches.append('owned worker/lease remains live')
    inv=inventory();(PRIVATE/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
    storage=LinuxGuard(LIB).probe(PRIVATE)
    if storage['available_bytes']<10*(1<<30) or memory()['MemAvailable']<4*(1<<30): mismatches.append('resource floor crossed')
    total=sum(int(re.search(r'Ran (\d+) tests',r['stderr']).group(1)) for r in records)
    report={'timestamp_UTC':datetime.now(timezone.utc).isoformat(),'passed':not mismatches,'focused_methods':total,
            'test_records':records,'PW_HSE_MPI_run':False,'native_fixture_admitted':False,
            'gates':{'compiled_transport_source_and_dual_binding':'PASS COMPONENT',
                     'actual_native_MPI_lease_collectives':'NOT RUN / NOT QUALIFIED',
                     'first_ACE_instruments':'COMPILED / SERIAL CODEC CHECKED; NATIVE VALUES NOT RUN',
                     'native_qeh5_existing_wave_density_ACE_decode':'PASS BITWISE, SERIAL ONLY',
                     'SCF_restart_both_stop_paths':'NOT RUN / NOT QUALIFIED',
                     'actual_small_FFT_layout':'UNCERTIFIED','whole_output_bound':'UNCERTIFIED',
                     'common_initial_state':'UNCERTIFIED; existing reference incompatible',
                     'global_inventory':inv['native_inventory_gate']},
            'preservation':{'mismatches':mismatches,'DFT_head':head,'dirty_status_unchanged':dirty==before['DFT_status'],
                            'sessions':sessions,'protected_pins_checked':len(before['pins'])},
            'runtime_closed':{'ABI_workers':workers,'lease_holders':flock_owner(LOCK),'M4_own_ledger':read_meta(REGISTRY)},
            'visible_MPI_families_after_tests':mpi_inventory(),'MemAvailable_bytes':memory()['MemAvailable'],
            'free_disk_bytes':storage['available_bytes'],'compiler_peak_RSS_KiB':build['maximum_child_RSS_KiB'],
            'source_sha256':{p.name:artifact_sha256(p) for p in HERE.iterdir() if p.suffix in ['.py','.c','.f90']},
            'runtime_client_sha256':artifact_sha256(HERE.parent/'runtime_admission/runtime_client.py')}
    for source,target in [('build.json','build_results.json'),('link.json','link_results.json'),
                          ('unit_results.json','unit_results.json'),('readback.json','readback_results.json'),
                          ('inventory.json','inventory_results.json')]:
        shutil.copy2(PRIVATE/source,HERE/target)
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    if mismatches: raise Refusal(str(mismatches))
    print(f'PASS: {total} focused methods, serial readback/source/link gates, protected state. Native M5 BLOCKED / NOT RUN.')


if __name__=='__main__': main()
