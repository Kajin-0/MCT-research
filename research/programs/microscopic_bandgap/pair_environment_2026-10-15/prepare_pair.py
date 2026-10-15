"""Freeze exactly two fresh, same-composition stock-QE configurations."""
from pathlib import Path
import fcntl,json,os,socket,subprocess,sys,uuid
import owner as r
from geometry import compute,symbols


def protected():
    previous=json.loads((r.HERE.parent/'chemical_pbe16_p2_2026-10-15/protected_before.json').read_text())
    now=dict(DFT_HEAD=subprocess.check_output(['git','-C',str(r.DFT),'rev-parse','HEAD'],text=True).strip(),DFT_status=subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True),DFT_tracked_diff_sha256=r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest(),files={p:r.sha(p) for p in previous['files']})
    for k in now:assert now[k]==previous[k],('protected DFT changed',k)
    return now


def prepare():
    assert subprocess.check_output(['git','-C',str(r.HERE),'rev-parse','--short','HEAD'],text=True).strip()=='892079f'
    if r.PAIR.exists():raise FileExistsError('fresh acquisition only')
    before=protected()
    h=json.loads((r.HERE.parent/'chemical_pbe16_p2_2026-10-15/host_readback_v2.json').read_text())
    assert h['scientific_pass'] and h['terminal']['terminal'] and h['guard']['pass_guard']
    assert not r.cgroup_path(h['guard']['cgroup']).exists()
    for path,pin in h['source_hashes'].items():assert r.sha(path)==pin
    for name in ['pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    fd=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(fd)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    geometry=compute();r.atomic_json(r.HERE/'geometry_result.json',geometry)
    r.atomic_json(r.HERE/'protected_before.json',before)
    r.PAIR.mkdir(mode=0o700);addresses={};pins=[]
    template=(r.HOST/'pw.in').read_text()
    for member in ['unshared','shared']:
        root=r.PAIR/member;root.mkdir(mode=0o700)
        for n in ['out','tmp','pp']:(root/n).mkdir(mode=0o700)
        for pp in (r.HOST/'pp').iterdir():(root/'pp'/pp.name).write_bytes(pp.read_bytes())
        text=template.replace(str(r.HOST),str(root)).replace('max_seconds=840','max_seconds=540')
        lines=text.splitlines();i=lines.index('ATOMIC_POSITIONS crystal')+1
        for j,s in enumerate(symbols(member)):
            fields=lines[i+j].split();lines[i+j]=' '.join([s]+fields[1:])
        text='\n'.join(lines)+'\n';(root/'pw.in').write_text(text)
        address=r.checked_address(root);r.refuse_reuse(root)
        server=socket.socket(socket.AF_UNIX);client=socket.socket(socket.AF_UNIX)
        try:
            server.bind(address);inode=Path(address).lstat().st_ino;server.listen(1)
            client.connect(address);peer,_=server.accept();peer.close()
            assert r.Account.permitted(type('A',(),{'root':root})(),Path(address),'socket')
        finally:
            client.close();server.close()
            if Path(address).exists() and Path(address).lstat().st_ino==inode:Path(address).unlink()
        addresses[member]=dict(bytes=len(address.encode()),live_bind_connect_pass=True,fresh_no_state=True)
        pins += [root/'pw.in',*list((root/'pp').iterdir())]
    old=json.loads((r.HERE.parent/'chemical_pbe16_p2_2026-10-15/frozen_cd_protocol.json').read_text())['profile']
    pins += [Path(p) for p in old['pins']]+[Path(p) for p in h['source_hashes']]
    pins += [r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*[r.HERE/n for n in ['owner.py','prepare_pair.py','geometry.py','environment_science.py','environment_resource_guard.py','address_admission.py','preregistration.md','geometry_result.json','protected_before.json']]]
    limits=dict(old['limits'],wall=600)
    profile=dict(kind='R07_PBE16_SAME_COMPOSITION_ORDERED_ENVIRONMENT_V1',pins={str(p):r.sha(p) for p in pins},physical=dict(old['physical'],Cd_indices_0based={'unshared':[0,7],'shared':[0,1]},conv_thr_Ry=1e-9),limits=limits,ranks=2,hostwide_exclusion=False,private_network_proof=False,reference_frame='accepted16atom50Ry native host Gamma6/Gamma8')
    r.atomic_json(r.PAIR/'PROFILE.json',profile);jobs={}
    for member in ['unshared','shared']:
        root=r.PAIR/member;job=dict(kind=profile['kind'],root=str(root),member=member,unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
        r.atomic_json(root/'JOB.json',job);jobs[member]=job
    r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs=jobs))
    for member in jobs:r.load(member)
    storage=r.LinuxGuard(r.LIB).probe(r.PAIR/'unshared');mem=r.memory()['MemAvailable']
    admitted=r.admission(storage,[64*2**20],14*2**30,mem)
    r.atomic_json(r.HERE/'preflight.json',dict(admission=admitted,host_available_B=mem,disk_available_B=storage['available_bytes'],socket_checks=addresses,protected_DFT_pass=True,prior_host_wall_s=h['guard']['elapsed_s'],prior_host_peak_kernel_B=h['guard']['peak_kernel_memory_B'],native_not_yet_launched=True))
    print(json.dumps(dict(admitted=admitted,socket_checks=addresses,host_available_B=mem,disk_available_B=storage['available_bytes']),indent=2))


if __name__=='__main__':prepare()
