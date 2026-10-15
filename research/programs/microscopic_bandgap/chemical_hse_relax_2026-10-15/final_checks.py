"""Read-only final preservation, owned cleanup and sampled-output accounting."""
import ast,fcntl,hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
import run_pilot_fixed as r

HERE=Path(__file__).resolve().parent

def main():
    before=json.loads((HERE/'protected_before.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.DFT,text=True).strip()==before['DFT_HEAD']
    assert subprocess.check_output(['git','status','--short'],cwd=r.DFT,text=True)==before['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','diff','--binary'],cwd=r.DFT)).hexdigest()==before['DFT_tracked_diff_sha256']
    for path,pin in before['files'].items():assert r.sha(path)==pin,path
    (HERE/'protected_after.json').write_bytes((HERE/'protected_before.json').read_bytes())
    old=HERE.parent/'chemical_hse_firstace_p2_2026-10-14'
    for path,pin in json.loads((old/'evidence_manifest.json').read_text())['files'].items():assert r.sha(path)==pin['sha256'],path
    fd=r.os.open(r.LOCK,r.os.O_RDONLY|r.os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:r.os.close(fd)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    assert r.sha(r.REGISTRY)==json.loads((HERE/'preflight.json').read_text())['old_registry_sha256']
    for name in ['pw.x','mpirun','prterun','pw.hse8.relax']:
        q=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert q.returncode==1 and not q.stdout
    for m in ['host','cd']:
        _,_,root=r.load(m);f=json.loads((root/'FINAL.json').read_text());assert f['accepted'] and not r.cgroup_path(f['guard']['cgroup']).exists()
    accounts=[r.Account(r.PAIR/m,14*r.GIB,64*(1<<20),r.LinuxGuard(r.LIB)).sample() for m in ['host','cd']]
    total=sum(a['budget_charge_bytes'] for a in accounts);assert total<14*r.GIB
    for p in HERE.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
    for p in HERE.rglob('*.json'):json.loads(p.read_text())
    record=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),all_frozen_pins_match=True,old_accepted_native_evidence_unchanged=True,protected_DFT_exact=True,known_lock_free=True,old_ledger_exact=True,both_own_cgroups_absent=True,visible_native_names_empty=True,hostwide_absence_claim=False,final_pair_output_charge_B=total,accounts=accounts,checks='native/source/archive hash, JSON/Python syntax and owned closure; no new native run')
    (HERE/'final_preservation_account.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='accounts'},indent=2))

if __name__=='__main__':main()
