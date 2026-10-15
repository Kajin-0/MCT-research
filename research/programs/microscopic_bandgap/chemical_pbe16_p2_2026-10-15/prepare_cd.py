"""ONE fresh Cd-only acquisition after independently corrected native-unit readback."""
from pathlib import Path
import fcntl,json,socket,subprocess,sys,uuid
import cd_owner as r


def prepare():
    if r.PAIR.exists():raise FileExistsError('fresh Cd acquisition only')
    h=json.loads((r.HERE/'host_readback_v2.json').read_text())
    assert h['scientific_pass'] and h['terminal']['terminal'] and h['guard']['pass_guard']
    assert not r.cgroup_path(h['guard']['cgroup']).exists()
    for path,pin in h['source_hashes'].items():assert r.sha(path)==pin
    previous=json.loads((r.HERE/'protected_before.json').read_text())
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==previous['DFT_status']
    for path,pin in previous['files'].items():assert r.sha(path)==pin
    for name in ['pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    fd=r.os.open(r.LOCK,r.os.O_RDONLY|r.os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:r.os.close(fd)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    r.PAIR.mkdir(mode=0o700);root=r.PAIR/'cd';root.mkdir(mode=0o700)
    for name in ['out','tmp','pp']:(root/name).mkdir(mode=0o700)
    old=r.HOST.parent/'cd'
    for pp in (old/'pp').iterdir():(root/'pp'/pp.name).write_bytes(pp.read_bytes())
    text=(old/'pw.in').read_text().replace(str(old),str(root));(root/'pw.in').write_text(text)
    assert text.replace(str(root),str(old))==(old/'pw.in').read_text()
    address=r.checked_address(root);r.refuse_reuse(root)
    server=socket.socket(socket.AF_UNIX);client=socket.socket(socket.AF_UNIX)
    try:
        server.bind(address);inode=Path(address).lstat().st_ino;server.listen(1)
        client.connect(address);peer,_=server.accept();peer.close()
        assert r.Account.permitted(type('A',(),{'root':root})(),Path(address),'socket')
    finally:
        client.close();server.close()
        if Path(address).exists() and Path(address).lstat().st_ino==inode:Path(address).unlink()
    oldprofile=json.loads((r.HERE/'frozen_protocol.json').read_text())['profile']
    pins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*[r.HERE/n for n in ['cd_owner.py','prepare_cd.py','science_units_v2.py','readback_addendum.md','host_readback_v2.json','preregistration.md','native_resource_guard.py','address_admission.py']],root/'pw.in',*list((root/'pp').iterdir())]
    pins+=[Path(v) for v in oldprofile['pins']]+[Path(v) for v in h['source_hashes']]
    for src in ['PW/src/pw_restart_new.f90','Modules/io_base.f90']:pins.append(r.DFT/'.local/qe75_lowram_20261011/q-e'/src)
    profile=dict(oldprofile,kind='R07_PBE16_CD_ONLY_CORRECT_NATIVE_UNITS_V2',pins={str(p):r.sha(p) for p in pins},retained_host_qualified_readonly=True,no_host_rerun=True,old_readback_assertion_still_failed=True)
    r.atomic_json(r.PAIR/'PROFILE.json',profile)
    job=dict(kind=profile['kind'],root=str(root),member='cd',unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
    r.atomic_json(root/'JOB.json',job);r.atomic_json(r.HERE/'frozen_cd_protocol.json',dict(profile=profile,jobs=dict(cd=job)))
    r.load('cd')
    storage=r.LinuxGuard(r.LIB).probe(root);mem=r.memory()['MemAvailable']
    admitted=r.admission(storage,[64*2**20],14*2**30,mem)
    r.atomic_json(r.HERE/'cd_preflight.json',dict(admission=admitted,host_available_B=mem,disk_available_B=storage['available_bytes'],socket_bytes=len(address.encode()),actual_socket_bind_and_connect_pass=True,retained_host_hashes_checked=True,old_failures_unchanged=True,native_HDF5_reciprocal_units='2pi/bohr',old_host_peak_kernel_B=h['guard']['peak_kernel_memory_B'],old_host_elapsed_s=h['guard']['elapsed_s']))
    print(json.dumps(admitted,indent=2))


if __name__=='__main__':prepare()
