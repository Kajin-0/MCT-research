"""One finite analytically directed complement test, never a material model."""
import json
import numpy as np
from scipy.linalg import eig
from analyze import HERE,SOURCE,PRIVATE,RYEV,norm

def main():
    f=np.load(PRIVATE/'trial.npz');V=f['Q'];P=f['P'];x=np.load(PRIVATE/'full_actions.npz');A=(x['H']+x['H'].conj().T)/2;R=x['HV']-V@A;R-=V@(V.conj().T@R);W=R.conj().T@R;B=V.conj().T@P
    s=json.loads((SOURCE/'native_science.json').read_text());mu=s['projected_FD_mu_Ry'];values,U=eig(W,A-mu*np.eye(304));candidates=[]
    for j,v in enumerate(values):
        if not np.isfinite(v) or abs(v.imag)>1e-6 or abs(mu+v.real)>100:continue
        u=U[:,j];weight=float(np.linalg.norm(B.conj().T@u)**2/np.linalg.norm(u)**2)
        candidates.append((weight,float(mu+v.real)))
    unique=[]
    for weight,c in sorted(candidates,reverse=True):
        if all(abs(c-a[1])>1e-5 for a in unique):unique.append((weight,c))
        if len(unique)==6:break
    eta=.05/RYEV;z=mu+1j*eta;rows=[];Anorm=norm(A);Rnorm=norm(R)
    for weight,c0 in unique:
        for dc in [-eta,0.,eta]:
            c=c0+dc;g=B.conj().T@np.linalg.solve(z*np.eye(304)-A-W/(z-c),B);g6=np.trace(g[:2,:2])/2;g8=np.trace(g[2:,2:])/4;ordering=float((1/g8-1/g6).real*RYEV)
            rows.append(dict(c_Ry=c,root_Ry=c0,offset_Ry=dc,original_probe_weight=weight,ordering_eV=ordering,causal_min_eigen_minus_Im_g=float(min(np.linalg.eigvalsh(-(g-g.conj().T)/(2j)))),norm_upper_Ry=max(Anorm,abs(c))+Rnorm))
    assert len(rows)<=18 and min(x['causal_min_eigen_minus_Im_g'] for x in rows)>0
    assert max(x['norm_upper_Ry'] for x in rows)<s['H_operator_norm_upper_Ry']
    result=dict(status='CALCULATED_FINITE_COMPLEMENT_FALSIFICATION_ONLY',eta_eV=.05,selected_real_roots=unique,rows=rows,range_eV=[min(x['ordering_eV'] for x in rows),max(x['ordering_eV'] for x in rows)],opposite_ordering_found=any(x['ordering_eV']>0 for x in rows),not_a_material_HSE_alternative=True,all304_basis_A_and_R_preserved=True,independent_12_physical_probe_actions_NOT_imposed=True)
    (HERE/'directed_completion_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
if __name__=='__main__':main()
