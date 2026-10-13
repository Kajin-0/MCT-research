"""Read-only qualification of the ONE actual streamed first-ACE experiment.
Never edits a native RESULT or issues a lease; no numerical run on replay.
"""
import hashlib,json,struct,sys,datetime
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import owned_pair as o
from compare_pair import decode
import validate_setup

def verify():
 root=o.PRIVATE/'stream';r=json.loads((root/'RESULT.json').read_text());j=json.loads((root/'JOB.json').read_text());p=json.loads((root/'PROFILE.json').read_text())
 expected=str(Path(r['real_rank_receipts'][0]['cgroup'])/'memory.oom.group')
 if r['reason']!='[Errno 2] No such file or directory: '+repr('/sys/fs/cgroup'+expected):raise o.Refusal('not the exact witnessed post-completion cgroup-file error')
 trace=json.loads((root/'ERROR_TRACE.json').read_text())
 if 'last=counters(cg)' not in trace['traceback'] or 'memory.oom.group' not in trace['traceback']:raise o.Refusal('exact error stack not retained')
 if not r['owned_cgroup_empty'] or o.show(r['unit'])['LoadState']!='not-found':raise o.Refusal('owned group not empty/collected')
 if not (r['manager_terminal']['Result']=='exit-code' and r['manager_terminal']['ExecMainStatus']=='1' and 'first ACE captured; intentional fixture stop, not SCF' in (root/'pw.out').read_text()):raise o.Refusal('exact native terminal')
 if o.digest(p)!=j['profile_sha256'] or o.sha(j['command'][6])!=p['binary_sha256'] or o.sha(root/'pw.in')!=p['input_sha256']:raise o.Refusal('actual native executable/input/profile')
 snapshots={str(HERE/'owned_pair.py'):HERE/'executed_owner.py',str(HERE/'sampled_output.py'):HERE/'executed_output.py'}
 for name,digest in j['launch_pins'].items():
  if o.sha(snapshots.get(name,name))!=digest:raise o.Refusal('executed launch pin missing/changed: '+name)
 o.certificate(False) # source/compiler/backend/geometry/PP/seed/disk/RAM checks
 setup=validate_setup.validate(o.PRIVATE/'setup',o)
 ranks={v['rank']:v['pid'] for v in r['real_rank_receipts'] if v['action']==1}
 if set(ranks)!={0,1} or len(set(ranks.values()))!=2:raise o.Refusal('real two-rank registration')
 for stage in [1,4,5,8,9,7,6]:
  rows=[v for v in r['real_rank_receipts'] if v['action']==stage]
  if len(rows)!=2 or {v['rank'] for v in rows}!={0,1}:raise o.Refusal('actual native phase missing')
  for v in rows:
   if v['pid']!=ranks[v['rank']] or v['invocation']!=r['invocation'] or v['job_sha256']!=o.digest(j) or v['profile_sha256']!=o.digest(p):raise o.Refusal('live receipt binding')
 if any(Path('/proc') .joinpath(str(pid)).exists() for pid in ranks.values()):raise o.Refusal('old rank PID not retired')
 if r['elapsed_seconds']>600 or r['peak_family_RSS_bytes']>o.MEMORY or r['minimum_MemAvailable_bytes']<4*o.GIB or r['minimum_free_disk_bytes']<10*o.GIB:raise o.Refusal('measured cap/floor')
 if any(r['final_kernel']['memory_events'][k] for k in ['max','oom','oom_kill']) or r['final_kernel']['pids_events']['max']:raise o.Refusal('kernel limit event')
 samples=json.loads((root/'SAMPLES.json').read_text())
 if not samples or any(not 0<=v['elapsed']<600 or v['RSS']>o.MEMORY or v['MemAvailable']<4*o.GIB or v['disk']<10*o.GIB or v['output']>o.OUTPUT for v in samples):raise o.Refusal('actual retained resource samples')
 for rank in [0,1]:
  for k in [1,2,3]:
   q=root/'readback'/f'rank{rank}.k{k}.input'
   if q.read_bytes()!=(o.CANONICAL/q.name).read_bytes():raise o.Refusal('canonical input byte difference')
  q=root/'kernel'/f'rank{rank}.kernel'
  if q.read_bytes()!=(o.PRIVATE/'setup/kernel'/q.name).read_bytes():raise o.Refusal('screen/kernel byte difference')
 o.fft_compare([o.CONTROL_ROOT/'fft'/f'rank{v}.fft' for v in [0,1]],[root/'fft'/f'rank{v}.fft' for v in [0,1]],dict(stock=o.digest(json.loads((o.CONTROL_ROOT/'PROFILE.json').read_text())),stream=o.digest(p)),p['common_input_sha256'])
 comparison=o.action_compare(o.action_paths(o.CONTROL_ROOT),o.action_paths(root),[1,2,3])
 bitwise=[];energies=[];wk=np.array([.125,.5,.375])
 for k in [1,2,3]:
  for rank in [0,1]:
   for name in ['before','after']:
    a=decode(o.CONTROL_ROOT/'diag'/f'rank{rank}.k{k}.{name}');b=decode(root/'diag'/f'rank{rank}.k{k}.{name}')
    fields=['phi','occupation','probe','vphi','gram','action'] if name=='before' else ['xi','factor','action']
    for field in fields:
     if np.ascontiguousarray(a[field]).tobytes()!=np.ascontiguousarray(b[field]).tobytes():raise o.Refusal('bitwise active comparison: '+field)
    if struct.pack('=d',a['energy'])!=struct.pack('=d',b['energy']):raise o.Refusal('bitwise native energy')
    bitwise.append(dict(rank=rank,k=k,stage=name,all_active_fields_bitwise=True))
  d=decode(root/'diag'/f'rank0.k{k}.before');weights=d['occupation'][:,k-1]*wk[k-1]
  e=0.
  for i in range(48):e+=weights[i]*d['gram'][i,i].real
  if abs(e-d['energy'])>1e-12:raise o.Refusal('independent weighted native energy reconstruction')
  energies.append(dict(k=k,native_weighted_exchange_contraction_Ry=d['energy'],independent_WG_trace_Ry=float(e),difference_Ry=float(e-d['energy'])))
 if not r['protected_old_ledger_unchanged'] or o.sha(o.OLD_REGISTRY)!=json.loads((o.PRIVATE/'PROTECTED_LEDGER.json').read_text())['sha256'] or o.flock_owner(o.LOCK):raise o.Refusal('protected old ledger or lease not closed')
 return dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),numerical_fixed_operator_qualified=True,original_owner_RESULT_retained_failed=True,owner_teardown_race_separately_unqualified=True,actual_control_and_stream_actions_bitwise_on_active_basis=bitwise,comparison=comparison,per_k=energies,summed_native_contraction_Ry=sum(v['native_weighted_exchange_contraction_Ry'] for v in energies),not_final_SCF_Fock_energy=True,stream_measured_summary={k:r[k] for k in ['unit','invocation','elapsed_seconds','peak_family_RSS_bytes','manager_terminal','minimum_MemAvailable_bytes','minimum_free_disk_bytes','output_maximum_sampled_charge_bytes','maximum_output_sample_gap_seconds','real_rank_receipts','reservations']},retained_resource_samples=len(samples),setup_data_qualification=setup,old_full_state_parity_refusal_unchanged=True,original_control_auxiliary_kernel_not_captured_reconstruction_source_conditioned=True,SCF_restart_convergence_physical_xc=False,continuous_resource_guarantee=False,hostwide_exclusion_or_private_network_proven=False)

if __name__=='__main__':
 d=verify();(HERE/'numerical_result.json').write_text(json.dumps(d,indent=2)+'\n')
 print('QUALIFIED actual streamed first ACE: all corresponding active EXX/ACE outputs bitwise; unique-k contraction',d['summed_native_contraction_Ry'],'Ry. Original owner failure retained.')
