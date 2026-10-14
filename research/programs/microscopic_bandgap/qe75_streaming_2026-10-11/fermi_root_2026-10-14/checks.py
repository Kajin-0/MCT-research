"""Focused independent qualification, actual spectra + one ambiguous causal scalar fixture."""
import ctypes,json,math,hashlib
from pathlib import Path
from decimal import Decimal,localcontext
import numpy as np
import qualify as q
HERE=Path(__file__).resolve().parent;ptr=ctypes.POINTER(ctypes.c_double);ip=ctypes.POINTER(ctypes.c_int)
lib=ctypes.CDLL(str(q.PRIVATE/'root.so'));lib.qualify.argtypes=[ptr,ptr,ptr,ptr,ip]
def run(et):
 et=np.array(et,order='F');m=ctypes.c_double();w=np.empty((48,3),order='F');c=np.empty(10);code=ctypes.c_int()
 lib.qualify(et.ctypes.data_as(ptr),ctypes.byref(m),w.ctypes.data_as(ptr),c.ctypes.data_as(ptr),ctypes.byref(code));return code.value,m.value,w,c

def independent_derivative(mu,et):
 with localcontext() as ctx:
  ctx.prec=100;pi=Decimal(q.cond.PI);sigma=Decimal.from_float(.001);two=Decimal(2);total=Decimal(0)
  for k,w in enumerate([.125,.5,.375]):
   for e in et[:,k]:
    y=(Decimal.from_float(float(mu))-Decimal.from_float(float(e)))/sigma-1/two.sqrt()
    if abs(y)>12:continue # bounded negligible ideal tail, not clipped w0gauss extrapolation
    total+=Decimal.from_float(w)*(-y*y).exp()*(1-two.sqrt()*y)/pi.sqrt()/sigma
  return float(total)
def charge(mu,et):
 f=np.array([[q.cond.high_precision_cold(mu,e) for e in row] for row in et]);return float((f*np.array([.125,.5,.375])).sum()-36)

def main():
 data=np.load(HERE/'retained_inputs.npz',allow_pickle=False);rows=json.loads((HERE/'root_qualification.json').read_text())['records'];out=[]
 for row in rows:
  et=data['et_'+str(row['id'])];c=row['certificate'];lo,hi=c[0],c[1]
  # Independent bisection uses high-precision analytic f, not sumkg or candidate control flow.
  for i in range(70):
   mid=lo+(hi-lo)/2;f=charge(mid,et)
   if f>0:hi=mid
   else:lo=mid
  independent=(lo+hi)/2;bound=1.1e-10/c[4]+4*np.spacing(abs(row['mu_Ry']))
  assert abs(independent-row['mu_Ry'])<=bound
  derivatives=[independent_derivative(x,et) for x in np.linspace(c[2],c[3],5)]
  assert min(derivatives)>=c[4] and max(derivatives)<=c[5]
  out.append(dict(id=row['id'],independent_root_Ry=independent,root_delta_Ry=abs(independent-row['mu_Ry']),certified_error_from_residual_over_slope_Ry=bound,independent_derivative_min=min(derivatives),independent_derivative_max=max(derivatives)))
 ambiguous=np.empty((48,3));ambiguous[:35]=0;ambiguous[35]=.004;ambiguous[36:]=.02
 code,mu,w,c=run(ambiguous);assert code==6,code
 nan=data['et_0'].copy();nan[0,0]=np.nan;assert run(nan)[0]==1
 outside=data['et_0'].copy();outside[0,0]=-101.;assert run(outside)[0]==1
 ref=data['et_10'];code,m,w,c=run(ref);code2,m2,w2,c2=run(ref+1.)
 assert code==code2==0 and abs(m2-m-1)<3e-12 and np.max(abs(w2-w))<3e-11
 result=dict(passed=True,all_retained_independent_checks=out,multiple_real_roots_refused_code=6,nonfinite_refused_code=1,energy_reference_shift_Ry=1.,reference_mu_error=float(abs(m2-m-1)),reference_wg_max_delta=float(abs(w2-w).max()),oracle_bounds_are_explicit_assumption_not_universal_libm_proof=True,no_MPI_QE=True)
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'retained':len(out),'ambiguous_refusal':6,'max_independent_root_delta_Ry':max(r['root_delta_Ry'] for r in out),'no_MPI':True},indent=2))
if __name__=='__main__':main()
