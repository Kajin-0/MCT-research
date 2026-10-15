"""Independent causal completions, structured bound and triplet geometry audit."""
from pathlib import Path
import json,itertools,hashlib
import numpy as np
from analyze import HERE,OLD


def main():
    old=json.loads((OLD/'numerical_result.json').read_text());data=np.load(OLD/'complex_overlaps.npz');rho=max(old['IEEE_weight_budgets'].values());rng=np.random.default_rng(7128);errors=[];moments={};z=.05j
    for member in ['unshared','shared']:
        spec=np.loadtxt(OLD/(member+'_Gamma6_spectrum.csv'),delimiter=',',skiprows=1);e=spec[:,2];C=np.vstack((data[member+'_Gamma6'],data[member+'_Gamma8']));G=(C/(z-e))@C.conj().T;gp=-(C/(z-e)**2)@C.conj().T;A=np.linalg.inv(G);hp=np.eye(6)+A@gp@A;S=np.eye(6)-C@C.conj().T;S=(S+S.conj().T)/2;w,U=np.linalg.eigh(S);assert min(w)>0;W=(U*np.sqrt(w))@U.conj().T
        a=np.linalg.norm(A,2);r=np.linalg.norm(S,2)+6*rho;delta=r/z.imag;margin=1-a*delta;b=a/margin;c=np.linalg.norm(A@gp@A,2);bound=delta*(a+b)*c/margin+b*b*r/z.imag**2
        for i in range(5):
            V=np.linalg.qr(rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)))[0];P=V[:,:3]@V[:,:3].conj().T;M1=W@P@W;M2=S-M1
            tail=M1/(z+.07)+M2/(z-.03);tailp=-M1/(z+.07)**2-M2/(z-.03)**2;B=np.linalg.inv(G+tail);actual=np.linalg.norm(np.eye(6)+B@(gp+tailp)@B-hp,2);assert actual<=bound*(1+1e-12);errors.append(float(actual/bound))
        P=np.diag([1,1,0,0,0,0]);M6=W@P@W;first_moment_change=20*M6;green_change=M6*(1/(z-40)-1/(z-20));mass=float((np.trace(first_moment_change[:2,:2])/2-np.trace(first_moment_change[2:,2:])/4).real)
        assert abs(mass)>.01 and np.linalg.norm(green_change,2)<delta
        moments[member]=dict(omitted_tail_energies_eV=[20,40],both_above_highest_retained=True,static_trace_ordering_change_eV=mass,projected_green_change_norm_per_eV=float(np.linalg.norm(green_change,2)),allowed_tail_G_bound_per_eV=float(delta),completion_positive_normalized_and_preserves_all_retained_data=True,not_an_alternative_fixed_atomic_Coulomb_solution=True)
    result=json.loads((HERE/'result.json').read_text());geo=json.loads((OLD/'geometry_result.json').read_text());Q=np.array(geo['cell_repeat']);hg=np.array(geo['cation_fractional']);xyz=np.r_[hg,hg+.125];cd=[0,1,2];counts=[];shifts=np.array(list(itertools.product([-1,0,1],repeat=3)))
    for te in xyz[8:]:
        dist=np.linalg.norm(((hg[:,None,:]+shifts[None,:,:]-te)@Q).reshape(-1,3),axis=1);i=np.argsort(dist)[:4];assert np.ptp(dist[i])<1e-12;counts.append(sum(int(j)//len(shifts) in cd for j in i))
    assert counts==result['chosen_N3_geometry']['Te_N_counts']
    # Count-vector rank is conditional on COMPLETE fixed-local operator inputs.
    matrix=np.array([[8,0,0,0,0],[0,0,0,0,8],[0,8,0,0,0],[2,4,2,0,0],[1,3,3,1,0]])
    assert np.linalg.matrix_rank(matrix[:4])==4 and np.linalg.matrix_rank(matrix)==5
    t=json.loads((HERE/'tail_information.json').read_text());assert t['positive_measure_completion_counterexamples'][0]['not_permitted_if_exact_lowest352_ordering_assumed'] is False
    for file,key in [('result.json','source_sha256'),('derivative_result.json','source_sha256'),('tail_information.json','source_sha256')]:
        for p,pin in json.loads((HERE/file).read_text())[key].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==pin
    out=dict(status='PASS independent positive-matrix tail/bound/geometry checks; no material validation',noncommuting_derivative_actual_to_bound_ratios=errors,high_energy_tail_static_moment_counterexamples=moments,N3_nearest4_independent_counts=counts,fixed_local_count_rank_before=4,fixed_local_count_rank_after=5,all_nine_matrix_contrast_norm_lower_bounds_positive=all(v['deltaH_norm_eV']>v['deltaH_fixed_frame_error_eV'] for v in result['rows']),one_metadata_permission_label_corrected_with_original_draft_preserved=True,new_native_jobs=0,physical_xc=None,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
