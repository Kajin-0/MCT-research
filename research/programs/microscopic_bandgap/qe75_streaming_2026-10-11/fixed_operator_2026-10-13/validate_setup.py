"""Read-only numerical-kernel qualification; original owner failure immutable."""
import json,struct
from pathlib import Path

def validate(root,o):
 root=Path(root);r=json.loads((root/'RESULT.json').read_text());j=json.loads((root/'JOB.json').read_text());p=json.loads((root/'PROFILE.json').read_text())
 if r['reason'] not in ['[Errno 19] No such device','FIXED_KERNEL_CAPTURED']:raise o.Refusal('unclassified setup failure')
 if not r['owned_cgroup_empty'] or o.show(r['unit'])['LoadState']!='not-found':raise o.Refusal('setup not empty/collected')
 if not (r['manager_terminal']['Result']=='exit-code' and r['manager_terminal']['ExecMainStatus']=='1' and 'kernel inputs captured; intentional no-SCF no-ACE stop' in (root/'pw.out').read_text()):raise o.Refusal('exact setup stop absent')
 if list((root/'diag').iterdir()):raise o.Refusal('setup unexpectedly performed EXX/ACE')
 if o.digest(p)!=j['profile_sha256'] or o.sha(j['command'][6])!=p['binary_sha256'] or o.sha(root/'pw.in')!=p['input_sha256']:raise o.Refusal('setup executable/input/profile changed')
 ranks={v['rank']:v['pid'] for v in r['real_rank_receipts'] if v['action']==1}
 if set(ranks)!={0,1} or len(set(ranks.values()))!=2:raise o.Refusal('real setup ranks')
 for stage in [4,5,8,9]:
  a=[v for v in r['real_rank_receipts'] if v['action']==stage]
  if len(a)!=2 or {v['rank'] for v in a}!={0,1}:raise o.Refusal('completed setup native phases')
  for v in a:
   if (v['pid']!=ranks[v['rank']] or v['invocation']!=r['invocation'] or v['job_sha256']!=o.digest(j) or v['profile_sha256']!=o.digest(p)):raise o.Refusal('live setup receipt bindings')
 if r['elapsed_seconds']>600 or r['peak_family_RSS_bytes']>o.MEMORY or r['minimum_MemAvailable_bytes']<4*o.GIB or r['minimum_free_disk_bytes']<10*o.GIB:raise o.Refusal('setup measured guards')
 if any(r['final_kernel']['memory_events'][v] for v in ['max','oom','oom_kill']) or r['final_kernel']['pids_events']['max']:raise o.Refusal('setup kernel pressure')
 for q in (root/'readback').iterdir():
  if q.read_bytes()!=(o.CANONICAL/q.name).read_bytes():raise o.Refusal('actual canonical readback')
 if len(list((root/'readback').iterdir()))!=6:raise o.Refusal('source readback coverage')
 o.fft_compare([o.CONTROL_ROOT/'fft'/f'rank{v}.fft' for v in [0,1]],[root/'fft'/f'rank{v}.fft' for v in [0,1]],dict(stock=o.digest(json.loads((o.CONTROL_ROOT/'PROFILE.json').read_text())),stream=o.digest(p)),p['common_input_sha256'])
 for row in json.loads((root/'KERNEL_CERTIFICATE.json').read_text())['files']:
  raw=Path(row['path']).read_bytes()
  if o.sha(row['path'])!=row['sha256'] or len(raw)!=row['bytes'] or raw[:16]!=b'QE75-KERNEL-01  ' or raw[-16:]!=b'QE75-KERNEL-END ':raise o.Refusal('closed kernel pin')
  if struct.unpack_from('=9q',raw,16)[:4]!=(row['header'][0],3,8,8):raise o.Refusal('kernel complete q coverage')
 files={str(q.relative_to(root)):o.sha(q) for folder in ['readback','kernel','fft'] for q in (root/folder).iterdir()}
 files.update({name:o.sha(root/name) for name in ['pw.in','pw.out','RESULT.json','JOB.json','PROFILE.json','KERNEL_ADMISSION.json','SAMPLES.json']})
 return dict(qualified_fixed_kernel_data=True,owner_RESULT_retained=r['reason'],original_resource_monitor_not_promoted=True,ENODEV_stack_location_not_recorded=True,complete_real_native_phases=[4,5,8,9],numerical_kernel_data_independent_of_post_capture_monitor=True,provenance=files,full_SCF_or_restart=False,continuous_resource_guarantee=False)
