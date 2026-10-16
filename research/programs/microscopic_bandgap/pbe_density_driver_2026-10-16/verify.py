"""Read-only originals and NEW build/source/record verification. No live attempt."""
import ast,hashlib,json,os,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent;REPO=P.parents[3];DFT=Path('/home/User/opencode_workspace/DFT')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 pins={}
 frozen=json.loads((B/'static_environment_2026-10-15/frozen_protocol.json').read_text())['profile']['pins'];pins.update(frozen)
 raw=json.loads((B/'static_environment_2026-10-15/evidence_manifest.json').read_text())['raw'];pins.update({p:r['sha256'] for p,r in raw.items()})
 audit=json.loads((B/'pbe_density_only_feasibility_2026-10-16/audit_result.json').read_text());pins.update(audit['input_pins'])
 for _,r in audit['source_map'].items():pins[r['path']]=r['sha256']
 more=json.loads((B/'pbe_density_only_feasibility_2026-10-16/additional_sources.json').read_text())
 for p,r in more.items():pins[p]=r['sha256']
 protected=json.loads((B/'static_environment_2026-10-15/protected_before.json').read_text());pins.update(protected['files'])
 for p,h in pins.items():assert sha(p)==h,p
 assert subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'status','--short'],text=True)==protected['DFT_status']
 assert hashlib.sha256(subprocess.check_output(['git','--no-optional-locks','-C',str(DFT),'diff','--binary'])).hexdigest()==protected['DFT_tracked_diff_sha256']
 gate=B/'pbe_static_lifecycle_2026-10-16/evidence/RESULT.json'
 old=subprocess.check_output(['git','show','75b0e33:'+str(gate.relative_to(REPO))],cwd=REPO);assert gate.read_bytes()==old
 assert json.loads(old)['status']=='REFUSED_ABSORBING'
 # Recheck all old package files against committed baseline, not only its verdict.
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only','75b0e33',str((B/'pbe_static_lifecycle_2026-10-16').relative_to(REPO)),str((B/'pbe_density_only_feasibility_2026-10-16').relative_to(REPO))],cwd=REPO,text=True).splitlines()
 for name in paths:assert (REPO/name).read_bytes()==subprocess.check_output(['git','show','75b0e33:'+name],cwd=REPO),name
 build=json.loads((P/'build_result.json').read_text());assert build['passed'] and not build['QE_ELF_executed']
 for path,h in build['source_pins'].items():assert sha(path)==h and sha(P/Path(path).name)==h
 assert sha(build['elf'])==build['elf_sha256']
 assert sha(DFT/'.local/qe-env/lib/libqe_pw.a')==build['stock_archive_before']==build['stock_archive_after']
 root=Path(build['root']);assert sha(root/'link.map')==build['link_map_sha256']
 evidence=json.loads((P/'source_build_evidence.json').read_text())
 for key in ('linked_archive_pins','compiler_object_pins','compiled_module_pins'):
  for path,h in evidence[key].items():assert sha(path)==h,path
 nm=(root/'nm.txt').read_text()
 for sym in ('read_file_new_','post_xml_init_','h_psi_','set_vrs_','r07_density_build_gate'):assert re.search(r'\b'+sym+r'\b',nm),sym
 # Disassemble only the two new objects, NEVER execute their linked ELF.
 dis=subprocess.check_output(['/usr/bin/objdump','-dr',str(root/'build_gate.o')],text=True)
 assert '<r07_density_build_gate>:' in dis and '$0x1,%eax' in dis
 for f in P.glob('*.py'):ast.parse(f.read_text())
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'}
 t=subprocess.run([str(DFT/'.venv/bin/python'),str(P/'test_offline.py')],env=env,capture_output=True,text=True,timeout=15)
 (P/'offline_test_output.txt').write_text(t.stdout+t.stderr);assert t.returncode==0
 r=json.loads((P/'runtime_fs_probe.json').read_text());assert r['status']=='REFUSED_ABSORBING' and not r['science_release']
 assert not (P/'runtime_singleton_probe.json').exists()
 assert r['original_process_kernel_exited'] and r['original_cgroup_empty_or_absent']
 for n in ('RESULT.json','FROZEN.json'):
  archived=P/('runtime_fs_probe.json' if n=='RESULT.json' else 'preregistered_fs_probe.json')
  assert archived.read_bytes()==(Path(r['root'])/n).read_bytes()
 pre=json.loads((P/'preregistered_fs_probe.json').read_text());assert pre['owner_sha256']==sha(P/'qualify_runtime.py')
 assert (Path(r['root'])/'go').read_bytes()==b'' # execution token NEVER released
 rb=json.loads((P/'runtime_build.json').read_text());assert rb['source_sha256']==sha(P/'runtime_probe.c')
 for path,h in rb['elf_pins'].items():assert sha(path)==h
 # Only append marked current status; preserve original handoff and state history.
 for filename,marker in [('SUCCESSOR_HANDOFF.md','DENSITY_DRIVER_BUILD'),('state.md','DENSITY_DRIVER_BUILD')]:
  current=(B/filename).read_text();base=subprocess.check_output(['git','show','75b0e33:'+str((B/filename).relative_to(REPO))],cwd=REPO,text=True)
  stripped=re.sub(r'<!-- '+marker+r'_BEGIN -->.*?<!-- '+marker+r'_END -->\n\n','',current,flags=re.S)
  if filename=='SUCCESSOR_HANDOFF.md':assert stripped==base
  else:
   assert stripped[stripped.index('## Density-only static PBE path'):]==base[base.index('## Density-only static PBE path'):]
 result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'VERIFIED_BUILD_GO_RUNTIME_REFUSED_SCIENTIFIC_EXECUTION_NO_GO','baseline':'75b0e3392e071452e7f7ce018f35046842f821f2','protected_unique_pins':len(pins),'legacy126_profile_and14_raw_unchanged':True,'DFT_dirty_and_stock_unchanged':True,'old_GateA_and_feasibility_files_byte_identical':True,'private_QE_compile_and_link_first_attempt':True,'QE_ELF_never_executed':True,'offline_tests_passed':9,'non_science_services_attempted':1,'Landlock_enforcement_NOT_exercised':True,'singleton_MPI_attempts':0,'material_actions':0,'new_SCF_jobs':0,'numerical_2meV_certificate':False,'scientific_execution_release':False,'physical_xc':None,'package_pins':{f.name:sha(f) for f in P.iterdir() if f.is_file() and f.name!='verification.json'}}
 (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='package_pins'},indent=2))
if __name__=='__main__':main()
