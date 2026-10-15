"""One fresh append query, same binary and source. No native execution here."""
from pathlib import Path
import ast,fcntl,json,os,socket,subprocess,sys,uuid
import numpy as np
import owner as r
from accepted import OLD,PRIVATE,decode,frames,old_action,sha


def prepare():
    if r.PAIR.exists():raise FileExistsError('fresh p2 only; preserve failed attempt')
    protected=json.loads((OLD/'protected_after.json').read_text())
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==protected['DFT_status']
    assert r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==protected['DFT_tracked_diff_sha256']
    for p,h in protected['files'].items():assert sha(p)==h
    for name in ['pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    assert json.loads(r.REGISTRY.read_text())['phase']=='FINISHED' and json.loads(r.REGISTRY.read_text())['members']==[]
    lock=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(lock)
    # Old accepted evidence and all immutable native inputs are independently pinned.
    frozen=json.loads((OLD/'frozen_protocol.json').read_text())
    for p,h in frozen['profile']['pins'].items():assert sha(p)==h
    manifest=json.loads((OLD/'evidence_manifest.json').read_text())
    for row in manifest['all_private_files']:assert sha(row['path'])==row['sha256']
    tr=json.loads((OLD/'trial_result.json').read_text());kr=json.loads((OLD/'krylov_result.json').read_text())
    assert sha(tr['trial_path'])==tr['trial_sha256'] and sha(kr['basis_path'])==kr['basis_sha256']
    build=json.loads((OLD/'build_results.json').read_text());assert build['passed'] and sha(r.QE)==build['binary_sha256']
    for p,h in build['source_pins'].items():assert sha(p)==h
    for p,h in build['backends'].items():assert sha(p)==h
    for p in r.HERE.glob('*.py'):ast.parse(p.read_text())
    f,b,G,Q,L,V=frames();B=np.column_stack((Q,L));C=V.conj().T@B;HQ=old_action(G)
    gram=float(np.linalg.norm(B.conj().T@B-np.eye(304),2));basis_error=float(np.linalg.norm(B-V@C,'fro'))
    fit=float(np.linalg.norm(HQ-V@(V.conj().T@HQ),'fro'))
    assert gram<1e-8 and basis_error<1e-8 and fit<1e-8 and kr['maximum_all_group_Theta_translation_leakage_F']<1e-8
    assert abs(sum(f['weights'])-144)<1e-8 and np.linalg.matrix_rank(C,tol=1e-8)==304
    root=r.PAIR/'host';root.mkdir(parents=True,mode=0o700)
    for name in ['out','tmp','pp','pilot']:(root/name).mkdir(mode=0o700)
    prior=PRIVATE/'p1/host';original=(prior/'pw.in').read_bytes();text=original.replace(str(prior).encode(),str(root).encode())
    assert text.replace(str(root).encode(),str(prior).encode())==original;(root/'pw.in').write_bytes(text)
    for p in (prior/'pp').iterdir():(root/'pp'/p.name).write_bytes(p.read_bytes())
    query=np.column_stack((L,f['trial'][:,152:]));assert query.shape[1]==164
    extents={}
    for rank in [0,1]:
        old=decode(prior/'pilot'/f'H.rank{rank}');p,n=map(int,old['h'][4:6]);lookup={tuple(g):i for i,g in enumerate(G)};i=np.array([lookup[tuple(g)] for g in old['G']]);glob=np.r_[i,len(G)+i];active=np.r_[np.arange(n),np.arange(p,p+n)]
        trial=np.zeros((2*p,164),complex);trial[active]=query[glob]
        oldbytes=(prior/'pilot'/f'input.rank{rank}').read_bytes();prefix=oldbytes[:-2*p*164*16]
        assert len(prefix)+trial.nbytes==len(oldbytes)
        path=root/'pilot'/f'input.rank{rank}'
        with path.open('xb') as out:out.write(prefix);out.write(trial.astype('<c16').tobytes(order='F'))
        assert path.read_bytes()[:len(prefix)]==prefix
        from packets import Reader
        rr=Reader(path);rr.take('<i8',(16,));rr.take('<f8',(3,3));rr.take('<f8',(3,));rr.take('<i8',(3,n));w=rr.take('<f8',(176,));s=rr.take('<c16',(2*p,176));t=rr.take('<c16',(2*p,164));rr.end()
        assert s.tobytes()==old['source'].tobytes() and w.tobytes()==old['wg'].tobytes()
        assert t[active].tobytes()==np.ascontiguousarray(query[glob]).tobytes()
        assert t[:,152:].tobytes()==old['trial'][:,152:].tobytes()
        bound=16*2*p*(176+5*164+6)+24*(n+216000)+16*216000*4+8*216000*8+16384
        assert bound<r.GIB;extents[str(rank)]=dict(npwx=p,nnpw=n,input_B=path.stat().st_size,old_prefix_sha256=r.hashlib.sha256(prefix).hexdigest(),output_upper_B=bound)
    address=r.checked_address(root);r.refuse_reuse(root);server=socket.socket(socket.AF_UNIX);client=socket.socket(socket.AF_UNIX)
    try:
        server.bind(address);inode=Path(address).lstat().st_ino;server.listen(1);client.connect(address);peer,_=server.accept();peer.close()
    finally:
        client.close();server.close()
        if Path(address).exists() and Path(address).lstat().st_ino==inode:Path(address).unlink()
    fixed=[p for p in PRIVATE.rglob('*') if p.is_file() and r.PAIR not in p.parents];fixed_charge=sum(p.stat().st_blocks*512+4096 for p in fixed)+8*2**20
    pins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*r.HERE.glob('*.py'),r.HERE/'preregistration.md',r.HERE/'operator_proof.md',root/'pw.in',*list((root/'pp').iterdir()),*list((root/'pilot').iterdir()),*fixed]
    pins += [Path(p) for p in frozen['profile']['pins']]+[OLD/'frozen_protocol.json',OLD/'evidence_manifest.json',OLD/'readback.py',OLD/'krylov_result.json',OLD/'verification.json']
    profile=dict(kind='R07_SAME_D_APPEND152_DIRECT_H_HOST_V1',physical=dict(nat=8,source_buffer=176,natural_source=146,joint_space=304,new_queries=152,trials=164,nelec=144,ecutwfc_Ry=50,ecutrho_Ry=200,ecutfock_Ry=200,kgrid=[1,1,1],qgrid=[1,1,1],exx_fraction=.25,screening_Bohr_inverse=.106,sigma_Ry=.001,same_D0_as_accepted=True,fixed_trial_NOT_FD=True),limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=600,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB-fixed_charge,file=r.GIB,escrow=64*2**20),fixed_prepared_charge_B=fixed_charge,total_owned_cap_B=14*r.GIB,pins={str(p):sha(p) for p in pins},ranks=2,SCF_performed=False,hostwide_exclusion=False,private_network_proof=False)
    job=dict(kind=profile['kind'],root=str(root),member='host',unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
    r.atomic_json(r.PAIR/'PROFILE.json',profile);r.atomic_json(root/'JOB.json',job);r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs=dict(host=job)))
    r.load('host');storage=r.LinuxGuard(r.LIB).probe(root);mem=r.memory()['MemAvailable'];admit=r.admission(storage,[64*2**20],14*r.GIB,mem)
    forecast=4245749760+2*r.GIB;timing=2*185.303861+60;assert forecast<12*r.GIB and timing<600
    result=dict(status='PASS prospective append admission; no native launch yet',old_native_and_source_hashes_verified=True,old_source_prefix_and_physical_controls_bitwise=True,query_Gram_op=gram,query_basis_reconstruction_F=basis_error,cached_HQ_outside304_F_Ry=fit,query_singular_min=float(np.linalg.svd(C,compute_uv=False)[-1]),exact_old_ELF_reused=True,physical_input_equal_except_owned_paths=True,socket_bytes=len(address.encode()),disposable_bind_connect=True,admission=admit,host_available_B=mem,disk_available_B=storage['available_bytes'],fixed_prepared_charge_B=fixed_charge,native_rank_extents=extents,forecast_memory_B_NOT_bound=forecast,forecast_wall_s_NOT_bound=timing,old_registry_sha256=sha(r.REGISTRY))
    r.atomic_json(r.HERE/'preflight.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':prepare()
