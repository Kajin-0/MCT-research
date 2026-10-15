"""Fresh fixed PBE16 decks, geometric proof, source pins; no native launch."""
from pathlib import Path
from datetime import datetime,timezone
import fcntl,itertools,json,subprocess,sys,uuid
import numpy as np
import run_pair as r
from science import Q,original


def prepare():
    if r.PAIR.exists() or (r.HERE/'frozen_protocol.json').exists():raise FileExistsError('no reused acquisition')
    previous=json.loads((r.HERE.parent/'symmetry_constructor_2026-10-15/protected_after.json').read_text())
    assert subprocess.check_output(['git','-C',str(r.DFT),'rev-parse','HEAD'],text=True).strip()==previous['DFT_HEAD']
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==previous['DFT_status']
    assert r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==previous['DFT_tracked_diff_sha256']
    for name,h in previous['files'].items():assert r.sha(name)==h
    lock=r.os.open(r.LOCK,r.os.O_RDONLY|r.os.O_CLOEXEC)
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:r.os.close(lock)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    for name in ['pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True)
        assert v.returncode==1 and not v.stdout
    # Full conventional composition motifs in the doubled FCC cell.
    hg=np.array(list(itertools.product([0.,.5],repeat=3)))
    te=hg+.125;xyz=np.r_[hg,te]
    cart=xyz@Q;ops=original.td_operations()
    for member in ['host','cd']:
        symbols=['Hg']*8+['Te']*8
        if member=='cd':symbols[0]='Cd'
        atoms={(s,tuple(np.rint(v*8).astype(int)%8)) for s,v in zip(symbols,xyz)}
        for op in ops:
            mapped=cart@op['spatial'].T@np.linalg.inv(Q)
            assert np.max(abs(mapped*8-np.rint(mapped*8)))<1e-12
            assert {(s,tuple(v%8)) for s,v in zip(symbols,np.rint(mapped*8).astype(int))}==atoms
    # Nearest cation shell exactly4 at a*sqrt(3)/4; count Cd neighbors.
    environments={}
    for member in ['host','cd']:
        counts=[]
        for a in te:
            neighbors=[]
            for i,h in enumerate(hg):
                for shift in itertools.product([-1,0,1],repeat=3):
                    dist=np.linalg.norm((h+shift-a)@Q)
                    if abs(dist-np.sqrt(3)/4)<1e-12:neighbors.append(i)
            assert len(neighbors)==4
            counts.append(sum(member=='cd' and i==0 for i in neighbors))
        environments[member]=counts
    assert sorted(environments['cd'])==[0,0,0,0,1,1,1,1]
    r.PAIR.mkdir(mode=0o700)
    pps=[r.DFT/('pseudopotentials/'+s+'_sg15_pbe_fr_v12.UPF') for s in ['Hg','Cd','Te']]
    for member in ['host','cd']:
        root=r.PAIR/member;root.mkdir(mode=0o700)
        for name in ['out','tmp','pp']:(root/name).mkdir(mode=0o700)
        for pp in pps:(root/'pp'/pp.name).write_bytes(pp.read_bytes())
        r.checked_address(root);r.refuse_reuse(root)
        text=f"""&CONTROL
 calculation='scf', prefix='r07pbe', outdir='{root}/out',
 pseudo_dir='{root}/pp', verbosity='high', disk_io='low', max_seconds=840,
/
&SYSTEM
 ibrav=0, nat=16, ntyp=3, nbnd=352, ecutwfc=50, ecutrho=200,
 occupations='smearing', smearing='fd', degauss=0.001,
 noncolin=.true., lspinorb=.true., nosym=.false., input_dft='PBE',
/
&ELECTRONS
 conv_thr=1d-9, mixing_beta=0.3, electron_maxstep=100,
 diagonalization='david', diago_full_acc=.true.,
 startingpot='atomic', startingwfc='atomic+random',
/
ATOMIC_SPECIES
Hg 200.59 Hg_sg15_pbe_fr_v12.UPF
Cd 112.411 Cd_sg15_pbe_fr_v12.UPF
Te 127.60 Te_sg15_pbe_fr_v12.UPF
CELL_PARAMETERS angstrom
0 6.46 6.46
6.46 0 6.46
6.46 6.46 0
ATOMIC_POSITIONS crystal
"""
        for i,v in enumerate(xyz):
            sym=('Cd' if member=='cd' and i==0 else 'Hg') if i<8 else 'Te'
            text+=sym+' '+' '.join(format(x,'.8f') for x in v)+'\n'
        text+='K_POINTS automatic\n1 1 1 0 0 0\n'
        (root/'pw.in').write_text(text)
    pins=[r.QE,r.MPI,Path(sys.executable).resolve(),r.LIB,*r.HERE.glob('*.py'),r.HERE/'preregistration.md']
    pins+=[r.BASE/'terminal_owner_2026-10-14'/n for n in ['retirement.py','sampled_output.py']]
    pins+=[r.BASE/'runtime_admission'/n for n in ['process_identity.py','family_runtime.py']]
    pins+=[r.BASE/'cgroup_owned_2026-10-13/contracts.py',r.BASE/'checkpoint_phase/resource_guard.py']
    pins+=[r.PAIR/m/'pw.in' for m in ['host','cd']]
    pins+=[r.PAIR/m/'pp'/pp.name for m in ['host','cd'] for pp in pps]
    pins+=[original.HERE/'analyze.py',original.HERE/'numerical_result.json',original.PAIR/'host/out/r07pbe.save/wfc1.hdf5',original.PAIR/'host/out/r07pbe.save/data-file-schema.xml',r.DFT/'src/mct_dft/qe_wavefunctions.py',r.HERE.parent/'native_matched_pilot_2026-10-11/reference_irrep_check.py']
    profile=dict(kind='R07_PBE16_ORDERED_X0125_FD_V1',physical=dict(nat=16,nbnd=352,nelec=288,ecutwfc_Ry=50,ecutrho_Ry=200,sigma_Ry=.001,functional='PBE+SOC',lattice_A=6.46,repeat=Q.tolist(),kgrid=[1,1,1]),limits=dict(memory=12*r.GIB,swap=0,tasks=12,wall=900,host_available=4*r.GIB,free_disk=10*r.GIB,aggregate_output=14*r.GIB,file=r.GIB,escrow=64*(1<<20)),pins={str(p):r.sha(p) for p in pins},ranks=2,hostwide_exclusion=False,private_network_proof=False)
    r.atomic_json(r.PAIR/'PROFILE.json',profile)
    for m in ['host','cd']:
        job=dict(kind=profile['kind'],root=str(r.PAIR/m),member=m,unit='r07-owned-'+uuid.uuid4().hex+'.service',nonce=uuid.uuid4().hex,profile_sha256=r.digest(profile))
        r.atomic_json(r.PAIR/m/'JOB.json',job)
    r.atomic_json(r.HERE/'frozen_protocol.json',dict(profile=profile,jobs={m:json.loads((r.PAIR/m/'JOB.json').read_text()) for m in ['host','cd']}))
    for m in ['host','cd']:r.load(m)
    storage=r.LinuxGuard(r.LIB).probe(r.PAIR);mem=r.memory()['MemAvailable']
    admitted=r.admission(storage,[64*2**20,64*2**20],14*2**30,mem)
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),geometric_Td_operations_verified=24,Te_Cd_nearest_neighbor_counts=environments,socket_bytes={m:len(r.checked_address(r.PAIR/m).encode()) for m in ['host','cd']},available_RAM_B=mem,storage=storage,admission=admitted,legacy_registry_sha256=r.sha(r.REGISTRY),hostwide_absence_claim=False,stock_sha256=r.sha(r.QE),no_completion_guarantee=True)
    r.atomic_json(r.HERE/'protected_before.json',previous);r.atomic_json(r.HERE/'preflight.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':prepare()
