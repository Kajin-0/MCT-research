"""Read-only real full-SCF summaries; convergence is never inferred from exit0."""
import json,re,sys,hashlib,datetime
from pathlib import Path
import numpy as np
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import owned_pair as owner,observables
from conditioning import density

def summarize(root):
 root=Path(root);r=json.loads((root/'RESULT.json').read_text());steps=[json.loads(p.read_text()) for p in root.glob('STEP_*.json')];steps.sort(key=lambda v:v['step'])
 for f in (root/'trajectory').glob('rank0.step*.stage1.scalars'):
  k=int(f.name.split('.step')[1].split('.')[0])
  if k not in {v['step'] for v in steps}:steps.append(dict(step=k,scalar=observables.scalars(root,k,1),online_gate_passed=False))
 steps.sort(key=lambda v:v['step'])
 text=(root/'pw.out').read_text();outer=[]
 previous=None
 for d in steps:
  step=d['step'];s=d['scalar']['values'];p=observables.paths(root,step,1)
  charge_change=None;orbital_change=None
  if previous is not None:
   aa=[observables.decode(observables.paths(root,previous,1)[(r,1)]) for r in [0,1]]
   bb=[observables.decode(p[(r,1)]) for r in [0,1]]
   charge_change={}
   for field in ['rhoR','rhoG']:
    charge_change[field+'_max']=max(observables.maxdiff(a[field],b[field]) for a,b in zip(aa,bb))
    delta=sum(np.linalg.norm(a[field]-b[field])**2 for a,b in zip(aa,bb))
    norm=sum(np.linalg.norm(a[field])**2 for a in aa)
    charge_change[field+'_relative_L2']=float(np.sqrt(delta/max(norm,1e-300)))
   # A trajectory CHANGE, not a same-state equality test or Hpsi residual.
   orbital_change={}
   for k in [1,2,3]:
    aa=[observables.decode(observables.paths(root,previous,1)[(r,k)]) for r in [0,1]]
    bb=[observables.decode(p[(r,k)]) for r in [0,1]]
    A=np.concatenate([v['wave'] for v in aa]);B=np.concatenate([v['wave'] for v in bb]);wk=[.125,.5,.375][k-1]
    fa=aa[0]['wg'][:,k-1]/wk;fb=bb[0]['wg'][:,k-1]/wk
    S=A.conj().T@B;R=B-A@S;M=R.conj().T@R;C=S*fb[None,:];D=np.diag(fa)-(S*fb[None,:])@S.conj().T
    norm2=np.vdot(D,D).real+2*np.trace(C@M@C.conj().T).real+np.sum(fb[:,None]*fb[None,:]*np.abs(M)**2)
    orbital_change[str(k)]=density(A,B,fa,fb)
   # Trajectory diagnostics are computed directly; preregistered comparison
   # thresholds are never changed or applied to physically different steps.
  outer.append(dict(outer_step=step,total_energy_Ry=s['etot_Ry'],native_ef_Ry=s['ef_Ry'],Fock_energy_Ry=.5*s['fock2_Ry'],dexx_Ry=s['dexx_Ry'],tr2_Ry=s['tr2_Ry'],ethr_Ry=s['ethr_Ry'],charge_change=charge_change,orbital_density_change_relative_F=orbital_change))
  previous=step
 schema=root/'out/r07m4.save/data-file-schema.xml';xml=ET.parse(schema).getroot()
 for e in xml.iter():e.tag=e.tag.split('}')[-1]
 def value(path):
  e=xml.find(path);return None if e is None else e.text.strip()
 achieved=value('./output/convergence_info/scf_conv/convergence_achieved')
 native=(achieved=='true' and len(steps)>=2 and steps[-1]['scalar']['values']['dexx_Ry']<1e-10 and 'EXX self-consistency reached' in text and r['native_execution_complete'])
 return dict(actual_native_full_SCF=True,native_complete_execution=r['native_execution_complete'],converged_HSE=native,xml_inner_convergence=achieved,soft_stop='Maximum CPU time exceeded' in text or 'Maximum CPU time' in text or 'Maximum time' in text or 'stopping ...' in text or 'Calculation (EXX) stopped' in text,outer_trajectory=outer,inner_estimated_SCF_accuracy_Ry=[float(v.replace('D','E')) for v in re.findall(r'estimated scf accuracy\s*<\s*([0-9.EeDd+-]+)\s*Ry',text)],final_schema_sha256=owner.sha(schema),final_XML_energy_Hartree=value('./output/total_energy/etot') if r['native_execution_complete'] else None,aborted_schema_not_a_final_SCF_result=not r['native_execution_complete'],resource=r,final_readback=json.loads((root/'FINAL_CERTIFICATE.json').read_text()) if (root/'FINAL_CERTIFICATE.json').exists() else None,native_restart_unqualified=True,physical_xc=False)

def main():
 outputs={}
 for mode in ['control','stream']:
  root=owner.PRIVATE/mode
  if (root/'RESULT.json').exists():outputs[mode]=summarize(root)
 common=[]
 if set(outputs)=={'control','stream'}:
  ks={d['outer_step'] for d in outputs['control']['outer_trajectory']}&{d['outer_step'] for d in outputs['stream']['outer_trajectory']}
  for k in sorted(ks):
   try:common.append(observables.step_certificate(owner.PRIVATE/'stream',k,1,owner.PRIVATE/'control'))
   except observables.Refusal as e:
    common.append(dict(step=k,failed=True,reason=str(e),diagnostic_states=observables.pair_states(observables.paths(owner.PRIVATE/'control',k,1),observables.paths(owner.PRIVATE/'stream',k,1),enforce=False),control_scalar=observables.scalars(owner.PRIVATE/'control',k,1),stream_scalar=observables.scalars(owner.PRIVATE/'stream',k,1)))
 result=dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),members=outputs,common_steps=[v['step'] for v in common],paired_common_completed_outer=comparison_summary(common),both_full_HSE_converged=bool(len(outputs)==2 and all(v['converged_HSE'] for v in outputs.values())),whole_SCF_memory_improvement_claim=False,preregistered_tolerances=observables.TOL,prospective_preregistration_sha256=owner.sha(HERE/'preregistration.md'),historical_step4_failure_unchanged=True,physical_xc=False)
 (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:{'outer_count':len(v['outer_trajectory']),'converged':v['converged_HSE'],'last':v['outer_trajectory'][-1] if v['outer_trajectory'] else None,'elapsed':v['resource']['elapsed_seconds'],'RSS':v['resource']['peak_family_RSS_bytes']} for k,v in outputs.items()},indent=2));return result

def comparison_summary(common):
 if not common:return dict(passed=False,reason='no corresponding completed outer steps')
 passed=[v for v in common if not v.get('failed')];failed=[v for v in common if v.get('failed')]
 energies={n:max(v['paired_scalar_difference'][n] for v in passed) for n in passed[0]['paired_scalar_difference']}
 states={n:max(v['paired_states'][str(k)][n] for v in passed for k in [1,2,3]) for n in ['eigenvalue_Ry','occupation','orbital_density_relative_F','rhoR','rhoG','vrs']}
 return dict(passed=not failed,passed_common_steps=[v['step'] for v in passed],failed_common_steps=failed,maximum_scalar_differences_on_passed_steps=energies,maximum_state_differences=states,compared_native_step_records=common)
if __name__=='__main__':main()
