"""Exact source/input/reference/known-owner/resource admission; no QE launch."""
from pathlib import Path
from datetime import datetime,timezone
import fcntl
import hashlib
import json
import re
import subprocess
import numpy as np
import run_pilot_fixed as r
from packets import Reader

HERE=Path(__file__).resolve().parent


def main():
    if r.PAIR.exists():raise FileExistsError('no reused science state')
    build=json.loads((HERE/'build_results.json').read_text());assert build['passed'] and not build['native_executed']
    assert r.sha(build['binary'])==build['binary_sha256']
    for name,h in {**build['source_pins'],**build['backends']}.items():assert r.sha(name)==h
    assert r.sha(r.DFT/'.local/qe-env/lib/libqe_pw.a')==build['stock_archive_sha256']
    old=json.loads((HERE.parent/'chemical_k3_2026-10-14/protected_after.json').read_text());before=dict(old,MCT_parent='04d767c')
    assert subprocess.check_output(['git','-C',str(r.DFT),'rev-parse','HEAD'],text=True).strip()==before['DFT_HEAD']
    assert subprocess.check_output(['git','-C',str(r.DFT),'status','--short'],text=True)==before['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','-C',str(r.DFT),'diff','--binary'])).hexdigest()==before['DFT_tracked_diff_sha256']
    for name,h in before['files'].items():assert r.sha(name)==h
    fd=r.os.open(r.LOCK,r.os.O_RDONLY|r.os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:r.os.close(fd)
    ledger=json.loads(r.REGISTRY.read_text());assert ledger['phase']=='FINISHED' and ledger['members']==[]
    for name in ['pw.x','mpirun','prterun','pw.hse8.firstace']:
        v=subprocess.run(['pgrep','-a','-x',name],capture_output=True,text=True);assert v.returncode==1 and not v.stdout
    r.PAIR.mkdir(mode=0o700);r.prepare()
    for member in ['host','cd']:
        r.load(member);root=r.PAIR/member
        f=Reader(root/'reference.bin');header=f.take('<i8',(4,));assert tuple(header)==(70251406,7809,6,1)
        B=f.take('<f8',(3,3));k=f.take('<f8',(3,));G=f.take('<i8',(3,7809));C=f.take('<c16',(15618,6));f.end()
        assert len(set(map(tuple,G.T)))==7809 and max(abs(k))==0 and np.linalg.norm(C.conj().T@C-np.eye(6),2)<1e-8
        t=(root/'pw.in').read_text();assert "input_dft='HSE'" in t and '1 1 1 0 0 0' in t and 'adaptive_thr=.false.' in t and 'exx_maxstep=8' in t
    assert (r.PAIR/'host/reference.bin').read_bytes()==(r.PAIR/'cd/reference.bin').read_bytes()
    # Native observer counts and original arithmetic evidence are tied to actualsource.
    src=Path(build['binary']).parent/'source';electrons=(src/'electrons.f90').read_text();run=(src/'run_pwscf.f90').read_text()
    assert electrons.count('CALL pilot_finish(exxen,fock2,etot)')==2 and electrons.count('CALL pilot_begin()')==2 and 'conv_elec=.FALSE.' in electrons
    assert "CALL punch('all')\n        CALL pilot_publish()" in run
    assert 'conv_elec=.TRUE.' not in run[run.index('IF(pilot_done)THEN'):run.index('IF(pilot_done)THEN')+280]
    storage=r.LinuxGuard(r.LIB).probe(r.PAIR);mem=r.memory()['MemAvailable']
    admitted=r.admission(storage,[64*2**20]*2,14*2**30,mem)
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),parent='04d767c',admission=admitted,storage=storage,
        available_RAM_B=mem,known_lock_available=True,old_registry=ledger,old_registry_sha256=r.sha(r.REGISTRY),
        visible_native_names_empty=True,hostwide_absence_claim=False,reference_exact_both_members=True,
        source_arithmetic_unchanged=build['arithmetic_byte_unchanged'],unchanged_static_matcalc_library=True,
        diagnostic_stop_does_not_set_HSE_convergence=True,binary_sha256=build['binary_sha256'],
        estimated_subtotal_is_not_bound=True,timing_estimate_is_not_bound=True,output_per_packet_source_payload_upper_B=2*10827*176*16*2+176*176*16+1*2**20,
        XML_numeric_export_tolerance_Ry=2e-14,wave_rho_packet_readback_is_byte_exact=True)
    (HERE/'protected_before.json').write_text(json.dumps(before,indent=2)+'\n')
    (HERE/'preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(admitted=admitted,RAM=mem,disk=storage['available_bytes'],reference_Gram=float(np.linalg.norm(C.conj().T@C-np.eye(6),2)),native_executed=False),indent=2))


if __name__=='__main__':main()
