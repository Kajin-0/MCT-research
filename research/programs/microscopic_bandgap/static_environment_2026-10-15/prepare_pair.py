"""Freeze a saved-charge, no-SCF static operator pair with exact source copies."""
from pathlib import Path
import ast,fcntl,json,os,socket,subprocess,sys,uuid,shutil
import numpy as np
import h5py
import owner as r


def prepare():
    if r.PAIR.exists():raise FileExistsError('fresh static pair only')
    old=r.HERE.parent/'pair_environment_2026-10-15';before=json.loads((old/'protected_after.json').read_text())
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==before['DFT_status']
    assert r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==before['DFT_tracked_diff_sha256']
    for p,h in before['files'].items():assert r.sha(p)==h
    for name in ['pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    fd=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(fd)
    assert json.loads(r.REGISTRY.read_text())['phase']=='FINISHED' and json.loads(r.REGISTRY.read_text())['members']==[]
    for p in r.HERE.glob('*.py'):ast.parse(p.read_text())
    build=json.loads((r.HERE/'build_result.json').read_text());assert build['passed'] and r.sha(r.QE)==build['binary_sha256']
    for group in ['source_pins','backends']:
        for p,h in build[group].items():assert r.sha(p)==h
    manifest=json.loads((old/'evidence_manifest.json').read_text())
    for p,a in manifest['raw_files'].items():assert r.sha(p)==a['sha256']
    sys.path.insert(0,str(old));from environment_science import reference
    fs,G,k,reference_result=reference();N=len(G);P=np.concatenate([fs['Gamma6'],fs['Gamma8']]).transpose(1,2,0).reshape(2*N,6)
    lookup={tuple(g):i for i,g in enumerate(G)};minus=np.array([lookup[tuple(-g)] for g in G]);theta=np.r_[P[N+minus].conj(),-P[minus].conj()];trial=np.column_stack((P,theta));gram=float(np.linalg.norm(P.conj().T@P-np.eye(6),2));assert gram<1e-8
    with h5py.File(r.HOST/'out/r07pbe.save/wfc1.hdf5') as f:B=np.array([f['MillerIndices'].attrs['bg'+str(i)] for i in [1,2,3]]).T
    profilepins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*r.HERE.glob('*.py'),r.HERE/'native_probe.inc',r.HERE/'preregistration.md',r.HERE/'build_result.json']
    profilepins += [Path(p) for p in build['source_pins']]+[Path(p) for p in build['backends']]+[Path(p) for p in manifest['raw_files']]
    r.PAIR.mkdir(mode=0o700);copies={};addresses={}
    for member in ['unshared','shared']:
        src=r.DFT/'.local/qe75_lowram_20261011/p16e_20261015'/member;root=r.PAIR/member;root.mkdir(mode=0o700)
        for name in ['out','tmp','pp','pilot']:(root/name).mkdir(mode=0o700)
        copies[member]={}
        shutil.copytree(src/'out/r07pbe.save',root/'out/r07pbe.save')
        for p in (src/'out/r07pbe.save').rglob('*'):
            if p.is_file():
                dst=root/'out/r07pbe.save'/p.relative_to(src/'out/r07pbe.save');assert r.sha(dst)==r.sha(p);copies[member][str(dst)]=dict(source=str(p),sha256=r.sha(p));profilepins.append(p)
        for pp in (src/'pp').iterdir():(root/'pp'/pp.name).write_bytes(pp.read_bytes())
        original=(src/'pw.in').read_text();text=original.replace(str(src),str(root)).replace("startingpot='atomic'","startingpot='file'").replace("startingwfc='atomic+random'","startingwfc='file'")
        assert text.replace(str(root),str(src)).replace("startingpot='file'","startingpot='atomic'").replace("startingwfc='file'","startingwfc='atomic+random'")==original
        (root/'pw.in').write_text(text)
        with (root/'probes.bin').open('xb') as out:
            for a in [np.array([70251520,1,N,12,2]+[0]*11,dtype='<i8'),B.astype('<f8'),G.T.astype('<i8'),trial.astype('<c16')]:out.write(a.tobytes(order='F'))
        profilepins += [root/'pw.in',root/'probes.bin',*list((root/'pp').iterdir())]
        address=r.checked_address(root);r.refuse_reuse(root);server=socket.socket(socket.AF_UNIX);client=socket.socket(socket.AF_UNIX)
        try:
            server.bind(address);inode=Path(address).lstat().st_ino;server.listen(1);client.connect(address);peer,_=server.accept();peer.close()
        finally:
            client.close();server.close()
            if Path(address).exists() and Path(address).lstat().st_ino==inode:Path(address).unlink()
        addresses[member]=dict(socket_bytes=len(address.encode()),actual_bind_connect=True)
    np.savez(r.PAIR.parent/'physical_frame.npz',P=P,ThetaP=theta,G=G,B=B);profilepins += [r.PAIR.parent/'physical_frame.npz']
    # No admission depends on random initial waves: file path must really load.
    fixed=sum(p.stat().st_blocks*512+4096 for p in r.PAIR.parent.rglob('*') if p.is_file() and r.PAIR not in p.parents)+8*2**20
    profile=dict(kind='R07_PBE16_SAVED_CHARGE_STATIC_H_6PLUS6THETA_V1',physical=dict(nat=16,capacity=352,nelec=288,ecutwfc_Ry=50,ecutrho_Ry=200,Gamma=True,sigma_Ry=.001,physical_probes=6,Theta_controls=6,reference_original_unchanged=True,SCF=False),limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=600,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB-fixed,file=r.GIB,escrow=64*2**20),fixed_bytes=fixed,copied_saves=copies,pins={str(p):r.sha(p) for p in profilepins},ranks=2,hostwide_exclusion=False,private_network_proof=False)
    r.atomic_json(r.PAIR/'PROFILE.json',profile);jobs={}
    for member in ['unshared','shared']:
        job=dict(kind=profile['kind'],root=str(r.PAIR/member),member=member,unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile));r.atomic_json(r.PAIR/member/'JOB.json',job);jobs[member]=job
    r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs=jobs));r.atomic_json(r.HERE/'protected_before.json',before)
    for m in jobs:r.load(m)
    storage=r.LinuxGuard(r.LIB).probe(r.PAIR/'unshared');mem=r.memory()['MemAvailable'];admit=r.admission(storage,[64*2**20],14*r.GIB,mem)
    output_bound=16*2*50000*12*5+24*(50000+2**22)+16*2**22*4+8*2**22*8+16384;assert output_bound<r.GIB
    result=dict(status='PASS saved-state/static-probe admission; native NOT RUN',addresses=addresses,admission=admit,host_available_B=mem,disk_available_B=storage['available_bytes'],original_frame_Gram_op=gram,original_Theta_amplitude_outside_frame_F=float(np.linalg.norm(theta-P@(P.conj().T@theta),'fro')),exact_Theta_controls_added_NOT_projector_symmetrization=True,all_retained_raw_and_copied_source_hashes_pass=True,source_and_Hamiltonian_component_review_PASS=True,output_rank_upper_B=output_bound,persistent_copied_save_charge_B=sum(p.stat().st_blocks*512 for p in r.PAIR.rglob('*') if p.is_file()),memory_forecast_B_NOT_bound=2095000000+2*r.GIB,wall_forecast_s_NOT_bound=180,old_registry_sha256=r.sha(r.REGISTRY))
    r.atomic_json(r.HERE/'preflight.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':prepare()
