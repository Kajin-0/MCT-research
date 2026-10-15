"""Finite preflight only; never launches a service or MPI."""
import ast,sys,json,os,socket,subprocess,re
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run_pilot_fixed as r,preflight
from address_admission import checked_address,refuse_reuse

def main():
    for f in HERE.glob('*.py'):ast.parse(f.read_text())
    qe=r.DFT/'.local/qe75_lowram_20261011/q-e'
    fft=(qe/'PW/src/allocate_fft.f90').read_text()
    assert 'CALL create_scf_type( vnew' in fft and 'CALL create_scf_type( v,' in fft
    s=(qe/'PW/src/scf_mod.f90').read_text()
    assert re.search(r'ALLOCATE\( rho%of_r\(dfftp%nnr,nspin\) \)',s)
    src=Path(json.loads((HERE/'build_results.json').read_text())['binary']).parent/'source'
    e=(src/'electrons.f90').read_text()
    assert e.index('conv_elec=.FALSE. ! exhausted8 budget')<e.index('IF(iter.ge.nexxiter) conv_elec=.TRUE.')
    assert "9101 FORMAT(/'     EXX self-consistency reached' )" in e
    assert 'EXX self-consistency reached' in (HERE/'packets.py').read_text()
    parent=Path('/sys/fs/cgroup/user.slice/user-1001.slice/user@1001.service')
    assert 'cpu' in (parent/'cgroup.controllers').read_text().split()
    assert 'cpu' in (parent/'cgroup.subtree_control').read_text().split()
    assert not r.PAIR.exists()
    for m in ['host','cd']:assert len(os.fsencode(checked_address(r.PAIR/m)))<=107
    preflight.main()
    binds={}
    for m in ['host','cd']:
        profile,job,root=r.load(m);refuse_reuse(root);addr=checked_address(root)
        assert not os.path.lexists(addr)
        sock=socket.socket(socket.AF_UNIX);sock.bind(addr);before=os.lstat(addr)
        sock.close();after=os.lstat(addr)
        assert(before.st_dev,before.st_ino)==(after.st_dev,after.st_ino)
        os.unlink(addr)
        v=subprocess.run(['/usr/bin/systemctl','--user','show',job['unit'],'--property=LoadState','--value'],env=r.manager_env(),capture_output=True,text=True)
        assert v.stdout.strip()=='not-found'
        oldroot=r.DFT/'.local/qe75_lowram_20261011/h8r_20261015/p1'/m
        old=(oldroot/'pw.in').read_text();new=(root/'pw.in').read_text()
        old=old.replace(str(oldroot),'ROOT').replace('max_seconds=500','max_seconds=1700').replace('exx_maxstep=2','exx_maxstep=8')
        assert old==new.replace(str(root),'ROOT')
        binds[m]=dict(bytes=len(os.fsencode(addr)),bound_and_identity_safe_removed=True,fresh_unit=job['unit'],input_exact_except_paths_outer_budget_deadline=True)
    result=dict(timestamp_UTC=datetime.now(timezone.utc).isoformat(),source_layout_checks=True,cpu_controller_available=True,binds=binds,all_pins_verified=True,native_executed=False,original_600s_protocol_unmodified=True,extended_deadline_justification='preregistration.md',prelaunch_source_check_correction='initial spacing-only assertion refused before root creation; corrected against actual create_scf_type allocation')
    (HERE/'launch_admission.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
