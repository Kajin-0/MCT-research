"""Freeze one same-D host acquisition only after source/trial/resource checks."""
from pathlib import Path
import ast,fcntl,json,os,socket,subprocess,sys,uuid
import numpy as np
import owner as r


def prepare():
    if r.PAIR.exists():raise FileExistsError('fresh finite acquisition, no retry')
    protected=json.loads((r.HERE.parent/'pair_environment_2026-10-15/protected_after.json').read_text())
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==protected['DFT_status']
    assert r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==protected['DFT_tracked_diff_sha256']
    for path,pin in protected['files'].items():assert r.sha(path)==pin
    for name in ['pw.x','mpirun','prterun']:
        q=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert q.returncode==1 and not q.stdout
    assert json.loads(r.REGISTRY.read_text())['phase']=='FINISHED' and json.loads(r.REGISTRY.read_text())['members']==[]
    lock=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(lock)
    for file in r.HERE.glob('*.py'):ast.parse(file.read_text())
    build=json.loads((r.HERE/'build_results.json').read_text());assert build['passed'] and r.sha(r.QE)==build['binary_sha256']
    tr=json.loads((r.HERE/'trial_result.json').read_text());assert r.sha(tr['trial_path'])==tr['trial_sha256'] and tr['max_density_group_covariance_op']<1e-8
    kval=json.loads((r.HERE/'qualification.json').read_text());assert kval['status'].startswith('PASS')
    for report in [tr,kval]:
        for path,pin in report['source_sha256'].items():assert r.sha(path)==pin
    root=r.PAIR/'host';root.mkdir(parents=True,mode=0o700)
    for name in ['out','tmp','pp','pilot']:(root/name).mkdir(mode=0o700)
    old=r.DFT/'.local/qe75_lowram_20261011/h8s_20261015/p1/host'
    text=(old/'pw.in').read_text().replace(str(old),str(root)).replace('max_seconds=850','max_seconds=540').replace('ace=.true.','ace=.false.')
    assert text.count('ace=.false.')==1;(root/'pw.in').write_text(text)
    for p in (old/'pp').iterdir():(root/'pp'/p.name).write_bytes(p.read_bytes())
    sys.path.insert(0,str(r.HERE.parent/'antiunitary_closure_2026-10-15'));from audit_native import ROOT as prior
    from packets import packet,Reader
    f=np.load(Path(tr['trial_path']));G=f['G'];N=len(G);lookup={tuple(g):i for i,g in enumerate(G)};expected_size={}
    for rank in [0,1]:
        b=packet(prior,'before',rank,1);n,p=b['nnpw'],b['npwx'];active=np.r_[np.arange(n),np.arange(p,p+n)];loc=np.array([lookup[tuple(g)] for g in b['G']]);ix=np.r_[loc,N+loc]
        source=np.zeros((2*p,176),complex);source[active]=f['source'][ix];trial=np.zeros((2*p,164),complex);trial[active]=f['trial'][ix]
        h=np.array([70251510,1,rank,p,n,176,2,164,152,146,142,4,144,0,0,0],dtype='<i8')
        values=[h,b['B'].astype('<f8'),b['k'].astype('<f8'),b['G'].T.astype('<i8'),f['weights'].astype('<f8'),source.astype('<c16'),trial.astype('<c16')]
        path=root/'pilot'/f'input.rank{rank}'
        with path.open('xb') as out:
            for v in values:out.write(v.tobytes(order='F'))
        rr=Reader(path)
        for v in values:np.testing.assert_array_equal(rr.take(v.dtype,v.shape),v)
        rr.end()
        # Worst declared descriptor extents, all matrix/g/rho pieces and padding.
        bound=16*2*p*(176+5*164+6)+24*(n+216000)+16*216000*4+8*216000*8+16384
        assert bound<r.GIB;expected_size[str(rank)]=dict(input_B=path.stat().st_size,native_output_upper_B=bound,npwx=p,nnpw=n)
    address=r.checked_address(root);r.refuse_reuse(root);server=socket.socket(socket.AF_UNIX);client=socket.socket(socket.AF_UNIX)
    try:
        server.bind(address);inode=Path(address).lstat().st_ino;server.listen(1);client.connect(address);peer,_=server.accept();peer.close()
        assert r.Account.permitted(type('A',(),{'root':root})(),Path(address),'socket')
    finally:
        client.close();server.close()
        if Path(address).exists() and Path(address).lstat().st_ino==inode:Path(address).unlink()
    private=r.PAIR.parent
    fixed=[p for p in private.rglob('*') if p.is_file() and r.PAIR not in p.parents]
    fixed_charge=sum(p.stat().st_blocks*512+4096 for p in fixed)+8*2**20
    pins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*r.HERE.glob('*.py'),r.HERE/'preregistration.md',r.HERE/'operator_proof.md',r.HERE/'build_results.json',r.HERE/'trial_result.json',r.HERE/'qualification.json',r.HERE/'probe_native.inc',root/'pw.in',*list((root/'pp').iterdir()),*list((root/'pilot').iterdir()),*fixed]
    pins += [Path(p) for p in build['source_pins']]+[Path(p) for p in build['backends']]+[r.DFT/'.local/qe-env/bin/pw.x']
    for folder,names in [('terminal_owner_2026-10-14',['retirement.py','sampled_output.py']),('runtime_admission',['family_runtime.py','process_identity.py']),('cgroup_owned_2026-10-13',['contracts.py']),('checkpoint_phase',['resource_guard.py'])]:pins += [r.BASE/folder/name for name in names]
    profile=dict(kind='R07_SAME_D_COMPLETE_DIRECT_H_HOST_V1',physical=dict(nat=8,source_buffer=176,natural_source=146,joint_space=152,trials=164,nelec=144,ecutwfc_Ry=50,ecutrho_Ry=200,ecutfock_Ry=200,kgrid=[1,1,1],qgrid=[1,1,1],exx_fraction=.25,screening_Bohr_inverse=.106,sigma_Ry=.001,fixed_trial_NOT_FD=True),limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=600,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB-fixed_charge,file=r.GIB,escrow=64*2**20),fixed_prepared_charge_B=fixed_charge,total_owned_cap_B=14*r.GIB,pins={str(p):r.sha(p) for p in pins},ranks=2,SCF_performed=False,hostwide_exclusion=False,private_network_proof=False)
    job=dict(kind=profile['kind'],root=str(root),member='host',unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
    r.atomic_json(r.PAIR/'PROFILE.json',profile);r.atomic_json(root/'JOB.json',job);r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs=dict(host=job)))
    r.load('host');storage=r.LinuxGuard(r.LIB).probe(root);mem=r.memory()['MemAvailable'];admit=r.admission(storage,[64*2**20],14*r.GIB,mem)
    # Earlier native376x2probe measured4.78GB; new persistent vector columns
    #1002 versus1104 and same FFT/source capacity. Extra guard margin2GiB.
    prior_peak=4780109824;forecast=prior_peak+2*r.GIB;assert forecast<12*r.GIB
    timing_forecast=3*(164+6)*.875+60;assert timing_forecast<600
    preflight=dict(admission=admit,host_available_B=mem,disk_available_B=storage['available_bytes'],socket_bytes=len(address.encode()),actual_bind_connect_pass=True,source_and_input_readback_PASS=True,native_rank_file_extent_upper=expected_size,fixed_prepared_charge_B=fixed_charge,forecast_memory_B_NOT_bound=forecast,forecast_wall_s_NOT_bound=timing_forecast,kernel_caps_are_hard=True,protected_DFT_exact=True,old_registry_sha256=r.sha(r.REGISTRY),no_native_launch_yet=True)
    r.atomic_json(r.HERE/'preflight.json',preflight);print(json.dumps(preflight,indent=2))


if __name__=='__main__':prepare()
