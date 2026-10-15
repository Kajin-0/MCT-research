"""Independent small bath/moment identities and actual source/protection checks."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from scipy.linalg import block_diag
from analyze import HERE,SOURCE,PRIVATE,RYEV,norm,tests
sys.path.insert(0,str(SOURCE))
import owner as native

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def main():
    profile,job,root=native.load('host');n=json.loads((SOURCE/'native_result.json').read_text());assert n['accepted'] and not native.cgroup_path(n['guard']['cgroup']).exists()
    for p,pin in n['source_hashes'].items():assert sha(p)==pin
    a=json.loads((HERE/'result.json').read_text());assert sha(PRIVATE/'full_actions.npz')==a['source_full_action_sha256']
    p=np.load(PRIVATE/'trial.npz');h=np.load(PRIVATE/'full_actions.npz');A=(h['H']+h['H'].conj().T)/2;R=h['HV']-p['Q']@A;R-=p['Q']@(p['Q'].conj().T@R);W=R.conj().T@R;B=p['Q'].conj().T@p['P'];e,U=np.linalg.eigh((W+W.conj().T)/2);assert min(e)>-1e-8;S=(U*np.sqrt(np.maximum(e,0)))@U.conj().T
    z=a['rows'][3]['energy_Ry']+.5j/RYEV;c=z.real+.1
    H=np.block([[A,S],[S,c*np.eye(304)]]);P=np.r_[B,np.zeros_like(B)]
    direct=P.conj().T@np.linalg.solve(z*np.eye(608)-H,P);schur=B.conj().T@np.linalg.solve(z*np.eye(304)-A-W/(z-c),B);err=norm(direct-schur);assert err<1e-7
    # Independent finite Hermitian moment decomposition, using exact H action
    # on V but leaving e*H e unknown; verifies the squared-leakage bound.
    rng=np.random.default_rng(72415);X=rng.normal(size=(12,12))+1j*rng.normal(size=(12,12));H=(X+X.conj().T)/2;V=np.eye(12)[:,:5];X=rng.normal(size=(12,2))+1j*rng.normal(size=(12,2));C=V.conj().T@X;E=X-V@C;HV=H@V
    known=C.conj().T@(V.conj().T@HV)@C+(HV@C).conj().T@E+E.conj().T@(HV@C)
    defect=norm(X.conj().T@H@X-known);upper=norm(H)*norm(E)**2;assert defect<=upper+1e-10
    m=np.load(HERE/'physical_moments.npz');M1=m['M1'];M2=m['M2'];variance=M2-M1@M1;assert min(np.linalg.eigvalsh((variance+variance.conj().T)/2))>0
    # Traces and inverse differences invariant under independent sector gauges.
    U2=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0];U4=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))[0];K=block_diag(U2,U4);rot=K.conj().T@direct@K;gauge_error=max(abs(np.trace(rot[:2,:2])-np.trace(direct[:2,:2])),abs(np.trace(rot[2:,2:])-np.trace(direct[2:,2:])));assert gauge_error<1e-10
    assert a['fullspace_FD1e8_stationarity_EXCLUDED_conditionally']
    assert [x['ordering_sign_conditional_on_action_error'] for x in a['rows']]==[False,False,False,True,True,True]
    assumptions=a['arithmetic_allowances_NOT_interval_native_proven'];assert assumptions
    D=native.DFT;assert hashlib.sha256(subprocess.check_output(['git','diff','--binary'],cwd=D)).hexdigest()=='a716be79058b719e363f19b16fdacc228e4093b3f87bdd6b64ac96aa7e78b0f0'
    assert sha(D/'.local/qe-env/bin/pw.x')=='1d66c7856f5d6b3cd9c66b8578e01512b16bbe907b4360e54234890712ccd6a1'
    assert sha(native.REGISTRY)=='82b3e668eeea5dff015b444cf362f945f7a5791d5fa6fe666948b0ab29c31baf'
    prior=json.loads((SOURCE/'verification.json').read_text())
    for path,pin in prior['old_negative_sha256'].items():assert sha(path)==pin
    tests()
    out=dict(status='PASS_READ_ONLY_PROOFS_AND_NATIVE_INPUT_CHECKS',independent608_dense_vs_Schur_error=err,independent_moment_unknown_block_error=defect,independent_moment_bound=upper,physical_sector_gauge_error=float(gauge_error),all_native_pins_and_protected_DFT_stock_old_failures_PASS=True,no_new_native_job=True,old_owner_and_splice_failures_NOT_reclassified=True,finite_arithmetic_condition_NOT_interval_proven=assumptions,sources={str(x):sha(x) for x in [HERE/'analyze.py',HERE/'moment_reduction.py',HERE/'completion_check.py',HERE/'directed_completion.py',HERE/'theory.md',SOURCE/'native_result.json',HERE/'result.json',HERE/'moment_result.json']},HSE_converged=False,physical_xc=None)
    (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
