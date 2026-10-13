"""Read-only consistency checks. Does not run MPI, probes, services or compilers."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent


def verify():
    b=json.loads((HERE/'harness_build.json').read_text())
    for path,wanted in b['pins'].items():
        p=Path(path)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=wanted:raise RuntimeError('pin changed: '+path)
    assert not b['MPI_Init_executed'] and not b['MPI_job_executed']
    assert b['new_scope']==3 and b['new_wire_magic']=='R07C'
    for name in ['isolation_result.json','isolation_actual_result.json','isolation_diagnostic_result.json']:
        r=json.loads((HERE/name).read_text())
        assert not r['passed'] and not r['native_MPI_launched']
        assert r['unit_unloaded'] and r['legacy_byte_exact']
    r=json.loads((HERE/'isolation_diagnostic_result.json').read_text())
    assert r['exit_status']==91
    assert r['observation']['failed_step']=='self_netns_stat' and r['observation']['errno']==13
    t=json.loads((HERE/'component_results.json').read_text())
    assert t['passed'] and t['methods']==10 and not t['actual_MPI_collectives'] and not t['MPI_Init']
    p=json.loads((HERE/'preservation.json').read_text())
    assert p['passed'] and p['legacy_registry_restored_byte_exact'] and not p['new_MPI_harness_launched']
    assert all(c['LoadState']=='not-found' and c['recorded_pid_absent'] for c in p['new_unit_cleanup_checks'])
    for filename in ['isolation_probe.py','build_harness.py','test_components.py','verify_artifacts.py']:
        compile((HERE/filename).read_text(),str(HERE/filename),'exec')
    # Original gate is intact, not replaced with a local receipt.
    prior=(HERE.parent/'cgroup_owned_2026-10-13/contracts.py').read_text()
    assert "def hostwide_gate(_):raise Refusal" in prior
    result={'passed':True,'pin_count':len(b['pins']),'serial_methods':10,
            'original_hostwide_gate':'UNPASSED_UNCHANGED','MPI_job_executed':False,
            'kind':'READ_ONLY_ARTIFACT_CONSISTENCY_NOT_NEW_MEASUREMENT'}
    return result


if __name__=='__main__':print(json.dumps(verify(),indent=2))
