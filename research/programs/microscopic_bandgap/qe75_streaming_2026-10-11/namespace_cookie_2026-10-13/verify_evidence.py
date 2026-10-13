"""Read-only evidence consistency/pins; no service, MPI, QE or compiler."""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent


def check():
    build=json.loads((HERE/'build.json').read_text())
    private=Path('/home/User/opencode_workspace/DFT/.local/qe75_lowram_20261011/namespace_cookie_20261013')
    assert hashlib.sha256((HERE/'cookie_probe.c').read_bytes()).hexdigest()==build['source_sha256']
    assert hashlib.sha256((private/'cookie_probe.v1').read_bytes()).hexdigest()==build['binary_sha256']
    assert not build['MPI_linked']
    r=json.loads((HERE/'normal_result.json').read_text());h=r['hello'];k=r['kernel_at_hello']
    assert not r['passed'] and r['reason']=='Refusal: namespace cookie comparison'
    assert h['cookies']==r['host_fresh_before']==r['host_fresh_after']==[1]*3
    assert h['interfaces']==5 and h['nonlo_entries']>0 and h['bad_addresses']>0
    assert h['ns_stat_errno']==13 and h['exe_stat_errno']==0
    assert r['parent_image_path_verified'] and r['manager_live']['MainPID']==str(h['pid'])
    assert r['manager_live']['InvocationID']==h['invocation']
    assert r['manager_live']['PrivateNetwork']=='yes' and r['manager_live']['PrivateUsers']=='yes'
    assert k['memory_max']=='67108864' and k['swap_max']=='0' and k['tasks_max']=='4' and k['oom_group']=='1'
    assert r['reservation']['requested']==4096 and r['reservation']['allocated']>=4096
    assert r['unit_unloaded'] and r['legacy_byte_exact'] and r['flock_retained_after_peer']
    assert r['terminal_manager']['ExecMainStatus']=='94' and not r['native_MPI_QE_HSE_executed']
    journal=json.loads((HERE/'owned_unit_journal.json').read_text())
    assert journal['returncode']==0 and 'proceeding without' in journal['stdout']
    assert json.loads((HERE/'independent_host_interfaces.json').read_text())['fresh_host_cookie']==1
    for name,count in [('validation_tests.json',7),('resource_tests.json',5),('replay_tests.json',1)]:
        t=json.loads((HERE/name).read_text());assert t['passed'] and t['methods']==count and not t['MPI_QE_executed']
    c=json.loads((HERE/'closure.json').read_text());assert c['recorded_PID_absent'] and c['LoadState']=='not-found' and c['flock_holders']==[]
    p=json.loads((HERE/'preservation.json').read_text());assert p['passed'] and p['legacy_registry_restored_byte_exact']
    assert p['dirty_status_unchanged'] and p['stock_prior_candidates_unchanged']
    return dict(passed=True,non_MPI_service_attempts=1,realized_network_isolation=False,
                fresh_getter_observation=True,cross_namespace_handshake_qualified=False,
                MPI_QE_HSE_executed=False,original_hostwide_exclusion='UNPASSED',kind='READ_ONLY_CONSISTENCY')


if __name__=='__main__':print(json.dumps(check(),indent=2))
