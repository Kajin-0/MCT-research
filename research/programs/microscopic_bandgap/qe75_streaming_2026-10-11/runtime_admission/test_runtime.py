"""Real tiny processes/fallocation/IPC; no QE/HSE/MPI. Each wait is bounded."""
from pathlib import Path
import fcntl
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from family_runtime import (HERE,PRIVATE,LOCK,REGISTRY,create_fake_job,verify_job,read_meta,
                            Family,Refusal,live_limits,exact_extent,atomic_json,stale_refusal)
from process_identity import Identity,proc,flock_owner,table,descendants,subreaper,reap
from runtime_client import request,authorize_native_hook

MEASURED=[]


def wait_file(path,seconds=3):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        if path.exists(): return read_meta(path)
        time.sleep(.02)
    raise AssertionError('bounded wait exhausted: '+str(path))


class RuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The dedicated test process adopts its intentionally crashed owners'
        # children, then reaps them; do not leave test zombies to container PID 1.
        subreaper()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=PRIVATE,prefix='test-')
        self.base=Path(self.temp.name);self.children=[]

    def tearDown(self):
        for process,identity in self.children:
            if identity.live(): identity.send(signal.SIGTERM)
            try: process.wait(timeout=4)
            except subprocess.TimeoutExpired:
                identity.send(signal.SIGKILL);process.wait(timeout=2)
            identity.close()
        reap()
        self.temp.cleanup()

    def job(self,name='job',**kw):
        root=self.base/name;create_fake_job(root,**kw);return root

    def start(self,root):
        out=open(root/'owner.log','wb')
        p=subprocess.Popen([sys.executable,str(HERE/'family_runtime.py'),'owner',str(root)],
                           stdout=out,stderr=out,close_fds=True)
        out.close();identity=Identity(p.pid);self.children.append((p,identity));return p,identity

    def finish(self,root,p):
        p.wait(timeout=7);result=wait_file(root/'RESULT.json')
        for member in result.get('members',[])+result.get('survivors',[]):
            try:
                now=proc(member['pid'])
                self.assertFalse(now['start_ticks']==member['start_ticks'] and now['state']!='Z',member)
            except FileNotFoundError: pass
        MEASURED.append({'case':self.id().split('.')[-1],**result})
        self.assertEqual(result['survivors'],[])
        self.assertEqual(flock_owner(LOCK),[])
        return result

    def test_normal_real_family_all_ranks_reservation(self):
        root=self.job();p,i=self.start(root);result=self.finish(root,p)
        self.assertTrue(result['passed'],result)
        self.assertEqual(set(result['rank_registration']),{'0','1'})
        self.assertGreater(result['peak_summed_RSS_bytes'],0)
        self.assertGreater(result['peak_summed_PSS_bytes'],0)
        self.assertGreaterEqual(result['minimum_free_disk_bytes'],10*(1<<30))
        for reserved in result['reservations']:
            path=Path(reserved['path']);st=path.stat()
            self.assertEqual(st.st_size,reserved['bytes']);self.assertGreaterEqual(st.st_blocks*512,st.st_size)
        with self.assertRaisesRegex(Refusal,'reused'): verify_job(root)

    def test_timeout_term_ignored_then_identity_safe_kill(self):
        root=self.job(scenario='ignore_term',wall=.6);p,i=self.start(root);result=self.finish(root,p)
        self.assertFalse(result['passed']);self.assertIn('wall cap',result['reason'])
        self.assertIn(signal.SIGKILL,[entry['signal'] for entry in result['signals']])

    def test_owner_cancellation(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root)
        wait_file(root/'out/authorized0.json');i.send(signal.SIGTERM)
        result=self.finish(root,p);self.assertIn('cancellation',result['reason'])

    def test_owner_sigkill_guardian_cleans_and_releases(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root)
        wait_file(root/'out/authorized0.json');i.send(signal.SIGKILL);p.wait(timeout=1)
        result=wait_file(root/'RESULT.json',4)
        deadline=time.monotonic()+1
        while flock_owner(LOCK) and time.monotonic()<deadline: time.sleep(.02)
        self.assertFalse(result['passed']);self.assertEqual(result['survivors'],[])
        self.assertEqual(flock_owner(LOCK),[])
        reap()
        MEASURED.append({'case':self.id().split('.')[-1],**result})
        # Fresh root can acquire the automatically released lease.
        new=self.job('after-crash');p2,i2=self.start(new);self.assertTrue(self.finish(new,p2)['passed'])

    def test_guardian_sigkill_owner_fallback(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root)
        wait_file(root/'out/authorized0.json');ticket=read_meta(root/'LEASE_ENDPOINT.json')
        guardian=Identity(ticket['guardian']['pid'])
        guardian.send(signal.SIGKILL);guardian.close()
        result=self.finish(root,p);self.assertIn('owner fallback',result['reason'])

    def test_detached_descendant_cannot_escape(self):
        root=self.job(scenario='detach');p,i=self.start(root);result=self.finish(root,p)
        self.assertFalse(result['passed']);self.assertIn('orphan',result['reason'])
        self.assertTrue((root/'out/detached_child.json').exists())
        child=read_meta(root/'out/detached_child.json')
        self.assertIn(child['pid'],[row['pid'] for row in result['members']])

    def test_worker_failure(self):
        root=self.job(scenario='fail');p,i=self.start(root);result=self.finish(root,p)
        self.assertFalse(result['passed']);self.assertIn('failure',result['reason'])

    def test_exclusive_lease_refuses_second_owner(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root)
        wait_file(root/'out/authorized0.json')
        other=self.job('other');p2,i2=self.start(other);p2.wait(timeout=2)
        result=wait_file(other/'RESULT.json');self.assertIn('exclusive lease',result['reason'])
        self.assertTrue(i.live());i.send(signal.SIGTERM);self.finish(root,p)

    def test_outside_peer_boolean_and_forged_monitor_do_not_authorize(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root)
        wait_file(root/'out/authorized0.json')
        (root/'MONITOR.json').write_text(json.dumps({'runtime_authorized':True,'ranks':[0,1],'pid':os.getpid()}))
        with self.assertRaisesRegex(Refusal,'outside owned'): request(root,'authorize')
        with self.assertRaisesRegex(Refusal,'synthetic'): authorize_native_hook(root,'0'*64,'authorize')
        i.send(signal.SIGTERM);self.finish(root,p)

    def test_reservation_collision_keeps_foreign_file(self):
        root=self.job();foreign=root/'scratch/rank1.stream';foreign.write_bytes(b'FOREIGN_KEEP')
        p,i=self.start(root);result=self.finish(root,p)
        self.assertFalse(result['passed']);self.assertEqual(foreign.read_bytes(),b'FOREIGN_KEEP')
        self.assertFalse((root/'scratch/rank0.stream').exists())

    def test_predicate_faults_stop_owned_real_processes(self):
        for fault,needle in [('mem','RAM reserve'),('disk','disk reserve'),('probe','probe'),('envelope','envelope')]:
            with self.subTest(fault=fault):
                root=self.job(fault,fault=fault);p,i=self.start(root);result=self.finish(root,p)
                self.assertFalse(result['passed']);self.assertIn(needle,result['reason'])

    def test_stricter_rss_actual_stop(self):
        root=self.job(rss_cap=1);p,i=self.start(root);result=self.finish(root,p)
        self.assertFalse(result['passed']);self.assertIn('RSS cap',result['reason'])

    def test_exact_600s_and_resource_boundaries(self):
        info={'available_bytes':10*(1<<30)}
        live_limits(info,4*(1<<30),12*(1<<30),599.999999)
        with self.assertRaisesRegex(Refusal,'wall'): live_limits(info,4*(1<<30),12*(1<<30),600.)
        with self.assertRaises(Refusal): live_limits(info,4*(1<<30),12*(1<<30)+1,0.)
        with self.assertRaises(Refusal): live_limits(info,4*(1<<30)-1,0,0.)
        with self.assertRaises(Refusal): live_limits({'available_bytes':10*(1<<30)-1},4*(1<<30),0,0.)
        self.assertEqual(exact_extent([524288,352,8]),23622320128)
        with self.assertRaises(Refusal): exact_extent([2**62,2,2])

    def test_incompatible_job_and_native_promotion_refused(self):
        root=self.job();job=read_meta(root/'JOB.json');job['rank_bytes'][0]+=1
        (root/'JOB.json').write_text(json.dumps(job))
        with self.assertRaisesRegex(Refusal,'extents'): verify_job(root)
        job['kind']='QEF_QE75_NATIVE_FIXTURE';job['native_qualified']=True
        (root/'JOB.json').write_text(json.dumps(job))
        with self.assertRaisesRegex(Refusal,'BLOCKED'): verify_job(root)

    def test_stale_identity_refuses_signal_and_unrelated_sentinel_survives_timeout(self):
        sentinel=subprocess.Popen([sys.executable,'-c','import time; time.sleep(8)'])
        identity=Identity(sentinel.pid);self.children.append((sentinel,identity))
        changed=dict(proc(sentinel.pid),start_ticks=identity.start_ticks+1)
        with mock.patch('process_identity.proc',return_value=changed), mock.patch('signal.pidfd_send_signal') as send:
            identity.send(signal.SIGKILL)
            self.assertFalse(identity.live())
            send.assert_not_called()
        root=self.job(scenario='ignore_term',wall=.6);p,i=self.start(root)
        result=self.finish(root,p)
        self.assertTrue(identity.live());self.assertNotIn(sentinel.pid,[row['pid'] for row in result['members']])

    def test_completed_ticket_cannot_authorize(self):
        root=self.job();p,i=self.start(root);self.finish(root,p)
        with self.assertRaises((Refusal,OSError)): request(root,'authorize')

    def test_double_crash_fences_restart_until_explicit_test_cleanup(self):
        root=self.job(scenario='hold',wall=4);p,i=self.start(root)
        wait_file(root/'out/authorized0.json');wait_file(root/'out/authorized1.json')
        known=[Identity(pid) for pid in descendants(p.pid,table())]
        guardian_pid=read_meta(root/'LEASE_ENDPOINT.json')['guardian']['pid']
        guardian=next(item for item in known if item.pid==guardian_pid)
        try:
            # Freeze the two cleanup authorities before crashing both. This
            # deliberately defeats automatic cleanup; only known test pidfds
            # below may clean the retained test workers.
            i.send(signal.SIGSTOP);guardian.send(signal.SIGSTOP)
            deadline=time.monotonic()+1
            while time.monotonic()<deadline:
                if proc(p.pid)['state']=='T' and proc(guardian_pid)['state']=='T': break
                time.sleep(.01)
            else: self.fail('cleanup authorities did not stop')
            guardian.send(signal.SIGKILL);i.send(signal.SIGKILL);p.wait(timeout=1)
            deadline=time.monotonic()+1
            while flock_owner(LOCK) and time.monotonic()<deadline: time.sleep(.01)
            self.assertEqual(flock_owner(LOCK),[])
            with self.assertRaisesRegex(Refusal,'not durably closed'): stale_refusal()
            other=self.job('refused-after-double-crash');p2,i2=self.start(other);p2.wait(timeout=2)
            refusal=wait_file(other/'RESULT.json');self.assertIn('not durably closed',refusal['reason'])
            MEASURED.append({'case':self.id().split('.')[-1],'expected_refusal':refusal,
                            'kernel_lease_released':True,'automatic_cleanup_claimed':False})
        finally:
            for item in known: item.send(signal.SIGKILL)
            deadline=time.monotonic()+2
            while any(item.live() for item in known) and time.monotonic()<deadline:
                reap();time.sleep(.01)
            reap()
            self.assertFalse(any(item.live() for item in known))
            # Test-only explicit reconciliation, not a production auto-restart.
            self.assertEqual(read_meta(REGISTRY)['job'],str(root))
            fd=os.open(LOCK,os.O_RDWR)
            try:
                fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
                atomic_json(REGISTRY,{'version':1,'job':str(root),'phase':'FINISHED','members':[],
                                     'test_only_explicit_pidfd_cleanup':True})
            finally: os.close(fd)
            for item in known: item.close()


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeTest)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    (PRIVATE/'test_runtime.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
      'results':MEASURED,'native_PW_HSE_MPI_executed':False},indent=2)+'\n')
    sys.exit(0 if result.wasSuccessful() else 1)
