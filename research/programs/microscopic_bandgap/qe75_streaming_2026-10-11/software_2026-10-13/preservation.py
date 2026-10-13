"""Read-only protected artifact/session checks for this software workstream."""
import json
from pathlib import Path
import subprocess
from build_wave import PRIVATE,ROOT,DFT
from native_bundle import artifact_sha256
from family_runtime import LOCK,REGISTRY,read_meta,memory,LIB,LinuxGuard
from process_identity import flock_owner


def check():
    b=read_meta(PRIVATE/'preservation_before.json');bad=[]
    for group in ['pins','readiness_candidates','integration_worker']:
        for p,h in b[group].items():
            if artifact_sha256(Path(p))!=h:bad.append(p)
    for p,h in b['stock'].items():
        if artifact_sha256(DFT/p)!=h:bad.append(p)
    for key,p in [('previous_candidate',ROOT/'link-only/pw.qstream.UNVALIDATED'),
                  ('bridge_binary_sha256',ROOT/'native_bridge/link-only/pw.bridge.RUNTIME_REFUSED'),
                  ('M4_control_sha256',ROOT/'runtime_admission/link-only/pw.control.M4_UNVALIDATED')]:
        if artifact_sha256(p)!=b[key]:bad.append(str(p))
    def cmd(args):return subprocess.check_output(args,cwd=DFT,text=True)
    head=cmd(['git','rev-parse','HEAD']).strip();dirty=cmd(['git','status','--porcelain'])
    sessions=cmd(['tmux','list-sessions','-F','#{session_name}:#{session_id}']).splitlines()
    if head!=b['DFT_head'] or dirty!=b['DFT_status']:bad.append('DFT HEAD/status')
    if sessions!=b['sessions']:bad.append('sessions')
    lease=flock_owner(LOCK);ledger=read_meta(REGISTRY)
    if lease or ledger['phase']!='FINISHED':bad.append('owned lease/ledger')
    free=LinuxGuard(LIB).probe(PRIVATE)['available_bytes'];mem=memory()['MemAvailable']
    if free<10*(1<<30) or mem<4*(1<<30):bad.append('resource floor')
    report={'passed':not bad,'mismatches':bad,'DFT_head':head,'dirty_status_unchanged':dirty==b['DFT_status'],
            'pins':len(b['pins']),'stock_prior_candidates_unchanged':not bad,'sessions':sessions,
            'lease_holders':lease,'own_ledger_phase':ledger['phase'],'MemAvailable_bytes':mem,'free_disk_bytes':free,
            'native_MPI_QE_run':False}
    if bad:raise RuntimeError(report)
    return report


if __name__=='__main__':print(json.dumps(check()))
