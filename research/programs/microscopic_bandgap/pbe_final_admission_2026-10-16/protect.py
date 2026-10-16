"""Read-only pin/diff verification; no protected writes or native action."""
import hashlib,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent;REPO=P.parents[3];DFT=Path('/home/User/opencode_workspace/DFT');BASELINE='0c8df58'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def verify():
 pins=dict(json.loads((B/'static_environment_2026-10-15/frozen_protocol.json').read_text())['profile']['pins'])
 pins.update({k:v['sha256'] for k,v in json.loads((B/'static_environment_2026-10-15/evidence_manifest.json').read_text())['raw'].items()})
 prior=B/'pbe_density_driver_2026-10-16';old=json.loads((prior/'verification.json').read_text())
 for name,h in old['package_pins'].items():
  if sha(prior/name)!=h:raise RuntimeError('OLD_DRIVER_PACKAGE_CHANGED: '+name)
 ev=json.loads((prior/'source_build_evidence.json').read_text())
 for k in ('linked_archive_pins','compiler_object_pins','compiled_module_pins'):pins.update(ev[k])
 protected=json.loads((B/'static_environment_2026-10-15/protected_before.json').read_text());pins.update(protected['files'])
 for path,h in pins.items():
  if sha(path)!=h:raise RuntimeError('PROTECTED_PIN_CHANGED: '+path)
 status=subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)
 diff=hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'diff','--binary'])).hexdigest()
 if status!=protected['DFT_status'] or diff!=protected['DFT_tracked_diff_sha256']:raise RuntimeError('DFT_DIRTY_CHANGED')
 unchanged=[]
 for folder in ('pbe_density_driver_2026-10-16','pbe_static_lifecycle_2026-10-16','pbe_static_completion_2026-10-16','pbe_density_only_feasibility_2026-10-16'):
  names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE,str((B/folder).relative_to(REPO))],text=True,cwd=REPO).splitlines()
  for n in names:
   if (REPO/n).read_bytes()!=subprocess.check_output(['git','show',BASELINE+':'+n],cwd=REPO):raise RuntimeError('HISTORICAL_FILE_CHANGED: '+n)
  unchanged+=names
 return dict(passed=True,source_data_object_archive_module_pins=len(pins),historical_files_byte_exact=len(unchanged),DFT_dirty_diff_sha256=diff,old_Gate_A_REFUSED=json.loads((B/'pbe_static_lifecycle_2026-10-16/evidence/RESULT.json').read_text())['status'],old_driver_REFUSED=json.loads((prior/'runtime_fs_probe.json').read_text())['status'],baseline=BASELINE)
if __name__=='__main__':
 result=verify()
 if sys.argv[1:]==['--before']:(P/'protection_before.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
