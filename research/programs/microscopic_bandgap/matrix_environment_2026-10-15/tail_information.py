"""Preconditioned derivative bounds and explicit positive-measure completions."""
from pathlib import Path
import json,hashlib
import numpy as np
from analyze import compute,HERE,OLD


def main():
    if (HERE/'tail_information.json').exists():raise FileExistsError('retain first input audit')
    f=np.load(OLD/'complex_overlaps.npz');old=json.loads((OLD/'numerical_result.json').read_text());rho=max(old['IEEE_weight_budgets'].values());z=.05j;data={}
    for m in ['unshared','shared']:
        v=np.loadtxt(OLD/(m+'_Gamma6_spectrum.csv'),delimiter=',',skiprows=1);e=v[:,2];C=np.vstack((f[m+'_Gamma6'],f[m+'_Gamma8']));G=(C/(z-e))@C.conj().T;gp=-(C/(z-e)**2)@C.conj().T;A=np.linalg.inv(G);S=np.eye(6)-C@C.conj().T;S=(S+S.conj().T)/2;assert min(np.linalg.eigvalsh(S))>0
        data[m]=dict(G=G,gp=gp,A=A,S=S,r=float(np.linalg.norm(S,2))+6*rho,c=float(np.linalg.norm(A@gp@A,2)),a=float(np.linalg.norm(A,2)),highest_retained_relative_E_eV=float(e[-1]))
    def bound(L=None):
        d=z.imag if L is None else abs(z-complex(L,0));total=0.
        for v in data.values():
            delta=v['r']/d;delta1=v['r']/d**2;a=v['a'];margin=1-a*delta
            if margin<=0:return None
            b=a/margin;total+=delta*(a+b)*v['c']/margin+b*b*delta1
        return total
    primary=json.loads((HERE/'derivative_result.json').read_text())['primary'];target=abs(primary['trace_ordering_derivative_contrast'])
    lo=0.;hi=10.
    for _ in range(80):
        mid=(lo+hi)/2
        if 2*bound(mid)>target:lo=mid
        else:hi=mid
    threshold=(lo+hi)/2
    def completed(m,E):
        v=data[m];g=v['G']+v['S']/(z-E);gp=v['gp']-v['S']/(z-E)**2;A=np.linalg.inv(g);H=z*np.eye(6)-A;hp=np.eye(6)+A@gp@A
        assert min(np.linalg.eigvalsh(-(H-H.conj().T)/(2j)))>-1e-10
        return H,hp
    completions=[]
    for es,eu in [(100.,100.),(0.,100.),(100.,0.)]:
        hs,ds=completed('shared',es);hu,du=completed('unshared',eu);D=ds-du;H=hs-hu
        completions.append(dict(shared_omitted_energy_eV=es,unshared_omitted_energy_eV=eu,trace_derivative_delta=float((np.trace(D[:2,:2])/2-np.trace(D[2:,2:])/4).real),trace_value_delta_eV=float((np.trace(H[:2,:2])/2-np.trace(H[2:,2:])/4).real),completion_positive_and_normalized=True,not_permitted_if_exact_lowest352_ordering_assumed=(es<data['shared']['highest_retained_relative_E_eV'] or eu<data['unshared']['highest_retained_relative_E_eV'])))
    assert min(x['trace_derivative_delta'] for x in completions)<0<max(x['trace_derivative_delta'] for x in completions)
    rawthreshold=min(v['highest_retained_relative_E_eV'] for v in data.values())
    result=dict(status='CALCULATED minimum tail-support information under explicit assumptions',primary_trace_derivative_delta=primary['trace_ordering_derivative_contrast'],original_unstructured_matrix_derivative_bound=primary['fixed_frame_derivative_error_bound'],improved_gapfree_matrix_derivative_bound=bound(),trace_derivative_gapfree_interval=[primary['trace_ordering_derivative_contrast']-2*bound(),primary['trace_ordering_derivative_contrast']+2*bound()],sufficient_common_omitted_support_lower_threshold_eV=threshold,threshold_is_measured_error_budget_NOT_material_fit=True,highest_printed_retained_energies_eV={m:v['highest_retained_relative_E_eV'] for m,v in data.items()},conditional_bound_IF_lowest_band_order_certified=bound(rawthreshold),exact_band_order_or_omitted_support_certificate_available=False,positive_measure_completion_counterexamples=completions,physical_Coulomb_Hamiltonian_nonuniqueness_NOT_claimed=True,no_new_native_job=True,no_material_A_or_xc=True,source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'analyze.py',HERE/'derivative_result.json',OLD/'complex_overlaps.npz']})
    (HERE/'tail_information.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
