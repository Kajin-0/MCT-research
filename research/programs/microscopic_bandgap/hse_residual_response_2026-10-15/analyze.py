"""Same-state full-action a-posteriori causal response; no native execution."""
from pathlib import Path
import hashlib,json
import numpy as np
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'single_state304_2026-10-15'
PRIVATE=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8u_20261015')
RYEV=13.605693122994

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(A):return float(np.linalg.norm(A,2))
def tests():
    rng=np.random.default_rng(10415);v=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));H=(v+v.conj().T)/2;A=H[:4,:4];R=H[4:,:4];C=H[4:,4:];Q=np.eye(4)[:,:2];P=np.eye(8)[:,:2];H0=np.block([[A,np.zeros((4,4))],[np.zeros((4,4)),C]]);E=H-H0;errors=[];perturbed=[]
    for eta in [.001,.05,1.,2.]:
        z=.3+1j*eta;G=np.linalg.inv(z*np.eye(8)-H);G0=np.linalg.inv(z*np.eye(8)-H0);Z=np.linalg.solve(z*np.eye(4)-A,Q);Zb=np.linalg.solve(z.conjugate()*np.eye(4)-A,Q);L=R@Zb;W=R@Z
        delta=P.conj().T@(G-G0)@P;two=P.conj().T@G0@E@G@E@G0@P
        ident=norm(delta-two);assert ident<1e-10
        bound=norm(L)*norm(W)/eta;assert norm(delta)<=bound+1e-10
        alpha=16.2;shift=np.linalg.inv((z+alpha)*np.eye(8)-(H+alpha*np.eye(8)));assert norm(shift-G)<1e-10
        errors.append(dict(eta=eta,second_order_identity_error=ident,actual_error=norm(delta),bound=bound))
        # True H is unchanged; measured non-Hermitian action error is bounded.
        noise=(rng.normal(size=(8,4))+1j*rng.normal(size=(8,4)))*1e-5
        Y=H[:,:4]+noise;Am=(Y[:4]+Y[:4].conj().T)/2;Vm=np.eye(8)[:,:4]
        Rm=Y-Vm@Am;eps=norm(noise);za=np.linalg.solve(z*np.eye(4)-Am,Q);zb=np.linalg.solve(z.conjugate()*np.eye(4)-Am,Q)
        err=norm(P.conj().T@G@P-Q.conj().T@za)
        upper=eps*norm(zb)*norm(za)+(norm(Rm@zb)+eps*norm(zb))*(norm(Rm@za)+eps*norm(za))/eta
        assert err<=upper+1e-10
        perturbed.append(dict(eta=eta,actual_error=err,action_only_bound=upper,known_whole_query_error=eps))
    # Causality/zero coupling do NOT determine the complement occupation.
    # A single negative unmeasured level leaves every known HQ unchanged.
    A=np.diag([-.1,.1]);Q=np.eye(2)[:,:1];z=.1+.001j
    assert np.linalg.eigvalsh(-np.linalg.inv(z*np.eye(2)-A).imag).min()>0
    return dict(status='PASS',bath_tests=errors,action_error_tests=perturbed,gauge_shift_invariant=True,no_positive_complement_or_gap_used=True)

