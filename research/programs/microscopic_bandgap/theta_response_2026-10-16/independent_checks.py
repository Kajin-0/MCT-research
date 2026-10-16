"""Actual-data column/trace formulas and coordinate-gauge checks; no models/jobs."""
import json
import csv
import sys
from pathlib import Path
import numpy as np
from analyze import HERE, PARENT, RY, W, setup, split, op, herm


def main():
    d=np.load(PARENT/'contracted_actions.npz'); F,G=d['reference'],d['G']
    theta,V,inv,R,info=setup(F,G)
    result=json.loads((HERE/'result.json').read_text())
    records={}
    # Unitary changes of coordinates WITHIN the original sectors, not a new
    # projector or an invented material Hamiltonian.
    U=np.zeros((6,6),complex)
    for lo,n in [(0,2),(2,4)]:
        k=np.arange(n); U[lo:lo+n,lo:lo+n]=np.exp(2j*np.pi*np.outer(k,k)/n)/np.sqrt(n)
    assert op(U.conj().T@U-np.eye(6))<1e-14
    for key,label,M in [('c1','chemical_1',64),('c2','chemical_2',64),('change','chemical_change',128)]:
        Y=d[key+'_action_Ry']; Yv=Y@inv; raw=V.conj().T@Yv; A=herm(raw)
        B=Yv-V@raw; Yh=V@A+B; J=V.conj().T@theta(V); a=float(np.trace(A).real/6)
        TY=-theta(Yh@J+V@(B.conj().T@R)+a*R)
        E,O=(Yh+TY)/2,(Yh-TY)/2
        direct_formula=(J.conj().T@A@J+J.conj().T@B.conj().T@R+
                        R.conj().T@B@J+a*R.conj().T@R).conj()
        rr,e,o=split(Y,F,theta,V,inv,R,M)
        compare=op(E-e)*RY+op(O-o)*RY
        trace_error=abs(float(np.trace(W@direct_formula).real*RY)-
                        float(np.trace(W@(V.conj().T@TY)).real*RY))
        assert compare<1e-9 and trace_error<1e-9
        theta2,V2,inv2,R2,_=setup(F@U,G)
        rotated,e2,o2=split(Y@U,F@U,theta2,V2,inv2,R2,M)
        unitary_error=max(op(e2-e@U),op(o2-o@U))*RY
        # Scalar energy origin and global antiunitary phase must not alter the
        # Q actions or trace. An unanchored zero-QQ representative would FAIL.
        shift=.125
        shifted,es,os=split(Y+shift*F,F,theta,V,inv,R,M)
        scalar_error=max(op(es-e-shift*V),op(os-o))*RY
        zeta=np.exp(1j*.713)
        phased,ep,oo=split(Y,F,lambda x:zeta*theta(x),V,inv,R,M)
        phase_error=max(op(ep-e),op(oo-o))*RY
        assert max(unitary_error,scalar_error,phase_error)<1e-8
        for sign in ('even','odd'):
            assert abs(rotated[sign]['known_column_centre_trace_meV']-rr[sign]['known_column_centre_trace_meV'])<1e-8
            assert abs(shifted[sign]['known_column_centre_trace_meV']-rr[sign]['known_column_centre_trace_meV'])<1e-8
        records[label]=dict(alternative_column_reconstruction_meV=compare,
             independent_transformed_trace_error_meV=trace_error,
             block_unitary_covariance_error_meV=unitary_error,
             scalar_reference_covariance_error_meV=scalar_error,
             antiunitary_phase_invariance_error_meV=phase_error)
        assert abs(rr['even']['Q_op_centre_meV']-result['observations'][label]['even']['Q_op_centre_meV'])<1e-9
    # Demonstrate non-identifiability on the ACTUAL native reference residual,
    # without a synthetic spectrum. A Hermitian QQ perturbation leaves CF exact
    # but changes the transformed trace since R W Rdagger is nonzero.
    Q,_=np.linalg.qr(R); K=herm((Q.conj().T@R)@W@(R.conj().T@Q))
    vals,vec=np.linalg.eigh(K); j=int(np.argmax(abs(vals))); u=Q@vec[:,j]
    u-=V@np.linalg.solve(V.conj().T@V,V.conj().T@u); u/=np.linalg.norm(u)
    input_omission=op(u.conj()[None,:]@V)
    ur=u.conj()@R
    actual_trace_direction=float((ur@W@ur.conj()).real/2)
    assert input_omission<1e-14 and abs(actual_trace_direction)>1e-16
    out=dict(passed=True,native_jobs=0,actual_data_checks=records,
       information_NO_GO=dict(unknown_QQ_rank1_leaves_input_residual=input_omission,
         nonzero_half_transformed_trace_direction=actual_trace_direction,
         exact_six_column_decomposition_identified=False),
       source_conditioned_not_material_bounds=True,
       scope='column algebra, transformed trace, real/basis/scalar/Theta phase gauges on retained data; no synthetic Hamiltonian')
    (HERE/'independent_results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    with (HERE/'response_table.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(['response','original_trace_meV','even_trace_lower_meV','even_trace_upper_meV',
          'odd_trace_lower_meV','odd_trace_upper_meV','Q_even_op_lower_meV','Q_even_op_upper_meV',
          'Q_odd_op_lower_meV','Q_odd_op_upper_meV','interval_status'])
        for name,row in result['observations'].items():
            writer.writerow([name,row['original_trace_meV'],*row['even']['trace_interval_meV'],
              *row['odd']['trace_interval_meV'],*row['even']['Q_op_interval_meV'],
              *row['odd']['Q_op_interval_meV'],'source-conditioned; floating evaluation; not material uncertainty'])
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
