"""Analytic causal energy derivatives with uniform omitted-measure budgets."""
from pathlib import Path
import json,hashlib
import numpy as np
from analyze import compute,OLD,HERE


def evaluate(C,e,z,rho):
    base=compute(C,e,z,rho);G=base['G'];inv=np.linalg.inv(G);gp=-(C/(z-e)**2)@C.conj().T;hp=np.eye(6)+inv@gp@inv;a=float(np.linalg.norm(inv,2));b=a/base['margin'];err=base['deltaH']*float(np.linalg.norm(gp,2))*(a+b)+b*b*base['deltaG']/z.imag
    return hp,err


def main():
    if (HERE/'derivative_result.json').exists():raise FileExistsError('retain first derivative evidence')
    a=json.loads((OLD/'numerical_result.json').read_text());f=np.load(OLD/'complex_overlaps.npz');rho=max(a['IEEE_weight_budgets'].values());data={};rows=[];fd=[]
    for m in ['unshared','shared']:
        v=np.loadtxt(OLD/(m+'_Gamma6_spectrum.csv'),delimiter=',',skiprows=1);data[m]=(np.vstack((f[m+'_Gamma6'],f[m+'_Gamma8'])),v[:,2])
    for t in [-.1,0.,.1]:
        for eta in [.025,.05,.1]:
            z=t+1j*eta;b={m:evaluate(C,e,z,rho) for m,(C,e) in data.items()};d=b['shared'][0]-b['unshared'][0];err=sum(v[1] for v in b.values());ordering=float((np.trace(d[:2,:2])/2-np.trace(d[2:,2:])/4).real)
            rows.append(dict(t_from_each_own_Fermi_eV=t,eta_eV=eta,matrix_derivative_contrast_norm=float(np.linalg.norm(d,2)),fixed_frame_derivative_error_bound=err,trace_ordering_derivative_contrast=ordering,trace_derivative_error_bound=2*err,trace_derivative_interval=[ordering-2*err,ordering+2*err],not_impurity_Tprime_or_alloy_A=True))
            if t==0 and eta==.05:
                for m,(C,e) in data.items():
                    h=1e-6;central=(compute(C,e,z+h,rho)['H']-compute(C,e,z-h,rho)['H'])/(2*h);fd.append(float(np.linalg.norm(central-b[m][0],2)))
    assert max(fd)<1e-7
    result=dict(status='CALCULATED derivatives of retained projected kernels only',rows=rows,primary=next(v for v in rows if v['t_from_each_own_Fermi_eV']==0 and v['eta_eV']==.05),analytic_central_difference_errors=fd,no_omitted_energy_support_certificate=True,no_material_A_prediction=True,physical_xc=None,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'analyze.py',HERE/'derivative_protocol.md',OLD/'numerical_result.json',OLD/'complex_overlaps.npz']})
    (HERE/'derivative_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(primary=result['primary'],central_errors=fd),indent=2))


if __name__=='__main__':main()
