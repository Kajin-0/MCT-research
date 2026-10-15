"""Preserve native refusal, all small evidence and raw source pins; no new run."""
import ast,fcntl,hashlib,json,shutil,subprocess
from datetime import datetime,timezone
import run_probe as r

def main():
    root=r.PAIR/'host';profile,job,_=r.load('host')
    assert not(root/'FINAL.json').exists()
    g=json.loads((root/'GUARD_RESULT.json').read_text());t=json.loads((root/'TERMINAL.json').read_text())
    assert g['pass_guard'] and t['terminal'] and not r.cgroup_path(g['cgroup']).exists()
    fd=r.os.open(r.LOCK,r.os.O_RDONLY|r.os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:r.os.close(fd)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    p=json.loads((r.HERE/'protected_before.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.DFT,text=True).strip()==p['DFT_HEAD']
    assert subprocess.check_output(['git','status','--short'],cwd=r.DFT,text=True)==p['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','diff','--binary'],cwd=r.DFT)).hexdigest()==p['DFT_tracked_diff_sha256']
    for path,h in p['files'].items():assert r.sha(path)==h
    old=r.HERE.parent/'hybrid_convergence_2026-10-15'
    for path,rec in json.loads((old/'evidence_manifest.json').read_text())['files'].items():assert r.sha(path)==rec['sha256']
    assert r.sha(r.REGISTRY)==json.loads((old/'preflight.json').read_text())['old_registry_sha256']
    for name in ['pw.x','mpirun','prterun','pw.hse8.outer','pw.hse8.fixedTR']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    dest=r.HERE/'evidence';dest.mkdir(exist_ok=False);files={}
    names=['pw.in','pw.out','JOB.json','READY.json','REFERENCED.json','LAUNCH.json','RANKS.json','GUARD_RESULT.json','TERMINAL.json','telemetry.jsonl']
    for name in names:
        f=root/name;target=dest/name;shutil.copy2(f,target);files[str(f)]=dict(sha256=r.sha(f),bytes=f.stat().st_size,archive_relative=str(target.relative_to(r.HERE)))
    for f in sorted((root/'pilot').iterdir())+list((root/'pp').iterdir()):files[str(f)]=dict(sha256=r.sha(f),bytes=f.stat().st_size,retained_private=True)
    account=r.Account(root,14*r.GIB,64*(1<<20),r.LinuxGuard(r.LIB)).sample()
    prior=json.loads((old/'final_preservation_account.json').read_text())['final_pair_output_charge_B']
    assert account['budget_charge_bytes']+prior<14*r.GIB
    (r.HERE/'evidence_manifest.json').write_text(json.dumps(dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='63b8d75',verdict='REFUSED_REFERENCE_BYTE_MISMATCH',QE_ELF=str(r.QE),QE_ELF_sha256=r.sha(r.QE),files=files),indent=2)+'\n')
    (r.HERE/'protected_after.json').write_bytes((r.HERE/'protected_before.json').read_bytes())
    for f in r.HERE.glob('*.py'):ast.parse(f.read_text())
    for f in r.HERE.rglob('*.json'):json.loads(f.read_text())
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),all_frozen_pins_match=True,protected_DFT_exact=True,old_native_evidence_exact=True,
        known_lock_free=True,old_ledger_exact=True,own_cgroup_absent=True,no_live_visible_native_names=True,hostwide_absence_claim=False,
        original_byte_refusal_unchanged=True,no_accepted_FINAL=True,new_output_charge_B=account['budget_charge_bytes'],preceding_host_output_charge_B=prior,
        combined_phase_output_B=prior+account['budget_charge_bytes'],below14GiB=True,account=account,no_new_native_invocation=True)
    (r.HERE/'final_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='account'},indent=2))

if __name__=='__main__':main()
