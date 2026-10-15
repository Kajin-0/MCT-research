"""Exact finite Bernoulli enumeration and causal missing-environment example."""
from pathlib import Path
import itertools,json,math


def main():
    rows=[]
    for x in [.125,.17,.25]:
        P=[math.comb(4,n)*x**n*(1-x)**(4-n) for n in range(5)]
        h=[n*(n-1)*(4-n) for n in range(5)]
        j=[n*(n-1)*(n-2)*(4-n) for n in range(5)]
        assert all(h[n]==j[n]==0 for n in [0,1,4])
        assert abs(sum(p*v for p,v in zip(P,h))-24*x*x*(1-x))<1e-14
        assert abs(sum(p*v for p,v in zip(P,j))-24*x**3*(1-x))<1e-14
        # Independent enumeration rather than reuse of the binomial polynomial.
        probs=[0.]*5
        for bits in itertools.product([0,1],repeat=4):
            prob=math.prod(x if b else 1-x for b in bits);probs[sum(bits)]+=prob
        assert max(abs(a-b) for a,b in zip(P,probs))<1e-15
        z=.05j;E=[-.3]*5
        g0=sum(P[n]/(z-E[n]) for n in range(5))
        g1=sum(P[n]/(z-E[n]-(.1 if n==2 else 0)) for n in range(5))
        assert g0.imag<0 and g1.imag<0 and abs(g0-g1)>0
        rows.append(dict(x=x,P2=P[2],P3=P[3],P2_over_P3=P[2]/P[3],causal_g_change_abs=abs(g1-g0),inverse_real_change_eV=(1/g1-1/g0).real))
    out=dict(status='exact algebra/enumeration plus synthetic causal counterexample, not material validation',unseen_environment_matrix_dimension=2,rows=rows,physical_xc=None)
    (Path(__file__).parent/'checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
