"""One-time compact evidence intake and read-only protected-state verification.

No execution of QE, MPI or systemd jobs; refuses existing archive destinations.
Large native spinors remain pinned in private DFT storage.
"""
from pathlib import Path
from datetime import datetime, timezone
import fcntl
import gzip
import json
import os
import subprocess
import run_k3 as runtime

HERE=Path(__file__).resolve().parent
PAIR=runtime.PAIR
DFT=runtime.DFT
read=lambda p:json.loads(Path(p).read_text())


def protected_snapshot():
    before=read(HERE/'protected_before.json')
    result=dict(DFT_HEAD=subprocess.check_output(['git','-C',str(DFT),'rev-parse','HEAD'],text=True).strip(),
        DFT_status=subprocess.check_output(['git','-C',str(DFT),'status','--short'],text=True),
        DFT_tracked_diff_sha256=runtime.hashlib.sha256(subprocess.check_output(['git','-C',str(DFT),'diff','--binary'])).hexdigest(),
        files={name:runtime.sha(name) for name in before['files']},MCT_parent=before['MCT_parent'])
    if result!=before:raise ValueError('protected DFT/stock/dirty state changed')
    return result


def evaluate():
    dest=HERE/'native_evidence'
    if dest.exists():raise FileExistsError('preserve existing evidence')
    frozen=read(HERE/'frozen_protocol.json')
    for name,pin in frozen['profile']['pins'].items():
        if runtime.sha(name)!=pin:raise ValueError('frozen pin changed: '+name)
    accounts=[];terminal=[]
    for member in ['host','cd']:
        root=PAIR/member;f=read(root/'FINAL.json');t=read(root/'TERMINAL.json')
        if not f['accepted'] or not t['terminal'] or t['manager']['ExecMainStatus']!='0':raise ValueError('terminal/science gate')
        if Path('/sys/fs/cgroup'+f['guard']['cgroup']).exists():raise ValueError('owned group remains')
        accounts.append(runtime.Account(root,14*2**30,64*2**20).sample())
        terminal.append(dict(member=member,unit=frozen['jobs'][member]['unit'],invocation=f['guard']['invocation'],owned_group_absent=True))
    total=sum(v['budget_charge_bytes'] for v in accounts)
    if total>14*2**30:raise ValueError('independent final aggregate gate')
    fd=os.open(runtime.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(fd)
    ledger=read(runtime.REGISTRY);old=read(HERE/'preflight.json')['old_registry']
    if ledger!=old or ledger['phase']!='FINISHED' or ledger['members']:raise ValueError('protected old ledger changed')
    after=protected_snapshot()
    inventory={};dest.mkdir()
    for member in ['host','cd']:
        root=PAIR/member;target=dest/member;target.mkdir()
        paths=[root/n for n in ['pw.in','JOB.json','READY.json','RANKS.json','LAUNCH.json','GUARD_RESULT.json','FINAL.json','TERMINAL.json','pw.out','telemetry.jsonl']]
        paths.append(root/'out/r07pbe.save/data-file-schema.xml')
        for p in paths:
            raw=p.read_bytes();name=p.name
            compressed=name in ['pw.out','telemetry.jsonl'];out=target/(name+'.gz' if compressed else name)
            payload=gzip.compress(raw,mtime=0) if compressed else raw;out.write_bytes(payload)
            inventory[str(p)]=dict(source_sha256=runtime.sha(p),source_bytes=len(raw),archive_relative=str(out.relative_to(HERE)),archive_sha256=runtime.sha(out),compression='gzip' if compressed else None)
        for p in (root/'out/r07pbe.save').glob('wfc*.hdf5'):
            inventory[str(p)]=dict(source_sha256=runtime.sha(p),source_bytes=p.stat().st_size,archive_relative=None,retained_private=True)
    (dest/'PROFILE.json').write_bytes((PAIR/'PROFILE.json').read_bytes())
    record=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='3fe5ef2',native_root=str(PAIR),files=inventory,
        unchanged_profile_pins=True,protected_state_unchanged=True,large_spinors_retained_private=True,native_HSE_launched=False)
    def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    save('evidence_manifest.json',record);save('protected_after.json',after)
    save('final_retained_account.json',dict(final_independent_aggregate_B=total,member_accounts=accounts,passed=True,sampled_not_continuous=True))
    save('terminal_cleanup.json',dict(timestamp_UTC=record['timestamp_UTC'],members=terminal,exclusive_lock_available=True,old_ledger=ledger,old_ledger_sha256=runtime.sha(runtime.REGISTRY),protected_state_unchanged=True))
    print(json.dumps(dict(aggregate_B=total,protected=True,owned_groups_absent=True,files=len(inventory)),indent=2))


if __name__=='__main__':evaluate()
