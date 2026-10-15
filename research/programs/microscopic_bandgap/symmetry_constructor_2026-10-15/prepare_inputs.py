"""Fresh versioned canonical data, paired auxiliary cover and immutable profile."""
import json
import sys
import uuid
from pathlib import Path
import numpy as np
import run_probe as r

OLD = r.HERE.parent/'hybrid_convergence_2026-10-15'
ANALYSIS = r.HERE.parent/'antiunitary_closure_2026-10-15'
sys.path.insert(0, str(OLD)); sys.path.insert(0, str(ANALYSIS))
from packets import packet


def prepare():
    if r.PAIR.exists():
        raise FileExistsError('fresh operator root only; never retry old job')
    prior=r.DFT/'.local/qe75_lowram_20261011/h8c_20261015/p1/host'
    before=[packet(prior,'before',i,1) for i in [0,1]]
    after=[packet(prior,'after',i,1) for i in [0,1]]
    G=np.array(sorted(tuple(g) for b in before for g in b['G'])); N=len(G)
    assert N==10827
    lookup={tuple(g):i for i,g in enumerate(G)}
    minus=np.array([lookup[tuple(-g)] for g in G])
    phi=np.empty((2*N,176),complex); P=np.empty((2*N,6),complex)
    for b,a in zip(before,after):
        n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        phi[glob]=b['phi'][ix];P[glob]=a['probe'][ix]
    theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    old=json.loads((ANALYSIS/'constructor_result.json').read_text())
    assert r.sha(old['basis_path'])==old['basis_sha256']
    Q=np.load(old['basis_path'])['Q']
    # Extend the measured352paired basis by the independent physical reference.
    # This does not modify the original reference or its Gamma assignment.
    for j in range(6):
        q=P[:,j].copy()
        for _ in range(2):q-=Q@(Q.conj().T@q)
        norm=np.linalg.norm(q)
        assert norm>1e-10, 'unexpected reference rank; freeze new design before native use'
        q/=norm
        Q=np.column_stack((Q,q,theta(q[:,None])[:,0]))
    assert Q.shape==(2*N,364)
    cover_phi=float(np.linalg.norm(phi-Q@(Q.conj().T@phi),2))
    cover_P=float(np.linalg.norm(P-Q@(Q.conj().T@P),2))
    gram=float(np.linalg.norm(Q.conj().T@Q-np.eye(364),2))
    closure=float(np.linalg.norm(theta(Q)-Q@(Q.conj().T@theta(Q)),2))
    assert max(cover_phi,cover_P,gram,closure)<1e-10
    trial=np.column_stack((Q,P,theta(P))); nt=trial.shape[1]
    assert nt==376
    root=r.PAIR/'host';root.mkdir(parents=True,mode=0o700)
    for name in ['out','tmp','pp','pilot']:(root/name).mkdir(mode=0o700)
    text=(prior/'pw.in').read_text().replace(str(prior),str(root)).replace('max_seconds=1700','max_seconds=850')
    (root/'pw.in').write_text(text)
    (root/'reference.bin').write_bytes((prior/'reference.bin').read_bytes())
    for pp in (prior/'pp').iterdir():(root/'pp'/pp.name).write_bytes(pp.read_bytes())
    for rank,b in enumerate(before):
        n,p=b['nnpw'],b['npwx']; ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        reverse=np.zeros_like(b['phi']);reverse[ix]=theta(phi)[glob]
        trials=np.zeros((2*p,nt),complex);trials[ix]=trial[glob]
        values=[np.array([70251501,1,rank,p,n,176,2,nt],dtype='<i8'),b['B'].astype('<f8'),b['k'].astype('<f8'),b['G'].T.astype('<i8'),b['et'].astype('<f8'),b['wg'].astype('<f8'),b['phi'].astype('<c16'),reverse.astype('<c16'),trials.astype('<c16')]
        with (root/'pilot'/f'input.rank{rank}').open('xb') as f:
            for v in values:f.write(v.tobytes(order='F'))
    build=json.loads((r.HERE/'build_results.json').read_text());assert build['passed'] and r.sha(r.QE)==build['binary_sha256']
    pins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*r.HERE.glob('*.py'),r.HERE/'preregistration.md',r.HERE/'operator_input_proof.md',r.HERE/'probe_native.inc',r.HERE/'build_results.json']
    pins+=[r.BASE/'terminal_owner_2026-10-14'/n for n in ['retirement.py','sampled_output.py']]
    pins+=[r.BASE/'runtime_admission'/n for n in ['process_identity.py','family_runtime.py']]
    pins+=[r.BASE/'cgroup_owned_2026-10-13/contracts.py',r.BASE/'checkpoint_phase/resource_guard.py']
    pins+=[root/'pw.in',root/'reference.bin',*list((root/'pp').iterdir()),*list((root/'pilot').iterdir())]
    pins+=[prior/'FINAL.json',prior/'pw.in',OLD/'packets.py',ANALYSIS/'constructor.py',ANALYSIS/'constructor_result.json',Path(old['basis_path'])]
    pins+=[prior/'pilot'/f'c1_{stage}.rank{rank}' for stage in ['before','after'] for rank in [0,1]]
    pins+=[Path(v) for v in build['source_pins']]+[Path(v) for v in build['backends']]
    pins+=[r.DFT/'.local/qe-env/bin/pw.x']
    profile=dict(kind='R07_PAIRED_CONSTRAINED_ENSEMBLE_FOCK_V1',physical=dict(nat=8,nbnd=176,nelec=144,ecutwfc_Ry=50,ecutrho_Ry=200,ecutfock_Ry=200,kgrid=[1,1,1],qgrid=[1,1,1],exx_fraction=.25,screening_Bohr_inverse=.106),
        limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=900,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB,file=r.GIB,escrow=64*(1<<20)),
        pins={str(p):r.sha(p) for p in pins},ranks=2,hostwide_exclusion=False,private_network_proof=False,SCF_performed=False,
        auxiliary_columns=364,trials=376,TR_constrained_ensemble=True,native_ACE_built=False)
    job=dict(kind=profile['kind'],root=str(root),member='host',unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
    r.atomic_json(r.PAIR/'PROFILE.json',profile);r.atomic_json(root/'JOB.json',job)
    r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs=dict(host=job)))
    r.atomic_json(r.HERE/'extended_basis.json',dict(dimension=364,trial_columns=376,source_cover_op=cover_phi,reference_cover_op=cover_P,Gram_defect_op=gram,TR_closure_op=closure,paired_constructor='extend measured352basis by6reference/Theta pairs',no_source_or_occupation_edit=True))


if __name__=='__main__':prepare()
