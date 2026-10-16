"""Independent immutable-result audit; never launches/repairs/retries a worker."""
import hashlib,json,os,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
from protect import verify,sha
P=Path(__file__).resolve().parent

def main():
 protection=verify();started=json.loads((P/'STARTED.json').read_text());r=json.loads((P/'result_fs.json').read_text());fs,mpi=started['jobs'];root=Path(fs['root'])
 def require(name,v):
  if not v:raise RuntimeError(name)
 require('absorbing_refusal',r['status']=='REFUSED_ABSORBING' and not r['science_release'])
 require('immutable_original_result',(root/'RESULT.json').read_bytes()==(P/'result_fs.json').read_bytes())
 require('fresh_nonce_FS',(root/'go').read_text()==fs['nonce'])
 require('withheld_MPI',not (P/'result_mpi.json').exists() and (Path(mpi['root'])/'go').read_bytes()==b'')
 require('pinned_owner',sha(P/'owner_v2.py')==started['owner_sha256'])
 require('pinned_predicates',sha(P/'checks.py')==started['checks_sha256'])
 build=json.loads((P/'build_result.json').read_text());require('pinned_source',sha(P/'runtime_probe_v2.c')==build['source_sha256'])
 for path,h in build['elf_pins'].items():require('pinned_elf',sha(path)==h)
 data=(P/'predicates_fs.jsonl').read_bytes();require('original_journal',data==(root/'predicates.jsonl').read_bytes())
 lines=data.splitlines(keepends=True);events=[json.loads(s) for s in lines]
 require('ordered_durable_events',all(row['sequence']==i for i,row in enumerate(events)))
 require('monotonic',all(b['monotonic']>=a['monotonic'] for a,b in zip(events,events[1:])))
 release=next(i for i,e in enumerate(events) if e['name']=='PRE_NONCE_COMPLETE');require('all_pre_nonce_passed',all(e['passed'] for e in events[:release+1]))
 failed=next(e for e in events if not e['passed']);require('exact_failure',failed['name']=='BOUNDED_SAMPLE')
 obs=failed['observed'];guards=dict(host=obs['MemAvailable_B']>=4*(1<<30),disk=obs['free_disk_B']>=10*(1<<30),output=max(obs['output_blocks_B'],obs['output_logical_B'])<14*(1<<30),inodes=obs['output_inodes']<128,holder=obs['holder_peak_RSS_B']<512*(1<<20),members=obs['members']==[r['identity']['pid']])
 require('only_holder_predicate_failed',all(v for k,v in guards.items() if k!='holder') and not guards['holder'])
 require('traceback_is_specific','owner_v2.py' in r['traceback'] and 'line 107' in r['traceback'] and 'BOUNDED_SAMPLE' in r['traceback'])
 # Result hashes journal BEFORE post-result RefUnit cleanup append. Preserve and
 # disclose this scope defect; audit prefix+complete journal separately.
 require('cleanup_event_last',events[-1]['name']=='CLEANUP.UnrefUnit')
 prefix=b''.join(lines[:-1]);require('result_journal_prefix',hashlib.sha256(prefix).hexdigest()==r['predicates_sha256'])
 require('native_FS_completion','LANDLOCK abi=7 allowed=1 RO_foreign_TMPDIR_devshm_denied=1 socket_spawn_denied=1 inherited_exemption_demonstrated_then_closed=1' in r['stdout'] and r['stderr']=='')
 require('native_exit_zero',r['terminal_manager']['ExecMainCode']=='1' and r['terminal_manager']['ExecMainStatus']=='0')
 for n in ('input/ro','foreign/canary','foreign/new_missing','temp/ro'):require('unchanged_dummy_canary', (root/n).read_bytes()==b'canary')
 require('explicit_inherited_capability_only',(root/'foreign/inherited').read_bytes()==b'Xanary')
 require('allowed_output',(root/'output/allowed').read_bytes()==b'allowed\n')
 require('original_cleanup',r['process_pidfd_exited'] and r['original_cgroup_empty_or_absent'])
 cleanup={};env=dict(os.environ,XDG_RUNTIME_DIR='/run/user/1001',DBUS_SESSION_BUS_ADDRESS='unix:path=/run/user/1001/bus')
 for j in (fs,mpi):
  c=subprocess.run(['/usr/bin/systemctl','--user','show',j['unit'],'--property=LoadState,ActiveState,MainPID,ControlGroup'],env=env,capture_output=True,text=True,timeout=3)
  cleanup[j['kind']]={'argv':c.args,'returncode':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
  require('owned_unit_unloaded','LoadState=not-found' in c.stdout and 'MainPID=0' in c.stdout)
 cg=Path('/sys/fs/cgroup')/r['identity']['cgroup'].lstrip('/');require('original_cgroup_absent',not cg.exists())
 source_records=json.loads((P/'science_sources.json').read_text())
 for path,info in source_records['native_implementation_sources'].items():require('science_source_pin',sha(path)==info['sha256'])
 for path,h in source_records['existing_result_sources'].items():require('retained_science_pin',sha(path)==h)
 repo=P.parents[3];base=P.parent
 for filename in ('SUCCESSOR_HANDOFF.md','state.md'):
  current=(base/filename).read_text();original=subprocess.check_output(['git','show','0c8df58:'+str((base/filename).relative_to(repo))],cwd=repo,text=True)
  stripped=re.sub(r'<!-- PBE_FINAL_ADMISSION_BEGIN -->.*?<!-- PBE_FINAL_ADMISSION_END -->\n\n','',current,flags=re.S)
  if filename=='SUCCESSOR_HANDOFF.md':require('handoff_history_exact',stripped==original)
  else:require('state_history_exact',stripped[stripped.index('<!-- DENSITY_DRIVER_BUILD_BEGIN -->'):]==original[original.index('<!-- DENSITY_DRIVER_BUILD_BEGIN -->'):])
 sources={str(f):sha(f) for f in P.iterdir() if f.is_file() and f.name!='verification.json'}
 result=dict(UTC=datetime.now(timezone.utc).isoformat(),verdict='TERMINATE_PBE_STATIC_DIAGNOSTIC',scientific_execution_release=False,material_actions=0,native_QE_executions=0,non_science_services=1,singleton_MPI_executions=0,offline_tests=14,actual_Landlock_ABI7_negative_checks_completed=True,sequence_runtime_PASS=False,exact_failed_guard='holder_peak_RSS_B < 536870912',observed_holder_peak_RSS_B=obs['holder_peak_RSS_B'],current_holder_RSS_NOT_recorded=True,only_failed_subpredicate=guards,worker_kernel_peak_B=int(r['terminal_manager']['MemoryPeak']),worker_swap_peak_B=int(r['terminal_manager']['MemorySwapPeak']),worker_elapsed_s=(int(r['terminal_manager']['ExecMainExitTimestampMonotonic'])-int(r['terminal_manager']['ExecMainStartTimestampMonotonic']))/1e6,owner_elapsed_s=r['elapsed_s'],native_evidence_not_scientific_qualification=True,journal_prefix_sha256=r['predicates_sha256'],complete_journal_sha256=sha(P/'predicates_fs.jsonl'),journal_cleanup_append_scope_defect_disclosed=True,old_refusals_unchanged=True,protection=protection,cleanup=cleanup,physical_xc=None,package_pins=sources)
 (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='package_pins'},indent=2))
if __name__=='__main__':main()
