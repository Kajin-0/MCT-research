"""One preflight for the separately frozen fixed-source constructor, no MPI."""
import ast
import fcntl
import hashlib
import json
import os
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import run_probe as r


def main():
    for p in r.HERE.glob('*.py'):ast.parse(p.read_text())
    previous=r.HERE.parent/'exchange_symmetry_2026-10-15'
    protected=json.loads((previous/'protected_after.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.DFT,text=True).strip()==protected['DFT_HEAD']
    assert subprocess.check_output(['git','status','--short'],cwd=r.DFT,text=True)==protected['DFT_status']
    assert hashlib.sha256(subprocess.check_output(['git','diff','--binary'],cwd=r.DFT)).hexdigest()==protected['DFT_tracked_diff_sha256']
    for p,h in protected['files'].items():assert r.sha(p)==h
    old=r.HERE.parent/'hybrid_convergence_2026-10-15'
    assert r.sha(r.REGISTRY)==json.loads((old/'preflight.json').read_text())['old_registry_sha256']
    fd=os.open(r.LOCK,os.O_RDONLY|os.O_CLOEXEC)
    try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    finally:os.close(fd)
    # Native comm names can be truncated to15bytes; do not pgrep an overlong name.
    visible=subprocess.check_output(['ps','-eo','pid=,comm='],text=True)
    for line in visible.splitlines():
        pid,name=line.split(maxsplit=1)
        assert name not in ['pw.x','mpirun','prterun'] and not name.startswith('pw.hse8'),line
    build=json.loads((r.HERE/'build_results.json').read_text());assert build['passed'] and not build['native_executed']
    for p,h in {**build['source_pins'],**build['backends']}.items():assert r.sha(p)==h
    assert r.sha(r.DFT/'.local/qe-env/lib/libqe_pw.a')==build['stock_archive_sha256']
    src=Path(build['binary']).parent/'source'
    run=(src/'run_pwscf.f90').read_text()
    assert run.index('CALL r07_fixed_TR_probe()')<run.index('main_loop: DO')
    assert 'RETURN ! fixed operator only' in run
    native=(r.HERE/'probe_native.inc').read_text()
    assert all(v not in native for v in ['CALL aceinit','CALL electrons','CALL v_of_rho','CALL punch'])
    assert 'DO i=1,nt,176' in native and 'DO source=1,2' in native
    profile,job,root=r.load('host');r.refuse_reuse(root)
    assert profile['limits']['wall']==900 and profile['auxiliary_columns']==364
    addr=r.checked_address(root);assert not os.path.lexists(addr)
    s=socket.socket(socket.AF_UNIX);s.bind(addr);ino=os.lstat(addr);s.close();now=os.lstat(addr)
    assert (ino.st_dev,ino.st_ino)==(now.st_dev,now.st_ino);os.unlink(addr)
    assert subprocess.check_output(['/usr/bin/systemctl','--user','show',job['unit'],'--property=LoadState','--value'],env=r.manager_env(),text=True).strip()=='not-found'
    storage=r.LinuxGuard(r.LIB).probe(root);mem=r.memory()['MemAvailable']
    budget=r.admission(storage,[64*(1<<20)],14*r.GIB,mem)
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),native_executed=False,source_and_backend_pins_pass=True,protected_state_exact=True,
        known_owner_lock_free=True,visible_native_names_absent=True,hostwide_absence_claim=False,
        source_domain_proof='operator_input_proof.md',socket_bytes=len(os.fsencode(addr)),
        socket_actual_bind_and_identity_cleanup=True,fresh_job=job,admission=budget,
        available_RAM_B=mem,disk_available_B=storage['available_bytes'],
        wall_cap_s=900,forecast_s=630,forecast_not_bound=True,
        auxiliary_completion_not_extra_physical_bands=True)
    (r.HERE/'protected_before.json').write_text(json.dumps(protected,indent=2)+'\n')
    (r.HERE/'preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
