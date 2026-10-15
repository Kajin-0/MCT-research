"""Read-only numerical intake AFTER preserved cross-run byte-control refusal."""
import json
from pathlib import Path
import numpy as np
from compare import input_record,output_record,packet
import run_probe as r

def main():
    root=r.PAIR/'host';old=r.DFT/'.local/qe75_lowram_20261011/h8c_20261015/p1/host'
    assert 'retained canonical direct action byte mismatch' in (r.HERE/'launch.log').read_text()
    assert not(root/'FINAL.json').exists()
    ranks=json.loads((root/'RANKS.json').read_text());inputs=[input_record(root,k) for k in [0,1]]
    G=np.array(sorted(tuple(g) for b in inputs for g in b['G']));N=len(G);lookup={tuple(g):i for i,g in enumerate(G)}
    minus=np.array([lookup[tuple(-g)] for g in G]);A={s:np.empty((2*N,12),complex) for s in [1,2]};controls=[]
    for rank,b in enumerate(inputs):
        p,n=map(int,b['h'][3:5]);ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        prior=packet(old,'after',rank,1)
        for s in [1,2]:
            v=output_record(root,rank,s);assert int(v['h'][3])==ranks[str(rank)]['pid']
            for key in ['B','k','G','et','wg','trial']:assert v[key].tobytes()==b[key].tobytes()
            assert v['phi'].tobytes()==b['phi' if s==1 else 'reverse'].tobytes()
            A[s][glob]=v['action'][ix]
            if s==1:
                a=v['action'][:,:6];c=prior['direct_probe'];d=a-c
                controls.append(dict(rank=rank,byte_equal=a.tobytes()==c.tobytes(),max_abs_Ry=float(max(abs(d).ravel())),
                    relative=float(np.linalg.norm(d)/max(1.,np.linalg.norm(a),np.linalg.norm(c))),numeric_elements_unequal=int(np.sum(a!=c)),
                    active_max_Ry=float(max(abs(d[ix]).ravel())),padding_max_Ry=float(max(abs(np.delete(d,ix,axis=0)).ravel())) if p>n else 0.))
    theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    relative=lambda a,b:float(np.linalg.norm(a-b)/max(1.,np.linalg.norm(a),np.linalg.norm(b)))
    g=json.loads((root/'GUARD_RESULT.json').read_text());t=json.loads((root/'TERMINAL.json').read_text())
    assert g['pass_guard'] and t['terminal'] and not r.cgroup_path(g['cgroup']).exists()
    result=dict(verdict='REFUSED_REFERENCE_BYTE_MISMATCH_UNCHANGED',preregistered_qualification_pass=False,new_native_invocations=0,
        original_refusal_log_sha256=r.sha(r.HERE/'launch.log'),all_actual_source_trial_and_basis_bytes_match=True,control_differences=controls,
        diagnostic_internal_kernel_TR_covariance_relative=relative(A[2][:,6:],theta(A[1][:,:6])),
        diagnostic_second_covariance_relative=relative(A[2][:,:6],-theta(A[1][:,6:])),
        diagnostic_internal_covariance_absolute_max_Ry=float(max(abs(A[2][:,6:]-theta(A[1][:,:6])).ravel())),
        diagnostic_within_original_source_TR_relative=relative(A[1][:,6:],theta(A[1][:,:6])),
        diagnostic_only_no_retroactive_byte_gate_relaxation=True,guard=g,terminal=t,physical_xc=None)
    np.savez(r.HERE/'refused_native_actions.npz',G=G,D_action=A[1],ThetaD_action=A[2])
    (r.HERE/'refusal_audit.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['terminal','guard']},indent=2))

if __name__=='__main__':main()
