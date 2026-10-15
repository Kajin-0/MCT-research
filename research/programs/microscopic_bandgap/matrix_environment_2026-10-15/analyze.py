"""Full causal matrix contrasts at nine fixed probes; no native execution."""
from pathlib import Path
import hashlib,json,sys,itertools
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;OLD=BASE/'pair_environment_2026-10-15'


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def compute(C,e,z,rho):
    G=(C/(z-e))@C.conj().T;R=np.eye(6)-C@C.conj().T;ev=np.linalg.eigvalsh((R+R.conj().T)/2);assert min(ev)>-6*rho
    delta=(max(0.,float(max(ev)))+6*rho)/z.imag;inv=np.linalg.inv(G);a=float(np.linalg.norm(inv,2));margin=1-a*delta
    H=z*np.eye(6)-inv;damp=-(H-H.conj().T)/(2j);assert min(np.linalg.eigvalsh(damp))>-1e-10
    err=a*a*delta/margin if margin>0 else None
    return dict(G=G,H=H,deltaG=delta,deltaH=err,margin=margin,damping_min=float(min(np.linalg.eigvalsh(damp))))


def main():
    if (HERE/'result.json').exists():raise FileExistsError('preserve first matrix audit')
    old=json.loads((OLD/'numerical_result.json').read_text());f=np.load(OLD/'complex_overlaps.npz');data={};rho=max(old['IEEE_weight_budgets'].values());rows=[];arrays={};checks=[]
    for m in ['unshared','shared']:
        v=np.loadtxt(OLD/(m+'_Gamma6_spectrum.csv'),delimiter=',',skiprows=1);data[m]=(np.vstack((f[m+'_Gamma6'],f[m+'_Gamma8'])),v[:,2])
    U=np.eye(6,dtype=complex);U[:2,:2]=np.array([[1,1j],[1j,1]])/np.sqrt(2);U[2:,2:]=np.fft.fft(np.eye(4))/2
    for t in [-.1,0.,.1]:
        for eta in [.025,.05,.1]:
            z=t+1j*eta;v={m:compute(C,e,z,rho) for m,(C,e) in data.items()};dG=v['shared']['G']-v['unshared']['G'];dH=v['shared']['H']-v['unshared']['H'];real=(dH+dH.conj().T)/2
            identity=v['shared']['H']-v['unshared']['H']-np.linalg.inv(v['shared']['G'])@dG@np.linalg.inv(v['unshared']['G']);checks.append(float(np.linalg.norm(identity,2)))
            alt={m:compute(U@C,e,z,rho) for m,(C,e) in data.items()};checks.append(float(np.linalg.norm(alt['shared']['H']-alt['unshared']['H']-U@dH@U.conj().T,2)))
            tr6=np.trace(dH[:2,:2])/2;tr8=np.trace(dH[2:,2:])/4;err=None if any(x['deltaH'] is None for x in v.values()) else sum(x['deltaH'] for x in v.values());ordering=float((tr6-tr8).real)
            row=dict(t_from_each_own_Fermi_eV=t,eta_eV=eta,deltaG_norm_per_eV=float(np.linalg.norm(dG,2)),deltaG_fixed_frame_error_per_eV=sum(x['deltaG'] for x in v.values()),deltaH_norm_eV=float(np.linalg.norm(dH,2)),deltaH_fixed_frame_error_eV=err,trace_ordering_delta_eV=ordering,mass_delta_eV=ordering/2,common_delta_eV=float(((tr6+tr8)/2).real),ordering_error_bound_eV=None if err is None else 2*err,ordering_interval_eV=None if err is None else [ordering-2*err,ordering+2*err],deltaH_offblock_norm_eV=float(np.linalg.norm(dH[:2,2:],2)),Gamma8_Hermitian_anisotropy_eV=float(np.linalg.norm(real[2:,2:]-np.trace(real[2:,2:])/4*np.eye(4),2)),Hermitian_deltaH_eigenvalues_eV=np.linalg.eigvalsh(real).tolist(),member_inversion_margins={m:a['margin'] for m,a in v.items()},member_min_causal_damping_eV={m:a['damping_min'] for m,a in v.items()},physical_frame_fixed=True,nearby_projector_transport_error_included=False)
            rows.append(row);key=f't{t}_eta{eta}';arrays[key+'_deltaG']=dG;arrays[key+'_deltaH']=dH
    primary=next(v for v in rows if v['t_from_each_own_Fermi_eV']==0 and v['eta_eV']==.05);oldvalue=next(v for v in old['matrix_causal_rows'] if v['eta_eV']==.05)['delta_eV'];assert abs(primary['trace_ordering_delta_eV']-oldvalue)<1e-12 and max(checks)<1e-11
    # Exhaustive triplet incidence, same actual cell and cation labels.
    geo=json.loads((OLD/'geometry_result.json').read_text());shells=geo['Te_nn_cation_indices'];configs=[]
    for cd in itertools.combinations(range(8),3):
        ns=[sum(i in cd for i in shell) for shell in shells];configs.append(dict(Cd_indices_0based=list(cd),Te_N_counts=ns,histogram={str(n):ns.count(n) for n in range(5)}))
    bearing=[v for v in configs if v['histogram']['3']>0];hist={}
    for c in configs:
        key=tuple(c['histogram'][str(n)] for n in range(5));hist[str(key)]=hist.get(str(key),0)+1
    chosen=next(v for v in configs if v['Cd_indices_0based']==[0,1,2]);assert chosen['histogram']['3']>0
    Q=np.array(geo['cell_repeat']);xyz=np.array(geo['cation_fractional']);pos=np.r_[xyz,xyz+.125];syms=['Cd' if i in [0,1,2] else 'Hg' for i in range(8)]+['Te']*8;keys=lambda x:{(s,tuple(np.rint(y*8).astype(int)%8)) for s,y in zip(syms,x)};ops=[]
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([-1,1],repeat=3):
            R=np.eye(3)[list(perm)]*np.array(signs)[:,None];S=np.linalg.inv(Q.T)@R@Q.T
            good=[shift.tolist() for shift in xyz if keys(pos@S.T+shift)==keys(pos)]
            if good:ops.append(dict(cartesian=R.astype(int).tolist(),translations=good))
    chosen=dict(chosen,point_group_order=len(ops),operations=ops,x=.375,native_not_launched=True)
    np.savez(HERE/'matrix_differences.npz',**arrays)
    result=dict(status='CALCULATED retained native matrix contrasts and exhaustive geometry; no newQE',rows=rows,primary=primary,maximum_inverse_identity_and_blockunitary_error=float(max(checks)),triplet_total=len(configs),N3bearing_count=len(bearing),triplet_histogram_multiplicities=hist,chosen_N3_geometry=chosen,physical_xc=None,not_random_alloy_self_energy=True,source_sha256={str(p):sha(p) for p in [Path(__file__),HERE/'protocol.md',OLD/'numerical_result.json',OLD/'complex_overlaps.npz',OLD/'geometry_result.json']})
    (HERE/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(dict(primary=primary,N3bearing_count=len(bearing),histograms=hist,N3chosen={k:v for k,v in chosen.items() if k!='operations'},max_check_error=max(checks)),indent=2))


if __name__=='__main__':main()
