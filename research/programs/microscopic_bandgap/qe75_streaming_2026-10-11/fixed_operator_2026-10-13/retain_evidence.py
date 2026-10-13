"""Archive small native logs/metadata and hashes of retained large private data.
No service or QE invocation. Does not copy wave/PP/q-store data into Git.
"""
import datetime,json,hashlib,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import owned_pair as o
from verify_result import verify

def main():
 result=verify();raw=HERE/'raw';raw.mkdir(exist_ok=True)
 records=[]
 for label,root in [('setup_v1',o.ROOT/'fixed_operator_20261013/setup'),('setup_v2',o.PRIVATE/'setup'),('stream',o.PRIVATE/'stream')]:
  for path in sorted(root.rglob('*')):
   if not path.is_file() or path.name=='output.escrow':continue
   record=dict(member=label,path=str(path),bytes=path.stat().st_size,sha256=o.sha(path));records.append(record)
  for name in ['pw.in','pw.out','RESULT.json','JOB.json','PROFILE.json','KERNEL_ADMISSION.json','SAMPLES.json','ERROR_TRACE.json','FIXED_INPUT_CERTIFICATE.json','KERNEL_CERTIFICATE.json','STREAM_RESERVED.json','EXCHANGE_CERTIFICATE.json']:
   p=root/name
   if p.exists():
    n=label+'_'+name+('.txt' if name in ['pw.in','pw.out'] else '')
    (raw/n).write_bytes(p.read_bytes())
 for p in [o.CONTROL_ROOT/'diag'/f'rank{r}.k{k}.{s}' for r in [0,1] for k in [1,2,3] for s in ['before','after']]:records.append(dict(member='control',path=str(p),bytes=p.stat().st_size,sha256=o.sha(p)))
 (HERE/'raw_provenance.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),records=records,raw_large_arrays_retained_private=True,original_control_and_full_state_refusal_untouched=True),indent=2)+'\n')
 before=json.loads((HERE/'protected_before.json').read_text())
 actual=dict(DFT_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=o.DFT,text=True).strip(),DFT_status=subprocess.check_output(['git','status','--porcelain'],cwd=o.DFT,text=True),DFT_tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'],cwd=o.DFT)).hexdigest(),stock_QE_path=before['stock_QE_path'],stock_QE_sha256=o.sha(before['stock_QE_path']),sessions=subprocess.check_output(['tmux','list-sessions'],text=True))
 for k,v in actual.items():
  if before[k]!=v:raise o.Refusal('protected state changed: '+k)
 actual.update(protected_old_ledger_unchanged=True,known_shared_lease_holders=o.flock_owner(o.LOCK),own_units={label:o.show(root['unit'])['LoadState'] for label,root in [('setup_v1',json.loads((o.ROOT/'fixed_operator_20261013/setup/RESULT.json').read_text())),('setup_v2',json.loads((o.PRIVATE/'setup/RESULT.json').read_text())),('stream',json.loads((o.PRIVATE/'stream/RESULT.json').read_text()))]})
 if actual['known_shared_lease_holders'] or any(v!='not-found' for v in actual['own_units'].values()):raise o.Refusal('cleanup incomplete')
 (HERE/'protected_after.json').write_text(json.dumps(actual,indent=2)+'\n')
 # Delete only dispensable, uniquely owned escrow after independently proven empty group.
 p=o.PRIVATE/'stream/output.escrow'
 if p.exists():
  s=p.stat()
  if s.st_nlink!=1 or s.st_uid!=o.os.getuid() or s.st_size!=o.ESCROW:raise o.Refusal('escrow identity')
  record=dict(path=str(p),dev=s.st_dev,inode=s.st_ino,bytes=s.st_size,all_native_outputs_preserved=True)
  p.unlink();(HERE/'escrow_retirement.json').write_text(json.dumps(record,indent=2)+'\n')
 (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Actual raw logs/metadata retained; large array hashes recorded; protected states byte-exact; owned units collected, lease free.')
if __name__=='__main__':main()
