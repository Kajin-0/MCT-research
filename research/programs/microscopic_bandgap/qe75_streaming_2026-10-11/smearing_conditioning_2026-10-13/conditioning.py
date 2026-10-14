"""Analytic conditioning plus bounded pointwise independent Decimal check."""
import math
from decimal import Decimal,localcontext
import numpy as np
L=.7541710171545021; SIGMA=.001; EVAL=64*np.finfo(float).eps
ENERGY=1e-8; EPS_BUDGET=(ENERGY/2)/(48*1.1)
PI='3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647'

def high_precision_cold(mu,e):
 with localcontext() as c:
  c.prec=120
  one=Decimal(1);two=Decimal(2);pi=Decimal(PI)
  x=(Decimal.from_float(float(mu))-Decimal.from_float(float(e)))/Decimal.from_float(SIGMA)
  y=x-one/two.sqrt();a=abs(y)
  # erf tail <= exp(-a*a)/(a*sqrt(pi)), <=1e-64 at |y|>=12.
  if a>=12:erf=one if y>0 else -one
  else:
   term=y;total=y;n=0
   while True:
    term=-term*y*y*Decimal(2*n+1)/Decimal((n+1)*(2*n+3));n+=1
    total+=term
    if n>y*y and abs(term)<Decimal('1e-75'):break
    if n>2000:raise ValueError('bounded Decimal erf series')
   erf=two/pi.sqrt()*total
  value=erf/two+(-min(Decimal(200),y*y)).exp()/(two*pi).sqrt()+one/two
  return float(value)

def evaluation_check(mu,et,f):
 expected=np.array([[high_precision_cold(mu,e) for e in row] for row in et])
 error=float(np.max(abs(expected-f)))
 if error>EVAL:raise ValueError('independent high-precision cold evaluation allowance')
 return error

def density(A,B,fa,fb):
 Q,RA=np.linalg.qr(A,mode='reduced')
 S=Q.conj().T@B;R=B-Q@S;M=R.conj().T@R;C=S*fb[None,:]
 D=(RA*fa[None,:])@RA.conj().T-(S*fb[None,:])@S.conj().T
 norm2=np.vdot(D,D).real+2*np.trace(C@M@C.conj().T).real+np.sum(fb[:,None]*fb[None,:]*abs(M)**2)
 return float(np.sqrt(max(0.,norm2))/max(np.linalg.norm(fa),1.))
