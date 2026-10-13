"""Finite real user-unit tests, <=128MiB/16tasks; NO MPI or native QE."""
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import unittest
from unittest.mock import patch
from contracts import *
from controller import run,recover_closed,closed,LEDGER

EVIDENCE=[]


def measured(case,action=None):
    root=create_job(case);result=run(root,action)
    EVIDENCE.append({'case':case,'root':str(root),'action':action,'result':result})
    if not result['owned_unit_closed'] or result['lease_holders_after']:raise AssertionError('owned unit/lease cleanup failed')
    return root,result


class OwnedTest(unittest.TestCase):
    def test_01_real_kernel_limits_typed_two_rank_lease_and_clean_completion(self):
        root,r=measured('normal');self.assertTrue(r['passed']);self.assertEqual(set(r['guard']['ranks']),{'0','1'})
        self.assertEqual(r['hello']['kernel']['memory_max'],str(128*(1<<20)))
        self.assertEqual(r['hello']['kernel']['swap_max'],'0');self.assertEqual(r['hello']['kernel']['tasks_max'],'16')
        self.assertEqual(r['hello']['kernel']['oom_group'],'1')
        self.assertTrue(all(w['invocation']==r['hello']['invocation'] for w in r['guard']['wire']))
        self.assertFalse(r['hostwide_exclusivity_proven'])
        self.assertTrue(r['escrow_exclusive_after_guard_exit'])
        self.assertEqual([s['allocated'] for s in r['guard']['reservations']],[4096,4096])
    def test_02_task_limit_actual_fork_refusal(self):
        root,r=measured('task_limit');self.assertTrue(r['passed'])
        self.assertIn(b'TASK_LIMIT_EAGAIN 1',(root/'logs/workers.log').read_bytes())
        self.assertGreater(r['guard']['kernel_final']['pids_events']['max'],0)
    def test_03_memory_limit_actual_OOM_group_cleanup(self):
        root,r=measured('oom');self.assertFalse(r['passed']);self.assertEqual(r['hello']['kernel']['memory_max'],str(64*(1<<20)))
        events=[s['memory_events'] for s in r['samples']]
        observed=max([e.get('oom_group_kill',0) for e in events],default=0)
        EVIDENCE[-1]['OOM_group_counter_observed']=observed
        self.assertEqual(r['manager_terminal']['Result'],'oom-kill','authoritative invocation OOM result required; exit alone insufficient')
        self.assertEqual(r['manager_terminal']['ExecMainStatus'],'9')
    def test_04_exact_log_cap(self):
        root,r=measured('log_flood');self.assertFalse(r['passed'])
        self.assertIn('exact aggregate worker log cap',r['guard']['reason'])
        self.assertEqual((root/'logs/workers.log').stat().st_size,COMMON['log_max'])
    def test_05_kernel_file_size_limit(self):
        root,r=measured('file_limit');self.assertFalse(r['passed'])
        files=list((root/'out').glob('rank*.data'));self.assertTrue(files)
        self.assertTrue(all(p.stat().st_size<=COMMON['file_max'] for p in files))
        self.assertTrue(any(p.stat().st_size==COMMON['file_max'] for p in files))
    def test_06_manager_runtime_cap_and_user_cancellation(self):
        _,r=measured('hold');self.assertFalse(r['passed']);self.assertLess(r['controller_elapsed_seconds'],7)
        _,r=measured('hold','cancel');self.assertFalse(r['passed']);self.assertIn('owner cancellation',r['guard']['reason'])
    def test_07_guard_crash_and_detached_child_cleanup(self):
        root,r=measured('guard_crash');self.assertFalse(r['passed']);self.assertTrue((root/'CRASH_WITNESS.json').exists())
        root,r=measured('orphan');self.assertFalse(r['passed']);self.assertIn('detached descendant',r['guard']['reason'])
    def test_08_owner_crash_fail_closed_restart_and_verified_recovery(self):
        root=create_job('hold')
        p=subprocess.Popen([sys.executable,str(HERE/'controller.py'),str(root),'owner_crash'],env=manager_env(),
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p.communicate(timeout=8);self.assertEqual(p.returncode,76)
        prior=json.loads(LEDGER.read_text());self.assertEqual(prior['phase'],'RUNNING')
        self.assertEqual(json.loads(REGISTRY.read_text())['phase'],'CGROUP_RUNNING')
        from family_runtime import stale_refusal
        with patch('family_runtime.mpi_inventory',side_effect=AssertionError('foreign inventory must not run')):
            with self.assertRaisesRegex(Refusal,'previous family'):stale_refusal()
        # A released client/lease alone is not sufficient to restart.
        deadline=time.monotonic()+4
        while not closed(prior) and time.monotonic()<deadline:time.sleep(.02)
        self.assertTrue(closed(prior));recover_closed();self.assertEqual(json.loads(LEDGER.read_text())['phase'],'FINISHED')
        self.assertFalse(flock_owner(LOCK))
        self.assertEqual(show(prior['unit'])['LoadState'],'not-found')
        EVIDENCE.append({'case':'owner_crash','root':str(root),'returncode':p.returncode,'record':prior,'cleanup_verified':True})
    def test_09_native_scope_cannot_use_ABI_receipt(self):
        root,r=measured('native_scope');self.assertFalse(r['passed'])
        self.assertIn(b'REGISTER_REFUSED 13',(root/'logs/workers.log').read_bytes())
        self.assertFalse(any(w['action']==2 and w['status']==0 for w in r['guard']['wire']))
    def test_10_source_profile_limits_and_foreign_unit_refusals_before_execution(self):
        root=create_job();job=json.loads((root/'JOB.json').read_text())
        bad=dict(job);bad['kind']='QEF_QE75_NATIVE_FIXTURE';atomic_json(root/'JOB.json',bad)
        with self.assertRaisesRegex(Refusal,'native'):load_job(root)
        atomic_json(root/'JOB.json',job);bad=dict(job);bad['profile_sha256']='0'*64;atomic_json(root/'JOB.json',bad)
        with self.assertRaises(Refusal):load_job(root)
        atomic_json(root/'JOB.json',job);profile=json.loads((root/'PROFILE.json').read_text())
        profile['limits']['memory_max']=1<<30;job['limits']['memory_max']=1<<30;job['profile_sha256']=digest(profile)
        atomic_json(root/'PROFILE.json',profile);atomic_json(root/'JOB.json',job)
        with self.assertRaisesRegex(Refusal,'enlarged'):load_job(root)
        with self.assertRaisesRegex(Refusal,'unowned'):ctl('commander.service','stop')
        with self.assertRaisesRegex(Refusal,'host-wide'):hostwide_gate({'kernel_limits_verified':True})
    def test_11_lease_busy_resource_and_missing_manager_refusals(self):
        root=create_job();fd=os.open(LOCK,os.O_RDWR);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            with self.assertRaisesRegex(Refusal,'lease busy'):run(root)
        finally:os.close(fd)
        root=create_job()
        with patch.object(LinuxGuard,'probe',return_value={'available_bytes':0}):
            with self.assertRaisesRegex(Refusal,'headroom'):run(root)
        with patch('contracts.subprocess.run',side_effect=FileNotFoundError('manager absent')):
            with self.assertRaises(FileNotFoundError):show(json.loads((root/'JOB.json').read_text())['unit'])
    def test_12_invocation_and_kernel_binding_cannot_be_a_boolean(self):
        job={'unit':'r07-owned-'+'a'*32+'.service','limits':dict(COMMON)}
        with self.assertRaisesRegex(Refusal,'inactive'):verify_unit(job,{'verified':True},os.getpid(),'a'*32)
        with self.assertRaisesRegex(Refusal,'invocation'):verify_unit(job,{'Id':job['unit'],'LoadState':'loaded','ActiveState':'active',
                                                                       'InvocationID':'b'*32,'MainPID':str(os.getpid())},os.getpid(),'a'*32)
    def test_13_missing_source_allowlist_cannot_pass_a_matching_digest(self):
        root=create_job();job=json.loads((root/'JOB.json').read_text());job['files']={}
        atomic_json(root/'JOB.json',job)
        with self.assertRaisesRegex(Refusal,'allowlist'):load_job(root)


if __name__=='__main__':
    if len(sys.argv)>1:
        suite=unittest.TestSuite([OwnedTest(name) for name in sys.argv[1:]])
    else:suite=unittest.defaultTestLoader.loadTestsFromTestCase(OwnedTest)
    result=unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)
    report={'passed':result.wasSuccessful(),'methods':result.testsRun,'real_tiny_unit_cases':EVIDENCE,
            'hostwide_inventory_scanned':False,'native_QE_MPI_HSE_executed':False,'kernel_limit_scope':'new transient UID1001 family only',
            'final_owned_ledger':json.loads(LEDGER.read_text()) if LEDGER.exists() else None,'lease_holders':flock_owner(LOCK)}
    target='lease_final_tests.json' if len(sys.argv)>1 else 'tests.json'
    (PRIVATE/target).write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
