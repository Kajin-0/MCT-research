"""R07 Stage0 isolated dry and primitive owner preparation; never launches native QE."""
from pathlib import Path
import json,uuid,socket,hashlib,os,sys
import run_vca as r
def prepare():
 if r.PAIR.exists() or (r.HERE/'owner_frozen_protocol.json').exists():raise RuntimeError('no reuse')
 # Never run while another protected lease exists.
 ledger=json.loads(r.REGISTRY.read_text())
 assert ledger['phase']=='FINISHED' and ledger['members']==[]
 r.PAIR.mkdir(mode=0o700)
 deck=(r.HERE/'pbe_vca_x025.in').read_text()
 assert "nbnd=46" in deck and "2 2 2 0 0 0" in deck
 for member in ['dry','primitive']:
  root=r.PAIR/member;root.mkdir(mode=0o700)
  for sub in ['out','tmp','pp']:(root/sub).mkdir(mode=0o700)
  for s in ['Te']:
   source=r.DFT/'pseudopotentials'/f'{s}_sg15_pbe_fr_v12.UPF'
   (root/'pp'/source.name).write_bytes(source.read_bytes())
  vca=r.DFT/'.local/r07s2_20261017_pseudo/NewPseudo.UPF'
  (root/'pp'/'VCA_HgCd_x025.UPF').write_bytes(vca.read_bytes())
  path=r.checked_address(root)
  assert len(path.encode())<=107
  sock=socket.socket(socket.AF_UNIX)
  cli=socket.socket(socket.AF_UNIX)
  try:
   sock.bind(path);ino=Path(path).lstat().st_ino;sock.listen(1);cli.connect(path);peer,_=sock.accept();peer.close()
  finally:
   cli.close();sock.close()
   if Path(path).exists() and Path(path).lstat().st_ino==ino:Path(path).unlink()
  assert r.Account.permitted(type('Root',(),{'root':root})(),Path(path),'socket')
  text=deck.replace("outdir='./out'","outdir='"+str(root/'out')+"'").replace("pseudo_dir='./pp'","pseudo_dir='"+str(root/'pp')+"'")
  (root/'pw.in').write_text(text)
  r.refuse_reuse(root)
 paths=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,r.HERE.parent/'pbe_bridge_prereg_2026-10-17/protocol.md',r.HERE/'pbe_vca_x025.in',r.HERE/'pbe_vca_x025.in',r.HERE/'run_vca.py',r.HERE/'prepare_vca.py',r.HERE/'pbe_vca_x025.in']
 for f in ['native_resource_guard.py','address_admission.py']:
  paths.append(r.HERE.parent/'chemical_pbe16_p2_2026-10-15'/f)
 for root in [r.BASE/'terminal_owner_2026-10-14',r.BASE/'runtime_admission',r.BASE/'cgroup_owned_2026-10-13']:
  for name in {'terminal_owner_2026-10-14':['retirement.py','sampled_output.py'],
               'runtime_admission':['process_identity.py','family_runtime.py'],
               'cgroup_owned_2026-10-13':['contracts.py']}[root.name]:
   paths.append(root/name)
 for m in ['dry','primitive']:
  root=r.PAIR/m
  paths += [root/'pw.in',root/'pp/VCA_HgCd_x025.UPF',root/'pp/Te_sg15_pbe_fr_v12.UPF']
 profile=dict(kind='R07_PBE_VCA_X025_STAGE2_EXPLORATORY_V1',physical=dict(nat=2,nbnd=46,nelec=36,kmesh=[2,2,2,0,0,0],cutoffs_Ry=[50,200],smear_fd_Ry=.001),limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=900,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB,file=r.GIB,escrow=64*(1<<20)),pins={str(p):r.sha(p) for p in paths},ranks=2)
 r.atomic_json(r.PAIR/'PROFILE.json',profile)
 jobs={}
 for m in ['dry','primitive']:
  root=r.PAIR/m
  jobs[m]=dict(kind=profile['kind'],root=str(root),member=m,unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
  r.atomic_json(root/'JOB.json',jobs[m])
 r.atomic_json(r.HERE/'owner_frozen_protocol.json',dict(profile=profile,jobs=jobs))
 for m in jobs:r.load(m)
 storage=r.LinuxGuard(r.LIB).probe(r.PAIR);headroom=r.memory()['MemAvailable']
 pre=r.admission(storage,[64*2**20],14*2**30,headroom)
 r.atomic_json(r.HERE/'owner_preflight.json',dict(admission=pre,storage=storage,mem_available_B=headroom,addresses={m:r.checked_address(r.PAIR/m) for m in jobs},native_authorized=False,typed_rank_test='PENDING_DRY_RUN',profiles_sha256=r.digest(profile)))
 print(json.dumps({'PASS_preflight':True,'kind':profile['kind'],'storage_admission':pre,'roots':list(jobs)},indent=2))
if __name__=='__main__':prepare()
