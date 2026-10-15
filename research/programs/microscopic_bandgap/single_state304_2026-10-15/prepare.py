"""Freeze one simultaneous304query at the unchanged sourceD0; no old action reuse."""
from pathlib import Path
import ast,fcntl,json,os,socket,subprocess,sys,uuid,shutil,importlib.util
import numpy as np
import owner as r


def prepare():
    if r.PAIR.exists():raise FileExistsError('fresh ONE native attempt only')
    OLD=r.HERE.parent/'same_density_hamiltonian_2026-10-15';src=r.DFT/'.local/qe75_lowram_20261011/h8h_20261015';private=r.PAIR.parent
    protected=json.loads((OLD/'protected_after.json').read_text())
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==protected['DFT_status']
    assert r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==protected['DFT_tracked_diff_sha256']
    for p,h in protected['files'].items():assert r.sha(p)==h
    for name in ['pw.x','pw.static','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    assert json.loads(r.REGISTRY.read_text())['phase']=='FINISHED' and json.loads(r.REGISTRY.read_text())['members']==[]
    lock=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(lock)
    for p in r.HERE.glob('*.py'):ast.parse(p.read_text())
    # Real imports before native launch, not merely syntax/AST.
    import readback
    assert callable(readback.decode) and callable(readback.validate_native)
    build=json.loads((r.HERE/'build_results.json').read_text());assert build['passed'] and r.sha(r.QE)==build['binary_sha256']
    for group in ['source_pins','backends']:
        for p,h in build[group].items():assert r.sha(p)==h
    tr=json.loads((OLD/'trial_result.json').read_text());kr=json.loads((OLD/'krylov_result.json').read_text());assert r.sha(tr['trial_path'])==tr['trial_sha256'] and r.sha(kr['basis_path'])==kr['basis_sha256']
    f=np.load(src/'trial.npz');basis=np.load(src/'full_action_basis.npz');V=basis['Q'];G=f['G'];N=len(G);S=f['source'][:,:146];w=f['weights'][:146]
    assert kr['maximum_all_group_Theta_translation_leakage_F']<1e-8
    gram=float(np.linalg.norm(V.conj().T@V-np.eye(304),2));assert gram<1e-8
    A=V.conj().T@S;D=(A*w)@A.conj().T;outside=float(np.linalg.norm(S-V@A,'fro'));assert outside<1e-8 and abs(np.trace(D).real-144)<1e-8
    trial=np.column_stack((V,f['trial'][:,152:164]));assert trial.shape==(2*N,316)
    bundle=private/'trial.npz';assert not bundle.exists();np.savez(bundle,Q=V,G=G,D_Q=D,source=f['source'],weights=f['weights'],trial=trial,P=f['P'])
    new=np.load(bundle);assert new['source'].tobytes()==f['source'].tobytes() and new['weights'].tobytes()==f['weights'].tobytes() and new['P'].tobytes()==f['P'].tobytes()
    shutil.copy2(src/'expected_density.npz',private/'expected_density.npz')
    spec=importlib.util.spec_from_file_location('r07_old_decoder',OLD/'readback.py');od=importlib.util.module_from_spec(spec);spec.loader.exec_module(od)
    root=r.PAIR/'host';root.mkdir(parents=True,mode=0o700)
    for name in ['out','tmp','pp','pilot']:(root/name).mkdir(mode=0o700)
    prior=src/'p1/host';text=(prior/'pw.in').read_text().replace(str(prior),str(root));assert text.replace(str(root),str(prior))==(prior/'pw.in').read_text();(root/'pw.in').write_text(text)
    for p in (prior/'pp').iterdir():(root/'pp'/p.name).write_bytes(p.read_bytes())
    extents={};lookup={tuple(g):i for i,g in enumerate(G)}
    for rank in [0,1]:
        b=od.decode(prior/'pilot'/f'H.rank{rank}');p,n,ng,nr,ns,nkb,nhm=map(int,b['h'][[4,5,8,9,10,11,12]]);i=np.array([lookup[tuple(g)] for g in b['G']]);j=np.r_[i,N+i];active=np.r_[np.arange(n),np.arange(p,p+n)]
        source=np.zeros((2*p,176),complex);source[active]=f['source'][j];query=np.zeros((2*p,316),complex);query[active]=trial[j]
        values=[np.array([70251540,2,rank,p,n,176,2,316,304,146,142,4,144,0,0,0],dtype='<i8'),b['B'].astype('<f8'),b['k'].astype('<f8'),b['G'].T.astype('<i8'),f['weights'].astype('<f8'),source.astype('<c16'),query.astype('<c16')]
        path=root/'pilot'/f'input.rank{rank}'
        with path.open('xb') as out:
            for a in values:out.write(a.tobytes(order='F'))
        rr=readback.Reader(path)
        for a in values:assert rr.take(a.dtype,a.shape).tobytes()==a.tobytes()
        rr.end()
        # Exxbuff snapshot size uses active146 source columns only; no duplicate RAM.
        ngt=int(b['fft'][12,2]);nrxx=int(b['dims'][0]//2);assert nrxx<=216000
        snapshot_bound=128+1024+16*ng*4+8*nr*4+8*ns*4+16*p*nkb+16*nhm*nhm*8*4+8*176+8*216000+16*2*nrxx*146
        output_bound=16*2*p*(176+5*316+6)+24*(n+216000)+16*216000*4+8*216000*8+16384
        assert max(snapshot_bound,output_bound)<r.GIB
        extents[str(rank)]=dict(npwx=p,nnpw=n,nkb=nkb,nhm=nhm,input_B=path.stat().st_size,action_file_upper_B=output_bound,EACH_snapshot_file_upper_B=snapshot_bound)
    address=r.checked_address(root);r.refuse_reuse(root);server=socket.socket(socket.AF_UNIX);client=socket.socket(socket.AF_UNIX)
    try:
        server.bind(address);inode=Path(address).lstat().st_ino;server.listen(1);client.connect(address);peer,_=server.accept();peer.close()
    finally:
        client.close();server.close()
        if Path(address).exists() and Path(address).lstat().st_ino==inode:Path(address).unlink()
    fixed=[p for p in private.rglob('*') if p.is_file() and r.PAIR not in p.parents];fixed_charge=sum(p.stat().st_blocks*512+4096 for p in fixed)+8*2**20
    pins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*r.HERE.glob('*.py'),r.HERE/'probe_native.inc',r.HERE/'preregistration.md',r.HERE/'operator_proof.md',r.HERE/'build_results.json',root/'pw.in',*list((root/'pp').iterdir()),*list((root/'pilot').iterdir()),*fixed,src/'trial.npz',src/'full_action_basis.npz',src/'expected_density.npz',OLD/'trial_result.json',OLD/'krylov_result.json',OLD/'readback.py']
    pins += [Path(p) for p in build['source_pins']]+[Path(p) for p in build['backends']]+[r.DFT/'.local/qe-env/bin/pw.x']
    for folder,names in [('terminal_owner_2026-10-14',['retirement.py','sampled_output.py']),('runtime_admission',['family_runtime.py','process_identity.py']),('cgroup_owned_2026-10-13',['contracts.py']),('checkpoint_phase',['resource_guard.py'])]:pins += [r.BASE/folder/name for name in names]
    profile=dict(kind='R07_SINGLE_NATIVE_STATE304_HSE_D0_V1',physical=dict(nat=8,source_capacity176=True,nelec=144,joint_queries=304,physical_Theta_controls=12,application_blocks=[158,158],no_cross_run_action_reuse=True,physics_identical_to_accepted_D0=True),limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=600,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB-fixed_charge,file=r.GIB,escrow=64*2**20),fixed_prepared_charge_B=fixed_charge,total_owned_cap_B=14*r.GIB,pins={str(p):r.sha(p) for p in pins},ranks=2,SCF_performed=False,hostwide_exclusion=False,private_network_proof=False)
    job=dict(kind=profile['kind'],root=str(root),member='host',unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile));r.atomic_json(r.PAIR/'PROFILE.json',profile);r.atomic_json(root/'JOB.json',job);r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs=dict(host=job)));r.load('host')
    storage=r.LinuxGuard(r.LIB).probe(root);mem=r.memory()['MemAvailable'];admit=r.admission(storage,[64*2**20],14*r.GIB,mem)
    extra=5*2*10827*(316-164)*16;forecast=4245749760+extra+2*r.GIB;wall=322/170*185.303861+60;assert forecast<12*r.GIB and wall<600
    result=dict(status='PASS prospective single-state304admission; nativeNOTRUN',source_trialD0_bytes_unchanged=True,old304basis_SHA_pass=True,query_Gram_op=gram,source_outside304_F=outside,Reader_and_owner_actual_import_PASS=True,source_build_arithmetic_PASS=True,unsafe_m316_direct_call_REJECTED=True,two158calls_same_frozen_operator=True,socket_bytes=len(address.encode()),actual_bind_connect_pass=True,admission=admit,host_available_B=mem,disk_available_B=storage['available_bytes'],rank_extents=extents,fixed_prepared_charge_B=fixed_charge,forecast_family_memory_B_NOT_bound=forecast,forecast_wall_s_NOT_bound=wall,hard_cgroup_caps=True,old_registry_sha256=r.sha(r.REGISTRY),protected_DFT_exact=True)
    r.atomic_json(r.HERE/'preflight.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':prepare()
