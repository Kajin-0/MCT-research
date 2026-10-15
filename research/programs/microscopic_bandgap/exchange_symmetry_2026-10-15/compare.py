"""Complete canonical readback, retained direct control and pure-kernel TR test."""
import json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hybrid_convergence_2026-10-15'))
from packets import Reader,packet

def input_record(root,rank):
    r=Reader(root/'pilot'/f'input.rank{rank}');h=r.take('<i8',(8,));p,n=map(int,h[3:5])
    assert tuple(h)==(70251501,1,rank,p,n,176,2,12)
    x=dict(h=h,B=r.take('<f8',(3,3)),k=r.take('<f8',(3,)),G=r.take('<i8',(3,n)).T,et=r.take('<f8',(176,)),wg=r.take('<f8',(176,)),phi=r.take('<c16',(p*2,176)),reverse=r.take('<c16',(p*2,176)),trial=r.take('<c16',(p*2,12)))
    r.end();return x

def output_record(root,rank,source):
    r=Reader(root/'pilot'/f's{source}.rank{rank}');h=r.take('<i8',(8,));p,n=map(int,h[4:6])
    assert tuple(h[[0,1,2,6,7]])==(70251502,1,rank,source,176)
    x=dict(h=h,extent=r.take('<i8',(10,)),B=r.take('<f8',(3,3)),k=r.take('<f8',(3,)),scalars=r.take('<f8',(4,)),G=r.take('<i8',(3,n)).T,et=r.take('<f8',(176,)),wg=r.take('<f8',(176,)),phi=r.take('<c16',(p*2,176)),trial=r.take('<c16',(p*2,12)),action=r.take('<c16',(p*2,12)))
    r.end();return x

def validate_native(root):
    old=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/h8c_20261015/p1/host')
    ranks=json.loads((root/'RANKS.json').read_text());before=[input_record(root,i) for i in [0,1]]
    G=np.array(sorted(tuple(g) for b in before for g in b['G']));N=len(G);assert N==10827
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G])
    A={s:np.empty((2*N,12),complex) for s in [1,2]};checks=[]
    for rank,b in enumerate(before):
        prior=packet(old,'after',rank,1)
        p,n=map(int,b['h'][3:5]);ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        for source in [1,2]:
            v=output_record(root,rank,source)
            assert int(v['h'][3])==ranks[str(rank)]['pid'] and tuple(v['h'][4:6])==(p,n)
            for key in ['B','k','G','et','wg','trial']:
                assert v[key].tobytes()==b[key].tobytes(),(source,rank,key)
            assert v['phi'].tobytes()==b['phi' if source==1 else 'reverse'].tobytes()
            assert tuple(v['extent'][:3])==(60,60,60) and v['extent'][6]==1 and v['extent'][9]==1
            np.testing.assert_allclose(v['scalars'],[1.,.25,200.,.106],rtol=0,atol=1e-12)
            assert abs(sum(v['wg'])-144)<1e-8
            A[source][glob]=v['action'][ix]
            if source==1:
                # Exact six-column native layout, including padding/signed zeros.
                assert v['action'][:,:6].tobytes()==prior['direct_probe'].tobytes(),'retained canonical direct action byte mismatch'
            checks.append(dict(source=source,rank=rank,source_trial_basis_byte_exact=True))
    theta=lambda v:np.r_[v[N+minus].conj(),-v[minus].conj()]
    relative=lambda a,b:float(np.linalg.norm(a-b)/max(1.,np.linalg.norm(a),np.linalg.norm(b)))
    first=relative(A[2][:,6:],theta(A[1][:,:6]))
    second=relative(A[2][:,:6],-theta(A[1][:,6:]))
    text=(root/'pw.out').read_text();assert text.count('R07_FIXED_FOCK_SOURCE_COMPLETE')==2 and 'R07_FIXED_FOCK_TR_DONE' in text and 'JOB DONE.' in text
    result=dict(scientific_pass=bool(max(first,second)<=1e-8),source_checks=checks,retained_first_direct_control_byte_exact=True,
        kernel_TR_covariance_relative=first,kernel_TR_covariance_second_identity_relative=second,
        kernel_TR_covariance_absolute_max_Ry=float(max(abs(A[2][:,6:]-theta(A[1][:,:6])).ravel())),
        within_original_source_TR_action_relative=relative(A[1][:,6:],theta(A[1][:,:6])),
        SCF_performed=False,not_assuming_source_TR_invariant=True,physical_xc=None)
    np.savez(HERE/'native_actions.npz',G=G,D_action=A[1],ThetaD_action=A[2])
    (HERE/'numerical_result.json').write_text(json.dumps(result,indent=2)+'\n');return result
