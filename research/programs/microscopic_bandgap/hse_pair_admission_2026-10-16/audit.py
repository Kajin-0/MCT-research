"""One bounded READ-ONLY HSE scientific admission audit, NOT a launch tool.
Only writes audit.json in this scoped MCT package. Never runs a solver/build.
"""
import collections,hashlib,json,os,platform,re,struct,subprocess
from datetime import datetime,timezone
from pathlib import Path
from xml.etree import ElementTree as ET
P=Path(__file__).resolve().parent;B=P.parent;REPO=P.parents[3]
DFT=Path('/home/User/opencode_workspace/DFT');ENV=DFT/'.local/qe-env';QE=DFT/'.local/qe75_lowram_20261011/q-e'
GIB=1<<30
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def require(v,name):
 if not v:raise RuntimeError(name)
def main():
 pins={};artifacts={};model={};relax=B/'chemical_hse_relax_2026-10-15';frozen=json.loads((relax/'frozen_protocol.json').read_text())
 builds={folder:json.loads((B/folder/'build_results.json').read_text()) for folder in ['chemical_hse_relax_2026-10-15','hybrid_convergence_2026-10-15','single_state304_2026-10-15']}
 binaries={'stock_QE75':ENV/'bin/pw.x'}
 for folder,r in builds.items():binaries[folder]=Path(r['binary'])
 for label,path in binaries.items():
  h=sha(path);expected=frozen['profile']['pins'][str(path)] if label=='stock_QE75' else builds[label]['binary_sha256'];require(h==expected,'ELF pin '+label)
  header=subprocess.check_output(['/usr/bin/readelf','-h',str(path)],text=True)
  artifacts[label]={'path':str(path),'sha256':h,'bytes':path.stat().st_size,'ELF_header':header,'executed':False};pins[str(path)]=h
 for name in ['exx','mp_global','wvfct','klist','scf','becmod','noncollin_module']:
  paths=list((ENV/'include/qe').rglob(name+'.mod'));require(len(paths)==1,'module '+name);p=paths[0];pins[str(p)]=sha(p)
 backend=builds['chemical_hse_relax_2026-10-15']['backends']
 for path,h in backend.items():require(sha(path)==h,'backend '+path)
 source_files=[QE/'PW/src/h_psi.f90',QE/'PW/src/input.f90',QE/'PW/Doc/INPUT_PW.def',QE/'KS_Solvers/Davidson/cegterg.f90',DFT/'src/mct_dft/runner.py',DFT/'scripts/run_stage.py',relax/'run_pilot_fixed.py',relax/'pilot_native.inc']
 # Use pristine native EXX, NOT the protected streaming-modified working source.
 src=DFT/'.local/qe75_lowram_20261011/h8r_20261015/build1/source'
 source_files += [src/'pristine_exx.f90',src/'pristine_electrons.f90',src/'electrons.f90',src/'run_pwscf.f90']
 for p in source_files:pins[str(p)]=sha(p)
 for member in ('host','cd'):
  root=Path(frozen['jobs'][member]['root']);inp=root/'pw.in';xml=root/'out/r07hse8.save/data-file-schema.xml'
  require(inp.read_bytes()==(relax/'evidence'/member/'pw.in').read_bytes(),'archive input equality')
  require(xml.read_bytes()==(relax/'evidence'/member/'data-file-schema.xml').read_bytes(),'archive XML equality')
  for p in (inp,xml,root/'reference.bin',root/'out/r07hse8.save/charge-density.hdf5'):
   h=sha(p);pins[str(p)]=h
   if str(p) in frozen['profile']['pins']:require(h==frozen['profile']['pins'][str(p)],'frozen input pin')
  out=ET.parse(xml).find('output');atoms=out.find('atomic_structure/atomic_positions');counts=collections.Counter(a.attrib['name'] for a in atoms)
  pps={}
  for name in ('Hg','Cd','Te'):
   pp=root/'pp'/f'{name}_sg15_pbe_fr_v12.UPF';h=sha(pp);require(h==frozen['profile']['pins'][str(pp)],'PP pin');pins[str(pp)]=h;header=ET.parse(pp).find('PP_HEADER').attrib
   require(all(header[k]==v for k,v in {'pseudo_type':'NC','relativistic':'full','has_so':'T','is_ultrasoft':'F','is_paw':'F','core_correction':'F'}.items()),'PP domain')
   pps[name]={'sha256':h,'path':str(pp),'z_valence':float(header['z_valence']),'functional':header['functional'],'type':'FR NC noNLCC'}
  mag=out.find('magnetization');band=out.find('band_structure');hyb=out.find('dft/hybrid');basis=out.find('basis_set');geom=out.find('atomic_structure')
  headers=[]
  for rank in (0,1):
   packet=root/'pilot'/f'c2_before.rank{rank}'
   with packet.open('rb') as f: h=struct.unpack('<16q',f.read(128));ex=struct.unpack('<10q',f.read(80))
   require(h[0]==7025101408 and h[3]==rank and h[7:9]==(176,2) and h[12:14]==(144,2),'accepted packet header')
   headers.append({'path':str(packet),'sha256':sha(packet),'header16':h,'EXX_extent10':ex})
  with (root/'reference.bin').open('rb') as f:ref=struct.unpack('<4q',f.read(32))
  m={'input':str(inp),'input_sha256':sha(inp),'XML':str(xml),'XML_sha256':sha(xml),'counts':dict(counts),'nelec':float(band.findtext('nelec')),'bands':int(band.findtext('nbnd')),'cutoffs_Ry':[2*float(basis.findtext(t)) for t in ('ecutwfc','ecutrho')],'Fock_Ry':2*float(hyb.findtext('ecutfock')),'HSE_fraction':float(hyb.findtext('exx_fraction')),'screening_Bohr_inverse':float(hyb.findtext('screening_parameter')),'functional':out.findtext('dft/functional'),'k_grid':band.find('starting_k_points/monkhorst_pack').attrib,'q_grid':hyb.find('qpoint_grid').attrib,'sigma_Ry':2*float(band.find('smearing').attrib['degauss']),'smearing':band.findtext('smearing'),'magnetization':{n:mag.findtext(n) for n in ('noncolin','spinorbit','do_magnetization')},'cell_Bohr':[[float(v) for v in geom.findtext('cell/'+n).split()] for n in ('a1','a2','a3')],'positions':[(a.attrib['name'],[float(v) for v in a.text.split()]) for a in atoms],'nsym':int(out.findtext('symmetries/nsym')),'PP':pps,'reference_header':ref,'reference_sha256':sha(root/'reference.bin'),'initial_potential':'atomic; no separately pinned stationary input potential exists for a fresh calculation','starting_wfc':'atomic+random','native_headers':headers,'outer_converged':False}
  require(m['nelec']==sum(counts[sp]*pps[sp]['z_valence'] for sp in counts)==144,'electron accounting')
  require(m['bands']==176 and m['cutoffs_Ry']==[50,200] and m['Fock_Ry']==200 and m['HSE_fraction']==.25 and m['screening_Bohr_inverse']==.106 and m['smearing']=='fd' and m['sigma_Ry']==.001,'model')
  model[member]=m
 require(model['host']['cell_Bohr']==model['cd']['cell_Bohr'] and [p for _,p in model['host']['positions']]==[p for _,p in model['cd']['positions']],'common physical geometry')
 require(model['host']['reference_sha256']==model['cd']['reference_sha256'],'same fixed probes')
 require(model['host']['counts']=={'Hg':4,'Te':4} and model['cd']['counts']=={'Cd':1,'Hg':3,'Te':4},'x=.25 substitution')
 npwx=sum(h['header16'][5] for h in model['host']['native_headers']);require(npwx==10827,'global coefficient count')
 exx=sum(16*h['EXX_extent10'][4]*h['EXX_extent10'][5]*h['EXX_extent10'][6] for h in model['host']['native_headers']);require(exx==1216512000,'EXX subtotal')
 coefficients=16*2*npwx*176
 selected={'aggregate_native_EXX_B':exx,'aggregate_evc_B':coefficients,'Davidson_default_two_large_work_arrays_B':2*16*2*npwx*(2*176),'Davidson_three_small_dense_matrices_replicated_two_ranks_B':2*3*16*(2*176)**2,'beta_vkb_B_if_nkb356':16*npwx*356,'ACE_xi_B_omitted_in_direct_algorithm':coefficients}
 direct=sum(v for k,v in selected.items() if not k.startswith('ACE_'))
 timing=json.loads((relax/'timing_and_resources.json').read_text())['members']
 native=platform.uname();mem={a:int(v.split()[0])*1024 for a,v in (s.split(':',1) for s in Path('/proc/meminfo').read_text().splitlines())};disk=os.statvfs(REPO)
 packages=[]
 for p in (ENV/'conda-meta').glob('*.json'):
  q=json.loads(p.read_text())
  if q['name'] in ('qe','quantum-espresso','quantum_espresso','openmpi','abinit','cp2k','gpaw','pyscf','elk','exciting'):packages.append({k:q.get(k) for k in ('name','version','build')})
 hpsi=(QE/'PW/src/h_psi.f90').read_text();electrons=(src/'electrons.f90').read_text();owner=(relax/'run_pilot_fixed.py').read_text();ordinary=(DFT/'src/mct_dft/runner.py').read_text()
 checks={'stock_direct_exchange_branch_exists':all(x in hpsi for x in ['IF ( use_ace ) THEN','CALL vexx( lda, n, m, psi, hpsi, becp )']),'private_one_relax_has_unconditional_stop':"conv_elec=.FALSE. ! stop after rebuilt second ACE, not outer convergence\n        RETURN" in electrons,'fixed_hse_runner_pins_old_binary_and_root':all(x in owner for x in ["h8r_20261015/build1/pw.hse8.relax","h8r_20261015/p1","profile != frozen['profile']","'no retries/reused state'"]),'ordinary_runner_no_kernel_contract':all(x not in ordinary for x in ['MemoryMax','cgroup','MemorySwapMax','TasksMax','RuntimeMax','aggregate_output'])}
 require(all(checks.values()),'source checks')
 r=dict(UTC=datetime.now(timezone.utc).isoformat(),baseline='bd71deacf79e670419a80e8f4c9262dcaeed3274',verdict='NO_GO_BEFORE_EXECUTION',first_blocker='No existing qualified fresh stock/direct176-band HSE full-SCF launch profile; fixed private runner stops after second ACE.',artifacts=artifacts,modules={k:v for k,v in pins.items() if k.endswith('.mod')},backends=backend,pinned_sources_inputs=pins,matched_archived_model=model,source_checks=checks,known_full_SCF_memory_selected_only_B=selected,selected_direct_payload_sum_NOT_bound_B=direct,complete_direct_SCF_peak_B=None,direct_full_SCF_wall_upper_s=None,accepted_two_build_timing=timing,rejected_eight_build_observed=dict(wall_s=1628.053,allowed_s=600,over_by_s=1028.053,dexx_Ry=1.80403839e-6,target_Ry=1e-9,Theta_defect_lower=.99976526,Gamma8_spread_eV=.6552552,converged=False),hardware=dict(kernel=native.release,architecture=native.machine,logical_CPUs=os.cpu_count(),CPU_affinity=sorted(os.sched_getaffinity(0)),MemTotal_B=mem['MemTotal'],MemAvailable_B=mem['MemAvailable'],free_disk_B=disk.f_bavail*disk.f_frsize,CPU_model=next(s.split(':',1)[1].strip() for s in Path('/proc/cpuinfo').read_text().splitlines() if s.startswith('model name'))),checked_environment_packages=packages,full_scientific_output_upper_B=None,current_host_floors_pass=mem['MemAvailable']>=4*GIB and disk.f_bavail*disk.f_frsize>=10*GIB,new_material_jobs=0,new_services=0,new_builds=0,solver_ELFs_executed=0,new_runner_or_solver=False,PBE_closed=True,physical_xc=None)
 (P/'audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['verdict','first_blocker','hardware','selected_direct_payload_sum_NOT_bound_B','source_checks','checked_environment_packages']},indent=2))
if __name__=='__main__':main()
