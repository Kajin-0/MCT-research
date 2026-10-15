"""Actual original physical probe moments, with an explicit unknown block."""
import json,sys
import numpy as np
from analyze import HERE,SOURCE,PRIVATE,RYEV,norm
sys.path.insert(0,str(SOURCE))
from readback import decode

def positive_root(G):
    e,U=np.linalg.eigh((G+G.conj().T)/2);assert min(e)>0
    return (U*np.sqrt(e))@U.conj().T,(U/np.sqrt(e))@U.conj().T

def main():
    f=np.load(PRIVATE/'trial.npz');V=f['Q'];P=f['P'];G=f['G'];N=len(G);lookup={tuple(g):i for i,g in enumerate(G)};a=np.load(PRIVATE/'full_actions.npz');HV=a['HV'];A=(a['H']+a['H'].conj().T)/2;M=json.loads((SOURCE/'native_science.json').read_text())['H_operator_norm_upper_Ry']
    HP=np.zeros_like(P)
    for rank in [0,1]:
        b=decode(PRIVATE/'p1/host/pilot'/f'H.rank{rank}');p,n=map(int,b['h'][4:6]);local=np.r_[np.arange(n),np.arange(p,p+n)];loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc];HP[glob]=b['control'][local]
    _,inverse=positive_root(P.conj().T@P);Q1=P@inverse;HQ1=HP@inverse;A1=Q1.conj().T@HQ1;L=HQ1-Q1@A1;B1,invB1=positive_root(L.conj().T@L);Q2=L@invB1
    C=V.conj().T@Q2;e=Q2-V@C;HX=HV@C
    # Q2=VC+e. All cross terms with e are known from H(VC), not H(e).
    T22=C.conj().T@A@C+HX.conj().T@e+e.conj().T@HX
    unknown22=M*norm(e)**2
    direct_moments=[Q1.conj().T@HQ1,HQ1.conj().T@HQ1]
    # X=HQ1; decompose X into the known query space. Only e*H e unknown.
    CX=V.conj().T@HQ1;ex=HQ1-V@CX;HXknown=HV@CX
    M3=CX.conj().T@A@CX+HXknown.conj().T@ex+ex.conj().T@HXknown
    M3unknown=M*norm(ex)**2
    # Geometry of ALL known queries, including original P and ThetaP.
    # Only ranks above declared thresholds are numerical claims.
    probes=f['trial'][:,304:316];leak=probes-V@(V.conj().T@probes);uu,ss,_=np.linalg.svd(leak,full_matrices=False)
    geometry=[]
    for threshold in [1e-8,1e-10]:
        added=uu[:,ss>threshold];added-=V@(V.conj().T@added);added-=V@(V.conj().T@added);added=np.linalg.qr(added,mode='reduced')[0];T=np.c_[V,added];assert norm(T.conj().T@T-np.eye(T.shape[1]))<1e-12;out=Q2-T@(T.conj().T@Q2)
        sv=np.linalg.svd(out,compute_uv=False);geometry.append(dict(threshold=threshold,known_query_span_dimension=T.shape[1],outside_singular_values=sv.tolist(),missing_query_rank=int(sum(sv>threshold))))
    branches=[]
    for sl in [slice(0,2),slice(2,6)]:
        n=sl.stop-sl.start
        branches.append(dict(first_moment_Ry=float(np.trace(A1[sl,sl]).real/n),central_variance_Ry2=float(np.trace((B1@B1)[sl,sl]).real/n),spectral_standard_deviation_eV=float(np.sqrt(np.trace((B1@B1)[sl,sl]).real/n)*RYEV),second_block_diagonal_estimate_Ry=float(np.trace(T22[sl,sl]).real/n),second_block_diagonal_unknown_complement_error_Ry=unknown22,third_raw_moment_estimate_Ry3=float(np.trace(M3[sl,sl]).real/n),third_raw_moment_unknown_complement_error_Ry3=M3unknown))
    out=dict(status='CALCULATED_NATIVE_ORIGINAL_PROBE_MOMENTS',native_control_actions_USED=True,projected_control_error_op_Ry=norm(HP-HV@(V.conj().T@P)),physical_frame_Gram_normalization_op=norm(inverse-np.eye(6)),physical_frame_coverage_error_op=norm(P-V@(V.conj().T@P)),first_two_moments_full_action_measured=True,third_moment_only_CONDITIONAL_bounded_unknown_block=True,fourth_moment_NOT_closed=True,outside304_physical_residual_directions_rank_at_1e8=int(sum(np.linalg.svd(e,compute_uv=False)>1e-8)),all_known_query_geometry=geometry,known_vs_query_next_block_coverage_op=norm(e),second_block_diagonal_unknown_op_error_Ry=unknown22,third_moment_unknown_op_error_Ry3=M3unknown,branches_Gamma6_Gamma8=branches,whole_H_coarse_norm_bound_Ry=M,source_action_arithmetic_allowance_required_separately=True,HSE_converged=False,physical_xc=None)
    (HERE/'moment_result.json').write_text(json.dumps(out,indent=2)+'\n');np.savez(HERE/'physical_moments.npz',M1=direct_moments[0],M2=direct_moments[1],M3_estimate=M3,second_block_estimate=T22)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