def main():
    check=tests();r=json.loads((SOURCE/'native_result.json').read_text());assert r['accepted']
    data=np.load(PRIVATE/'trial.npz');full=np.load(PRIVATE/'full_actions.npz');V=data['Q'];P=data['P'];A=(full['H']+full['H'].conj().T)/2;HV=full['HV'];R=HV-V@A;B=V.conj().T@P;Perr=norm(P-V@B);Pnorm=norm(P);C=np.load(PRIVATE.parent/'h8h_20261015/trial.npz')['Q'];C=V.conj().T@C;A152=C.conj().T@A@C;B152=C.conj().T@B
    science=json.loads((SOURCE/'native_science.json').read_text());mu=science['projected_FD_mu_Ry'];F=np.load(SOURCE/'native_matrices.npz')['FD_Q'];eig=np.linalg.eigvalsh(F@(R.conj().T@R)@F);commop=float(np.sqrt(max(eig)));M=science['H_operator_norm_upper_Ry'];inspace_comm=norm(A@F-F@A)
    # Conditional finite arithmetic allowance, fixed BEFORE evaluating rows:
    # 1e-6 Ry WHOLE query-action op error, 1e-11 frame/input vector error.
    # Not an independently established interval enclosure of native H.
    epsH=1e-6;epsP=1e-11;rows=[]
    for eta_eV in [.05,.10,.20,.50,1.,2.]:
        eta=eta_eV/RYEV;z=mu+1j*eta;Z=np.linalg.solve(z*np.eye(304)-A,B);Zb=np.linalg.solve(z.conjugate()*np.eye(304)-A,B);g=B.conj().T@Z
        g152=B152.conj().T@np.linalg.solve(z*np.eye(152)-A152,B152)
        d1=Pnorm*norm(R@Z)/eta;d2=norm(R@Zb)*norm(R@Z)/eta
        frame=(2*norm(B)*Perr+Perr**2)/eta
        arithmetic=(2*Pnorm*epsP+epsP**2)/eta
        variants=[]
        for sl in [slice(0,2),slice(2,6)]:
            b=B[:,sl];dim=b.shape[1];za=Z[:,sl];zb=Zb[:,sl];v=complex(np.trace(g[sl,sl])/dim);v152=complex(np.trace(g152[sl,sl])/dim)
            rz=norm(R@za);rb=norm(R@zb);nz=norm(za);nb=norm(zb)
            action_herm=norm(V.conj().T@HV-A)
            def budget(epsilon):
                eps=epsilon+action_herm
                return eps*nb*nz+(rb+eps*nb)*(rz+eps*nz)/eta+frame+arithmetic
            err=budget(epsH)
            margin=abs(v)-err;inv_error=err/(abs(v)*margin) if margin>0 else None
            a=-v.imag/np.pi;aerr=err/np.pi
            variants.append(dict(action_error_zero_g_bound_Ry_inverse=budget(0.),action_residual_factors=[rb,rz,nb,nz],g_Ry_inverse=[v.real,v.imag],g152_Ry_inverse=[v152.real,v152.imag],spectral_density_per_eV=a/RYEV,spectral_density_error_per_eV=aerr/RYEV,g_error_Ry_inverse=err,nonzero_margin_Ry_inverse=margin,inverse_error_eV=None if inv_error is None else inv_error*RYEV,K_eV=(z-1/v).real*RYEV))
        delta=variants[0]['K_eV']-variants[1]['K_eV'];invqualified=all(x['inverse_error_eV'] is not None for x in variants);errsum=sum(x['inverse_error_eV'] for x in variants) if invqualified else None
        # Maximum WHOLE action error for a conditional negative sign, no
        # choice of this threshold from the native error or retrospective gate.
        def sign_at(epsilon):
            ee=[]
            for v in variants:
                rb,rz,nb,nz=v['action_residual_factors'];ep=epsilon+action_herm
                er=ep*nb*nz+(rb+ep*nb)*(rz+ep*nz)/eta+frame+arithmetic
                amp=abs(complex(*v['g_Ry_inverse']));margin=amp-er
                if margin<=0:return False
                ee.append(er/(amp*margin)*RYEV)
            return abs(delta)>sum(ee)
        cap=None
        if sign_at(0):
            lo=0.;hi=1.
            for _ in range(10):
                if not sign_at(hi):break
                hi*=2
            assert not sign_at(hi)
            for _ in range(70):
                middle=(lo+hi)/2
                if sign_at(middle):lo=middle
                else:hi=middle
            cap=lo
        rows.append(dict(max_independent_query_action_error_for_sign_Ry=cap,eta_eV=eta_eV,energy_Ry=mu,irrep=variants,ordering_eV=delta,ordering_error_eV=errsum,ordering_interval_eV=None if errsum is None else [delta-errsum,delta+errsum],ordering_sign_conditional_on_action_error=bool(errsum is not None and abs(delta)>errsum),projected_G_omission_first_order_upper_Ry_inverse=d1,projected_G_omission_second_order_upper_Ry_inverse=d2,frame_error_Ry_inverse=frame,conditional_arithmetic_error_Ry_inverse=arithmetic,same_H152_304_G_difference_Ry_inverse=norm(g-g152),causal_min_eigen_minus_Im_g_Ry_inverse=float(min(np.linalg.eigvalsh(-(g-g.conj().T)/(2j))))))
    out=dict(status='CALCULATED_CONDITIONAL_FINITE_NATIVE_MODEL',source_native_sha256=sha(SOURCE/'native_result.json'),source_full_action_sha256=sha(PRIVATE/'full_actions.npz'),original_physical_P_frame_projection_error_op=Perr,P_Gram_defect=norm(P.conj().T@P-np.eye(6)),fullspace_FD304_commutator_op_lower_Ry=commop-inspace_comm,FD304_inspace_commutator_roundoff_Ry=inspace_comm,fullspace_FD304_error_op_lower=(commop-inspace_comm-2*epsH)/(2*M),assumed_WHOLE_query_action_error_op_Ry=epsH,assumed_frame_input_error_op=epsP,arithmetic_allowances_NOT_interval_native_proven=True,fullspace_FD1e8_stationarity_EXCLUDED_conditionally=bool((commop-inspace_comm-2*epsH)/(2*M)>1e-8),unknown_complement_no_gap_assumed=True,rows=rows,HSE_converged=False,physical_xc=None)
    (HERE/'result.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');(HERE/'independent_checks.json').write_text(json.dumps(check,indent=2)+'\n')
    print('FD304 lower-op',out['fullspace_FD304_error_op_lower'])
    for x in rows:print(x['eta_eV'],x['ordering_eV'],x['ordering_interval_eV'],x['ordering_sign_conditional_on_action_error'])
if __name__=='__main__':main()
