"""Fresh canonical sources/trials and versioned profile; no service/native run."""
import json,os,sys,uuid
from pathlib import Path
import numpy as np
import run_probe as r
OLD=r.HERE.parent/'hybrid_convergence_2026-10-15'
sys.path.insert(0,str(OLD))
from packets import packet

def prepare():
    if r.PAIR.exists():raise FileExistsError('fresh root only')
    root=r.PAIR/'host';root.mkdir(parents=True,mode=0o700)
    for n in ['out','tmp','pp','pilot']:(root/n).mkdir(mode=0o700)
    prior=r.DFT/'.local/qe75_lowram_20261011/h8c_20261015/p1/host'
    final=json.loads((prior/'FINAL.json').read_text());assert final['accepted'] and not r.cgroup_path(final['guard']['cgroup']).exists()
    text=(prior/'pw.in').read_text().replace(str(prior),str(root)).replace('max_seconds=1700','max_seconds=500')
    (root/'pw.in').write_text(text);(root/'reference.bin').write_bytes((prior/'reference.bin').read_bytes())
    for pp in (prior/'pp').iterdir():(root/'pp'/pp.name).write_bytes(pp.read_bytes())
    before=[packet(prior,'before',i,1) for i in [0,1]];after=[packet(prior,'after',i,1) for i in [0,1]]
    G=np.array(sorted(tuple(g) for b in before for g in b['G']));assert len(G)==10827
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);N=len(G)
    phi=np.empty((2*N,176),complex);probe=np.empty((2*N,6),complex)
    for b,a in zip(before,after):
        n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        phi[glob]=b['phi'][ix];probe[glob]=a['probe'][ix]
    theta=lambda x:np.r_[x[N+minus].conj(),-x[minus].conj()]
    assert np.array_equal(theta(theta(phi)),-phi)
    assert np.linalg.norm(phi.conj().T@phi-np.eye(176),2)<1e-8
    assert np.linalg.norm(probe.conj().T@probe-np.eye(6),2)<1e-8
    tphi,tprobe=theta(phi),theta(probe)
    for rank,(b,a) in enumerate(zip(before,after)):
        n,p=b['nnpw'],b['npwx'];ix=np.r_[np.arange(n),np.arange(p,p+n)]
        loc=np.array([lookup[tuple(g)] for g in b['G']]);glob=np.r_[loc,N+loc]
        reversed=np.zeros_like(b['phi']);reversed[ix]=tphi[glob]
        trial=np.zeros((2*p,12),complex);trial[:,:6]=a['probe'];trial[ix,6:]=tprobe[glob]
        values=[np.array([70251501,1,rank,p,n,176,2,12],dtype='<i8'),b['B'].astype('<f8'),b['k'].astype('<f8'),b['G'].T.astype('<i8'),b['et'].astype('<f8'),b['wg'].astype('<f8'),b['phi'].astype('<c16'),reversed.astype('<c16'),trial.astype('<c16')]
        (root/'pilot'/f'input.rank{rank}').write_bytes(b''.join(v.tobytes(order='F') for v in values))
    build=json.loads((r.HERE/'build_results.json').read_text());assert build['passed'] and r.sha(r.QE)==build['binary_sha256']
    pins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,r.HERE/'run_probe.py',r.HERE/'preregistration.md',r.HERE/'operator_input_proof.md',r.HERE/'compare.py',r.HERE/'prepare_inputs.py',r.HERE/'probe_native.inc',r.HERE/'build_results.json',r.HERE/'address_admission.py']
    pins+=[r.BASE/'terminal_owner_2026-10-14'/n for n in ['retirement.py','sampled_output.py']]
    pins+=[r.BASE/'runtime_admission'/n for n in ['process_identity.py','family_runtime.py']]
    pins+=[r.BASE/'cgroup_owned_2026-10-13/contracts.py',r.BASE/'checkpoint_phase/resource_guard.py']
    pins+=[root/'pw.in',root/'reference.bin',*list((root/'pp').iterdir()),*list((root/'pilot').iterdir())]
    pins+=[prior/'FINAL.json',prior/'pw.in',OLD/'packets.py']
    pins+=[prior/'pilot'/f'c1_{stage}.rank{rank}' for stage in ['before','after'] for rank in [0,1]]
    pins+=[Path(v) for v in build['source_pins']]+[Path(v) for v in build['backends']]
    pins+=[r.DFT/'.local/qe-env/bin/pw.x']
    profile=dict(kind='R07_CANONICAL_FOCK_TR_V1',physical=dict(nat=8,nbnd=176,nelec=144,ecutwfc_Ry=50,ecutrho_Ry=200,ecutfock_Ry=200,kgrid=[1,1,1],qgrid=[1,1,1],exx_fraction=.25,screening_Bohr_inverse=.106),
        limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=600,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB,file=r.GIB,escrow=64*(1<<20)),
        pins={str(p):r.sha(p) for p in pins},ranks=2,hostwide_exclusion=False,private_network_proof=False,SCF_performed=False)
    job=dict(kind=profile['kind'],root=str(root),member='host',unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
    r.atomic_json(r.PAIR/'PROFILE.json',profile);r.atomic_json(root/'JOB.json',job)
    r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs=dict(host=job)))

if __name__=='__main__':prepare()
