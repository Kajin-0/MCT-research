"""Bounded scientific mesh/pin/resource admission; prepare once, never launch."""
from pathlib import Path
from datetime import datetime,timezone
import fcntl
import itertools
import json
import re
import subprocess
import numpy as np
import run_k3 as r
import analyze_k3 as a

HERE=Path(__file__).resolve().parent


def prove_mesh():
    ops=a.old.td_operations();assert len(ops)==24
    xyz=np.array([[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0],[.25,.25,.25],[.25,.75,.75],[.75,.25,.75],[.75,.75,.25]])
    for member in ['host','cd']:
        symbols=['Hg']*4+['Te']*4
        if member=='cd':symbols[0]='Cd'
        atoms={(symbols[i],tuple(np.rint(xyz[i]*4).astype(int)%4)) for i in range(8)}
        for op in ops:
            mapped=np.rint((xyz@op['spatial'].T)*4).astype(int)%4
            assert {(symbols[i],tuple(mapped[i])) for i in range(8)}==atoms
    points=list(itertools.product(range(3),repeat=3));stars={}
    for point in points:
        orbit={tuple((sign*np.array(point)@op['spatial'].T).astype(int)%3) for op in ops for sign in [-1,1]}
        stars[min(orbit)]=len(orbit)
    assert sorted(stars.values())==[1,6,8,12] and sum(stars.values())==27
    weights={(0,0,0):1/27,(0,0,1):6/27,(0,1,1):12/27,(1,1,1):8/27}
    # No-TR counterexample: the last star splits4+4; don't infer TR fromTd.
    withoutTR={}
    for point in points:
        orbit={tuple((np.array(point)@op['spatial'].T).astype(int)%3) for op in ops}
        withoutTR[min(orbit)]=len(orbit)
    assert sorted(withoutTR.values())==[1,4,4,6,12]
    return dict(full_points=27,Td_operations=24,atoms_both_invariant=True,star_sizes=sorted(stars.values()),
        expected_weights={str(k):v for k,v in weights.items()},without_TR_star_sizes=sorted(withoutTR.values()),TR_is_required=True)


def evaluate():
    if r.PAIR.exists() or (HERE/'preflight.json').exists():raise FileExistsError('no reused pair or preflight overwrite')
    assert subprocess.check_output(['git','-C',str(HERE.parents[3]),'rev-parse','--short','HEAD'],text=True).strip()=='3fe5ef2'
    original=json.loads((a.CUT/'protected_after.json').read_text());before=dict(original,MCT_parent='3fe5ef2')
    assert subprocess.check_output(['git','-C',str(r.DFT),'rev-parse','HEAD'],text=True).strip()==before['DFT_HEAD']
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==before['DFT_status']
    assert r.hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==before['DFT_tracked_diff_sha256']
    for name,h in before['files'].items():assert r.sha(name)==h
    mesh=prove_mesh()
    fd=r.os.open(r.LOCK,r.os.O_RDONLY|r.os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:r.os.close(fd)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    visible={}
    for name in ['pw.x','mpirun','prterun']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True)
        assert v.returncode==1 and not v.stdout
        visible[name]=[]
    r.PAIR.mkdir(mode=0o700)
    r.prepare()
    for member in ['host','cd']:
        old=r.DFT/'.local/qe75_lowram_20261011/chemical_pbe8_k2_e50_20261014'/member/'pw.in'
        new=r.PAIR/member/'pw.in'
        normalize=lambda s:re.sub(r"(?:outdir|pseudo_dir)='[^']+'",'private_path',s)
        assert normalize(new.read_text())==normalize(old.read_text().replace('2 2 2 0 0 0','3 3 3 0 0 0'))
        r.load(member)
    storage=r.LinuxGuard(r.LIB).probe(r.PAIR);mem=r.memory()['MemAvailable']
    admit=r.admission(storage,[64*2**20,64*2**20],14*2**30,mem)
    oldstats=json.loads((a.CUT/'cutoff_result.json').read_text())['members']
    maxkernel=max(v['guard']['peak_kernel_memory_B'] for v in oldstats.values())
    assert 4*maxkernel<12*2**30
    assert all(2*v['guard']['elapsed_s']<500 for v in oldstats.values())
    source=r.DFT/'.local/qe75_lowram_20261011/q-e/PW/src/setup.f90'
    text=source.read_text();assert 'magnetic_sym = noncolin .AND. domag' in text and 'time_reversal = .NOT. noinv .AND. .NOT. magnetic_sym' in text
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='3fe5ef2',mesh=mesh,visible_native_names_empty=visible,
        hostwide_absence_claim=False,exclusive_known_lock_available=True,old_registry=ledger,old_registry_sha256=r.sha(r.REGISTRY),
        physical_RAM_available_B=mem,storage=storage,admission=admit,only_input_grid_and_private_paths_changed=True,
        conservative_4x_previous_kernel_B=4*maxkernel,two_times_previous_member_elapsed_s={m:2*v['guard']['elapsed_s'] for m,v in oldstats.items()},
        not_a_convergence_guarantee=True,Td_TR_source_path=str(source),Td_TR_source_sha256=r.sha(source))
    (HERE/'protected_before.json').write_text(json.dumps(before,indent=2)+'\n')
    (HERE/'preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(mesh=mesh,available_RAM=mem,free_disk=storage['available_bytes'],admission=admit),indent=2))


if __name__=='__main__':evaluate()
