"""Independent read-only preservation/result checks; never creates a unit."""
from pathlib import Path
from datetime import datetime,timezone
import ast
import hashlib
import json
import shutil
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import owner
from protocol import sha,durable
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=HERE.parents[3]
DFT=Path('/home/User/opencode_workspace/DFT')

def main():
    frozen=json.loads((HERE/'frozen_execution.json').read_text());profile=frozen['profile'];root=Path(profile['root'])
    before=json.loads((HERE/'preflight.json').read_text())
    for p,h in profile['pins'].items():assert sha(p)==h,p
    for case,j in frozen['jobs'].items():
        assert j['profile_sha256']==owner.digest(profile)
        assert j['job_sha256']==owner.digest({k:v for k,v in j.items() if k!='job_sha256'})
        assert json.loads((root/case/'JOB.json').read_text())==j
        assert json.loads((root/case/'PROFILE.json').read_text())==profile
    result=json.loads((root/'positive/RESULT.json').read_text())
    cleanup=json.loads((root/'positive/CLEANUP.json').read_text())
    started=json.loads((root/'positive/STARTED.json').read_text())
    command=json.loads((root/'positive/COMMAND.json').read_text())
    assert result['status']=='REFUSED_ABSORBING' and result['ranks']=={} and result['finals']==[]
    assert result['error']=='incomplete/unknown live final pair'
    assert not (root/'positive/LIVE_BEGIN.json').exists() and not (root/'positive/LIVE_FINAL.json').exists()
    assert not (root/'positive/OUTSIDE_FINAL.json').exists()
    assert cleanup['clean'] and cleanup['refusal_preserved'] and cleanup['client_returncode']!=0
    assert cleanup['known_members_pidfds_exited'] and cleanup['cgroup_empty_or_absent']
    assert cleanup['manager']['InvocationID']==result['invocation']==started['invocation']
    assert cleanup['manager']['Id']==result['unit'] and cleanup['manager']['MainPID']=='0'
    assert cleanup['manager']['ActiveState']=='failed' and cleanup['manager']['Result']=='exit-code'
    assert not (root/'PENDING_UNIT.json').exists()
    assert not (root/'missing_final/COMMAND.json').exists() and not (root/'missing_final/output.escrow').exists()
    # Verify actual installed controls, not merely proposed command switches.
    manager=started['manager'];kernel=started['kernel']
    for k,v in dict(MemoryMax=str(12<<30),MemorySwapMax='0',TasksMax='12',RuntimeMaxUSec='10min',
                    Restart='no',Delegate='no',Transient='yes',NoNewPrivileges='yes').items():assert manager[k]==v
    for k,v in dict(memory_max=str(12<<30),swap_max='0',tasks_max='12',oom_group='1').items():assert kernel[k]==v
    assert started['holder_cgroup']!=manager['ControlGroup']
    # Only the freshly bound unit is queried; no host process search.
    live=owner.show(result['unit'])
    assert live['LoadState']=='not-found' or (live['InvocationID']==result['invocation'] and live['ActiveState']=='failed' and live['MainPID']=='0')
    cg=owner.cgroup_path(manager['ControlGroup'])
    assert not cg.exists() or (not (cg/'cgroup.procs').read_text().strip() and not any(cg.glob('*/cgroup.procs')))
    assert owner.show(frozen['jobs']['missing_final']['unit'])['LoadState']=='not-found'
    # This is terminal retained-tree accounting, not a live-FD substitute.
    output=[]
    for case in ['positive','missing_final']:
        account=owner.Account(root/case,14<<30,64<<20)
        output.append(account.sample())
    assert sum(r['budget_charge_bytes']+r['escrow_blocks_bytes'] for r in output)<14<<30
    # Preserve original frozen implementation, source build pins and refused raw.
    original=BASE/'pbe_static_completion_2026-10-16'
    oldver=json.loads((original/'verification.json').read_text())
    for name,h in oldver['package_sha256'].items():assert sha(original/name)==h,name
    raw=json.loads((BASE/'static_environment_2026-10-15/evidence_manifest.json').read_text())['raw']
    for p,r in raw.items():assert sha(p)==r['sha256'],p
    oldprofile=json.loads((BASE/'static_environment_2026-10-15/frozen_protocol.json').read_text())['profile']
    for p,h in oldprofile['pins'].items():assert sha(p)==h,p
    protected=json.loads((BASE/'static_environment_2026-10-15/protected_before.json').read_text())
    for p,h in protected['files'].items():assert sha(p)==h,p
    status=subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)
    diff=subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'diff','--binary'])
    assert status==before['DFT_status']==protected['DFT_status']
    assert hashlib.sha256(diff).hexdigest()==before['DFT_tracked_diff_sha256']==protected['DFT_tracked_diff_sha256']
    assert sha(owner.REGISTRY)==before['ledger_sha256']
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=False)
    manifest={}
    for name in ['STARTED.json','COMMAND.json','RESULT.json','CLEANUP.json','pw.out','JOB.json']:
        src=root/'positive'/name;dst=evidence/name
        shutil.copyfile(src,dst);assert sha(src)==sha(dst)
        manifest[str(src)]=dict(sha256=sha(src),bytes=src.stat().st_size,copy='evidence/'+name)
    out=dict(status='GATE_A_NO_GO_ACTUAL_OWNER_REFUSAL_BEFORE_RANK_REGISTRATION',UTC=datetime.now(timezone.utc).isoformat(),
        baseline='9f59814',live_service_attempts=1,live_negative_attempts=0,retries=0,
        unit=result['unit'],invocation=result['invocation'],actual_authenticated_ranks=0,actual_live_finals=0,
        MPI_collective_completion_NOT_demonstrated=True,real_manager_and_cgroup_controls_verified=True,
        cleanup_verified_in_actual_owner_and_independent_terminal_observation=True,
        failed_transient_metadata_retained_NO_active_service=True,terminal_owned_output_accounts=output,
        package_and_frozen_runtime_pins_unchanged=True,old_refused_raw_pins_unchanged=len(raw),
        old_profile_pins_unchanged=len(oldprofile['pins']),DFT_dirty_and_stock_and_protected_pins_unchanged=True,
        protected_old_family_ledger_unchanged=True,evidence=manifest,
        source_and_compile_PASS_not_lifecycle_PASS=True,Gate_B_or_science_release=False,
        native_QE_PW_HSE_SCF_saved_density_actions=0,scientific_resource_or_2meV_certificate=False,
        live_crash_cancel_and_deliberate_negative_NOT_exercised=True,
        hostwide_MPI_absence_proved=False,private_network_namespace_proved=False,physical_xc=None)
    for p in HERE.glob('*.py'):ast.parse(p.read_text())
    durable(HERE/'verification.json',out);print(json.dumps(out,indent=2))

if __name__=='__main__':main()
