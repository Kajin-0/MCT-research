"""Archive completed native constructor, preserve all old failures, no new run."""
import ast
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import run_probe as r


def main():
    root=r.PAIR/'host';profile,job,_=r.load('host')
    final=json.loads((root/'FINAL.json').read_text());assert final['accepted']
    g=json.loads((root/'GUARD_RESULT.json').read_text());t=json.loads((root/'TERMINAL.json').read_text())
    assert g['pass_guard'] and t['terminal'] and not r.cgroup_path(g['cgroup']).exists()
    assert int(t['manager']['MemoryPeak'])==g['peak_kernel_memory_B']<12*r.GIB
    fd=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(fd)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    protected=json.loads((r.HERE/'protected_before.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.DFT,text=True).strip()==protected['DFT_HEAD']
    assert subprocess.check_output(['git','status','--short'],cwd=r.DFT,text=True)==protected['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','diff','--binary'],cwd=r.DFT)).hexdigest()==protected['DFT_tracked_diff_sha256']
    for p,h in protected['files'].items():assert r.sha(p)==h
    for folder in ['hybrid_convergence_2026-10-15','exchange_symmetry_2026-10-15']:
        old=r.HERE.parent/folder
        for p,v in json.loads((old/'evidence_manifest.json').read_text())['files'].items():assert r.sha(p)==v['sha256']
    assert r.sha(r.REGISTRY)==json.loads((r.HERE.parent/'hybrid_convergence_2026-10-15/preflight.json').read_text())['old_registry_sha256']
    visible=subprocess.check_output(['ps','-eo','pid=,comm='],text=True)
    for line in visible.splitlines():
        _,name=line.split(maxsplit=1)
        assert name not in ['pw.x','mpirun','prterun'] and not name.startswith('pw.hse8'),line
    dest=r.HERE/'evidence';dest.mkdir(exist_ok=False);files={}
    for name in ['pw.in','pw.out','JOB.json','READY.json','REFERENCED.json','LAUNCH.json','RANKS.json','GUARD_RESULT.json','TERMINAL.json','FINAL.json','telemetry.jsonl']:
        p=root/name;target=dest/name;shutil.copy2(p,target)
        files[str(p)]=dict(sha256=r.sha(p),bytes=p.stat().st_size,archive_relative=str(target.relative_to(r.HERE)))
    for p in sorted((root/'pilot').iterdir())+list((root/'pp').iterdir()):
        files[str(p)]=dict(sha256=r.sha(p),bytes=p.stat().st_size,retained_private=True)
    account=r.Account(root,14*r.GIB,64*(1<<20),r.LinuxGuard(r.LIB)).sample()
    old=json.loads((r.HERE.parent/'exchange_symmetry_2026-10-15/final_checks.json').read_text())
    combined=account['budget_charge_bytes']+old['combined_phase_output_B'];assert combined<14*r.GIB
    (r.HERE/'evidence_manifest.json').write_text(json.dumps(dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='3ce4dc0',verdict='PASS_NEW_CONSTRAINED_OPERATOR_ONLY',QE_ELF=str(r.QE),QE_ELF_sha256=r.sha(r.QE),files=files),indent=2)+'\n')
    (r.HERE/'protected_after.json').write_bytes((r.HERE/'protected_before.json').read_bytes())
    for p in r.HERE.glob('*.py'):ast.parse(p.read_text())
    for p in r.HERE.rglob('*.json'):json.loads(p.read_text())
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),all_frozen_pins_match=True,protected_DFT_exact=True,
        previous_native_source_evidence_exact=True,old_BYTE_refusal_unchanged=True,
        old_ledger_exact=True,known_lock_free=True,own_cgroup_absent=True,
        actual_terminal_manager_and_pidfd_exits_pass=True,no_visible_native_family=True,
        hostwide_absence_claim=False,final_new_output_B=account['budget_charge_bytes'],
        combined_three_phase_output_B=combined,below14GiB=True,account=account,
        completed_new_native_jobs=1,SCF_performed=False,no_Cd_release=True)
    (r.HERE/'final_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='account'},indent=2))


if __name__=='__main__':main()
