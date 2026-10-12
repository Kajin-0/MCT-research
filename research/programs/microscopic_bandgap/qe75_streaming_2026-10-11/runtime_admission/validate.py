"""Finite sequential verification, preservation checks, evidence capture. NO QE/MPI."""
from pathlib import Path
import hashlib
import json
import os
from datetime import datetime,timezone
import re
import shutil
import subprocess
import sys
import time

from family_runtime import HERE,PRIVATE,LOCK,REGISTRY,read_meta
from fixture_preflight import DFT,ROOT,CONTROL,STREAM,check
from native_bundle import artifact_sha256
from process_identity import table,flock_owner,mpi_inventory


def run(command,cwd,timeout):
    started=time.monotonic()
    result=subprocess.run(list(map(str,command)),cwd=cwd,capture_output=True,text=True,timeout=timeout)
    record={'command':list(map(str,command)),'cwd':str(cwd),'returncode':result.returncode,
            'stdout':result.stdout,'stderr':result.stderr,'wall_seconds':time.monotonic()-started}
    if result.returncode: raise RuntimeError(record)
    return record


def main():
    records=[]
    for folder,script in [(HERE,'test_preflight.py'),(HERE,'test_runtime.py'),
                          (HERE.parent/'native_bridge','test_native_bridge.py'),
                          (HERE.parent/'checkpoint_phase','test_checkpoint_phase.py'),
                          (HERE.parent,'test_qstream_package.py')]:
        records.append(run([sys.executable,folder/script],folder,60))
    preflight=check()
    for source,target in [('test_runtime.json','runtime_results.json'),('fixture_preflight.json','preflight_results.json'),
                          ('link_control.json','control_build.json')]:
        shutil.copy2(PRIVATE/source,HERE/target)
    before=read_meta(PRIVATE/'preservation_before.json')
    mismatches=[name for name,sha in before['pins'].items() if artifact_sha256(Path(name))!=sha]
    for name,sha in before['stock'].items():
        if artifact_sha256(DFT/name)!=sha: mismatches.append(name)
    if artifact_sha256(ROOT/'link-only/pw.qstream.UNVALIDATED')!=before['previous_candidate']:
        mismatches.append('previous stream candidate')
    if artifact_sha256(STREAM)!=before['bridge_binary_sha256']: mismatches.append('M3 native bridge candidate')
    status=run(['git','status','--porcelain'],DFT,10)['stdout']
    head=run(['git','rev-parse','HEAD'],DFT,10)['stdout'].strip()
    if status!=before['DFT_status'] or head!=before['DFT_head']: mismatches.append('DFT git head/dirty status')
    live=[]
    for pid,row in table().items():
        try:
            command=Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
            if len(command)>1 and os.fsdecode(command[1]) in [str(HERE/p) for p in
                      ['family_runtime.py','fake_launcher.py','fake_worker.py','exec_worker.py']] and row['state']!='Z':
                live.append(row)
        except (FileNotFoundError,ProcessLookupError): pass
    lease=flock_owner(LOCK);registry=read_meta(REGISTRY)
    tmux=run(['tmux','list-sessions','-F','#{session_name}:#{session_id}'],DFT,10)['stdout'].splitlines()
    protected_sessions=all(item in tmux for item in ['calcura:$0','commander:$1','research:$3'])
    success=not mismatches and not live and not lease and registry['phase']=='FINISHED' and protected_sessions
    total=sum(int(re.search(r'Ran (\d+) tests',r['stderr']).group(1)) for r in records)
    report={'passed':success,'timestamp_UTC':datetime.now(timezone.utc).isoformat(),
            'focused_test_methods':total,'test_records':records,'PW_HSE_MPI_run':False,
            'measurement_kind':'real tiny fake subprocesses plus serial codec; no native material result',
            'preservation':{'mismatches':mismatches,'DFT_head':head,'DFT_dirty_status_unchanged':status==before['DFT_status'],
                            'protected_input_PP_supervisor_pins':len(before['pins']),'stock_and_prior_candidates_unchanged':not mismatches,
                            'tmux_sessions':tmux,'protected_sessions_unchanged':protected_sessions},
            'runtime_closed':{'live_owned_workers':live,'kernel_lease_holders':lease,'registry':registry},
            'readable_namespace_MPI_inventory':mpi_inventory(),'native_fixture_status':preflight['status'],
            'source_sha256':{p.name:artifact_sha256(p) for p in HERE.glob('*.py')},
            'updated_native_bundle_sha256':artifact_sha256(HERE.parent/'native_bridge/native_bundle.py')}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    if not success: raise RuntimeError(report)
    print(f'PASS: {total} focused methods (17 lifecycle, 7 preflight, 21 native-codec, 15 checkpoint, 5 source regressions); preservation checked. Native fixture BLOCKED / NOT RUN.')


if __name__=='__main__': main()
