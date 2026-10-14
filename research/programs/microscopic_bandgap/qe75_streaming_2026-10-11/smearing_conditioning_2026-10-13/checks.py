"""Focused independent analytic checks, no MPI/QE job."""
import hashlib,json,math,sys,importlib.util
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));import conditioning as c,observables as new,audit
spec=importlib.util.spec_from_file_location('historical_observables',HERE.parent/'full_scf_2026-10-13/observables.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
ROOT=audit.ROOT/'full_scf_pair_v2_20261013'
y=(1-math.sqrt(5))/(2*math.sqrt(2));L=math.exp(-y*y)*(1-math.sqrt(2)*y)/math.sqrt(math.pi)
assert abs(L-c.L)<2e-16
# Stable QR identity independently compared with actual small gamma difference;
# include deliberately nonorthonormal columns to reject an implicit ideal Gram.
rng=np.random.default_rng(7525);A=rng.normal(size=(14,4))+1j*rng.normal(size=(14,4));B=A+1e-5*(rng.normal(size=(14,4))+1j*rng.normal(size=(14,4)));fa=np.array([1,.9,.5,.1]);fb=fa+np.array([0,1e-5,-1e-5,0])
actual=np.linalg.norm((A*fa)@A.conj().T-(B*fb)@B.conj().T)/max(np.linalg.norm(fa),1.)
qr=c.density(A,B,fa,fb);assert abs(qr-actual)<2e-13
phase=np.exp(1j*np.array([.2,.9,1.2,-.5]));assert c.density(A,A*phase,fa,fa)<1e-13
try:old.step_certificate(ROOT/'stream',4,1,ROOT/'control')
except old.Refusal as e:historical=str(e)
else:raise AssertionError('historical FAIL altered')
records=json.loads((HERE/'retained_audit.json').read_text())['records'];pointwise=[]
for row in records:
 for mode in ['control','stream']:
  d=old.decode(old.paths(ROOT/mode,row['step'],1)[(0,1)])
  pointwise.append(dict(step=row['step'],mode=mode,independent_decimal_max_error=c.evaluation_check(row['member'][mode]['mu_Ry'],d['et'],d['wg']/audit.WK)))
# Nonmonotonic cold occupation: same target on ascending/descending branches.
def f(x):return .5*math.erf(x-1/math.sqrt(2))+math.exp(-(x-1/math.sqrt(2))**2)/math.sqrt(2*math.pi)+.5
def bisect(a,b,target):
 sa=f(a)-target
 for _ in range(80):
  mid=(a+b)/2
  if sa*(f(mid)-target)<=0:b=mid
  else:a=mid;sa=f(a)-target
 return (a+b)/2
r1=bisect(.7,math.sqrt(2),1.04);r2=bisect(math.sqrt(2),5,1.04)
assert abs(f(r1)-1.04)<1e-15 and abs(f(r2)-1.04)<1e-15 and r2>r1
result=dict(passed=True,L=L,eigen_mu_budget_Ry=c.EPS_BUDGET,prospective_worst_occupation_upper=2*c.L/c.SIGMA*c.EPS_BUDGET+2*c.EVAL,small_density_direct=actual,small_density_QR=qr,cold_nonunique_counterexample=dict(target=1.04,x1=r1,x2=r2),pointwise_decimal=pointwise,historical_step4_still_refused=historical,not_native_MPI=True)
(HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
# Serial library was extended only with at_mu: update before frozen launch pins.
p=HERE/'build_results.json';b=json.loads(p.read_text());lib=audit.PRIVATE/'replay.so';b['source_and_exchange_archive_pins'][str(lib)]=hashlib.sha256(lib.read_bytes()).hexdigest();p.write_text(json.dumps(b,indent=2)+'\n')
